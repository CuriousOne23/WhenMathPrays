# **SROB Software Architecture**
*(primitives/srob/srob_software_architecture.md)*

**Status:** Working design (leans from `srob_sob_comm_architect.md` v1.1)  
**Aligned with:** 20.40.020 v2.0, 20.40.010, tp_path_a_map.md, srob_sob_comm_architect.md  
**Non-goals:** YAML body contents, testbench YAMLs, full `srob.py` implementation

---

## **1. Architectural Philosophy**

The SROB layer must be:

- **small** — core logic fits in one file (`srob.py`)
- **linear** — refine what SOB already placed on the TP; no second lexical extraction engine
- **modular** — normalization rules and sharpen maps externalized
- **deterministic** — identical TP(SOB) + rules → identical SROB output
- **bounded** — structural and semantic-adjacent refinement only, within SOB field space
- **debuggable** — every behavior traceable to a small module; SOB↔SROB vocab desync is loud
- **expandable** — deepen maps under existing SOB parents without touching core logic
- **coupled, never disjoint** — SROB parent keys ⊆ SOB coarse category set; hierarchical fine ids

The goal is that reading `srob.py` feels **unimpressive** — simple, predictable, easy to maintain.

SROB is **post-SOB refinement**.  
It consumes SOB-owned fields **read-only** from the TP, does **not** load `sob_*.yaml`, and writes only SROB-owned fields for downstream (CnOB primary, then SmOB, scoring/routing).

**Invariant:** SOB does not surprise SROB — in structural units or in lexical/hint field space.

---

## **2. Directory Structure**

```
primitives/
  sob/
    sob.py
    sob_*.yaml                 # lexical extraction (SOB only; SROB does not load)

  srob/
    srob.py                    # tiny execution core
    srob_software_architecture.md
    srob_py_struc_pgm.md
    srob_sob_comm_architect.md # handoff contract / design board

    srob_normalize_rules.yaml  # list/table/block/boundary/discourse normalize (lean: thin-3)
    srob_sharpen_maps.yaml     # coarse → fine within SOB type families
    srob_importance_rules.yaml # positional structural-importance labels
```

**Testbench YAMLs** live under progressive-lineup paths (not defined here).

This structure ensures:

- SROB is **self-contained** for refinement policy
- SROB core remains **tiny**
- debugging is **local** (rules vs maps vs core)
- expansion is **safe** (deeper under SOB parents only)
- upstream/downstream boundaries remain intact

---

## **3. SROB Core (`srob.py`)**

### **3.1 Responsibilities**

`srob.py` performs a fixed set of operations:

1. **Load SROB support YAMLs** (not SOB dictionaries)
2. **Validate vocab coupling** (sharpen map parents vs SOB coarse tags / declared inventory)
3. **Read SOB fields from TP** (`sob_structural_map`, `sob_residue`, related structural metadata)
4. **Normalize structure** (lists, tables, code/math blocks, boundaries, nesting, unit consistency)
5. **Sharpen tags** within SOB families (operator / domain / tone / constraint)
6. **Normalize discourse flags** present on SOB residue (canonical names)
7. **Assign / refine structural-importance** (positional cues; not semantic roles)
8. **Form SROB residue and full refined structural map**
9. **Write SROB-owned fields + audit** (optional diagnostic-only metadata)

**Does not:**

- Re-load `sob_*.yaml` or re-tag raw text as a second SOB
- Invent new hint **types** outside SOB’s field space
- Enforce constraints
- Resolve referent identity or entity meaning
- Modify TP text, meaning-layer, Context Frame, MSL, identity, freeze, routing_metadata
- Route directly to semantic OBs

### **3.2 Execution Flow**

```
load_srob_yaml_files()
validate_sharpen_maps_against_sob_vocab()
sob_map, sob_residue = read_sob_fields(tp)   # TP only

units = normalize_structure(sob_map, normalize_rules)
units = resolve_boundaries(units, normalize_rules)

sharpened = sharpen_tags(sob_map, sob_residue, sharpen_maps)  # pass-through if no child
discourse = canonicalize_discourse(sob_residue, normalize_rules)
importance = apply_importance_rules(units, sob_residue, importance_rules)

srob_map = build_full_refined_map(units, sharpened, discourse, importance)
srob_residue = form_residue(...)
audit = build_audit(...)

write owned fields only
return tp
```

Core should stay on the order of a few hundred lines, not a second NLP stack.

### **3.3 Two work streams (do not conflate)**

| Stream | Input | Output contribution |
|--------|-------|---------------------|
| **A. Structure** | SOB segments / block cues | Canonical list/table/block geometry, boundaries, nesting |
| **B. Tags** | SOB coarse operator/domain/tone/constraint | Finer ids under same parents; pass-through if no map child |

---

## **4. Support YAML Files (SROB-owned)**

Each file is **policy**, not a second lexical surface dictionary.

### **4.1 `srob_normalize_rules.yaml`** (lean: includes boundary + discourse)

- List markers, depth, ordered/unordered, parent binding
- Table header/body/cell structure (content untouched)
- Code/math block typing (content untouched)
- Boundary / continuation rules
- Discourse flag **canonicalize** map (variant names → canonical)

### **4.2 `srob_sharpen_maps.yaml`**

- Top-level keys = **exact SOB coarse category ids**
- Children = hierarchical fine ids (`parent.child`)
- Empty child list = pass-through of coarse tag
- Optional `when` conditions structural/tag-based (not a new surface lexicon)
- **Forbidden:** parent keys not in SOB vocab; fine ids that do not nest under parent

### **4.3 `srob_importance_rules.yaml`**

- Positional labels: header_like, anchor_like, subject_like, object_like, list_lead, …
- Rules over segment type, depth, index, position
- Not semantic role labeling or referent resolution

### **4.4 Vocab sync (hard rule)**

| Rule | Effect |
|------|--------|
| SOB defines coarse category set | Closed parent inventory |
| SROB map keys ⊆ that set | No disjoint taxonomy |
| Fine id = `parent + "." + child` | Obvious + inherent hierarchy |
| Load/test validation | `SROB_MAP_DESYNC` (or equivalent) on illegal parents |
| Start minimal | Empty refinements OK; grow depth under existing parents |
| Grow paths | Wider SOB coarse **or** deeper SROB child — never SROB-only types |

Desync must be a **named dictionary fault**, not a silent downstream mystery.

---

## **5. Why These Files Exist**

### **5.1 Modularity**
SROB core stays tiny and readable.

### **5.2 Debuggability**
Mis-refine? Check: SOB TP fields → normalize rules → sharpen maps → importance rules. Few places.

### **5.3 Expandability**
Add a fine subtype: edit sharpen map under an existing SOB parent; run tests. No core rewrite.

### **5.4 Determinism**
Versioned YAML; explicit; reproducible.

### **5.5 Safety**
No second extraction lexicon. Structure rules + tag views over SOB schema only.

---

## **6. Upstream Consumption**

SROB reads from TP (after SOB):

- `structural.sob_structural_map`
- `structural.sob_residue`
- Related structural / discourse-adjacent metadata SOB wrote
- Optional read-only context cues already on TP (same discipline as 20.40.020) when useful for boundary/normalize — **not** to invent tags SOB never emitted

SROB does **not** read or load:

- `sob_dictionary.yaml`, `sob_operators.yaml`, `sob_domains.yaml`, etc.
- routing_metadata, ΔH%, truth/done, lineage, Pipeline-B envelopes (as forbidden in 20.40.020)

**Sufficiency rule:** If SROB cannot do its job from TP(SOB) + SROB YAMLs, **fix SOB** — do not re-implement SOB inside SROB.

---

## **7. Downstream Boundaries**

SROB produces refined structure/tags for:

| Consumer | Primary use |
|----------|-------------|
| **CnOB** | Canonical structure + sharper constraint (and related) hints |
| **SmOB** | Stable units + finer domain/operator/tone cues |
| **ISc / SSG / STPX** | Cleaner residue features |
| **TR / DCB / RBU / RB** | More stable routing features (indirect) |
| **IdOB** | Boundaries/cues only; not identity/meaning ownership |

SROB does **not** duplicate: constraint enforcement, semantic-layer meaning, identity freeze, routing decisions, commit.

**Consumer lean:** In full Path-A sequence, CnOB prefers **SROB** fields when present (SROB required in sequence; progressive-lineup toggles may still isolate stages in tests).

---

## **8. Owned Fields**

SROB writes only:

- `TP.structural.srob_structural_map` — **full** refined map (lean: not delta-only)
- `TP.structural.srob_residue`
- `TP.metadata.srob_audit_record`
- Optional diagnostic-only metadata (not required reading for other primitives)

Modality lean: **SOB-final** unless a boundary/unit change forces modality to move with the unit.

---

## **9. Summary**

The SROB software architecture is:

- **modular** and **dictionary/policy-driven** (refinement, not re-lex)
- **linear** and **bounded**
- **deterministic** and **debuggable**
- **vocab-coupled** to SOB (obvious + inherent; never disjoint)
- **minimal-first, deepen later**
- **non-duplicative** of SOB extraction and of downstream meaning/routing

Aligned with:

- **20.40.020_srob_prim.md** (v2.0)
- **srob_sob_comm_architect.md**
- **tp_path_a_map.md**
- SOB architecture pattern (small core, external YAML, owned fields)

---

**End of `srob_software_architecture.md`**

---
