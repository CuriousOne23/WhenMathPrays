# 40.106_dcb_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP review, 2026-06-08; 40.510-407)
- Phase B: **pending**
- Program row: **40.510-407** (W3)

## Two-Phase Execution Model (Global 40.* Rule)
- Phase A: `software_description.md` only.
- Phase B: implementation after approval.

## Scaffold Metadata
- scaffold_status: Phase A complete — stub only
- intended_20_anchor: [20.106_dcb_requirements.md](../../20_requirements/20.106_dcb_requirements.md)
- intended_20_secondary: [20.165](../../20_requirements/20.165_dcb_stability_requirements.md) (qualitative stability bounds)
- upstream_playground_modules: [40.401](../40.401_ob_prototypes/software_description.md), [40.37](../40.37_tr_router_prototypes/software_description.md), [40.165](../40.165_dcb_stability_prototypes/software_description.md)
- applicability: **DCB geometric meta-basin** — trajectory observation; ephemeral TR inputs
- program_wave: **W3**

## Purpose

Exploratory implementation of **Directional Change Basin (DCB)** per [20.106](../../20_requirements/20.106_dcb_requirements.md) — geometric trajectory observation that emits **ephemeral directional-change events** consumed by TR when `tr_needs_update` is true.

Responsibilities:
- Classify as geometric meta-basin — no semantic extraction (HLR-20.106-001, -002, -003)
- Observe persisted TP trajectory / MTP projection fields only (HLR-20.106-004–008, -025, -035)
- Emit bounded geometric events per cycle (HLR-20.106-010, -036)
- Execute after OB, before TR in same cycle (HLR-20.106-012)
- Events are ephemeral TR inputs — not persisted on TP (HLR-20.106-014)

Does **not**:
- Set `tr_needs_update` (HLR-20.106-020)
- Perform OB-class evidence extraction (HLR-20.106-002)
- Be consumed directly by RB (HLR-20.106-015)
- Read authoritative semantic MTP fields (HLR-20.106-035)

## Normative A-Chain Placement

Within `ob_processing` cycle window: **OB → DCB → TR** per 20.37 §7 and 20.106-012.

## Scope (W3 Phase B)
- Trajectory observation fixtures with synthetic geometry
- Ephemeral event batch ordering (HLR-20.106-028)
- Per-cycle emission bound negative test
- TR consumption hook (joint with 40.37 W3 extension)
- Qualitative stability cross-check with 40.165

## Flows Alignment Statement

- **Forward Flow (20-series):** [20.106](../../20_requirements/20.106_dcb_requirements.md) HLR-001–036; [20.37](../../20_requirements/20.37_thought_router_tr_specification.md) §4.4 overlay.
- **Backward Flow (40-series evidence):** None — Phase A.
- **Iterative Design Flow (50-series influence):** [50.165](../../50_thought_simulator_design/50.165_dcb_stability_design.md) qualitative only.

**Agreement Statement**: Provisionally aligned — DCB is geometric-only overlay. Phase B must prove no `tr_needs_update` writes and TR-only consumption path.

## Phase B Test Matrix (draft)

| Scenario | Type | HLR |
|----------|------|-----|
| Curvature exceed → event emit | Behavioral | 010, 011 |
| Per-cycle emission bound | Negative | 036 |
| No `tr_needs_update` write | Negative | 020 |
| Event batch canonical order | Structural | 028 |
| Forbidden semantic field read | Negative | 035 |