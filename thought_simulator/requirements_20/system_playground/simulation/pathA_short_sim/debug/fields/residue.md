# **residue.md — Structural Residue Field**

## **1. Definition**  
`residue` is the **leftover structural material** produced when a primitive cannot fully stabilize the structure it is responsible for.

Residue is **not an error**.  
It is a **signal** that:

- segmentation (SOB)  
- role assignment (SROB)  
- constraint geometry (CnOB)  
- basin smoothing (SmOB)  

left something **partially matched**, **unstable**, or **incomplete**.

Residue is always **primitive‑specific**:

- **SOB residue** → segmentation leftovers  
- **SROB residue** → role‑alignment leftovers  
- **CnOB residue** → constraint leftovers  
- **SmOB residue** → basin smoothing leftovers  

IdOB does **not** produce residue — it consumes it.

---

## **2. Token‑Level Intuition (Why Residue Exists)**  
Tokens alone do **not** contain residue.

Residue only appears **after tokens are transformed** into:

- segments (SOB)  
- roles (SROB)  
- constraints (CnOB)  
- semantic‑adjacent cues (SmOB)

Example token intuition:

> “Where is the book on the table?”  
You intuitively know:
- “Where” applies to the whole clause  
- “on the table” modifies “book”  

But the simulator must **prove** these relationships structurally.

If the structural proof is incomplete, residue is produced.

For a full walkthrough from tokens → structure → residue, see:  
**Appendix X — Token‑to‑Structure Bridge**

---

## **3. Structured‑World Meaning**  
Residue is a **list of structural signals** that were not fully stabilized by a primitive.

Examples from your debug_out.md :
- `interrogative_scope`  
- `locative_adjacent`  
- `modifier_chain`  
- `underspecification_adjacent`  
- `state_adjacent`  
- `conflict_adjacent`  
- `modality_cue`  

Residue is **not semantic**.  
It is **pre‑semantic structural material** that must be stabilized by downstream primitives.

---

## **4. Residue by Primitive (Structured‑World Breakdown)**

### **4.1 SOB Residue (Segmentation Residue)**  
Produced when segmentation geometry cannot fully group tokens.

Example:
```
residue = ['segment_boundary_uncertain']
```

### **4.2 SROB Residue (Role Residue)**  
Produced when role geometry cannot fully align segments with functional roles.

Example:
```
residue = ['modifier_chain']
```

### **4.3 CnOB Residue (Constraint Residue)**  
Produced when constraint geometry cannot fully stabilize adjacency or compatibility.

Examples:
```
residue = ['interrogative_scope', 'locative_adjacent']
```

### **4.4 SmOB Residue (Smoothing Residue)**  
Produced when basin smoothing cannot stabilize all semantic‑adjacent cues.

Example:
```
smoothing_residue = ['underspecification_adjacent']
```

SmOB residue is **distinct** from CnOB residue.

---

## **5. Effects Across the Simulator**

Residue influences every downstream primitive:

### **SROB**
- uses SOB residue to adjust role geometry

### **CnOB**
- uses SROB residue to evaluate constraints

### **SmOB**
- uses CnOB residue to extract semantic‑adjacent cues  
- produces its own smoothing_residue

### **IdOB**
- consumes all residue types  
- determines whether identity can be formed  
- determines truth_relation stability

Residue is the simulator’s **continuity signal**.

---

## **6. Allowed Residue Types**  
Residue is not a single value — it is a **set of structural leftovers**.

Common residue types include:

- **interrogative_scope**  
- **locative_adjacent**  
- **modifier_chain**  
- **state_adjacent**  
- **modality_cue**  
- **underspecification_adjacent**  
- **conflict_adjacent**  
- **segment_boundary_uncertain**  

These correspond to the structural geometries defined in your dictionaries.

---

## **7. Examples (Structured‑World)**  
These examples match your debug output style.

### **Example 1 — CnOB Residue**
```
CnOB residue: ['interrogative_scope', 'locative_adjacent']
```
Meaning:
- interrogative scope not fully stabilized  
- locative adjacency not fully stabilized  

### **Example 2 — SmOB Smoothing Residue**
```
SmOB smoothing_residue: ['underspecification_adjacent']
```
Meaning:
- basin smoothing could not stabilize underspecification  

### **Example 3 — SROB Role Residue**
```
SROB residue: ['modifier_chain']
```
Meaning:
- role alignment incomplete for NP + LOC chain  

---

## **8. Token‑to‑Structure Comparison Example**

### **Token view**
> “the book on the table”  
You intuitively know:
- NP + LOC adjacency  
- modifier chain is stable  

### **Structured view**
SOB:
```
segments = ['NP', 'LOC']
```
SROB:
```
roles = {'NP': 'entity', 'LOC': 'locative_modifier'}
```
CnOB:
```
residue = ['locative_adjacent']
```
SmOB:
```
semantic_adjacent_cues = ['locative_adjacent']
smoothing_residue = []
```

This shows how token intuition becomes structured residue.

For full examples across all primitives, see:  
[Appendix X — Token‑to‑Structure Bridge](../primitives/appendix_x_token_to_structure_bridge.md)  


