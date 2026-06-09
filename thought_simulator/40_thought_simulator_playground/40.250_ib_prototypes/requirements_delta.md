# Requirements Delta

## Purpose

This file records requirement-change proposals, implementer feedback, and executed evidence deltas for `40.250_ib_prototypes`.

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

## W3 Extension Deltas (40.510-411)

- 20.510 §15.3 + 20.17: IIInB repair escalation path is distinguished from normal OB-IB creation; direct OUB bypass for escalation/repair is rejected (source_channel="ob_ib" enforcement).
	- Evidence: `w3_iiinb_repair_escalation_distinction` (and negative_direct_oub_bypass baseline)
	- Traceability: `source_channel`, request_reason (iiinb_repair_escalation) -> reject reason_code
- 20.510 §15.3 + 20.17: IMR Type A/B correction triggers route into Pipeline A only (via IB promote to OUB-ready, no direct B mutation).
	- Evidence: `w3_imr_correction_to_a_pipeline`
	- Traceability: promote (IMR-style) -> promoted_outputs (A-side)
- 20.510 §15.3 + 20.17: Cross-evidence with 40.60 (unknown-token escalation → CIL path) is supported via IB pending_evidence_requests.
	- Evidence: `w3_iiinb_cil_cross_evidence`
	- Traceability: evidence_request_delta (cil_*) -> pending_evidence_requests

## Rationale

- This execution removes scaffold ambiguity and proves deterministic IB lifecycle behavior with reproducible JSON artifacts.
- TP-tagging and audit records now provide explicit replay-visible lineage across creation, evolution, split/merge, and promotion paths.
- Safe-boundary gating and fixed reject reason codes reduce supervisory-control ambiguity.
- W3 extension adds explicit verification of IIInB/IB/IMR escalation seams (distinction, A-only routing, 40.60 cross) while retaining legacy 2026-06-03 baseline.

## Impacted Documents

- `software_description.md`
- `prototype.py`
- `harness.py`
- `verification_capsule.md`
- `requirements_delta.md`
- `40.510_refactor.md` (W3 row 411)

## Open Validation Needed

- Confirm whether additional negative tests are required for invalid merge-origin snapshots and unsupported GB decision enums.
- Confirm whether an explicit IB suspend/reshape supervisory scenario is required before 30-layer promotion.
- Confirm when to add measured TCU cycle fields to IB artifact output for TCU budgeting promotion.
- Joint test with live 40.60 IIInB for unknown-token → CIL escalation (cross-evidence).

## Execution Log

- 2026-06-03: Legacy Phase B executed through `python harness.py` (core IB lifecycle).
- Artifact (baseline): `artifacts/ib_verification_run_2026-06-03.json`.
- Result: PASS (7 scenarios, 0 failures).
- 2026-06-09: W3 Phase B extension executed (added explicit IIInB/IB distinction, IMR A-only, 40.60 CIL cross scenarios on top of legacy baseline).
- Artifact: `artifacts/ib_verification_run_2026-06-09.json`.
- Result: PASS (10 scenarios total, 0 failures). W3 extension evidence added per software_description.
