# Requirements Delta - 40.37 Thought Router (TR)

**Module ID:** 40.37  
**Version:** 0.2  
**Date:** 2026-06-04  
**Status:** Evidence-backed deltas. Software description approved. Aligned with 40.20 structure.

## Purpose

This file records requirement changes, implementer feedback, and migration notes for the `40.37_tr_router_prototypes` module.
It follows the format established by `40.20_tp_lifecycle/requirements_delta.md`.

## Verified Deltas (Evidence-Based)

| Requirement | Status | Evidence Source | Notes |
|-------------|--------|------------------|-------|
| Deterministic routing | ✅ Implemented | prototype.py + harness (3 runs) | Same input always produces identical route + delta_h across run1/run2/run3 |
| Correct basin selection based on content | ✅ Implemented | TC001–TC004 in harness | Math keywords → math_basin (0.15); thought keywords → thought_basin (0.08); else general_basin (0.05) |
| Fixed / monotonic ΔH% assignment | ✅ Implemented | All test outputs + determinism snapshot | Values are constant per route class; audited in verification_capsule |
| No randomness in routing layer | ✅ Implemented | Full prototype code + multiple runs | No random, time, or mutable global state |
| Explicit error path for invalid input | ✅ Implemented | Malformed input test case | Returns `{"route": "error", "reason": "invalid_input"}` with no side effects |
| Artifact organization in subdir | ✅ Implemented | harness.py update | Artifacts now written to `artifacts/` (40.20 alignment) |

## Structural / Process Requirements Discovered / Applied (40.20 Alignment)

- Add requirement that `software_description.md` is the canonical high-level intent document and must include Flows Alignment Statement + Agreement Statement (done; approved).
- Add requirement that `verification_capsule.md` is the canonical verification report with detailed ledgers, determinism evidence across runs, and three-flow statements (expanded in this pass).
- Add requirement that `requirements_delta.md` is the canonical implementer feedback and requirement-change report (this document).
- Add requirement that artifacts live in `artifacts/` subdirectory (harness updated; 3 runs generated for determinism comparison).
- Add requirement that the module produce supporting narrative docs in `docs/` (experiments.md, prototype_notes.md, reasoning_trail.md) for traceability (created in this pass).
- Add requirement that harness supports repeatable runs for determinism evidence (implemented; run1/run2/run3).
- IO schema and artifact path expectations documented in software_description.md §8 (already present).

## Rationale

- The 40.37 module intentionally explores only the *basin-selection + ΔH% tagging* aspect of routing as a minimal proxy.
- This provides early evidence for the deterministic routing principle (20.10, 20.30) and the TR dirty-flag contract (20.37) without implementing the full semantic field population yet.
- Aligning structure with 40.20 (the reference TP lifecycle module) improves consistency across the playground and makes promotion to 30-series easier.

## Impacted Documents

- `software_description.md` (Phase A approved by Copilot)
- `prototype.py` (minimal but sufficient for proxy scope)
- `harness.py` (updated for artifacts/ + multi-run)
- `verification_capsule.md` (major expansion)
- `requirements_delta.md` (this document)
- `docs/` (new: experiments.md, prototype_notes.md, reasoning_trail.md)
- 10.50.37 (canonical TR requirements seeded from this prototype's behavior)
- 30.37 (when promoted)

## Open Validation Needed / Future Work (explicitly non-goals for this iteration)

- Full 12-field TP.TR population and derivation logic (see 20.37 §6 and software_description §5 Non-Goals).
- tr_needs_update dirty-flag lifecycle integrated with RB / OB / Merge / IB.
- MTP snapshot (read-only) consumption by the router.
- Atomic write + clear-on-success semantics.
- Read-only consumption by GB / other basins at safe boundaries.
- Performance / TCU budgeting.
- Integration with actual pipeline (beyond standalone harness).

These are reserved for Iterative Design Flow iterations driven by 50.37 design work.

## Summary

This prototype satisfies the minimal viable requirements for an exploratory 40.37 TR implementation focused on deterministic basin routing + consistent ΔH% tagging.

All deltas are directly supported by the executed harness artifacts (now three runs in `artifacts/`).

The module has been brought into structural alignment with 40.20_tp_lifecycle now that the software_description.md has received approval.

---
