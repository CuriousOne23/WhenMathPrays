# 40.200_ob_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP W3 Phase A review, 2026-06-08 — no blockers)
- Phase B: **complete** (2026-06-09 harness PASS; artifact generated; see verification_capsule.md)
- Program row: **40.510-406** (W3)

## Two-Phase Execution Model (Global 40.* Rule)
- Phase A: `software_description.md` only.
- Phase B: implementation after approval.

## Scaffold Metadata
- scaffold_status: Phase A complete — stub only
- intended_20_anchor: [20.40_ob_requirements.md](../../20_requirements/20.40_ob_requirements.md)
- upstream_playground_modules: [40.190](../40.190_rb_prototypes/software_description.md), [40.240](../40.240_tr_router_prototypes/software_description.md), [40.210](../40.210_dcb_prototypes/software_description.md)
- applicability: **Pipeline A OB** — lane-local evidence extraction; pattern detector not interpreter
- program_wave: **W3**
- numbering_note: suffix `.401` aligns with 20.40; folder `40.270_scheduler_prototypes/` is scheduler glue (W5)

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
- Act as geometric meta-basin (HLR-20.040-027) — that is DCB (40.210)
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

- **Forward Flow (20-series):** [20.40](../../20_requirements/20.40_ob_requirements.md) HLR-001–043; [20.37](../../20_requirements/20.37_thought_router_tr_specification.md) TR-input + tr_needs_update contract; [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §2.1.
- **Backward Flow (40-series evidence):** Phase B harness (5/5 PASS, artifact ob_verification_run_2026-06-09.json) confirms lane-local evidence emission, tr_needs_update on semantic change, forbidden truth_hypotheses read (audit + degrade), overflow degrade with telemetry, and seed-independent replay. Joint with 40.190/40.240/40.230.
- **Iterative Design Flow (50-series influence):** Evidence package (capsule + delta + artifact) ready for 50 insight on OB pattern detection vs. B-side and DCB.

**Agreement Statement**: Phase B complete 2026-06-09 per 40.05/40.510 W3. CP Phase A (2026-06-08) confirmed lane-local + TR handoff boundaries; Phase B proved the matrix (emit 001/022, tr flag per 20.37, forbidden 043, overflow 025/026, replay 009) with deterministic canonical outputs and strict read-set enforcement. Handoffs to 40.190 (upstream), 40.240 (TR), 40.230 (TB) verified. 40.180 review passed; 40.190 under review.

## CP W3 Phase A Review Record (2026-06-08)

| Check | Result |
|-------|--------|
| W3 create scope vs 40.510-406 | Pass |
| 20.40 OB lane-local evidence extraction | Pass |
| TR-input + `tr_needs_update` emission | Pass |
| Not geometric meta-basin (DCB separate) | Pass |
| Approved MTP read-set boundaries | Pass |
| Handoffs to 40.190 / 40.240 / 40.210 / 40.230 | Pass |
| Blockers | **None** — Phase B authorized |

## Phase B Test Matrix (draft)

| Scenario | Type | HLR |
|----------|------|-----|
| Lane-local evidence emit | Behavioral | 001, 022 |
| `tr_needs_update` set on change | Behavioral | 20.37 step 2 |
| Forbidden truth_hypotheses read | Negative | 043 |
| Overflow deterministic degrade | Negative | 025, 026 |
| Replay identical outputs | Replay | 009 |