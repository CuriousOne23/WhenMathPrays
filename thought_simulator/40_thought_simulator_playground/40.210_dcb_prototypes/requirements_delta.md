# 40.210_dcb_prototypes / requirements_delta.md

## Status
Phase B complete — HLR mapping exercised and recorded from 2026-06-09 verification run (5/5 PASS). Artifact: artifacts/dcb_verification_run_2026-06-09.json

## Primary 20-series anchors
- [20.106_dcb_requirements.md](../../20_requirements/20.106_dcb_requirements.md) — HLR-20.106-001–036 (geometric meta-basin, trajectory observation, ephemeral events, bounds, no tr_needs_update, approved read-set)
- [20.37_thought_router_tr_specification.md](../../20_requirements/20.37_thought_router_tr_specification.md) — §4.4 DCB as ephemeral TR overlay (no flag writes)
- [20.165_dcb_stability_requirements.md](../../20_requirements/20.165_dcb_stability_requirements.md) — qualitative non-expansive bounds
- [20.95_ts_numeric_policy.md](../../20_requirements/20.95_ts_numeric_policy.md) — geometry encoding (when numeric)

## Flows Alignment Statement

- **Forward Flow (20-series):** DCB geometric observation after OB (40.200), before TR (40.240) per 20.106-012 and 20.37 §4.4; emits ephemeral events only.
- **Backward Flow (40-series evidence):** Phase B runs confirm curvature-driven event emission, per-cycle bound with audit, zero tr_needs_update writes, canonical event ordering, and immediate audit+suppress on any semantic field read (035). Joint qualitative stability evidence prepared for 40.220.
- **Iterative Design Flow (50-series influence):** Evidence package supports 50.190 DCB stability design; reinforces geometric-only role distinct from OB semantic extraction.

**Agreement Statement**: Phase B complete per 40.05 and 40.510 W3. Full traceability from scenarios to 20.106 HLRs. Ready for 30.00 normalization and 50 insight. Handoffs to 40.200 (OB), 40.240 (TR), 40.220 (stability) exercised via mocks and contracts.

## Phase B HLR Exercise Summary (2026-06-09 harness run)

- Curvature exceed → event emit: HLR-20.106-010 (exceed invariant), -011 (geometric signal only). Evidence: single event with curvature > threshold, direction_delta, rationale.
- Per-cycle emission bound: HLR-20.106-036 (finite non-expansive). Evidence: high-curvature traj → ≤ max_events + EMISSION_BOUND audit.
- No `tr_needs_update` write: HLR-20.106-020. Evidence: any valid observation produces events without touching or signaling the flag.
- Event batch canonical order: HLR-20.106-028. Evidence: unsorted input steps → events sorted by step then |curvature|.
- Forbidden semantic field read: HLR-20.106-035 (approved geometric read-set only). Evidence: propositions/truth_hypotheses in traj → FORBIDDEN_READ audit + zero events emitted.

All 036 HLRs addressed at high level via the 5 scenarios + pure geometric logic + explicit boundary enforcement. Core contract (trajectory list → ordered events + audit; no side effects on TP) stable.

## Impacted / Referenced Documents
- 40.200_ob_prototypes (immediate upstream in OB → DCB → TR window)
- 40.240_tr_router_prototypes (consumer of ephemeral DCB events)
- 40.220_dcb_stability_prototypes (qualitative stability cross-check)
- 20.106, 20.37, 20.165, 20.95 (as above)
- 40.05_master_program_guide.md (process)
- 30.30_verification_glossary.md (for future 30 of "directional_change_event", "ephemeral TR overlay")
- 40.510_refactor.md (program tracking + W3 wave)
- 20.105 (TP trajectory coordinate fields for future live integration)

## Migration / Implementation Notes
- Self-contained (synthetic trajectory dicts with direction/curvature/step); shape compatible with persisted TP trajectory projections from 40.105/40.200.
- DCB.observe(trajectory, *, policy_signature, cycle_id) → DCBOutput with events (always canonically sorted) + audit.
- Curvature threshold and max_events_per_cycle are injectable for test; real bounds/policy per 20.165 + 20.95.
- No tr_needs_update ever written or returned — pure observer (enforced in all paths).
- Forbidden check is exhaustive on known semantic keys; early return with audit + empty events for negative tests.
- Events carry only geometric data (step, curvature, direction_delta, optional position) — no semantic tags.
- When 40.240 and live trajectory sources are ready, the same harness scenarios can be re-run with real objects.

## Open Items / Gaps
- Exact numeric curvature computation and invariant thresholds (current simple > threshold; production values per 20.95/50.190).
- Full multi-step trajectory stitching across MTP horizon (current single-pass on provided list).
- Live joint test with 40.240 (actual consumption of DCB events as TR hints) and 40.220 (stability argument) — deferred.
- 30.00 promotion: 10.50 peer + 30 capsule citing this + 40.200/40.240/40.220 evidence.
- 50 insight: DCB event schema and bound policy are inputs to 50.190 qualitative stability design.

All deltas incorporated as of 2026-06-09 Phase B completion. No outstanding from Phase A.
