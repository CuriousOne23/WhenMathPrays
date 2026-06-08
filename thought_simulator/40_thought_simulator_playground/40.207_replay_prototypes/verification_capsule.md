# Verification Capsule

## Status
Phase A **complete and promotion-ready** (2026-06-08). Initial Phase B: C7 **5/5 PASS** + `strip_replay_invariant` PASS (GATE-A approval pending — 40.510-102).

## Evidence Summary
- Artifact: `artifacts/replay_class7_verification_run_2026-06-08.json`
- Command: `python harness.py` (from module directory)
- Evidence types (40.20): behavioral, structural (fixture/assertion shape), replay, golden diff (strip digest)

## Class 7 Results
| Sub-ID | Fixture | Result |
|--------|---------|--------|
| C7-A | `REPLAY_C7_PROFILE_DISABLED` | PASS |
| C7-B | `REPLAY_C7_USP_RULE_APPLY` | PASS |
| C7-C | `REPLAY_C7_ESCALATE_NO_GUESS` | PASS |
| C7-D | `REPLAY_C7_CLARIFY_COMMIT_CROSS_TURN` | PASS |
| C7-E | `REPLAY_C7_GB_VETO_COMMIT` | PASS |

Additional: `strip_replay_invariant` PASS

## HLR Coverage (initial pass)
| HLR | Scenario(s) |
|-----|-------------|
| 20.36-058 | C7-B, C7-C |
| 20.36-059 | C7-A |
| 20.36-060 | C7-B, C7-C |
| 20.36-061 | C7-D (simulated) |
| 20.36-062 | C7-E (simulated) |
| 20.207-001, 019 | `strip_replay_invariant` |

**Open:** Classes 1–6, E2 regen, 20.207-028..030 negatives, live UPI/GB — see `requirements_delta.md` Open / partial table.

## Phase A Evidence Checklist
| Check | Status |
|-------|--------|
| `software_description.md` (Phase A deliverables) | ☑ |
| 20.207 HLRs + 20.36 Class 7 HLRs visible in description | ☑ |
| Flows alignment + agreement statements | ☑ |
| C7-A..E fixture contracts documented | ☑ |
| Upstream 40.100/40.101 referenced | ☑ |
| Initial harness artifact on disk (C7 5/5) | ☑ |
| `requirements_delta.md` current | ☑ |

## Flows Alignment Statement

- **Forward Flow (20-series)**: [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §9 Class 7; [20.207](../../20_requirements/20.207_execution_replay_specification.md) E1 strip; upstream [40.100](../40.100_inb_prototypes/software_description.md), [40.101](../40.101_iiinb_prototypes/software_description.md).
- **Backward Flow (40-series evidence)**: C7 5/5 + strip demo PASS (`artifacts/replay_class7_verification_run_2026-06-08.json`).
- **Iterative Design Flow (50-series influence)**: None yet; W5 orchestration per [40.510](../40.510_refactor.md).

**Agreement Statement**: Provisionally aligned — Phase A software description complete; initial Class 7 evidence supports GATE-A replay scope. Formal approval requires Phase B expansion and reviewer sign-off on 40.510-102.

## Phase B Obligations (next)
- Expand test matrix (Classes 1–6 stubs or W5 schedule)
- Strengthen C7-D/E when Wave 2 UPI/GB modules exist
- Add `b_regeneration_equivalent` scaffold
- CP review → mark Phase B approved in 40.510-102