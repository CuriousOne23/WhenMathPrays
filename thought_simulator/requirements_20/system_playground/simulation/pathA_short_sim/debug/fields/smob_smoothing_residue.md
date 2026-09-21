# **smob_smoothing_residue.md — SmOB Smoothing Residue Field**

## **1. Definition**  
`smob_smoothing_residue` records the **leftover structural material** that SmOB could *not* stabilize during basin‑level smoothing.

It is **not**:

- SOB residue  
- SROB residue  
- CnOB residue  
- cumulative residue from the entire pipeline  

It is **only** the residue produced by **SmOB’s basin operations**, after:

- adjacency smoothing  
- continuity smoothing  
- role‑alignment smoothing  
- segment‑alignment smoothing  
- basin compression smoothing  

SmOB residue represents **unstabilized semantic‑adjacent signals** that must be passed to IdOB separately.

---

## **2. Token‑Level Intuition (Why This Field Exists)**  
Tokens do **not** contain smoothing residue.

Example tokens:
```
['He', 'might', 'be', 'somewhere']
```

Token intuition:
- “might” → modality  
- “somewhere” → underspecification  

But the simulator must **prove** these relationships structurally.

CnOB produces residue:
```
['modality_cue', 'underspecification_adjacent']
```

SmOB tries to stabilize both.  
If SmOB cannot stabilize one of them, it becomes **smoothing_residue**.

This field is the structured‑world representation of **what SmOB could not fix**.

For a full walkthrough from tokens → segments → roles → constraints → basin, see:  
**[Appendix X — Token‑to‑Structure Bridge](../primitives/appendix_x_token_to_structure_bridge.md)**

---

## **3. Structured‑World Meaning**  
In the structured world, `smob_smoothing_residue` is a **list of unresolved adjacency signals** remaining after SmOB applies smoothing operations.

Examples include:

- `underspecification_adjacent`  
- `conflict_adjacent`  
- `modality_cue` (if unstable)  
- `state_adjacent` (rare)  
- `locative_adjacent` (rare)  

These are **not errors** — they are **signals** that IdOB must consider when forming identity.

SmOB residue is **distinct** from CnOB residue:

- **CnOB residue** → constraint failures  
- **SmOB residue** → basin smoothing failures  

IdOB needs both.

---

## **4. Allowed Values**  
SmOB residue may include any unresolved adjacency cue, including:

- **underspecification_adjacent**  
- **conflict_adjacent**  
- **modality_cue**  
- **state_adjacent**  
- **locative_adjacent**  
- **descriptive_adjacent**  

These correspond to the adjacency geometries defined in your dictionaries.

---

## **5. Effects Across Primitives**

### **SmOB**
- produces smoothing_residue when basin smoothing cannot stabilize all cues  
- determines which cues IdOB can use  
- influences semantic_core stability  

### **IdOB**
- consumes smoothing_residue  
- determines whether identity_geometry can be formed  
- influences truth_relation stability  
- may produce identity_notes indicating unresolved adjacency  

SmOB residue is one of the strongest predictors of **identity uncertainty**.

---

## **6. Examples (Structured‑World)**  
These examples match your debug output style.

### **Example 1 — Continuity Smoothing**
```
smoothing_operations: ['continuity_smoothing']
semantic_adjacent_cues: ['modality_cue']
smob_smoothing_residue: ['underspecification_adjacent']
```

### **Example 2 — Basin Compression Smoothing**
```
smoothing_operations: ['basin_compression_smoothing']
semantic_adjacent_cues: ['modality_cue', 'conflict_adjacent']
smob_smoothing_residue: ['underspecification_adjacent']
```

### **Example 3 — No Residue**
```
smoothing_operations: ['segment_smoothing']
semantic_adjacent_cues: ['locative_adjacent']
smob_smoothing_residue: []
```

---

## **7. Token‑to‑Structure Comparison Example**

### **Token view**
> “He might be somewhere.”  
You intuitively know:
- modality (“might”)  
- underspecification (“somewhere”)  

### **Structured view**
SOB:
```
segments = ['NP', 'VP']
```
SROB:
```
roles = {'NP': 'entity', 'VP': 'state'}
```
CnOB:
```
residue = ['modality_cue', 'underspecification_adjacent']
```
SmOB:
```
smoothing_operations = ['continuity_smoothing']
semantic_adjacent_cues = ['modality_cue']
smob_smoothing_residue = ['underspecification_adjacent']
```

This shows how token intuition becomes basin residue.

For full examples across all primitives, see:  
**[Appendix X — Token‑to‑Structure Bridge](../primitives/appendix_x_token_to_structure_bridge.md)**

---
