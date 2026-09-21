# **CnOB.md — Constraint Observation Block**  
### *Path‑A Short Simulator Primitive Documentation*

## **1. Definition**  
The **Constraint Observation Block (CnOB)** evaluates **structural**, **adjacency**, and **compatibility constraints** across segments and roles.  
Its purpose is to determine whether the utterance satisfies the required **constraint geometry** for downstream primitives.

This aligns with your current file’s definition:  
> “CnOB evaluates structural, adjacency, and compatibility constraints across segments and roles.” 

---

## **2. Purpose and Function**

CnOB answers the question:

> **“Do the segment–role combinations satisfy the required constraints for coherent interpretation?”**

CnOB performs:

- constraint geometry activation  
- constraint satisfaction evaluation  
- structural coherence checks  
- adjacency rule evaluation  
- compatibility rule evaluation  
- continuity rule evaluation  

This matches your existing description:  
> “It determines whether required conditions are satisfied and governs the activation of constraint geometry.”  

---

## **3. Allowed Constraint Values**

CnOB may match any of the following constraint types (from your current file):  

- **adjacency_rule**  
- **compatibility_rule**  
- **structural_rule**  
- **continuity_rule**  

These correspond to the constraint geometries defined in your dictionaries.

---

## **4. Structural Variables Filled by CnOB (Local View)**  
CnOB is the third primitive in the Path‑A pipeline.  
It fills **constraint‑related structural variables** and produces **constraint residue**.

For the **full IdOB structural envelope**, see:  
**`IdOB.md — Section 4: IdOB Structural Envelope (Canonical)`**

### **4.1 Structural Origin Mini‑Table (CnOB View)**

| Structural Term          | Filled by CnOB? | Notes |
|--------------------------|----------------|-------|
| **segments**             | ✘              | Provided by SOB. |
| **segment_tokens**       | ✘              | Provided by SOB. |
| **roles**                | ✘              | Provided by SROB. |
| **constraints_matched**  | ✔              | **Primary output of CnOB** — evaluates and matches constraint geometry. |
| **residue**              | ✔              | CnOB produces structural residue when constraints partially match or fail. |
| **smoothing_operations** | ✘              | Produced only by SmOB. |
| **smoothing_residue**    | ✘              | Produced only by SmOB. |
| **semantic_adjacent_cues** | ✘            | Produced only by SmOB. |
| **semantic_core**        | ✘              | Constructed by IdOB. |
| **truth_relation**       | ✘              | Determined by IdOB. |
| **token_relations**      | ✘              | Determined by IdOB. |
| **ob_set_notes**         | ✔              | CnOB may add notes about constraint geometry activation. |

### **4.2 Summary**

CnOB fills:

- `constraints_matched`  
- `residue`  
- `ob_set_notes` (constraint‑related notes)

All other structural, relational, smoothing, and semantic variables are filled by downstream primitives:

```
SOB → SROB → CnOB → SmOB → IdOB
```

---

## **5. Effects**

CnOB produces the following effects (from your current file):  

- **governs constraint satisfaction envelopes** for structural interpretation  
- **restricts segment‑role combinations** for SOB and SROB  
- **shapes smoothing requirements** for SmOB  
- **influences identity confirmation** for IdOB  

These effects ensure that only structurally coherent interpretations propagate downstream.

---

## **6. Examples**

Examples adapted from your current file:

- `"CnOB matched: constraint_geometry=compatibility_rule, constraints_matched=compatibility_rule"` 
- `"CnOB matched: constraint_geometry=adjacency_rule, residue=adjacency_residue"` 

These illustrate constraint matching and residue generation.

---

## **7. Notes**

- CnOB does not modify segmentation.  
- CnOB does not assign roles.  
- CnOB does not perform smoothing.  
- CnOB is required for deterministic meaning: without constraints, IdOB cannot form identity.

---
