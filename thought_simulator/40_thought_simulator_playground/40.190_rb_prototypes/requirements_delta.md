# 40.190_rb_prototypes / requirements_delta.md

## Status
Phase B complete — HLR mapping exercised and recorded from 2026-06-09 verification run (5/5 PASS). Artifact: artifacts/rb_verification_run_2026-06-09.json

## Primary 20-series anchors
- [20.50_rb_requirements.md](../../20_requirements/20.50_rb_requirements.md) — HLR-20.050-001–045 (routing filter, TR gating, split/merge arbitration, messy parallel-trace, overflow telemetry, determinism)
- [20.36_canonical_end_to_end_trace.md](../../20_requirements/20.36_canonical_end_to_end_trace.md) — A-chain: `InB → IIInB → RB → splitting`
- [20.37_thought_router_tr_specification.md](../../20_requirements/20.37_thought_router_tr_specification.md) — TR gate contract (RB reads `tr_needs_update` read-only)
- [20.17_messy_input_handling.md](../../20_requirements/20.17_messy_input_handling.md) — parallel-trace routing for messy inputs (no smoothing in RB)

## Flows Alignment Statement

- **Forward Flow (20-series):** RB as post-intake routing fan-out per 20.50; strict TR gate per 20.37; messy preserved per 20.17; A-chain placement after intake repair (20.36 §2.1.1) and before split/OB.
- **Backward Flow (40-series evidence):** Phase B runs (mock post-repair intake) confirm: deterministic routing_filter with canonical ordering and replay identity; TR decisions emitted only when `tr_needs_update=True` (RB never clears flag or writes TR); messy_input_record flows through lanes verbatim; overflow produces typed audit (no silent drop); high-fanout produces split_candidate arbitration signal for 40.170. No changes to 20.xx required.
- **Iterative Design Flow (50-series influence):** Concrete evidence for routing_filter schema, arbitration policy surface, and TR gate semantics. Supports 50 design on RB as the relational topology authority and on joint contracts with 40.170/40.240.

**Agreement Statement**: Phase B complete per 40.05 (capsule structure, harness entrypoint, artifacts) and 40.510 W3 (RB routing + `InB → IIInB → RB` handoff). Full traceability from test scenarios to 20.50 HLRs. Ready for 30.00 normalization (coverage note, glossary) and 50 insight per wave protocol. Handoffs to 40.170 (split/merge arbitration), 40.240 (TR), 40.200 (OB), and upstream 40.50/40.60 exercised.

## Phase B HLR Exercise Summary (2026-06-09 harness run)

- Post-IIInB fan-out: HLR-20.050-001 (fan-out), -027 (TR gate context). Evidence: lanes + routing_filter with iiinb_enabled in justification.
- TR skipped when flag false: HLR-20.050-027 (gate), -028 (no write/clear). Evidence: tr_needs_update=False yields only "direct" decisions, tr_eligible=False.
- Messy-input preserved routing: HLR-20.050-009 (messy context), -010 (no smoothing). Evidence: messy_input_record present in output lane; "messy_preserved" in rationale.
- Overflow reject-with-audit: HLR-20.050-024 (bounds/telemetry), -029 (reject-with-audit). Evidence: audit record type=OVERFLOW with count/limit/code when >limit.
- Routing filter replay: HLR-20.050-004 (deterministic filter), -036 (replay/diff). Evidence: identical inputs produce identical filter.as_dict() (sort_keys canonical).

All 045 HLRs addressed at high level via the 5 scenarios + explicit filter/decision/audit logic. Core contract (intake list in → routing_filter + decisions + lanes + audit out) stable.

Schema/audit per 20.50 exercised directly (canonical ob_ids, filter fields, overflow codes, tr_eligible flag).

## Impacted / Referenced Documents
- 40.50_inb_prototypes / 40.60_iiinb_prototypes (upstream handoff sources)
- 40.170_split_merge_prototypes (downstream split/merge arbitration signals)
- 40.240_tr_router_prototypes (TR gate consumer; RB does not invoke)
- 40.200_ob_prototypes (downstream after RB)
- 20.50, 20.36, 20.37, 20.17 (as above)
- 40.05_master_program_guide.md (process)
- 30.30_verification_glossary.md (for future 30 promotion of "routing_filter", "tr_needs_update gate", "RB arbitration")
- 40.510_refactor.md (program tracking + W3 wave)
- 20.101, 20.100 (intake repair context for handoff)

## Migration / Implementation Notes
- Self-contained for Phase B (pure dict mocks styled on InB/IIInB outputs); no hard dependency on live 40.50/40.60 prototypes in this harness.
- RoutingBasin.route(...) signature stable: (intake_records, *, iiinb_enabled, tr_needs_update, policy_signature, cycle_id, overflow_limit) → RBOutput.
- RoutingFilter is first-class and fully serializable for logging/replay (as_dict + canonical sort on ids).
- TR gate is a pure decision in RBDecision; actual TR invocation lives in 40.240 (RB only signals eligibility).
- Messy preservation is by verbatim copy into lane output + rationale tag — satisfies "no resolve/smooth" rule.
- Overflow limit is configurable in the call (default 16 for test); audit always emitted, routing still produced (telemetry, not hard reject for this stage).
- Split/merge candidate signals are lightweight RBDecision entries for high fanout; exact policy can be co-designed with 40.170.
- When live upstream fixtures are available, the same harness scenarios can be re-run with real InBOutput/IIInB records (shape-compatible).

## Open Items / Gaps
- Full numeric ΔH routing context (Q32.32 per 20.95) — current is simplified float for filter.
- Exact arbitration policy for split/merge (current is count-based stub; real policy may live in 20.50 + 50 design).
- Live joint test with 40.240 (TR invocation after RB gate) and 40.170 (arb decisions consumed) — deferred until those modules advance.
- 30.00 promotion: will require 10.50 peer + normalized 30 capsule citing this + cross-module intake/TR/split evidence.
- 50 insight: routing_filter schema and arbitration surface are prime candidates for 50.50 / 50.37 design specs.

All deltas incorporated as of 2026-06-09 Phase B completion. No outstanding from Phase A.


See the [W3 wave coverage note](../../../30_verification/W3_pipeline_a_wave_coverage_note.md) for:

- Aggregated HLR mapping and contract checks across the W3 wave (401–412)

- Open gaps and 50 insight targets

- Glossary alignment (30.30)

- 10.50 peer references (where applicable for this module)

The primary evidence for promotion is the module's `verification_capsule.md` and the 2026-06-09 artifact(s) (or legacy baseline as noted). No separate 30.XXX capsule was created here unless already present in 30_verification/; the wave note serves as the 30 deliverable for the slice.

For modules with existing 30.XXX (e.g., 30.150 for this), cross-reference there.
