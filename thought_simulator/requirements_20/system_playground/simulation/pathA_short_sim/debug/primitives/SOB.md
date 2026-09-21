# **SOB.md — Segment Observation Block**  
### *Path‑A Short Simulator Primitive Documentation*

## **1. Definition**  
The **Segment Observation Block (SOB)** is the first primitive in the Path‑A short simulation chain. It performs structural segmentation of the input utterance and establishes the segment geometry that all downstream primitives depend on. SOB identifies admissible segment classes and constructs the structural envelope for role assignment, constraint matching, smoothing, and identity formation. 

SOB is responsible for answering the question:

> **“How is this utterance structurally divided?”**

This segmentation determines whether the simulator can proceed deterministically through SROB → CnOB → SmOB → IdOB.

---

## **2. Purpose and Function**

SOB evaluates:

- **segment geometry** (atomic, composite, recursive, discontinuous)  
- **segment class admissibility**  
- **structural envelope** for downstream primitives  
- **segment token grouping**  
- **structural residue** (if segmentation is incomplete)

These behaviors are consistent with the effects described in your existing SOB.md:  
- SOB constrains role geometry activation for SROB  
- SOB shapes constraint satisfaction envelopes for CnOB  
- SOB influences smoothing requirements for SmOB  
- SOB provides structural anchors for IdOB identity confirmation 

---

## **3. Allowed Segment Classes**  
SOB may classify segments into the following admissible classes: 

- `atomic_segment`  
- `composite_segment`  
- `recursive_segment`  
- `discontinuous_segment`

These classes correspond to the structural geometries defined in your segment dictionaries.

---

## **4. SOB Output Schema**

SOB produces a structured block in `debug_out.md` with the following fields:

### **segments**  
List of segment classes detected (e.g., `WQ`, `IQ`, `NP`).

### **segment_tokens**  
Token lists grouped by segment.

### **roles**  
Empty at SOB stage; filled by SROB.

### **constraints_matched**  
Empty at SOB stage; filled by CnOB.

### **residue**  
Structural residue from segmentation.

### **smoothing_residue**  
Empty at SOB stage.

### **smoothing_operations**  
Empty at SOB stage.

### **semantic_adjacent_cues**  
Empty at SOB stage.

### **semantic_core**  
Empty at SOB stage.

### **token_relations**  
Empty at SOB stage.

### **ob_set_notes**  
Human‑readable notes summarizing the segmentation.

---

## **5. Example (from your simulator)**  
This is the exact example you described — the one you want to appear when clicking SOB:

```
segments:
  - WQ
  - IQ
  - NP

segment_tokens:
  - ['why']
  - ['is']
  - ['the', 'sky', 'blue']

roles:
  - []

constraints_matched:
  - []

residue:
  - []

smoothing_residue:
  - []

smoothing_operations:
  - []

semantic_adjacent_cues:
  - []

semantic_core:
  - {}

token_relations:
  - []

ob_set_notes:
  - OB-Set: Segments = WQ, IQ, NP
  - OB-Set: Segment tokens = ['why'] | ['is'] | ['the', 'sky', 'blue']
```

This example is fully aligned with the SOB definition and the structural envelope described in your existing SOB.md. 

---

## **6. Notes**

- SOB is purely structural; it does not assign roles or meaning.  
- SOB success is a **hard requirement** for deterministic meaning.  
- If SOB fails (unknown tokens, unmatched segment patterns), IdOB sufficiency becomes impossible.  
- SOB output is the mnemonic anchor for debugging — clicking SOB should always show this schema and example.

---

## **7. Relationship to Downstream Primitives**

SOB → SROB  
SOB constrains which roles can be assigned.

SOB → CnOB  
SOB shapes the constraint satisfaction envelope.

SOB → SmOB  
SOB determines adjacency and smoothing requirements.

SOB → IdOB  
SOB provides the structural anchors for identity confirmation.

These relationships match the effects listed in your current SOB.md. 

---
