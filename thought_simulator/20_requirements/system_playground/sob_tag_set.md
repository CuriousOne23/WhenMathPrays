# SOB Tag Set
**sob_tag_set.md**  
**Revision:** 1.4 (Stabilized Baseline)  
**Date:** 2026-06-20  
**Status:** Stabilized Draft – Recommended for Lock

---

### 1. Purpose

This document defines the **frozen, finite, purely structural tag set** used exclusively by the SOB layer.  

These tags represent the maximal structural information that can be extracted from raw input without any semantic, pragmatic, or interpretive inference.

This tag set supports:
- `OB_search_and_tag_spec.md` (Rev 1.2)
- `OB_data_structures.md` (Rev 2.5)
- All OB pipeline invariants (Rev 7)

### 2. Core Principles (Locked)

- All tags must be **purely structural**.
- Tags must be **deterministic**, **idempotent**, and **layer-local**.
- The tag set is **finite and frozen** once finalized.
- Additions require versioned update and explicit leakage review.
- Every tag must support full provenance and traceability.

### 3. SOB_TAG_SET (Current Enumeration)

Tags are organized into three orthogonal families.

#### 3.1 Atomic Form Tags (What the unit is)

| Tag            | Description                              | Must Not Imply          |
|----------------|------------------------------------------|-------------------------|
| TOKEN          | Single token or sub-token                | POS, meaning, category  |
| SPAN           | Contiguous or non-contiguous token sequence | Phrase, semantic grouping |
| PUNCT          | Single punctuation mark                  | Emotion or emphasis     |
| PUNCT_CLUSTER  | Cluster of punctuation marks             | Emotional intensity     |
| DELIMITER      | Brackets, quotes, braces                 | Quotation or grouping meaning |
| SYMBOL         | Non-alphanumeric symbol                  | Mathematical role       |

#### 3.2 Structural Relation Tags (How units relate)

| Tag             | Description                              | Must Not Imply          |
|-----------------|------------------------------------------|-------------------------|
| ADJACENT        | Immediate adjacency                      | Grammar or causality    |
| PROXIMAL        | Within a small structural window         | Relatedness             |
| STRUCT_GROUP    | Structural grouping (layout-based)       | Semantic topic          |
| ORDER           | Positional sequencing                    | Temporal or logical order |
| REPEAT_UNIT     | Repeated structural element              | Emphasis or rhetoric    |
| PARALLEL_UNIT   | Parallel structural construction         | Comparison or balance   |
| LIST_MARKER     | Structural list-like indicator           | Enumeration meaning     |

#### 3.3 Rhythm & Distribution Tags (How units are distributed)

| Tag            | Description                              | Must Not Imply          |
|----------------|------------------------------------------|-------------------------|
| LOCAL_DENSE    | High local token density                 | Urgency                 |
| LOCAL_SPARSE   | Low local token density                  | Calmness                |
| LOCAL_CLUSTER  | Localized grouping of elements           | Focus                   |
| EVEN_SPACING   | Even distribution across a span          | Balance                 |

### 4. Usage Rules

- SOB may only apply tags from this set.
- Tags are **additive** — multiple tags may apply to the same atom.
- All tags must remain **strictly pre-semantic**.
- New tags must be structural, orthogonal, and invariant-safe.
- All tags must be applied deterministically.

### 5. Extensibility & Versioning

- Tag set is versioned (`SOB_TAG_SET_v1`, etc.).
- Additions must be structural, non-overlapping, and invariant-safe.
- Deprecation follows rules in `OB_data_structures.md` (Rev 2.5).
- All changes must be reflected in the OB Map.

### 6. Next Steps / Open Items

- Validate tags against representative input examples.
- Confirm orthogonality with upcoming SROB rewrite rules (R1–Rk).
- Final review for any remaining leakage risk.

---

**End of Revision 1.4**

---

If this looks good, we can lock SOB_TAG_SET and move forward (e.g., to rewrite rules R1–Rk or constraint families C1–C7).

Ready when you are.
