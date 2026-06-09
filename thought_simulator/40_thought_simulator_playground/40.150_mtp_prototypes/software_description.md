# 40.150_mtp_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP W3 Phase A review, 2026-06-08 — no blockers)
- Phase B (prototype + harness + evidence): **cleared to start** — pending implementation
- Program row: **40.510-401** (W3) — **A-chain anchor** (`commit_id` / `mtp_update`)

## Two-Phase Execution Model (Global 40.* Rule)
- Phase A: define and review `software_description.md` only.
- Mandatory stop after Phase A until explicit human approval.
- Phase B (only after approval): implement `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

## Scaffold Metadata
- scaffold_status: Phase A complete — scaffold stub only
- intended_20_anchor: [20.115_mtp_requirements.md](../../20_requirements/20.115_mtp_requirements.md), [20.120_mtp_schema_requirements.md](../../20_requirements/20.120_mtp_schema_requirements.md)
- intended_20_secondary: [20.206](../../20_requirements/20.206_pipeline_a_b_synchronization_contract.md) (`commit_id` handoff), [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §2.1 (`mtp_update` terminal stage)
- upstream_playground_modules: [40.170](../40.170_split_merge_prototypes/software_description.md) (merge before commit), [40.180](../40.180_truth_done_prototypes/software_description.md) (truth/done gate), [40.160_tp](../40.160_tp_lifecycle/software_description.md) (lane contributions)
- applicability: **MTP lifecycle owner** — aggregation, pre-commit mutation, `mtp_update`, `commit_id` emission, `semantic_core` freeze for Pipeline B
- disposition_target: promote (GATE prerequisite for W4/W5)
- program_wave: **W3** per [40.510](../40.510_refactor.md) §4.2
- numbering_note: suffix `.115` aligns with 20.115; avoids collision with legacy MTP folders under `40.9x`

## Purpose

Exploratory implementation of the **Meaning Trajectory Point (MTP)** as the authoritative Pipeline A meaning store and the sole normative **`mtp_update` / `commit_id` publisher** per [20.115](../../20_requirements/20.115_mtp_requirements.md) and [20.206](../../20_requirements/20.206_pipeline_a_b_synchronization_contract.md).

MTP is responsible for:
- Hosting authoritative `semantic_core` after successful `mtp_update` (HLR-20.115-027)
- Emitting exactly one immutable `commit_id` per `mtp_update` (HLR-20.115-034, -035)
- Publishing `mtp_commit_record` with `semantic_snapshot_ref` (HLR-20.115-036, -037)
- Deterministic lane merge integration before Truth/Done (HLR-20.115-031, -040)
- Append-only supervisory and lineage audit (HLR-20.115-010, -011)

MTP **does not**:
- Carry `exec_plan`, `exec_trace`, or Pipeline B routing artifacts (HLR-20.115-028)
- Accept Pipeline B writes or IMR Type B direct mutation (HLR-20.115-030)
- Expose `lane_id` / `tp_id` as B routing inputs (HLR-20.115-029)
- Run `mtp_update` before Truth/Done completes (HLR-20.115-032, -033)

## Normative A-Chain Placement

Per [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §2.1, MTP `mtp_update` is the **terminal Pipeline A stage**:

`… → merging → truth_done_evaluation → **mtp_update**`

Optional Track H prefix: `InB → IIInB → RB → …` (W1 modules).

## Scope

**In scope (W3 Phase B target):**
- MTP create / pre-commit field updates at safe boundaries
- Lane contribution aggregation and merge integration hooks
- Truth/Done completion gate — `mtp_update` only after explicit pass or policy skip record
- `commit_id` derivation and `mtp_commit_record` emission
- `semantic_snapshot_ref` content-hash binding
- Negative: reject B-envelope fields on MTP core; reject pre-truth `mtp_update`
- Replay: identical inputs → identical `commit_id` and snapshot bytes

**Out of scope:**
- Pipeline B realization (W4)
- A↔B orchestration glue (40.206 — W5)
- Full multi-lane scheduler integration (40.270 — W5)

## Flows Alignment Statement

- **Forward Flow (20-series):** Driven by [20.115](../../20_requirements/20.115_mtp_requirements.md) (HLR-001–040), [20.120](../../20_requirements/20.120_mtp_schema_requirements.md) schema, [20.206](../../20_requirements/20.206_pipeline_a_b_synchronization_contract.md) commit contract, [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) stage order.

- **Backward Flow (40-series evidence):** None yet — Phase A only. W1/W2 modules do not implement `mtp_update`; this module closes the A-chain freeze seam.

- **Iterative Design Flow (50-series influence):** No 50.115 design spec yet; 20.115 remains authoritative until W3 Phase B evidence.

**Agreement Statement**: Aligned — CP review 2026-06-08 confirms MTP as sole `commit_id` / `mtp_update` owner and A-chain terminal stage per 20.115/20.206. Phase B must prove merge→truth→commit ordering and B-envelope rejection before W4 entry (40.510 A.1 hard dep on 401).

## CP W3 Phase A Review Record (2026-06-08)

| Check | Result |
|-------|--------|
| W3 create scope vs 40.510-401 | Pass |
| `commit_id` / `semantic_snapshot_ref` contract | Pass |
| A-terminal `mtp_update` placement (20.36 §2.1) | Pass |
| B-envelope rejection on MTP core | Pass |
| Hard dep for W4/W5 (501, 307) acknowledged | Pass |
| Blockers | **None** — Phase B authorized |

## Phase A Deliverables (this document)
- MTP role, boundaries, and A-chain terminal placement
- `commit_id` / `semantic_snapshot_ref` contract sketch
- Phase B test matrix (positive commit, negative pre-truth commit, B-field reject, replay digest)
- HLR exploratory index (20.115-027–040, 20.120)
- Hard dependency note for rows 501, 307, W4

## Phase B Test Matrix (draft)

| Scenario | Evidence type | Primary HLR |
|----------|---------------|-------------|
| Happy `mtp_update` after truth pass | Behavioral + Structural | 20.115-032, -034, -036 |
| Reject `mtp_update` before truth | Negative | 20.115-032 |
| Reject `exec_plan` on MTP core | Negative | 20.115-028 |
| Identical replay → same `commit_id` | Replay + Golden diff | 20.115-039, 20.95 |
| Lane merge then commit immutability | Behavioral | 20.115-040 |