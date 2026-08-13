# ⭐ **`srob_py_struc_pgm.md` (Version 1.1)**
### *Python & C++ Implementation Blueprint for the SROB Primitive*
### *Aligned with 20.40.020 v2.0, srob_software_architecture.md, srob_sob_comm_architect.md, 20.105.*, 20.15*

**Schema authority:** This document owns the **normative v1** field schemas for `srob_structural_map` and `srob_residue` (P6). Architecture points here; testbench expected blocks must match this schema.

---

# **1. SROB’s Role in the Pipeline**

SROB is the **structural refinement** primitive of Path-A.  
It immediately follows SOB:

1. **TPU** — authoritative commit (as applicable upstream)
2. **SOB** — lexical tagging + coarse structural residue
3. **SROB** — normalize structure + sharpen tags within SOB families
4. **CnOB** — constraint-oriented consumption of refined structure/tags
5. **SmOB** → … → scoring / routing / identity / commit

SROB is responsible for:

- loading **SROB-owned** support YAMLs only
- validating **SOB↔SROB vocab coupling** (no disjoint maps)
- reading **SOB-owned TP fields** (not `sob_*.yaml`)
- **structure normalization** (lists, tables, blocks, boundaries, nesting)
- **tag sharpening** inside SOB operator/domain/tone/constraint families
- discourse flag canonicalization (when SOB flags present)
- positional structural-importance labels
- forming **`srob_structural_map`** (full refined map — P2)
- producing **`srob_residue{}`**
- producing **`srob_audit_record{}`**
- optional diagnostic-only metadata
- preserving upstream / SOB / meaning fields (read-only)
- **preserving SOB segment ids** through refine (P1)

SROB consumes:

- TP after SOB, including:
  - `structural.sob_structural_map`
  - `structural.sob_residue`
  - `metadata.sob_audit_record` (read-only, for lineage/debug)
  - other TP envelopes read-only as allowed by 20.40.020
- SROB YAMLs:
  - `srob_normalize_rules.yaml`
  - `srob_sharpen_maps.yaml`
  - `srob_importance_rules.yaml`

SROB produces:

- `structural.srob_structural_map`
- `structural.srob_residue`
- `metadata.srob_audit_record`

SROB does **not**:

- load SOB lexical dictionaries or re-tag raw text as a second SOB
- invent new hint types outside SOB field space
- generate semantic meaning or enforce constraints
- interpret identity or continuity as owner
- modify semantic_core, intake/context fields, routing, freeze, identity metadata
- route directly to semantic OBs

SROB is deterministic, bounded, replay-safe, and the **sole structural-refinement authority** immediately after SOB.

---

# **2. Public API (Python & C++)**

```python
srob = SROB(tp_input)
srob.process()
```

SROB SHALL populate or update only the following TP envelopes/metadata:

### **SROB-written fields**

- `TP.structural.srob_structural_map`
- `TP.structural.srob_residue`
- `TP.metadata.srob_audit_record`
- optional diagnostic-only keys under SROB ownership (not required for other primitives)

### Required method

```python
def process(self):
    # load SROB YAMLs
    # validate sharpen map parents against SOB coarse vocab
    # read SOB map/residue from TP
    # normalize structure + boundaries (preserve segment ids)
    # sharpen tags per multi_refinement_policy
    # canonicalize discourse flags
    # apply importance rules (multi-label OK)
    # form srob_structural_map (full)
    # form srob_residue
    # produce audit record
    # return updated TP
```

---

# **3. Intake Model (Single Input)**

SROB receives **one** bounded input: the TP stream after SOB.

## **3.1 TP Input**

SROB reads (read-only except SROB-owned writes):

- SOB structural map and residue (required for normal operation)
- context / discourse-adjacent fields already on TP when applicable
- provenance / audit from SOB (read-only)
- structural metadata needed for normalize/sharpen

SROB treats all non-SROB-owned fields as **read-only**.

**Sufficiency:** Missing coarse structure or tags needed for a duty ⇒ SOB gap, not a reason to load `sob_operators.yaml` inside SROB.

---

# **4. Deterministic Rule Ordering**

SROB must apply operations in **exact order**:

1. Read TP (post-SOB)
2. Load SROB support YAMLs
3. Validate vocab coupling (sharpen maps ↔ SOB coarse category set)
4. Read `sob_structural_map` / `sob_residue`
5. Normalize structure (lists/tables/blocks/unit consistency); **preserve SOB segment ids** (P1)
6. Resolve boundaries / nesting (still preserve ids)
7. Sharpen tags within SOB families per **§5.4 multi-refinement policy** (P3)
8. Canonicalize discourse flags present on SOB residue
9. Apply structural-importance rules (**multi-label allowed** — P5)
10. Build **full** `srob_structural_map` (P2)
11. Build `srob_residue`
12. Build `srob_audit_record`
13. Emit deterministic TP + SROB fields

This ordering ensures:

- replay determinism
- Python/C++ parity
- stable integration with CnOB, SmOB, ISc, TR, RB, IdOB

---

# **5. Vocab Coupling and Sharpening**

### **5.1 Coupling rules**

- Parent keys in `srob_sharpen_maps.yaml` MUST be exact SOB coarse category strings
- Fine ids MUST be hierarchical: `parent.child`
- Illegal parent at load/test ⇒ hard failure (`SROB_MAP_DESYNC` or equivalent)
- **No sharpen without SOB tag**

### **5.2 Families in scope**

- operators
- domains
- tones
- constraints

Modality: **SOB-final** by default (unless a boundary/unit change forces modality to move with the unit).

### **5.3 Growth**

- Start minimal (pass-through maps OK)
- Grow by adding children under existing parents or adding SOB coarse tags first
- Never introduce SROB-only top-level categories

### **5.4 Multi-refinement policy (P3) — NORMATIVE**

For a coarse tag present on the TP and a matching parent in the sharpen map:

| Map state | Primary tag field behavior |
|-----------|----------------------------|
| `refinements: []` or parent absent | **Pass-through** coarse id |
| Exactly **one** child | May emit that single fine id as the refined tag |
| **Multiple** children and **no** matching `when` | **Pass-through coarse** on primary tag fields; do **not** auto-emit all children |
| Multiple children with `when` (future) | First matching `when` wins; else pass-through |

Optional diagnostic (residue / audit only, not required for CnOB):

- `available_refinements[]` — list of fine ids under the parent when multi-child pass-through occurred

### **5.5 Unmapped coarse policy (P4) — NORMATIVE**

If SOB emits a coarse id with **no** parent key in the sharpen map:

- **Pass-through** the coarse id on primary tag fields
- Optional diagnostic: `unmapped_coarse[]` entry in residue

---

# **6. Structure Normalization**

SROB normalizes using `srob_normalize_rules.yaml`:

- list depth, ordering, parent indices, **stable item ids (preserve SOB ids — P1)**
- table header/body/cells (text content unchanged)
- code/math blocks typed; content unchanged
- boundary and continuation attachment
- consistent unit types across the TP

SROB does **not** invent structural units that SOB never proposed (default: no surprise units).

---

# **7. Normative v1 Schemas (P2, P6)**

These shapes are **normative for v1**. Testbench `expected` blocks and `srob.py` SHALL conform. Optional fields may be omitted when empty; required fields must be present.

## **7.1 Segment object (within `segments[]`)**

| Field | Required | Notes |
|-------|----------|--------|
| `id` | yes | **Same as SOB segment id** (P1); do not renumber |
| `type` | yes | Canonical unit type after normalize |
| `text` | yes | Unchanged from SOB |
| `modality` | yes when SOB provided | SOB-final by default |
| `depth` | when list_item | 1-based |
| `parent_id` | when nested | SOB id of parent or null |
| `index_in_parent` | when list_item | 0-based within parent |
| `ordered` | when list_item | true/false if known |
| `structural_importance` | no | array of labels (P5 multi OK) |

## **7.2 `TP.structural.srob_structural_map` (full map every run — P2)**

```
srob_structural_map:
  segments: []                 # required; segment objects per §7.1
  list_structure: {}           # optional; summary of lists if any
  table_structure: {}          # optional
  block_structure: {}          # optional
  operators: []                # refined or pass-through coarse ids
  lexical_domains: []
  lexical_tones: []
  lexical_constraints: []
  discourse_flags: []          # canonicalized when present
  structural_importance: []    # optional aggregate; per-segment preferred
  modality: []                 # optional aggregate from segments
```

Tag arrays use **string ids** (coarse or fine). Primary entries follow §5.4 / §5.5.

## **7.3 `TP.structural.srob_residue`**

```
srob_residue:
  refined_tags: []             # tags that were actually sharpened to fine ids
  pass_through_tags: []        # coarse tags kept under P3/P4
  structural_adjacent: []      # optional structural-adjacent fragments
  unmapped_coarse: []          # optional diagnostic (P4)
  available_refinements: []    # optional diagnostic (P3 multi-child)
  disagreement_flags: []       # optional
  override_flags: []           # optional; SROB-owned only
```

## **7.4 Rules**

- All fields deterministic and replay-safe
- **Full** refined map every successful run (not delta-only) — P2
- Writer authority: SROB-owned fields only
- Bounded structural / semantic-adjacent refinement only

Downstream consumers: CnOB (primary), SmOB, ISc, SSG/STPX, TR/RB (features), IdOB (cues only).

---

# **8. SROB Audit Record**

SROB produces an audit record containing:

- support YAML load status
- vocab validation status / map inventory ref or hash
- normalization decisions (summary)
- sharpen decisions (coarse → fine, single-child refine, or pass-through)
- importance decisions
- discourse canonicalization decisions
- provenance lineage (`last_update`: SROB; origin linkage to SOB as applicable)
- `srob_structural_map` hash
- `srob_residue` hash
- timestamp

Audit record is read-only for downstream primitives.

---

# **9. Forbidden Behavior**

SROB must not:

- load or re-apply SOB lexical dictionaries to raw text
- invent coarse tags SOB did not emit
- invent new hint **types** outside SOB families
- auto-emit all multi-child fine ids on primary tag fields when no `when` (P3)
- renumber SOB segment ids (P1)
- enforce constraints
- generate meaning or resolve referents/identity
- modify semantic_core, intake/context, routing, identity, freeze, entropy metadata
- write outside SROB-owned TP envelopes
- require other primitives to consume diagnostic-only fields
- route directly into semantic OBs

---

# **10. Implementation Skeleton (Python)**

```python
class SROB:
    def __init__(self, tp_input):
        self.tp = tp_input

    def process(self):
        rules = self._load_support_yamls()
        self._validate_vocab_coupling(rules)

        sob_map = self._read_sob_map(self.tp)
        sob_residue = self._read_sob_residue(self.tp)

        units = self._normalize_structure(sob_map, rules)  # preserve ids
        units = self._resolve_boundaries(units, rules)

        sharpened = self._sharpen_tags(sob_map, sob_residue, rules)  # P3/P4
        discourse = self._canonicalize_discourse(sob_residue, rules)
        importance = self._apply_importance(units, sob_residue, rules)  # P5

        srob_map = self._build_structural_map(
            units, sharpened, discourse, importance, sob_map
        )
        residue = self._build_residue(sharpened, discourse, importance, sob_residue)
        audit = self._build_audit_record(srob_map, residue, rules)

        self.tp.setdefault("structural", {})
        self.tp["structural"]["srob_structural_map"] = srob_map
        self.tp["structural"]["srob_residue"] = residue
        self.tp.setdefault("metadata", {})
        self.tp["metadata"]["srob_audit_record"] = audit

        return self.tp
```

---

# **11. Implementation Skeleton (C++)**

```cpp
class SROB {
public:
    SROB(TP& tp_input) : tp(tp_input) {}

    TP process() {
        auto rules = load_support_yamls();
        validate_vocab_coupling(rules);

        auto sob_map = read_sob_map(tp);
        auto sob_residue = read_sob_residue(tp);

        auto units = normalize_structure(sob_map, rules);
        units = resolve_boundaries(units, rules);

        auto sharpened = sharpen_tags(sob_map, sob_residue, rules);
        auto discourse = canonicalize_discourse(sob_residue, rules);
        auto importance = apply_importance(units, sob_residue, rules);

        auto srob_map = build_structural_map(
            units, sharpened, discourse, importance, sob_map);
        auto residue = build_residue(
            sharpened, discourse, importance, sob_residue);

        tp.structural.srob_structural_map = srob_map;
        tp.structural.srob_residue = residue;
        tp.metadata.srob_audit_record =
            build_audit_record(srob_map, residue, rules);

        return tp;
    }

private:
    TP& tp;
};
```

---

# **12. Downstream Consumption Map (Normative Intent)**

| Primitive | Consumes | Purpose |
|-----------|----------|--------|
| **CnOB** | srob map/residue | constraint-oriented structure + constraint hints |
| **SmOB** | srob map/residue | semantic-adjacent cues on stable units |
| **ISc** | srob residue | scoring features |
| **SSG/STPX** | refined tags/structure | semantic-layer adjacent activation |
| **TR/RB** | residue features | routing cues |
| **IdOB** | structure/cues only | binding support; not SROB-owned meaning |

---

# **13. Locked Policies (P1–P6)**

| ID | Topic | Lock |
|----|--------|------|
| **P1** | Segment ids | **Preserve SOB `seg_*` ids**; do not renumber |
| **P2** | Map style | **Full** `srob_structural_map` every run |
| **P3** | Multi-child, no `when` | **Pass-through coarse** on primary tags; optional `available_refinements`; single child may refine |
| **P4** | Unmapped coarse | **Pass-through** + optional `unmapped_coarse` |
| **P5** | Importance labels | **Multiple labels allowed** per segment |
| **P6** | Schema home | **This document** owns normative v1 field schema |

Other working leans: thin-3 YAML pack; always run SROB in Path-A; CnOB prefers SROB fields when present; modality SOB-final by default.

---

# ⭐ **End of Document — `srob_py_struc_pgm.md` (Version 1.1)**

---
