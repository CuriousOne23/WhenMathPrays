# Verification Capsule — 40.103 UPI

## Status
Phase B **approved** (8/8 PASS; CP review, 2026-06-08; 40.510-202 **GATE-B**)

## Evidence
- Artifact: `artifacts/upi_verification_run_2026-06-08.json`

## Scenarios
| Scenario | Result |
|----------|--------|
| `positive_single_commit` | PASS |
| `positive_fifo_two_events` | PASS |
| `positive_gb_approve` | PASS |
| `positive_gb_veto` | PASS |
| `negative_incomplete_event` | PASS |
| `negative_usp_cap_overflow` | PASS |
| `negative_pending_commit_cap` | PASS |
| `positive_replay_identical_ref` | PASS |

## HLR coverage (20.103)
| HLR family | Scenario(s) |
|------------|-------------|
| 005–008 | `positive_single_commit`, `positive_fifo_two_events`, `negative_incomplete_event` |
| 009–011 | `positive_gb_approve`, `positive_gb_veto` |
| 012–014 | `positive_fifo_two_events`, `positive_replay_identical_ref` |
| 015–016 | `negative_usp_cap_overflow`, `negative_pending_commit_cap` |
| 022 | audit on all paths |