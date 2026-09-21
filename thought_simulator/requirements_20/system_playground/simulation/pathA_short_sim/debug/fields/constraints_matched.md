# **constraints_matched.md — Constraint Geometry Match Field**

## **1. Definition**  
`constraints_matched` records **which constraint geometries were successfully satisfied** during interpretation.  
These constraints operate in the **structured world** (segments, roles, adjacency, compatibility), not at the token level.

When CnOB evaluates segment–role combinations, it checks whether the utterance satisfies:

- structural rules  
- adjacency rules  
- compatibility rules  
- continuity rules  

If a rule is satisfied, it is recorded in `constraints_matched`.

This field is the simulator’s indicator of **structural coherence** and determines whether CnOB can activate successfully.  
It also influences downstream primitives (SmOB, IdOB).

---

## **2. Token‑Level Intuition (Why This Field Exists)**  
Tokens alone do **not** contain constraints.  
Constraints emerge only after tokens are transformed into:

- **segments** (SOB)  
- **roles** (SROB)  
- **constraint geometry** (CnOB)

Example token intuition:

> “Where is the book on the table?”  
You intuitively know:
- “Where” applies to the whole clause → interrogative scope  
- “on the table” modifies “book” → locative adjacency  

But the simulator must **prove** these relationships structurally.

`constraints_matched` is the record of which structural proofs succeeded.

For a full walkthrough from tokens → structure → constraints, see:  
**Appendix X — Token‑to‑Structure Bridge**

---

## **3. Structured‑World Meaning**  
In the structured world, `constraints_matched` is a **set of constraint geometries** that were successfully matched.

### **allowed_values**  
- **adjacency_rule**  
- **compatibility_rule**  
- **structural_rule**  
- **continuity_rule**

These correspond to the four constraint geometries defined in your dictionaries.

### What each means structurally  
- **adjacency_rule** — segments are adjacent in a way that satisfies constraint geometry  
- **compatibility_rule** — roles are compatible (e.g., NP + LOC modifier)  
- **structural_rule** — segment ordering and grouping satisfy structural constraints  
- **continuity_rule** — no discontinuity in segment–role flow (e.g., interrogative scope continuity)

---

## **4. Effects Across Primitives**  
`constraints_matched` influences every primitive downstream from CnOB:

- **CnOB**  
  - determines whether constraint geometry activates  
  - governs constraint satisfaction envelopes  

- **SOB & SROB**  
  - restricts segment–role combinations  
  - prevents illegal segment/role patterns  

- **SmOB**  
  - shapes basin smoothing requirements  
  - determines which semantic‑adjacent cues can be extracted  

- **IdOB**  
  - influences identity confirmation  
  - affects truth‑relation determination  

This field is one of the simulator’s **structural backbone signals**.

---

## **5. Examples (Structured‑World)**  
These examples reflect the content and style of your debug output and match the patterns shown in your current tab   [Current page](citation-section://1147020954/3).

### **Example 1 — CnOB success**
```
CnOB matched: constraints_matched=compatibility_rule, role_geometry=argument
```
Meaning:
- The argument role is compatible with the segment geometry.
- Constraint geometry activated successfully.

### **Example 2 — Upstream primitive blocked**
```
SOB blocked: constraints_matched=adjacency_rule not satisfied
```
Meaning:
- SOB segmentation failed because adjacency constraints were violated.
- CnOB cannot activate.

---

## **6. Token‑to‑Structure Comparison Example**  
To help readers who only understand tokens:

### **Token view**
> “the book on the table”  
You intuitively know:
- “on the table” modifies “book”  
- adjacency is valid  

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
constraints_matched = ['adjacency_rule', 'compatibility_rule']
```

This shows how token intuition becomes structured constraint geometry.

For full examples across all primitives, see:  
**Appendix X — Token‑to‑Structure Bridge**

---

## **7. Cross‑Reference**  
For a complete walkthrough from tokens → segments → roles → constraints → basin → identity, see:

See [Appendix X — Token‑to‑Structure Bridge](appendix_x_token_to_structure_bridge.md)  

This appendix provides examples for every field, including `constraints_matched`.
