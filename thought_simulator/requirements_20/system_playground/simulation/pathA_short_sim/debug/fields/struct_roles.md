# **struct_roles.md — Structural Roles Field**

## **1. Definition**  
`struct_roles` records the **functional roles** assigned to segments by **SROB (Segment Role Observation Block)**.  
Roles describe **how each segment behaves** inside the structured world:

- which segment is the **head**  
- which segment is the **entity**  
- which segment is the **modifier**  
- which segment is the **predicate**  
- which segment is the **argument**

Roles are **not token labels**.  
They are **functional assignments** that emerge only after segmentation.

This field reflects the simulator’s evaluation of **role geometry**, which determines how segments participate in:

- constraint evaluation (CnOB)  
- adjacency and basin smoothing (SmOB)  
- identity formation (IdOB)

---

## **2. Token‑Level Intuition (Why This Field Exists)**  
Tokens alone do **not** contain roles.

Example tokens:
```
['Where', 'is', 'the', 'book', 'on', 'the', 'table', '?']
```

Token intuition:
- “Where” feels like the question head  
- “the book” feels like the entity  
- “on the table” feels like a modifier  
- “is” feels like a state predicate  

But the simulator cannot rely on intuition.  
It must **derive roles structurally**.

`struct_roles` is the structured‑world representation of those intuitive functional assignments.

For a full walkthrough from tokens → segments → roles, see:  
**Appendix X — Token‑to‑Structure Bridge**

---

## **3. Structured‑World Meaning**  
In the structured world, `struct_roles` is a **mapping** from segment → role.

Example:
```
struct_roles = {
  'WQ': 'interrogative_head',
  'NP': 'entity',
  'LOC': 'locative_modifier'
}
```

Roles determine:

- how segments interact  
- which constraints apply  
- which adjacency cues are possible  
- which identity geometries are valid  

Roles are the **functional backbone** of the structured world.

---

## **4. Allowed Values**  
Your simulator defines the following allowed role values:

- **head**  
- **modifier**  
- **predicate**  
- **argument**  

These are the **canonical role classes**.

Specific roles (e.g., `interrogative_head`, `locative_modifier`) map into these classes.

---

## **5. Effects Across Primitives**

### **SOB**
- segmentation determines which segments can receive roles

### **SROB**
- assigns roles  
- activates role geometry  
- produces role‑related notes

### **CnOB**
- uses roles to evaluate constraint geometry  
- certain constraints require specific role combinations (e.g., NP + LOC)

### **SmOB**
- role geometry influences adjacency smoothing  
- modifier chains often produce semantic‑adjacent cues

### **IdOB**
- uses roles to determine semantic_core  
- roles influence identity_geometry  
- roles influence truth_relation stability

Roles are one of the strongest predictors of identity formation.

---

## **6. Examples (Structured‑World)**  
These examples match your debug output style.

### **Example 1 — SROB Role Assignment**
```
SROB fired:
  struct_roles = {
    'NP': 'entity',
    'LOC': 'locative_modifier'
  }
  role_geometry = modifier
```

### **Example 2 — Role Geometry Influencing Identity**
```
IdOB fired:
  struct_roles = {
    'WQ': 'interrogative_head',
    'NP': 'entity'
  }
  identity_geometry = referential_identity
```

---

## **7. Token‑to‑Structure Comparison Example**

### **Token view**
> “the book on the table”  
You intuitively know:
- “the book” → entity  
- “on the table” → modifier  

### **Structured view**
SOB:
```
segments = ['NP', 'LOC']
```
SROB:
```
struct_roles = {
  'NP': 'entity',
  'LOC': 'locative_modifier'
}
```
CnOB:
```
constraints_matched = ['compatibility_rule']
```
SmOB:
```
semantic_adjacent_cues = ['locative_adjacent']
```
IdOB:
```
semantic_core = ['entity', 'locative_modifier']
identity_geometry = referential_identity
```

This shows how token intuition becomes structured role geometry.

For full examples across all primitives, see:  
[Appendix X — Token‑to‑Structure Bridge](appendix_x_token_to_structure_bridge.md) 

---
 
- **locative_modifier.md**  

Or update all field docs to reference Appendix X.
