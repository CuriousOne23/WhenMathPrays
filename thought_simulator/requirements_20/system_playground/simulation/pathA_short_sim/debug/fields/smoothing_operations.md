# **smoothing_operations.md — Basin Smoothing Operations Field**

## **1. Definition**  
`smoothing_operations` records **which basin‑level stabilization actions SmOB performed** when processing structural residue from CnOB.

These operations are **not semantic**.  
They are **structural basin actions** that stabilize adjacency, continuity, role alignment, and segment alignment so that **semantic_adjacent_cues** can be extracted deterministically.

SmOB uses smoothing operations to convert:

```
CnOB residue → stable semantic-adjacent cues
```

and to produce:

- `semantic_adjacent_cues`  
- `smoothing_residue`  
- deterministic pre‑semantic compression  

---

## **2. Token‑Level Intuition (Why This Field Exists)**  
Tokens alone do **not** contain smoothing operations.

Example tokens:
```
['Where', 'is', 'the', 'book', 'on', 'the', 'table', '?']
```

Token intuition:
- “Where” → interrogative  
- “the book” → entity  
- “on the table” → location  
- “is” → state  

But the simulator must **prove** these relationships structurally.

SmOB receives structural residue such as:
```
['interrogative_scope', 'locative_adjacent']
```

Then SmOB applies **smoothing operations** to stabilize these adjacency signals.

`smoothing_operations` is the structured‑world record of those basin actions.

For a full walkthrough from tokens → segments → roles → constraints → basin, see:  
**Appendix X — Token‑to‑Structure Bridge**

---

## **3. Structured‑World Meaning**  
In the structured world, `smoothing_operations` is a **list of basin actions** SmOB performed to stabilize structural residue.

These operations include:

- **adjacency_smoothing**  
- **continuity_smoothing**  
- **role_smoothing**  
- **segment_smoothing**  
- **basin_compression_smoothing**

Each operation corresponds to a specific structural stabilization need.

### What each operation means structurally

- **adjacency_smoothing**  
  Stabilizes adjacency relationships (e.g., interrogative_scope, state_adjacent).

- **continuity_smoothing**  
  Stabilizes continuity breaks (e.g., modality_cue + underspecification_adjacent).

- **role_smoothing**  
  Stabilizes role alignment (e.g., modifier_chain).

- **segment_smoothing**  
  Stabilizes segment adjacency (e.g., NP ↔ LOC).

- **basin_compression_smoothing**  
  Catch‑all operation for mixed or ambiguous residue.

---

## **4. Allowed Values**  
Your simulator defines the following allowed smoothing operations:

- **adjacency_smoothing**  
- **continuity_smoothing**  
- **role_smoothing**  
- **segment_smoothing**  
- **basin_compression_smoothing**

These are the **canonical basin operations**.

---

## **5. Effects Across Primitives**

### **SmOB**
- Performs smoothing operations  
- Extracts semantic_adjacent_cues  
- Produces smoothing_residue  
- Generates deterministic pre‑semantic representation  

### **CnOB**
- Provides the residue that determines which smoothing operations are needed  

### **IdOB**
- Uses stabilized cues to form identity  
- Uses smoothing_residue to determine truth‑relation stability  

Smoothing operations are the **bridge** between constraint residue and semantic adjacency.

---

## **6. Examples (Structured‑World)**  
These examples match your debug output style.

### **Example 1 — Adjacency Smoothing**
```
smoothing_operations: ['adjacency_smoothing']
semantic_adjacent_cues: ['interrogative_scope', 'state_adjacent']
smoothing_residue: []
```

### **Example 2 — Continuity Smoothing**
```
smoothing_operations: ['continuity_smoothing']
semantic_adjacent_cues: ['modality_cue']
smoothing_residue: ['underspecification_adjacent']
```

### **Example 3 — Role Smoothing**
```
smoothing_operations: ['role_smoothing']
semantic_adjacent_cues: ['modifier_chain']
smoothing_residue: []
```

### **Example 4 — Segment Smoothing**
```
smoothing_operations: ['segment_smoothing']
semantic_adjacent_cues: ['locative_adjacent']
smoothing_residue: []
```

### **Example 5 — Basin Compression Smoothing**
```
smoothing_operations: ['basin_compression_smoothing']
semantic_adjacent_cues: ['modality_cue', 'conflict_adjacent']
smoothing_residue: ['underspecification_adjacent']
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
smoothing_operations = ['segment_smoothing']
semantic_adjacent_cues = ['locative_adjacent']
smoothing_residue = []
```

This shows how token intuition becomes basin smoothing operations.

For full examples across all primitives, see:  
**Appendix X — Token‑to‑Structure Bridge](../primitives/appendix_x_token_to_structure_bridge.md)**

---
