# **struct_segments.md (Canonical Version)**

## **1. Purpose**
`struct_segments` is the **structured‑world segmentation field** produced by the SOB primitive.  
It represents the simulator’s first deterministic structural interpretation of the utterance.  
Downstream primitives (SROB → CnOB → SmOB → IdOB) rely on this field to assign roles, match constraints, propagate residue, and finalize identity geometry.

### **1.1 Source Geometry**
`segment_geometry` from [../dimensions/segment_geometry.md](../dimensions/segment_geometry.md).

---

## **2. Definition**
`struct_segments` is an **ordered list of segment labels**, each describing a structural unit of the utterance.  
These labels are **not linguistic tags** but **structured‑world abstractions** that encode functional geometry.

Example:
```
struct_segments: ['WQ', 'IQ', 'NP']
```

---

## **3. Segment Labels**
The simulator recognizes a small, deterministic set of segment labels.  
Typical values include:

- **WQ** — Wh‑question head  
- **IQ** — Interrogative auxiliary  
- **NP** — Noun phrase  
- **VP** — Verb phrase  
- **LOC** — Locative modifier  
- **MOD** — Modifier segment  
- **ARG** — Argument segment  

These labels are produced by SOB’s segmentation logic and are **stable across all primitives**.

---

## **4. Structured‑World Meaning**
Structured‑World Meaning consists of **two paired fields**:

### **4.1 struct_segments**  
The ordered list of segment labels.

### **4.2 segment_tokens**  
The token groups associated with each segment label.

Example:
```
struct_segments: ['WQ', 'IQ', 'NP']
segment_tokens: [['why'], ['is'], ['the', 'sky', 'blue']]
```

Notes:

- Punctuation (e.g., `?`) is **not** included in `segment_tokens`.  
  It functions as a **boundary marker**, not a structural unit.
- The pairing between `struct_segments` and `segment_tokens` is **deterministic** and preserved across all downstream primitives.

---

## **5. Downstream Usage**
`struct_segments` is consumed by:

- **SROB** — assigns roles to segments  
- **CnOB** — applies structural and adjacency constraints  
- **SmOB** — performs smoothing and adjacency cue propagation  
- **IdOB** — computes identity geometry, truth relation, and semantic core  

Because these primitives depend on segment geometry, `struct_segments` must be:

- deterministic  
- stable  
- identical across the entire ladder  
- reproducible under replay  

Your simulator now satisfies all of these requirements.

## 6. Notes for Debugging
- If this field is empty, downstream canonical fields are unreliable.
- Verify alignment with `segment_tokens` for the same segment labels.

---


