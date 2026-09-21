# **SOB.md — structural Object Basin**  
### *Path‑A Short Simulator Primitive Documentation*

## **1. Definition**  
The **Structural Object Basin (SOB)** is the first primitive in the Path‑A short simulation chain. It performs structural segmentation of the input utterance and establishes the segment geometry that all downstream primitives depend on. SOB identifies admissible segment classes and constructs the structural envelope for role assignment, constraint matching, smoothing, and identity formation. 

SOB is responsible for answering the question:

> **“How is this utterance structurally divided?”**

This segmentation determines whether the simulator can proceed deterministically through SROB → CnOB → SmOB → IdOB.

---

## **2. Purpose and Function**

SOB evaluates:

- **segment geometry** (atomic, composite, recursive, discontinuous)  
- **segment class admissibility**  
- **structural envelope** for downstream primitives  
- **segment token grouping**  
- **structural residue** (if segmentation is incomplete)

These behaviors are consistent with the effects described in your existing SOB.md:  
- SOB constrains role geometry activation for SROB  
- SOB shapes constraint satisfaction envelopes for CnOB  
- SOB influences smoothing requirements for SmOB  
- SOB provides structural anchors for IdOB identity confirmation 

---

## **3. Allowed Segment Classes**  
SOB may classify segments into the following admissible classes: 

- `atomic_segment`  
- `composite_segment`  
- `recursive_segment`  
- `discontinuous_segment`

These classes correspond to the structural geometries defined in your segment dictionaries.

---

# **4. Structural Variables Filled by SOB (Local View)**  
SOB is the first primitive in the Path‑A pipeline. It establishes the **structural segmentation envelope** that all downstream primitives depend on.  
This section shows **only** the structural variables that SOB fills, along with those it leaves empty for later primitives.

For the **full IdOB structural envelope**, see:  
**`IdOB.md — Section 4: IdOB Structural Envelope (Canonical)`**

---

## **4.1 Structural Origin Mini‑Table (SOB View)**

| Structural Term          | Filled by SOB? | Notes |
|--------------------------|----------------|-------|
| **segments**             | ✔              | SOB performs segmentation and assigns segment classes (e.g., WQ, IQ, NP). |
| **segment_tokens**       | ✔              | SOB groups tokens into segments according to segment geometry. |
| **roles**                | ✘              | Assigned by SROB. SOB does not perform role assignment. |
| **constraints_matched**  | ✘              | Determined by CnOB. SOB does not evaluate constraints. |
| **residue**              | ✘              | Produced by CnOB. SOB does not generate constraint residue. |
| **smoothing_operations** | ✘              | Produced only by SmOB. SOB performs no smoothing. |
| **smoothing_residue**    | ✘              | Produced only by SmOB. |
| **semantic_adjacent_cues** | ✘            | Produced only by SmOB. |
| **semantic_core**        | ✘              | Constructed by IdOB. SOB does not interpret meaning. |
| **truth_relation**       | ✘              | Determined by IdOB. |
| **token_relations**      | ✘              | Determined by IdOB. |
| **ob_set_notes**         | ✔              | SOB produces structural notes summarizing segmentation. |

---

## **4.2 Summary**

SOB fills **only** the structural segmentation layer:

- `segments`  
- `segment_tokens`  
- `ob_set_notes`

All other structural, relational, smoothing, and semantic variables are filled by downstream primitives:

```
SOB → SROB → CnOB → SmOB → IdOB
```

This mini‑table provides a quick mnemonic reference when debugging SOB output.

---

## **5. Example (from your simulator)**  
This is the exact example you described — the one you want to appear when clicking SOB:

```
segments:
  - WQ
  - IQ
  - NP

segment_tokens:
  - ['why']
  - ['is']
  - ['the', 'sky', 'blue']

roles:
  - []

constraints_matched:
  - []

residue:
  - []

smoothing_residue:
  - []

smoothing_operations:
  - []

semantic_adjacent_cues:
  - []

semantic_core:
  - {}

token_relations:
  - []

ob_set_notes:
  - OB-Set: Segments = WQ, IQ, NP
  - OB-Set: Segment tokens = ['why'] | ['is'] | ['the', 'sky', 'blue']
```

This example is fully aligned with the SOB definition and the structural envelope described in your existing SOB.md. 

---

## **6. Notes**

- SOB is purely structural; it does not assign roles or meaning.  
- SOB success is a **hard requirement** for deterministic meaning.  
- If SOB fails (unknown tokens, unmatched segment patterns), IdOB sufficiency becomes impossible.  
- SOB output is the mnemonic anchor for debugging — clicking SOB should always show this schema and example.

---

## **7. Relationship to Downstream Primitives**

SOB → SROB  
SOB constrains which roles can be assigned.

SOB → CnOB  
SOB shapes the constraint satisfaction envelope.

SOB → SmOB  
SOB determines adjacency and smoothing requirements.

SOB → IdOB  
SOB provides the structural anchors for identity confirmation.

These relationships match the effects listed in your current SOB.md. 

---

## **8. Explanation and Examples Starting from Tokens**

See [Appendix X — Token‑to‑Structure Bridge](appendix_x_token_to_structure_bridge.md)  
for a full walkthrough from tokens → segments → roles → constraints → basin → identity.

---
