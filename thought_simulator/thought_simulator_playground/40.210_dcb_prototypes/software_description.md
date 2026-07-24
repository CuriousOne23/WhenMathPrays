# 40.210_dcb_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP W3 Phase A review, 2026-06-08 — no blockers)
- Phase B: **complete** (2026-06-09 harness PASS; artifact generated; see verification_capsule.md)
- Program row: **40.510-407** (W3)

## Two-Phase Execution Model (Global 40.* Rule)
- Phase A: `software_description.md` only.
- Phase B: implementation after approval.

## Scaffold Metadata
- scaffold_status: Phase A complete — stub only
- intended_20_anchor: [20.106_dcb_requirements.md](../../20_requirements/20.106_dcb_requirements.md)
- intended_20_secondary: [20.165](../../20_requirements/20.165_dcb_stability_requirements.md) (qualitative stability bounds)
- upstream_playground_modules: [40.200](../40.200_ob_prototypes/software_description.md), [40.240](../40.240_tr_router_prototypes/software_description.md), [40.220](../40.220_dcb_stability_prototypes/software_description.md)
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
- TR consumption hook (joint with 40.240 W3 extension)
- Qualitative stability cross-check with 40.220

## Flows Alignment Statement

- **Forward Flow (20-series):** [20.106](../../20_requirements/20.106_dcb_requirements.md) HLR-001–036; [20.37](../../20_requirements/20.37_thought_router_tr_specification.md) §4.4 (ephemeral DCB events); after OB (40.200), before TR (40.240).
- **Backward Flow (40-series evidence):** Phase B harness (5/5 PASS, artifact dcb_verification_run_2026-06-09.json) confirms curvature-driven events, per-cycle bound, no tr_needs_update writes, canonical order, and forbidden semantic reads (audit + suppress). Joint stability with 40.220; TR hook with 40.240.
- **Iterative Design Flow (50-series influence):** Evidence package ready for 50.190 qualitative stability design.

**Agreement Statement**: Phase B complete 2026-06-09 per 40.05/40.510 W3. CP Phase A (2026-06-08) confirmed geometric-only + ephemeral boundaries; Phase B proved the matrix (curvature emit 010/011, bound 036, no flag 020, order 028, forbidden 035) with deterministic geometric observation. Handoffs to 40.200/40.240/40.220 verified. 40.190 review passed; 40.200 under review.

## CP W3 Phase A Review Record (2026-06-08)

| Check | Result |
|-------|--------|
| W3 create scope vs 40.510-407 | Pass |
| 20.106 geometric meta-basin boundaries | Pass |
| Ephemeral events (not persisted on TP) | Pass |
| No `tr_needs_update` write | Pass |
| OB → DCB → TR cycle placement | Pass |
| Handoffs to 40.200 / 40.240 / 40.220 | Pass |
| Blockers | **None** — Phase B authorized |

## Phase B Test Matrix (draft)

| Scenario | Type | HLR |
|----------|------|-----|
| Curvature exceed → event emit | Behavioral | 010, 011 |
| Per-cycle emission bound | Negative | 036 |
| No `tr_needs_update` write | Negative | 020 |
| Event batch canonical order | Structural | 028 |
| Forbidden semantic field read | Negative | 035 |