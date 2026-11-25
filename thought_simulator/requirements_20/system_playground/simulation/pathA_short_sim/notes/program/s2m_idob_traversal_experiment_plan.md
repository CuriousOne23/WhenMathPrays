# S2M IdOB Traversal Experiment Plan

**Date:** 2026-11-25  
**Status:** Frozen bounded plan for current realization.  
**Depends on:** [s2m_idob_traversal_proposal.md](s2m_idob_traversal_proposal.md), [s2m_idob_traversal_program_reference.md](s2m_idob_traversal_program_reference.md).  
**Execution scope:** only experiments requiring no unresolved architectural choice and no semantic-policy change.

## Intent

Challenge (not confirm) the traversal proposal against present software realization by:

1. testing what can be observed directly;
2. exposing representability boundaries as evidence;
3. preserving unavailable states explicitly.

## Frozen execution surfaces

- Simulator entrypoint: [pathA_short_simulator.py](../../pathA_short_simulator.py) `run_pathA_short`
- Existing replay controls:  
  - [support/tools/s2m_canonical_sentences_replay.py](../../support/tools/s2m_canonical_sentences_replay.py)  
  - [support/tools/s2m_category_selection_replay.py](../../support/tools/s2m_category_selection_replay.py)
- Observed outputs only from existing fields:
  - `s2m_seed`
  - `s2m_meaning`
  - primitive trace entries for `CEx`, `CE`, `ISc`
  - `TP.semantic.isc_category_result`

No architecture-changing code edits are authorized by this plan.

## Measurement contract (per case)

Record, from current fields only:

- case ID
- input/evidence configuration
- door result (or explicit unavailability)
- `C_t` observation
- correspondence observation
- provenance/dependency observation
- `D_t`, `Q_t` (or explicit unavailability)
- `B_t` if legitimately computable
- `P_t` if legitimately computable
- `H_t` if legitimately computable
- artifact/log identity
- replay result
- anomaly/stop status

## Controlled matrix (smallest useful under current realization)

| Required control question | Planned case ID | Planned input/control | Expected representability status |
|---|---|---|---|
| 1) legal candidate + explicit supporting correspondence | `TC01_support` | `"The sky is blue."` + prior `["cold"]` | **Executable** (support-like relation visible through cue + legitimation surface). |
| 2) legal candidate + no established correspondence | `TC02_no_correspondence` | `"The sky is blue."` + no prior cue | **Executable** (candidate remains unselected; no opposition write). |
| 3) explicit opposition | `TC03_opposition_probe` | `"The sky is blue."` + prior `["not cold"]` | **Boundary probe** (expected unavailable without explicit opposition semantics). |
| 4) multiple independent supporting evidence families | `TC04_multi_source_support` | `"The sky is cold."` + prior `["cold"]` | **Boundary probe** (multi-source cue visible; independence not classifiable). |
| 5) duplicated/dependent supporting observations | `TC05_duplicate_prior` | `"The sky is blue."` + prior `["cold","cold","cold"]` | **Executable as duplicate probe** (check dedup/visibility; not independence). |
| 6) unknown-dependency evidence | `TC06_unknown_dependency_probe` | `"The sky is blue."` + prior `["cold from source a","cold from source b"]` | **Boundary probe** (unknown dependency expected unavailable). |
| 7) internal conflict | `TC07_internal_conflict_probe` | `"The book is on the table."` + prior `["cold"]` | **Executable conflict proxy** (mixed cue majors; no formal conflict qualifier expected). |
| 8) equal S/O balance with distinguishable evidence state | `TC08_balance_probe` | `"The book is on the table."` + prior `["cold table"]` | **Expected unavailable** (no directional `S/O` tuple). |
| 9) unequal directional discrimination | `TC09_unequal_direction_probe` | `"The book is on the table."` + prior `["table"]` | **Expected unavailable for directional tuple**; score surface observable only. |
| 10) >1 legal candidate with different directional support | `TC10_multi_candidate` | `"Where is the book?"` + no prior | **Executable for candidate-state diversity**; directional support tuple expected unavailable. |

Cases that are representationally unavailable will be marked `UNAVAILABLE` and treated as findings.

## Proposition challenge mapping

- **A (door / `C_t`)**: challenge finite-candidate observability and check whether structural legality is distinct from cue support.
- **B (`E_t`)**: challenge whether current surfaces can separate support/no-relation/opposition without reinterpreting missingness as opposition.
- **C (`L_t`)**: challenge provenance retention and dependency visibility boundaries.
- **D (`D_t`,`Q_t`)**: determine if directional and qualifier tuples are separately observable (expected boundary).
- **E (`B_t`)**: compute only if `D_t` legitimately exists (expected unavailable).
- **F (`P_t`)**: observe existing softmax only as category-scoring policy, not traversal architecture.
- **G (`H_t`)**: compute only if legitimate `P_t` for traversal candidates exists (expected unavailable).
- **H (continue/OuBA)**: do not define an exit rule; only observe available facts.

## Stop conditions (active)

Stop and report immediately if execution requires:

- inventing a correspondence relation;
- inventing opposition semantics;
- inventing dependency classification policy;
- inventing directional weighting or continue/OuBA sufficiency policy;
- changing existing semantic/category behavior or replay determinism;
- redefining normative 20-series boundaries.

## Replay / zero-drift verification plan

After case execution:

1. run [support/tools/s2m_canonical_sentences_replay.py](../../support/tools/s2m_canonical_sentences_replay.py);
2. run [support/tools/s2m_category_selection_replay.py](../../support/tools/s2m_category_selection_replay.py);
3. record pass/fail and anomalies in observation.

## Freeze note

This plan is frozen for the current run.  
Only the cases listed above may be executed under this plan.
