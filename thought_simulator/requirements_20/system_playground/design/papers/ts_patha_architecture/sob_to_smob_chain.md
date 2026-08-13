# **SOB → SROB → CnOB → SmOB Chain**
**Document:** `primitives/smob/sob_to_smob_chain.md`  
**Status:** Support / orientation (implementation-aligned)  
**Version:** 1.0  
**Purpose:** One-page progressive-digestion picture for the OB quartet so support does not treat layers as interchangeable “finer copies” of each other  
**Aligned with:** 20.40.010, 20.40.020 v2.0, 20.40.030 v2.0, 20.40.040 v2.0, tp_path_a_map.md

---

## **1. Why this document exists**

The Path-A OB family exists to **shrink the open meaning/search space** before SSG, TR/RB, and IdOB.  
Each layer has a **different window** on the same TP. Treating SmOB as “finer CnOB” or CnOB as “finer SROB” is a design error and a support trap.

---

## **2. Progressive lineup (macro)**

```
TPU / text surface
        │
        ▼
      SOB     — coarse structure + lexical tags (wide lexicon)
        │
        ▼
      SROB    — normalize structure + sharpen tags (deeper policy, same families)
        │
        ▼
      CnOB    — constraint objects (C1–C7, gaps, conflicts, constraint-importance)
        │
        ▼
      SmOB    — semantic-adjacent cues + compression (hash, TR-input vector)
        │
        ▼
   SSG / TR / RB / IdOB / …
```

**Goal of the chain:** human-league, non-omniscient digestion — rigid fields, visible gaps, exact addressing — not perfect meaning.

---

## **3. Layer comparison**

| Layer | Window | Primary writes | Coupling to previous |
|-------|--------|----------------|----------------------|
| **SOB** | Text → coarse units/tags | `sob_structural_map`, `sob_residue` | Lexicons / extraction |
| **SROB** | Structure/tag refinement | `srob_structural_map`, `srob_residue` | **Dictionary sync** to SOB parents |
| **CnOB** | Constraint projection | `cnob_constraint_map`, `cnob_residue` | **TP surface contract** with SROB |
| **SmOB** | Semantic-adjacent cue + compress | `smob_cue_map` / residue, hash, TR vector | **TP surface + residue contract** with CnOB (prefer CnOB) |

---

## **4. What each layer *earns***

| Layer | Earns its place by… |
|-------|---------------------|
| **SOB** | Making structure and coarse tags **exist** from text |
| **SROB** | Making structure **canonical** and tags **higher-resolution** without a second lexicon |
| **CnOB** | Making **obligation, absence, conflict** explicit as constraint objects |
| **SmOB** | Making **SSG/TR-ready cues** and a **fixed-size pre-semantic address** without deep meaning |

Without SmOB, SSG would re-chew CnOB+SROB surfaces and risk unbounded “soft semantics.”  
Without CnOB, SmOB would rediscover gaps/conflicts from structure alone.

---

## **5. Coupling types (support-critical)**

| Edge | Coupling kind | Fail mode |
|------|---------------|-----------|
| SOB ↔ SROB | Hierarchical **vocab sync** | `SROB_MAP_DESYNC` / illegal parents |
| SROB ↔ CnOB | **Surface contract** (field predicates) | Rule never fires; wrong field names |
| CnOB ↔ SmOB | **Surface + residue contract** (prefer CnOB map/residue) | Starved cues; wrong sync model if SmOB tries to key-sync CnOB YAML trees |

**Never** apply SOB↔SROB dictionary rules to CnOB or SmOB policy files by default.

---

## **6. Downstream of SmOB**

| Consumer | Uses |
|----------|------|
| **SSG** | Sole pre-semantic input (HLR-009 intent): cues + compressed residue |
| **TR / RB** | TR-input vector + residue hash for exact route keys |
| **IdOB** | Reduced cue/constraint rails; content still often TPU |
| **ISc** | Scoring features from cues/importance |

---

## **7. Support debug order (chain)**

1. Which layer failed?  
2. Inspect **TP owned fields of the prior layer** (not prior YAML trees, except SOB↔SROB vocab).  
3. Match consumer rule predicates to those fields.  
4. Fix handoff or rules — do not re-implement upstream inside the starved layer.

---

## **8. Pointers**

| Topic | Document |
|-------|----------|
| SmOB ↔ CnOB handoff | `smob_cnob_comm_architect.md` |
| SmOB software shape | `smob_software_architecture.md` |
| SmOB schemas / process | `smob_py_struc_pgm.md` |
| CnOB ↔ SROB handoff | `../cnob/cnob_srob_comm_architect.md` |
| SROB ↔ SOB handoff | `../srob/srob_sob_comm_architect.md` |

---

**End of `sob_to_smob_chain.md` (v1.0)**

---
