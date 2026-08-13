# ⭐ **`cnob_py_struc_pgm.md` (Version 1.0)**
### *Python & C++ Implementation Blueprint for the CnOB Primitive*
### *Aligned with 20.40.030 v2.0, cnob_software_architecture.md, cnob_srob_comm_architect.md*

**Schema authority:** This document owns the **normative v1** field schemas for `cnob_constraint_map` and `cnob_residue` (Q6). Testbench expected blocks SHALL match.

---

# **1. CnOB’s Role in the Pipeline**

1. TPU → SOB → **SROB** → **CnOB** → SmOB → … → routing / IdOB

CnOB is responsible for:

- loading **CnOB-owned** support YAMLs only
- reading **SROB-owned TP fields** (not `srob_*.yaml`)
- encoding **C1–C7** constraint families
- emitting missing-slot, underspecification, conflict signals
- refining structural-importance → constraint-importance
- forming **`cnob_constraint_map`** (full — Q1)
- producing **`cnob_residue{}`**
- producing **`cnob_audit_record{}`**
- hashing constraint outputs for exact addressing / replay
- preserving upstream fields (read-only)
- referencing **SROB segment ids** (Q2)

CnOB does **not**: re-normalize structure; re-lex text; invent tag types; enforce constraints; resolve meaning/referents; modify semantic_core / routing envelopes / identity.

---

# **2. Public API**

```python
cnob = CnOB(tp_input)
cnob.process()
```

### **CnOB-written fields**

- `TP.structural.cnob_constraint_map`
- `TP.structural.cnob_residue`
- `TP.metadata.cnob_audit_record`
- optional diagnostic-only keys

---

# **3. Intake Model**

SROB fields required for normal operation:

- `structural.srob_structural_map`
- `structural.srob_residue` (preferred)

Fallback: if SROB absent and isolation mode, may read SOB fields — **not** default Path-A.

All non-CnOB fields are **read-only**.

---

# **4. Deterministic Rule Ordering**

1. Read TP (post-SROB)
2. Load CnOB YAMLs
3. Read `srob_structural_map` / `srob_residue`
4. Encode C1–C7 (`cnob_constraint_rules.yaml`)
5. Apply missing-slot / underspec rules
6. Apply conflict rules
7. Apply constraint-importance rules (multi-label OK)
8. Canonical-order all lists (family, rule_id, segment_id)
9. Build **full** `cnob_constraint_map`
10. Build `cnob_residue`
11. Compute hashes
12. Build `cnob_audit_record`
13. Emit TP

---

# **5. Normative v1 Schemas**

## **5.1 Constraint entry**

```
constraint_entry:
  family: C1 | C2 | C3 | C4 | C5 | C6 | C7   # required
  rule_id: string                            # required
  segment_ids: []                            # optional; SROB ids
  payload: {}                                # optional small structured notes
```

## **5.2 `TP.structural.cnob_constraint_map` (full every run — Q1)**

```
cnob_constraint_map:
  constraint_families:
    C1: []    # list of constraint_entry
    C2: []
    C3: []
    C4: []
    C5: []
    C6: []
    C7: []
  missing_slot_signals: []      # see §5.3 signal object
  underspecification_markers: []
  conflict_indicators: []
  constraint_importance: []     # see §5.4
  discourse_constraints: []     # optional normalized discourse→constraint notes
  lineage_constraints: []       # optional C5-detailed; may mirror C5 entries
  routing_constraints: []       # optional C7-detailed
  policy_constraints: []        # optional; empty in v1 thin
```

Empty lists are valid (Q4). Keys C1–C7 **must** be present.

## **5.3 Signal object (missing / underspec / conflict)**

```
signal:
  id: string              # e.g. miss_001, conf_001
  kind: missing_slot | underspecification | conflict
  rule_id: string
  segment_ids: []         # SROB ids when local
  participants: []        # optional; tag ids or modality labels for conflicts
  note: string            # optional short machine note; not free meaning prose
```

## **5.4 Constraint-importance object**

```
constraint_importance_item:
  labels: []              # e.g. [constraint_anchor, gap_high]
  segment_ids: []         # optional
  source: structural | gap | conflict | mixed
```

Multiple labels allowed (Q3).

## **5.5 `TP.structural.cnob_residue`**

```
cnob_residue:
  missing_slot_signals: []       # may mirror map or be the sole copy; v1: mirror map lists
  underspecification_markers: []
  conflict_indicators: []
  constraint_importance: []
  constraint_family_summary: []  # optional list of family ids that are non-empty
  disagreement_flags: []
  override_flags: []
  constraint_residue_hash: string   # required on success
  # optional diagnostics:
  # rule_fire_log: []
```

**v1 rule:** Map holds the authoritative structured view; residue **must** include the gap/conflict/importance arrays and **`constraint_residue_hash`**. Duplicating the three signal arrays into residue is required for SmOB-friendly consumption (parallel to SROB residue pattern).

## **5.6 Hash (Q7)**

- Serialize canonical `cnob_constraint_map` (sorted keys / ordered lists) + residue signal arrays (excluding the hash field itself)
- `constraint_residue_hash = sha256(...).hexdigest()[:16]` (or project-standard length matching SOB/SROB)
- Audit may also store `cnob_constraint_map_hash`

## **5.7 Audit record**

```
cnob_audit_record:
  support_yaml_load_status: ok | partial | fail
  family_encoding_decisions: []
  gap_decisions: []
  conflict_decisions: []
  importance_decisions: []
  provenance_lineage:
    origin: CnOB
    last_update: CnOB
  cnob_constraint_map_hash: string
  constraint_residue_hash: string
  timestamp: iso8601
```

---

# **6. v1 Rule Behaviors (enough for goldens)**

These behaviors are **normative for thin v1** so `cnob_testbench.yaml` can lock expected blocks. YAML may encode the same rules explicitly.

### **6.1 Always-on structural families (when segments exist)**

| Condition | Emit |
|-----------|------|
| `len(segments) >= 1` | C1 entry `rule_id: c1_segment_exists` |
| `len(segments) >= 2` | C3 entry `rule_id: c3_multi_segment_order` |
| any `type == list_item` | C4 entry `rule_id: c4_list_boundary` with those segment_ids |
| any list_item with `parent_id` set | C2 entry `rule_id: c2_list_parent_child` |
| any segment with stable id | C5 entry `rule_id: c5_segment_id_lineage` (once per TP) |

### **6.2 Tag-driven**

| Condition | Emit |
|-----------|------|
| any operator present | C1 entry `rule_id: c1_operator_present` |
| any lexical_constraints tag present | C7 entry `rule_id: c7_constraint_hint_present` |
| discourse_flags non-empty | discourse_constraints note + C2/C3 as applicable `rule_id: c2_discourse_present` |

### **6.3 Gaps**

| Condition | Emit |
|-----------|------|
| segment text empty/whitespace | missing_slot `rule_id: miss_empty_text` |
| modality interrogative and operators empty | underspecification `rule_id: under_question_no_operator` |
| lexical_constraints non-empty and operators empty | underspecification `rule_id: under_constraint_no_operator` |

### **6.4 Conflicts (Q8)**

| Condition | Emit |
|-----------|------|
| both `precision` and `conciseness` in lexical_constraints (string match on tag id or suffix) | conflict `rule_id: conf_precision_vs_conciseness` |
| both imperative and interrogative modalities present across segments | conflict `rule_id: conf_imperative_vs_interrogative` |

### **6.5 Importance**

| Condition | Labels |
|-----------|--------|
| structural_importance contains `anchor_like` | `constraint_anchor` |
| any missing_slot | `gap_high` |
| any conflict | `conflict_high` |
| list_lead on segment | `order_sensitive` |

---

# **7. Forbidden Behavior**

CnOB must not:

- load `srob_*.yaml` or `sob_*.yaml`
- re-segment or renumber segment ids
- invent operators/domains/tones/constraint **types** not on TP
- fill missing content as meaning
- enforce constraints on TP text
- evaluate truth or assign stance-as-conclusion
- resolve referent identity
- consume routing_metadata / Pipeline-B ΔH% envelopes
- write outside CnOB-owned fields
- require other primitives to read diagnostic-only metadata

---

# **8. Implementation Skeleton (Python)**

```python
class CnOB:
    def __init__(self, tp_input):
        self.tp = tp_input

    def process(self):
        rules = self._load_support_yamls()
        srob_map = self._read_srob_map(self.tp)
        srob_residue = self._read_srob_residue(self.tp)

        families = self._encode_families(srob_map, srob_residue, rules)
        missing, under = self._apply_gap_rules(srob_map, srob_residue, rules)
        conflicts = self._apply_conflict_rules(srob_map, srob_residue, rules)
        importance = self._apply_importance(
            srob_map, missing, under, conflicts, rules
        )

        cnob_map = self._build_constraint_map(
            families, missing, under, conflicts, importance
        )
        residue = self._build_residue(cnob_map, missing, under, conflicts, importance)
        audit = self._build_audit_record(cnob_map, residue)

        self.tp.setdefault("structural", {})
        self.tp["structural"]["cnob_constraint_map"] = cnob_map
        self.tp["structural"]["cnob_residue"] = residue
        self.tp.setdefault("metadata", {})
        self.tp["metadata"]["cnob_audit_record"] = audit
        return self.tp
```

---

# **9. Downstream Consumption**

| Primitive | Consumes | Purpose |
|-----------|----------|--------|
| **SmOB** | cnob map/residue | semantic-adjacent cues from constraints/gaps |
| **SSG/TR/RB** | residue hash + routing_constraints / C7 | exact addressing + eligibility features |
| **ISc** | constraint features | scoring |
| **IdOB** | gaps/conflicts/importance as rails | reduced search; content often TPU |

---

# **10. Locked Policies (Q1–Q8)**

| ID | Topic | Lock |
|----|--------|------|
| **Q1** | Map style | Full `cnob_constraint_map` every run |
| **Q2** | Segment ids | Reference SROB ids; do not renumber |
| **Q3** | Importance | Multi-label allowed |
| **Q4** | Empty | Empty family lists OK; keys present |
| **Q5** | Input | Prefer/require SROB in full Path-A |
| **Q6** | Schema | **This document** |
| **Q7** | Hash | Canonical map + signal arrays |
| **Q8** | Conflict example | precision vs conciseness |

---

# **11. Testbench contract (normative intent)**

- Inputs: **SROB-shaped** TP (`structural.srob_*`), analogous to SROB tests using SOB-shaped inputs
- Expected: `cnob_constraint_map` + `cnob_residue` per §5; hash may be checked as present or exact if serialization frozen
- Minimum scenarios for a first `cnob_testbench.yaml`:
  1. Single declarative segment + operator → C1 exists + operator rules; no conflict
  2. List with parent/child → C2/C4
  3. Empty text segment → missing_slot
  4. Interrogative, no operator → underspecification
  5. precision + conciseness constraints → conflict Q8
  6. anchor_like importance → constraint_anchor label

---

# ⭐ **End of Document — `cnob_py_struc_pgm.md` (Version 1.0)**

---
