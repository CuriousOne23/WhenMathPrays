# CNOB Constraints Families
**cnob_constraint_families.md**  
**Revision:** 1.2 (Polished & Stabilized)  
**Date:** 2026-06-20  
**Status:** Working Draft – For Review by CuriousOne23 & CP  

---

### 1. Purpose

Please see [OB_development_playbook.md](OB_development_playbook.md) for complete list of documents which pertain to the OB system playground papers.

This document defines the **C1–C7 constraint families** used by the CnOB (Constraint Object Basin) layer.

These families specify the **purely structural constraints** that CnOB is allowed to detect and annotate on SROB output. No semantic plausibility, world knowledge, intent, or repair is permitted.

This specification supports:
- `OB_pipeline_spec.md` (Rev 7)
- `OB_search_and_tag_spec.md` (Rev 1.2)
- `OB_data_structures.md` (Rev 2.5)
- `sob_tag_set.md` (Rev 1.4)
- `srob_rewrite_rules.md` (Rev 1.2)

### 2. Core Principles (Locked)

- All constraints must be **purely structural** and **provably entailed** by the current graph.
- Constraints must accumulate **monotonically** (never weaken or remove prior constraints).
- No constraint may fill gaps, silently repair, or imply preferred resolutions.
- All constraints must carry full provenance.
- Constraint families are **finite and frozen** once finalized.

### 3. CnOB Constraint Families (C1–C7)

| Family ID | Name                    | Description                                                                 | Applies To                     | Must Not Do                                      |
|-----------|-------------------------|-----------------------------------------------------------------------------|--------------------------------|--------------------------------------------------|
| C1        | Slot Presence           | Detects structurally expected positions that are absent                    | Spans, struct_groups, lists    | Suggest content or reason for the gap            |
| C2        | Ordering                | Detects violations of purely positional ordering rules                     | ORDER edges, sequences         | Infer temporal, logical, or narrative meaning    |
| C3        | Cardinality             | Detects incorrect count of elements relative to structural pattern         | Groups, lists, delimiters      | Infer importance or semantic enumeration         |
| C4        | Adjacency               | Detects broken adjacency where it is structurally required                 | Adjacent atoms, delimiters     | Infer grammar or causality                       |
| C5        | Dependency              | Detects unresolved structural dependencies                                 | Nodes with relations           | Resolve or guess missing content                 |
| C6        | Nesting                 | Detects improper or contradictory nesting of structural groups             | struct_group hierarchies       | Flatten based on semantic judgment               |
| C7        | Closure                 | Detects unclosed or improperly closed structural constructs               | Delimiters, spans, groups      | Infer meaning of the unclosed structure          |

*(C8+ will be added after validation against real examples)*

### 4. Usage Rules

- CnOB may only detect and annotate constraints from these families.
- Constraints must be **structurally entailed** — never guessed or based on plausibility.
- Constraints are **additive and monotonic**.
- Any irresolvable conflict must be recorded as `CONSTRAINT_CONFLICT` with full provenance.
- No constraint may imply a preferred resolution or semantic interpretation.

### 5. Extensibility & Versioning

- Families are versioned (`CNOB_CONSTRAINT_FAMILIES_v1`, etc.).
- New families must be purely structural, monotonic, and invariant-safe.
- Deprecation follows rules in `OB_data_structures.md` (Rev 2.5).

### 6. Next Steps / Open Items

- Validate each family against representative input examples
- Define precise structural conditions for each family
- Ensure compatibility with RB routing and SmOB residue
- Expand with C8+ based on observed patterns

---

**End of Revision 1.2**

---
