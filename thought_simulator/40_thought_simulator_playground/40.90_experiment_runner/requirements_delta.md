# Requirements Delta

## Proposed Requirement Changes

- Add experiment-runner requirement IDs for deterministic run identity and batch ordering.
- Add explicit negative-path requirements for malformed experiment requests.

## Rationale

- Executed harness evidence confirms deterministic run identity and stable batch execution behavior.
- Promotion still requires deterministic evidence mapped to stable canonical requirement IDs.

## Impacted Documents

- `software_description.md`
- `verification_capsule.md`
- future canonical requirement anchor under `10_thought_simulator_req/`

## Open Validation Needed

- Validate minimal request/response schema fields for replayability.
- Validate batch merge policy and its determinism guarantees.

## Phase B Evidence Snapshot

- Harness result: PASS
- Artifact: `artifacts/experiment_runner_verification_run_2026-05-28.json`
- Scenario outcomes:
	- `positive_deterministic_replay` PASS
	- `positive_batch_run` PASS
	- `negative_invalid_max_ticks` PASS
	- `negative_empty_request_list` PASS

