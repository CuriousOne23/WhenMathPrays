# 40.35_ib_prototypes / software_description.md

## Approval State
Phase A draft complete and approved for execution. Phase B implementation executed on 2026-06-03.

## Two-Phase Execution Model (Global 40.* Rule)

- Phase A: define and review `software_description.md` only.
- Mandatory stop after Phase A until explicit human approval.
- Phase B (only after approval): implement `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

## 1. Purpose

Define deterministic Inquiry Basin (IB) prototype behavior for asynchronous GB-approved inquiry creation, bounded inquiry evolution, supervised split/merge transitions, promotion/retirement flow, and append-only TP tagging.

## 2. Scope

- deterministic IB-Creation-Request flow from OB<->IB routing with asynchronous GB approval
- deterministic inquiry-state evolution with bounded depth and explicit hypothesis/evidence deltas
- deterministic GB-supervised split/merge lifecycle transitions with lineage preservation
- deterministic GB-mediated promotion to OuB-ready output and retirement transitions
- deterministic reject-with-audit behavior for direct OuB bypass, sequence violations, and safe-boundary violations

This document now serves as the governing design baseline for the executed Phase B prototype and harness.

## 3. Source Index (Requirement Anchors)

Primary normative sources:

- `thought_simulator/20_requirements/20.90_ib_requirements.md`
- `thought_simulator/20_requirements/20.30_ts_functional_model.md`
- `thought_simulator/20_requirements/20.80_gb_requirements.md`
- `thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md`
- `thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md`
- `thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md`

## 4. Functional Boundaries

IB does:

- accept inquiry creation requests only from approved OB<->IB interaction paths
- instantiate IB state only after deterministic GB approval and reference tagging
- evolve inquiry state with bounded depth, explicit deltas, and deterministic ordering
- apply split/merge/promote/retire lifecycle transitions only at deterministic safe boundaries
- emit append-only deterministic TP tags and audit records for every lifecycle transition

IB does not:

- accept direct OuB routing for creation requests
- bypass GB supervisory approval gates
- mutate OB registry state during promotion to OuB-ready outputs
- update inquiry state or emit TP tags outside deterministic safe boundaries

## 5. IO Contract

Inbound contract (JSON-compatible):

- `event_type` (enum): `request_create|gb_decision|evolve|split|merge|promote|retire`
- `sequence` (integer): deterministic ordering token
- `safe_boundary` (bool): required for all mutating lifecycle transitions except request creation
- `request_id` / `ib_id` / `merged_ib_id` (string)
- `snapshot_id` (string)
- `triggering_ob_ids` (array[string])
- `source_channel` (string): expected `ob_ib`
- `decision` (enum): `approve|deny`
- `hypothesis_delta` / `evidence_request_delta` / `partial_interpretations` (array[string])
- `child_suffixes` / `source_ib_ids` (array[string])
- `gb_reference` (string)
- `oub_output_id` (string)

Outbound contract (JSON-compatible):

- `sequence` (integer)
- `pending_requests` (array)
- `active_ibs` (array)
- `retired_ibs` (array)
- `promoted_outputs` (array)
- `audit_log` (array)
- `profile_signature` (string)
- `verification_digest` (string)

## 6. Deterministic Invariants

- IB instantiation occurs only from approved pending requests and is deterministic for equivalent request/decision inputs
- lifecycle transitions are sequence-driven and independent of wall-clock precedence
- safe-boundary gating is mandatory for GB decisions and all mutating lifecycle transitions
- split/merge behavior preserves deterministic lineage and auditable transition context
- TP tagging is append-only, deterministic, and replay-visible under identical inputs
- unsupported routes and invalid transition ordering reject with fixed reason codes

## 7. TCU and Tick-Budget Expectations

- IB execution must remain bounded per tick phase under constraints in `20.150_tcu_budgeting_requirements.md`
- Harness evidence should support future cycle-budget fields: `scenario_id`, `seed`, `N`, `config_hash`, `cycles_measured`
- measured cycle budgets remain promotion-controlled through 30 verification capsules

## 8. Verification Intent for Phase B

Planned positive checks:

- deterministic asynchronous creation and GB approval flow
- deterministic inquiry evolution with TP-tagging and bounded state progression
- deterministic split/merge lifecycle transitions and lineage integrity
- deterministic promotion and retirement flow under GB supervision

Planned negative-path checks:

- direct OuB routing bypass rejection
- safe-boundary violation rejection
- out-of-order sequence rejection

## 9. Promotion Readiness Conditions

Before promotion from 40 to 30:

- executable harness with deterministic pass/fail scenario set
- artifact evidence covering creation/evolution/lifecycle/promote invariants
- explicit HLR/LLR mapping to 20.90 and parent anchors
- completed `verification_capsule.md` and `requirements_delta.md` with traceable scenario records
