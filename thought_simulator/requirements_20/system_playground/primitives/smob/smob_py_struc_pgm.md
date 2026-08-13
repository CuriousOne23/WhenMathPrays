# ⭐ **`smob_py_struc_pgm.md` (Version 1.0)**
### *Python & C++ Implementation Blueprint for the SmOB Primitive*
### *Aligned with 20.40.040 v2.0, smob_software_architecture.md, smob_cnob_comm_architect.md*

**Schema authority:** Normative v1 shapes for `smob_cue_map` and `smob_residue` (R5).  
**Coupling authority:** CnOB↔SmOB is a **TP surface + residue contract** — `smob_cnob_comm_architect.md` §2.6 (R4).

---

# **1. SmOB’s Role in the Pipeline**

1. TPU → SOB → SROB → **CnOB** → **SmOB** → SSG → TR / RB / IdOB

SmOB is responsible for:

- loading **SmOB-owned** support YAMLs only
- reading **CnOB-owned TP fields** (prefer; not `cnob_*.yaml`)
- **Job 1:** pre-semantic / semantic-adjacent cue extraction
- discourse-adjacent normalization
- constraint-importance → semantic-adjacent importance
- **Job 2:** TR-input vector + pre-semantic residue hash
- optional change signals from **allowed** fields only
- writing `smob_cue_map`, `smob_residue`, `smob_audit_record`

SmOB does **not**: deep meaning, truth, stance-as-conclusion, referent identity, generative fill, load upstream OB YAMLs, overwrite CnOB/SROB/SOB, consume routing_metadata / Pipeline-B ΔH% envelopes.

---

# **2. Public API**

```python
smob = SmOB(tp_input)
smob.process()
```

### **SmOB-written fields**

- `TP.structural.smob_cue_map`
- `TP.structural.smob_residue`
- `TP.metadata.smob_audit_record`
- optional diagnostic-only keys

---

# **3. Intake Model and Coupling (R4)**

Required for normal Path-A:

- `structural.cnob_constraint_map`
- `structural.cnob_residue` (preferred)

Optional secondary: `srob_structural_map` (modality, discourse_flags).

### **3.1 Normative coupling rules**

1. SmOB **SHALL NOT** load `cnob_*.yaml`, `srob_*.yaml`, or `sob_*.yaml`.
2. SmOB **SHALL NOT** require hierarchical dictionary sync with CnOB support files.
3. SmOB **SHALL** depend on **CnOB TP field names and residue conventions**.
4. Rule conditions **SHALL** use explicit predicates mappable to those fields.
5. Missing expected CnOB fields → **handoff/support defect**, not invent-inside-SmOB.

**Debug order:** TP(CnOB) → rule `if:` → SmOB encode/compress.

---

# **4. Deterministic Rule Ordering (R9)**

1. Read TP (post-CnOB)
2. Load SmOB YAMLs only
3. Read `cnob_constraint_map` / `cnob_residue`
4. **Job 1:** extract cues (`smob_cue_rules.yaml`)
5. Normalize discourse-adjacent cues
6. Apply importance-adjacent rules
7. Canonical-order all cue lists
8. **Job 2:** form `tr_input_cues` (`smob_compress_rules.yaml`)
9. Compute `presemantic_residue_hash`
10. Optional `delta_h_semantic_adjacent` from allowed fields
11. Build full `smob_cue_map`
12. Build `smob_residue`
13. Build `smob_audit_record`
14. Emit TP

---

# **5. Normative v1 Schemas**

## **5.1 Cue entry**

```
cue_entry:
  family: string          # e.g. conflict_adjacent, modality, routing_semantic
  cue_id: string          # e.g. conf_adjacent_present
  rule_id: string
  segment_ids: []         # optional; referenced ids only
  source: cnob | srob | mixed
  note: string            # optional machine note
```

## **5.2 `TP.structural.smob_cue_map` (full every run — R1)**

```
smob_cue_map:
  semantic_adjacent_cues: []
  modality_cues: []
  affect_markers: []                    # may be empty v1 (R7)
  conflict_adjacent_signals: []
  underspecification_adjacent_signals: []
  constraint_importance_adjacent_signals: []
  discourse_adjacent_cues: []
  routing_semantic_cues: []
  delta_h_semantic_adjacent: []         # optional; from allowed fields only
```

Each list holds `cue_entry` objects (or empty).

## **5.3 `TP.structural.smob_residue`**

```
smob_residue:
  semantic_adjacent_cues: []            # mirror or compact ids
  conflict_adjacent_signals: []
  underspecification_adjacent_signals: []
  constraint_importance_adjacent_signals: []
  tr_input_cues: []                     # ordered vector (R8)
  presemantic_residue_hash: string      # required on success
  cue_family_summary: []                # non-empty family names
  disagreement_flags: []
  override_flags: []
```

**v1:** Residue **must** include `tr_input_cues` and `presemantic_residue_hash`. Cue signal arrays may mirror the map for SSG-friendly consumption.

## **5.4 TR-input vector (R8) — thin v1 slots**

Fixed order (string or small object per slot; empty string if inactive):

| Index | Slot name | v1 fill rule |
|-------|-----------|--------------|
| 0 | `modality` | dominant modality cue id or `""` |
| 1 | `conflict` | `conflict_adjacent` if any conflict else `""` |
| 2 | `underspec` | `underspec_adjacent` if any gap/underspec else `""` |
| 3 | `importance` | first importance-adjacent label or `""` |
| 4 | `routing` | `routing_cue` if C7/routing cues else `""` |
| 5 | `discourse` | first discourse-adjacent id or `""` |

Implementations MAY represent `tr_input_cues` as a list of `{slot, value}` in this order.

## **5.5 Hash (R6)**

- Canonical serialize: `smob_cue_map` (sorted) + residue signal arrays **excluding** the hash field itself + `tr_input_cues`
- `presemantic_residue_hash = sha256(...).hexdigest()[:16]` (or project standard matching CnOB/SROB)

## **5.6 Audit record**

```
smob_audit_record:
  support_yaml_load_status: ok | partial | fail
  cue_decisions: []
  importance_decisions: []
  compress_decisions: []
  provenance_lineage:
    origin: SmOB
    last_update: SmOB
  smob_cue_map_hash: string
  presemantic_residue_hash: string
  timestamp: iso8601
```

---

# **6. v1 Rule Behaviors (enough for goldens)**

### **6.1 Cue extraction (Job 1)**

| Condition (on CnOB TP) | Emit |
|------------------------|------|
| any `conflict_indicators` | `conflict_adjacent_signals`: cue_id `conflict_adjacent`, rule `cue_conflict_present` |
| any `missing_slot_signals` | underspec-adjacent: `gap_adjacent`, rule `cue_missing_slot` |
| any `underspecification_markers` | underspec-adjacent: `underspec_adjacent`, rule `cue_underspec` |
| any `constraint_importance` | importance-adjacent: copy/map labels, rule `cue_importance` |
| C7 family non-empty OR routing_constraints non-empty | `routing_semantic_cues`: `routing_cue`, rule `cue_routing` |
| SROB modalities present (secondary) | `modality_cues` from unique modalities |
| CnOB discourse_constraints or SROB discourse_flags | `discourse_adjacent_cues` |

Also push a compact id into `semantic_adjacent_cues` for each fired family (canonical order).

### **6.2 Importance-adjacent**

| CnOB label | SmOB adjacent label |
|------------|---------------------|
| `gap_high` | `sa_gap_high` |
| `conflict_high` | `sa_conflict_high` |
| `constraint_anchor` | `sa_anchor` |
| `order_sensitive` | `sa_order_sensitive` |

### **6.3 Compression (Job 2)**

Fill TR slots per §5.4; always compute `presemantic_residue_hash`.

---

# **7. Forbidden Behavior**

SmOB must not:

- load upstream OB YAML packs
- require dictionary sync with CnOB rule trees
- re-emit C1–C7 as its primary owned product (may *reference* them in cues)
- invent meaning, truth, stance conclusions, or referents
- generative-fill missing content
- consume routing_metadata / Pipeline-B ΔH% envelopes
- write outside SmOB-owned fields
- require other primitives to read diagnostic-only metadata

---

# **8. Implementation Skeleton (Python)**

```python
class SmOB:
    def __init__(self, tp_input):
        self.tp = tp_input

    def process(self):
        rules = self._load_support_yamls()
        cnob_map = self._read_cnob_map(self.tp)
        cnob_residue = self._read_cnob_residue(self.tp)

        cues = self._extract_cues(cnob_map, cnob_residue, rules)      # Job 1
        cues = self._normalize_discourse(cues, rules)
        cues = self._apply_importance(cues, cnob_map, rules)

        tr = self._form_tr_vector(cues, rules)                         # Job 2
        body = self._build_cue_map(cues)
        residue = self._build_residue(body, tr)
        audit = self._build_audit_record(body, residue)

        self.tp.setdefault("structural", {})
        self.tp["structural"]["smob_cue_map"] = body
        self.tp["structural"]["smob_residue"] = residue
        self.tp.setdefault("metadata", {})
        self.tp["metadata"]["smob_audit_record"] = audit
        return self.tp
```

---

# **9. Downstream Consumption**

| Primitive | Consumes | Purpose |
|-----------|----------|--------|
| **SSG** | smob_cue_map / residue | Sole pre-semantic input |
| **TR / RB** | tr_input_cues + presemantic_residue_hash | Exact addressing / eligibility |
| **IdOB** | cues / importance-adjacent | Reduced search rails |
| **ISc** | cue features | Scoring |

---

# **10. Locked Policies (R1–R9)**

| ID | Topic | Lock |
|----|--------|------|
| **R1** | Map style | Full `smob_cue_map` every run |
| **R2** | Segment ids | Reference only |
| **R3** | Input | Prefer/require CnOB in full Path-A |
| **R4** | Coupling | Surface + residue contract |
| **R5** | Schema | **This document** |
| **R6** | Hash | Canonical cue map + signals + TR vector |
| **R7** | Affect | Thin/optional v1 |
| **R8** | TR vector | Fixed ordered slots §5.4 |
| **R9** | Order | Job 1 then Job 2 |

---

# **11. Testbench contract**

- Inputs: **CnOB-shaped** TP (`structural.cnob_*`)
- Expected: schemas §5; hashes may be `present`-normalized
- Minimum scenarios:
  1. Clean C1/C5 only → modality optional; empty conflict/underspec; hash present
  2. CnOB conflict present → conflict_adjacent + TR conflict slot
  3. missing_slot → gap_adjacent / underspec path
  4. underspec marker → underspec_adjacent
  5. C7 non-empty → routing_semantic_cues
  6. constraint_importance gap_high → sa_gap_high

---

# ⭐ **End of Document — `smob_py_struc_pgm.md` (Version 1.0)**

---
