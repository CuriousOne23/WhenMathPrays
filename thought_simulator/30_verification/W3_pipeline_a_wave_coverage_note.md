# W3 Pipeline A Wave Coverage Note

**Date:** 2026-06-09  
**Wave:** W3 (40.150–40.260; Pipeline A primitives per 40.510 rows 401–412)  
**Deliverable:** 40.510 §4.2.2 step 2 — 30 normalize: HLR mapping from 40 capsules, glossary alignment (30.30), open gaps; all 40 Phase B approved.

## Promoted modules

| 40 source | 40 capsule / artifact | 30 module (if promoted) | Harness | HLR / contract coverage |
|-----------|-----------------------|-------------------------|---------|-------------------------|
| 40.150_mtp_prototypes | verification_capsule.md; mtp_verification_run_2026-06-09.json | 30.150_tp_lifecycle | 5/5 PASS | 20.115, 20.120 (commit_id, snapshot, pre-truth gate); joint 130/140 |
| 40.160_tp_lifecycle | verification_capsule.md; tp_state.json + determinism runs | (via 30.150 / 30.160) | 10/10 PASS | 20.105 (intake repair, commit boundary, tr_dirty, rb_gate, determinism) |
| 40.170_split_merge_prototypes | verification_capsule.md; split_merge_verification_run_2026-06-09.json | 30.170_ib_prototypes (partial) | 5/5 PASS | 20.130 (lineage_delta, ΔH%, limits, replay); joint 402/501/115 |
| 40.180_truth_done_prototypes | verification_capsule.md; truth_done_verification_run_2026-06-09.json | 30.180_tr_prototypes (partial) | 5/5 PASS | 20.140 (truth/done gate post-merge pre-mtp; messy, ordering, replay); joint 601/130/115 |
| 40.190_rb_prototypes | verification_capsule.md; rb_verification_run_2026-06-09.json | — | 5/5 PASS | 20.50 (routing filter, TR gate, messy preserved, overflow, replay); joint 100/101/37/130/170/240 |
| 40.200_ob_prototypes | verification_capsule.md; ob_verification_run_2026-06-09.json | — | 5/5 PASS | 20.40 (lane-local evidence, tr_input, tr_needs_update, forbidden reads, overflow, replay); joint 501/37/106/601/190/240/230 |
| 40.210_dcb_prototypes | verification_capsule.md; dcb_verification_run_2026-06-09.json | 30.190_dcb_stability_prototypes (partial) | 5/5 PASS | 20.106 (geometric meta-basin, ephemeral events, tr gate, no writes, canonical order, forbidden semantic); joint 401/37/165/200/240/220 |
| 40.220_dcb_stability_prototypes | verification_capsule.md; dcb_stability_verification_run_2026-06-09.json | 30.190_dcb_stability_prototypes | 5/5 PASS | 20.165 (qualitative stability: no amplification, no oscillation/runaway, read-only, contraction, observability); joint 40.210 |
| 40.230_tb_prototypes | verification_capsule.md; tb_verification_run_2026-06-09.json | 30.180_tr_prototypes (partial) | 5/5 PASS | 20.60 (5-channel interp, truth_hypotheses with evidence_refs, forbidden TR, overflow, canonical, replay); joint 200/180 |
| 40.240_tr_router_prototypes | verification_capsule.md; tr_verification_run_2026-06-09.json (W3) + legacy 2026-06-03 | 30.180_tr_prototypes | 10/10 PASS (W3) | 20.37 (on-TP: tr_needs_update gate, OB TR-input + DCB events, atomic TP.TR + clear flag; DCB-direct reject); proxy regression; joint 40.210/40.200 |
| 40.250_ib_prototypes | verification_capsule.md; ib_verification_run_2026-06-09.json (W3) + legacy 2026-06-03 | 30.170_ib_prototypes | 10/10 PASS (W3) | 20.90/20.17 (async GB-approved creation, bounded evolve, split/merge lineage, promote/retire, safe-boundary, no OUB bypass, IIInB/IB/IMR seam, 40.60 CIL cross); W3 extension |
| 40.260_basin_prototypes | verification_capsule.md; basin_verification_run_2026-06-09.json (W3) + legacy 2026-05-27 | 30.160_basin_prototypes | 5/5 PASS (W3) | 20.01 B2 + cross (decompose to RB/OB/DCB/TB/IB contracts 405–411; split contracts, no collapse, strip-replay without legacy generic IDs); joint 405–411 |

## Contract check (W3 insight targets from 40.510)

| Contract / Invariant | Status | Evidence |
|----------------------|--------|----------|
| Normative A-chain order (InB → ... → RB → OB → DCB → TR → TB → ... → truth_done → mtp_update) | OK | All 40 capsules reference 20.36 §2.1; 40.260 decomposition scenario; 40.240 on-TP gate |
| `commit_id` / snapshot boundary before B (no lane_id in B fixtures) | OK | 40.150 commit_id; 40.260 W3 note on A freeze; 40.510 A-meaning freeze |
| RB / OB / DCB / TB / IB roles not collapsed (split contracts) | OK | 40.260 positive_w3_basin_decomposition (role metadata, distinct basin_ids, per-role replay) |
| `tr_needs_update` gating + atomic TP.TR (no direct DCB to RB) | OK | 40.240 W3-TC003/004 negatives + success cases; 40.210 DCB no-write; 40.200 tr_needs_update |
| Lineage / ΔH% / provenance preservation across splits/merges | OK | 40.170 lineage_delta; 40.260 decomposition + 40.170/40.150 joints |
| Messy-input handling at safe boundaries (no smoothing in RB/OB/TB) | OK | 40.190/40.200/40.230 messy cases; 40.250 safe_boundary |
| Strip-replay / determinism independent of legacy generic basin IDs | OK | 40.260 W3 replay; all 40 capsules have determinism sections |
| Approved read-sets (no truth_hypotheses in OB/DCB/TB early; no TR in TB) | OK | 40.200/40.210/40.230 forbidden read negatives; 40.180/40.140 |

## Glossary alignment ([30.30](../30_verification/30.30_verification_glossary.md))

- New/updated terms from W3: `tr_needs_update` (gating), `ephemeral_event` (DCB), `truth_hypothesis_record`, `directional_change_event`, `basin_role` (decomposition), `IIInB_repair_escalation`, `IMR_A_pipeline`.
- All exercised in 40 capsules; added to 30.30 where missing (cross-ref 30.30_verification_glossary updates).
- Reason codes, provenance, verification_digest standardized across 40 W3.

## Open gaps (non-blocking for W3 `continue` to 50 insight)

| Area | Owner | Notes |
|------|-------|-------|
| 40.240 full field-level TP.TR population + live 40.200/40.210 joints | 50 insight / 30.180 | W3 harness used mocks; proxy regression ok |
| 40.260 full role-specific event sets for all 5 (RB/OB/DCB/TB/IB) | 50 / later 30 | Current W3 demo uses RB/OB exemplars; extensible |
| 40.250/40.170/40.180 live cross with 40.60 IIInB unknown-token CIL | 30.170/30.180 | W3 scenarios simulated; 40.60 W2 evidence exists |
| Dedicated 50 design specs for basins / TR on-TP | 50 insight | 50.190 etc. to cite these 30/40 capsules |
| 40.510-410/411/412 regression of old pre-W3 artifacts into new contracts | 30 audit | Legacy retained; new 2026-06-09 runs supersede for promotion |
| Full 30.XXX capsules for all 12 (some partial via 30.150/160/170/180/190) | 30 | Wave note aggregates 40 capsules; individual 30 promotion per module as needed |

## 10.50 peers (where applicable for W3)

- 40.250/40.260: Existing 10.50.170/10.50.80/90/140 etc. from prior; W3 deltas in 30 capsules.
- Cross: 10.50.180 (TR), 10.50.190 (basins) to receive W3 evidence.
- No new 10.50 for early W3 (401-409) beyond prior promotions.

See the new [40_to_10.50_design_requirements_guide.md](../10_thought_simulator_req/docs/40_to_10.50_design_requirements_guide.md) for the formal process of translating 40 Phase B evidence (including via wave notes) into 10.50 anchors. The 50_to_10.50_flow_down_protocol.md will be used for any refinements once W3 50 insight begins.

## Inventory updates

- [30.01_verification_inventory_index.md](../30_verification/30.01_verification_inventory_index.md) — W3 rows 401–412 promoted via this note + individual 30.XXX where present (30.150/160/170/180/190).
- [30.30_verification_glossary.md](../30_verification/30.30_verification_glossary.md) — W3 terms (tr_needs_update, ephemeral_event, basin_role, IIInB_repair_escalation, etc.) aligned.
- 40.510 wave log updated with this 30 normalize entry.
- 40 W3 directories (150–260): source of Phase B capsules + 2026-06-09 artifacts (read-only for 30.00); promotion recorded here (wave note), in 30.01 W3 table, relevant 30.XXX peers (e.g. 30.180), and 10.50 peers (e.g. 10.50.180 for TR). No modifications to 40/ prototype deltas required by 30.00.

## Decision

W3 30 normalize complete. Proceed to 50 insight (wave-level + module 50 design specs citing these capsules). All 40 Phase B evidence promoted. Ready for `continue` + 50-note. 

**Next:** 50 insight pass for W3 (A-chain contracts, decomposition, on-TP TR). GATE for W3 if required.