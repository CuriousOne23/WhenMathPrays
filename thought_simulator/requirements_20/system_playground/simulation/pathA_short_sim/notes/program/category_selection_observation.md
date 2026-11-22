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

## Experiment record — EXP2 sentence-internal-cue characterization (accepted)

### 1) What executed (exact command, times/order)

- Order: single-command experiment execution (no additional experiment commands).
- Command executed exactly as specified in the experiment plan:
  `python -c "import sys; from pathlib import Path; p=Path('thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim').resolve(); sys.path.insert(0,str(p)); import run_examples as rx; from characterization.dispatcher import resolve_characterization; sim=rx.run_pathA_short('Where is the book?', enable_s2m_seed=False, enable_category_selection=True, prior_context=None); resolved=resolve_characterization('infra_smoke', None); req={'type':resolved['type'],'version':resolved['version'],'session_id':'exp2_sentence_internal','run_index':1,'resolved_type_parameters':resolved['params_resolver']({}),'runner':resolved['runner']}; result=rx.run_characterization_once(req, sim, {'execution_case':'sentence_internal_where_book','enable_category_selection':True,'enable_s2m_seed':False,'show_category_observations':False,'prior_context':None}); print(result['persistence']['committed_final_path'])"`
- Exit code: `0`.

### 2) Inputs and controls used

- Sentence-under-test: `"Where is the book?"`.
- TS-affecting controls:
  - `enable_category_selection=True`
  - `enable_s2m_seed=False`
  - `prior_context=None`
- Characterization controls:
  - type/version: `infra_smoke` / `1.0`
  - identity: `session_id=exp2_sentence_internal`, `run_index=1`
  - runtime metadata execution_case: `sentence_internal_where_book`

### 3) Produced artifacts/logs (exact paths)

- Committed artifact path returned by execution:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp2_sentence_internal/runs/000001__infra_smoke__1.0.tschar.json`
- Baseline artifact used for bounded comparison:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp1_baseline/runs/000001__infra_smoke__1.0.tschar.json`
- No additional experiment log file was produced by this in-process command.

### 4) Observed outputs (facts only)

- EXP2 artifact identity/schema/status:
  - `schema_id=ts.characterization.run`
  - `schema_version=1.0`
  - `characterization.type=infra_smoke`
  - `characterization.version=1.0`
  - `identity.session_id=exp2_sentence_internal`
  - `identity.run_index=1`
  - `execution_status=succeeded`
- EXP2 runtime-provided observations were present for:
  - `final_tp.truth_relation`
  - `trace.primitive_sequence`
  - `final_tp.semantic.isc_category_result`
- EXP2 unavailable observations were present for:
  - `entropy` (`milestone1_unavailable`)
  - `top_vs_second_margin` (`milestone1_unavailable`)
- EXP2 `final_tp.semantic.isc_category_result.value` included:
  - `category_cue=["perspectival"]`
  - `top_category="perspectival"`
  - `category_confidence=0.31090105669062545`
  - `category_rationale=["category_cue_applied","top_category=perspectival"]`
  - provenance source including `"sentence"`
- Bounded EXP1↔EXP2 fact-level comparison:
  - runtime/unavailable section shape was present in both artifacts;
  - `trace.primitive_sequence` was present in both artifacts;
  - `isc_category_result` differed from EXP1 baseline (`[]/null/0.0`) to EXP2 sentence-internal cue result (`["perspectival"]/"perspectival"/0.31090105669062545`);
  - `final_tp.truth_relation` was `declarative` in EXP1 and `interrogative` in EXP2.

### 5) Unavailable measurements/deviations

- `entropy` and `top_vs_second_margin` remained unavailable and explicitly marked as unavailable in EXP2.
- No deviation from the approved EXP2 command/controls was introduced.

### 6) Unexpected behavior/anomalies

- None observed for this execution.

### 7) Interpretation (bounded)

- This run establishes one controlled sentence-internal-cue characterization record under currently implemented capabilities and yields a concrete artifact suitable for comparison against EXP1 baseline.
- The record supports a bounded observational statement that EXP2 and EXP1 differ in the observed `isc_category_result` fields under their respective inputs/controls.

### 8) Not established

- No threshold/no-category policy is established.
- No support-boundary conclusion is established.
- No scientific meaning claim is established from the category result.
- No multi-run stability or generalization claim is established from this single EXP2 run.

### 9) Questions raised

- What is the smallest controlled prior-context cue/provenance experiment that can serve as a clean reference point against EXP1 baseline and EXP2 sentence-internal cue observations?

### 10) Next-step options (suggestions only, not decisions)

- Option A: design/specify EXP3 as the smallest prior-context cue/provenance experiment using current implementation controls.
- Option B: run one bounded off-plan verification replay (new run index) before EXP3 execution authorization.
- Option C: defer EXP3 until additional reviewer constraints are provided.

## Experiment record — EXP3 prior-context cue/provenance characterization (executed, pending review-gate decision)

### 1) What executed (exact command, times/order)

- Order: single-command experiment execution (no additional experiment commands).
- Command executed exactly as specified in the experiment plan:
  `python -c "import sys; from pathlib import Path; p=Path('thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim').resolve(); sys.path.insert(0,str(p)); import run_examples as rx; from characterization.dispatcher import resolve_characterization; sim=rx.run_pathA_short('The sky is blue.', enable_s2m_seed=False, enable_category_selection=True, prior_context=['location']); resolved=resolve_characterization('infra_smoke', None); req={'type':resolved['type'],'version':resolved['version'],'session_id':'exp3_prior_context','run_index':1,'resolved_type_parameters':resolved['params_resolver']({}),'runner':resolved['runner']}; result=rx.run_characterization_once(req, sim, {'execution_case':'sky_blue_prior_context_location','enable_category_selection':True,'enable_s2m_seed':False,'show_category_observations':False,'prior_context':['location']}); print(result['persistence']['committed_final_path'])"`
- Exit code: `0`.

### 2) Inputs and controls used

- Sentence-under-test: `"The sky is blue."`.
- Prior context: `["location"]`.
- TS-affecting controls:
  - `enable_category_selection=True`
  - `enable_s2m_seed=False`
  - `prior_context=["location"]`
- Characterization controls:
  - type/version: `infra_smoke` / `1.0`
  - identity: `session_id=exp3_prior_context`, `run_index=1`
  - runtime metadata execution_case: `sky_blue_prior_context_location`

### 3) Produced artifacts/logs (exact paths)

- Committed artifact path returned by execution:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp3_prior_context/runs/000001__infra_smoke__1.0.tschar.json`
- Accepted reference artifacts used for bounded comparison:
  - `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp1_baseline/runs/000001__infra_smoke__1.0.tschar.json`
  - `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp2_sentence_internal/runs/000001__infra_smoke__1.0.tschar.json`
- No additional experiment log file was produced by this in-process command.

### 4) Observed outputs (facts only)

- EXP3 artifact identity/schema/status:
  - `schema_id=ts.characterization.run`
  - `schema_version=1.0`
  - `characterization.type=infra_smoke`
  - `characterization.version=1.0`
  - `identity.session_id=exp3_prior_context`
  - `identity.run_index=1`
  - `execution_status=succeeded`
- EXP3 runtime-provided observations were present for:
  - `final_tp.truth_relation`
  - `trace.primitive_sequence`
  - `final_tp.semantic.isc_category_result`
- EXP3 unavailable observations were present for:
  - `entropy` (`milestone1_unavailable`)
  - `top_vs_second_margin` (`milestone1_unavailable`)
- EXP3 `final_tp.semantic.isc_category_result.value` included:
  - `category_cue=["perspectival"]`
  - `top_category="perspectival"`
  - `category_confidence=0.2505069933606234`
  - `category_rationale=["category_cue_applied","top_category=perspectival"]`
  - provenance: `source=["prior_context_cex"]`, `upstream="ce"`, and expected weight fields
- Bounded EXP1↔EXP2↔EXP3 fact-level comparison:
  - runtime/unavailable section shape present in all three artifacts;
  - `trace.primitive_sequence` present in all three artifacts;
  - provenance `source` field distinctions:
    - EXP1: `[]`
    - EXP2: `["sentence"]`
    - EXP3: `["prior_context_cex"]`
  - `final_tp.truth_relation`:
    - EXP1: `declarative`
    - EXP2: `interrogative`
    - EXP3: `declarative`

### 5) Unavailable measurements/deviations

- `entropy` and `top_vs_second_margin` remained unavailable and explicitly marked as unavailable in EXP3.
- No deviation from the approved EXP3 command/controls was introduced.

### 6) Unexpected behavior/anomalies

- None observed for this execution.

### 7) Interpretation (bounded)

- This run establishes one controlled prior-context characterization record under currently implemented capabilities and yields a concrete prior-context provenance reference artifact.
- The run supports bounded observational contrast of provenance-source fields across accepted references: no cue source (EXP1), sentence source (EXP2), and prior-context source (EXP3).

### 8) Not established

- No threshold/no-category policy is established.
- No support-boundary conclusion is established.
- No scientific meaning claim is established from category results.
- No multi-run stability or generalization claim is established from this single EXP3 run.

### 9) Questions raised

- Should EXP3 be accepted as the prior-context provenance reference point for subsequent experiment design decisions?
- Should any next step prioritize ambiguity-family comparison, boundary-family comparison, or a bounded off-plan verification run?

### 10) Next-step options (suggestions only, not decisions)

- Option A: accept EXP3 and authorize EXP4 design/specification under the existing review-gated process.
- Option B: request one bounded off-plan verification run focused on provenance replay before EXP4 direction.
- Option C: accept EXP3 and defer EXP4 pending reviewer prioritization among provisional roadmap families.

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
