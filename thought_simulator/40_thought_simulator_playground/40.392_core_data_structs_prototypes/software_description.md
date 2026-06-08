# 40.392_core_data_structs_prototypes / software_description.md

## Approval State
- Phase A (software_description): **draft — pending review**
- Phase B (prototype + harness + evidence): not started
- Program row: **40.510-203** (W2)

## Two-Phase Execution Model (Global 40.* Rule)
- Phase A: define and review `software_description.md` only.
- Mandatory stop after Phase A until explicit human approval.
- Phase B (only after approval): implement `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

## Scaffold Metadata
- scaffold_status: Phase A draft
- intended_20_anchor: [20.39_ts_core_data_structures.md](../../20_requirements/20.39_ts_core_data_structures.md) §3.1–3.2
- intended_20_secondary: [20.102](../../20_requirements/20.102_usp_requirements.md), [20.101](../../20_requirements/20.101_iiinb_requirements.md), [20.103](../../20_requirements/20.103_upi_requirements.md)
- upstream_playground_modules: [40.101](../40.101_iiinb_prototypes/software_description.md) (inline `UspSnapshot` today), [40.100](../40.100_inb_prototypes/software_description.md)
- applicability: shared **conversation-layer and intake struct** prototypes — canonical shapes for W2 wire-up across USP/UPI/IIInB/COB
- disposition_target: promote (structural evidence; feeds 30.392 when normalized)
- program_wave: **W2** per [40.510_refactor.md](../40.510_refactor.md) §4.2
- numbering_note: suffix `.392` avoids collision with `40.39_mb_prototypes` (Monitoring Basin)

## Purpose

This module provides exploratory **canonical struct prototypes** for Track H and conversation-layer wiring per [20.39](../../20_requirements/20.39_ts_core_data_structures.md) §3.1–3.2:

- `UspSnapshot` — immutable read-only USP view for IIInB repair passes
- `InputRepairTag` — intake-bound repair audit tag shape
- `ConversationLayerState` — durable conversation-scoped state (outside four runtime envelopes)
- Supporting audit structs: `ClarificationEvent`, `UpiCommitRecord`, `UspVersionRecord`, `CobUspSnapshotPin` (serialization golden targets)

The module **does not** implement USP/UPI business logic (40.102/40.103). It defines **structural contracts**, canonical JSON serialization, envelope separation guards, and golden diff fixtures consumed by downstream W2 modules.

## Scope

**In scope (W2 Phase B target):**
- Deterministic sorted-key serialization per [20.95](../../20_requirements/20.95_ts_numeric_policy.md)
- Round-trip encode/decode for each struct skeleton
- Envelope separation: conversation-layer structs MUST NOT embed `semantic_core`, `exec_plan`, `exec_trace`
- `UspSnapshot` immutability contract for one IIInB pass (pin `usp_version_ref`)
- Golden JSON fixtures for struct compliance

**Out of scope:**
- USP rule store mutation (40.102)
- UPI commit orchestration (40.103)
- Pipeline A/B basin behavior

## Flows Alignment Statement

- **Forward Flow (20-series):** Driven by [20.39](../../20_requirements/20.39_ts_core_data_structures.md) §3.1–3.2 (conversation-layer vs runtime envelope partition), [20.102](../../20_requirements/20.102_usp_requirements.md) snapshot consumption, [20.101](../../20_requirements/20.101_iiinb_requirements.md) intake-bound fields, [20.38](../../20_requirements/20.38_ts_implementation_guidelines.md) §2 envelope guards.

- **Backward Flow (40-series evidence):** None yet — Phase A only. W1 [40.101](../40.101_iiinb_prototypes/software_description.md) uses inline `UspSnapshot`; this module formalizes shared shapes for W2 integration.

- **Iterative Design Flow (50-series influence):** [50.101](../../50_thought_simulator_design/50.101_iiinb_design_spec.md) and [50.45](../../50_thought_simulator_design/50.45_data_structures.md) inform struct naming; no normative override of 20.39.

**Agreement Statement**: Provisionally aligned — Phase A scaffold only. Struct shapes must align with 20.39 and W1 IIInB evidence; Phase B golden diffs required before downstream GATE-B modules treat this as stable.

## Phase A Deliverables (this document)
- Struct responsibility map (`UspSnapshot`, `InputRepairTag`, `ConversationLayerState`, audit records)
- Envelope separation invariants
- Canonical serialization obligations
- What Phase B must explore (test matrix)
- Cross-links to W2 dependents (201, 202, 101, 207)

## Struct Contract Sketches (Draft)

### UspSnapshot
```
UspSnapshot {
  schema_version: "usp_snapshot_v1",
  usp_version_id: int,
  usp_version_ref: str,   // content-addressed digest
  rules: [UspRule],       // ACTIVE-only at snapshot boundary
}
```

### InputRepairTag
```
InputRepairTag {
  tag_id: str,
  segment_index: int,
  rule_id: str | null,
  outcome: "APPLIED" | "ESCALATED",
}
```

### ConversationLayerState
```
ConversationLayerState {
  schema_version: "conversation_layer_v1",
  conversation_id: str,
  usp_version_ref_pinned: str | null,
  pending_clarifications: int,
}
```

## What Phase B Must Explore

| # | Topic | Evidence type |
|---|--------|----------------|
| 1 | `UspSnapshot` round-trip + sorted-key JSON | structural / golden diff |
| 2 | `InputRepairTag` canonical ordering | golden diff |
| 3 | `ConversationLayerState` envelope separation (no B fields) | structural / negative |
| 4 | Audit struct exports (`ClarificationEvent`, `UpiCommitRecord`, …) | golden diff |
| 5 | Cross-fixture compatibility with 40.101 inline snapshot digest | replay |
| 6 | Schema version reject for unknown `schema_version` | negative |

## Test Matrix (Phase B draft)

| Scenario ID | HLR anchor (20.39) | Expected |
|-------------|-------------------|----------|
| `positive_usp_snapshot_roundtrip` | 022 | Identical digest after encode/decode |
| `positive_input_repair_tag_ordering` | 024 | Stable export ordering |
| `positive_conversation_layer_envelope_clean` | 021–025 | No forbidden envelope fields |
| `negative_forbidden_semantic_core_field` | envelope guard | Deterministic reject |
| `positive_golden_fixture_match` | 024 | Byte-stable vs golden JSON |

## HLR Reference (Exploratory Visibility — 20.39 §3.1–3.2)

Key anchors for this module: HLR-20.039-021 through -025 (conversation-layer partition, audit structs, canonical ordering). Full normative text remains in [20.39](../../20_requirements/20.39_ts_core_data_structures.md).

## Risks & Unknowns
- Whether `40.101` inline types migrate in-place or via import from this module (Phase B decision)
- Golden fixture location: `artifacts/` vs `fixtures/` (follow 40.20 convention)
- Level of `TpLaneView` coverage in W2 vs deferred to W3

## Traceability
- [40.510_refactor.md](../40.510_refactor.md) row 40.510-203
- [20.39_ts_core_data_structures.md](../../20_requirements/20.39_ts_core_data_structures.md)
- Appendix A.2 conversation-layer boundary (40.510)