# OB Pipeline Examples
**ob_pipeline_examples.md**  
**Revision:** 1.2 (Medium Validation Set)  
**Date:** 2026-06-20  
**Status:** Working Draft – For Review by CuriousOne23 & CP  

---

### 1. Purpose

Please see [OB_development_playbook.md](OB_development_playbook.md) for complete list of documents which pertain to the OB system playground papers.

This document provides a **medium-sized set of structural examples** of the full OB pipeline (SOB → SROB → CnOB → SmOB).  

These examples are designed to:
- Validate core flow and invariants
- Expose common edge cases and ambiguity patterns
- Test monotonicity, residue quality, and RB readiness
- Serve as a practical regression corpus

### 2. Core Validation Criteria (Applied to Every Example)

- Strict pre-semantic boundaries maintained
- Monotonic entropy reduction
- No semantic leakage
- Correct provenance and traceability
- Proper uncertainty / gap propagation
- RB-ready output (`structural_signature`, `residue`, `bindings`)

---

### 3. Examples

#### Example 1 – Minimal Clean Input
**Input:** `Hello world.`  
**Key Behavior:** Clean, unambiguous flow.  
**SOB:** Basic tokens + adjacent relation.  
**SROB:** Canonical span, no rules triggered.  
**CnOB:** No constraints.  
**SmOB:** Slot marker on span, anchor points on tokens, clean residue.  
**Validation:** Perfect happy path.

#### Example 2 – Simple Repetition
**Input:** `The the quick quick brown fox.`  
**Key Behavior:** Repetition handling.  
**SOB:** Detects `REPEAT_UNIT` on "the" and "quick".  
**SROB:** No collapse; uncertainty marker on repetition pattern.  
**CnOB:** Cardinality constraint on repeated units.  
**SmOB:** Gap marker + uncertainty propagated.  
**Validation:** Repetition preserved as structural, not interpreted.

#### Example 3 – Punctuation Noise
**Input:** `Hello... world !! ? what ?`  
**Key Behavior:** Heavy punctuation.  
**SOB:** Strong `PUNCT_CLUSTER` and `LOCAL_DENSE`.  
**SROB:** Cluster merge + uncertainty on boundaries.  
**CnOB:** Closure and adjacency constraints triggered.  
**SmOB:** Gap marker + boundary marker around noisy region.  
**Validation:** Noise isolated structurally.

#### Example 4 – Structural Ambiguity
**Input:** `Time flies like an arrow.`  
**Key Behavior:** Classic ambiguity.  
**SOB:** Multiple possible groupings and relations.  
**SROB:** No forced resolution; uncertainty on grouping.  
**CnOB:** Multiple slot presence and ordering constraints.  
**SmOB:** Multiple slot markers + high uncertainty carry.  
**Validation:** Ambiguity preserved for RB.

#### Example 5 – Contradiction / Inconsistency
**Input:** `John is here. John is not here.`  
**Key Behavior:** Direct contradiction.  
**SOB:** Parallel structures detected.  
**SROB:** No collapse.  
**CnOB:** Strong contradiction constraint flagged.  
**SmOB:** Gap marker + explicit contradiction propagation.  
**Validation:** Contradiction preserved, not resolved.

#### Example 6 – Longer Multi-Sentence Flow
**Input:** `The team worked hard. They succeeded. However, challenges remain.`  
**Key Behavior:** Discourse flow.  
**SOB:** Multiple spans and adjacency chains.  
**SROB:** Span normalization.  
**CnOB:** Ordering and dependency constraints.  
**SmOB:** Boundary markers between sentences + residue for discourse.  
**Validation:** Maintains structure across sentences.

#### Example 7 – Very Short / Edge Input
**Input:** `Yes.`  
**Key Behavior:** Minimal input.  
**SOB:** Single token + punctuation.  
**SROB:** Minimal processing.  
**CnOB:** Slot presence constraint (incomplete thought).  
**SmOB:** High uncertainty + gap marker.  
**Validation:** Graceful handling of minimal cases.

#### Example 8 – Degraded / Messy Real-World
**Input:** `Hello world!!  what  r u doing  ???`  
**Key Behavior:** Typos, irregular spacing, heavy punctuation.  
**SOB:** Dense punctuation + noise patterns.  
**SROB:** Noise markers + high uncertainty.  
**CnOB:** Multiple closure and adjacency violations.  
**SmOB:** Strong gap and uncertainty markers.  
**Validation:** Pipeline degrades gracefully without hallucinating structure.

---

### 4. Validation Summary Table

| Example                  | Monotonicity | Pre-Semantic | Residue Quality | RB Readiness | Uncertainty Handled |
|--------------------------|--------------|--------------|-----------------|--------------|---------------------|
| 1 Clean                  | Yes          | Yes          | High            | High         | N/A                 |
| 2 Repetition             | Yes          | Yes          | Medium          | Good         | Yes                 |
| 3 Punctuation Noise      | Yes          | Yes          | Medium          | Good         | Yes                 |
| 4 Ambiguity              | Yes          | Yes          | High            | High         | Yes                 |
| 5 Contradiction          | Yes          | Yes          | High            | Good         | Yes                 |
| 6 Multi-Sentence         | Yes          | Yes          | High            | Good         | Low                 |
| 7 Very Short             | Yes          | Yes          | Medium          | Medium       | High                |
| 8 Messy/Degraded         | Yes          | Yes          | Medium          | Good         | High                |

---

### 5. Next Steps / Open Items

- Expand to 15–20 examples (including adversarial cases)
- Create automated validation suite based on this corpus
- Use as regression tests for any future OB changes

---

**End of Revision 1.2 — ob_pipeline_examples.md**

---
