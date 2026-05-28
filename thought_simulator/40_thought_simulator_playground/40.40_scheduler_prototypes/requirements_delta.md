# Requirements Delta

## Purpose

This file records requirement-change proposals, implementer feedback, and migration notes for `40.40_scheduler_prototypes`.

## Migrated Structural Changes

- Replaced all Phase B template files with executable scheduler prototype, harness, and evidence-led verification records.
- Added deterministic JSON artifact under `artifacts/` for the first scheduler verification run.

## Evidence-Backed Requirement Deltas

- `HLR-20.440-001`: Scheduler phase behavior shall remain deterministic and replayable for identical event sequences.
	- Evidence: `positive_deterministic_replay`
	- Traceability: `tick`, `policy`, `max_active`, `selected_tp_ids`, `history`, `verification_digest`
- `HLR-20.440-002`: Scheduler baseline fairness policy shall support deterministic round-robin progress without starvation in the exercised sequence.
	- Evidence: `positive_round_robin_fairness`
	- Traceability: `selected_tp_ids`, `wait_ticks`, `total_selected`
- `HLR-20.440-003`: Scheduler contract validation shall reject empty TP identifiers, non-monotonic ticks, and unsupported policy names.
	- Evidence: `negative_empty_tp_id`, `negative_non_monotonic_tick`, `negative_invalid_policy`
	- Traceability: `tp_id`, `tick`, `event_type`, `policy`
- `LLR-30.40-001`: Harness shall emit a JSON artifact under `artifacts/` containing scenario outcomes and run summary.
	- Evidence: `artifacts/scheduler_verification_run_2026-05-28.json`
	- Traceability: artifact persistence, scenario ledger, summary status

## Rationale

- Scheduler behavior is central to deterministic tick execution and must be demonstrated via replayable evidence.
- Fairness and deterministic tie behavior are high-risk areas and require explicit scenario outputs.
- Negative-path validation is necessary to prevent silent nondeterministic drift from malformed scheduler inputs.

## Impacted Documents

- `software_description.md`
- `prototype.py`
- `harness.py`
- `verification_capsule.md`

## Open Validation Needed

- Confirm canonical default policy decision: `round_robin` vs `weighted_round_robin`.
- Confirm formal tie-break key order for weighted scheduling once promotion planning begins.
- Decide whether additional safety rejection paths are required (for example, empty thoughtpoint set at runtime reconfiguration).

## Migration Notes

- Scheduler prototype now has a stable JSON contract shape and deterministic evidence artifact.
- Scheduler exploratory verification IDs are aligned to canonical scheduler anchor IDs in `10_thought_simulator_req/10.40_scheduler_requirements.md`.
- Future deltas should append evidence-backed updates rather than replacing this baseline record.

