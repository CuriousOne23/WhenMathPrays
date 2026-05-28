# Verification Capsule

## Purpose

Track verification evidence for `40.50_regulator_prototypes`.

## Phase State

- Phase A complete status: pending human approval of `software_description.md`.
- Phase B execution status: completed in sandbox (not promotable before Phase A approval).

## Invariants

- Equivalent inputs produce equivalent regulator decisions in deterministic mode.
- Decision records are replay-safe and include required observability fields.

## Verification Steps (executed)

1. Deterministic replay of identical regulator input sequences.
2. Comparison run across policy modes (`clamp` vs `attenuate`) for stable decision fields.
3. Negative-path validation for invalid policy mode and invalid numeric input.

## Evidence

- Harness command: `.venv/Scripts/python.exe harness.py`
- Harness result: PASS
- Artifacts:
	- `artifacts/regulator_verification_run_2026-05-28.json`
- Scenarios:
	- `positive_deterministic_replay` PASS
	- `positive_policy_comparison` PASS
	- `negative_invalid_policy_mode` PASS
	- `negative_negative_pressure` PASS

## Status

- Current status: PHASE_B_EXECUTED_UNAPPROVED
- Confidence: MEDIUM
- Next action: human approval of `software_description.md`, then map proven behavior to canonical requirement IDs.

