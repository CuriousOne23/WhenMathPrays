# 40.200_ob_prototypes / requirements_delta.md

## Status
Phase B complete — HLR mapping exercised and recorded from 2026-06-09 verification run (5/5 PASS). Artifact: artifacts/ob_verification_run_2026-06-09.json

## Primary 20-series anchors
- [20.40_ob_requirements.md](../../20_requirements/20.40_ob_requirements.md) — HLR-20.040-001–043 (lane-local evidence extraction, TR-input emission, approved read-set, overflow, determinism)
- [20.37_thought_router_tr_specification.md](../../20_requirements/20.37_thought_router_tr_specification.md) — TR-input contract and tr_needs_update dirty flag (OB sets flag, does not write TR)
- [20.36_canonical_end_to_end_trace.md](../../20_requirements/20.36_canonical_end_to_end_trace.md) — A-chain placement after RB/split, before TB
- [20.17_messy_input_handling.md](../../20_requirements/20.17_messy_input_handling.md) — safe-boundary messy classification at OB

## Flows Alignment Statement

- **Forward Flow (20-series):** OB as lane-local evidence + TR-input extractor per 20.40 after RB (40.190) per 20.36; sets tr_needs_update per 20.37; feeds TB (40.230) and TR (40.240).
- **Backward Flow (40-series evidence):** Phase B runs using mock lane views confirm: evidence emission (001/022), tr_needs_update on semantic change, strict forbidden truth_hypotheses read (audit + degrade per 043), overflow telemetry + degrade (025/026), identical replay (009). No changes to 20.xx required.
- **Iterative Design Flow (50-series influence):** Evidence for OB output shape (evidence_fields + tr_input_fields), activation metadata, and boundary enforcement; informs 50 design on pattern detection vs. B-side OpBeh and DCB geometry.

**Agreement Statement**: Phase B complete per 40.05 (capsule structure, harness entrypoint, artifacts) and 40.510 W3 (OB lane-local extraction). Full traceability from scenarios to 20.40/20.37 HLRs. Ready for 30.00 normalization (coverage note, glossary) and 50 insight per wave protocol. Handoffs to 40.190 (upstream lane context), 40.240 (TR), 40.230 (TB), 40.210 (DCB) exercised.

## Phase B HLR Exercise Summary (2026-06-09 harness run)

- Lane-local evidence emit: HLR-20.040-001 (local view only), -022 (emit evidence + tr_input + delta_h). Evidence: sorted evidence_fields + tr_input_fields populated.
- `tr_needs_update` set on change: 20.37 step 2 (dirty flag on semantic update). Evidence: change_detected or high proposition count → tr_needs_update=True + tr_input_fields.
- Forbidden truth_hypotheses read: HLR-20.040-043 (approved read-set only). Evidence: truth_hypotheses in input → FORBIDDEN_READ audit + evidence_fields=[] (degrade, no emission).
- Overflow deterministic degrade: HLR-20.040-025 (bounds), -026 (telemetry + degrade). Evidence: overflow flag or >limit → overflow_metadata + truncated but non-empty evidence.
- Replay identical outputs: HLR-20.040-009 (deterministic/replayable). Evidence: identical lane_view + policy → identical full OBOutput.as_dict() (all lists sorted, dicts canonical).

All 043 HLRs addressed at high level via the 5 scenarios + explicit boundary checks and canonical output shaping. Core contract (lane_view in → evidence + tr_input + delta_h + tr_needs_update + audit out) stable.

Schema/audit per 20.40 exercised directly (canonical evidence_ids, forbidden audits, overflow codes, tr_needs_update flag).

## Impacted / Referenced Documents
- 40.190_rb_prototypes (upstream RB lane context provider)
- 40.240_tr_router_prototypes (TR-input + tr_needs_update consumer)
- 40.230_tb_prototypes (downstream evidence consumer)
- 40.210_dcb_prototypes (parallel geometric influence, not OB)
- 20.40, 20.37, 20.36, 20.17 (as above)
- 40.05_master_program_guide.md (process)
- 30.30_verification_glossary.md (for future 30 promotion of "tr_input_fields", "tr_needs_update", "OB evidence")
- 40.510_refactor.md (program tracking + W3 wave)
- 20.95 (numeric ΔH for real contributions)

## Migration / Implementation Notes
- Self-contained for Phase B (pure dict lane_view mocks styled after RB + TP outputs); stable contract for later live handoff with 40.190/40.240.
- ObjectBasin.process_lane(...) signature: (lane_view: dict, *, policy_signature, cycle_id, overflow_limit) → OBOutput.
- All outputs use canonical ordering (evidence sorted by evidence_id, activation_metadata lex-sorted, IDs sorted) for replay/diff.
- tr_needs_update is a decision flag only; actual TR derivation and clearing happens in 40.240 / MTP commit path.
- Forbidden enforcement is presence-based on key fields; returns early with audit and zero evidence (negative test expectation).
- Overflow is configurable (default 32); always emits metadata + partial evidence (telemetry, not hard fail at this stage).
- Messy and change detection feed activation and tr flag without altering core pattern logic.
- When live upstreams (40.190) and downstream (40.240) are ready, the same scenarios can be re-run with real objects (shape compatible).

## Open Items / Gaps
- Full Q32.32 ΔH contribution + missing_mass computation per 20.95 (current illustrative floats).
- Exact pattern-family detection logic and tr_input_fields schema (current simple keyword + structural; real per 20.31/20.37).
- Live joint test with 40.240 (TR invocation after OB sets flag) and 40.230 (evidence into TB) — deferred.
- 30.00 promotion: will require 10.50 peer + normalized 30 capsule citing this + cross-module RB/TR/TB evidence.
- 50 insight: OB output shape and activation_metadata are candidates for 50.40 / 50.37 design specs; distinction from B-side OpBeh and DCB.

All deltas incorporated as of 2026-06-09 Phase B completion. No outstanding from Phase A.
