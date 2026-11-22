# Category Selection Observation

**Document:** notes/program/category_selection_observation.md  
**Status:** Active empirical observation record (non-normative).  
**Date:** 2026-11-22

## Purpose

Record empirical category-selection observations from approved experiments with explicit boundaries between observed facts, bounded interpretation, and not-established claims.

## Observation discipline

Each experiment record preserves:

1. **Observed** — what the instrument displayed.
2. **Interpretation** — bounded interpretation of those observations.
3. **Not established** — claims not supported by the evidence.
4. **Anomaly or unexpected observation** — deviations, failures, or architecture-limiting findings.
5. **Future question** — follow-on question motivated by the record.

## Experiment record — EXP1 baseline characterization (accepted)

### Observed

- Executed command:
  `python run_examples.py --execution-case sky_blue --enable-category-selection --no-category-observations --no-s2m-seed --characterize --char-type infra_smoke --char-session-id exp1_baseline --char-run-index 1 > run.log`
- Exit code was `0`.
- `run.log` contained normal TS output (`=== Final TP ===`, `=== Trace ===`) and exactly one final `=== CHAR TRACE ===` block.
- CHAR TRACE status line reported success for `infra_smoke` with `session_id=exp1_baseline` and `run_index=1`.
- CHAR TRACE pointed to a committed artifact at:
  `local_characterization/sessions/exp1_baseline/runs/000001__infra_smoke__1.0.tschar.json`.
- Artifact existed and parsed as schema `ts.characterization.run` / `1.0` with execution status `succeeded`.
- Artifact runtime-provided observations included:
  - `final_tp.truth_relation`
  - `trace.primitive_sequence`
  - `final_tp.semantic.isc_category_result`
- Artifact unavailable observations included:
  - `entropy`
  - `top_vs_second_margin`
- Baseline category-result values recorded for this run included:
  - `category_cue=[]`
  - `top_category=null`
  - `category_confidence=0.0`
  - rationale including `empty_category_cue`.

### Interpretation (bounded)

- This run supports that the implemented Milestone-1 infrastructure can execute one controlled characterization run and preserve baseline no-cue evidence with explicit provenance/unavailability fields.
- This run is a baseline infrastructure characterization record, not a threshold/policy conclusion.

### Not established

- No category-selection threshold or no-category decision policy is established.
- No entropy or top-vs-second-margin cutoff is established.
- No support-boundary conclusion is established.
- No empirical comparison between sentence-internal cue and prior-context cue paths is established by this single baseline run.

### Anomaly or unexpected observation

- None observed in this experiment.

### Future question

- What differences are observed between this no-cue baseline and the smallest controlled sentence-internal-cue case under the same TS-affecting controls, using currently implemented capabilities?

## Linked program context

- [category_selection_index.md](category_selection_index.md)
- [category_selection_research_plan.md](category_selection_research_plan.md)
- [category_selection_program_reference.md](category_selection_program_reference.md)
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md)
- [category_selection_proposal.md](category_selection_proposal.md)
- [category_structure_observation.md](category_structure_observation.md)

Generated characterization artifacts are evidence inputs to future entries in this observation record; this Markdown document remains the human scientific/observational record.

## Category-selection document family

For the complete category-selection document map, document roles, authority relationships, software references, characterization documents, and observation records, see:

[category_selection_index.md](category_selection_index.md)

## Explicit boundary

This placeholder contains no fabricated observations, no expected outcomes, and no prewritten experimental conclusions.
