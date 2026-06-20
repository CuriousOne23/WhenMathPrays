# SMOB Mapping Hooks
**smob_mapping_hooks.md**  
**Revision:** 1.2 (Polished & Stabilized)  
**Date:** 2026-06-20  
**Status:** Working Draft – For Review by CuriousOne23 & CP  

---

### 1. Purpose

This document defines the **H1–Hn mapping hooks** used by the SmOB (Semantic Mapping Object Basin) layer.

These hooks create **neutral, pre-semantic scaffolding** that allows RB (Relational Basin) and TB (Truth Basin) to attach meaning later, without SmOB performing any interpretation, inference, or semantic preparation.

This specification supports:
- `OB_pipeline_spec.md` (Rev 7)
- `OB_search_and_tag_spec.md` (Rev 1.2)
- `OB_data_structures.md` (Rev 2.5)
- `sob_tag_set.md` (Rev 1.4)
- `srob_rewrite_rules.md` (Rev 1.2)
- `cnob_constraint_families.md` (Rev 1.2)

### 2. Core Principles (Locked)

- All hooks must remain **strictly pre-semantic** — no meaning, stance, role, or intent is assigned.
- Hooks must be **neutral** under all possible interpretations.
- Hooks must not imply what should fill a slot or what a relation might be.
- Hooks must preserve full provenance and traceability.
- The hook set is **finite and frozen** once finalized.

### 3. SmOB Mapping Hooks (H1–Hn)

| Hook ID | Name                  | Description                                                                 | Applies To                     | Must Not Do                                      |
|---------|-----------------------|-----------------------------------------------------------------------------|--------------------------------|--------------------------------------------------|
| H1      | Slot Marker           | Marks a structural position that may accept a future semantic attachment   | Spans, struct_groups, nodes    | Suggest what belongs in the slot                 |
| H2      | Anchor Point          | Identifies a structural element that can serve as a stable reference point | Atoms, nodes, spans            | Assign referent identity or meaning              |
| H3      | Relation Anchor       | Marks a location where a relation could attach, without implying its type  | Edges, groups, adjacency points| Infer the nature or direction of the relation    |
| H4      | Boundary Marker       | Marks a structural boundary where semantic interpretation may begin later  | Span edges, group boundaries   | Imply segmentation, topic, or semantic scope     |
| H5      | Uncertainty Marker    | Carries forward unresolved structural uncertainty from earlier layers      | Any unresolved element         | Resolve, minimize, or interpret the uncertainty  |
| H6      | Gap Marker            | Marks a structural gap that must be preserved for later resolution         | Missing slots, incomplete groups | Propose how the gap should be filled             |

*(H7+ will be added after validation against real examples)*

### 4. Usage Rules

- SmOB may only create hooks from this set.
- Hooks are **additive** — multiple hooks may apply to the same element.
- All hooks must remain **neutral** and **pre-semantic**.
- Hooks must preserve full provenance from prior layers.
- If a hook would imply any interpretation, it must not be created.

### 5. Extensibility & Versioning

- Hook set is versioned (`SMOB_MAPPING_HOOKS_v1`, etc.).
- New hooks must be pre-semantic, neutral, and invariant-safe.
- Deprecation follows rules in `OB_data_structures.md` (Rev 2.5).

### 6. Next Steps / Open Items

- Validate each hook against representative input examples
- Confirm compatibility with RB routing and binding graph
- Ensure hooks properly support residue and entailment propagation
- Expand with H7+ based on observed structural needs

---

**End of Revision 1.2**

---

This version feels solid and well-protected. If it looks good to you, we can lock it and decide on the next step (structural examples, RB routing policy, or something else).

Ready when you are.
