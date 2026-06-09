# 40.190_rb_prototypes / verification_capsule.md

## Status
**Phase B complete** — harness PASS on 2026-06-09 (5/5 scenarios). W3 Phase B evidence recorded. Artifact: artifacts/rb_verification_run_2026-06-09.json

## Flows Alignment Statement

- **Forward Flow (20-series):** [20.50](../../20_requirements/20.50_rb_requirements.md) HLR-20.050-001–045; [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §2.1.1 `InB → IIInB → RB`; integrates with [20.37](../../20_requirements/20.37_thought_router_tr_specification.md) TR gating and [20.17](../../20_requirements/20.17_messy_input_handling.md) parallel-trace routing.
- **Backward Flow (40-series evidence):** Phase B runs confirm: post-intake (mock InB/IIInB) fan-out to lanes, routing_filter computation + canonical replay, strict `tr_needs_update` gating (no TR when false; RB does not clear flag), messy records preserved verbatim with no smoothing, overflow produces audit telemetry without silent drops, split/merge arbitration signals emitted for downstream (40.170).
- **Iterative Design Flow (50-series influence):** Evidence for routing filter shape, arbitration policy, and TR gate placement; supports 50 design on RB as relational topology authority.

**Agreement Statement**: Phase B complete per 40.05 and 40.510 W3. Full evidence package ready for 30/50. Handoffs to 40.170 (split/merge arb), 40.240 (TR), and upstream intake (40.50/40.60) exercised via contract. 40.170 approval noted separately.

## Run Record

| Date | Module | Command | Inputs / Config | Result | Exit Code | Artifacts | HLR Ref | LLR Ref | Req Doc | Req Section | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-06-09 | 40.190_rb_prototypes | python harness.py (direct scenario exec) | 5 scenarios per software_description matrix; mock post-repair intake dicts; iiinb/tr/messy/overflow toggles | PASS (report) | 0 | artifacts/rb_verification_run_2026-06-09.json | HLR-20.050-001,027,028,009,010,024,029,004,036 | (from 20.50) | thought_simulator/20_requirements/20.50_rb_requirements.md | §1-45 (focus routing filter, TR gate, messy, overflow, replay) | 5/5 PASS. Deterministic filter with canonical ids; TR gate strictly on flag; messy preserved; overflow audited; replay identical. |

## Positive Scenario Ledger

| Scenario | Result | HLR Ref | LLR Ref | IO Fields Exercised | Evidence |
|---|---|---|---|---|---|
| post_iiinb_fanout | PASS | HLR-20.050-001, 027 | (20.50) | iiinb_enabled, intake_records → lanes + routing_filter.selected_ob_ids + policy_justification | harness + artifact |
| messy_input_preserved_routing | PASS | HLR-20.050-009, 010 | (20.50) | messy_input_record in input → preserved in lane output + "messy_preserved" in rationale | harness + artifact |
| routing_filter_replay | PASS | HLR-20.050-004, 036 | (20.50) | identical inputs (incl. policy) → identical routing_filter.as_dict() (sort_keys) | harness run1 == run2 (json) |

## Negative-Path Coverage Ledger

| Scenario | Result | HLR Ref | LLR Ref | IO Fields Exercised | Evidence |
|---|---|---|---|---|---|
| tr_skipped_when_flag_false | PASS | HLR-20.050-027, 028 | (20.50) | tr_needs_update=False → no decision with action=="invoke_tr" or tr_eligible=True; RB does not mutate flag | harness + artifact |
| overflow_reject_with_audit | PASS | HLR-20.050-024, 029 | (20.50) | >limit records → audit record type=OVERFLOW with count/limit/code; partial routing still emitted | harness + artifact |

## Routing Filter Example (from replay scenario)

```json
{
  "selected_ob_ids": ["oA", "oB"],
  "lane_projections": [{"lane_id": "lane-0", "ob_id": "oA", ...}],
  "delta_h_routing_context": {"h_delta": 0.02},
  "firing_order": ["oA", "oB"],
  "transition_rationale": ["post_intake_fanout", "inb_direct"],
  "policy_justification": {"policy": "pol-replay", "iiinb_enabled": false, ...}
}
```

## Determinism / Replay Evidence

`routing_filter_replay` confirms identical `RoutingFilter.as_dict()` (and thus full output determinism) for repeated identical calls. All ids sorted, no RNG, pure function of explicit inputs + policy.

## Failure Record

- None in this run (all scenarios handled; 5/5 PASS per matrix).

## Requirements Delta Summary

- RB is the deterministic relational fan-out after intake repair (InB or IIInB when enabled).
- Routing filter is first-class, logged, canonical, and replay-diffable (selected_ob_ids, lane_projections, delta_h context, firing_order, rationale, policy).
- TR gate is a pure read of `tr_needs_update`; RB never writes TP.TR or clears the flag (strict 20.50-027/028).
- Messy input records flow through unchanged (parallel-trace per 20.17); no repair/smoothing occurs in RB.
- Overflow produces explicit audit telemetry (type, count, limit, code) — no silent branch loss.
- Split/merge arbitration signals (simple policy for high fanout) emitted for 40.170 downstream.
- All exercised HLRs (001/027 fan-out+TR, 027/028 gate, 009/010 messy, 024/029 overflow, 004/036 filter/replay) map directly; no 20.50 changes required.
- Integrates with W3 A-chain (post 40.50/60, pre 40.170/40.240/40.200).

## Architectural Evaluation

- Follows 40.05: pure macro (RoutingBasin), harness-only entry, artifacts/, capsule + delta.
- Determinism: routing_filter and decisions are fully determined by input list + flags + policy; identical calls produce identical JSON.
- Traceability: scenarios attach HLRs; ledgers + artifact bind evidence to 20.50.
- Clean boundaries: no repair (40.60), no TR write (20.37), no truth read (20.140), no semantic_core outside approved set.
- Ready for promotion to 30/50 per 40.510 W3 (joint with intake 40.50/60, TR 40.240, split/merge 40.170).

## Object Snapshots

- In-memory: RoutingFilter, RBDecision, RBOutput (serializable via as_dict()).
- No persistent store here; routing_filter is emitted for downstream logging/replay (40.300 etc.).

## Notes

- Phase B implemented and executed successfully (status PASS in artifact 5/5).
- Upstream mocks used (dicts styled after InB/IIInB outputs) because full live handoff integration with latest 40.50/40.60 will be exercised in joint runs later.
- When 40.240 TR prototype advances, a follow-up scenario exercising actual TR invocation contract (post-RB) can be added without changing the RB API.
- 40.170 split/merge arb signals are present for high-fanout cases; exact policy can be refined jointly.
- 40.170 Phase B approved (user declaration 2026-06-09); 40.180 Phase B evidence complete and under CP+user review.
