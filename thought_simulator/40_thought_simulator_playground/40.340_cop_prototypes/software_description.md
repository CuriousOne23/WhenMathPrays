# 40.3400_cop_prototypes / software_description.md

## Approval State
Phase A draft complete and approved for execution. Phase B implementation executed on 2026-06-03.

## Two-Phase Execution Model (Global 40.* Rule)

- Phase A: define and review `software_description.md` only.
- Mandatory stop after Phase A until explicit human approval.
- Phase B (only after approval): implement `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

## 1. Purpose

Define deterministic Conversation Coprocessor (COP) prototype behavior for proposal provenance capture, bounded queue admission, GB-supervised approval, safe-boundary commit visibility, overload handling, and append-only audit evidence.

## 2. Scope

- deterministic proposal admission with canonical provenance hashing
- bounded queue handling under profile-bound fairness and overload policy
- GB supervisory decision staging with no direct authoritative-state mutation
- safe-boundary-only transition from approved proposal to visible commit
- deterministic reject-with-audit behavior for unsupported profile/state and sequence violations

This document now serves as the governing design baseline for the executed Phase B prototype and harness.

## 3. Source Index (Requirement Anchors)

Primary normative sources:

- `thought_simulator/20_requirements/20.34_cop_requirements.md`
- `thought_simulator/20_requirements/20.30_ts_functional_model.md`
- `thought_simulator/20_requirements/20.10_ts_architectural_principles.md`
- `thought_simulator/20_requirements/20.80_gb_requirements.md`
- `thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md`
- `thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md`
- `thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md`

## 4. Functional Boundaries

COP does:

- accept proposal packets through explicit deterministic interfaces only
- compute deterministic provenance digests from canonicalized proposal input
- maintain a bounded queue under profile-bound fairness and overload policy
- stage GB-approved proposals before visibility and expose them only at safe-boundary commit
- preserve append-only audit records for proposal submission, preemption, supervisory decision, commit, and rejection

COP does not:

- mutate authoritative TS decision state directly
- bypass GB supervisory approval or safe-boundary commit rules
- read or mutate internal OB, RB, TB, IB, InB, OuB, CIL, COB, or MTP implementation state
- use wall-clock precedence for ordering-critical behavior

## 5. IO Contract

Inbound contract (JSON-compatible):

- `event_type` (enum): `submit_proposal|gb_decision|commit_ready|profile_change`
- `sequence` (integer): deterministic ordering token
- `safe_boundary` (bool): mandatory for GB decision, commit visibility, and profile changes
- `proposal_id` (string): deterministic proposal identity
- `source` (string): COP proposal source surface
- `basis_snapshot` (string): snapshot provenance reference
- `priority` (enum): `normal|safety_critical`
- `proposal_input` (object): canonicalized proposal payload used for deterministic hash generation
- `decision` (enum): `approve|reject|expire`
- `profile` (string): execution-signature-bound COP policy selector

Outbound contract (JSON-compatible):

- `sequence` (integer)
- `policy` (object)
- `pending_queue` (array)
- `staged_commits` (array)
- `visible_commits` (array)
- `audit_log` (array)
- `active_profile` (string)
- `verification_digest` (string)

## 6. Deterministic Invariants

- queue admission and ordering are deterministic for fixed sequence and active profile
- proposal provenance hashes are canonical and replay-stable for equivalent input payloads
- approved proposals remain non-visible until a deterministic safe-boundary commit event occurs
- overload handling remains bounded and deterministic under the active policy
- unsupported profile/enum states reject with fixed reason codes
- active signature-bound profile takes precedence over environment default policy

## 7. TCU and Tick-Budget Expectations

- COP prototype execution must remain bounded per tick phase under constraints in `20.150_tcu_budgeting_requirements.md`
- Harness evidence should support future cycle-budgeting fields: `scenario_id`, `seed`, `N`, `config_hash`, `cycles_measured`
- measured cycle budgets remain promotion-controlled through 30 verification capsules

## 8. Verification Intent for Phase B

Planned positive checks:

- deterministic proposal provenance hashing and FIFO queue admission
- deterministic GB approval staging and safe-boundary commit visibility
- deterministic overload handling with safety-critical preemption behavior
- deterministic profile precedence over environment defaults

Planned negative-path checks:

- unsupported profile rejection with fixed reason codes
- out-of-order sequence rejection
- safe-boundary violation rejection

## 9. Promotion Readiness Conditions

Before promotion from 40 to 30:

- executable harness with deterministic pass/fail scenario set
- artifact evidence covering proposal, queue, approval, and overload invariants
- explicit HLR/LLR mapping to 20.34 and parent anchors
- completed `verification_capsule.md` and `requirements_delta.md` with traceable scenario records
