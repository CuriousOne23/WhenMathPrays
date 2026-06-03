# Requirements Delta

## Purpose

This file records requirement-change proposals, implementer feedback, and executed evidence deltas for `40.32_cob_prototypes`.

## Anchors

- 20-anchor: thought_simulator/20_requirements/20.32_cob_requirements.md
- 20-anchor: thought_simulator/20_requirements/20.10_ts_architectural_principles.md
- 20-anchor: thought_simulator/20_requirements/20.30_ts_functional_model.md
- 20-anchor: thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md
- 10.10-anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md
- 10.10-anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md

## Evidence-Backed Requirement Deltas

- HLR-20.031-003/004/005/020: COB lifecycle transitions now preserve lineage and append-only deterministic audit records.
	- Evidence: `lifecycle_lineage_and_audit`
	- Traceability: `winner_lineage`, `split_children`, `merge_sources`, `audit_log`
- HLR-20.031-010/011/012/013/015: replay/export behavior now emits deterministic manifests with canonical digest stability and deterministic empty-artifact handling.
	- Evidence: `deterministic_replay_and_export`
	- Traceability: `replay_mode`, `exports`, `verification_digest`, `summary_proof`
- HLR-20.031-016/017: profile precedence is signature-bound and deterministic at export time.
	- Evidence: `profile_precedence_signature_over_env_default`
	- Traceability: `profile_signature`, `env_default_profile`, `export manifest`
- HLR-20.031-014/026: ordering-critical behavior is sequence-driven with deterministic rejection on out-of-order transitions.
	- Evidence: `negative_sequence_violation`
	- Traceability: `sequence`, fixed reject `reason_code`
- HLR-20.031-018/025: unsupported replay modes and unsupported event types are deterministically rejected using fixed reason codes.
	- Evidence: `negative_unsupported_replay_mode`, `negative_unsupported_event_type`
	- Traceability: unsupported `replay_mode` or `event_type` -> fixed reject `reason_code`
- HLR-20.031-024: safe-boundary gating is enforced for lifecycle transitions.
	- Evidence: `negative_safe_boundary_violation`
	- Traceability: `safe_boundary`, `event_type`, reject `reason_code`

## Rationale

- This execution removes scaffold ambiguity and proves deterministic COB behavior with reproducible JSON artifacts.
- Fixed reason-code rejection paths improve auditability and reduce ambiguity in failure triage.
- Signature-bound profile precedence prevents environment drift from changing export-visible artifacts.

## Impacted Documents

- `software_description.md`
- `prototype.py`
- `harness.py`
- `verification_capsule.md`
- `requirements_delta.md`

## Open Validation Needed

- Confirm whether COB-specific LLR IDs should be formalized in the 20-layer requirement corpus.
- Confirm whether additional negative tests are required for repeated deprecate and invalid merge/split payloads.
- Confirm whether TCU cycle measurement should be added directly to this harness run output or handled by a shared benchmarking harness.

## Execution Log

- 2026-06-03: Phase B executed through `python harness.py`.
- Artifact generated: `artifacts/cob_verification_run_2026-06-03.json`.
- Result: PASS (7 scenarios, 0 failures).
