# Verification Capsule — 40.80 USP

## Status
Phase B **approved** (8/8 PASS; CP review, 2026-06-08; 40.510-201 **GATE-B**)

## Evidence
- Artifact: `artifacts/usp_verification_run_2026-06-08.json`

## Scenarios
| Scenario | Result |
|----------|--------|
| `positive_empty_profile_snapshot` | PASS |
| `positive_single_rule_commit` | PASS |
| `positive_supersede_chain` | PASS |
| `positive_revoke_rule` | PASS |
| `positive_iiinb_readonly_load` | PASS |
| `negative_cap_overflow` | PASS |
| `negative_gb_veto_no_active` | PASS |
| `positive_replay_identical_ref` | PASS |

## HLR coverage (20.102)
| HLR family | Scenario(s) |
|------------|-------------|
| 006–008 | `positive_iiinb_readonly_load`, `positive_empty_profile_snapshot` |
| 009–012, 018 | `positive_single_rule_commit`, `positive_supersede_chain`, `positive_replay_identical_ref` |
| 013–015 | `positive_supersede_chain`, `positive_revoke_rule` |
| 014 | `negative_gb_veto_no_active` |
| 016 | `negative_cap_overflow` |
| 024 | full matrix |