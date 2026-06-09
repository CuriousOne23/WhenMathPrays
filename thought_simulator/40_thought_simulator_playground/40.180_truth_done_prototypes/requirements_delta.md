# 40.180_truth_done_prototypes / requirements_delta.md

## Status
Phase B complete — HLR mapping exercised and recorded from 2026-06-09 verification run (5/5 PASS). Artifact: artifacts/truth_done_verification_run_2026-06-09.json

## Primary 20-series anchors
- [20.140_truth_evaluation_requirements.md](../../20_requirements/20.140_truth_evaluation_requirements.md) — HLR-20.140-001–045 (terminal truth/done gate, messy handling, ordering, forbidden reads, determinism)
- [20.60_tb_requirements.md](../../20_requirements/20.60_tb_requirements.md) — TB as sole provider of truth_hypothesis_records (pre-Truth/Done)
- [20.36_canonical_end_to_end_trace.md](../../20_requirements/20.36_canonical_end_to_end_trace.md) — A-chain placement: ... → merging → truth_done → mtp_update

## Flows Alignment Statement

- **Forward Flow (20-series):** Truth/Done evaluation per 20.140 after merge (40.170 lineage) and before mtp_update (40.150); TB records only (40.230/20.60); explicit completion gate with H% and reason codes.
- **Backward Flow (40-series evidence):** Phase B runs using mock TB inputs confirm: happy path emits SUPPORTED hypotheses + DONE; messy_input_record forces BLOCKED/PARTIAL + blocked flag + codes (029/030); routing_metadata presence produces FORBIDDEN_READ audit and suppresses hypotheses (043); output hypotheses always canonically sorted (038); repeated identical calls produce byte-identical as_dict JSON (024, replay). No changes to 20.xx normative text required.
- **Iterative Design Flow (50-series influence):** Provides concrete evidence for 50 design on truth accounting policy, messy classification placement, H% formula, and A/B freeze around the gate. May influence 50.140 or 50.36 updates.

**Agreement Statement**: Phase B complete per 40.05 (capsule structure, harness entrypoint, artifacts) and 40.510 W3 (truth/done as A primitive gate). Full traceability from scenarios to 20.140 HLRs. Ready for 30.00 normalization (coverage note + glossary) and 50 insight per wave protocol. Handoffs to 40.150 (commit gate) and 40.230 (TB record source) exercised via contract shapes.

## Phase B HLR Exercise Summary (2026-06-09 harness run)

- Happy truth + done after merge: HLR-20.140-019 (placement), -021 (emit hypotheses + done_state + H%). Evidence: 2 hypotheses (SUPPORTED), done=DONE, h_percent attached.
- Blocked by messy-input: HLR-20.140-029 (messy detection), -030 (block/partial + codes). Evidence: MI_VAGUE → BLOCKED, blocked_by_messy_input=True, reason_codes includes class.
- Forbidden routing_metadata read: HLR-20.140-043 (no B / routing reads in this stage). Evidence: routing_metadata in input → FORBIDDEN_READ in audit, hypotheses=[], done=BLOCKED with code.
- Canonical ordering golden diff: HLR-20.140-038 (deterministic canonical order of hypotheses). Evidence: input h2 then h1 → output sorted ["h1","h2"]; stable golden form.
- Replay seed-independent outputs: HLR-20.140-024 (replayable, seed-independent). Evidence: identical input dicts → identical full output JSON (sort_keys).

All 045 HLRs addressed at high level via the 5 scenarios + explicit field rules. Core contract (TB records in, truth_hypotheses + done_state + audit out) stable.

Schema/audit per 20.140 exercised directly (audit records for violations, reason_codes, completion_status enum).

## Impacted / Referenced Documents
- 40.150_mtp_prototypes (downstream consumer of truth_hypotheses / done_state / H% before commit)
- 40.170_split_merge_prototypes (upstream merge produces input context)
- 40.230_tb_prototypes (upstream producer of truth_hypothesis_records)
- 20.140, 20.60, 20.36 (as above)
- 40.05_master_program_guide.md (process)
- 30.30_verification_glossary.md (for future 30 promotion of terms like done_state, completion_reason_codes)
- 40.510_refactor.md (program tracking + W3 wave)
- 20.115 / 20.120 (MTP will snapshot the truth hypotheses at commit)

## Migration / Implementation Notes
- Self-contained (no upstream prototype import needed; 40.230 still pending so harness uses pure dict mocks matching expected TB record shape).
- Classes are simple dataclasses (TruthHypothesisRecord, DoneState, TruthDoneOutput) for easy JSON round-trip and 40.150 consumption.
- evaluate() signature stable: (inputs: dict, policy_signature: str, cycle_id: str) → TruthDoneOutput.
- Messy class strings passed through verbatim into reason_codes (policy owns the taxonomy).
- H% currently a simple stub (1.0 happy / 0.5 messy / 0.0 empty); real formula (evidence strength, etc.) is 20.140 / 50 territory.
- Forbidden check is presence-based (inputs.get("routing_metadata")) per 20.140-043 spirit; expands easily if more B fields are enumerated.
- Canonical sort is by hypothesis_id (string) for determinism and golden-diff friendliness.
- No latent inference anywhere — all decisions are direct field reads + tiny rules.
- When 40.230 lands, swap mocks for real TB record fixtures in a follow-up run (no API change expected).

## Open Items / Gaps
- Full H% / evidence-strength computation per 20.140 (current is illustrative; may require 20.95 numeric or 50 design).
- Exact enumeration of "forbidden" fields beyond routing_metadata (current is conservative any-truthy presence).
- Joint test with real 40.150 (pre-truth reject) and 40.230 (record shape) — deferred until those Phase B close.
- 30.00 promotion: will require 10.50 peer + normalized 30 capsule citing this + 40.150/40.230.
- 50 insight: may propose updates to 50.140 or truth accounting design docs.

All deltas incorporated as of 2026-06-09 Phase B completion. No outstanding from Phase A.
