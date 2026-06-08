# 40.102_usp_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP review, 2026-06-08; 40.510-201)
- Phase B (prototype + harness + evidence): **approved** (8/8 PASS; CP review, 2026-06-08; GATE-B)
- Program row: **40.510-201** (W2) — **GATE-B**

## Two-Phase Execution Model (Global 40.* Rule)
- Phase A: define and review `software_description.md` only.
- Mandatory stop after Phase A until explicit human approval.
- Phase B (only after approval): implement `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

## Scaffold Metadata
- scaffold_status: Phase B complete (8/8 PASS; 2026-06-08)
- intended_20_anchor: [20.102_usp_requirements.md](../../20_requirements/20.102_usp_requirements.md)
- intended_20_secondary: [20.103](../../20_requirements/20.103_upi_requirements.md) (write path), [20.101](../../20_requirements/20.101_iiinb_requirements.md) (read path)
- upstream_playground_modules: [40.392](../40.392_core_data_structs_prototypes/software_description.md) (`UspRule` / `UspSnapshot` shapes), [40.101](../40.101_iiinb_prototypes/software_description.md) (consumer)
- applicability: versioned **User Shorthand Profile (USP)** rule store — read-only to IIInB; writes only via UPI commit
- disposition_target: promote
- program_wave: **W2** — **GATE-B prerequisite** per [40.510](../40.510_refactor.md)

## Purpose

Exploratory implementation of the **USP** — the durable conversation-layer store for explicit shorthand rules used by IIInB during `input_semantic_repair`.

USP is responsible for:
- Storing only explicit shorthand rules from approved clarification outcomes (no latent inference)
- Producing immutable read-only snapshots pinned by `usp_version_ref` for IIInB
- Monotonic `usp_version_id` and content-addressed `usp_version_ref` on each commit
- Rule states: `ACTIVE`, `SUPERSEDED`, `REVOKED` with deterministic precedence
- Bounded active rule count with deterministic cap-overflow reject
- Append-only `usp_version_record` audit trail (COB-visible)
- Canonical serialization for replay export per [20.95](../../20_requirements/20.95_ts_numeric_policy.md)

USP **does not**:
- Write TP, MTP, `semantic_core`, Pipeline B envelopes, or basin internals
- Accept writes except via UPI-authorized commit pathway
- Perform per-turn meaning construction or routing
- Guess expansions (IIInB escalates per 20.101)

## Scope

W2 Phase B explores the **store + snapshot + version transition** core. Full multi-turn CIL→UPI→GB wire is evidenced jointly with 40.103/40.33/40.36; USP module isolates store semantics.

Golden fixtures MUST remain byte-stable across W2 unless `schema_version` increments (breaking change requires explicit migration note). Future `usp_snapshot_v2` (or successor) requires explicit version negotiation before COB/IIInB pin authority transfers off `usp_snapshot_v1`.

### UspRule struct authority

`UspRule` is **not redefined here** — canonical leaf shape is owned by [40.392](../40.392_core_data_structs_prototypes/software_description.md) (W2 export authority; field-compatible with [40.101 `UspRule`](../40.101_iiinb_prototypes/prototype.py)). This module implements store semantics, version transitions, and snapshot assembly over imported struct shapes.

## Flows Alignment Statement

- **Forward Flow (20-series):** [20.102](../../20_requirements/20.102_usp_requirements.md) (HLR-001–024), [20.101](../../20_requirements/20.101_iiinb_requirements.md) read-only consume (006–008), [20.32](../../20_requirements/20.32_cob_requirements.md) snapshot pins (010), [20.80](../../20_requirements/20.80_gb_requirements.md) §10 veto (014).

- **Backward Flow (40-series evidence):** W1 [40.101](../40.101_iiinb_prototypes/software_description.md) demonstrated read-only apply with inline `UspSnapshot`; this module replaces ad hoc store with normative USP semantics.

- **Iterative Design Flow (50-series influence):** [50.101](../../50_thought_simulator_design/50.101_iiinb_design_spec.md) `usp_version_ref` pinning contract; USP store design remains 20.102-authoritative.

**Agreement Statement**: Aligned — Phase A + Phase B approved (CP, 2026-06-08). Store boundaries, 8/8 harness evidence, and snapshot contract align with [20.102](../../20_requirements/20.102_usp_requirements.md) HLR-001–024; digest authority via [40.392](../40.392_core_data_structs_prototypes/software_description.md). GATE-B row 201 closed.

## Phase A Deliverables (this document)
- USP role and boundaries on conversation layer
- Snapshot contract for IIInB (`usp_snapshot_v1`)
- Version transition model (create / supersede / revoke)
- What Phase B must explore + test matrix
- HLR exploratory visibility index (20.102)

## Snapshot Contract (Draft — IIInB consume)

```
usp_handoff_snapshot = {
  "schema_version": "usp_snapshot_v1",
  "usp_version_id": <int>,
  "usp_version_ref": <content_hash>,
  "rules": [ { "rule_id", "pattern", "expansion", "state": "ACTIVE" } ]
}
```

IIInB loads snapshot once per repair pass; snapshot immutable until pass completes (HLR-20.102-006/007).

## What Phase B Must Explore

| # | Topic | HLR family |
|---|--------|------------|
| 1 | Read-only snapshot export for IIInB | 006–008 |
| 2 | UPI commit → monotonic version + `usp_version_ref` | 009, 018 |
| 3 | ACTIVE / SUPERSEDED / REVOKED transitions | 012–015 |
| 4 | GB veto → no ACTIVE rule | 014 |
| 5 | Active rule cap overflow reject | 016 |
| 6 | Deterministic precedence resolution | 012 |
| 7 | Fixed reason codes on reject paths | 022 |
| 8 | Canonical serialization golden diff | 019 |

## Test Matrix (Phase B draft)

| Scenario ID | HLR | Expected |
|-------------|-----|----------|
| `positive_empty_profile_snapshot` | 024 | Empty ACTIVE set; stable ref |
| `positive_single_rule_commit` | 009, 018 | version_id=1; digest stable |
| `positive_supersede_chain` | 012, 013 | One ACTIVE; prior SUPERSEDED |
| `positive_revoke_rule` | 015 | Revoked rule excluded from snapshot |
| `positive_iiinb_readonly_load` | 006, 007 | Snapshot unchanged after IIInB consume |
| `negative_cap_overflow` | 016 | Deterministic reject + reason code |
| `negative_gb_veto_no_active` | 014 | No ACTIVE entry; audit only |
| `positive_replay_identical_ref` | 018 | Same inputs → same `usp_version_ref` |

## HLR Reference (Exploratory Visibility — 20.102)

Normative set: HLR-20.102-001 through -024 (store boundary, read path, version model, caps, audit, parent cross-check). Full text: [20.102_usp_requirements.md](../../20_requirements/20.102_usp_requirements.md).

### HLR family → Phase-B scenario mapping

| HLR family | Topic (20.102) | Phase-B topic # | Primary scenario IDs |
|------------|----------------|-----------------|----------------------|
| 001–005 | Store semantics and authority | — (boundary guard) | structural negatives in harness setup |
| 006–008 | Read model (IIInB) | 1 | `positive_iiinb_readonly_load`, `positive_empty_profile_snapshot` |
| 009–012 | Versioning + COB integration | 2, 6 | `positive_single_rule_commit`, `positive_supersede_chain`, `positive_replay_identical_ref` |
| 013–015 | Rule lifecycle | 3 | `positive_supersede_chain`, `positive_revoke_rule` |
| 014 | GB veto (lifecycle) | 4 | `negative_gb_veto_no_active` |
| 016–017 | Bounds and determinism | 5 | `negative_cap_overflow` |
| 018–019 | Replay + canonical serialization | 2, 8 | `positive_replay_identical_ref`, golden diff suite |
| 020–022 | Audit and observability | 7 | reason-code asserts on all negative paths |
| 023 | Parent compliance | — | cross-check vs 20.10/20.30 invariants (review gate) |
| 024 | Deterministic fixture testability | all | full test matrix (empty, single, supersede, revoke, cap, veto) |

## Risks & Unknowns
- Simulated UPI commit API in Phase B before 40.103 lands vs minimal internal commit driver
- COB pin integration deferred to 40.32 W2 extension
- Parameter defaults (256 rules, etc.) — playground fixtures vs [20.90](../../20_requirements/20.90_ts_parameter_table.md)

## Traceability
- [40.510_refactor.md](../40.510_refactor.md) row 40.510-201 (**GATE-B**)
- Blocks: 40.510-202, 40.510-204, 40.101 live USP path