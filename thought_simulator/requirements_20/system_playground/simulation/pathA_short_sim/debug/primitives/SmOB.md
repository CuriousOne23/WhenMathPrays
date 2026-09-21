# **SmOB.md — Semantic Object Basin**  
### *Path‑A Short Simulator Primitive Documentation*

## **1. Definition**  
The **Semantic Object Basin (SmOB)** is the fourth primitive in the Path‑A short simulation chain.  
SmOB performs two jobs:

1. **Semantic‑adjacent cue extraction**  
   It identifies semantic‑adjacent, modality, affect, conflict‑adjacent, and underspecification‑adjacent signals emerging from SOB → SROB → CnOB residue.

2. **Deterministic pre‑semantic compression**  
   It compresses upstream residue plus SmOB cues into:
   - a **deterministic pre‑semantic hash**, and  
   - a **TR‑input cue vector** used by the Thought Router and SSG.

SmOB is not a semantic interpreter.  
It is a **pre‑semantic basin** that stabilizes upstream structure and prepares deterministic routing inputs.

This aligns with your normative definition in 20.40.040.

---

## **2. Purpose and Function**

SmOB answers the question:

> **“What semantic‑adjacent cues exist, and how do we compress all upstream residue into a deterministic representation for routing?”**

SmOB performs:

- semantic‑adjacent cue extraction  
- modality cue extraction  
- affect marker extraction  
- conflict‑adjacent and underspecification‑adjacent signal detection  
- deterministic pre‑semantic hashing  
- TR‑input cue vector formation  
- stabilization of upstream residue  
- preparation of routing‑adjacent geometry  

SmOB ensures that downstream primitives (SSG, TR, IdOB) receive a **canonical, replay‑safe representation**.

---

## **3. Allowed SmOB Values**

SmOB may activate any of the following basin geometries:

- **semantic_adjacent_cue**  
- **modality_cue**  
- **affect_marker**  
- **routing_adjacent_cue**  
- **presemantic_residue_hash**  
- **tr_input_vector**

These correspond to the basin geometries defined in your semantic‑adjacent and routing dictionaries.

---

# **4. Structural Variables Filled by SmOB (Local View)**  
SmOB is the fourth primitive in the Path‑A pipeline.  
It fills **all semantic‑adjacent and pre‑semantic compression variables**.

For the **full IdOB structural envelope**, see:  
**`IdOB.md — Section 4: IdOB Structural Envelope (Canonical)`**

### **4.1 Structural Origin Mini‑Table (SmOB View)**

| Structural Term            | Filled by SmOB? | Notes |
|----------------------------|------------------|-------|
| **segments**               | ✘                | Provided by SOB. |
| **segment_tokens**         | ✘                | Provided by SOB. |
| **roles**                  | ✘                | Provided by SROB. |
| **constraints_matched**    | ✘                | Provided by CnOB. |
| **residue**                | ✘                | Provided by CnOB. |
| **smoothing_operations**   | ✔                | SmOB applies basin‑level smoothing to stabilize upstream residue. |
| **smoothing_residue**      | ✔                | Residue after basin smoothing. |
| **semantic_adjacent_cues** | ✔                | **Primary output** — semantic‑adjacent, modality, affect, conflict‑adjacent cues. |
| **semantic_core**          | ✘                | Constructed by IdOB. |
| **truth_relation**         | ✘                | Determined by IdOB. |
| **token_relations**        | ✘                | Determined by IdOB. |
| **ob_set_notes**           | ✔                | SmOB may add notes about cue extraction and basin compression. |

### **4.2 Summary**

SmOB fills:

- `semantic_adjacent_cues`  
- `smoothing_operations`  
- `smoothing_residue`  
- `ob_set_notes` (basin‑related notes)

All other structural, relational, and semantic variables are filled by other primitives:

```
SOB → SROB → CnOB → SmOB → IdOB
```

---

## **5. Effects**

SmOB produces the following effects:

- extracts semantic‑adjacent cues needed for IdOB  
- stabilizes upstream residue for deterministic routing  
- prepares TR‑input cue vectors  
- supports constraint satisfaction continuity  
- influences identity confirmation pathways  
- ensures replay‑safe pre‑semantic geometry  

These effects ensure that identity formation and routing operate on stable, deterministic inputs.

---

## **6. Examples**

Examples adapted from your current debug format:

- `"SmOB applied: semantic_adjacent_cues=[interrogative_scope], smoothing_operations=[adjacency_smoothing]"`  
- `"SmOB applied: semantic_adjacent_cues=[modality_cue], smoothing_residue=presemantic_residue"`  

These illustrate cue extraction and basin stabilization.

---

## **7. Notes**

- SmOB is **not** a semantic interpreter.  
- SmOB does **not** assign roles.  
- SmOB does **not** evaluate constraints.  
- SmOB is required for deterministic meaning: without basin compression, IdOB cannot form identity deterministically.  
- SmOB provides the **canonical pre‑semantic representation** for routing and identity.

---
