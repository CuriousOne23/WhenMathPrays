# **theoretical_utility_of_isc.md**  
### *Intent Scoring — Theoretical Utility, Placement, Necessity, and Function in Path‑A*  
### *Aligned with 20.40.050, ts_meaning_theory.md, and the Path‑A Upstream Pipeline*

---

# **1. Introduction**

The Intent Scoring primitive (ISc) is the **third primitive** in the Path‑A upstream pipeline:

```
CE → WrdNm → ISc → TPU → SOB → SROB → CnOB → SmOB → SSG → STPX → RBU → TR → RB → refinement loop → OuBA
```

ISc is responsible for computing **semantic intent scores** for the user’s turn.  
It transforms numeric encodings (from WrdNm) and surface metadata (from CE) into a **semantic‑intent profile** that TPU commits and OB‑Set consumes downstream.

Meaning theory defines:

> **Meaning = (what is stated) × (the context in which it is stated)**

ISc is the primitive that begins encoding **semantic intent** — the first semantic representation of “what is stated.”  
It does not compute meaning, context, continuity, or identity.  
It computes **semantic intent scores** that downstream primitives use to interpret the turn.

ISc is the **semantic origin** of Path‑A.

---

# **2. Placement of ISc in Path‑A**

ISc appears immediately after WrdNm:

```
CE → WrdNm → ISc → TPU → SOB → SROB → CnOB → SmOB → SSG → …
```

This placement is intentional:

- **Upstream**: ISc receives numeric encodings and lexical metadata.  
- **Downstream**: ISc provides semantic intent scores to TPU, which commits them into the TP.

ISc is the **first semantic representation** of the turn.

---

# **3. Why ISc Exists (Necessity)**

ISc is necessary because Path‑A requires:

### **1. Semantic intent scoring**  
ISc computes:

- semantic intent scores  
- semantic polarity  
- semantic shading  
- semantic modality  
- semantic emphasis  
- semantic conflict  
- semantic underspecification  

These scores are essential for:

- TPU → commit of semantic intent  
- IdOB → identity continuity  
- STPX → discourse normalization  
- RBU → routing arbitration  
- TR → truth‑relation mapping  
- RB → routing decisions  
- refinement loop → semantic refinement  

### **2. Semantic‑intent provenance**  
ISc records:

- semantic intent origin  
- semantic intent lineage  
- semantic intent continuity anchors  

These anchors are required for deterministic replay.

### **3. Semantic‑intent stability**  
ISc produces stable semantic intent scores that downstream primitives rely on.

### **4. Deterministic replay**  
Replay determinism requires:

- stable semantic scoring  
- stable semantic polarity  
- stable semantic modality  
- stable semantic shading  

ISc provides these.

### **5. Laptop‑scale cognition**  
ISc produces a bounded semantic‑intent representation that downstream primitives can operate on efficiently.

---

# **4. Inputs ISc Consumes**

ISc consumes:

### **4.1 WrdNm numeric encodings (read‑only)**  
- token_numeric  
- token_embedding  
- token_expression_numeric  
- token_base_numeric  

### **4.2 CE surface metadata (read‑only)**  
- lexical metadata  
- punctuation metadata  
- syntactic metadata  
- discourse metadata  

### **4.3 Contextual metadata (read‑only)**  
- continuity metadata  
- identity metadata  
- referent metadata  
- topic metadata  
- stance metadata  
- direction metadata  

### **4.4 Provenance metadata (read‑only)**  
- TPU commit metadata  
- previous turn lineage  
- semantic mode metadata  

ISc does **not** modify any upstream metadata.

---

# **5. What ISc Does (Function)**

ISc performs **three theoretical jobs**:

---

## **Job 1 — Semantic Intent Scoring**

ISc computes semantic intent scores from:

- numeric encodings  
- lexical metadata  
- syntactic boundaries  
- discourse markers  
- token expression metadata  

These scores include:

- semantic polarity  
- semantic modality  
- semantic emphasis  
- semantic shading  
- semantic conflict  
- semantic underspecification  

These scores are essential for:

- TPU → commit  
- IdOB → identity continuity  
- STPX → discourse normalization  
- RBU → routing arbitration  
- TR → truth‑relation mapping  
- RB → routing decisions  

---

## **Job 2 — Semantic Intent Profile Construction**

ISc constructs a **semantic intent profile**, including:

- semantic intent vector  
- semantic polarity vector  
- semantic modality vector  
- semantic emphasis vector  
- semantic conflict vector  
- semantic underspecification vector  

This profile is committed by TPU and consumed by:

- OB‑Set → structural meaning pipeline  
- STPX → discourse normalization  
- RBU → routing arbitration  
- TR → truth‑relation mapping  
- RB → routing decisions  

---

## **Job 3 — Semantic Intent Provenance**

ISc records:

- semantic intent origin  
- semantic intent lineage  
- semantic intent continuity anchors  

This provenance is essential for deterministic replay.

---

# **6. Outputs ISc Produces**

ISc writes:

- `TP.semantic.intent_scores`  
- `TP.semantic.intent_profile`  
- `TP.semantic.intent_polarity`  
- `TP.semantic.intent_modality`  
- `TP.semantic.intent_shading`  
- `TP.semantic.intent_conflict`  
- `TP.semantic.intent_underspecification`  
- `TP.semantic.intent_provenance`  

These outputs form the **semantic substrate** for TPU and OB‑Set.

---

# **7. Downstream Consumers of ISc Output**

ISc’s semantic intent scores and profile are consumed by:

### **TPU**  
Commits semantic intent into the TP.

### **SOB / SROB / CnOB / SmOB / SSG**  
Use semantic intent metadata for structural meaning.

### **STPX**  
Normalizes discourse structure using semantic intent.

### **RBU / TR / RB**  
Use semantic intent for routing and truth‑relation mapping.

### **IdOB**  
Uses semantic intent for identity continuity.

### **Refinement Loop**  
Uses semantic intent as the semantic baseline.

---

# **8. ISc and Meaning Theory**

Meaning theory defines:

> **Meaning = Stated × Context**

ISc encodes the **semantic portion** of the “stated” operand by:

- computing semantic intent  
- computing semantic polarity  
- computing semantic modality  
- computing semantic shading  
- computing semantic conflict  
- computing semantic underspecification  

This semantic‑intent formation is the **first semantic representation** of “what is stated.”

Downstream primitives refine the **context** operand until SSG produces the structural manifold.

Thus:

### ⭐ **ISc is the first step in making semantic intent computable.**

---

# **9. ISc and Deterministic Replay**

Replay determinism requires:

- stable semantic scoring  
- stable semantic polarity  
- stable semantic modality  
- stable semantic shading  
- stable semantic conflict  
- stable semantic underspecification  
- stable provenance  

ISc provides all of these.

Without ISc, replay determinism would fail at the semantic level.

---

# **10. ISc and Laptop‑Scale Cognition**

ISc enables laptop‑scale cognition by:

- producing bounded semantic intent scores  
- producing bounded semantic intent profiles  
- enabling efficient TPU commit  
- enabling efficient structural segmentation  
- enabling efficient constraint formation  
- enabling efficient semantic‑adjacent cue extraction  
- enabling efficient manifold construction  

ISc is the **first bounded semantic representation** of the turn.

---

# **11. Summary**

ISc is the **semantic origin** of the turn.

It is necessary because:

- meaning requires semantic intent  
- structural meaning requires semantic intent  
- routing requires semantic intent  
- truth‑relation mapping requires semantic intent  
- identity continuity requires semantic intent  
- replay determinism requires semantic intent stability  
- laptop‑scale cognition requires bounded semantic intent  

ISc consumes numeric encodings and surface metadata, produces semantic intent scores and profiles, and provides the semantic substrate for TPU and OB‑Set.

ISc is the **third step** in the Path‑A meaning pipeline.

---
