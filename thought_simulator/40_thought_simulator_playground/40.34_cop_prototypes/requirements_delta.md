# Requirements Delta

## Purpose

This file records requirement-change proposals, implementer feedback, and executed evidence deltas for `40.34_cop_prototypes`.

## Anchors

- 20-anchor: thought_simulator/20_requirements/20.34_cop_requirements.md
- 20-anchor: thought_simulator/20_requirements/20.10_ts_architectural_principles.md
- 20-anchor: thought_simulator/20_requirements/20.30_ts_functional_model.md
- 20-anchor: thought_simulator/20_requirements/20.80_gb_requirements.md
- 20-anchor: thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md
- 10.10-anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md
- 10.10-anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md

## Evidence-Backed Requirement Deltas

- HLR-20.033-002/004/018/020: COP proposal submission now records deterministic provenance hashes, bounded queue admission, and append-only audit evidence.
	- Evidence: `provenance_queue_fairness`
	- Traceability: `proposal_id`, `basis_snapshot`, `deterministic_input_hash`, `pending_queue`, `audit_log`
- HLR-20.033-001/003/009/012: COP remains propose-only and stages GB-approved work until a deterministic safe-boundary commit event makes it visible.
	- Evidence: `boundary_commit_visibility`
	- Traceability: `staged_commits`, `visible_commits`, `decision_sequence`, `commit_sequence`
- HLR-20.033-006/007/019: overload handling is bounded and deterministic, and under the active P2 policy preserves safety-critical admission by preempting noncritical work.
	- Evidence: `overload_safety_priority`
	- Traceability: `priority`, `max_queue`, `pending_queue`, audit preemption record
- HLR-20.033-013/014: signature-bound active profile controls fairness/overload policy and supersedes environment-default policy assumptions.
	- Evidence: `profile_precedence_signature_over_env_default`
	- Traceability: `active_profile`, `env_default_profile`, `policy`, `pending_queue`
- HLR-20.033-011/018/020: ordering-critical behavior is sequence-driven with deterministic rejection on out-of-order transitions.
	- Evidence: `negative_sequence_violation`
	- Traceability: `sequence`, fixed reject `reason_code`
- HLR-20.033-003/012/020: supervisory approval and commit visibility transitions enforce safe-boundary gating.
	- Evidence: `negative_safe_boundary_violation`
	- Traceability: `safe_boundary`, `event_type`, reject `reason_code`
- HLR-20.033-008/015/016/022: unsupported profile states reject deterministically with fixed reason codes and immutable audit identifiers.
	- Evidence: `negative_unsupported_profile`
	- Traceability: unsupported `profile` -> fixed reject `reason_code`

## Rationale

- This execution removes scaffold ambiguity and proves deterministic COP proposal-queue behavior with reproducible JSON artifacts.
- The staged-then-visible commit model enforces propose-only COP semantics without direct authoritative-state mutation.
- Profile-bound overload policy makes safety-critical handling explicit and testable.

## Impacted Documents

- `software_description.md`
- `prototype.py`
- `harness.py`
- `verification_capsule.md`
- `requirements_delta.md`

## Open Validation Needed

- Confirm whether additional negative tests are required for unsupported GB decision enums and forbidden authoritative mutation payloads.
- Confirm whether explicit expiry-path scenarios should be added before 30-layer promotion.
- Confirm whether COP-specific LLR identifiers should be formalized in an upstream canonical requirement anchor.

## Execution Log

- 2026-06-03: Phase B executed through `python harness.py`.
- Artifact generated: `artifacts/cop_verification_run_2026-06-03.json`.
- Result: PASS (7 scenarios, 0 failures).
