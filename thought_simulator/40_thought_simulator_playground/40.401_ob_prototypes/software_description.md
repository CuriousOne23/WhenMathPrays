# 40.401_ob_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP W3 Phase A review, 2026-06-08 — no blockers)
- Phase B: **cleared to start** — pending implementation
- Program row: **40.510-406** (W3)

## Two-Phase Execution Model (Global 40.* Rule)
- Phase A: `software_description.md` only.
- Phase B: implementation after approval.

## Scaffold Metadata
- scaffold_status: Phase A complete — stub only
- intended_20_anchor: [20.40_ob_requirements.md](../../20_requirements/20.40_ob_requirements.md)
- upstream_playground_modules: [40.501](../40.501_rb_prototypes/software_description.md), [40.37](../40.37_tr_router_prototypes/software_description.md), [40.106](../40.106_dcb_prototypes/software_description.md)
- applicability: **Pipeline A OB** — lane-local evidence extraction; pattern detector not interpreter
- program_wave: **W3**
- numbering_note: suffix `.401` aligns with 20.40; folder `40.40_scheduler_prototypes/` is scheduler glue (W5)

## Purpose

Exploratory implementation of **OB (semantic/stance basin)** per [20.40](../../20_requirements/20.40_ob_requirements.md) — deterministic **lane-local evidence extraction** feeding TR-input and TB downstream.

Responsibilities:
- Process lane-local TP views only (HLR-20.040-001)
- Emit structured evidence + bounded ΔH% records (HLR-20.040-005, -006)
- Write TR-input fields; set `tr_needs_update` when semantic-relevant inputs change (20.37 step 2)
- Messy-input concept-equivalent activation (HLR-20.040-007, 20.17)
- Overflow telemetry — no silent evidence drop (HLR-20.040-025, -026)

Does **not**:
- Perform merge/split arbitration (HLR-20.040-003)
- Act as geometric meta-basin (HLR-20.040-027) — that is DCB (40.106)
- Read `truth_hypotheses` or execution envelopes (HLR-20.040-043)
- Perform probabilistic inference (HLR-20.040-008)

## Normative A-Chain Placement

`… → ob_processing → tb_interpretation → …` per [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §2.1.

OB executes after routing/splitting; before TB and DCB→TR overlay in same cycle per 20.37/20.106 ordering.

## Scope (W3 Phase B)
- Lane-local activation fixtures
- TR-input field emission + `tr_needs_update` toggle
- ΔH% Q32.32 contribution records
- Approved MTP read-set negative tests
- Replay seed-independent outputs

## Flows Alignment Statement

- **Forward Flow (20-series):** [20.40](../../20_requirements/20.40_ob_requirements.md) HLR-001–043; [20.37](../../20_requirements/20.37_thought_router_tr_specification.md) TR-input contract.
- **Backward Flow (40-series evidence):** None — Phase A.
- **Iterative Design Flow (50-series influence):** None yet.

**Agreement Statement**: Aligned — CP review 2026-06-08 confirms OB as A-only lane-local evidence basin per 20.40, distinct from B-side OpBeh (W4) and DCB (40.106). Phase B must wire TR-input + `tr_needs_update` handoff for 40.37 and evidence path to 40.601 (TB).

## CP W3 Phase A Review Record (2026-06-08)

| Check | Result |
|-------|--------|
| W3 create scope vs 40.510-406 | Pass |
| 20.40 OB lane-local evidence extraction | Pass |
| TR-input + `tr_needs_update` emission | Pass |
| Not geometric meta-basin (DCB separate) | Pass |
| Approved MTP read-set boundaries | Pass |
| Handoffs to 40.501 / 40.37 / 40.106 / 40.601 | Pass |
| Blockers | **None** — Phase B authorized |

## Phase B Test Matrix (draft)

| Scenario | Type | HLR |
|----------|------|-----|
| Lane-local evidence emit | Behavioral | 001, 022 |
| `tr_needs_update` set on change | Behavioral | 20.37 step 2 |
| Forbidden truth_hypotheses read | Negative | 043 |
| Overflow deterministic degrade | Negative | 025, 026 |
| Replay identical outputs | Replay | 009 |