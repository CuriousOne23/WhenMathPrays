# **appendix_x_token_to_structure_bridge.md**  
### *A shared appendix for SOB, SROB, CnOB, SmOB, and IdOB*

This appendix is the **single, authoritative bridge** between:

- the **token world** (intuitive, human‑readable)  
- the **structured world** (segments, roles, constraints, basin, identity)  

Every primitive in the Path‑A short simulator points here for:

- definitions  
- structural walkthroughs  
- examples  
- comparisons between token‑level intuition and structured‑level function  

This appendix ensures that readers who only understand tokens can still understand the structured world.

---

# **0. Overview: Why This Appendix Exists**

Tokens are intuitive.  
Structure is not.

The simulator primitives operate entirely in the structured world, but humans think in tokens.  
This appendix shows **how tokens become structure**, and how each primitive’s structural function works.

Pipeline:

```
Tokens
 → SOB (segments)
 → SROB (roles)
 → CnOB (constraints + residue)
 → SmOB (semantic-adjacent cues + basin smoothing)
 → IdOB (identity formation)
```

Each primitive transforms the representation.  
This appendix shows that transformation clearly.

---

# **1. Starting at Tokens**

Take a simple utterance:

> **“Where is the book on the table?”**

Tokens:
```
['Where', 'is', 'the', 'book', 'on', 'the', 'table', '?']
```

Tokens have:

- no structure  
- no roles  
- no constraints  
- no adjacency  
- no identity  

Everything the simulator does must be built on top of tokens.

---

# **2. SOB — From Tokens → Segments**

SOB groups tokens into [segments](../fields/struct_segments.md) using segment geometry.

Example segmentation:
```
segments = ['WQ', 'NP', 'LOC']
segment_tokens = {
  'WQ': ['Where'],
  'NP': ['the', 'book'],
  'LOC': ['on', 'the', 'table']
}
```

### Token intuition
You see:
- “Where” → question word  
- “the book” → thing being asked about  
- “on the table” → location  

### Structured world
SOB sees:
- WQ segment  
- NP segment  
- LOC segment  

SOB’s structural function:
- **define segmentation geometry**  
- **produce segment_tokens**  
- **produce ob_set_notes**  

---

# **3. SROB — From Segments → Roles**

SROB assigns **functional roles** to segments.

Example:
```
roles = {
  'WQ': 'interrogative_head',
  'NP': 'entity',
  'LOC': 'locative_modifier'
}
```

### Token intuition
You see:
- “Where” → the question head  
- “the book” → the entity  
- “on the table” → a modifier  

### Structured world
SROB sees:
- interrogative_head  
- entity  
- locative_modifier  

SROB’s structural function:
- **assign roles**  
- **activate role geometry**  
- **produce ob_set_notes**  

---

# **4. CnOB — From Roles → Constraints**

CnOB checks whether segment + role combinations satisfy structural rules.

Example residue:
```
residue = ['interrogative_scope', 'locative_adjacent']
```

### Token intuition
You see:
- The question applies to the whole clause  
- The location modifies the entity  

### Structured world
CnOB sees:
- interrogative scope not fully stabilized  
- locative adjacency not fully stabilized  

CnOB’s structural function:
- **match constraints**  
- **produce constraint residue**  
- **produce ob_set_notes**  

---

# **5. SmOB — From Constraints → Basin Stabilization**

SmOB receives residue from CnOB and performs:

- semantic‑adjacent cue extraction  
- basin‑level smoothing  
- deterministic pre‑semantic compression  

Example:
```
smoothing_operations: ['adjacency_smoothing']
semantic_adjacent_cues: ['interrogative_scope', 'state_adjacent']
smoothing_residue: []
```

### Token intuition
You see:
- “Where” → question  
- “is” → state  
- “on the table” → location  

### Structured world
SmOB sees:
- interrogative_scope adjacency  
- state adjacency  
- no leftover residue  

SmOB’s structural function:
- **extract semantic‑adjacent cues**  
- **perform basin smoothing**  
- **produce smoothing_residue**  
- **produce ob_set_notes**  

---

# **6. IdOB — From Basin → Identity**

IdOB forms:

- semantic_core  
- truth_relation  
- identity_geometry  
- identity_packet  

Example:
```
identity_geometry = referential_identity
semantic_core = ['entity', 'locative_modifier']
truth_relation = 'interrogative'
```

### Token intuition
You see:
- It’s a question  
- About an entity  
- With a location  

### Structured world
IdOB sees:
- referential identity  
- interrogative truth mode  
- stable semantic core  

IdOB’s structural function:
- **form identity**  
- **determine truth_relation**  
- **produce identity_packet**  

---

# **7. Side‑by‑Side Comparison (Token vs Structure)**

| Stage | Token View | Structured View | Primitive Output |
|-------|------------|-----------------|------------------|
| SOB | “Where / the book / on the table” | WQ, NP, LOC segments | segments, segment_tokens |
| SROB | “question / entity / modifier” | interrogative_head, entity, locative_modifier | roles |
| CnOB | “question applies to clause” | interrogative_scope residue | constraints_matched, residue |
| SmOB | “semantic adjacency” | semantic_adjacent_cues | smoothing_operations, smoothing_residue |
| IdOB | “identity of the question” | referential_identity | identity_geometry, semantic_core |

This table is the **core bridge** between intuition and structure.

---

# **8. Examples for Each Primitive**

### **8.1 SOB Example**
Tokens:
```
['Where', 'is', 'the', 'book']
```
Segments:
```
['WQ', 'NP']
```

### **8.2 SROB Example**
Roles:
```
WQ → interrogative_head
NP → entity
```

### **8.3 CnOB Example**
Residue:
```
['interrogative_scope']
```

### **8.4 SmOB Example**
Basin:
```
semantic_adjacent_cues: ['interrogative_scope']
smoothing_residue: []
```

### **8.5 IdOB Example**
Identity:
```
identity_geometry: referential_identity
truth_relation: interrogative
```

---

# **9. Glossary of Structural Terms**

### **segments**
Structural units created by SOB.

### **roles**
Functional assignments created by SROB.

### **constraints_matched**
Structural rules satisfied by CnOB.

### **residue**
Leftover structural material from CnOB.

### **semantic_adjacent_cues**
Pre‑semantic signals extracted by SmOB.

### **smoothing_operations**
Basin‑level stabilization actions.

### **smoothing_residue**
Leftover basin material after SmOB smoothing.

### **semantic_core**
Identity‑relevant semantic structure formed by IdOB.

### **truth_relation**
Interrogative, declarative, or unknown.

### **identity_geometry**
Referential, structural, semantic, or packet identity.

---
