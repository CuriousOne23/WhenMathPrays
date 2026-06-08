# Requirements Delta

## Scaffold Status
- scaffold_status: implemented (Phase B v0.1 — Class 7 + E1 strip runnable, 2026-06-08)
- Phase A: **approved** (CP review, 2026-06-08)
- Phase B: v0.1 complete (C7 5/5 + strip demo PASS); formal approval pending (40.510-102, GATE-A)

## Anchors
- 20-anchor: thought_simulator/20_requirements/20.36_canonical_end_to_end_trace.md §9 (REPLAY_CLASS_7)
- 20-secondary: thought_simulator/20_requirements/20.207_execution_replay_specification.md (E1/E2/E3)
- upstream: 40.100_inb_prototypes, 40.101_iiinb_prototypes

## Exploratory Note
The full 20.207 HLR set (001–030) and 20.36 Class 7 HLRs (058–064) are visible in `software_description.md`. 20.xx is authoritative; 30.xx is the coverage audit layer. 40.207 is non-canonical.

## Part A Documentation (Phase A deliverables)
- `software_description.md`: purpose, W1/W5 roles, Class 7 fixture contracts, strip/E2 skeletons, digest, verdict taxonomy, full 20.207 HLR visibility, test matrix
- `verification_capsule.md`: Phase A checklist + initial C7 evidence baseline
- `prototype.py` / `harness.py`: C7-A..E runners + strip demo (pre-dated Phase A doc)

## Part B Evidence (Initial pass — 2026-06-08)
- Harness run: 2026-06-08
- Artifact: `artifacts/replay_class7_verification_run_2026-06-08.json`
- Status: PASS (C7 5/5 + `strip_replay_invariant`)
- Evidence types: behavioral, structural, replay, golden diff (strip digest)

### Implemented / demonstrated
| HLR | Implementation | Scenario |
|-----|----------------|----------|
| 20.36-058 | Replay digest equivalence in C7-B; escalate path C7-C | `run_c7_b`, `run_c7_c` |
| 20.36-059 | Zero Track H stages when profile disabled | `run_c7_a` |
| 20.36-060 | `envelope_guard` on repair paths | `run_c7_b`, `run_c7_c` |
| 20.36-061 | Cross-turn `usp_version_ref` change (simulated) | `run_c7_d` |
| 20.36-062 | GB veto — prior snapshot unchanged (simulated) | `run_c7_e` |
| 20.207-001 | `strip_b_envelopes` removes B envelopes | `strip_replay_invariant` |
| 20.207-019 | Strip scope `[exec_plan, exec_trace]` documented | `run_class_7_suite` + strip demo |

### Open / partial
| HLR / area | Gap | Notes |
|------------|-----|-------|
| 20.36-016 | Classes 1–5 not runnable | W5 / 40.90 |
| 20.36-051 / 20.207-017, 020 | `b_regeneration_equivalent` | E2 regen deferred W5 |
| 20.207-002..016 | Full E2 procedure | No B cluster in W1 |
| 20.207-028..030 | Negative regen fixtures | W5 |
| 20.36-061, 062 (live) | UPI/GB wire | C7-D/E simulated; Wave 2 |
| 20.36-018 | YAML golden import | Inline runners only |

## Phase 1 delta (40.510-102)
- Created Class 7 harness: C7-A..E per 20.36 §9; composes 40.100 + 40.101
- Initial C7 5/5 PASS; Phase A approved (CP review, 2026-06-08)

## Flows Alignment Statement

- **Forward Flow (20-series)**: [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §9 and [20.207](../../20_requirements/20.207_execution_replay_specification.md) drive replay obligations; [40.100](../40.100_inb_prototypes/software_description.md) / [40.101](../40.101_iiinb_prototypes/software_description.md) supply intake path.
- **Backward Flow (40-series evidence)**: C7 5/5 + strip demo PASS; open classes named above.
- **Iterative Design Flow (50-series influence)**: None yet; W5 orchestration deferred per [40.510](../40.510_refactor.md).

**Agreement Statement**: Provisionally aligned — Phase A approved (CP, 2026-06-08). Phase B formal approval requires expanded matrix and GATE-A sign-off on 40.510-102.

## Open gaps (W5 / Wave 2)
- Classes 1–6 unified runner (40.90, 40.80)
- E2 `b_regeneration_equivalent` on Class 1 fixture
- Live UPI/GB for C7-D/E (40.103, 40.36)
- YAML golden import from 20.36