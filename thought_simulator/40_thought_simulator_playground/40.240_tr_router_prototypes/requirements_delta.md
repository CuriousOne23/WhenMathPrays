# Requirements Delta - 40.240 Thought Router (TR)

**Module ID:** 40.240  
**Version:** 0.4 (W3 Phase B)  
**Date:** 2026-06-09  
**Status:** W3 Phase B complete. Proxy regression + full 20.37 on-TP integration now evidence-backed.

## Purpose

Requirement-change and implementer-feedback record for `40.240_tr_router_prototypes` (W3 extension), per 40.05 format.

**W3 Phase B Summary:** Extended beyond proxy to on-TP semantics per 20.37 flow contract (OB TR-input + DCB events when tr_needs_update=true → atomic TP.TR + clear flag). Legacy proxy (2026-06-03) retained as regression baseline. 10/10 tests PASS in 2026-06-09 run.

## Verified Deltas — Proxy Regression (Baseline)

| Requirement | Status | Evidence Source | HLR / Canonical |
|-------------|--------|-----------------|-----------------|
| Deterministic routing | ✅ (regression) | proxy cases in 2026-06-09 run | HLR-20.437-001 |
| Content-based basin selection | ✅ (regression) | TC001–TC004 | HLR-20.437-001 |
| Fixed ΔH% per route class | ✅ (regression) | TC001–TC004 | HLR-20.437-002 |
| Explicit error path (no side-effects) | ✅ (regression) | TC005, TC006 | HLR-20.437-003 |
| Artifacts in `artifacts/` + determinism | ✅ | multi-run pattern + new 2026-06-09 artifact | 40.05 structure |

## W3 On-TP Integration Deltas (New for Phase B)

| Requirement (20.37 + 20.106) | Status | Evidence Source (2026-06-09) | Anchor |
|------------------------------|--------|------------------------------|--------|
| TR routine runs **iff** `tr_needs_update = true` | ✅ Implemented | W3-TC003-negative (flag=false → skipped) | HLR-20.037-049 |
| Consume OB TR-input + permitted DCB events | ✅ Implemented | W3-TC001 (happy with dcb), W3-TC002 (no dcb) | HLR-20.037-050, 20.106 |
| Atomic `TP.TR` write + clear `tr_needs_update` on success only | ✅ Implemented | W3-TC001 / W3-TC002 (flag cleared, TR written) | HLR-20.037-040, -051 |
| Reject DCB-direct consumption (must come via gate) | ✅ Implemented | W3-TC004-negative (no tr_input + dcb → rejected) | HLR-20.037-051, 20.106 |
| Preserve proxy as regression subset | ✅ | TC001–TC006 pass identically to 2026-06-03 baseline | 40.510-410 W3 scope |

## Structural / Process Requirements (40.05 + W3)

- `software_description.md` — W3 Phase A approved + W3 Phase B marked complete (this pass)
- `prototype.py` — extended with `process_tr_step` (on-TP) while preserving `route()` proxy
- `harness.py` — 10 tests (6 proxy regression + 4 W3 on-TP), new 2026-06-09 artifact
- `verification_capsule.md` — updated with W3 ledgers + three-flow for full 20.37 scope
- `requirements_delta.md` — this file (W3 deltas added)
- `artifacts/tr_verification_run_2026-06-09.json` — new W3 evidence (proxy + integration)

## Rationale

- W3 Phase B completes the on-TP contract that the Phase A software_description scoped for 40.510-410 (joint 40.200/40.210/40.190).
- Proxy regression guarantees no breakage for downstream consumers of the old basin-selection behavior.
- All new HLRs (20.037-049/050/051 + 20.106 DCB) now have direct harness evidence.

## Impacted Documents

- `software_description.md` (W3 Phase B status + evidence note)
- `prototype.py`, `harness.py`
- `verification_capsule.md`, `requirements_delta.md`
- `40.510_refactor.md` (row 410 + W3 log)
- `10.50.180`, `30.180` (can now promote full on-TP TR)
- `20.37` (evidence now backs the flow contract for this module)

## Open Items (Post W3)

- Full field-level `TP.TR` population details (deferred to 50-series if needed)
- Live joint runs with real 40.200 OB + 40.210 DCB outputs (mocks used for isolation)
- Any 30.180 updates once 40.240 W3 is approved

## Summary

W3 Phase B complete for 40.240: 10/10 tests, proxy regression + full on-TP 20.37 integration (gating, DCB consumption, atomic write + flag clear, DCB-direct reject). Legacy proxy preserved. Ready for reviewer sign-off and wave closure.