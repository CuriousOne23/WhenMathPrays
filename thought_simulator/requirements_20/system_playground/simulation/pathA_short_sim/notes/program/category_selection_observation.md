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

## Accepted synthesis — EXP1 to EXP3 (tractability evidence, bounded)

Accepted EXP1–EXP3 records provide initial empirical evidence that the current Category Selection mechanism is a tractable experimental system under the present Milestone-1 characterization method.

Current accepted reference points are:

- **EXP1:** no supplied category cue reference (`category_cue=[]`, no cue provenance source).
- **EXP2:** sentence-derived category evidence/provenance reference (source includes `"sentence"`).
- **EXP3:** prior-context-derived category evidence/provenance reference (source includes `"prior_context_cex"`).

This synthesis is bounded: these accepted runs support tractable observation and controlled comparison reference points; they do not establish the full Category Selection space, its boundaries, its internal geometry/curve, a confidence threshold/no-category policy, stability/generalization, or scientific meaning conclusions.

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

## Experiment record — EXP3 prior-context cue/provenance characterization (accepted)

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

- Which bounded EXP4 boundary proposal should be reviewed first, given accepted EXP1–EXP3 tractability/reference evidence?

### 10) Next-step options (suggestions only, not decisions)

- Option A: propose (but do not yet fully commit) the first EXP4 boundary subexperiment for review.
- Option B: request one bounded off-plan verification run focused on provenance replay before EXP4 direction.
- Option C: defer EXP4 boundary proposal pending reviewer prioritization.

## Experiment record — EXP4A prior-context representability boundary (accepted)

### 1) What executed (exact command, times/order)

- Order: two-command paired execution under one session identity (`exp4a_prior_context_repr`).
- Run 1 (mapped `location`) command:
  `python -c "import sys; from pathlib import Path; p=Path('thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim').resolve(); sys.path.insert(0,str(p)); import run_examples as rx; from characterization.dispatcher import resolve_characterization; sim=rx.run_pathA_short('The sky is blue.', enable_s2m_seed=False, enable_category_selection=True, prior_context=['location']); resolved=resolve_characterization('infra_smoke', None); req={'type':resolved['type'],'version':resolved['version'],'session_id':'exp4a_prior_context_repr','run_index':1,'resolved_type_parameters':resolved['params_resolver']({}),'runner':resolved['runner']}; result=rx.run_characterization_once(req, sim, {'execution_case':'sky_blue_prior_context_location','enable_category_selection':True,'enable_s2m_seed':False,'show_category_observations':False,'prior_context':['location']}); print(result['persistence']['committed_final_path'])"`
- Run 2 (unmapped `position`) command:
  `python -c "import sys; from pathlib import Path; p=Path('thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim').resolve(); sys.path.insert(0,str(p)); import run_examples as rx; from characterization.dispatcher import resolve_characterization; sim=rx.run_pathA_short('The sky is blue.', enable_s2m_seed=False, enable_category_selection=True, prior_context=['position']); resolved=resolve_characterization('infra_smoke', None); req={'type':resolved['type'],'version':resolved['version'],'session_id':'exp4a_prior_context_repr','run_index':2,'resolved_type_parameters':resolved['params_resolver']({}),'runner':resolved['runner']}; result=rx.run_characterization_once(req, sim, {'execution_case':'sky_blue_prior_context_position','enable_category_selection':True,'enable_s2m_seed':False,'show_category_observations':False,'prior_context':['position']}); print(result['persistence']['committed_final_path'])"`
- Exit codes: run 1 `0`; run 2 `0`.

### 2) Inputs and controls used

- Utterance fixed in both runs: `"The sky is blue."`.
- Prior context:
  - run 1 mapped: `["location"]`
  - run 2 unmapped: `["position"]`
- Fixed TS-affecting controls (both runs):
  - `enable_category_selection=True`
  - `enable_s2m_seed=False`
- Fixed characterization controls (both runs):
  - type/version: `infra_smoke` / `1.0`
  - session: `exp4a_prior_context_repr`
  - run indices: `1`, `2`

### 3) Produced artifacts/logs (exact paths)

- Run 1 committed artifact:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp4a_prior_context_repr/runs/000001__infra_smoke__1.0.tschar.json`
- Run 2 committed artifact:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp4a_prior_context_repr/runs/000002__infra_smoke__1.0.tschar.json`
- Accepted mapped-anchor reference artifact (EXP3):
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp3_prior_context/runs/000001__infra_smoke__1.0.tschar.json`
- No additional experiment log file was produced by these in-process commands.

### 4) Observed outputs (facts only)

- Both EXP4A artifacts reported:
  - `schema_id=ts.characterization.run`
  - `schema_version=1.0`
  - `characterization.type=infra_smoke`
  - `characterization.version=1.0`
  - `execution_status=succeeded`
- Runtime-provided observation shape was present in both runs for:
  - `final_tp.truth_relation`
  - `trace.primitive_sequence`
  - `final_tp.semantic.isc_category_result`
- Unavailable observations were present in both runs for:
  - `entropy` (`milestone1_unavailable`)
  - `top_vs_second_margin` (`milestone1_unavailable`)
- Fact-level mapped vs unmapped comparison:
  - run 1 (`location`) `isc_category_result.value`:
    - `category_cue=["perspectival"]`
    - `top_category="perspectival"`
    - `category_confidence=0.2505069933606234`
    - `provenance.source=["prior_context_cex"]`
  - run 2 (`position`) `isc_category_result.value`:
    - `category_cue=[]`
    - `top_category=null`
    - `category_confidence=0.0`
    - `provenance.source=[]`
- Fact-level mapped-run anchor check versus accepted EXP3 mapped reference:
  - run 1 and EXP3 mapped artifact matched on key observed cue/result/provenance fields above.

### 5) Unavailable measurements/deviations

- `entropy` and `top_vs_second_margin` remained unavailable and explicitly marked as unavailable in both runs.
- No deviation from approved EXP4A controls/identity structure was introduced.

### 6) Unexpected behavior/anomalies

- None observed in this paired execution.

### 7) Interpretation (bounded)

- This paired run set provides an observable mapped-versus-unmapped prior-context representability reference under fixed utterance and fixed controls.
- The mapped side is consistent with accepted EXP3 mapped reference on the documented fact-level fields.
- Under the tested conditions, this accepted record provides evidence for an observable prior-context representability boundary: mapped prior-context information produced category evidence and a category result, while the selected unmapped comparator did not.

### 8) Not established

- No threshold/no-category policy is established.
- No global category-space boundary geometry or curve is established.
- No stability/generalization claim beyond this paired case is established.
- No scientific meaning claim is established.

### 9) Questions raised

- What is the cleanest mapped-versus-unmapped present-utterance representability pair for EXP4B under fixed controls?
- Which specific EXP4B pair should be approved for one-at-a-time execution authorization?

### 10) Next-step options (suggestions only, not decisions)

- Option A: fully specify EXP4B only (present-utterance representability boundary), then stop at pre-execution review gate.
- Option B: defer EXP4B specification pending additional pair-selection constraints.
- Option C: retain EXP4A as accepted and reprioritize later EXP4 boundary candidates before EXP4B.

## Experiment record — EXP4B present-utterance representability boundary (accepted)

### 1) What executed (exact command, times/order)

- Order: two-command paired execution under one session identity (`exp4b_utterance_repr`).
- Run 1 (mapped `where`) command:
  `python -c "import sys; from pathlib import Path; p=Path('thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim').resolve(); sys.path.insert(0,str(p)); import run_examples as rx; from characterization.dispatcher import resolve_characterization; sim=rx.run_pathA_short('Where is the book?', enable_s2m_seed=False, enable_category_selection=True, prior_context=None); resolved=resolve_characterization('infra_smoke', None); req={'type':resolved['type'],'version':resolved['version'],'session_id':'exp4b_utterance_repr','run_index':1,'resolved_type_parameters':resolved['params_resolver']({}),'runner':resolved['runner']}; result=rx.run_characterization_once(req, sim, {'execution_case':'where_is_book_mapped','enable_category_selection':True,'enable_s2m_seed':False,'show_category_observations':False,'prior_context':None}); print(result['persistence']['committed_final_path'])"`
- Run 2 (unmapped `when`) command:
  `python -c "import sys; from pathlib import Path; p=Path('thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim').resolve(); sys.path.insert(0,str(p)); import run_examples as rx; from characterization.dispatcher import resolve_characterization; sim=rx.run_pathA_short('When is the book?', enable_s2m_seed=False, enable_category_selection=True, prior_context=None); resolved=resolve_characterization('infra_smoke', None); req={'type':resolved['type'],'version':resolved['version'],'session_id':'exp4b_utterance_repr','run_index':2,'resolved_type_parameters':resolved['params_resolver']({}),'runner':resolved['runner']}; result=rx.run_characterization_once(req, sim, {'execution_case':'when_is_book_unmapped','enable_category_selection':True,'enable_s2m_seed':False,'show_category_observations':False,'prior_context':None}); print(result['persistence']['committed_final_path'])"`
- Exit codes: run 1 `0`; run 2 `0`.

### 2) Inputs and controls used

- Present utterances:
  - run 1 mapped: `"Where is the book?"`
  - run 2 unmapped: `"When is the book?"`
- Prior context fixed absent for both runs: `prior_context=None`.
- Fixed TS-affecting controls:
  - `enable_category_selection=True`
  - `enable_s2m_seed=False`
- Fixed characterization controls:
  - type/version: `infra_smoke` / `1.0`
  - session: `exp4b_utterance_repr`
  - run indices: `1`, `2`

### 3) Produced artifacts/logs (exact paths)

- Run 1 committed artifact:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp4b_utterance_repr/runs/000001__infra_smoke__1.0.tschar.json`
- Run 2 committed artifact:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp4b_utterance_repr/runs/000002__infra_smoke__1.0.tschar.json`
- Accepted mapped reference artifact (EXP2):
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp2_sentence_internal/runs/000001__infra_smoke__1.0.tschar.json`
- No additional experiment log file was produced by these in-process commands.

### 4) Observed outputs (facts only)

- Both EXP4B artifacts reported:
  - `schema_id=ts.characterization.run`
  - `schema_version=1.0`
  - `characterization.type=infra_smoke`
  - `characterization.version=1.0`
  - `execution_status=succeeded`
- Runtime-provided observation shape was present in both runs for:
  - `final_tp.truth_relation`
  - `trace.primitive_sequence`
  - `final_tp.semantic.isc_category_result`
- Unavailable observations were present in both runs for:
  - `entropy` (`milestone1_unavailable`)
  - `top_vs_second_margin` (`milestone1_unavailable`)
- Fact-level mapped vs unmapped comparison (`where` vs `when`):
  - run 1 mapped:
    - `category_cue=["perspectival"]`
    - `top_category="perspectival"`
    - `category_confidence=0.31090105669062545`
    - `category_rationale=["category_cue_applied","top_category=perspectival"]`
    - `provenance.source=["sentence"]`
  - run 2 unmapped:
    - `category_cue=[]`
    - `top_category=null`
    - `category_confidence=0.0`
    - `category_rationale=["empty_category_cue","top_category=null"]`
    - `provenance.source=[]`
- Relevant mapped-reference comparison to accepted EXP2:
  - EXP4B run 1 and EXP2 mapped artifact align on truth relation (`interrogative`), mapped cue/result/confidence/rationale/provenance fields listed above.

### 5) Unavailable measurements/deviations

- `entropy` and `top_vs_second_margin` remained unavailable and explicitly marked as unavailable in both runs.
- No deviation from approved EXP4B paired controls/identity structure was introduced.

### 6) Unexpected behavior/anomalies

- None observed in this paired execution.

### 7) Interpretation (bounded)

- This paired run set provides an observable mapped-versus-unmapped present-utterance representability reference under fixed controls.
- The mapped side is consistent with accepted EXP2 mapped reference on documented fact-level fields.
- Under the tested conditions, this accepted record provides evidence for an observable present-utterance representability boundary: mapped present-utterance information produced category evidence and a category result, while the selected unmapped comparator did not.

### 8) Not established

- No threshold/no-category policy is established.
- No global category-space boundary geometry/curve is established.
- No stability/generalization claim beyond this paired case is established.
- No scientific meaning claim is established.

### 9) Questions raised

- What is the cleanest contextual-applicability pair for EXP4G where mapped lexical representability is held constant across both sides?
- Which specific EXP4G pair should be approved for one-at-a-time execution authorization?

### 10) Next-step options (suggestions only, not decisions)

- Option A: fully specify EXP4G only (contextual-applicability boundary), then stop at pre-execution review gate.
- Option B: defer EXP4G specification pending additional contextual-applicability pair-selection constraints.
- Option C: retain EXP4B as accepted and reprioritize later retained EXP4 boundary candidates before EXP4G.

## Experiment record — EXP4G contextual-applicability boundary (accepted, audit limitation noted)

### 1) What executed (exact command, times/order)

- Order: two-command paired execution under one session identity (`exp4g_contextual_applicability`).
- Run 1 (contextually applicable `support`) command:
  `python -c "import sys; from pathlib import Path; p=Path('thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim').resolve(); sys.path.insert(0,str(p)); import run_examples as rx; from characterization.dispatcher import resolve_characterization; sim=rx.run_pathA_short('The bridge needs support.', enable_s2m_seed=False, enable_category_selection=True, prior_context=None); resolved=resolve_characterization('infra_smoke', None); req={'type':resolved['type'],'version':resolved['version'],'session_id':'exp4g_contextual_applicability','run_index':1,'resolved_type_parameters':resolved['params_resolver']({}),'runner':resolved['runner']}; result=rx.run_characterization_once(req, sim, {'execution_case':'support_context_applicable','enable_category_selection':True,'enable_s2m_seed':False,'show_category_observations':False,'prior_context':None}); print(result['persistence']['committed_final_path'])"`
- Run 2 (contextually inapplicable/metalinguistic `support`) command:
  `python -c "import sys; from pathlib import Path; p=Path('thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim').resolve(); sys.path.insert(0,str(p)); import run_examples as rx; from characterization.dispatcher import resolve_characterization; sim=rx.run_pathA_short('The word support has seven letters.', enable_s2m_seed=False, enable_category_selection=True, prior_context=None); resolved=resolve_characterization('infra_smoke', None); req={'type':resolved['type'],'version':resolved['version'],'session_id':'exp4g_contextual_applicability','run_index':2,'resolved_type_parameters':resolved['params_resolver']({}),'runner':resolved['runner']}; result=rx.run_characterization_once(req, sim, {'execution_case':'support_context_metalinguistic','enable_category_selection':True,'enable_s2m_seed':False,'show_category_observations':False,'prior_context':None}); print(result['persistence']['committed_final_path'])"`
- Exit codes: paired command execution `0`.

### 2) Inputs and controls used

- Present utterances:
  - run 1 (contextually applicable): `"The bridge needs support."`
  - run 2 (contextually inapplicable/metalinguistic): `"The word support has seven letters."`
- Mapped cue held constant in both utterances: `support -> physical` (sentence-internal mapping).
- Prior context fixed absent for both runs: `prior_context=None`.
- Fixed TS-affecting controls:
  - `enable_category_selection=True`
  - `enable_s2m_seed=False`
- Fixed characterization controls:
  - type/version: `infra_smoke` / `1.0`
  - session: `exp4g_contextual_applicability`
  - run indices: `1`, `2`

### 3) Produced artifacts/logs (exact paths)

- Run 1 committed artifact:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp4g_contextual_applicability/runs/000001__infra_smoke__1.0.tschar.json`
- Run 2 committed artifact:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp4g_contextual_applicability/runs/000002__infra_smoke__1.0.tschar.json`
- No additional experiment log file was produced by these in-process commands.

### 4) Observed outputs (facts only)

- Both EXP4G artifacts reported:
  - `schema_id=ts.characterization.run`
  - `schema_version=1.0`
  - `characterization.type=infra_smoke`
  - `characterization.version=1.0`
  - `execution_status=succeeded`
- Runtime-provided observation shape was present in both runs for:
  - `final_tp.truth_relation`
  - `trace.primitive_sequence`
  - `final_tp.semantic.isc_category_result`
- Unavailable observations were present in both runs for:
  - `entropy` (`milestone1_unavailable`)
  - `top_vs_second_margin` (`milestone1_unavailable`)
- Fact-level comparison (same mapped cue token `support` in both contextual uses):
  - run 1 (contextually applicable):
    - `category_cue=["physical"]`
    - `top_category="physical"`
    - `category_confidence=0.26974629435004127`
    - `category_rationale=["category_cue_applied","top_category=physical"]`
    - `provenance.source=["sentence"]`
  - run 2 (contextually inapplicable/metalinguistic):
    - `category_cue=["physical"]`
    - `top_category="physical"`
    - `category_confidence=0.26974629435004127`
    - `category_rationale=["category_cue_applied","top_category=physical"]`
    - `provenance.source=["sentence"]`
- Observed paired result for key cue/result/confidence/rationale/provenance fields above: no difference observed between run 1 and run 2.

### 5) Unavailable measurements/deviations

- `entropy` and `top_vs_second_margin` remained unavailable and explicitly marked as unavailable in both runs.
- No deviation from approved EXP4G paired controls/identity structure was introduced.

### 6) Unexpected behavior/anomalies

- None observed in this paired execution.

### 7) Interpretation (bounded)

- Under tested EXP4G conditions, the two mapped `support` usages produced the same observed Category Selection cue/result/confidence/rationale/provenance fields.
- This is compatible with the currently implemented lexical cue-recognition behavior and does not by itself constitute failure.
- This paired record may characterize the current boundary between lexical mapped-cue recognition and contextual applicability discrimination under this implementation.
- Accepted audit limitation note: non-executing support/dictionary audit found sparse non-cue lexical coverage for both EXP4G utterances; no strong differential static-representation confound was identified for this paired comparison.

### 8) Not established

- No claim is established that contextual applicability is never distinguishable in all cases.
- No threshold/no-category policy is established.
- No global category-space boundary geometry/curve is established.
- No stability/generalization claim beyond this paired case is established.
- No scientific meaning claim is established.

### 9) Questions raised

- Which retained EXP4 boundary candidate should be specified next under one-at-a-time review gating?
- Should any additional lexical-coverage controls be required for later linguistic boundary pair selection beyond mandatory vocabulary/support-coverage auditing?

### 10) Next-step options (suggestions only, not decisions)

- Option A: select one retained EXP4 boundary candidate for full specification only (no execution yet), then stop at pre-execution review gate.
- Option B: defer next EXP4 specification pending additional pair/control constraints.
- Option C: hold boundary progression while reprioritizing retained EXP4 sequence with current accepted records.

## Experiment record — EXP4C1 within-utterance conflicting mapped category evidence (accepted)

### 1) What executed (exact command, times/order)

- Order: one-command execution under one session identity (`exp4c1_within_utterance_conflict`).
- Run 1 (conflict utterance) command:
  `python -c "import sys; from pathlib import Path; p=Path('thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim').resolve(); sys.path.insert(0,str(p)); import run_examples as rx; from characterization.dispatcher import resolve_characterization; sim=rx.run_pathA_short('Where is the cold book?', enable_s2m_seed=False, enable_category_selection=True, prior_context=None); resolved=resolve_characterization('infra_smoke', None); req={'type':resolved['type'],'version':resolved['version'],'session_id':'exp4c1_within_utterance_conflict','run_index':1,'resolved_type_parameters':resolved['params_resolver']({}),'runner':resolved['runner']}; result=rx.run_characterization_once(req, sim, {'execution_case':'within_utterance_conflict_where_cold_book','enable_category_selection':True,'enable_s2m_seed':False,'show_category_observations':False,'prior_context':None}); print(result['persistence']['committed_final_path'])"`
- Exit code: `0`.

### 2) Inputs and controls used

- Present utterance: `"Where is the cold book?"`
- Intended mapped cue directions in same utterance:
  - `where -> perspectival`
  - `cold -> affective`
- Prior context fixed absent: `prior_context=None`.
- Fixed TS-affecting controls:
  - `enable_category_selection=True`
  - `enable_s2m_seed=False`
- Fixed characterization controls:
  - type/version: `infra_smoke` / `1.0`
  - session: `exp4c1_within_utterance_conflict`
  - run index: `1`

### 3) Produced artifacts/logs (exact paths)

- Run 1 committed artifact:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp4c1_within_utterance_conflict/runs/000001__infra_smoke__1.0.tschar.json`
- Accepted bounded comparison reference artifact (EXP2):
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp2_sentence_internal/runs/000001__infra_smoke__1.0.tschar.json`
- No additional experiment log file was produced by this in-process command.

### 4) Observed outputs (facts only)

- EXP4C1 artifact reported:
  - `schema_id=ts.characterization.run`
  - `schema_version=1.0`
  - `characterization.type=infra_smoke`
  - `characterization.version=1.0`
  - `execution_status=succeeded`
- Runtime-provided observation shape was present for:
  - `final_tp.truth_relation`
  - `trace.primitive_sequence`
  - `final_tp.semantic.isc_category_result`
- Unavailable observations were present:
  - `entropy` (`milestone1_unavailable`)
  - `top_vs_second_margin` (`milestone1_unavailable`)
- EXP4C1 category-result facts:
  - `category_cue=["affective","perspectival"]`
  - `category_weighted_distribution` includes mapped-category entries:
    - `perspectival`: `probability=0.26892192702831497`, `category_hit=true`
    - `affective`: `probability=0.22017465183507434`, `category_hit=true`
  - `top_category="perspectival"`
  - `category_confidence=0.26892192702831497`
  - `category_rationale=["category_cue_applied","top_category=perspectival"]`
  - `provenance.source=["sentence"]`
  - `provenance.upstream="ce"`
  - `provenance.weights={"w_s":0.35,"w_b":0.25,"w_e":0.2,"w_i":0.2,"w_cat":0.6}`
- Simultaneous multi-direction mapped cue presence check:
  - both intended mapped directions were observed in `category_cue` (`affective` and `perspectival`) in this single run.
- Bounded comparison with accepted EXP2 mapped reference (where appropriate):
  - both runs report `truth_relation="interrogative"`;
  - both runs report `provenance.source=["sentence"]`;
  - EXP2 mapped reference has single mapped cue (`["perspectival"]`), whereas EXP4C1 reports two mapped cues (`["affective","perspectival"]`);
  - EXP2 `category_confidence=0.31090105669062545`, EXP4C1 `category_confidence=0.26892192702831497`.

### 5) Unavailable measurements/deviations

- `entropy` and `top_vs_second_margin` remained unavailable and explicitly marked as unavailable.
- No deviation from approved EXP4C1 fixed controls/identity structure was introduced.

### 6) Unexpected behavior/anomalies

- None observed in this single-run execution.

### 7) Interpretation (bounded)

- Under tested EXP4C1 conditions, this run records simultaneous mapped multi-direction cue presence in one utterance and the resulting bounded category-result fields.
- This record characterizes a within-utterance conflict boundary condition for the current implementation.
- Under the tested conditions, this accepted record provides evidence for an observable within-utterance conflict boundary: multiple mapped category directions were simultaneously present in `category_cue` and yielded bounded category-result fields.

### 8) Not established

- No claim is made about which category should win in principle.
- No competition curve, crossover point, or interior strength trajectory is established.
- No threshold/no-category policy is established.
- No stability/generalization claim beyond this case is established.
- No scientific meaning claim is established.

### 9) Questions raised

- What is the cleanest first cross-source conflict case for EXP4C2 under fixed controls?
- Which specific EXP4C2 case should be approved for one-at-a-time execution authorization?

### 10) Next-step options (suggestions only, not decisions)

- Option A: fully specify EXP4C2 only (cross-source conflict boundary), then stop at pre-execution review gate.
- Option B: defer EXP4C2 specification pending additional pair/control constraints.
- Option C: retain EXP4C1 as accepted and reprioritize later retained EXP4 boundary candidates before EXP4C2.

## Experiment record — EXP4C2 cross-source conflicting mapped category evidence (executed, pending review-gate decision)

### 1) What executed (exact command, times/order)

- Order: one-command execution under one session identity (`exp4c2_cross_source_conflict`).
- Run 1 (cross-source conflict case) command:
  `python -c "import sys; from pathlib import Path; p=Path('thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim').resolve(); sys.path.insert(0,str(p)); import run_examples as rx; from characterization.dispatcher import resolve_characterization; sim=rx.run_pathA_short('The book is cold.', enable_s2m_seed=False, enable_category_selection=True, prior_context=['location']); resolved=resolve_characterization('infra_smoke', None); req={'type':resolved['type'],'version':resolved['version'],'session_id':'exp4c2_cross_source_conflict','run_index':1,'resolved_type_parameters':resolved['params_resolver']({}),'runner':resolved['runner']}; result=rx.run_characterization_once(req, sim, {'execution_case':'cross_source_conflict_book_cold_location','enable_category_selection':True,'enable_s2m_seed':False,'show_category_observations':False,'prior_context':['location']}); print(result['persistence']['committed_final_path'])"`
- Exit code: `0`.

### 2) Inputs and controls used

- Present utterance: `"The book is cold."`
- Prior context: `["location"]`
- Intended mapped cue directions in different sources:
  - sentence cue `cold -> affective`
  - prior-context cue `location -> perspectival`
- Fixed TS-affecting controls:
  - `enable_category_selection=True`
  - `enable_s2m_seed=False`
- Fixed characterization controls:
  - type/version: `infra_smoke` / `1.0`
  - session: `exp4c2_cross_source_conflict`
  - run index: `1`

### 3) Produced artifacts/logs (exact paths)

- Run 1 committed artifact:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp4c2_cross_source_conflict/runs/000001__infra_smoke__1.0.tschar.json`
- Accepted bounded comparison references:
  - EXP2 mapped sentence-source reference:
    `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp2_sentence_internal/runs/000001__infra_smoke__1.0.tschar.json`
  - EXP3 mapped prior-context-source reference:
    `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp3_prior_context/runs/000001__infra_smoke__1.0.tschar.json`
  - EXP4B mapped sentence representability reference:
    `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/exp4b_utterance_repr/runs/000001__infra_smoke__1.0.tschar.json`
- No additional experiment log file was produced by this in-process command.

### 4) Observed outputs (facts only)

- EXP4C2 artifact reported:
  - `schema_id=ts.characterization.run`
  - `schema_version=1.0`
  - `characterization.type=infra_smoke`
  - `characterization.version=1.0`
  - `execution_status=succeeded`
- Runtime-provided observation shape was present for:
  - `final_tp.truth_relation`
  - `trace.primitive_sequence`
  - `final_tp.semantic.isc_category_result`
- Unavailable observations were present:
  - `entropy` (`milestone1_unavailable`)
  - `top_vs_second_margin` (`milestone1_unavailable`)
- EXP4C2 category-result facts:
  - `category_cue=["affective","perspectival"]`
  - `category_weighted_distribution` includes mapped-category entries:
    - `affective`: `probability=0.23667050650980903`, `category_hit=true`
    - `perspectival`: `probability=0.2141483300355984`, `category_hit=true`
  - `top_category="affective"`
  - `category_confidence=0.23667050650980903`
  - `category_rationale=["category_cue_applied","top_category=affective"]`
  - `provenance.source=["sentence","prior_context_cex"]`
  - `provenance.upstream="ce"`
  - `provenance.weights={"w_s":0.35,"w_b":0.25,"w_e":0.2,"w_i":0.2,"w_cat":0.6}`
- Intended cross-source coexistence/provenance check:
  - both intended mapped directions were represented in `category_cue` (`affective` and `perspectival`);
  - mixed source provenance remained observable in `provenance.source` (`sentence` and `prior_context_cex`).
- Trace/truth-relation facts:
  - `truth_relation="declarative"`
  - trace primitive sequence present (`InB`→...→`OuBA`, same primitive list shape as accepted references).
- Bounded reference comparisons (where appropriate):
  - EXP2/EXP4B mapped sentence references show `provenance.source=["sentence"]`;
  - EXP3 mapped prior-context reference shows `provenance.source=["prior_context_cex"]`;
  - EXP4C2 run records both sources together (`["sentence","prior_context_cex"]`).

### 5) Unavailable measurements/deviations

- `entropy` and `top_vs_second_margin` remained unavailable and explicitly marked as unavailable.
- No deviation from approved EXP4C2 fixed controls/identity structure was introduced.

### 6) Unexpected behavior/anomalies

- None observed in this single-run execution.

### 7) Interpretation (bounded)

- Under tested EXP4C2 conditions, this run records cross-source mapped cue coexistence and observable mixed-source provenance in one run with bounded category-result fields.
- This record characterizes a cross-source conflict boundary condition for the current implementation.

### 8) Not established

- No claim is made about which category should win in principle.
- No competition curve, crossover point, or interior strength trajectory is established.
- No threshold/no-category policy is established.
- No stability/generalization claim beyond this case is established.
- No scientific meaning claim is established.

### 9) Questions raised

- Should EXP4C2 be accepted as the current cross-source conflict boundary reference under tested conditions?
- Which retained EXP4 boundary should be authorized next under one-at-a-time review gating?

### 10) Next-step options (suggestions only, not decisions)

- Option A: accept EXP4C2 and authorize next retained EXP4 boundary candidate selection at review gate.
- Option B: request one bounded replay of EXP4C2 run 1 (new run index) before next boundary authorization.
- Option C: accept EXP4C2 and hold further execution pending EXP4 sequence reprioritization.

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
