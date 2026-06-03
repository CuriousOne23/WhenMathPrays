# Requirements Delta

## Purpose

This file records requirement-change proposals, implementer feedback, and executed evidence deltas for `40.35_ib_prototypes`.

## Anchors

- 20-anchor: thought_simulator/20_requirements/20.90_ib_requirements.md
- 20-anchor: thought_simulator/20_requirements/20.30_ts_functional_model.md
- 20-anchor: thought_simulator/20_requirements/20.80_gb_requirements.md
- 20-anchor: thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md
- 10.10-anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md
- 10.10-anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md

## Evidence-Backed Requirement Deltas

- HLR-20.090-006/032/033: IB creation now uses asynchronous GB approval and instantiates IB state only from approved pending requests.
	- Evidence: `async_creation_approval`
	- Traceability: `request_id`, `decision`, `pending_requests`, `active_ibs`
- HLR-20.090-008/014/035/036/037/038: deterministic inquiry evolution now updates bounded state fields and appends TP-visible lifecycle tags at safe boundary.
	- Evidence: `deterministic_evolution_tp_tagging`
	- Traceability: `hypothesis_delta`, `evidence_request_delta`, `depth_state`, `tp_log`
- HLR-20.090-019/021/022: deterministic split/merge lifecycle transitions now preserve auditable lineage and controlled source retirement behavior.
	- Evidence: `split_merge_lifecycle`
	- Traceability: `child_suffixes`, `source_ib_ids`, `merged_ib_id`, `retired_ibs`, `lineage`
- HLR-20.090-023/024/025/026: promotion/retirement transitions now remain GB-mediated, safe-boundary applied, and audit-visible without direct OB mutation.
	- Evidence: `promote_and_retire`
	- Traceability: `oub_output_id`, `promoted_outputs`, `retired_ibs`, `gb_reference`
- HLR-20.090-007: direct OuB routing bypass attempts are deterministically rejected.
	- Evidence: `negative_direct_oub_bypass`
	- Traceability: `source_channel`, fixed reject reason code
- HLR-20.090-020/038: lifecycle and supervisory transitions now enforce safe-boundary gating.
	- Evidence: `negative_safe_boundary_violation`
	- Traceability: `safe_boundary`, `event_type`, reject reason code
- HLR-20.090-019/034/038: out-of-order lifecycle transitions are rejected with deterministic reason codes and append-only audit records.
	- Evidence: `negative_sequence_violation`
	- Traceability: `sequence`, reject reason code, `audit_log`

## Rationale

- This execution removes scaffold ambiguity and proves deterministic IB lifecycle behavior with reproducible JSON artifacts.
- TP-tagging and audit records now provide explicit replay-visible lineage across creation, evolution, split/merge, and promotion paths.
- Safe-boundary gating and fixed reject reason codes reduce supervisory-control ambiguity.

## Impacted Documents

- `software_description.md`
- `prototype.py`
- `harness.py`
- `verification_capsule.md`
- `requirements_delta.md`

## Open Validation Needed

- Confirm whether additional negative tests are required for invalid merge-origin snapshots and unsupported GB decision enums.
- Confirm whether an explicit IB suspend/reshape supervisory scenario is required before 30-layer promotion.
- Confirm when to add measured TCU cycle fields to IB artifact output for TCU budgeting promotion.

## Execution Log

- 2026-06-03: Phase B executed through `python harness.py`.
- Artifact generated: `artifacts/ib_verification_run_2026-06-03.json`.
- Result: PASS (7 scenarios, 0 failures).
