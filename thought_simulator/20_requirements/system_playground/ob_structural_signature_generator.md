# ob_structural_signature_generator.md
**Revision:** 1.0 (Initial Proposal)  
**Date:** 2026-06-20  
**Status:** Proposal – For Review by CuriousOne23 & CP  

---

## 1. Purpose

This document proposes the addition of a new, small, focused primitive called the **Structural Signature Generator**.

Its sole responsibility is to take the final output of the OB pipeline (SmOB) and produce a compact, consistent **structural vector** (signature) that can be used for efficient similarity comparison and routing in RB.

---

## 2. Why This Is Needed

As we develop the routing and reuse capabilities of TS, we need an efficient way to determine how similar a new input is to previously processed OBs.

The current design gives us excellent structural information through the OB pipeline, but we do not yet have a clean, standardized way to turn that structural information into a comparable form for distance calculations.

Without this capability, routing and structural reuse would be inefficient or overly complex.

---

## 3. Design Principles

This new block must follow the core TS principle:

> **Each block should have one clear, narrow responsibility.**  
> Complexity should come from composition, not from making any single block complex.

Therefore, the Structural Signature Generator should:
- Be small and focused
- Have a single, well-defined job
- Not perform semantic interpretation
- Not modify the core OB pipeline
- Be easy to understand and maintain

---

## 4. Proposed Position in the Pipeline

**Recommended placement:** Immediately after SmOB.

**Pipeline flow:**

1. Raw Input
2. Message Correction (IIInB)
3. SOB → SROB → CnOB → SmOB
4. **Structural Signature Generator** ← New block here
5. RB (routing, similarity search, reuse logic)

This placement ensures the signature is generated from the **final, refined structural output** of the OB pipeline.

---

## 5. Responsibilities of the Structural Signature Generator

The block should:

- Accept the final `SEMANTIC_SKELETON` (or a defined subset of it) as input
- Produce a compact, consistent structural vector (the signature)
- Be deterministic and reproducible
- Remain strictly structural (no semantic interpretation)
- Be versionable (support future improvements to how signatures are generated)

It should **not**:
- Perform any part of the OB pipeline
- Make semantic decisions
- Modify the residue or hooks
- Be responsible for routing logic itself

---

## 6. Benefits

- Enables efficient structural similarity search for RB routing
- Supports future capabilities such as structural reuse and caching
- Keeps the core OB layers clean and focused on their primary jobs
- Provides a clean, testable interface between the structural and routing layers
- Allows independent evolution of how signatures are generated without changing the OB pipeline

---

## 7. Open Questions for Discussion

1. Should this block take the full `SEMANTIC_SKELETON` as input, or only a curated subset?
2. What should the initial vector representation look like? (sparse feature vector, small dense embedding, etc.)
3. Should we start with a simpler method (e.g., weighted feature bag) and evolve to cosine similarity later?
4. How should versioning of the signature generation logic be handled?
5. Should this block be optional in early implementations, or required from the start?

---

## 8. Recommendation

I recommend we create this as a **new, small, dedicated primitive** rather than embedding the logic inside SmOB or RB. This keeps the architecture clean and aligned with the principle of focused, composable blocks.

---

**End of Proposal**
