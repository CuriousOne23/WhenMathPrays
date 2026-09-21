# **struct_segments.md — Structural Segments Field**

## **1. Definition**  
`struct_segments` records the **segments** produced by **SOB (Segment Observation Block)**.  
Segments are the simulator’s **first structured representation** of an utterance.

A segment is a **group of tokens** that forms a functional unit such as:

- WQ (interrogative head)  
- NP (noun phrase / entity)  
- LOC (locative modifier)  
- VP / predicate  
- MOD (modifier)  

Segments are **not tokens**.  
They are **structural groupings** created by SOB using segmentation geometry.

This field reflects the simulator’s evaluation of **segment geometry**, which determines how the utterance will be interpreted by all downstream primitives.

---

## **2. Token‑Level Intuition (Why This Field Exists)**  
Tokens alone do **not** contain segments.

Example tokens:
```
['Where', 'is', 'the', 'book', 'on', 'the', 'table', '?']
```

Token intuition:
- “Where” feels like the question head  
- “the book” feels like a noun phrase  
- “on the table” feels like a location modifier  

But the simulator cannot rely on intuition.  
It must **derive segments structurally**.

`struct_segments` is the structured‑world representation of those intuitive groupings.

For a full walkthrough from tokens → segments → roles, see:  
**Appendix X — Token‑to‑Structure Bridge**

---

## **3. Structured‑World Meaning**  
In the structured world, `struct_segments` is a **list of segment labels** produced by SOB.

Example:
```
struct_segments = ['WQ', 'NP', 'LOC']
```

Each segment corresponds to a **token group**:

```
segment_tokens = {
  'WQ': ['Where'],
  'NP': ['the', 'book'],
  'LOC': ['on', 'the', 'table']
}
```

Segments determine:

- which roles can be assigned (SROB)  
- which constraints apply (CnOB)  
- which adjacency cues are possible (SmOB)  
- which identity geometries are valid (IdOB)

Segments are the **foundation** of the structured world.

---

## **4. Allowed Values**  
Your simulator defines the following allowed segment classes:

- **WQ** — interrogative head  
- **NP** — noun phrase / entity  
- **LOC** — locative modifier  
- **VP** — predicate / verb phrase  
- **MOD** — modifier  
- **ARG** — argument segment  

These are the **canonical segment types**.

Specific segment labels (e.g., `WQ`, `NP`, `LOC`) map into these classes.

---

## **5. Effects Across Primitives**

### **SOB**
- produces segments  
- determines segment boundaries  
- creates segment_tokens  

### **SROB**
- assigns roles based on segment type  
- activates role geometry  

### **CnOB**
- evaluates constraints between segments  
- adjacency and compatibility depend on segment layout  

### **SmOB**
- extracts semantic‑adjacent cues from segment relationships  
- performs basin smoothing based on segment adjacency  

### **IdOB**
- uses segments to determine semantic_core  
- segments influence identity_geometry  
- segments influence truth_relation stability  

Segments are the **structural backbone** of the entire simulator.

---

## **6. Examples (Structured‑World)**  
These examples match your debug output style.

### **Example 1 — SOB Segmentation**
```
SOB fired:
  struct_segments = ['WQ', 'NP', 'LOC']
  segment_tokens = {
    'WQ': ['Where'],
    'NP': ['the', 'book'],
    'LOC': ['on', 'the', 'table']
  }
```

### **Example 2 — Segments Influencing Identity**
```
IdOB fired:
  struct_segments = ['NP', 'LOC']
  semantic_core = ['entity', 'locative_modifier']
  identity_geometry = referential_identity
```

---

## **7. Token‑to‑Structure Comparison Example**

### **Token view**
> “the book on the table”  
You intuitively know:
- “the book” → entity  
- “on the table” → location modifier  

### **Structured view**
SOB:
```
struct_segments = ['NP', 'LOC']
segment_tokens = {
  'NP': ['the', 'book'],
  'LOC': ['on', 'the', 'table']
}
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

This shows how token intuition becomes structured segmentation.

For full examples across all primitives, see:  
[Appendix X — Token‑to‑Structure Bridge](appendix_x_token_to_structure_bridge.md) 

---



