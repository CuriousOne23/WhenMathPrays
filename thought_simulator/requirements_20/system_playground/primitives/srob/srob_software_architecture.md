# **SROB Software Architecture**
*(primitives/srob/srob_software_architecture.md)*

**Status:** Working design; **P1–P6 locked** (see §8.1 and `srob_py_struc_pgm.md` v1.1)  
**Aligned with:** 20.40.020 v2.0, 20.40.010, tp_path_a_map.md, srob_sob_comm_architect.md  
**Non-goals:** Full YAML refinement depth, testbench YAMLs, full `srob.py` implementation

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

**Schema authority (P6):** Normative v1 shapes for `srob_structural_map` and `srob_residue` live in **`srob_py_struc_pgm.md`**. This architecture file does not redefine field schemas.

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
    srob_py_struc_pgm.md       # normative process + v1 field schemas (P6)
    srob_sob_comm_architect.md # handoff contract / design board

    srob_normalize_rules.yaml  # list/table/block/boundary/discourse normalize (thin-3)
    srob_sharpen_maps.yaml     # coarse → fine within SOB type families
    srob_importance_rules.yaml # positional structural-importance labels
```

**Testbench YAMLs** live under progressive-lineup paths (not defined here).

---

## **3. SROB Core (`srob.py`)**

### **3.1 Responsibilities**

`srob.py` performs a fixed set of operations:

1. **Load SROB support YAMLs** (not SOB dictionaries)
2. **Validate vocab coupling** (sharpen map parents vs SOB coarse tags / declared inventory)
3. **Read SOB fields from TP** (`sob_structural_map`, `sob_residue`, related structural metadata)
4. **Normalize structure** (lists, tables, code/math blocks, boundaries, nesting, unit consistency) while **preserving SOB segment ids** (P1)
5. **Sharpen tags** within SOB families per multi-refinement policy (P3) — not “always emit fine tags”
6. **Normalize discourse flags** present on SOB residue (canonical names)
7. **Assign / refine structural-importance** (positional cues; multi-label OK — P5)
8. **Form full SROB structural map + residue** (P2)
9. **Write SROB-owned fields + audit** (optional diagnostic-only metadata)

**Does not:**

- Re-load `sob_*.yaml` or re-tag raw text as a second SOB
- Invent new hint **types** outside SOB’s field space
- Auto-emit all multi-child fine ids on primary tag fields when no `when` (P3)
- Renumber SOB segment ids (P1)
- Enforce constraints
- Resolve referent identity or entity meaning
- Modify TP text, meaning-layer, Context Frame, MSL, identity, freeze, routing_metadata
- Route directly to semantic OBs

### **3.2 Execution Flow**

```
load_srob_yaml_files()
validate_sharpen_maps_against_sob_vocab()
sob_map, sob_residue = read_sob_fields(tp)   # TP only

units = normalize_structure(sob_map, normalize_rules)  # preserve ids
units = resolve_boundaries(units, normalize_rules)

sharpened = sharpen_tags(...)  # P3: pass-through unless single child or when
discourse = canonicalize_discourse(sob_residue, normalize_rules)
importance = apply_importance_rules(...)  # P5 multi-label OK

srob_map = build_full_refined_map(...)     # P2 full map
srob_residue = form_residue(...)           # includes optional P3/P4 diagnostics
audit = build_audit(...)

write owned fields only
return tp
```

### **3.3 Two work streams (do not conflate)**

| Stream | Input | Output contribution |
|--------|-------|---------------------|
| **A. Structure** | SOB segments / block cues | Canonical list/table/block geometry, boundaries, nesting |
| **B. Tags** | SOB coarse operator/domain/tone/constraint | Fine id only under P3; else pass-through coarse |

---

## **4. Support YAML Files (SROB-owned)**

Each file is **policy**, not a second lexical surface dictionary.

### **4.1 `srob_normalize_rules.yaml`**

- List markers, depth, ordered/unordered, parent binding
- Table header/body/cell structure (content untouched)
- Code/math block typing (content untouched)
- Boundary / continuation rules
- Discourse flag **canonicalize** map (variant names → canonical)

### **4.2 `srob_sharpen_maps.yaml`**

- Top-level keys = **exact SOB coarse category ids**
- Children = hierarchical fine ids (`parent.child`)
- Empty child list = pass-through of coarse tag
- Multi-child without `when` = **pass-through coarse** on primary tags (P3); children remain available for later `when` / diagnostics
- Optional `when` conditions structural/tag-based (not a new surface lexicon)
- **Forbidden:** parent keys not in SOB vocab; fine ids that do not nest under parent

### **4.3 `srob_importance_rules.yaml`**

- Positional labels: header_like, anchor_like, subject_like, object_like, list_lead, …
- Rules over segment type, depth, index, position
- Multiple labels per segment allowed (P5)
- Not semantic role labeling or referent resolution

### **4.4 Vocab sync (hard rule)**

| Rule | Effect |
|------|--------|
| SOB defines coarse category set | Closed parent inventory |
| SROB map keys ⊆ that set | No disjoint taxonomy |
| Fine id = `parent + "." + child` | Obvious + inherent hierarchy |
| Load/test validation | `SROB_MAP_DESYNC` on illegal parents |
| Unmapped coarse on TP | Pass-through + optional diagnostic (P4) |
| Start minimal | Empty refinements OK; grow depth under existing parents |
| Grow paths | Wider SOB coarse **or** deeper SROB child — never SROB-only types |

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
| **CnOB** | Canonical structure + constraint (and related) hints |
| **SmOB** | Stable units + domain/operator/tone cues |
| **ISc / SSG / STPX** | Cleaner residue features |
| **TR / DCB / RBU / RB** | More stable routing features (indirect) |
| **IdOB** | Boundaries/cues only; not identity/meaning ownership |

SROB does **not** duplicate: constraint enforcement, semantic-layer meaning, identity freeze, routing decisions, commit.

**Consumer lean:** In full Path-A sequence, CnOB prefers **SROB** fields when present.

---

## **8. Owned Fields and Locked Policies**

SROB writes only:

- `TP.structural.srob_structural_map` — **full** refined map (P2)
- `TP.structural.srob_residue`
- `TP.metadata.srob_audit_record`
- Optional diagnostic-only metadata (not required reading for other primitives)

Modality: **SOB-final** unless a boundary/unit change forces modality to move with the unit.

### **8.1 Locked policies (P1–P6)**

| ID | Topic | Lock |
|----|--------|------|
| **P1** | Segment ids | Preserve SOB segment ids; do not renumber |
| **P2** | Map style | Full `srob_structural_map` every run |
| **P3** | Multi-child, no `when` | Pass-through coarse on primary tags; optional `available_refinements`; single child may refine |
| **P4** | Unmapped coarse | Pass-through + optional `unmapped_coarse` |
| **P5** | Importance | Multiple labels allowed per segment |
| **P6** | Schema home | **`srob_py_struc_pgm.md`** owns normative v1 field schema |

**Important:** Multi-child entries in `srob_sharpen_maps.yaml` document *available* depth for later `when` rules and diagnostics. They do **not** mean SROB always writes fine tags.

---

## **9. Summary**

The SROB software architecture is:

- **modular** and **policy-driven** (refinement, not re-lex)
- **linear** and **bounded**
- **deterministic** and **debuggable**
- **vocab-coupled** to SOB (obvious + inherent; never disjoint)
- **minimal-first, deepen later** under locked selection policies
- **non-duplicative** of SOB extraction and of downstream meaning/routing

Aligned with:

- **20.40.020_srob_prim.md** (v2.0)
- **srob_sob_comm_architect.md**
- **srob_py_struc_pgm.md** (v1.1 — schema + P1–P6)
- **tp_path_a_map.md**

---

**End of `srob_software_architecture.md`**

---
