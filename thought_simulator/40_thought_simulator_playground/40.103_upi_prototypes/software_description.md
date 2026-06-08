# 40.103_upi_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP review, 2026-06-08; 40.510-202)
- Phase B (prototype + harness + evidence): **approved** (8/8 PASS; CP review, 2026-06-08; GATE-B)
- Program row: **40.510-202** (W2) — **GATE-B**

## Two-Phase Execution Model (Global 40.* Rule)
- Phase A: define and review `software_description.md` only.
- Mandatory stop after Phase A until explicit human approval.
- Phase B (only after approval): implement `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

## Scaffold Metadata
- scaffold_status: Phase B complete (8/8 PASS; 2026-06-08)
- intended_20_anchor: [20.103_upi_requirements.md](../../20_requirements/20.103_upi_requirements.md)
- intended_20_secondary: [20.102](../../20_requirements/20.102_usp_requirements.md), [20.33](../../20_requirements/20.33_cil_requirements.md), [20.80](../../20_requirements/20.80_gb_requirements.md) §10
- prerequisite_row: **40.510-201** (USP) must be `approved` before GATE-B close on this row
- upstream_playground_modules: [40.102](../40.102_usp_prototypes/software_description.md) (USP write surface), [40.392](../40.392_core_data_structs_prototypes/software_description.md) (`UpiCommitRecord` / event shapes), [40.33](../40.33_cil_prototypes/software_description.md) (W2 wire)
- applicability: **User Preference Integrator (UPI)** — sole authorized writer of `usp_rule` entries; clarification → GB gate → USP commit
- disposition_target: promote
- program_wave: **W2** — **GATE-B** per [40.510](../40.510_refactor.md)

## Purpose

Exploratory implementation of **UPI** on the conversation layer: the only subsystem authorized to create or activate USP rules from validated `clarification_event` records.

UPI is responsible for:
- FIFO processing of `clarification_event` per conversation scope
- Mapping clarification outcomes to bounded `pattern` / `expansion` `usp_rule` fields
- GB safety evaluation before `ACTIVE` promotion (default required v0)
- `upi_commit_record` append on every attempt (`COMMITTED`, `GB_VETOED`, `REJECTED`)
- Monotonic USP `usp_version_id` advance on successful commit
- Deterministic replay: identical event sequence + GB outcomes → identical `usp_version_ref`
- Enforcing pending-commit cap and USP active-rule cap with fixed reason codes

UPI **does not**:
- Read/write Pipeline A basins or Pipeline B envelopes
- Initiate clarification (CIL emits events; IIInB escalates to CIL)
- Be invoked by IMR, OuB, or Pipeline B
- Bypass IB-Creation-Request for `MI_INCOMP`
- Depend on wall-clock ordering

## Scope

W2 Phase B explores commit orchestration with **simulated or stubbed CIL FIFO input** and **GB gate callback**. Live CIL wire extension is row 40.510-205; joint integration bundle "Track H turn-1→2" after GATE-B.

Golden fixtures MUST remain byte-stable across W2 unless `schema_version` increments (breaking change requires explicit migration note).

**GB veto reason-code propagation:** On veto, `UpiCommitRecord.commit_status = GB_VETOED`; `gb_reason_code` and `reason_codes[]` both carry the evaluator code (stub: `GB_TEST_VETO`; live: [40.36](../40.36_gb_prototypes/prototype.py) `evaluate_upi_commit` → e.g. `GB_VETO_UNSAFE_RULE`). No `usp_version_id` advance; USP remains unchanged (20.103-010, 20.102-014).

**`integration_seq` bounds:** CIL emits monotonic `integration_seq` per conversation (20.032-030); UPI sorts FIFO by this field. Playground does not cap `integration_seq` magnitude — ordering is by value, not wall-clock. Pending-commit cap (default 8, HLR-016) is the primary queue bound; overflow rejects with `UPI_RSN_002_PENDING_CAP`.

### USP store API boundary (40.102 dependency)

UPI owns **orchestration only** — validation, GB gate, audit emission, FIFO ordering. [40.102](../40.102_usp_prototypes/software_description.md) owns **store semantics** (version transitions, cap enforcement, `usp_version_record` append, `usp_version_ref` digest).

Phase B write surface (UPI → USP):
- `usp_apply_commit(commit_payload)` — sole authorized write entry; accepts bounded rule fields + transition intent (`create` / `supersede` / `revoke`); returns `{ usp_version_id, usp_version_ref, active_rule_count }` or deterministic reject with fixed reason code
- UPI does **not** call USP snapshot export (`export_snapshot` is IIInB read-only path on 40.102)
- Wire structs (`clarification_event`, `upi_commit_record`, `UspRule`) imported from [40.392](../40.392_core_data_structs_prototypes/software_description.md); neither module redefines leaf shapes

## Flows Alignment Statement

- **Forward Flow (20-series):** [20.103](../../20_requirements/20.103_upi_requirements.md) (HLR-001–022), [20.102](../../20_requirements/20.102_usp_requirements.md) (commit effects), [20.33](../../20_requirements/20.33_cil_requirements.md) (`clarification_event` source), [20.80](../../20_requirements/20.80_gb_requirements.md) §10 (GB gate/veto).

- **Backward Flow (40-series evidence):** W1 [40.207](../40.207_replay_prototypes/software_description.md) C7-D/E used **simulated** UPI/GB; this module provides live commit path for W2 replay refresh.

- **Iterative Design Flow (50-series influence):** None yet for UPI-specific 50.xx; conversation layer specs deferred until 30 promotion.

**Agreement Statement**: Aligned — Phase A + Phase B approved (CP, 2026-06-08). 8/8 harness evidence; commit pipeline aligns with [20.103](../../20_requirements/20.103_upi_requirements.md) HLR-001–022. Live GB path evidenced via [40.36](../40.36_gb_prototypes/software_description.md) `harness_w2.py`. GATE-B row 202 closed.

## Phase A Deliverables (this document)
- UPI role on conversation layer (not a basin stage)
- `clarification_event` → commit pipeline sketch
- GB gate outcomes and audit records
- What Phase B must explore + test matrix
- Dependency on 40.102 USP store

## Wire Sketches (Draft)

### clarification_event (input — from CIL)
```
clarification_event = {
  "schema_version": "clarification_event_v1",
  "event_id": str,
  "integration_seq": int,
  "pattern": str,
  "expansion": str,
  "scope": str,
  "source": "CIL" | "TEST_FIXTURE",
}
```

### upi_commit_record (output audit)
```
upi_commit_record = {
  "commit_status": "COMMITTED" | "GB_VETOED" | "REJECTED",
  "usp_version_id": int | null,
  "usp_version_ref": str | null,
  "gb_reason_code": str | null,
  "reason_codes": [str],
}
```

## What Phase B Must Explore

| # | Topic | HLR family |
|---|--------|------------|
| 1 | Sole USP write authority | 001–004 |
| 2 | FIFO `clarification_event` processing | 005–008 |
| 3 | GB gate approve vs veto | 009–011 |
| 4 | Deterministic replay of commits | 012–014 |
| 5 | USP / pending-commit caps | 015–016 |
| 6 | No Pipeline A/B mutation | 004, 017 |
| 7 | Append-only audit for MB consume | 022 |

## Test Matrix (Phase B draft)

| Scenario ID | HLR | Expected |
|-------------|-----|----------|
| `positive_single_commit` | 005, 006 | ACTIVE rule; version_id++ |
| `positive_fifo_two_events` | 005, 012 | Order-preserving commits |
| `positive_gb_approve` | 009, 011 | ACTIVE rule + audit |
| `positive_gb_veto` | 010 | `GB_VETOED`; no ACTIVE rule |
| `negative_incomplete_event` | 008 | REJECTED + reason code |
| `negative_usp_cap_overflow` | 015 | Reject commit |
| `negative_pending_commit_cap` | 016 | Queue-or-reject policy |
| `positive_replay_identical_ref` | 012 | Same ref on rerun |

## HLR Reference (Exploratory Visibility — 20.103)

Normative set: HLR-20.103-001 through -022. Full text: [20.103_upi_requirements.md](../../20_requirements/20.103_upi_requirements.md).

### HLR family → Phase-B scenario mapping

| HLR family | Topic (20.103) | Phase-B topic # | Primary scenario IDs |
|------------|----------------|-----------------|----------------------|
| 001–004 | Authority and placement | 1, 6 | structural negatives in harness setup |
| 005–008 | Clarification → commit flow | 2 | `positive_single_commit`, `positive_fifo_two_events`, `negative_incomplete_event` |
| 009–011 | GB governance | 3 | `positive_gb_approve`, `positive_gb_veto` |
| 012–014 | Determinism and replay | 4 | `positive_fifo_two_events`, `positive_replay_identical_ref` |
| 015–016 | Bounds | 5 | `negative_usp_cap_overflow`, `negative_pending_commit_cap` |
| 017–019 | Cross-program separation | 6 | structural negatives (no A/B / CIL-init bypass) |
| 020 | Parent compliance | — | cross-check vs 20.10/20.30 invariants (review gate) |
| 021 | Deterministic fixture testability | all | full test matrix |
| 022 | Append-only audit | 7 | audit asserts on every commit attempt path |

## Risks & Unknowns
- GB gate simulated vs live [40.36](../40.36_gb_prototypes/software_description.md) callback in Phase B
- CIL FIFO wire timing — stub events acceptable for GATE-B isolated harness
- Cross-turn replay refresh for 40.207 C7-D/E (W2 integration bundle)

## Traceability
- [40.510_refactor.md](../40.510_refactor.md) row 40.510-202 (**GATE-B**)
- Blocks: 40.510-205, 40.510-206, 40.510-204