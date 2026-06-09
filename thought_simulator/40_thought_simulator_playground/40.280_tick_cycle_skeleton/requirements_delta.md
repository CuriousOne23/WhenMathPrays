# Requirements Delta

## Proposed Requirement Changes

- Add explicit requirement IDs for phase-order determinism and tick monotonicity.
- Add negative-path requirements for invalid phase maps and repeated phase execution.

## Rationale

- Executed harness evidence confirms deterministic outputs and expected failures for invalid sequence/order cases.
- Promotion still requires traceable canonical requirement IDs in `10_thought_simulator_req/`.

## Impacted Documents

- `software_description.md`
- `verification_capsule.md`
- future canonical requirement anchor under `10_thought_simulator_req/`

## Open Validation Needed

- Validate mandatory phase sequence for minimal canonical tick cycle.
- Validate whether phase plugin points require additional safety constraints.

## Phase B Evidence Snapshot

- Harness result: PASS
- Artifact: `artifacts/tick_cycle_verification_run_2026-05-28.json`
- Scenario outcomes:
	- `positive_deterministic_replay` PASS
	- `negative_non_monotonic_tick` PASS
	- `negative_invalid_phase_order` PASS

