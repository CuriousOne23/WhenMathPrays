# 40.130_split_merge_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP W3 Phase A review, 2026-06-08 — no blockers)
- Phase B: **cleared to start** — pending implementation
- Program row: **40.510-403** (W3)

## Two-Phase Execution Model (Global 40.* Rule)
- Phase A: `software_description.md` only. Mandatory stop until approval.
- Phase B: prototype, harness, capsule, delta, artifacts.

## Scaffold Metadata
- scaffold_status: Phase A complete — stub only
- intended_20_anchor: [20.130_splitting_and_merging_requirements.md](../../20_requirements/20.130_splitting_and_merging_requirements.md)
- upstream_playground_modules: [40.20_tp](../40.20_tp_lifecycle/software_description.md), [40.501](../40.501_rb_prototypes/software_description.md) (split/merge arbitration), [40.115](../40.115_mtp_prototypes/software_description.md) (merge into MTP)
- applicability: lane **split/merge** with `lineage_delta`, ΔH% ledger, safe-boundary gating
- program_wave: **W3**

## Purpose

Exploratory implementation of deterministic **TP split and lane merge** per [20.130](../../20_requirements/20.130_splitting_and_merging_requirements.md), resolving lane conflicts **before** Truth/Done and `mtp_update`.

Responsibilities:
- Deterministic split projection with parent lineage preservation (HLR-20.130-001, -005)
- Deterministic merge reconciliation into MTP-bound state (HLR-20.130-002, -008)
- Append-only `lineage_delta` audit with reason codes (HLR-20.130-004, -019)
- ΔH% contribution and missing-mass markers on split/merge outputs (HLR-20.130-015, -016)
- Safe-boundary-only mutations (HLR-20.130-010, -011)

Does **not**:
- Invent meaning beyond explicit source fields (HLR-20.130-006)
- Bypass GB supervisory pathways (HLR-20.130-022)
- Run merge after Truth/Done (downstream of 40.140)

## Normative A-Chain Placement

[20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §2.1: `routing → splitting → ob_processing → … → merging → truth_done_evaluation → mtp_update`.

Split follows routing; merge precedes truth/done.

## Scope (W3 Phase B)
- Split/merge fixtures with bounded lane counts
- `lineage_delta` golden serialization
- ΔH% trajectory field updates (Q32.32 per 20.95)
- Overflow/defer reject paths (HLR-20.130-013)
- Replay equivalence for identical effective state

## Flows Alignment Statement

- **Forward Flow (20-series):** [20.130](../../20_requirements/20.130_splitting_and_merging_requirements.md) HLR-001–026; [20.105](../../20_requirements/20.105_tp_requirements.md) TP carrier; [20.115](../../20_requirements/20.115_mtp_requirements.md) merge-before-commit.
- **Backward Flow (40-series evidence):** None — Phase A.
- **Iterative Design Flow (50-series influence):** None yet.

**Agreement Statement**: Aligned — CP review 2026-06-08 confirms split/merge before truth/done, `lineage_delta` audit, and ΔH% ledger per 20.130. Phase B must evidence RB arbitration handoff (40.501) and MTP-bound merge (40.115) without repair logic bleed.

## CP W3 Phase A Review Record (2026-06-08)

| Check | Result |
|-------|--------|
| W3 create scope vs 40.510-403 | Pass |
| 20.130 split/merge + `lineage_delta` | Pass |
| ΔH% ledger obligations | Pass |
| A-chain placement (split before OB; merge before truth) | Pass |
| Handoffs to 40.20_tp / 40.501 / 40.115 | Pass |
| Blockers | **None** — Phase B authorized |

## Phase B Test Matrix (draft)

| Scenario | Type | HLR |
|----------|------|-----|
| Nominal split → lane outputs | Behavioral | 001, 005, 015 |
| Nominal merge → MTP-bound state | Behavioral | 002, 008, 016 |
| Limit exceed → deterministic reject | Negative | 012, 013 |
| `lineage_delta` golden diff | Golden diff | 004, 019 |
| Replay identical state | Replay | 017 |