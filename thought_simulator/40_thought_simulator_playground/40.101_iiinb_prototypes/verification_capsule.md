# 40.101 Verification Capsule

**Run date:** 2026-06-08  
**Command:** `python harness.py`  
**Exit code:** 0  
**Status:** PASS (6/6)

## Artifact

`artifacts/iiinb_verification_run_2026-06-08.json`

## Scenarios

| Scenario | HLR focus | Result |
|----------|-----------|--------|
| profile_disabled_skip | 20.101-001, 002 | PASS |
| positive_usp_rule_apply | 20.101-011, 015 | PASS |
| negative_escalate_no_guess | 20.101-012, 017 | PASS |
| positive_deterministic_replay | 20.101-021 | PASS |
| positive_inb_iiinb_rb_order | 20.101-003 | PASS |
| negative_apply_cap | 20.101-019 | PASS |

## Flows Alignment Statement

Identical to `software_description.md` — Phase B evidence recorded.

**Agreement Statement:** Aligned for Phase 1 GATE-A scope; envelope write-guard negative tests (40.510-207) may extend this module in Phase 2.