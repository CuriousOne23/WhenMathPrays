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

## Experiment record — Stage 7 Batch 1 reference ordered response (`cold` / affective) (accepted)

### 1) What executed (exact order)

Batch 1 executed in frozen order under one session identity:

- `B1-1` (`run_index=1`)
- `B1-2` (`run_index=2`)
- `B1-3` (`run_index=3`)
- `B1-4` (`run_index=4`)
- `B1-5` (`run_index=5`)

Execution identity:

- characterization type/version: `infra_smoke/1.0`
- session: `stage7_batch1_reference_cold`

### 2) Inputs and controls used

- Global controls held for all five runs:
  - `enable_category_selection=True`
  - `enable_s2m_seed=False`
- Per-case inputs:
  - `B1-1`: sentence `"The sky is blue."`, prior context `["cold"]`
  - `B1-2`: sentence `"The sky is cold."`, prior context `None`
  - `B1-3`: sentence `"The sky is cold."`, prior context `["cold"]`
  - `B1-4`: sentence `"The sky stays cold."`, prior context `None`
  - `B1-5`: sentence `"The sky is blue."`, prior context `None`

### 3) Produced artifacts/logs (exact paths)

- `B1-1`: `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch1_reference_cold/runs/000001__infra_smoke__1.0.tschar.json`
- `B1-2`: `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch1_reference_cold/runs/000002__infra_smoke__1.0.tschar.json`
- `B1-3`: `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch1_reference_cold/runs/000003__infra_smoke__1.0.tschar.json`
- `B1-4`: `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch1_reference_cold/runs/000004__infra_smoke__1.0.tschar.json`
- `B1-5`: `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch1_reference_cold/runs/000005__infra_smoke__1.0.tschar.json`

### 4) Observed outputs (facts only)

Shared artifact/measurement shape (all five runs):

- `schema_id=ts.characterization.run`
- `schema_version=1.0`
- `characterization.type=infra_smoke`
- `characterization.version=1.0`
- `execution_status=succeeded`
- runtime-provided observations present for:
  - `final_tp.truth_relation`
  - `trace.primitive_sequence`
  - `final_tp.semantic.isc_category_result`
- unavailable observations present:
  - `entropy` (`milestone1_unavailable`)
  - `top_vs_second_margin` (`milestone1_unavailable`)

Case-level observed category-result fields:

- `B1-1` (prior-only):
  - `category_cue=["affective"]`
  - `category_weighted_distribution`:
    - `affective`: `0.2505069933606234`
    - each of `mental`, `metaphysical`, `perceptual`, `perspectival`, `physical`, `social`, `spiritual`: `0.10707042951991096`
  - `top_category="affective"`
  - `category_confidence=0.2505069933606234`
  - `category_rationale=["category_cue_applied","top_category=affective"]`
  - `provenance.source=["prior_context_cex"]`
  - `provenance.upstream="ce"`

- `B1-2` (sentence-only):
  - `category_cue=["affective"]`
  - `category_weighted_distribution`:
    - `affective`: `0.26974629435004127`
    - each of `mental`, `metaphysical`, `perceptual`, `perspectival`, `physical`, `social`, `spiritual`: `0.1043219579499941`
  - `top_category="affective"`
  - `category_confidence=0.26974629435004127`
  - `category_rationale=["category_cue_applied","top_category=affective"]`
  - `provenance.source=["sentence"]`
  - `provenance.upstream="ce"`

- `B1-3` (both sources):
  - `category_cue=["affective"]`
  - `category_weighted_distribution`:
    - `affective`: `0.32171311115883794`
    - each of `mental`, `metaphysical`, `perceptual`, `perspectival`, `physical`, `social`, `spiritual`: `0.09689812697730887`
  - `top_category="affective"`
  - `category_confidence=0.32171311115883794`
  - `category_rationale=["category_cue_applied","top_category=affective"]`
  - `provenance.source=["sentence","prior_context_cex"]`
  - `provenance.upstream="ce"`

- `B1-4` (alternate sentence scaffold):
  - `category_cue=["affective"]`
  - `category_weighted_distribution`:
    - `affective`: `0.26974629435004127`
    - each of `mental`, `metaphysical`, `perceptual`, `perspectival`, `physical`, `social`, `spiritual`: `0.1043219579499941`
  - `top_category="affective"`
  - `category_confidence=0.26974629435004127`
  - `category_rationale=["category_cue_applied","top_category=affective"]`
  - `provenance.source=["sentence"]`
  - `provenance.upstream="ce"`

- `B1-5` (clean non-cue baseline):
  - `category_cue=[]`
  - `category_weighted_distribution`:
    - each of `affective`, `mental`, `metaphysical`, `perceptual`, `perspectival`, `physical`, `social`, `spiritual`: `0.125`
  - `top_category=null`
  - `category_confidence=0.0`
  - `category_rationale=["empty_category_cue","top_category=null"]`
  - `provenance.source=[]`
  - `provenance.upstream="ce"`

Batch-level factual checks from executed artifacts:

- three-point confidence ordering across B1-1/B1-2/B1-3 was observed:
  - `0.2505069933606234 < 0.26974629435004127 < 0.32171311115883794`
- B1-4 relative to B1-2:
  - same cue (`["affective"]`), same source (`["sentence"]`), same top category (`"affective"`), same confidence/distribution values.
- B1-5 remained cue-free (`category_cue=[]`).

### 5) Unavailable measurements/deviations

- Unavailable in all five runs:
  - `entropy`
  - `top_vs_second_margin`
- No recorded deviation from the frozen Batch 1 case identities, ordering, or controls.

### 6) Unexpected behavior/anomalies

- None observed in artifact-recorded Category Selection fields for this batch.
- `trace.primitive_sequence` and `truth_relation` were present in each run (`truth_relation="declarative"` for all five runs).

### 7) Interpretation (bounded)

- Under the tested Stage 7 Batch 1 conditions, recorded artifacts show:
  - observed local three-point ordered response for the reference `cold` affective source-composition condition;
  - one limited alternate-scaffold sentence-only case with matching recorded category-result fields to the canonical sentence-only case;
  - one clean non-cue baseline case with empty cue and null top category.

### 8) Not established

- No entropy- or margin-based interior geometry is established (both unavailable).
- No threshold/no-category policy is established.
- No global axis claim or broader generalization beyond this frozen batch is established.
- No cross-batch authorization or structural-confidence closeout claim is established.

### 9) Questions raised

- Review gate accepted Stage 7 Batch 1 as completed under frozen specification with no triggered stop condition.
- Which (if any) next batch should be authorized separately under one-batch-at-a-time gating?

### 10) Next-step options (suggestions only, not decisions)

- Option A: authorize Batch 2 under separate one-batch-at-a-time gating.
- Option B: request one bounded replay of a selected Batch 1 case using a new run index before Batch 2 execution.
- Option C: hold formal campaign execution after accepted Batch 1 pending review prioritization.

## Experiment record — Stage 7 Batch 2 cross-category generality (`table` / physical; `place` / perspectival) (accepted)

### 1) What executed

- Stage 7 Batch 2 executed as one formal characterization session:
  - `session_id=stage7_batch2_cross_category_generality`
  - `characterization.type=infra_smoke`
  - `characterization.version=1.0`
- Run identities:
  - `B2-1 -> run_index=1`
  - `B2-2 -> run_index=2`
  - `B2-3 -> run_index=3`
  - `B2-4 -> run_index=4`
  - `B2-5 -> run_index=5`
  - `B2-6 -> run_index=6`

### 2) Inputs and controls

- TS-affecting controls for all six runs:
  - `enable_category_selection=True`
  - `enable_s2m_seed=False`
- Physical sequence:
  - `B2-1`: sentence `"The book is on the desk."`, prior context `["table"]`
  - `B2-2`: sentence `"The book is on the table."`, prior context `None`
  - `B2-3`: sentence `"The book is on the table."`, prior context `["table"]`
- Perspectival sequence:
  - `B2-4`: sentence `"The lamp is in the hall."`, prior context `["place"]`
  - `B2-5`: sentence `"The lamp is in the place."`, prior context `None`
  - `B2-6`: sentence `"The lamp is in the place."`, prior context `["place"]`

### 3) Produced artifacts/logs

- `B2-1`:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch2_cross_category_generality/runs/000001__infra_smoke__1.0.tschar.json`
- `B2-2`:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch2_cross_category_generality/runs/000002__infra_smoke__1.0.tschar.json`
- `B2-3`:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch2_cross_category_generality/runs/000003__infra_smoke__1.0.tschar.json`
- `B2-4`:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch2_cross_category_generality/runs/000004__infra_smoke__1.0.tschar.json`
- `B2-5`:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch2_cross_category_generality/runs/000005__infra_smoke__1.0.tschar.json`
- `B2-6`:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch2_cross_category_generality/runs/000006__infra_smoke__1.0.tschar.json`

### 4) Observed outputs — facts only

- Shared artifact fields (all six runs):
  - `schema_id=ts.characterization.run`
  - `schema_version=1.0`
  - `execution_status=succeeded`
  - runtime-provided observations present for:
    - `final_tp.truth_relation`
    - `trace.primitive_sequence`
    - `final_tp.semantic.isc_category_result`
  - `final_tp.truth_relation="declarative"` for all six runs
  - `trace.primitive_sequence` present for all six runs (`InB`→`IIInB`→`IE`→`CEx`→`CE`→`ISc`→`TPU`→`SOB`→`SROB`→`CnOB`→`SmOB`→`SSG`→`RBU`→`RB`→`TR`→`TRU`→`RTU`→`CTP`→`IdOB`→`OuBA`)

- `B2-1` (physical prior-only):
  - `category_cue=["physical"]`
  - full distribution:
    - `physical=0.2505069933606234`
    - `affective=0.10707042951991096`
    - `mental=0.10707042951991096`
    - `metaphysical=0.10707042951991096`
    - `perceptual=0.10707042951991096`
    - `perspectival=0.10707042951991096`
    - `social=0.10707042951991096`
    - `spiritual=0.10707042951991096`
  - `top_category="physical"`
  - `category_confidence=0.2505069933606234`
  - `category_rationale=["category_cue_applied","top_category=physical"]`
  - `provenance.source=["prior_context_cex"]`
  - `provenance.upstream="ce"`

- `B2-2` (physical sentence-only):
  - `category_cue=["physical"]`
  - full distribution:
    - `physical=0.26974629435004127`
    - `affective=0.1043219579499941`
    - `mental=0.1043219579499941`
    - `metaphysical=0.1043219579499941`
    - `perceptual=0.1043219579499941`
    - `perspectival=0.1043219579499941`
    - `social=0.1043219579499941`
    - `spiritual=0.1043219579499941`
  - `top_category="physical"`
  - `category_confidence=0.26974629435004127`
  - `category_rationale=["category_cue_applied","top_category=physical"]`
  - `provenance.source=["sentence"]`
  - `provenance.upstream="ce"`

- `B2-3` (physical both-source):
  - `category_cue=["physical"]`
  - full distribution:
    - `physical=0.32171311115883794`
    - `affective=0.09689812697730887`
    - `mental=0.09689812697730887`
    - `metaphysical=0.09689812697730887`
    - `perceptual=0.09689812697730887`
    - `perspectival=0.09689812697730887`
    - `social=0.09689812697730887`
    - `spiritual=0.09689812697730887`
  - `top_category="physical"`
  - `category_confidence=0.32171311115883794`
  - `category_rationale=["category_cue_applied","top_category=physical"]`
  - `provenance.source=["sentence","prior_context_cex"]`
  - `provenance.upstream="ce"`

- Physical ordering facts from artifacts:
  - target-category distribution/confidence values:
    `0.2505069933606234 < 0.26974629435004127 < 0.32171311115883794`
  - corresponding source-state order:
    `prior-only < sentence-only < both`

- `B2-4` (perspectival prior-only):
  - `category_cue=["perspectival"]`
  - full distribution:
    - `perspectival=0.2505069933606234`
    - `affective=0.10707042951991096`
    - `mental=0.10707042951991096`
    - `metaphysical=0.10707042951991096`
    - `perceptual=0.10707042951991096`
    - `physical=0.10707042951991096`
    - `social=0.10707042951991096`
    - `spiritual=0.10707042951991096`
  - `top_category="perspectival"`
  - `category_confidence=0.2505069933606234`
  - `category_rationale=["category_cue_applied","top_category=perspectival"]`
  - `provenance.source=["prior_context_cex"]`
  - `provenance.upstream="ce"`

- `B2-5` (perspectival sentence-only):
  - `category_cue=["perspectival"]`
  - full distribution:
    - `perspectival=0.26974629435004127`
    - `affective=0.1043219579499941`
    - `mental=0.1043219579499941`
    - `metaphysical=0.1043219579499941`
    - `perceptual=0.1043219579499941`
    - `physical=0.1043219579499941`
    - `social=0.1043219579499941`
    - `spiritual=0.1043219579499941`
  - `top_category="perspectival"`
  - `category_confidence=0.26974629435004127`
  - `category_rationale=["category_cue_applied","top_category=perspectival"]`
  - `provenance.source=["sentence"]`
  - `provenance.upstream="ce"`

- `B2-6` (perspectival both-source):
  - `category_cue=["perspectival"]`
  - full distribution:
    - `perspectival=0.32171311115883794`
    - `affective=0.09689812697730887`
    - `mental=0.09689812697730887`
    - `metaphysical=0.09689812697730887`
    - `perceptual=0.09689812697730887`
    - `physical=0.09689812697730887`
    - `social=0.09689812697730887`
    - `spiritual=0.09689812697730887`
  - `top_category="perspectival"`
  - `category_confidence=0.32171311115883794`
  - `category_rationale=["category_cue_applied","top_category=perspectival"]`
  - `provenance.source=["sentence","prior_context_cex"]`
  - `provenance.upstream="ce"`

- Perspectival ordering facts from artifacts:
  - target-category distribution/confidence values:
    `0.2505069933606234 < 0.26974629435004127 < 0.32171311115883794`
  - corresponding source-state order:
    `prior-only < sentence-only < both`

### 5) Unavailable measurements/deviations

- Unavailable in all six runs:
  - `entropy`
  - `top_vs_second_margin`
- No deviation from the frozen Batch 2 case identities, ordering, or run-index mapping was recorded.

### 6) Unexpected behavior/anomalies

- The six formal Batch 2 `.tschar.json` artifacts do not include token-class-level `UNK` flags or `constraint_residue`/`semantic_adjacent_cues`/`smoothing_residue` fields.
- Therefore, from this artifact-only evidence set, no additional structural anomaly claim is asserted beyond the recorded truth-relation and primitive-sequence facts.

### 7) Interpretation — bounded

- Under the tested Palette v1 conditions, the local weighted source-composition ordering previously observed for affective/`cold` was also observed for physical/`table` and perspectival/`place`.
- This provides first-order cross-category generality evidence for the tested local source-composition response across the three canonical Palette v1 category realizations when considered together with accepted Batch 1.

### 8) Not established

- No global Category Selection behavior is established.
- No globally valid evidence-strength axis is established.
- No continuous gradients are established.
- No fine interior geometry is established.
- No entropy-based ambiguity behavior is established.
- No top-versus-second-margin behavior is established.
- No broad construction invariance is established.
- No competition behavior is established.
- No deeper representability/support-edge behavior is established.
- No generalization outside the tested canonical Palette v1 category identities is established.
- No Category Selection structural-confidence closeout is established.
- No claim is made that Batch 2 alone is sufficient evidence to advance TS.
- Batch 3 authorization is not established by this record.

### 9) Questions raised

- Review gate accepted Stage 7 Batch 2 as completed under frozen specification with no triggered stop condition.
- Batch 3 is separately authorized; Batch 4A remains unauthorized pending a separate review-gate decision.

### 10) Next-step options — suggestions only, not decisions

- Option A: authorize Batch 3 under separate one-batch-at-a-time gating.
- Option B: request one bounded replay of a selected Batch 2 case using a new run index before Batch 3 execution.
- Option C: hold formal campaign execution after accepted Batch 2 pending review prioritization.

## Experiment record — Stage 7 Batch 3 robustness + competition (`table` / physical; `place` / perspectival; mixed competition pairs) (accepted)

### 1) What executed

- Stage 7 Batch 3 executed as one formal characterization session:
  - `session_id=stage7_batch3_robustness_competition`
  - `characterization.type=infra_smoke`
  - `characterization.version=1.0`
- Run identities:
  - `B3-1 -> run_index=1`
  - `B3-2 -> run_index=2`
  - `B3-3 -> run_index=3`
  - `B3-4 -> run_index=4`
  - `B3-5 -> run_index=5`

### 2) Inputs and controls

- TS-affecting controls for all five runs:
  - `enable_category_selection=True`
  - `enable_s2m_seed=False`
- Robustness cases:
  - `B3-1`: sentence `"The book rests on the table."`, prior context `["table"]`
  - `B3-2`: sentence `"The lamp stays in the place."`, prior context `["place"]`
- Competition cases:
  - `B3-3`: sentence `"The book is on the table."`, prior context `["cold"]`
  - `B3-4`: sentence `"The lamp is in the place."`, prior context `["cold"]`
  - `B3-5`: sentence `"The lamp is in the place."`, prior context `["table"]`

### 3) Produced artifacts/logs

- `B3-1`:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch3_robustness_competition/runs/000001__infra_smoke__1.0.tschar.json`
- `B3-2`:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch3_robustness_competition/runs/000002__infra_smoke__1.0.tschar.json`
- `B3-3`:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch3_robustness_competition/runs/000003__infra_smoke__1.0.tschar.json`
- `B3-4`:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch3_robustness_competition/runs/000004__infra_smoke__1.0.tschar.json`
- `B3-5`:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch3_robustness_competition/runs/000005__infra_smoke__1.0.tschar.json`

### 4) Observed outputs — facts only

- Shared artifact fields (all five runs):
  - `schema_id=ts.characterization.run`
  - `schema_version=1.0`
  - `execution_status=succeeded`
  - `final_tp.truth_relation="declarative"`
  - `trace.primitive_sequence` present with the same sequence as accepted Batch 2

- `B3-1` (physical alternate scaffold, both-source):
  - `category_cue=["physical"]`
  - full distribution:
    - `physical=0.32171311115883794`
    - `affective=0.09689812697730887`
    - `mental=0.09689812697730887`
    - `metaphysical=0.09689812697730887`
    - `perceptual=0.09689812697730887`
    - `perspectival=0.09689812697730887`
    - `social=0.09689812697730887`
    - `spiritual=0.09689812697730887`
  - `top_category="physical"`
  - `category_confidence=0.32171311115883794`
  - `category_rationale=["category_cue_applied","top_category=physical"]`
  - `provenance.source=["sentence","prior_context_cex"]`

- `B3-2` (perspectival alternate scaffold, both-source):
  - `category_cue=["perspectival"]`
  - full distribution:
    - `perspectival=0.32171311115883794`
    - `affective=0.09689812697730887`
    - `mental=0.09689812697730887`
    - `metaphysical=0.09689812697730887`
    - `perceptual=0.09689812697730887`
    - `physical=0.09689812697730887`
    - `social=0.09689812697730887`
    - `spiritual=0.09689812697730887`
  - `top_category="perspectival"`
  - `category_confidence=0.32171311115883794`
  - `category_rationale=["category_cue_applied","top_category=perspectival"]`
  - `provenance.source=["sentence","prior_context_cex"]`

- Mandatory robustness gate comparisons (factual):
  - `B3-1` vs accepted `B2-3`: cue/provenance/top/distribution/confidence matched.
  - `B3-2` vs accepted `B2-6`: cue/provenance/top/distribution/confidence matched.

- `B3-3` (affective + physical competition):
  - `category_cue=["affective","physical"]`
  - full distribution:
    - `physical=0.23667050650980903`
    - `affective=0.2141483300355984`
    - `mental=0.09153019390909874`
    - `metaphysical=0.09153019390909874`
    - `perceptual=0.09153019390909874`
    - `perspectival=0.09153019390909874`
    - `social=0.09153019390909874`
    - `spiritual=0.09153019390909874`
  - `top_category="physical"`
  - `category_confidence=0.23667050650980903`
  - `category_rationale=["category_cue_applied","top_category=physical"]`
  - `provenance.source=["sentence","prior_context_cex"]`

- `B3-4` (affective + perspectival competition):
  - `category_cue=["affective","perspectival"]`
  - full distribution:
    - `perspectival=0.23667050650980903`
    - `affective=0.2141483300355984`
    - `mental=0.09153019390909874`
    - `metaphysical=0.09153019390909874`
    - `perceptual=0.09153019390909874`
    - `physical=0.09153019390909874`
    - `social=0.09153019390909874`
    - `spiritual=0.09153019390909874`
  - `top_category="perspectival"`
  - `category_confidence=0.23667050650980903`
  - `category_rationale=["category_cue_applied","top_category=perspectival"]`
  - `provenance.source=["sentence","prior_context_cex"]`

- `B3-5` (physical + perspectival competition):
  - `category_cue=["perspectival","physical"]`
  - full distribution:
    - `perspectival=0.23667050650980903`
    - `physical=0.2141483300355984`
    - `affective=0.09153019390909874`
    - `mental=0.09153019390909874`
    - `metaphysical=0.09153019390909874`
    - `perceptual=0.09153019390909874`
    - `social=0.09153019390909874`
    - `spiritual=0.09153019390909874`
  - `top_category="perspectival"`
  - `category_confidence=0.23667050650980903`
  - `category_rationale=["category_cue_applied","top_category=perspectival"]`
  - `provenance.source=["sentence","prior_context_cex"]`

### 5) Unavailable measurements/deviations

- Unavailable in all five runs:
  - `entropy`
  - `top_vs_second_margin`
- No deviation from the frozen Batch 3 case identities, session/run mapping, or artifact identity contract was recorded.

### 6) Unexpected behavior/anomalies

- No Batch 3 predefined stop condition was triggered in the formal execution record.
- As with Batch 2 `infra_smoke` artifacts, no additional token-class-level `UNK`, `constraint_residue`, `semantic_adjacent_cues`, or `smoothing_residue` fields are present in these five `.tschar.json` records.

### 7) Interpretation — bounded

- Under tested Palette v1 conditions, one alternate scaffold for physical both-source and one alternate scaffold for perspectival both-source produced recorded cue/provenance/top/distribution/confidence values matching accepted canonical both-source references (`B2-3`, `B2-6`).
- Under tested Palette v1 conditions, the three frozen mixed-source competition cases produced interpretable two-direction outputs with intended cue pairs and mixed-source provenance.

### 8) Not established

- No global competition hierarchy is established.
- No general sentence-over-prior or prior-over-sentence rule is established.
- No competition gradient/crossover geometry is established.
- No entropy-based ambiguity or top-versus-second-margin behavior is established.
- No global Category Selection behavior is established.
- No broad robustness/generalization claim outside tested Batch 3 conditions is established.
- No Category Selection structural-confidence closeout is established.
- Batch 4A authorization is not established by Batch 3 evidence alone.

### 9) Questions raised

- Review gate accepted Stage 7 Batch 3 as completed under frozen specification with no triggered stop condition.
- Should Batch 4A be separately authorized under one-batch-at-a-time gating?

### 10) Next-step options — suggestions only, not decisions

- Option A: authorize Batch 4A under separate one-batch-at-a-time gating.
- Option B: request one bounded replay of a selected Batch 3 competition case using a new run index before Batch 4A decision.
- Option C: hold campaign progression after accepted Batch 3 pending review prioritization.

## Experiment record — Stage 7 Batch 4A clean representability boundary (`cold` mapped baseline; `blue` matched unmapped control) (executed, pending review-gate decision)

### 1) What executed

- Stage 7 Batch 4A executed as one formal characterization session:
  - `session_id=stage7_batch4a_clean_representability`
  - `characterization.type=infra_smoke`
  - `characterization.version=1.0`
- Run identities:
  - `B4A-1 -> run_index=1`
  - `B4A-2 -> run_index=2`

### 2) Inputs and controls

- TS-affecting controls for both runs:
  - `enable_category_selection=True`
  - `enable_s2m_seed=False`
- Cases:
  - `B4A-1`: sentence `"The sky is cold."`, prior context `None`
  - `B4A-2`: sentence `"The sky is blue."`, prior context `None`

### 3) Produced artifacts/logs

- `B4A-1`:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch4a_clean_representability/runs/000001__infra_smoke__1.0.tschar.json`
- `B4A-2`:
  `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/stage7_batch4a_clean_representability/runs/000002__infra_smoke__1.0.tschar.json`

### 4) Observed outputs — facts only

- Shared artifact fields (both runs):
  - `schema_id=ts.characterization.run`
  - `schema_version=1.0`
  - `execution_status=succeeded`
  - `final_tp.truth_relation="declarative"`
  - `trace.primitive_sequence` present with the standard sequence

- `B4A-1` (mapped baseline):
  - `category_cue=["affective"]`
  - full distribution:
    - `affective=0.26974629435004127`
    - `mental=0.1043219579499941`
    - `metaphysical=0.1043219579499941`
    - `perceptual=0.1043219579499941`
    - `perspectival=0.1043219579499941`
    - `physical=0.1043219579499941`
    - `social=0.1043219579499941`
    - `spiritual=0.1043219579499941`
  - `top_category="affective"`
  - `category_confidence=0.26974629435004127`
  - `category_rationale=["category_cue_applied","top_category=affective"]`
  - `provenance.source=["sentence"]`
  - `provenance.upstream="ce"`

- `B4A-2` (matched unmapped control):
  - `category_cue=[]`
  - full distribution:
    - `affective=0.125`
    - `mental=0.125`
    - `metaphysical=0.125`
    - `perceptual=0.125`
    - `perspectival=0.125`
    - `physical=0.125`
    - `social=0.125`
    - `spiritual=0.125`
  - `top_category=null`
  - `category_confidence=0.0`
  - `category_rationale=["empty_category_cue","top_category=null"]`
  - `provenance.source=[]`
  - `provenance.upstream="ce"`

- Required mapped/unmapped comparison (factual):
  - cue, full distribution, top category, confidence, rationale, and provenance are distinguishable between `B4A-1` and `B4A-2`.

### 5) Unavailable measurements/deviations

- Unavailable in both runs:
  - `entropy`
  - `top_vs_second_margin`
- No deviation from frozen Batch 4A case identities or run-index mapping was recorded.

### 6) Unexpected behavior/anomalies

- No Batch 4A stop condition was triggered in the formal execution record.
- As with prior `infra_smoke` artifacts, no additional token-class-level `UNK`, `constraint_residue`, `semantic_adjacent_cues`, or `smoothing_residue` fields are present in these two `.tschar.json` records.

### 7) Interpretation — bounded

- Under tested frozen Palette v1 conditions, Batch 4A produced a clean local mapped/unmapped representability boundary between `cold` (mapped affective cue present) and matched `blue` control (no category cue, null top category).

### 8) Not established

- No global representability boundary is established.
- No threshold/no-category policy is established beyond the observed local batch cases.
- No entropy- or margin-based interior geometry is established.
- No Category Selection structural-confidence closeout is established.
- Batch 4B authorization is not established by Batch 4A evidence.

### 9) Questions raised

- Should Stage 7 Batch 4A be accepted at review gate under the frozen specification?
- Should Batch 4B remain deferred pending separate review-gate direction?

### 10) Next-step options — suggestions only, not decisions

- Option A: review and decide Batch 4A acceptance at review gate.
- Option B: request one bounded replay of a selected Batch 4A case using a new run index before acceptance decision.
- Option C: hold campaign progression after Batch 4A execution pending review prioritization.

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
