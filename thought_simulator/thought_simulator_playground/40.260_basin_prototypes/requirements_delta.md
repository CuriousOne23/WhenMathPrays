# Requirements Delta

## Purpose

This file records requirement-change proposals, implementer feedback, and migration notes for `40.260_basin_prototypes` (W3 full redo).

## Migrated Structural Changes

- Renamed the module report files to the canonical `verification_capsule.md` and `requirements_delta.md` structure.
- Added a deterministic JSON artifact under `artifacts/` for the first executable verification run (legacy baseline 2026-05-27 retained).

## Evidence-Backed Requirement Deltas (Legacy Core)

- `HLR-?` (20.105/20.90): Basin state objects shall expose a JSON-compatible IO contract that preserves `basin_id`, `tp_id`, and `state_counter` without transformation.
  - Evidence: `positive_deterministic_replay`
  - Traceability: `basin_id`, `tp_id`, `state_counter`, `history`, `verification_digest`
- `HLR-?` (20.200/20.105): Basin replay of identical input contracts shall produce identical final snapshots and identical digests.
  - Evidence: `positive_deterministic_replay`
  - Traceability: `deterministic_mode`, `entropy_vector`, `history`, `verification_digest`
- `HLR-?` (20.90/20.170): Basin validation shall reject empty basin identifiers, duplicate provenance identifiers, and entropy-vector shape mismatches.
  - Evidence: `negative_empty_basin_id`, `negative_duplicate_provenance`, `negative_entropy_length_mismatch`
  - Traceability: `basin_id`, `provenance_ids`, `provenance_id`, `event_type`, `entropy_vector`
- `LLR-?` (20.200): The harness shall emit a JSON artifact under `artifacts/` containing scenario results, traceability fields, and a run summary.
  - Evidence: `artifacts/basin_verification_run_2026-05-27.json` (baseline)
  - Traceability: execution reporting, artifact persistence, scenario ledger

## W3 Full Redo Deltas (20.01 B2 + 40.510-412)

- 20.01 B2 + 40.510: BasinPrototype MUST support decomposition to normative A-basin boundaries (RB/OB/DCB/TB/IB from 405–411) without collapsing roles into a single generic type.
  - Evidence: `positive_w3_basin_decomposition` (role metadata "rb"/"ob" + distinct basin_ids + independent replay)
  - Traceability: metadata.basin_role, basin_id (per-role), history (no legacy generic ID dependency in strip-replay)
- 20.01 B2 + 40.510: Strip-replay fixtures SHALL NOT depend on legacy generic basin IDs after W3 closure.
  - Evidence: `positive_w3_basin_decomposition` (replay uses role-specific contracts from 40.190/40.200 style)
  - Traceability: verification_digest per role, no shared generic basin_id across roles
- 20.01 B2 + 40.510: Phase B may retain shared harness utilities but MUST split basin contracts to match 40.190 (RB), 40.200 (OB), 40.210 (DCB), 40.230 (TB), 40.250 (IB) boundaries.
  - Evidence: `positive_w3_basin_decomposition` (extensible metadata + per-role sequence tests; demonstrated for RB/OB)
  - Traceability: metadata.source_module, role-specific events (provenance/transition/entropy)

## Rationale

- The W3 full redo decomposes the pre-partition generic basin model to align with the normative A-chain (405–411) while preserving deterministic core invariants.
- Legacy 2026-05-27 evidence retained as baseline; 2026-06-09 run adds explicit W3 decomposition scenarios.
- Negative-path coverage retained for contract validation.
- Deltas now reference 20.01 B2 and 40.510 W3 scope; this module can now feed a future basin-specific HLR document.

## Impacted Documents

- `software_description.md`
- `prototype.py`
- `harness.py`
- `verification_capsule.md`
- `requirements_delta.md`
- `40.510_refactor.md` (row 412 + W3 log)

## Open Validation Needed

- Define whether the basin prototype should remain a standalone exploratory contract or be promoted into a formal basin design specification (50-series).
- Decide whether future basin requirements should be a dedicated HLR doc or remain as deltas.
- Confirm additional coverage for full RB/OB/DCB/TB/IB role-specific events (current W3 demo uses RB/OB as exemplars).
- Joint regression of strip-replay fixtures from 40.190/200/210/230/250 against the decomposed contracts.

## Migration Notes

- The basin prototype now has a stable contract shape, deterministic replay, and W3 decomposition evidence.
- Future deltas should extend the W3 sections rather than replacing legacy core.
- Legacy 2026-05-27 artifact retained in docs for baseline reference.

## Execution Log

- 2026-05-27: Legacy baseline executed (4 scenarios, core invariants).
- Artifact (baseline): `artifacts/basin_verification_run_2026-05-27.json`.
- 2026-06-09: W3 Phase B full redo executed (added decomposition scenario for 20.01 B2 alignment; 5/5 PASS).
- Artifact: `artifacts/basin_verification_run_2026-06-09.json`.
- Result: PASS. W3 decomposition to A-basin boundaries (RB/OB demonstrated; extensible) + strip-replay without legacy generic IDs.