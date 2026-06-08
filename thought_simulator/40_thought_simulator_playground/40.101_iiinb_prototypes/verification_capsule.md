# Verification Capsule

## Status
Phase A **approved** (CP review, 2026-06-08). Phase B v0.1 harness **6/6 PASS** (formal Phase B approval pending — 40.510-101, GATE-A).

## Evidence Summary
- Artifact: `artifacts/iiinb_verification_run_2026-06-08.json`
- Evidence types (40.20): behavioral, structural (intake path ordering), negative (escalate, apply cap), replay
- Core invariants demonstrated (initial pass):
  - `profile_enabled=false` skip with zero semantic effect (no USP load)
  - Read-only USP rule apply on intake-bound TP fields
  - Escalate-without-guess for uncovered shorthand segments
  - `InB → IIInB → RB` intake path ordering via `run_intake_path`
  - Apply cap enforcement (≤16 rule applications)
  - Envelope guard: `semantic_core` and `TP.TR` unchanged after repair
  - Deterministic replay (identical digest across runs)

## HLR Coverage (exploratory harness mapping — initial pass)
| HLR | Scenario(s) |
|-----|-------------|
| 001, 002 | `profile_disabled_skip` |
| 003 | `positive_inb_iiinb_rb_order` |
| 005–008, 011, 014, 015 | `positive_usp_rule_apply` |
| 009, 012, 017 | `negative_escalate_no_guess` |
| 019 | `negative_apply_cap` |
| 021 | `positive_deterministic_replay` |

**Open (Phase B expansion):** 004, 006, 010, 013, 016, 018, 020, 022–028; `FAIL_ENVELOPE` negatives deferred per `software_description.md` Risks & Unknowns (40.510-207).

## Scenarios Executed
| Scenario | Result |
|----------|--------|
| `profile_disabled_skip` | PASS |
| `positive_usp_rule_apply` | PASS |
| `negative_escalate_no_guess` | PASS |
| `positive_deterministic_replay` | PASS |
| `positive_inb_iiinb_rb_order` | PASS |
| `negative_apply_cap` | PASS |

## Flows Alignment Statement

- **Forward Flow (20-series)**: Driven by [20.101](../../20_requirements/20.101_iiinb_requirements.md) (profile gate, USP consumption, repair semantics, intake-bound TP writes, escalation, bounds, determinism), [20.102](../../20_requirements/20.102_usp_requirements.md) (read-only snapshot), [20.105](../../20_requirements/20.105_tp_requirements.md) §3.4, [20.38](../../20_requirements/20.38_ts_implementation_guidelines.md) §6, and upstream [20.100](../../20_requirements/20.100_inb_requirements.md) / [40.100](../40.100_inb_prototypes/software_description.md) handoff (`inb_to_iiinb_v1`).
- **Backward Flow (40-series evidence)**: Initial harness 6/6 PASS (`artifacts/iiinb_verification_run_2026-06-08.json`) — behavioral, structural, negative, and replay evidence for core Track H repair path. Remaining HLRs tracked in `software_description.md` Test Matrix.
- **Iterative Design Flow (50-series influence)**: None yet; CIL/UPI cross-turn wiring deferred to Wave 2 per [40.510](../40.510_refactor.md).

**Agreement Statement**: Provisionally aligned — Phase A approved (CP, 2026-06-08); Phase B v0.1 evidence supports core `input_semantic_repair` invariants. Formal GATE-A closure requires expanded test matrix and reviewer ☑ on 40.510-101.

## Phase A Evidence Checklist
| Check | Status |
|-------|--------|
| `software_description.md` (Phase A deliverables) | ☑ |
| All 28 × 20.101 HLRs visible in description | ☑ |
| Flows alignment + agreement statements | ☑ |
| InB handoff contract (`inb_to_iiinb_v1`) documented | ☑ |
| `requirements_delta.md` current | ☑ |
| Initial harness artifact on disk (6/6 PASS) | ☑ |

## Phase B Obligations (next)
- Expand scenario matrix per Test Matrix in `software_description.md`
- Add `FAIL_ENVELOPE` envelope-guard negatives (40.510-207)
- Cross-validate with 40.100 handoff artifact; integrated intake-path replay with 40.207 when scheduled
- CP review → mark Phase B approved in 40.510-101

## Next (30-series promotion path)
- Normalize capsule per [30.00](../../30_verification/30.00_verification_user_guide.md) after Phase B formal approval.
- Close open HLR gaps via expanded harness or defer explicitly to 30-series coverage audit.