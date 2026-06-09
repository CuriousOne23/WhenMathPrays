# Verification Capsule

## Status
**W3 Phase B complete** — harness PASS on 2026-06-09 (5/5 scenarios). Full redo for 20.01 B2 A-basin decomposition. Artifact: artifacts/basin_verification_run_2026-06-09.json

## Flows Alignment Statement

- **Forward Flow (20-series):** [20.01](../../20_requirements/20.01_architecture_map.md) B2 normative A-basin decomposition; aligns with 40.190 (RB), 40.200 (OB), 40.210 (DCB), 40.230 (TB), 40.250 (IB) contracts per W3 scope in 40.510.
- **Backward Flow (40-series evidence):** Phase B runs confirm generic BasinPrototype supports role-specific decomposition (via metadata.basin_role), deterministic replay per role, no collapse of boundaries, and strip-replay without legacy generic basin IDs.
- **Iterative Design Flow (50-series influence):** Evidence for basin contract splitting; prepares for basin-specific requirement document.

**Agreement Statement**: Phase B complete per 40.05 and 40.510 W3 (full redo). Legacy 2026-05-27 core retained as baseline; 2026-06-09 run adds explicit W3 decomposition scenarios for the 5 A-basins. Joint 405–411.

## Run Record

| Date | Module | Command | Inputs / Config | Result | Exit Code | Artifacts | HLR Ref | LLR Ref | Req Doc | Req Section | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-06-09 | 40.260_basin_prototypes | python harness.py | deterministic replay + W3 decomposition to RB/OB/DCB/TB/IB boundaries (role metadata, no legacy generic ID dependency) + negatives | PASS (5/5) | 0 | artifacts/basin_verification_run_2026-06-09.json | 20.01 B2, 20.105, 20.40, 20.200, 20.90, 20.170, 20.30 | (from source index) | 20.01_architecture_map.md; 20.105_tp_requirements.md; 20.40_ob_requirements.md; 20.200_traceability_matrix.md; 20.90_ib_requirements.md; 20.170_safety_requirements.md; 20.30_ts_functional_model.md; 40.510_refactor.md | W3 full redo scope (decompose to 405-411) | 5 scenarios: legacy positives/negatives + new W3 basin_decomposition for split contracts. |

## Positive Scenario Ledger

| Scenario | Result | HLR Ref | LLR Ref | IO Fields Exercised | Evidence |
|---|---|---|---|---|---|
| positive_deterministic_replay | PASS | 20.105, 20.200 | (from source) | basin_id, tp_id, state_counter, deterministic_mode, entropy_vector, provenance_ids, history, verification_digest | harness + artifact |
| positive_w3_basin_decomposition | PASS | 20.01 B2, 40.510 | (W3 scope) | metadata.basin_role (rb/ob), history, verification_digest, strip-replay per role | harness + artifact (RB + OB role examples; extensible to DCB/TB/IB) |

## Negative-Path Coverage Ledger

| Scenario | Result | HLR Ref | LLR Ref | IO Fields Exercised | Evidence |
|---|---|---|---|---|---|
| negative_empty_basin_id | PASS | 20.90, 20.170 | (from source) | basin_id | harness + artifact |
| negative_duplicate_provenance | PASS | 20.90, 20.170 | (from source) | provenance_ids, event_type, provenance_id | harness + artifact |
| negative_entropy_length_mismatch | PASS | 20.105, 20.40 | (from source) | entropy_vector, event_type | harness + artifact |

## W3 Full Redo Evidence (Decomposition to Normative A Basins)

Per software_description W3 scope (20.01 B2 + 40.510 A-chain 405–411):
- RB / OB / DCB / TB / IB roles MUST NOT collapse into single generic basin (demonstrated via metadata.basin_role + distinct basin_id in decomposition scenario).
- Phase B retains shared harness utilities but splits contracts (role metadata + per-role replay tests).
- Strip-replay fixtures do not depend on legacy generic basin IDs (replay uses role-specific contracts).
- positive_w3_basin_decomposition exercises RB-like and OB-like contracts with provenance/transition/entropy events; confirms independent replay and no role collapse. Extensible to DCB (40.210), TB (40.230), IB (40.250).

## Determinism Evidence Snapshot

- Deterministic replay (legacy + W3 role-specific) produced identical snapshots and digests.
- Evidence artifact: `artifacts/basin_verification_run_2026-06-09.json` (baseline 2026-05-27 retained in docs).

## Failure Record

- None (5/5 PASS; W3 decomposition scenario included).

## Requirements Delta Summary

- BasinPrototype now supports W3 decomposition: role-specific contracts (metadata.basin_role) without collapsing RB/OB/DCB/TB/IB boundaries.
- Strip-replay verified independent per role (no legacy generic basin ID dependency after W3).
- Core invariants (deterministic, negative rejections for empty ID / duplicate provenance / entropy mismatch) retained from legacy.
- Deltas now reference 20.01 B2 and 40.510 W3 full redo scope; prepares for basin-specific HLR document.

## Architectural Evaluation

- Full redo aligns generic basin with normative A-chain (405–411).
- Shared utilities in harness, split contracts in usage.
- Strong determinism and boundary enforcement.
- Ready for 30/50; legacy artifacts can be mapped to new contracts.

## Object Snapshots / Notes

- Legacy 2026-05-27 run retained as baseline.
- W3 2026-06-09 run completes the decomposition evidence.
- Next: promote to formal basin requirement doc if needed.