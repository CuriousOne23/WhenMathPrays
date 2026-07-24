# OB_search_and_tag_spec.md**  
**Revision:** 1.2 (Polished Draft)  
**Date:** 2026-06-20  
**Status:** Working Draft – Ready for Review

### 1. Purpose
This document defines **what** each OB layer searches for, detects, and tags. It specifies the structural search space, detection rules, and tagging mechanisms for SOB, SROB, CnOB, and SmOB while strictly preserving pre-semantic boundaries.

This spec sits between:
- `OB_pipeline_spec.md` (Rev 7) — architecture & invariants
- `OB_data_structures.md` — concrete schemas

### 2. Core Principles (Locked)

- All detection and tagging must remain **purely structural**.
- No layer may use semantic plausibility, world knowledge, or intent inference.
- Every tag belongs to a **frozen, finite, layer-local tag set** (no cross-layer reuse).
- All detections must be **deterministic** and **replayable**.
- Uncertainty and gaps must be explicitly tagged and propagated.
- Monotonicity: No layer may weaken or remove tags from prior layers (except explicit noise removal in SROB).

### 3. Layer-by-Layer Search & Tag Specification

#### 3.1 SOB — Structural Object Basin
**Focus:** Maximal raw structural extraction.

**Searches For / Detects:**
- Tokens and token sequences
- Spans (contiguous and non-contiguous)
- Adjacency and proximity patterns
- Basic grouping (repetition, parallelism, clustering)
- Punctuation and delimiter clusters
- Surface ordering and positional information
- Structural rhythm (distribution, density, spacing)

**Tagging (SOB_TAG_SET — to be enumerated):**
- TOKEN, SPAN, REL, GROUP, ORDER, PUNCT_CLUSTER
- REPETITION, PARALLELISM, LIST_LIKE
- Rhythm tags: DENSE, SPARSE, CLUSTERED, etc.

**Must Not Detect/Tag:** Any semantic role, intent, emotional valence, normalization, or disambiguation.

---

#### 3.2 SROB — Structural Refinement Object Basin
**Focus:** Structural normalization and canonicalization.

**Searches For / Detects:**
- Provable structural duplicates and redundancy
- Equivalent structural forms under defined equivalence classes (R1–Rk)
- Reorderable subsequences licensed by structural equivalence
- Structural noise patterns (tokenization artifacts, repeated delimiters)

**Tagging (SROB_TAG_SET — to be enumerated):**
- NOISE_MARKER
- CANONICAL_FORM
- REORDERABLE_GROUP
- UNCERTAINTY_REFINEMENT

**Must Not Detect/Tag:** Anything requiring semantic resolution or removal of legitimate ambiguity.

---

#### 3.3 CnOB — Constraint Object Basin
**Focus:** Structural constraint detection and gap identification.

**Searches For / Detects:**
- Missing slots or expected structural positions
- Ordering violations
- Cardinality violations
- Dependency breaks
- Structural contradictions
- Constraint entailments (what must hold given the current structure)

**Tagging (C1–C7 families — to be enumerated):**
- GAP_MISSING_SLOT
- CONSTRAINT_VIOLATION (with subtype)
- CONTRADICTION
- DEPENDENCY_BREAK
- ENTAILED_CONSTRAINT

**Must Not Detect/Tag:** Semantic plausibility or any preference for resolution.

---

#### 3.4 SmOB — Semantic Mapping Object Basin
**Focus:** Preparation of neutral semantic-ready structures.

**Searches For / Detects:**
- Potential attachment points for relational interpretation
- Open slots that can accept referents
- Structural anchors suitable for relational binding
- Unresolved gaps and constraints from prior layers
- Semantic-ready boundaries (where RB/TB will attach meaning)

**Tagging (H1–Hn hooks — to be enumerated):**
- SLOT_OPEN
- REFERENT_ANCHOR
- RELATIONAL_HOOK
- SEMANTIC_BOUNDARY
- UNCERTAINTY_CARRY
- GAP_PENDING

**Must Not Detect/Tag:** Any semantic filling, interpretation, stance, or truth-value suggestion.

---

### 4. Global Search & Tag Rules

1. **Finite Layer-Local Tag Sets** — Each layer has its own frozen namespace.
2. **Traceability** — Every tag carries provenance to the originating input location.
3. **Uncertainty Propagation** — Partial or ambiguous detections must be explicitly tagged.
4. **No Semantic Leakage** — No tag may imply meaning, intent, or plausibility.
5. **Monotonicity** — Earlier tags may only be refined or annotated, never weakened (except explicit noise removal in SROB).

---

### 5. Next Steps / Open Items

- Final enumeration of `SOB_TAG_SET`
- Definition of rewrite rules R1–Rk (SROB)
- Definition of constraint families C1–C7 (CnOB)
- Definition of mapping hooks H1–Hn (SmOB)
- Cross-layer consistency validation examples

---

**End of Revision 1.2**

---
