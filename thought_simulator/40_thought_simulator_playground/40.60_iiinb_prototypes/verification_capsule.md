# Verification Capsule

## Status
Phase A **approved** (CP review, 2026-06-08). Phase B **approved** (19/19 PASS; CP review, 2026-06-08; 40.510-101).

## Evidence Summary
- Artifact: `artifacts/iiinb_verification_run_2026-06-08.json`
- Evidence types (40.160): behavioral, structural (intake ordering, basin-chain exclusion), negative (escalate, caps, rejected handoff, USP load failure), replay, golden diff (diagnostic export)
- Core invariants demonstrated:
  - `profile_enabled` gate with zero semantic effect on skip
  - Read-only USP apply; snapshot immutability; version ref pinning
  - Escalate-without-guess; non-blocking CIL escalation handoff
  - `InB → IIInB → RB` intake path ordering; not in RB→OB→TR→TB chain
  - Apply cap (16) and segment cap (32) with truncate-with-audit
  - Envelope guard: `semantic_core`, `TP.TR`, `exec_plan`, `exec_trace` unchanged
  - Multi-rule precedence (ACTIVE rules only)
  - Deterministic replay and segmentation
  - TCU cost reporting per repair pass
  - One `iiinb_repair_record` per pass (`audit_records`)
  - Deterministic diagnostic export ordering (MB-consumable)
  - Fixed `REASON_CODES` registry with assert on emission

## HLR Coverage (exploratory harness mapping)
| HLR | Scenario(s) |
|-----|-------------|
| 001, 002 | `profile_disabled_skip` |
| 003 | `positive_inb_iiinb_rb_order`, `negative_rejected_inb_handoff` |
| 004 | `positive_not_in_rb_ob_chain` |
| 005, 022 | `positive_usp_rule_apply`, `negative_usp_load_failure` |
| 006 | `positive_usp_version_ref_pinned` |
| 007 | `positive_multi_rule_precedence` |
| 008 | `positive_usp_snapshot_immutable` |
| 009, 012 | `negative_escalate_no_guess` |
| 010 | `positive_segmentation_deterministic`, `negative_segment_cap` |
| 011, 014, 015 | `positive_usp_rule_apply` |
| 016 | `positive_audit_record_per_pass` |
| 017, 018 | `positive_cil_escalation_nonblocking`, `negative_escalate_no_guess` |
| 019 | `negative_apply_cap`, `negative_segment_cap` |
| 020 | `positive_tcu_cost_reported` |
| 021 | `positive_deterministic_replay` |
| 024 | `positive_pipeline_b_envelope_unchanged` |
| 026–028 | full harness fixture matrix, `positive_diagnostic_export_ordering` |

**Open:** HLR-013 (MI_VAGUE/MI_INCOMP), HLR-023 (IMR same-cycle), HLR-025 (parent cross-check), HLR-024b (`FAIL_ENVELOPE` negatives, 40.510-207) — see `requirements_delta.md` Open / partial table.

## Scenarios Executed
| Scenario | Result |
|----------|--------|
| `profile_disabled_skip` | PASS |
| `positive_usp_rule_apply` | PASS |
| `negative_escalate_no_guess` | PASS |
| `positive_deterministic_replay` | PASS |
| `positive_inb_iiinb_rb_order` | PASS |
| `negative_apply_cap` | PASS |
| `positive_not_in_rb_ob_chain` | PASS |
| `positive_multi_rule_precedence` | PASS |
| `negative_rejected_inb_handoff` | PASS |
| `negative_usp_load_failure` | PASS |
| `positive_cil_escalation_nonblocking` | PASS |
| `positive_tcu_cost_reported` | PASS |
| `negative_segment_cap` | PASS |
| `positive_usp_version_ref_pinned` | PASS |
| `positive_pipeline_b_envelope_unchanged` | PASS |
| `positive_audit_record_per_pass` | PASS |
| `positive_diagnostic_export_ordering` | PASS |
| `positive_usp_snapshot_immutable` | PASS |
| `positive_segmentation_deterministic` | PASS |

## Flows Alignment Statement

- **Forward Flow (20-series)**: Driven by [20.101](../../20_requirements/20.101_iiinb_requirements.md), [20.102](../../20_requirements/20.102_usp_requirements.md), [20.105](../../20_requirements/20.105_tp_requirements.md) §3.4, [20.38](../../20_requirements/20.38_ts_implementation_guidelines.md) §6, and upstream [40.50](../40.50_inb_prototypes/software_description.md) handoff.
- **Backward Flow (40-series evidence)**: Harness 19/19 PASS (`artifacts/iiinb_verification_run_2026-06-08.json`) — behavioral, structural, negative, replay, and golden-diff evidence for 25/28 HLRs with named residuals.
- **Iterative Design Flow (50-series influence)**: None yet; full CIL FIFO wire deferred to Wave 2 per [40.510](../40.510_refactor.md).

**Agreement Statement**: Aligned — Phase B scope closed per test matrix. Extend only via 30-series promotion, 40.510-207 `FAIL_ENVELOPE` negatives, or integrated intake-path runs with 40.70; do not add surface canonicalization to IIInB.

## Next (30-series promotion path)
- Normalize capsule per [30.00](../../30_verification/30.00_verification_user_guide.md) — GATE-A closed 2026-06-08; W1 step 2 (30 normalize) next per [40.510](../40.510_refactor.md) §4.2.2.
- Close HLR-013, 023, 025 residuals; `FAIL_ENVELOPE` via 40.510-207.
- Integrated `InB → IIInB` strip replay with 40.70 Class 7 fixtures when scheduled.