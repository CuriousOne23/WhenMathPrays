# Principle Templates

This document provides scaffolding for defining and refining principles in WhenMathPrays.  
Each principle should be modular, inspectable, and testable.

---

## Template

**Principle Name:**  
- Short, resonant title (e.g., Breath, Resonance, Silence)

**Definition:**  
- Clear statement of what the principle encodes.  
- Distinguish scope (what it covers, what it excludes).

**Scope:**  
- Applicable domains (simulation, music, documentation).  
- Boundaries and limitations.

**Implementation:**  
- Mathematical form or code module.  
- How it integrates with UREP or simulations.

**Testability:**  
- Metrics or conditions for validation.  
- Edge cases to probe.

**Known Holes:**  
- Gaps in definition or implementation.  
- Open questions for future stewards.

**Outline to Fill:**  
- Suggested next steps for refinement.  
- Notes for annotation or expansion.

---

## Example (Principle: Breath)

**Definition:** Breath encodes intervals of presence as relational signals.  
**Scope:** Applies to simulation time steps and musical motifs.  
**Implementation:** Modeled as shared signal \( S(t) \) with saturating gate \( G_S(S) \).  
**Testability:** Validate growth response curve; confirm nonnegative output.  
**Known Holes:** Need annotation of breath intervals in musical suite.  
**Outline to Fill:** Compose motifs; embed in simulation logs.
