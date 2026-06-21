# OB Structural Signature Generator
**ob_structural_signature_generator.md**  
**Revision:** 1.2 (Aligned & Polished)  
**Date:** 2026-06-20  
**Status:** Working Draft – For Review by CuriousOne23 & CP  

---

### 1. Purpose

This document defines the **Structural Signature Generator** — a small, single-responsibility block that converts the final output of the SmOB layer into a compact, stable vector suitable for cosine similarity and RB routing.

Its only job is **structural compression**, not tokenization, not semantic analysis, and not routing.

### 2. Architectural Positioning

```
Raw Input
   ↓
Message Correction (IIInB)
   ↓
SOB → SROB → CnOB → SmOB   ← Full OB pipeline (structural analysis)
   ↓
**Structural Signature Generator**   ← New block
   ↓
RB (routing, similarity, reuse, caching)
```

- The OB pipeline ends at SmOB.
- The Signature Generator is the entry point into RB.
- This keeps responsibilities clean and respects the pre-semantic boundary.

### 3. Core Principles

- Strictly operates on **structural output** from SmOB (never on raw text).
- Produces a **deterministic**, **stable**, and **versioned** vector.  
  **The Structural Signature Generator must be a pure function**: no randomness, no external state, no semantic interpretation.
- Handles natural correlations between structural features gracefully.
- Must preserve routing-critical structure (signature, residue, bindings, entailment edges) without aggressive loss.
- Must support versioning and extensibility.
- Must be lightweight and efficient.

### 4. Input & Output

**Input:** `STRUCTURAL_SKELETON` (from SmOB)  
**Output:** `STRUCTURAL_SIGNATURE`

```markdown
STRUCTURAL_SIGNATURE {
  version: SignatureVersion
  vector: FloatVector          // dense or sparse vector
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

1. Extract relevant structural features from SmOB output (tags, constraints, residue, bindings, etc.).
2. Apply weighting and normalization.
3. Convert the features into a consistent vector representation.
4. Produce a versioned signature suitable for cosine similarity.

No text tokenization occurs here — all input comes from the already-processed structural representation.

### 6. Why This Design

- Keeps OB focused on deep structural analysis.
- Keeps the Signature Generator focused on compression.
- Allows RB to do fast similarity comparisons without heavy computation.
- Supports future optimizations (caching, selective processing, reuse) without changing core OB.

### 7. Open Questions for Discussion

- Optimal vector dimensionality and sparsity strategy
- Feature weighting scheme
- Versioning strategy for signatures
- Whether to support both dense and sparse vectors

---

**End of Revision 1.2**

---

---

**Jeff —** This should now be well-aligned with CP’s vision. Would you like any changes before we lock it, or should we move on?
