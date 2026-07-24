# Requirements Delta

## Scaffold Status
- scaffold_status: implemented (Phase B complete, 2026-06-08)
- Phase A: **approved** (CP review, 2026-06-08)
- Phase B: **approved** (19/19 PASS; CP review, 2026-06-08; 40.510-101)

## Anchors
- 20-anchor: thought_simulator/20_requirements/20.101_iiinb_requirements.md (full 28 HLRs in software_description.md)
- 10.10-anchors: 10.10.10, 10.10.20, 10.10.50 (intake-bound writes, read-only USP, envelope isolation)
- upstream: 40.50_inb_prototypes (InB handoff `inb_to_iiinb_v1`)

## Exploratory Note
The complete set of HLR-20.101-001 through HLR-20.101-028 is made visible in `software_description.md` for playground exploration. 20.xx remains authoritative; 30.xx is the coverage audit layer. 40.60 is non-canonical.

## Part B Evidence (Executed — 2026-06-08)
- Harness run: 2026-06-08 (Phase B complete)
- Artifact: `artifacts/iiinb_verification_run_2026-06-08.json`
- Status: PASS (19/19 scenarios)
- Evidence types: behavioral, structural, negative, replay, golden diff
- Coverage note: 19 scenarios exercise **25/28 HLRs** — several HLRs are covered by multiple scenarios (e.g. 003, 009, 014–015), while 013, 023, 025, and 024b remain deferred.

### Implemented / demonstrated
| HLR | Implementation | Scenario |
|-----|----------------|----------|
| 001 | `repair_pass` skip when `profile_enabled=false` | `profile_disabled_skip` |
| 002 | No USP load on profile-disabled path | `profile_disabled_skip` |
| 003 | `run_intake_path` ordering; rejected InB guard | `positive_inb_iiinb_rb_order`, `negative_rejected_inb_handoff` |
| 004 | `INTAKE_PATH_STAGES` vs `BASIN_CHAIN_STAGES` | `positive_not_in_rb_ob_chain` |
| 005 | Read-only `UspSnapshot`; load failure path | `positive_usp_rule_apply`, `negative_usp_load_failure` |
| 006 | `usp_version_ref` on record and output | `positive_usp_version_ref_pinned` |
| 007 | `_active_rules` precedence + INACTIVE skip | `positive_multi_rule_precedence` |
| 008 | Snapshot `to_dict()` unchanged after pass | `positive_usp_snapshot_immutable` |
| 009 | Bounded pattern→expansion only | `positive_usp_rule_apply`, `negative_escalate_no_guess` |
| 010 | `_segment_intake` deterministic whitespace | `positive_segmentation_deterministic`, `negative_segment_cap` |
| 011 | `repair_outcome=APPLIED` + `rule_id` | `positive_usp_rule_apply` |
| 012 | `repair_outcome=ESCALATED` when no rule | `negative_escalate_no_guess` |
| 014 | Writes confined to `tp_intake_fields` | all repair scenarios |
| 015 | `envelope_guard` semantic_core/tp_tr | all repair scenarios |
| 016 | `audit_records` per pass | `positive_audit_record_per_pass` |
| 017 | Escalation refs with reason code | `negative_escalate_no_guess`, `positive_cil_escalation_nonblocking` |
| 018 | Non-blocking handoff to routing | `positive_cil_escalation_nonblocking` |
| 019 | `MAX_RULE_APPLICATIONS` / `MAX_SEGMENTS` | `negative_apply_cap`, `negative_segment_cap` |
| 020 | `tcu_cost` on record | `positive_tcu_cost_reported` |
| 021 | `_canonical_digest` replay contract | `positive_deterministic_replay` |
| 022 | `REASON_CODES` frozenset + `_assert_reason_code` | profile skip, USP failure, caps, escalate |
| 024a | `exec_plan`/`exec_trace` guard (positive) | `positive_pipeline_b_envelope_unchanged` |
| 026 | Full harness fixture matrix | all 19 scenarios |
| 027, 028 | `export_repair_diagnostics()` | `positive_diagnostic_export_ordering` |

HLR-013, 023, and 025 are intentionally excluded here and tracked in the Open / partial table below.

### Open / partial
| HLR | Gap | Notes |
|-----|-----|-------|
| 013 | MI_VAGUE/MI_INCOMP non-resolution | Policy documented; no dedicated messy-input fixture |
| 023 | IMR same-cycle isolation | Not modeled in playground |
| 025 | Parent 20.10/20.30 cross-check | Deferred to 30-series coverage audit |
| 024b | `FAIL_ENVELOPE` negative replay verdicts | Deferred to 40.510-207 (024a positive guard in Implemented table) |

## Phase 1 delta (40.510-101)
- Created IIInB module: `profile_enabled` gate, read-only USP apply, intake-bound TP writes, `run_intake_path` ordering
- Phase A approved (CP, 2026-06-08)

## Phase B delta (40.05)
- Added `export_repair_diagnostics`, extended envelope guard (`exec_plan`, `exec_trace`), `REASON_CODES` assert
- Added `INB_HANDOFF_REJECTED`; `BASIN_CHAIN_STAGES` / `INTAKE_PATH_STAGES` constants
- Expanded harness from 6 → 19 scenarios; full test matrix PASS

## Flows Alignment Statement

- **Forward Flow (20-series)**: [20.101](../../20_requirements/20.101_iiinb_requirements.md) drives all implemented obligations; [20.100](../../20_requirements/20.100_inb_requirements.md) / [40.50](../40.50_inb_prototypes/software_description.md) inform upstream handoff.
- **Backward Flow (40-series evidence)**: 19/19 PASS artifact proves Track H repair-path skeleton; residuals named above.
- **Iterative Design Flow (50-series influence)**: None yet; Wave 2 conversation layer deferred per [40.510](../40.510_refactor.md).

**Agreement Statement**: Aligned for Phase B closure. Promotion to 30-series requires closing HLR-013, 023, 025 gaps and 40.510-207 `FAIL_ENVELOPE` negatives.

## Open gaps (Phase 2+)
- Full CIL FIFO wire (40.120 redo)
- TCU reporting fidelity vs 20.150 authoritative budgets
- `FAIL_ENVELOPE` replay verdict fixtures (40.510-207)