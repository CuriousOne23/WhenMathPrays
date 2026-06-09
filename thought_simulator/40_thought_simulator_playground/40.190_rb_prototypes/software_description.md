# 40.190_rb_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP W3 Phase A review, 2026-06-08 — no blockers)
- Phase B: **complete** (2026-06-09 harness PASS; artifact generated; see verification_capsule.md)
- Program row: **40.510-405** (W3)

## Two-Phase Execution Model (Global 40.* Rule)
- Phase A: `software_description.md` only.
- Phase B: implementation after approval.

## Scaffold Metadata
- scaffold_status: Phase A complete — stub only
- intended_20_anchor: [20.50_rb_requirements.md](../../20_requirements/20.50_rb_requirements.md)
- intended_20_secondary: [20.17](../../20_requirements/20.17_messy_input_handling.md), [20.37](../../20_requirements/20.37_thought_router_tr_specification.md) (TR gating)
- upstream_playground_modules: [40.50](../40.50_inb_prototypes/software_description.md), [40.60](../40.60_iiinb_prototypes/software_description.md), [40.240](../40.240_tr_router_prototypes/software_description.md)
- applicability: **Routing Basin (RB)** — fan-out after intake repair; `InB → IIInB → RB` handoff
- program_wave: **W3**
- numbering_note: suffix `.501` aligns with 20.50; folder `40.320_regulator_prototypes/` is the regulator (20.150 ΔH%) — distinct collision per [40.510 §3](../40.510_refactor.md)

## Purpose

Exploratory implementation of **RB routing** per [20.50](../../20_requirements/20.50_rb_requirements.md) — deterministic lane fan-out **after** Track H intake repair, with **no semantic repair logic** in RB.

Responsibilities:
- Accept handoff from IIInB (when enabled) or InB-only path per 20.36 §2.1.1
- Compute deterministic routing filter each cycle (HLR-20.050-021, -022)
- Gate TR invocation on `tr_needs_update` only (HLR-20.050-027, -028)
- Split/merge arbitration under explicit policy (HLR-20.050-006, -007, -008)
- Messy-input routing without smoothing contradiction (HLR-20.050-009, -010)
- Overflow telemetry with no silent branch drop (HLR-20.050-024, -026, -029)

Does **not**:
- Perform `input_semantic_repair` (40.60)
- Read `truth_hypotheses` for routing (HLR-20.050-043)
- Write `TP.TR` or clear `tr_needs_update` (HLR-20.050-028)
- Consume `semantic_core` outside approved read set (HLR-20.050-045)

## Normative A-Chain Placement

Track H: `InB → IIInB → **RB** → splitting → …`

RB follows intake repair; precedes split and OB stages.

## Scope (W3 Phase B)
- `InB → IIInB → RB` handoff fixtures (joint with W1)
- Routing filter log + replay reproduction
- TR gate positive/negative scenarios
- Split/merge arbitration decision logs
- Overflow bound exceedance

## Flows Alignment Statement

- **Forward Flow (20-series):** [20.50](../../20_requirements/20.50_rb_requirements.md) HLR-001–045; [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §2.1.1 `InB → IIInB → RB`.
- **Backward Flow (40-series evidence):** Phase B harness (5/5 PASS, artifact rb_verification_run_2026-06-09.json) confirms deterministic routing_filter, strict TR gate on tr_needs_update (no writes), messy preservation, overflow audit, replay identity, and split/merge arb signals. Joint with 40.170/40.240.
- **Iterative Design Flow (50-series influence):** Evidence package (capsule + delta + artifact) ready for 50 insight on routing filter schema and arbitration policy.

**Agreement Statement**: Phase B complete 2026-06-09 per 40.05/40.510 W3. CP Phase A (2026-06-08) confirmed routing-only post-intake + handoff; Phase B proved the matrix (fan-out 001/027, TR gate 027/028, messy 009/010, overflow 024/029, replay 004/036) with deterministic filter and clean boundaries. Handoffs to 40.170 (arb), 40.240 (TR), and upstream intake verified via contract.

## CP W3 Phase A Review Record (2026-06-08)

| Check | Result |
|-------|--------|
| W3 create scope vs 40.510-405 | Pass |
| 20.50 RB routing + routing filter | Pass |
| `InB → IIInB → RB` handoff (20.36 §2.1.1) | Pass |
| No repair logic in RB | Pass |
| TR gating / split-merge arbitration scope | Pass |
| Handoffs to 40.50/60/240/170 | Pass |
| Blockers | **None** — Phase B authorized |

## Phase B Test Matrix (draft)

| Scenario | Type | HLR |
|----------|------|-----|
| Post-IIInB fan-out | Behavioral | 001, 027 |
| TR skipped when flag false | Negative | 027, 028 |
| Messy-input preserved routing | Behavioral | 009, 010 |
| Overflow reject-with-audit | Negative | 024, 029 |
| Routing filter replay | Replay | 004, 036 |