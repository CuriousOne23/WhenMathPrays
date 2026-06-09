# Verification Capsule

## Status
Phase A **approved** (CP review, 2026-06-08). Phase B **approved** (18/18 PASS; CP review, 2026-06-08; 40.510-102).

## Evidence Summary
- Artifact: `artifacts/replay_class7_verification_run_2026-06-08.json`
- Command: `py -3 harness.py` (from module directory)
- Evidence types (40.160): behavioral, structural (fixture IDs, intake path, B envelope guards), negative (regen input / forbidden lane_id), replay, golden diff (strip + diagnostic export digests)
- Core invariants demonstrated:
  - REPLAY_CLASS_7 C7-A..E (live 40.50/40.60 + simulated UPI/GB for C7-D/E)
  - E1 strip scope `[exec_plan, exec_trace]`; `semantic_core` retained
  - Class 7 suite deterministic replay (identical assertion maps)
  - C7-B intake path ordering (`inb_surface_norm` → `input_semantic_repair` → `routing`)
  - Class 1 strip demo — `semantic_core` stable across strip
  - Regen input validation (`FAIL_REGEN_INPUT`, `FAIL_REGEN_FORBIDDEN_READ`)
  - Fixture-root merge for omitted regen fields
  - `b_regeneration_equivalent` scaffold (`SCAFFOLD_DEFERRED`; E2 execution W5)
  - B envelope `lane_id`/`tp_id` guard
  - Deterministic replay diagnostic export ordering

## HLR Coverage (exploratory harness mapping)
| HLR | Scenario(s) |
|-----|-------------|
| 20.36-017 | `positive_class7_fixture_ids` |
| 20.36-018 | `positive_strip_digest_deterministic`, `positive_replay_diagnostic_export` |
| 20.36-021 | `positive_class1_strip_semantic_core_stable` |
| 20.36-053 | `positive_b_envelope_no_lane_tp`, `negative_regen_forbidden_lane_tp` |
| 20.36-058 | C7-B, C7-C, `positive_class7_suite_deterministic`, `positive_c7_b_intake_path_order` |
| 20.36-059 | C7-A |
| 20.36-060 | C7-B, C7-C, `positive_strip_semantic_core_retained` |
| 20.36-061 | C7-D (simulated UPI/GB) |
| 20.36-062 | C7-E (simulated UPI/GB/CIL) |
| 20.207-001 | strip scenarios, `positive_class1_strip_semantic_core_stable` |
| 20.207-004 | `negative_regen_input_incomplete`, `positive_regen_merge_from_fixture_root`, scaffold merge |
| 20.207-007 | `negative_regen_forbidden_lane_tp`, `positive_b_envelope_no_lane_tp` |
| 20.207-017, 020 | `scaffold_b_regeneration_equivalent` |
| 20.207-019 | `positive_strip_replay_invariant`, strip suite |
| 20.207-028 | `negative_regen_input_incomplete` |
| 20.207-029 | `negative_regen_forbidden_lane_tp` |
| 20.101-003 | `positive_c7_b_intake_path_order` |

**Coverage note:** 18 scenarios map to **17 distinct HLR anchors** — the scenario count exceeds the anchor count because one HLR is often exercised by multiple scenarios. Residuals: Classes 2–6 full runners, live E2 regen, `REGEN_STALE_EPOCH`, live UPI/GB wire, YAML golden import — see [`requirements_delta.md`](requirements_delta.md) Open / partial table.

## Scenarios Executed
| Scenario | Result |
|----------|--------|
| `replay_c7_a_profile_disabled` | PASS |
| `replay_c7_b_usp_rule_apply` | PASS |
| `replay_c7_c_escalate_no_guess` | PASS |
| `replay_c7_d_cross_turn_usp` | PASS |
| `replay_c7_e_gb_veto` | PASS |
| `positive_strip_replay_invariant` | PASS |
| `positive_strip_semantic_core_retained` | PASS |
| `positive_strip_digest_deterministic` | PASS |
| `positive_class7_suite_deterministic` | PASS |
| `positive_c7_b_intake_path_order` | PASS |
| `positive_class1_strip_semantic_core_stable` | PASS |
| `negative_regen_input_incomplete` | PASS |
| `negative_regen_forbidden_lane_tp` | PASS |
| `scaffold_b_regeneration_equivalent` | PASS |
| `positive_regen_merge_from_fixture_root` | PASS |
| `positive_b_envelope_no_lane_tp` | PASS |
| `positive_class7_fixture_ids` | PASS |
| `positive_replay_diagnostic_export` | PASS |

## Phase A Evidence Checklist
| Check | Status |
|-------|--------|
| `software_description.md` (Phase A deliverables) | ☑ |
| 20.207 HLRs + 20.36 Class 7 HLRs visible in description | ☑ |
| Flows alignment + agreement statements | ☑ |
| C7-A..E fixture contracts documented | ☑ |
| Upstream 40.50/40.60 referenced | ☑ |
| Phase B harness artifact on disk (18/18) | ☑ |
| `requirements_delta.md` current | ☑ |

## Flows Alignment Statement

- **Forward Flow (20-series)**: [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §9 Class 7; [20.207](../../20_requirements/20.207_execution_replay_specification.md) E1 strip + regen input scaffold; upstream [40.50](../40.50_inb_prototypes/software_description.md), [40.60](../40.60_iiinb_prototypes/software_description.md).
- **Backward Flow (40-series evidence)**: Harness 18/18 PASS (`artifacts/replay_class7_verification_run_2026-06-08.json`) — behavioral, structural, negative, replay, and golden-diff evidence for GATE-A REPLAY_CLASS_7 scope with named W5/W2 residuals.
- **Iterative Design Flow (50-series influence)**: None yet; W5 orchestration and live E2 per [40.510](../40.510_refactor.md).

**Agreement Statement**: Aligned — Phase B approved (CP review, 2026-06-08). Scope closed per test matrix. Extend only via 30-series promotion, W5 Classes 1–6 runners, live E2 `b_regeneration_equivalent`, or Wave 2 UPI/GB wire for C7-D/E; do not claim dual-pipeline PoC closure from Class 7 alone.

## Next (30-series promotion path)
- Normalize capsule per [30.00](../../30_verification/30.00_verification_user_guide.md) — GATE-A closed 2026-06-08; W1 step 2 (30 normalize) next per [40.510](../40.510_refactor.md) §4.2.2.
- Close Classes 2–6, live E2, `REGEN_STALE_EPOCH`, and YAML import residuals via W5 rows 505–506.
- Wire live UPI/GB for C7-D/E when 40.90/40.130 prototypes exist (Wave 2).