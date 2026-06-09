# Requirements Delta - 40.240 Thought Router (TR)

**Module ID:** 40.240  
**Version:** 0.3  
**Date:** 2026-06-05 (40.05 pass)  
**Status:** Evidence-backed proxy deltas. Integration HLRs anchored, not harness-proven.

## Purpose

Requirement-change and implementer-feedback record for `40.240_tr_router_prototypes`, per `40.160_tp_lifecycle` / `40.05_master_program_guide.md` format.

**Alignment Summary (2026-06-05):** Synchronized with `20.37` Semantic Interpretation Flow Contract. Harness proves `HLR-20.437-*` only. `HLR-20.037-049/050/051` deferred to Phase C.

## Verified Deltas (Evidence-Based — Proxy Only)

| Requirement | Status | Evidence Source | HLR / Canonical |
|-------------|--------|-----------------|-----------------|
| Deterministic routing | ✅ Implemented | prototype + harness run1/2/3 | HLR-20.437-001 |
| Content-based basin selection | ✅ Implemented | TC001–TC004 | HLR-20.437-001 |
| Fixed ΔH% per route class | ✅ Implemented | TC001–TC004 outputs | HLR-20.437-002 |
| No randomness in routing | ✅ Implemented | code review + 3 runs | HLR-20.437-001 |
| Explicit error path | ✅ Implemented | TC005, TC006 | HLR-20.437-003 |
| Artifacts in `artifacts/` | ✅ Implemented | harness.py | 40.05 structure |
| Multi-run determinism | ✅ Implemented | run1/2/3 match | 40.05 evidence |
| Proxy scope metadata in JSON | ✅ Implemented | harness `evidence_scope`, `hlr_proven` | 2026-06-05 |

## Anchored Not Proven (20.37 Integration — Phase C)

| Topic | Status | 20.37 anchor |
|-------|--------|--------------|
| Semantic Interpretation Flow Contract | 📋 Anchored | Contract section; HLR-20.037-049 |
| OB TR-input + `tr_needs_update` | 📋 Anchored | §4, §7; HLR-038, -050 |
| TR exclusive `TP.TR` write + clear | 📋 Anchored | §3, §7; HLR-002, -040 |
| RB iff gate + `TP.TR` consumption | 📋 Anchored | §5, §7; HLR-039, -051 |
| DCB ephemeral hints | 📋 Anchored | §4.4; 20.106 |

## Structural / Process Requirements (40.05 Alignment)

- `software_description.md` — Phase A/B/C, Alignment Summary, 20.37 contract table (2026-06-05)
- `verification_capsule.md` — ledgers, integration-open table, 40.05 checklist
- `requirements_delta.md` — this file
- `artifacts/tr_verification_run{1,2,3}_2026-06-03.json` — regenerated 2026-06-05 (6/6 pass)
- `docs/` — experiments, prototype_notes, reasoning_trail

## Rationale

- 40.240 remains a **basin-selection + ΔH% proxy**, not the full TR routine in 20.37.
- 40.05 pass adds TC005/TC006 so error-path claims are artifact-backed.
- Integration contract is documented for promotion traceability without inflating evidence.

## Impacted Documents

- `software_description.md`
- `prototype.py`, `harness.py`
- `verification_capsule.md`
- `10.50.180_tr_requirements.md` (proxy + FLOW sections)
- `30.180` (refresh if promoted with 6-test artifacts)

## Open Validation / Phase C

- Full `TP.TR` field population (20.37 §6)
- `tr_needs_update` lifecycle with RB, OB, Merge, IB (20.31 §10)
- MTP read-only consumption
- DCB post-OB / pre-TR (20.106)
- Conformance evidence for HLR-20.037-049/050/051

Reserved for Phase C per `software_description.md`.

## Summary

40.05 pass complete for **Phase B proxy**: 6/6 tests, 3-run determinism, proxy-only JSON metadata, capsule/delta aligned with updated 20.37. Integration verification remains open.