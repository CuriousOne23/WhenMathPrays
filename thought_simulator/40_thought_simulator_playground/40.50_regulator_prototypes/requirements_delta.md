# Requirements Delta

## Proposed Requirement Changes

- Add regulator-specific requirement anchors for deterministic decision replay and policy-mode behavior.
- Add explicit negative-path requirements for invalid policy mode and invalid numeric pressure input.

## Rationale

- Executed harness evidence now confirms deterministic replay and expected policy differentiation.
- Promotion still requires canonical requirement IDs tied to this evidence.

## Impacted Documents

- `software_description.md`
- `verification_capsule.md`
- future canonical requirement anchor under `10_thought_simulator_req/`

## Open Validation Needed

- Confirm minimum regulator decision schema for canonical audit/replay requirements.
- Define tie-break requirements when multiple regulator actions compete.

## Phase B Evidence Snapshot

- Harness result: PASS
- Artifact: `artifacts/regulator_verification_run_2026-05-28.json`
- Scenario outcomes:
	- `positive_deterministic_replay` PASS
	- `positive_policy_comparison` PASS
	- `negative_invalid_policy_mode` PASS
	- `negative_negative_pressure` PASS

