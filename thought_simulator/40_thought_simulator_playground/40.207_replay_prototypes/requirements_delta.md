# Requirements Delta

## Scaffold Status
- scaffold_status: implemented (Phase B complete, 2026-06-08)
- Phase A: **approved** (CP review, 2026-06-08)
- Phase B: **approved** (18/18 PASS, 2026-06-08; 40.510-102 GATE-A reviewer ☑ pending)

## Anchors
- 20-anchor: thought_simulator/20_requirements/20.36_canonical_end_to_end_trace.md §9 (REPLAY_CLASS_7)
- 20-secondary: thought_simulator/20_requirements/20.207_execution_replay_specification.md (E1/E2/E3)
- upstream: 40.100_inb_prototypes, 40.101_iiinb_prototypes

## Exploratory Note
The full 20.207 HLR set (001–030) and 20.36 Class 7 HLRs (058–064) are visible in `software_description.md`. 20.xx is authoritative; 30.xx is the coverage audit layer. 40.207 is non-canonical.

## Part A Documentation (Phase A deliverables)
- `software_description.md`: purpose, W1/W5 roles, Class 7 fixture contracts, strip/E2 skeletons, digest, verdict taxonomy, full 20.207 HLR visibility, test matrix
- `verification_capsule.md`: Phase A checklist + Phase B evidence
- `prototype.py` / `harness.py`: C7-A..E runners + expanded Phase B matrix

## Part B Evidence (Executed — 2026-06-08)
- Harness run: 2026-06-08 (Phase B complete)
- Artifact: `artifacts/replay_class7_verification_run_2026-06-08.json`
- Status: PASS (18/18 scenarios)
- Evidence types: behavioral, structural, negative, replay, golden diff
- Coverage note: 18 scenarios exercise **17 distinct HLR anchors** — several HLRs are covered by multiple scenarios; Classes 2–6, live E2, and YAML import remain deferred.

### Implemented / demonstrated
| HLR | Implementation | Scenario |
|-----|----------------|----------|
| 20.36-017 | `CLASS_7_FIXTURE_IDS` 1:1 mapping | `positive_class7_fixture_ids` |
| 20.36-018 | `canonical_json_digest`; `export_replay_diagnostics` | `positive_strip_digest_deterministic`, `positive_replay_diagnostic_export` |
| 20.36-021 | Class 1 strip `semantic_core` stability demo | `positive_class1_strip_semantic_core_stable` |
| 20.36-053 | `assert_no_forbidden_lane_tp_fields` | `positive_b_envelope_no_lane_tp` |
| 20.36-058 | Replay equivalence C7-B/C; suite determinism | C7-B, C7-C, `positive_class7_suite_deterministic` |
| 20.36-059 | Zero Track H stages when profile disabled | `run_c7_a` |
| 20.36-060 | `envelope_guard` on repair paths; strip retains core | C7-B, C7-C, `positive_strip_semantic_core_retained` |
| 20.36-061 | Cross-turn `usp_version_ref` change (simulated) | `run_c7_d` |
| 20.36-062 | GB veto — prior snapshot unchanged (simulated) | `run_c7_e` |
| 20.207-001 | `strip_b_envelopes` removes B envelopes | strip scenarios |
| 20.207-004 | `validate_regeneration_input`; `merge_regeneration_input` | `negative_regen_input_incomplete`, `positive_regen_merge_from_fixture_root` |
| 20.207-007 | Forbidden `lane_id`/`tp_id` in regen path | `negative_regen_forbidden_lane_tp` |
| 20.207-017, 020 | `b_regeneration_equivalent_scaffold` (input validation only) | `scaffold_b_regeneration_equivalent` |
| 20.207-019 | Strip scope `[exec_plan, exec_trace]` | `positive_strip_replay_invariant`, `run_class_7_suite` |
| 20.207-028 | `REGEN_INPUT_INCOMPLETE` → `FAIL_REGEN_INPUT` | `negative_regen_input_incomplete` |
| 20.207-029 | `REGEN_TP_READ` → `FAIL_REGEN_FORBIDDEN_READ` | `negative_regen_forbidden_lane_tp` |
| 20.101-003 | Intake path stage ordering via live compose | `positive_c7_b_intake_path_order` |

### Open / partial
| HLR / area | Gap | Notes |
|------------|-----|-------|
| 20.36-016 | Classes 1–5 not runnable | W5 / 40.90 |
| 20.36-051 | Full `b_regeneration_equivalent` execution | E2 regen deferred W5 |
| 20.207-002..016 | Full E2 procedure | No B cluster in W1 |
| 20.207-005, 006, 030 | `REGEN_COMMIT_MISMATCH`, `REGEN_STALE_EPOCH` | W5 negative fixtures |
| 20.36-061, 062 (live) | UPI/GB wire | C7-D/E simulated; Wave 2 |
| 20.36-018 (YAML) | Golden file import | Inline runners only |
| 20.36-064 | Strip vs intake-bound diff scope | Partial via strip scenarios |

## Phase 1 delta (40.510-102)
- Created Class 7 harness: C7-A..E per 20.36 §9; composes 40.100 + 40.101
- Initial C7 5/5 PASS; Phase A approved (CP review, 2026-06-08)

## Phase B delta (40.20)
- Extended `prototype.py`: regen validation/merge, `b_regeneration_equivalent_scaffold`, `export_replay_diagnostics`, `REPLAY_VERDICTS`, B envelope guards
- Expanded harness from 6 → 18 scenarios: strip variants, determinism, intake path order, Class 1 strip demo, regen negatives/scaffold, fixture IDs, diagnostic export
- Full test matrix PASS; artifact `replay_class7_verification_run_2026-06-08.json`

## Flows Alignment Statement

- **Forward Flow (20-series)**: [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §9 and [20.207](../../20_requirements/20.207_execution_replay_specification.md) drive replay obligations; [40.100](../40.100_inb_prototypes/software_description.md) / [40.101](../40.101_iiinb_prototypes/software_description.md) supply intake path.
- **Backward Flow (40-series evidence)**: 18/18 PASS artifact proves GATE-A REPLAY_CLASS_7 + E1 strip + regen scaffold scope; residuals named above.
- **Iterative Design Flow (50-series influence)**: None yet; W5 orchestration deferred per [40.510](../40.510_refactor.md).

**Agreement Statement**: Aligned for Phase B closure. Promotion to 30-series and GATE-A sign-off require reviewer ☑ on 40.510-102; dual-pipeline PoC still needs W5 Classes 1–6 and live E2.

## Open gaps (W5 / Wave 2)
- Classes 1–6 unified runner (40.90, 40.80)
- E2 `b_regeneration_equivalent` execution on Class 1 fixture
- Live UPI/GB for C7-D/E (40.103, 40.36)
- YAML golden import from 20.36
- `REGEN_STALE_EPOCH` and commit-mismatch negatives