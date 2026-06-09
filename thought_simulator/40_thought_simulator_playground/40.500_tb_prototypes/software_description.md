# 40.500_tb_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP review, 2026-06-08; 40.510-409)
- Phase B: **pending**
- Program row: **40.510-409** (W3)

## Two-Phase Execution Model (Global 40.* Rule)
- Phase A: `software_description.md` only.
- Phase B: implementation after approval.

## Scaffold Metadata
- scaffold_status: Phase A complete — stub only
- intended_20_anchor: [20.60_tb_requirements.md](../../20_requirements/20.60_tb_requirements.md)
- upstream_playground_modules: [40.401](../40.401_ob_prototypes/software_description.md), [40.140](../40.140_truth_done_prototypes/software_description.md)
- applicability: **TB interpretation** — five-channel truth hypothesis inputs **before** Truth/Done
- program_wave: **W3**
- numbering_note: suffix `.601` aligns with 20.60; folder `40.60_tick_cycle_skeleton/` is tick glue (W5)

## Purpose

Exploratory implementation of **Truth Basin (TB)** per [20.60](../../20_requirements/20.60_tb_requirements.md) — structured multi-channel interpretation of OB evidence **before** final Truth/Done scoring (40.140).

Responsibilities:
- Consume OB evidence + approved MTP read set (HLR-20.060-021, -039, -045)
- Emit five deterministic channels + `truth_hypothesis_records[]` (HLR-20.060-005, -022)
- Supply explicit `evidence_refs[]` traceable to OB (HLR-20.060-033)
- Enforce interpretation bounds + overflow telemetry (HLR-20.060-024, -025, -026)
- Canonical ordering for export/replay (HLR-20.060-038, -044)

Does **not**:
- Perform final truth/done scoring (HLR-20.060-033) — 40.140 owns terminal evaluation
- Read `TP.TR` / routing semantics for derivation (HLR-20.060-043)
- Use latent Bayesian inference on prior hypotheses (HLR-20.060-041)

## Normative A-Chain Placement

`… → ob_processing → **tb_interpretation** → delta_h_normalization → merging → truth_done_evaluation → mtp_update` per [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §2.1.

## Scope (W3 Phase B)
- Five-channel interpretation fixtures
- `truth_hypothesis_records[]` golden ordering
- Overflow / bound exceedance negative paths
- Handoff to 40.140 — TB records as sole truth inputs
- Strip-replay preservation in `semantic_core` (HLR-20.060-036)

## Flows Alignment Statement

- **Forward Flow (20-series):** [20.60](../../20_requirements/20.60_tb_requirements.md) HLR-001–045; downstream [20.140](../../20_requirements/20.140_truth_evaluation_requirements.md).
- **Backward Flow (40-series evidence):** None — Phase A.
- **Iterative Design Flow (50-series influence):** None yet.

**Agreement Statement**: Provisionally aligned — TB stops at interpretation inputs; Truth/Done remains separate module. Phase B must prove channel ordering and OB-only evidence refs.

## Phase B Test Matrix (draft)

| Scenario | Type | HLR |
|----------|------|-----|
| Five-channel happy path | Behavioral | 005, 022 |
| Forbidden TR field read | Negative | 043 |
| Overflow no silent drop | Negative | 025, 026 |
| Channel map canonical order | Golden diff | 044 |
| Replay seed-independent | Replay | 009, 036 |