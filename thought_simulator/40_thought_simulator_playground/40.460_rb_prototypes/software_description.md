# 40.460_rb_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP W3 Phase A review, 2026-06-08 — no blockers)
- Phase B: **cleared to start** — pending implementation
- Program row: **40.510-405** (W3)

## Two-Phase Execution Model (Global 40.* Rule)
- Phase A: `software_description.md` only.
- Phase B: implementation after approval.

## Scaffold Metadata
- scaffold_status: Phase A complete — stub only
- intended_20_anchor: [20.50_rb_requirements.md](../../20_requirements/20.50_rb_requirements.md)
- intended_20_secondary: [20.17](../../20_requirements/20.17_messy_input_handling.md), [20.37](../../20_requirements/20.37_thought_router_tr_specification.md) (TR gating)
- upstream_playground_modules: [40.100](../40.100_inb_prototypes/software_description.md), [40.101](../40.101_iiinb_prototypes/software_description.md), [40.37](../40.37_tr_router_prototypes/software_description.md)
- applicability: **Routing Basin (RB)** — fan-out after intake repair; `InB → IIInB → RB` handoff
- program_wave: **W3**
- numbering_note: suffix `.501` aligns with 20.50; folder `40.50_regulator_prototypes/` is the regulator (20.150 ΔH%) — distinct collision per [40.510 §3](../40.510_refactor.md)

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
- Perform `input_semantic_repair` (40.101)
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

- **Forward Flow (20-series):** [20.50](../../20_requirements/20.50_rb_requirements.md) HLR-001–045; [20.101](../../20_requirements/20.101_iiinb_requirements.md) handoff; [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §2.1.1.
- **Backward Flow (40-series evidence):** W1 40.100/101 demonstrate intake; RB module isolates post-repair fan-out.
- **Iterative Design Flow (50-series influence):** None yet.

**Agreement Statement**: Aligned — CP review 2026-06-08 confirms RB as routing-only post-intake per 20.50; `InB → IIInB → RB` handoff with no repair logic in RB. Phase B must prove TR gating (40.37) and split/merge arbitration handoff (40.130).

## CP W3 Phase A Review Record (2026-06-08)

| Check | Result |
|-------|--------|
| W3 create scope vs 40.510-405 | Pass |
| 20.50 RB routing + routing filter | Pass |
| `InB → IIInB → RB` handoff (20.36 §2.1.1) | Pass |
| No repair logic in RB | Pass |
| TR gating / split-merge arbitration scope | Pass |
| Handoffs to 40.100/101/37/130 | Pass |
| Blockers | **None** — Phase B authorized |

## Phase B Test Matrix (draft)

| Scenario | Type | HLR |
|----------|------|-----|
| Post-IIInB fan-out | Behavioral | 001, 027 |
| TR skipped when flag false | Negative | 027, 028 |
| Messy-input preserved routing | Behavioral | 009, 010 |
| Overflow reject-with-audit | Negative | 024, 029 |
| Routing filter replay | Replay | 004, 036 |