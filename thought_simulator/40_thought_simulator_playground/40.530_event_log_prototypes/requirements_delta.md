# Requirements Delta

## Proposed Requirement Changes

- Add module-level requirement IDs for event schema and replay contract stability.
- Add explicit negative-path requirements for malformed or out-of-order events.

## Rationale

- Executed harness evidence confirms deterministic replay and strict append/sequence checks.
- Promotion still requires deterministic replay evidence tied to stable canonical IDs.

## Impacted Documents

- `software_description.md`
- `verification_capsule.md`
- future canonical requirement anchor under `10_thought_simulator_req/`

## Open Validation Needed

- Validate minimal required event payload fields for replay-grade traceability.
- Validate compaction policies against deterministic replay fidelity.

## Phase B Evidence Snapshot

- Harness result: PASS
- Artifact: `artifacts/event_log_verification_run_2026-05-28.json`
- Scenario outcomes:
	- `positive_deterministic_replay` PASS
	- `negative_out_of_order_sequence` PASS
	- `negative_missing_field` PASS

