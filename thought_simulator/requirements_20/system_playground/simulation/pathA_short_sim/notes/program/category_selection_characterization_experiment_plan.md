# Category Selection Characterization Experiment Plan

**Document:** notes/program/category_selection_characterization_experiment_plan.md  
**Status:** Controlled execution plan for characterization experiments (non-normative).  
**Date:** 2026-11-22

## 1) Purpose and scope

This document is the execution-control plan for running category-selection characterization experiments with the currently implemented Milestone-1 infrastructure.

It defines how to execute experiments sequentially under mandatory review gates:

**observe -> characterize -> review -> decide next experiment**

This document does not replace research/reference authority and does not pre-commit scientific conclusions.

## 2) Authoritative/reference documents and roles

- [category_selection_index.md](category_selection_index.md): document routing/ownership.
- [category_selection_research_plan.md](category_selection_research_plan.md): research questions, principles, and experiment-family framing.
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md): characterization method/contract boundaries.
- [category_selection_program_reference.md](category_selection_program_reference.md): realization-side contract boundaries.
- [category_selection_characterization_milestone1_closeout.md](category_selection_characterization_milestone1_closeout.md): what Milestone-1 infrastructure actually established.
- [category_selection_observation.md](category_selection_observation.md): destination for empirical findings after evidence review.
- [user_guide.md](../../user_guide.md): operator workflow guidance.

Normative behavior/ownership remain in requirements documents referenced by the research/reference set above.

## 3) Experimental invariants

Every experiment in this campaign must preserve:

- characterization observes normal selected TS execution; it does not define an alternate meaning path;
- characterization does not own or silently alter TS-affecting controls;
- one characterization invocation performs one TS execution;
- canonical identity is `(session_id, run_index)`; successful evidence for an identity is not silently overwritten;
- `.tschar.json` is success-only machine-readable evidence;
- unavailable measurements must remain explicitly unavailable (not fabricated);
- category-result evidence is not equivalent to meaning selection by itself;
- Level-A behavior comparison exclusions are limited to approved non-behavioral metadata (`created_at_utc` only unless authority changes).

## 4) Explicit prohibited actions

The executing agent must not:

- change production/category-selection behavior to improve experiment outcomes;
- invent/tune thresholds or introduce a no-category decision rule without existing authority;
- silently repair unexpected behavior;
- fabricate unavailable measurements;
- treat category result as meaning conclusion;
- convert observations into pass/fail claims without a stated criterion;
- proceed automatically from Experiment N to Experiment N+1;
- broaden campaign scope into orchestration or new characterization types.

Unexpected behavior is evidence to report, not an automatic bug-fix directive.

## 5) Current implemented capability boundary (execution-relevant)

Current experiment execution is bounded to implemented capabilities:

- entrypoint: `run_examples.py`;
- execution case currently supported for controlled baseline: `--execution-case sky_blue`;
- execution controls available: `--enable-category-selection`, `--no-s2m-seed`, `--no-category-observations`;
- characterization controls available: `--characterize`, `--char-type`, `--char-session-id`, `--char-run-index`, `--char-version`, `--char-params-json`, `--char-params-file`;
- characterization type currently implemented for this campaign: `infra_smoke` (version `1.0`);
- success evidence location pattern:
  `local_characterization/sessions/<session_id>/runs/<run_index>__<type>__<version>.tschar.json`;
- stdout may include one final `=== CHAR TRACE ===` block per controlled characterization invocation;
- raw argparse type rejection can exit before CHAR TRACE.

## 6) Execution and artifact-recording procedure

For each experiment:

1. Define experiment ID, objective, and controlled variables before execution.
2. Declare exact command(s) and expected artifact identity `(session_id, run_index)`.
3. Run commands exactly as specified; do not edit runtime code/config as part of experiment execution.
4. Record:
   - command line(s),
   - exit code(s),
   - run.log path(s) when redirected,
   - CHAR TRACE status/pointer behavior (if applicable),
   - committed `.tschar.json` path(s) when successful.
5. Parse evidence only from produced runtime outputs/artifacts.
6. Record unavailable measurements explicitly as unavailable.
7. Preserve raw evidence long enough for review; clean only test-specific local outputs after review approval.

## 7) Campaign-level queue / roadmap (provisional beyond Experiment 1)

- **Experiment 1 (accepted):** smallest no-cue/baseline characterization (completed and accepted at review gate).
- **Experiment 2 (accepted):** smallest sentence-internal-cue comparison against Experiment 1 baseline (completed and accepted at review gate).
- **Experiment 3 (accepted):** smallest prior-context cue/provenance comparison against accepted EXP1/EXP2 references (completed and accepted at review gate).
- **Experiment 4 (proposed boundary family):** EXP4A, EXP4B, EXP4C1, EXP4C2, EXP4D initial boundary-characterization set (proposal/review only; not execution-authorized by default).
- **Experiment 5 (provisional):** interior characterization families (including supporting-evidence, ambiguity/competition, and weakening trajectories) after boundary-family review.

Only one experiment is execution-authorized at a time by explicit review-gate approval. Provisional roadmap items may be changed, deferred, replaced, or canceled after each review.

## 8) Standardized per-experiment specification template

Each experiment spec must include:

1. **Experiment ID and title**
2. **Objective (observation question, not conclusion)**
3. **Inputs/cases** (exact sentence/case/context)
4. **TS-affecting controls** (explicit values)
5. **Characterization controls** (type/session/run/version/params)
6. **Command(s)** (verbatim)
7. **Expected evidence surfaces** (`run.log`, CHAR TRACE, `.tschar.json`)
8. **Planned comparisons** (if any), including approved exclusions
9. **Stop/escalation triggers specific to this experiment**

## 9) Standardized result/observation record template

After execution, report:

1. **What executed** (exact commands, times/order)
2. **Inputs and controls used**
3. **Produced artifacts/logs** (exact paths)
4. **Observed outputs** (facts only)
5. **Unavailable measurements/deviations**
6. **Unexpected behavior/anomalies**
7. **Interpretation (bounded)**
8. **Not established**
9. **Questions raised**
10. **Next-step options** (suggestions, not decisions)

## 10) Mandatory review gate after every experiment

After each experiment, the executing agent must stop and present:

- what was executed;
- exact cases/inputs and controls;
- generated artifacts;
- observed results;
- unavailable/deviating measurements;
- unexpected behavior;
- questions raised;
- suggested next steps (clearly labeled as suggestions).

No further experiment may run without explicit authorization.

## 11) Rules for changing later experiments

After review, the next experiment may be:

- **continued** as drafted,
- **modified** (controls/cases narrowed or expanded),
- **repeated** (for replay/confirmation),
- **replaced** (if prior assumptions were invalid),
- **deferred/canceled** (if no longer relevant).

Any such decision must be tied to observed evidence from prior experiments, not prewritten campaign momentum.

## 11A) Verification-run flexibility (off-plan, bounded)

The formal campaign plan does not require every bounded diagnostic/verification run to be preplanned as a numbered experiment.

When explicitly requested during review, bounded off-plan verification runs may be executed to investigate a specific observation while preserving stated controls and stopping at review.

Rules:

- off-plan verification runs must remain narrow and evidence-driven;
- off-plan verification runs must preserve applicable control discipline and identity reporting;
- off-plan verification runs must stop at review (no automatic continuation);
- if an off-plan verification result materially changes interpretation, continuity, or next-step direction, record the accepted finding in [category_selection_observation.md](category_selection_observation.md) and add a concise retrospective note here as directed;
- routine verification that does not materially affect the research record does not by itself require campaign-plan expansion.

## 12) Stop/escalation conditions

Stop and escalate for review when any of the following occur:

- unexpected behavior that could indicate implementation ambiguity;
- missing capability needed for planned measurement;
- nondeterminism outside approved exclusions;
- apparent contradiction with governing documents;
- CHAR TRACE/artifact mismatch (for example, pointer does not correspond to committed artifact);
- identity/overwrite behavior diverges from expected safeguards;
- inability to preserve one-run-per-invocation discipline;
- requirement to change runtime behavior merely to continue experiments.

Escalation report must separate:

- observed fact,
- possible interpretations,
- requested decision.

## 13) Experiment 1 — fully specified (smallest useful no-cue baseline)

### 13.1 Objective

Establish an initial no-cue baseline characterization for the canonical `sky_blue` execution under controlled settings, confirming the current infrastructure records baseline runtime observations without asserting scientific category-policy conclusions.

### 13.2 Cases and controls

- Execution case: `sky_blue`
- Characterization type/version: `infra_smoke` / default (`1.0`)
- TS-affecting controls:
  - `--execution-case sky_blue`
  - `--enable-category-selection`
  - `--no-s2m-seed`
  - `--no-category-observations`
  - prior context: none (by selected execution case)
- Characterization identity:
  - `--char-session-id exp1_baseline`
  - `--char-run-index 1`

### 13.3 Command

```
python run_examples.py --execution-case sky_blue --enable-category-selection --no-category-observations --no-s2m-seed --characterize --char-type infra_smoke --char-session-id exp1_baseline --char-run-index 1 > run.log
```

### 13.4 Required evidence to capture

- command used exactly as run;
- exit code;
- `run.log` with normal TS output and one final CHAR TRACE block;
- CHAR TRACE success pointer path;
- committed artifact at:
  `local_characterization/sessions/exp1_baseline/runs/000001__infra_smoke__1.0.tschar.json`;
- artifact fields confirming runtime-provided/unavailable provenance behavior.

### 13.5 Allowed interpretation scope

- Allowed: describe observed baseline evidence and availability/unavailability state.
- Not allowed: infer threshold/no-category policy, support-boundary conclusions, or scientific conclusions.

### 13.6 Mandatory stop

After Experiment 1 record is prepared, stop and wait for explicit reviewer authorization before running any additional experiment.

## 14) Experiment review ledger

- **EXP1 status:** executed and accepted at review gate.
- **Accepted evidence summary:** one successful characterized baseline run (`exp1_baseline`, run 1) with committed artifact and expected no-cue baseline fields.
- **EXP2 status:** executed and accepted at review gate.
- **Accepted evidence summary:** one successful sentence-internal-cue characterization run (`exp2_sentence_internal`, run 1) with committed artifact, available runtime observations, explicit unavailable measurements, and bounded fact-level differences versus EXP1.
- **EXP3 status:** executed and accepted at review gate.
- **Accepted evidence summary:** one successful prior-context cue/provenance characterization run (`exp3_prior_context`, run 1) with committed artifact and bounded provenance-source contrast versus accepted EXP1 (`[]`) and EXP2 (`["sentence"]`) references.
- **Gate decision for next step:** propose EXP4 for review (do not fully commit/execute EXP4 until explicitly authorized).

## 15) Experiment 2 — fully specified (smallest useful sentence-internal-cue comparison)

### 15.1 Objective

Produce the smallest sentence-internal-cue characterization record that can be compared to EXP1 baseline while preserving identical TS-affecting controls where applicable.

### 15.2 Capability boundary used

Current `run_examples.py` characterization CLI exposes `--execution-case sky_blue` only. Therefore sentence-internal-cue comparison for `"Where is the book?"` is executed through currently implemented in-process APIs (no simulator behavior edits):

- `run_pathA_short(...)` for selected sentence execution,
- `run_examples.run_characterization_once(...)` for `infra_smoke` evidence capture/persistence.

### 15.3 Cases and controls

- Baseline reference: EXP1 artifact (`exp1_baseline`, run 1).
- Sentence-under-test: `"Where is the book?"` (sentence-internal cue path).
- TS-affecting controls for EXP2 execution:
  - `enable_category_selection=True`
  - `enable_s2m_seed=False`
  - `prior_context=None`
- Characterization controls:
  - type/version: `infra_smoke` / `1.0`
  - identity: `session_id=exp2_sentence_internal`, `run_index=1`

### 15.4 Command (implementation-aligned in-process execution)

Run in repository environment:

```
python -c "import sys; from pathlib import Path; p=Path('thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim').resolve(); sys.path.insert(0,str(p)); import run_examples as rx; from characterization.dispatcher import resolve_characterization; sim=rx.run_pathA_short('Where is the book?', enable_s2m_seed=False, enable_category_selection=True, prior_context=None); resolved=resolve_characterization('infra_smoke', None); req={'type':resolved['type'],'version':resolved['version'],'session_id':'exp2_sentence_internal','run_index':1,'resolved_type_parameters':resolved['params_resolver']({}),'runner':resolved['runner']}; result=rx.run_characterization_once(req, sim, {'execution_case':'sentence_internal_where_book','enable_category_selection':True,'enable_s2m_seed':False,'show_category_observations':False,'prior_context':None}); print(result['persistence']['committed_final_path'])"
```

### 15.5 Required evidence to capture

- exact command used;
- exit code;
- committed artifact path for `exp2_sentence_internal` run 1;
- artifact identity/type/version/schema/execution status;
- runtime-provided observations (including `final_tp.semantic.isc_category_result`);
- unavailable observations (`entropy`, `top_vs_second_margin`);
- bounded comparison notes versus EXP1 baseline artifact (fact-level differences only).

### 15.6 Planned baseline comparison focus (bounded)

Compare EXP2 artifact against EXP1 on:

- presence/shape of runtime and unavailable provenance sections;
- `final_tp.semantic.isc_category_result` cue/result fields;
- trace primitive sequence presence.

Do not infer threshold/policy conclusions from this single comparison.

### 15.7 Stop/escalation triggers (EXP2-specific)

Stop and escalate if:

- in-process execution cannot persist a valid artifact for the requested identity;
- produced artifact identity/path does not match requested `(session_id, run_index)`;
- expected runtime-provided observation fields are missing;
- unavailable observations are fabricated rather than marked unavailable;
- behavior suggests more than one TS execution for one characterization invocation.

### 15.8 Mandatory stop

After EXP2 execution record is prepared, stop at review gate and wait for explicit authorization before any EXP3 work.

## 16) Experiment 3 — fully specified (smallest useful prior-context cue/provenance reference)

### 16.1 Objective

Produce the smallest prior-context-driven characterization record that establishes a clean prior-context provenance reference point for bounded comparison with accepted EXP1 (no-cue baseline) and EXP2 (sentence-internal cue).

### 16.2 Capability boundary used

Current `run_examples.py` characterization CLI exposes `--execution-case sky_blue` only and does not expose a CLI flag for custom prior context. Therefore EXP3 uses currently implemented in-process APIs (no simulator behavior edits):

- `run_pathA_short(...)` for selected sentence execution with explicit `prior_context`,
- `run_examples.run_characterization_once(...)` for `infra_smoke` evidence capture/persistence.

### 16.3 Cases and controls

- Baseline references:
  - EXP1 artifact (`exp1_baseline`, run 1)
  - EXP2 artifact (`exp2_sentence_internal`, run 1)
- Sentence-under-test for EXP3: `"The sky is blue."`
- Prior context for EXP3: `["location"]`
- TS-affecting controls for EXP3 execution:
  - `enable_category_selection=True`
  - `enable_s2m_seed=False`
  - `prior_context=["location"]`
- Characterization controls:
  - type/version: `infra_smoke` / `1.0`
  - identity: `session_id=exp3_prior_context`, `run_index=1`

### 16.4 Command (implementation-aligned in-process execution)

Run in repository environment:

```
python -c "import sys; from pathlib import Path; p=Path('thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim').resolve(); sys.path.insert(0,str(p)); import run_examples as rx; from characterization.dispatcher import resolve_characterization; sim=rx.run_pathA_short('The sky is blue.', enable_s2m_seed=False, enable_category_selection=True, prior_context=['location']); resolved=resolve_characterization('infra_smoke', None); req={'type':resolved['type'],'version':resolved['version'],'session_id':'exp3_prior_context','run_index':1,'resolved_type_parameters':resolved['params_resolver']({}),'runner':resolved['runner']}; result=rx.run_characterization_once(req, sim, {'execution_case':'sky_blue_prior_context_location','enable_category_selection':True,'enable_s2m_seed':False,'show_category_observations':False,'prior_context':['location']}); print(result['persistence']['committed_final_path'])"
```

### 16.5 Required evidence to capture

- exact command used;
- exit code;
- committed artifact path for `exp3_prior_context` run 1;
- artifact identity/type/version/schema/execution status;
- runtime-provided observations (including `final_tp.semantic.isc_category_result`);
- provenance observations from `final_tp.semantic.isc_category_result.value.provenance`, including `source` and upstream/weights fields;
- unavailable observations (`entropy`, `top_vs_second_margin`);
- bounded fact-level comparison notes versus accepted EXP1 and EXP2 artifacts.

### 16.6 Planned comparison focus (bounded)

Compare EXP3 against accepted references on:

- runtime/unavailable observation section presence/shape;
- `final_tp.semantic.isc_category_result` cue/result fields;
- provenance source distinctions:
  - EXP1 expected no cue source (`[]`) baseline;
  - EXP2 observed sentence-driven source (includes `"sentence"`);
  - EXP3 prior-context reference (expected prior-context-driven source path);
- trace primitive sequence presence.

Interpret EXP2↔EXP3 numeric/category differences as potentially confounded by sentence/truth-relation differences (`"Where is the book?"` interrogative vs `"The sky is blue."` declarative); treat provenance-source contrast as the primary controlled comparison target.

Do not infer threshold/no-category policy, support-boundary conclusions, or scientific meaning conclusions from this single EXP3 run.

### 16.7 Unavailable measurements

Treat `entropy` and `top_vs_second_margin` as expected unavailable Milestone-1 measurements unless implementation authority changes.

### 16.8 Stop/escalation triggers (EXP3-specific)

Stop and escalate if:

- in-process execution cannot persist a valid artifact for `(session_id=exp3_prior_context, run_index=1)`;
- produced artifact identity/path does not match requested identity;
- expected runtime-provided observation fields are missing;
- unavailable measurements are fabricated instead of marked unavailable;
- `isc_category_result` provenance fields required for source comparison are missing;
- behavior suggests more than one TS execution for one characterization invocation;
- execution would require runtime/category-selection behavior modification to proceed.

### 16.9 Mandatory review gate

After EXP3 execution record is prepared, stop at review gate and wait for explicit authorization before any EXP4 or off-plan follow-up run.

## 17) EXP4 boundary-characterization family (proposed; review-only)

### 17.1 Phase direction (research-ordering decision)

Next-phase priority is boundary characterization of the currently tractable system before interior-shape characterization (curve/geometry/gradients/competition trajectories).

Boundary characterization asks where currently observable Category Selection behavior/capability reaches materially distinct edges or limiting conditions. It does not introduce threshold/no-category policy design.

### 17.2 Execution authority constraint

EXP4A, EXP4B, EXP4C1, EXP4C2, and EXP4D below are proposed boundary subexperiments. Fully describing them does not authorize execution.

- Execute at most one authorized subexperiment at a time.
- After each execution, stop at review gate.
- Later EXP4 items may be modified/reordered/replaced/deferred based on accepted earlier EXP4 evidence.

### 17.3 Common control discipline for EXP4 family

Unless a specific subexperiment explicitly states otherwise, hold fixed:

- characterization type/version: `infra_smoke` / `1.0`;
- one characterization invocation per run;
- `enable_s2m_seed=False`;
- identical artifact identity/reporting discipline and review-gate reporting template.

Do not change runtime/category-selection implementation to make EXP4 convenient.

### 17.4 EXP4A (proposed) — prior-context representability boundary

1. **Boundary question:** Does prior-context evidence move from representable/usable to non-represented/non-usable when prior-context marker content is changed while the utterance and controls remain fixed?
2. **Why boundary:** This isolates the edge between mappable and unmappable prior-context evidence in current implementation.
3. **Relationship to EXP1–EXP3:** Anchors against accepted EXP3 prior-context source reference and EXP1 no-cue baseline.
4. **Variable/condition changed:** prior-context marker content only.
5. **Controls fixed:** same utterance (recommended: `"The sky is blue."`), `enable_category_selection=True`, `enable_s2m_seed=False`.
6. **Current capability:** `run_pathA_short(..., prior_context=[...])` plus current prior-context cue mappings in [category_cues.yaml](../../support/dictionaries/category_cues.yaml) (for example mapped `location` vs currently unmapped `place`).
7. **Evidence surfaces:** `.tschar.json` identity/status; `final_tp.semantic.isc_category_result`; provenance/source fields; unavailable block.
8. **Known confounds/limitations:** marker matching is substring-based lexical matching; does not test synonym handling beyond current dictionary.
9. **Could legitimately inform:** observable prior-context representability boundary under controlled inputs.
10. **Cannot establish:** global boundary geometry, thresholds, no-category policy, or broad generalization.

### 17.5 EXP4B (proposed) — present-utterance representability boundary

1. **Boundary question:** Does present-utterance evidence move from representable/usable to non-represented/non-usable when utterance marker content is changed while prior context is fixed absent?
2. **Why boundary:** This isolates the representability edge for sentence-internal cues.
3. **Relationship to EXP1–EXP3:** Extends accepted EXP2 sentence-source reference and compares no-cue-like edge behavior with EXP1 where appropriate.
4. **Variable/condition changed:** sentence marker content only.
5. **Controls fixed:** no prior context, `enable_category_selection=True`, `enable_s2m_seed=False`.
6. **Current capability:** in-process sentence execution via `run_pathA_short(...)` and sentence cue mappings in [category_cues.yaml](../../support/dictionaries/category_cues.yaml) (for example mapped `where` vs currently unmapped `how`).
7. **Evidence surfaces:** `.tschar.json` identity/status; `isc_category_result` cue/result/provenance fields; unavailable block.
8. **Known confounds/limitations:** lexical sentence changes may affect non-category fields; boundary target is representability, not full semantic equivalence.
9. **Could legitimately inform:** observable present-utterance representability boundary in current mapping.
10. **Cannot establish:** interior competition curves, thresholds, or meaning-policy conclusions.

### 17.6 EXP4C1 (proposed) — conflicting category evidence within present utterance

1. **Boundary question:** What does the mechanism report when one utterance simultaneously contains markers for different category directions?
2. **Why boundary:** This probes the conflicting-evidence condition itself (an edge condition), not an interior strength sweep.
3. **Relationship to EXP1–EXP3:** Extends accepted single-source references (EXP2 sentence-only, EXP3 prior-only) into same-utterance conflict condition.
4. **Variable/condition changed:** sentence content changed from single-direction cue to multi-direction conflicting cues.
5. **Controls fixed:** no prior context, `enable_category_selection=True`, `enable_s2m_seed=False`.
6. **Current capability:** sentence cue extraction supports multiple markers per utterance through substring marker matching and ordered-unique cue merge in CE/ISc.
7. **Evidence surfaces:** `.tschar.json`; `isc_category_result.category_cue`, weighted distribution, top category/confidence, rationale, provenance source, trace primitive sequence.
8. **Known confounds/limitations:** marker matching is lexical; conflict realization depends on currently mapped markers and fixed weights; no strength variation in this experiment.
9. **Could legitimately inform:** whether conflicting sentence evidence is observably represented and how outputs are reported at that conflict condition.
10. **Cannot establish:** crossover points, dominance curves, thresholds, or generalized competition geometry.

**Supported concrete condition (current mappings):**
- sentence candidate: `"Where support cold?"`
  - currently mapped sentence markers present: `where -> perspectival`, `support -> physical`, `cold -> affective`
  - prior context fixed: `None`

### 17.7 EXP4C2 (proposed) — conflict between prior context and present utterance

1. **Boundary question:** What does the mechanism report when prior-context evidence points in a different category direction than present-utterance evidence?
2. **Why boundary:** This probes cross-source disagreement as a boundary condition without introducing cue-strength/crossover sweeps.
3. **Relationship to EXP1–EXP3:** Uses accepted EXP2 (sentence source observable) and EXP3 (prior source observable) as reference points, then tests disagreement condition.
4. **Variable/condition changed:** source-direction alignment changed from aligned/single-source references to cross-source conflicting directions.
5. **Controls fixed:** same utterance, explicit prior-context list, `enable_category_selection=True`, `enable_s2m_seed=False`.
6. **Current capability:** CE combines sentence and prior cues; provenance source list can include both `sentence` and `prior_context_cex`; persisted by infra_smoke.
7. **Evidence surfaces:** `.tschar.json`; `isc_category_result` cue/provenance/distribution fields; runtime flags capturing prior context; unavailable block.
8. **Known confounds/limitations:** lexical matching and fixed weights govern conflict behavior; this experiment does not vary strength ratios.
9. **Could legitimately inform:** whether cross-source conflict is observably represented and how the mechanism reports the disagreement condition.
10. **Cannot establish:** crossover thresholds, gradient response surfaces, or no-category policy.

**Supported concrete condition (current mappings):**
- sentence candidate: `"Where is the book?"` (`where -> perspectival`)
- prior context candidate: `["cold"]` (`cold -> affective`)

### 17.8 EXP4D (proposed, retained) — Category Selection availability boundary (operational/structural control)

1. **Boundary question:** What changes in observable category-result surfaces when Category Selection commitment is enabled versus disabled under otherwise comparable cue-bearing inputs?
2. **Why boundary:** This is an operational/structural boundary control (availability of commit path), not an interior evidence-strength experiment.
3. **Relationship to EXP1–EXP3:** Complements accepted enabled-path references with an explicit disabled-path boundary control.
4. **Variable/condition changed:** `enable_category_selection=True` vs `False`.
5. **Controls fixed:** same cue-bearing sentence/prior-context input, `enable_s2m_seed=False`, same characterization type/version.
6. **Current capability:** runtime flag `enable_category_selection` controls TPU commit behavior; infra_smoke captures `isc_category_result` only when present.
7. **Evidence surfaces:** artifact identity/status; presence/absence shape of runtime-provided `final_tp.semantic.isc_category_result`; unchanged unavailable block.
8. **Known confounds/limitations:** operational control boundary does not itself characterize support-space content boundaries.
9. **Could legitimately inform:** whether commit-path availability boundary is observable and recorded cleanly.
10. **Cannot establish:** confidence thresholds, no-category rules, or interior category-response behavior.

### 17.9 EXP4E (deferred) — category-inventory boundary

1. **Boundary question:** How do outputs change when category inventory itself is withheld/added?
2. **Status:** retained as important boundary direction from governing research documents, but deferred.
3. **Current limitation:** no clean, review-approved campaign mechanism currently exists for controlled inventory switching/versioning without broadening scope.
4. **Decision rule:** do not implement new inventory-switch mechanism in this stage; revisit after explicit approval.

### 17.10 Additional boundary proposals discovered

- **Potential EXP4F (presently tractable):** category-result versus downstream-meaning boundary.
  - **Question:** category result present, but no legitimized meaning extension written (or vice versa under controls).
  - **Why distinct:** tests the boundary between category evidence and meaning legitimation stage (proposal/research documents explicitly separate these).
  - **Status:** optional addition; not execution-authorized by default.

### 17.11 Deferred interior-characterization marker (supporting/reinforcing evidence)

After boundary characterization, investigate supporting/reinforcing evidence conditions as interior characterization, including:

1. multiple supporting cues in the same present utterance toward the same category direction;
2. prior-context and present-utterance evidence jointly supporting the same category direction.

Do not presume confidence increase or any specific response shape; treat as later interior characterization, not EXP4 boundary work.

### 17.12 Recommended ordering (proposal)

1. **EXP4A** — clean prior-context representability edge.
2. **EXP4B** — clean present-utterance representability edge.
3. **EXP4C1** — same-source (utterance) conflict boundary.
4. **EXP4C2** — cross-source (prior vs utterance) conflict boundary.
5. **EXP4D** — operational availability boundary control.
6. **EXP4F (optional, if retained)** — category-result vs meaning boundary.

Ordering rationale: move from clean lexical representability edges to conflict edges, then structural control, while preserving one-at-a-time review-gated execution.

### 17.13 EXP4-family mandatory review gate

After any authorized EXP4 subexperiment, stop and report evidence at review gate. Do not auto-advance to the next subexperiment.
