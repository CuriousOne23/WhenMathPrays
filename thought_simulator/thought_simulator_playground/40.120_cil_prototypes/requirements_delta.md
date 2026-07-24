# Requirements Delta

## Purpose

This file records requirement-change proposals, implementer feedback, and executed evidence deltas for `40.120_cil_prototypes`.

## Anchors

- 20-anchor: thought_simulator/20_requirements/20.33_cil_requirements.md
- 20-anchor: thought_simulator/20_requirements/20.30_ts_functional_model.md
- 20-anchor: thought_simulator/20_requirements/20.10_ts_architectural_principles.md
- 20-anchor: thought_simulator/20_requirements/20.80_gb_requirements.md
- 20-anchor: thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md
- 10.10-anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md
- 10.10-anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md

## Evidence-Backed Requirement Deltas

- HLR-20.032-001/002/022: CIL intake and integration now preserve deterministic FIFO ordering and snapshot coherence.
	- Evidence: `fifo_snapshot_coherence`
	- Traceability: `packet_id`, `snapshot_id`, `pending_queue`, `integrated_packets`
- HLR-20.032-003/004/009: CIL classification and tie-break behavior is deterministic and ambiguity escalates through deterministic GB channels.
	- Evidence: `classification_escalation_gb_flow`
	- Traceability: `confidence`, deterministic threshold/tie-break, `escalation_requests`
- HLR-20.032-006/007/023: timeout/default and late-approval re-entry outcomes are deterministic and bounded.
	- Evidence: `classification_escalation_gb_flow`
	- Traceability: `decision=timeout`, `decision=late_approve`, re-entry status transitions
- HLR-20.032-012/013: execution-signature profile precedence is preserved over environment defaults.
	- Evidence: `profile_precedence_signature_over_env_default`
	- Traceability: `active_profile`, `env_default_profile`, behavior under profile policy
- HLR-20.032-014/015: sequence and safe-boundary controls now enforce deterministic routing/escalation transition gates.
	- Evidence: `negative_sequence_violation`, `negative_safe_boundary_violation`
	- Traceability: `sequence`, `safe_boundary`, reject reason codes
- HLR-20.032-005/018: direct inquiry bypass attempts are deterministically rejected unless GB-mediated.
	- Evidence: `negative_direct_inquiry_bypass`
	- Traceability: `request_channel`, fixed reject reason code
- HLR-20.032-011/020/021: unsupported profile/enum states are deterministically rejected with fixed audit reason codes.
	- Evidence: `negative_unsupported_profile`
	- Traceability: `profile`, fixed reject reason code and append-only audit records

## Rationale

- Executed scenarios remove scaffold ambiguity and provide deterministic CIL supervisory-flow evidence.
- Fixed reject reason codes improve auditability and reduce ambiguity in policy-governance triage.
- FIFO + safe-boundary controls prevent order drift and mixed-cycle policy mutation hazards.

## Impacted Documents

- `software_description.md`
- `prototype.py`
- `harness.py`
- `verification_capsule.md`
- `requirements_delta.md`

## Open Validation Needed

- Confirm whether CIL-specific LLR IDs should be formalized in canonical 30-layer numbering.
- Confirm whether additional negative-path coverage is needed for unsupported decision enums in GB response events.
- Confirm when to add explicit cycle-measurement fields (`scenario_id`, `seed`, `N`, `config_hash`, `cycles_measured`) to CIL artifacts for TCU promotion.

## Execution Log

- 2026-06-03: Phase B executed through `python harness.py`.
- Artifact generated: `artifacts/cil_verification_run_2026-06-03.json`.
- Result: PASS (7 scenarios, 0 failures).
