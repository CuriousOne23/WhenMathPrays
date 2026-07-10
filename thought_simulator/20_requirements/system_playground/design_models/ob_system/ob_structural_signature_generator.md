# OB Structural Signature Generator
**ob_structural_signature_generator.md**  
**Revision:** 1.3 (Path A Positioning Corrected)  
**Date:** 2026-06-20  
**Status:** Working Draft – For Review by CuriousOne23 & CP  

---

### 1. Purpose

This document defines the **Structural Signature Generator** — a small, single-responsibility block that converts the final output of the SmOB layer into a compact, stable vector suitable for cosine similarity and RB routing.

Its only job is **structural compression**. It performs no tokenization, no semantic analysis, and no routing decisions.

### 2. Architectural Positioning (Path A)

```
IIInB (Message Correction)
   ↓
SOB → SROB → CnOB → SmOB     ← Full OB pipeline (structural analysis)
   ↓
**Structural Signature Generator**   ← New block
   ↓
RB‑prm (routing decision)
```

- The OB pipeline ends at SmOB.
- The Structural Signature Generator runs immediately after SmOB on **Path A**.
- It feeds directly into RB‑prm.
- It does **not** interact with RTU‑prm, RBU‑prm, TR‑prm, CIL, or any routing-layer primitives.

### 3. Core Principles

- Strictly operates on **structural output** from SmOB (never on raw text).
- Produces a **deterministic**, **stable**, and **versioned** vector.  
  The Structural Signature Generator must be a pure function: no randomness, no external state, no semantic interpretation.
- Handles natural correlations between structural features gracefully.
- Must preserve routing-critical structure (signature, residue, bindings, entailment edges) without aggressive loss.
- Must be lightweight and efficient.

### 4. Input & Output

**Input:** `STRUCTURAL_SKELETON` (from SmOB)  
**Output:** `STRUCTURAL_SIGNATURE`

```markdown
STRUCTURAL_SIGNATURE {
  version: SignatureVersion
  vector: FloatVector
  metadata: {
    source_smob_version,
    ruleset_ids,
    entropy_estimate,
    timestamp
  }
}
```

### 5. High-Level Design

The Signature Generator will:

1. Extract relevant structural features from SmOB output.
2. Apply weighting and normalization.
3. Convert the features into a consistent vector representation.
4. Produce a versioned signature suitable for cosine similarity in RB‑prm.

### 6. Why This Design

- Keeps OB focused on deep structural analysis.
- Keeps the Signature Generator focused purely on compression.
- Allows RB to perform fast similarity comparisons.
- Supports future optimizations (caching, selective processing, reuse).

### 7. Open Questions for Discussion

- Optimal vector dimensionality and sparsity strategy
- Feature weighting scheme
- Versioning strategy for signatures

---

**End of Revision 1.3**

---
