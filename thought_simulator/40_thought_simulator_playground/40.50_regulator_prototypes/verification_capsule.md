# Verification Capsule

## Purpose

Track verification evidence for `40.50_regulator_prototypes`.

## Phase State

- Phase A (software_description): scaffold (full detailed Phase A per 40.20 now documented; awaiting explicit human approval).
- Phase B execution status: preliminary implementation and harness exist in directory (evidence not yet promoted; full Phase B to follow Phase A approval per 40.20).

## Flows Alignment Statement (per 40.20; summary)

- **Forward Flow (10/20-series)**: See 40.50 software_description.md for full mapping from 10.10.40 regulator architecture + 20.150/20.170/20.30/20.40/20.90/20.200.
- **Backward Flow (40-series evidence)**: No full evidence yet; preliminary harness runs exist.
- **Iterative Design Flow (50-series influence)**: Downstream 10.50.50 and 50.50 anchors.

**Agreement Statement**: Scaffold stage only. Aligned provisionally on regulator as non-cognitive deterministic enforcer. Full statements in software_description.md and (post Phase B) in this capsule + delta.

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

