# 40.140_truth_done_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP W3 Phase A review, 2026-06-08 — no blockers)
- Phase B: **cleared to start** — pending implementation
- Program row: **40.510-404** (W3)

## Two-Phase Execution Model (Global 40.* Rule)
- Phase A: `software_description.md` only.
- Phase B: implementation after approval.

## Scaffold Metadata
- scaffold_status: Phase A complete — stub only
- intended_20_anchor: [20.140_truth_evaluation_requirements.md](../../20_requirements/20.140_truth_evaluation_requirements.md)
- intended_20_secondary: [20.60](../../20_requirements/20.60_tb_requirements.md) (TB inputs only — no re-interpretation)
- upstream_playground_modules: [40.601](../40.500_tb_prototypes/software_description.md), [40.130](../40.130_split_merge_prototypes/software_description.md), [40.115](../40.115_mtp_prototypes/software_description.md)
- applicability: **Truth/Done terminal evaluation** — explicit completion gate before `mtp_update`
- program_wave: **W3**

## Purpose

Exploratory implementation of **Truth/Done evaluation** per [20.140](../../20_requirements/20.140_truth_evaluation_requirements.md) — the Pipeline A stage that commits `truth_hypotheses` and `done_state` **after merge** and **before** `mtp_update`.

Responsibilities:
- Consume TB-committed interpretation records only (HLR-20.140-018, -043)
- Emit `truth_hypotheses`, `done_state`, H% accounting (HLR-20.140-021)
- Execute after `merging` / `delta_h_normalization`, before `mtp_update` (HLR-20.140-019, 20.36 §2.1)
- Deterministic field-based evaluation — no latent inference (HLR-20.140-004, -022)
- Messy-input blocked completion markers (HLR-20.140-029, -030)

Does **not**:
- Re-run OB/TB/RB cycles in same pass (HLR-20.140-020)
- Read `routing_metadata` or Pipeline B envelopes (HLR-20.140-043)
- Trigger `mtp_update` (40.115 owns commit)

## Scope (W3 Phase B)
- Truth pass / fail / blocked fixtures
- `done_state.completion_reason_codes[]` canonical ordering (HLR-20.140-038)
- Negative: reject raw OB evidence reads bypassing TB refs
- Gate: block `mtp_update` when truth incomplete (joint scenario with 40.115)

## Flows Alignment Statement

- **Forward Flow (20-series):** [20.140](../../20_requirements/20.140_truth_evaluation_requirements.md) HLR-001–045; placement [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §2.1.
- **Backward Flow (40-series evidence):** None — Phase A.
- **Iterative Design Flow (50-series influence):** None yet.

**Agreement Statement**: Aligned — CP review 2026-06-08 confirms Truth/Done as explicit A-chain completion gate before `mtp_update`; TB-input-only consumption per 20.140. Phase B must prove ordering relative to 40.601 (TB) and 40.115 (commit gate).

## CP W3 Phase A Review Record (2026-06-08)

| Check | Result |
|-------|--------|
| W3 create scope vs 40.510-404 | Pass |
| 20.140 truth/done terminal evaluation | Pass |
| TB-input-only (no OB re-interpretation) | Pass |
| A-chain placement (after merge; before `mtp_update`) | Pass |
| Handoffs to 40.601 / 40.130 / 40.115 | Pass |
| Blockers | **None** — Phase B authorized |

## Phase B Test Matrix (draft)

| Scenario | Type | HLR |
|----------|------|-----|
| Happy truth + done after merge | Behavioral | 019, 021 |
| Blocked by messy-input | Negative | 029, 030 |
| Forbidden routing_metadata read | Negative | 043 |
| Canonical ordering golden diff | Golden diff | 038 |
| Replay seed-independent outputs | Replay | 024 |