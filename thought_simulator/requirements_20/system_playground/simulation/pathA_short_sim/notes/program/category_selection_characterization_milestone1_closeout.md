# Category Selection Characterization — Milestone 1 Closeout

**Document:** notes/program/category_selection_characterization_milestone1_closeout.md  
**Status:** Non-normative implementation/verification closeout record.  
**Date:** 2026-11-22

## 1) Purpose and status

This document closes Characterization Infrastructure Milestone 1.

It records bounded implementation/verification completion status only. Normative and contractual authority remains in the program/reference documents, especially:

- [category_selection_program_reference.md](category_selection_program_reference.md)
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md)

This closeout does not claim scientific category-selection conclusions.

## 2) Milestone-1 scope

Milestone 1 established and verified characterization infrastructure for a single-run, CLI-driven workflow on current Path A short simulation execution.

It did not establish empirical category-selection policy conclusions.

## 3) Implemented capability

Milestone 1 implemented and verified bounded infrastructure for:

- explicit CLI-driven characterization;
- shared ordinary/characterized TS execution;
- execution-level case selection separate from characterization parameters;
- observer-only `infra_smoke`;
- one TS execution per characterization invocation;
- runtime-provided/unavailable observation provenance;
- success-only `.tschar.json` evidence;
- fixed local-only characterization storage;
- canonical `(session_id, run_index)` identity;
- safe temporary-file persistence with required flush/fsync;
- validated artifact construction;
- race-safe hard non-overwrite final placement;
- CHAR TRACE success/failure pointer reporting;
- compatibility with `run_examples.py -> run.log -> pathA_dbug.py -> debug_out.md`;
- unchanged [pathA_dbug.py](../../pathA_dbug.py) compatibility.

## 4) Verified invariants

Milestone-1 verification established that:

- characterization observes the same selected TS execution available to ordinary execution;
- characterization does not own or silently alter TS-affecting controls;
- `infra_smoke` does not mutate observed `simulation_result`;
- one characterization invocation performs one TS execution;
- equivalent ordinary/characterized execution agrees at Level A on behaviorally meaningful TS results;
- the only approved non-behavioral Level-A exclusion is `created_at_utc`;
- differences outside approved exclusions require investigation;
- Level B confirms faithful recording of selected runtime observations;
- successful evidence cannot silently overwrite prior evidence;
- duplicate canonical identity is rejected before TS execution where already visible;
- race-time final placement protection remains authoritative;
- ordinary non-characterized execution creates no characterization evidence;
- characterization payload/results do not leak into `run.log` or `debug_out.md`.

## 5) Verification/tooling

Durable verification mechanisms include:

- [support/tools/characterization_artifact_replay.py](../../support/tools/characterization_artifact_replay.py)  
  Role: characterization infrastructure persistence regression/replay verification.
- Existing workflow compatibility verification:
  `run_examples.py -> run.log -> pathA_dbug.py -> debug_out.md`.

Persistence replay verifies infrastructure properties; it is not empirical category-selection research evidence.

## 6) Explicit exclusions / not established

Milestone 1 did **not** establish:

- a final no-category decision function;
- category-selection threshold policy;
- entropy cutoff;
- top-vs-second-margin cutoff;
- hysteresis policy;
- persistence decision policy;
- unsupported-category/inadequate-inventory policy;
- support-boundary empirical conclusions;
- a multi-run characterization orchestrator;
- a session manifest/campaign-management layer;
- aggregate characterization analysis;
- empirical category-selection conclusions.

## 7) Closeout statement

Characterization Infrastructure Milestone 1 establishes the bounded, verified infrastructure required to begin controlled category-selection characterization.

It closes infrastructure establishment only.

It does not close the category-selection research program and does not preselect scientific results or policies that future characterization is intended to discover.

## 8) Next research/engineering boundary

Next work is to use this verified infrastructure for controlled characterization under:

- [category_selection_research_plan.md](category_selection_research_plan.md)
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md)

This closeout does not define the next experiment or preselect thresholds.

## 9) Related authoritative documents

- [category_selection_index.md](category_selection_index.md)
- [category_selection_program_reference.md](category_selection_program_reference.md)
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md)
- [category_selection_research_plan.md](category_selection_research_plan.md)
- [category_selection_observation.md](category_selection_observation.md)
