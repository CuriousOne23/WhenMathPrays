# ⭐ **`srob_py_struc_pgm.md` (Version 1.0)**
### *Python & C++ Implementation Blueprint for the SROB Primitive*
### *Aligned with 20.40.020 v2.0, srob_software_architecture.md, srob_sob_comm_architect.md, 20.105.*, 20.15*

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
- forming **`srob_structural_map`** (full refined map)
- producing **`srob_residue{}`**
- producing **`srob_audit_record{}`**
- optional diagnostic-only metadata
- preserving upstream / SOB / meaning fields (read-only)

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
    # normalize structure + boundaries
    # sharpen tags (pass-through if no refinement)
    # canonicalize discourse flags
    # apply importance rules
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
5. Normalize structure (lists/tables/blocks/unit consistency)
6. Resolve boundaries / nesting
7. Sharpen tags within SOB families (no parent tag ⇒ no invented fine tag)
8. Canonicalize discourse flags present on SOB residue
9. Apply structural-importance rules
10. Build full `srob_structural_map`
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
- Coarse tag on TP with empty/absent map entry ⇒ **pass-through** (keep coarse); optional diagnostic `unmapped_coarse`
- **No sharpen without SOB tag** (settled lean)

### **5.2 Families in scope**

- operators
- domains
- tones
- constraints

Modality: **SOB-final** by default (lean).

### **5.3 Growth**

- Start minimal (pass-through maps OK)
- Grow by adding children under existing parents or adding SOB coarse tags first
- Never introduce SROB-only top-level categories

---

# **6. Structure Normalization**

SROB normalizes using `srob_normalize_rules.yaml`:

- list depth, ordering, parent indices, stable item ids
- table header/body/cells (text content unchanged)
- code/math blocks typed; content unchanged
- boundary and continuation attachment
- consistent unit types across the TP

SROB does **not** invent structural units that SOB never proposed (default: no surprise units).

---

# **7. SROB Residue and Map Construction**

SROB constructs (illustrative shape — exact schema TBD with implementation):

```
TP.structural.srob_structural_map {
    segments[]              # normalized units, depth, parent, type
    list_structure{}
    table_structure{}
    block_structure{}
    operators[]             # sharpened or pass-through
    lexical_domains[]
    lexical_tones[]
    lexical_constraints[]
    discourse_flags[]       # canonicalized
    structural_importance[]
    modality[]              # typically from SOB
}
```

```
TP.structural.srob_residue {
    refined_tags[]
    structural_adjacent[]
    pass_through_flags[]
    unmapped_coarse[]       # optional diagnostic
    disagreement_flags[]    # optional vs SOB coarse when useful
}
```

Rules:

- All fields deterministic and replay-safe
- Full refined map (lean), not delta-only
- Writer authority: SROB-owned fields only
- Bounded structural / semantic-adjacent refinement only

Downstream consumers:

- CnOB (primary)
- SmOB
- ISc, SSG, STPX
- TR / RB (via residue features)
- IdOB (cues only)

---

# **8. SROB Audit Record**

SROB produces an audit record containing:

- support YAML load status
- vocab validation status / map inventory ref or hash
- normalization decisions (summary)
- sharpen decisions (coarse → fine or pass-through)
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

        units = self._normalize_structure(sob_map, rules)
        units = self._resolve_boundaries(units, rules)

        sharpened = self._sharpen_tags(sob_map, sob_residue, rules)
        discourse = self._canonicalize_discourse(sob_residue, rules)
        importance = self._apply_importance(units, sob_residue, rules)

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

    # Internal helpers:
    # _load_support_yamls
    # _validate_vocab_coupling
    # _read_sob_map / _read_sob_residue
    # _normalize_structure
    # _resolve_boundaries
    # _sharpen_tags
    # _canonicalize_discourse
    # _apply_importance
    # _build_structural_map
    # _build_residue
    # _build_audit_record
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
    // deterministic helper methods
};
```

---

# **12. Downstream Consumption Map (Normative Intent)**

SROB writes:

- `srob_structural_map`
- `srob_residue`
- `srob_audit_record{}`

| Primitive | Consumes | Purpose |
|-----------|----------|--------|
| **CnOB** | srob map/residue | constraint-oriented structure + sharper constraint hints |
| **SmOB** | srob map/residue | semantic-adjacent cues on stable units |
| **ISc** | srob residue | scoring features |
| **SSG/STPX** | refined tags/structure | semantic-layer adjacent activation |
| **TR/RB** | residue features | routing cues |
| **IdOB** | structure/cues only | binding support; not SROB-owned meaning |

SROB output must support deterministic replay and read-only consumption.

---

# **13. Working Leans (from comm architect; not all locked)**

| Topic | Lean |
|-------|------|
| YAML pack | Thin 3 (normalize incl. boundary/discourse; sharpen; importance) |
| Map style | Full refined map |
| Sharpen without SOB tag | Forbidden |
| Modality | SOB-final unless unit boundary forces carry |
| Importance | May derive positional cues from structure alone |
| Short-circuit | Always run SROB in Path-A sequence |
| CnOB | Prefer/require SROB fields when present in full sequence |

---

# ⭐ **End of Document — `srob_py_struc_pgm.md` (Version 1.0)**

---
