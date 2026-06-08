# 40.101 IIInB Prototypes / software_description.md

**Document ID:** 40.101  
**Phase:** B executed 2026-06-08  
**20-anchor:** [20.101](../../20_requirements/20.101_iiinb_requirements.md)

## Purpose

Exploratory `input_semantic_repair` stage: profile-gated, read-only USP apply, intake-bound TP writes, CIL escalation on unknown shorthand. Ordering: **InB → IIInB → RB**.

## Scope

- `profile_enabled` gate (skip with zero semantic effect when false)
- Deterministic segmentation and USP rule matching
- `input_repair_tags[]`, `input_segments[]`, `iiinb_escalation_refs[]` on TP only
- Envelope guard: no `semantic_core` / `TP.TR` mutation

## Flows Alignment Statement

- **Forward Flow (20-series):** [20.101](../../20_requirements/20.101_iiinb_requirements.md), [20.102](../../20_requirements/20.102_usp_requirements.md), [20.38](../../20_requirements/20.38_ts_implementation_guidelines.md) §6.
- **Backward Flow (40-series evidence):** Harness 6/6 PASS — `artifacts/iiinb_verification_run_2026-06-08.json`.
- **Iterative Design Flow (50-series influence):** None yet.

**Agreement Statement:** Provisionally aligned — core Track H intake repair path demonstrated; cross-turn UPI/GB wiring deferred to Phase 2 (40.102/40.103).