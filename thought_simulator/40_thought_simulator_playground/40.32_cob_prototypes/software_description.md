# 40.32_cob_prototypes / software_description.md

## Approval State
Phase A draft complete and approved for execution. Phase B implementation executed on 2026-06-03.

## Two-Phase Execution Model (Global 40.* Rule)

- Phase A: define and review `software_description.md` only.
- Mandatory stop after Phase A until explicit human approval.
- Phase B (only after approval): implement `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

## 1. Purpose

Define deterministic Conversation Object Basin (COB) prototype behavior for conversation object identity, lineage, lifecycle transitions, replay/export semantics, and audit-safe state evolution.

## 2. Scope

- prototype COB lifecycle operations: create, promote, deprecate, merge, split, compact, replay-mode switch, export issuance
- enforce deterministic ordering and safe-boundary activation rules
- preserve auditable lineage and append-only transition evidence
- expose JSON-first contracts for harness validation and replay checks

This document now serves as the governing design baseline for the executed Phase B prototype and harness.

## 3. Source Index (Requirement Anchors)

Primary normative sources:

- `thought_simulator/20_requirements/20.32_cob_requirements.md`
- `thought_simulator/20_requirements/20.30_ts_functional_model.md`
- `thought_simulator/20_requirements/20.10_ts_architectural_principles.md`
- `thought_simulator/20_requirements/20.90_ib_requirements.md`
- `thought_simulator/20_requirements/20.200_traceability_matrix.md`
- `thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md`
- `thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md`
- `thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md`

## 4. Functional Boundaries

COB does:

- own conversation object identity, lineage, lifecycle state, replay horizon mode, and export contract issuance
- enforce deterministic single-winner promotion semantics for provisional placeholders
- preserve immutable lineage edges required for audit proofs
- emit deterministic append-only transition evidence

COB does not:

- mutate OB, RB, TB, IB, InB, OuB, or MTP internal state
- perform supervisory control (GB role) or regulation (Regulator role)
- bypass deterministic safe-boundary activation rules

## 5. IO Contract

Inbound contract (JSON-compatible):

- `scenario_id` (string): deterministic test scenario identifier
- `seed` (integer/string): deterministic seed input used by harness
- `cob_id` (string): stable conversation object identifier
- `event_type` (enum): `create|promote|deprecate|merge|split|compact|replay_mode_change|export`
- `sequence` (integer): deterministic ordering token
- `lineage` (object): parent/child/merge-sources metadata
- `profile_signature` (string): versioned profile precedence selector
- `replay_mode` (enum): `full|windowed|summary_proof`

Outbound contract (JSON-compatible):

- `cob_id` (string)
- `lifecycle_state` (enum)
- `lineage_state` (object)
- `replay_state` (object)
- `export_manifest` (object)
- `audit_append_record` (object)
- `verification_digest` (string)

## 6. Deterministic Invariants

- fixed seed + fixed input cardinality + fixed configuration + fixed runtime profile -> deterministic lifecycle outcomes
- ordering-critical behavior derives from deterministic sequence state only
- replay/export manifests use canonical deterministic key ordering
- unsupported enums/profiles follow deterministic reject-with-audit behavior
- lifecycle transitions occur only at deterministic safe boundaries

## 7. TCU and Tick-Budget Expectations

- COB prototype execution must remain bounded per tick phase under the constraints defined by `20.150_tcu_budgeting_requirements.md`
- Phase B harness must emit cycle evidence fields: `scenario_id`, `seed`, `N`, `config_hash`, `cycles_measured`
- measured cycle budgets are promotion-controlled through 30 verification capsules

## 8. Verification Intent for Phase B

Planned positive checks:

- deterministic winner promotion per lineage
- deterministic replay horizon behavior across supported modes
- deterministic export manifest and redaction profile behavior
- deterministic safe-boundary activation and rollback behavior

Planned negative-path checks:

- unsupported replay mode/profile rejection with fixed reason codes
- invalid lineage transition rejection
- out-of-order sequence rejection

## 9. Promotion Readiness Conditions

Before promotion from 40 to 30:

- executable harness with deterministic pass/fail scenario set
- artifact evidence covering lifecycle and replay/export invariants
- explicit HLR/LLR mapping to 20.32 and parent anchors
- completed `verification_capsule.md` and `requirements_delta.md` with traceable scenario records

---

## W2 Phase A Extension (40.510-204)

**Approval State:** Phase A extension **draft — pending review** (base Phase B from 2026-06-03 remains valid).

**Program row:** [40.510-204](../40.510_refactor.md) — targeted redo for **USP snapshot version pins** on conversation objects.

### Purpose (W2 delta)

Extend COB to pin active `usp_version_ref` on conversation scope per [20.102](../../20_requirements/20.102_usp_requirements.md) HLR-20.102-010 and [20.32](../../20_requirements/20.32_cob_requirements.md) lifecycle policy — enabling cross-turn shorthand visibility for IIInB and replay (C7-D).

### What Phase B Must Explore (W2)

| Scenario | HLR anchor | Expected |
|----------|------------|----------|
| `positive_cob_usp_pin_on_commit` | 20.102-010 | COB records `usp_version_ref` after UPI commit |
| `positive_pin_survives_lifecycle_transition` | 20.032-027–032 | Pin stable across allowed COB transitions |
| `positive_replay_pin_equivalent` | 20.102-018 | Identical pin on deterministic replay |
| `negative_pin_without_usp_version` | structural | Reject invalid pin reference |

### Dependencies
- [40.102_usp_prototypes](../40.102_usp_prototypes/software_description.md) (GATE-B)
- [40.103_upi_prototypes](../40.103_upi_prototypes/software_description.md) (GATE-B)
- [40.392_core_data_structs_prototypes](../40.392_core_data_structs_prototypes/software_description.md) (`CobUspSnapshotPin` shape)

### Flows Alignment (W2 extension)
- **Forward Flow:** 20.32 + 20.102-010/020
- **Backward Flow:** Prior COB Phase B (2026-06-03) — extend harness only
- **Iterative Design Flow:** None yet

**Agreement Statement:** Provisionally aligned — W2 extension scoped to USP pin fields; does not alter prior COB lifecycle evidence without explicit regression scenarios.
