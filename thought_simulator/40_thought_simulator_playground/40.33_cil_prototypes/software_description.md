# 40.33_cil_prototypes / software_description.md

## Approval State
Phase A draft complete and approved for execution. Phase B implementation executed on 2026-06-03.

## Two-Phase Execution Model (Global 40.* Rule)

- Phase A: define and review `software_description.md` only.
- Mandatory stop after Phase A until explicit human approval.
- Phase B (only after approval): implement `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

## 1. Purpose

Define deterministic Conversation Integration Layer (CIL) prototype behavior for TP/MTP conversation intake, FIFO-preserving integration, deterministic classification, supervisory escalation flow, and auditable lifecycle outcomes.

## 2. Scope

- deterministic FIFO ingestion and queue processing for conversation packets
- deterministic snapshot coherence and sequence-token ordering controls
- deterministic classification and tie-break behavior under explicit profile policy
- deterministic ambiguity escalation to GB with bounded timeout/default and late-approval re-entry handling
- deterministic reject-with-audit handling for unsupported profile/policy/enum states

This document now serves as the governing design baseline for the executed Phase B prototype and harness.

## 3. Source Index (Requirement Anchors)

Primary normative sources:

- `thought_simulator/20_requirements/20.33_cil_requirements.md`
- `thought_simulator/20_requirements/20.30_ts_functional_model.md`
- `thought_simulator/20_requirements/20.10_ts_architectural_principles.md`
- `thought_simulator/20_requirements/20.80_gb_requirements.md`
- `thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md`
- `thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md`
- `thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md`

## 4. Functional Boundaries

CIL does:

- own deterministic TP/MTP conversation intake and FIFO-preserving integration sequence
- classify conversation thread state under explicit confidence and tie-break policy
- escalate ambiguity to GB only through deterministic supervisory request channels
- apply deterministic timeout/default and late-approval re-entry outcomes
- preserve append-only audit records for intake, classification, escalation, and supervisory outcomes

CIL does not:

- directly instantiate inquiry channels without GB approval
- bypass GB supervisory decision paths
- mutate OB, RB, TB, IB, InB, OuB, or MTP internal implementation state
- make ordering decisions based on wall-clock precedence

## 5. IO Contract

Inbound contract (JSON-compatible):

- `event_type` (enum): `ingest|process_next|gb_response|profile_change`
- `sequence` (integer): deterministic ordering token
- `safe_boundary` (bool): routing/escalation policy mutation gate
- `snapshot_id` (string): deterministic snapshot pin
- `packet_id` (string): deterministic packet identity
- `confidence` (float): classification confidence in [0, 1]
- `profile_signature` (string): execution signature-bound profile key
- `decision` (enum): `approve|deny|timeout|late_approve` for GB response

Outbound contract (JSON-compatible):

- `sequence` (integer)
- `pending_queue` (array)
- `integrated_packets` (array)
- `escalation_requests` (array)
- `audit_log` (array)
- `active_profile` (string)
- `verification_digest` (string)

## 6. Deterministic Invariants

- FIFO order is preserved from intake through integration outputs
- processing sequence is monotonic and must advance by one per accepted event
- classification/tie-break outcomes are deterministic for fixed profile + input packet
- unsupported profile/policy/enum states deterministically reject with fixed reason codes
- routing/escalation-affecting transitions occur only at deterministic safe boundaries
- profile precedence uses active signature-bound profile over environment defaults

## 7. TCU and Tick-Budget Expectations

- CIL prototype execution must remain bounded per tick phase under constraints in `20.150_tcu_budgeting_requirements.md`
- Harness evidence should support future cycle budgeting fields: `scenario_id`, `seed`, `N`, `config_hash`, `cycles_measured`
- measured cycle budgets are promotion-controlled through 30 verification capsules

## 8. Verification Intent for Phase B

Planned positive checks:

- deterministic FIFO intake and snapshot coherence behavior
- deterministic classification/tie-break and ambiguity escalation behavior
- deterministic GB supervisory response handling, timeout/default, and re-entry semantics
- deterministic profile precedence over environment defaults

Planned negative-path checks:

- unsupported profile/enum rejection with fixed reason codes
- out-of-order sequence rejection
- safe-boundary violation rejection
- direct-inquiry bypass rejection without GB approval

## 9. Promotion Readiness Conditions

Before promotion from 40 to 30:

- executable harness with deterministic pass/fail scenario set
- artifact evidence covering FIFO/classification/escalation invariants
- explicit HLR/LLR mapping to 20.33 and parent anchors
- completed `verification_capsule.md` and `requirements_delta.md` with traceable scenario records
