# Verification Capsule

## Purpose

Track verification evidence for `40.540_experiment_runner`.

## Phase State

- Phase A complete status: pending human approval of `software_description.md`.
- Phase B execution status: completed in sandbox (not promotable before Phase A approval).

## Invariants

- Experiment runner output identity is deterministic for equivalent requests.
- Batch result ordering remains stable and traceable.

## Verification Steps (executed)

1. Deterministic replay of identical single-run requests.
2. Deterministic batch-run validation with stable result ordering and digest output.
3. Negative-path validation for invalid `max_ticks` and empty request batch.

## Evidence

- Harness command: `.venv/Scripts/python.exe harness.py`
- Harness result: PASS
- Artifacts:
	- `artifacts/experiment_runner_verification_run_2026-05-28.json`
- Scenarios:
	- `positive_deterministic_replay` PASS
	- `positive_batch_run` PASS
	- `negative_invalid_max_ticks` PASS
	- `negative_empty_request_list` PASS

## Status

- Current status: PHASE_B_EXECUTED_UNAPPROVED
- Confidence: MEDIUM
- Next action: human approval of `software_description.md`, then map proven behavior to canonical requirement IDs.

