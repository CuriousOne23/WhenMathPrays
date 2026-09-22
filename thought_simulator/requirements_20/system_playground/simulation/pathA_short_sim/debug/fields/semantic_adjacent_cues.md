# **semantic_adjacent_cues.md — Semantic‑Adjacent Cue Field**

## **1. Definition**  
`semantic_adjacent_cues` records **meaning‑bearing signals** that arise from **adjacency relationships** between segments or roles.  
These cues are extracted by **SmOB** and represent how **semantic continuity** propagates through structural geometry.

This aligns with your page’s definition:  
> “meaning-bearing signals that arise from adjacency relationships between segments or roles”   [Current page](citation-section://1147020954/2)  
> “reflects how semantic cues propagate through structural geometry”   [Current page](citation-section://1147020954/3)  
> “captures semantic continuity across interpretation”   [Current page](citation-section://1147020954/4)

Semantic‑adjacent cues are **pre‑semantic**: they are not meaning themselves, but they are the **signals that meaning will be possible** once IdOB activates.

---

## **2. Token‑Level Intuition (Why This Field Exists)**  
Tokens alone do **not** contain semantic adjacency.  
Semantic adjacency emerges only after tokens are transformed into:

- segments (SOB)  
- roles (SROB)  
- constraint residue (CnOB)  
- basin smoothing (SmOB)

Example token intuition:

> “Where is the book on the table?”  
You intuitively know:
- “Where” → interrogative  
- “on the table” → locative modifier  
- “is” → state predicate  

But the simulator must **derive** these relationships structurally.

`semantic_adjacent_cues` is the structured‑world representation of those intuitive adjacency signals.

For a full walkthrough from tokens → structure → adjacency, see:  
**Appendix X — Token‑to‑Structure Bridge**

---

## **3. Structured‑World Meaning**  
In the structured world, `semantic_adjacent_cues` is a **list of adjacency‑derived signals** extracted by SmOB.

These signals indicate:

- interrogative adjacency  
- locative adjacency  
- state adjacency  
- modality adjacency  
- conflict adjacency  
- underspecification adjacency  
- descriptive adjacency  

They are **not semantic interpretations**.  
They are **semantic‑adjacent structural cues** that IdOB uses to form identity.

---

## **4. Allowed Values**  
Your page lists four allowed values:  
- **adjacent_cue**  
- **propagated_cue**  
- **structural_cue**  
- **semantic_cue**  
  [Current page](citation-section://1147020954/2)

These are **cue classes**, not specific cues.  
Specific cues include:

- `interrogative_scope`  
- `locative_adjacent`  
- `state_adjacent`  
- `modality_cue`  
- `conflict_adjacent`  
- `underspecification_adjacent`  
- `descriptive_adjacent`  

SmOB maps specific cues into one of the allowed classes.

---

## **5. Effects Across Primitives**  
Your page lists four effects:  
- activates semantic cue propagation for SmOB  
- influences constraint satisfaction for CnOB  
- shapes identity confirmation for IdOB  
- interacts with role geometry during SROB evaluation  
  [Current page](citation-section://1147020954/3)

Here is the structured explanation:

### **SmOB**
- Extracts semantic‑adjacent cues from CnOB residue  
- Uses cues to determine smoothing operations  
- Produces deterministic pre‑semantic representation

### **CnOB**
- Uses adjacency cues to evaluate constraint geometry  
- Some constraints require adjacency to be satisfied

### **SROB**
- Role geometry interacts with adjacency (e.g., modifier chains)

### **IdOB**
- Uses semantic‑adjacent cues to determine:  
  - truth_relation  
  - identity_geometry  
  - semantic_core stability  

Semantic‑adjacent cues are one of the strongest predictors of identity geometry.

---

## **6. Examples (Structured‑World)**  
Your page provides two examples:  
- “SmOB applied: semantic_adjacent_cues=adjacent_cue, role_geometry=modifier”   [Current page](citation-section://1147020954/5)  
- “IdOB fired: semantic_adjacent_cues=semantic_cue, identity_geometry=referential_identity”   [Current page](citation-section://1147020954/5)

Here are expanded versions consistent with your simulator:

### **Example 1 — SmOB Extraction**
```
SmOB applied:
  semantic_adjacent_cues = ['locative_adjacent']
  smoothing_operations = ['segment_smoothing']
  role_geometry = 'modifier'
```

### **Example 2 — IdOB Identity Formation**
```
IdOB fired:
  semantic_adjacent_cues = ['interrogative_scope']
  identity_geometry = referential_identity
  truth_relation = interrogative
```

---

## **7. Token‑to‑Structure Comparison Example**

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
IdOB:
```
identity_geometry = referential_identity
truth_relation = declarative
```

This shows how token intuition becomes structured adjacency.

For full examples across all primitives, see:  
[Appendix X — Token‑to‑Structure Bridge](../primitives/appendix_x_token_to_structure_bridge.md)  

---

