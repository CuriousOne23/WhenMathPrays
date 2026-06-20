# OB Pipeline Examples
**ob_pipeline_examples.md**  
**Revision:** 1.1 (Invariant‑Safe Structural Examples)  
**Date:** 2026‑06‑20  
**Status:** Stabilized Draft – Ready for Lock**

---

## 1. Purpose

This document provides concrete **end‑to‑end structural examples** of the OB pipeline:

**SOB → SROB → CnOB → SmOB**

The goals are to:

- Validate pipeline flow and invariants  
- Expose edge cases and ambiguity handling  
- Test monotonicity, residue formation, and routing readiness  
- Serve as a living test corpus for future changes  

Examples are intentionally minimal to moderate in complexity.

---

## 2. Core Validation Criteria (Per Example)

Each example is checked for:

- Strict pre‑semantic boundaries  
- Monotonic entropy reduction  
- No semantic leakage  
- Correct provenance and traceability  
- Proper uncertainty / gap propagation  
- RB‑ready output (`structural_signature`, `residue`, `bindings`)  

---

## 3. Example 1 — Minimal Clean Input

**Input:**  
`Hello world.`

### SOB Output (SOB_ATOM_SET)

- Atoms:  
  - TOKEN("Hello")  
  - TOKEN("world")  
  - PUNCT(".")  
- Tags:  
  - ADJACENT(Hello → world)  
  - PUNCT  
- Rhythm:  
  - EVEN_SPACING  

### SROB Output (SROB_GRAPH)

- Canonical span created  
- No rewrite rules triggered  
- `structural_signature` generated  

### CnOB Output (CONSTRAINT_LATTICE)

- No slot, ordering, adjacency, or closure constraints detected  

### SmOB Output (SEMANTIC_SKELETON)

- Slot Marker on full span  
- Anchor Points on each token  
- No uncertainty markers  
- Residue: structural atoms + edges  

**Validation:** Clean flow, no ambiguity, invariants satisfied.

---

## 4. Example 2 — Moderate Input with Repetition

**Input:**  
`The the quick quick brown fox.`

### SOB Output

- TOKEN("The") ×2  
- TOKEN("quick") ×2  
- TOKEN("brown"), TOKEN("fox"), PUNCT(".")  
- Tags:  
  - REPEAT_UNIT on repeated tokens  
  - ADJACENT edges  
  - PUNCT  

### SROB Output

- R2 (Punctuation Cluster Merge) applied  
- Repeated tokens preserved (no collapse)  
- `REFINEMENT_UNCERTAINTY` attached to ambiguous repetition patterns  

### CnOB Output

- C3 (Cardinality) on repeated structural units  
- C1 (Slot Presence) where repetition suggests possible missing structure  
- No semantic interpretation of repetition  

### SmOB Output

- Gap Marker on ambiguous repeated regions  
- Uncertainty Marker propagated  
- Slot Markers preserved  
- Residue includes repetition structure  

**Validation:** Repetition preserved; uncertainty propagated; no semantic inference.

---

## 5. Example 3 — Degraded / Noisy Input

**Input:**  
`Hello... world !! ? what ?`

### SOB Output

- TOKENs for words  
- PUNCT_CLUSTER("...")  
- PUNCT_CLUSTER("!!")  
- PUNCT("?")  
- Tags:  
  - LOCAL_DENSE around punctuation bursts  

### SROB Output

- R2 (Punctuation Cluster Merge) applied  
- `REFINEMENT_UNCERTAINTY` on ambiguous punctuation boundaries  

### CnOB Output

- C7 (Closure) on unmatched punctuation  
- C4 (Adjacency) where punctuation interrupts structural adjacency  
- No attempt to interpret punctuation  

### SmOB Output

- Gap Marker on noisy region  
- Uncertainty Marker propagated  
- Boundary Marker around punctuation cluster  
- Residue highlights structurally unstable region  

**Validation:** Degradation handled structurally; no invented meaning.

---

## 6. Validation Summary Table

| Example | Monotonicity | Pre‑Semantic | Residue Quality | RB Readiness | Uncertainty Handled |
|---------|--------------|--------------|-----------------|--------------|---------------------|
| 1 (Clean) | Yes | Yes | High | High | N/A |
| 2 (Repetition) | Yes | Yes | Medium | Good | Yes |
| 3 (Noisy) | Yes | Yes | Medium | Good | Yes |

---

## 7. Next Steps / Open Items

- Add longer, multi‑sentence examples  
- Add adversarial / contradictory structure cases  
- Build automated regression suite  
- Use examples to validate future OB evolution proposals  

---

**End of Revision 1.1 — ob_pipeline_examples.md**

---
