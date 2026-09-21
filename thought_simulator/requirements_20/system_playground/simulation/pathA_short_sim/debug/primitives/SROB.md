# **SROB.md — Segment Role Observation Block**  
### *Path‑A Short Simulator Primitive Documentation*

## **1. Definition**  
The **Segment Role Observation Block (SROB)** assigns **functional roles** to segments produced by SOB. These roles determine how each segment participates in dependency formation, constraint evaluation, smoothing, and identity formation.

SROB evaluates **role geometry** and aligns structural units with functional patterns such as **head**, **modifier**, **predicate**, or **argument**.  
This matches the intent described in your current file: SROB “assigns functional roles to segments” and “evaluates role geometry”.

---

## **2. Purpose and Function**

SROB answers the question:

> **“What functional role does each segment play in the utterance?”**

SROB provides the functional backbone for:

- constraint evaluation (CnOB)  
- semantic cue propagation (SmOB)  
- identity confirmation (IdOB)  

This aligns with your existing description that SROB “determines how segments participate in dependency formation” and “shapes semantic cue propagation”.
---

## **3. Allowed Role Values**

SROB may assign any of the following roles:

- **head**  
- **modifier**  
- **predicate**  
- **argument**

---

## **4. Structural Variables Filled by SROB (Local View)**  
SROB is the second primitive in the Path‑A pipeline.  
It fills **only** the functional role layer.

For the **full IdOB structural envelope**, see:  
**`IdOB.md — Section 4: IdOB Structural Envelope (Canonical)`**

### **4.1 Structural Origin Mini‑Table (SROB View)**

| Structural Term          | Filled by SROB? | Notes |
|--------------------------|----------------|-------|
| **segments**             | ✘              | Provided by SOB. SROB does not modify segmentation. |
| **segment_tokens**       | ✘              | Provided by SOB. |
| **roles**                | ✔              | **Primary output of SROB** — assigns functional roles (head, modifier, predicate, argument). |
| **constraints_matched**  | ✘              | Determined by CnOB. SROB only prepares role geometry for constraint evaluation. |
| **residue**              | ✘              | Produced by CnOB. |
| **smoothing_operations** | ✘              | Produced only by SmOB. |
| **smoothing_residue**    | ✘              | Produced only by SmOB. |
| **semantic_adjacent_cues** | ✘            | Produced only by SmOB. |
| **semantic_core**        | ✘              | Constructed by IdOB. |
| **truth_relation**       | ✘              | Determined by IdOB. |
| **token_relations**      | ✘              | Determined by IdOB. |
| **ob_set_notes**         | ✔              | SROB may add notes about role geometry activation. |

### **4.2 Summary**

SROB fills:

- `roles`  
- `ob_set_notes` (role‑related notes)

All other structural, relational, smoothing, and semantic variables are filled by downstream primitives:

```
SOB → SROB → CnOB → SmOB → IdOB
```

---

## **5. Effects**

SROB produces the following effects (aligned with your current file):

- activates role pattern matching for constraint evaluation in **CnOB**   
- shapes semantic cue propagation for **SmOB** 
- influences identity confirmation pathways for **IdOB** 
- constrains segment geometry interpretation for **SOB** (role feedback loop)

---

## **6. Examples**

Examples adapted from your current SROB.md:

- `"SROB fired: role_geometry=head, struct_roles=head"`
- `"SROB fired: role_geometry=modifier, semantic_adjacent_cues=adjacent_cue"`

These illustrate role assignment and semantic cue propagation.

---

## **7. Notes**

- SROB does not change segmentation.  
- SROB does not evaluate constraints.  
- SROB does not perform smoothing.  
- SROB is required for deterministic meaning: without roles, IdOB cannot form identity.

---
