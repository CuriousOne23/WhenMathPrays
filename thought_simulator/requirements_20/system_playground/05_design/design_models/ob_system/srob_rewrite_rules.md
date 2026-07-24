# SROB Rewrite Rules
**srob_rewrite_rules.md**  
**Revision:** 1.2 (Polished & Stabilized)  
**Date:** 2026-06-20  
**Status:** Working Draft – For Review by CuriousOne23 & CP  

---

### 1. Purpose

Please see [OB_development_playbook.md](OB_development_playbook.md) for complete list of documents which pertain to the OB system playground papers.

This document defines the **purely structural rewrite rules (R1–Rk)** used by the SROB layer to refine SOB output into a cleaner, canonical structural graph.

All rules are strictly semantics-free, monotonic, and designed to reduce entropy without destroying legitimate structural information or ambiguity.

This specification supports:
- `OB_pipeline_spec.md` (Rev 7)
- `OB_search_and_tag_spec.md` (Rev 1.2)
- `OB_data_structures.md` (Rev 2.5)
- `sob_tag_set.md` (Rev 1.4)

### 2. Core Principles (Locked)

- All rules must be **purely structural** — no semantic, syntactic, or plausibility judgments.
- Rules must be **deterministic**, **idempotent**, and **reversible** (except for provable noise removal).
- Rules may only **reduce entropy monotonically** while preserving legitimate ambiguity.
- Every applied rule must be explicitly logged in `metadata.applied_rules`.
- The rule set is **versioned and frozen**.

### 3. SROB Rewrite Rules (R1–Rk)

| Rule ID | Name                              | Description                                                                 | Input Condition                                      | Transformation                                      | Must Not Do                                      |
|---------|-----------------------------------|-----------------------------------------------------------------------------|------------------------------------------------------|-----------------------------------------------------|--------------------------------------------------|
| R1      | Delimiter Canonicalization        | Normalize equivalent delimiter forms without changing structure            | Different stylistic variants of same delimiter      | Convert to single canonical form                    | Convert brackets ↔ quotes, remove delimiters     |
| R2      | Punctuation Cluster Merge         | Merge consecutive punctuation into a single annotated cluster              | Two or more adjacent PUNCT tokens                   | Replace with one PUNCT_CLUSTER + count              | Merge across spans, delimiters, or groups        |
| R3      | Redundant Nesting Collapse        | Flatten provably redundant nested struct_group levels                      | Nested struct_group with identical boundaries       | Flatten to single level                             | Collapse groups with different structural roles  |
| R4      | Span Boundary Normalization       | Normalize equivalent spans caused by tokenization artifacts                | Multiple spans with identical token content         | Convert to canonical span representation            | Merge spans with different content               |
| R5      | Duplicate Structural Edge Removal | Remove redundant identical structural edges                                | Multiple identical edges between same nodes         | Retain single canonical edge                        | Remove edges with different types                |
| R6      | List Marker Normalization         | Normalize stylistic variations of list markers                             | Different stylistic list markers                    | Convert to canonical list marker form               | Infer enumeration or ordering semantics          |

*(R7+ will be added after validation against real examples)*

### 4. Usage Rules

- SROB may only apply rules from this set.
- All rule applications must be explicitly logged.
- If a transformation would require semantic knowledge or destroy legitimate ambiguity, do **not** apply it. Attach `REFINEMENT_UNCERTAINTY` instead.
- Transformations must remain fully replayable.

### 5. Extensibility & Versioning

- Ruleset is versioned (`SROB_REWRITE_RULESET_v1`, etc.).
- New rules must be purely structural, monotonic, and invariant-safe.
- Deprecation follows rules in `OB_data_structures.md` (Rev 2.5).

### 6. Next Steps / Open Items

- Validate each rule against representative input examples
- Confirm no rule introduces semantic leakage
- Expand rule set (R7+) based on observed structural patterns
- Cross-check compatibility with CnOB constraint detection

---

**End of Revision 1.2**

---
