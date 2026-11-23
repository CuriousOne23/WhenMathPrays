# Category-Supported Admission Characterization

**Document:** notes/program/category_supported_admission_characterization.md  
**Status:** Agreed working specification with recorded qualified baseline execution (non-normative). Observational only.  
**Date:** 2026-11-23  
**Purpose:** Freeze the narrow observational plan for the existing category-supported admission mechanism already present in the Path A short realization. Establish its basic behavioral geometry before asking whether that geometry is adequate for S2M.

## Frozen finding

The S2M function previously discussed under the explanatory word “relevance” already exists operationally as category-supported admission.

In `s2m/loop.py` (`apply`):

- `propose(seed)` produces available candidates.
- The committed `TP.semantic.isc_category_result` narrows `selected_space` (preferring `top_category` when it matches a proposal major; otherwise matching cue values).
- A proposal receives `selection_state = "category_supported"` only when its major is in `selected_space`.
- Only category-supported proposals are passed to `legitimate()`.
- Post-check updates the same proposals to `"legitimized"` or `"refused"`.
- Only legitimized relations are written.

The intermediate state is already reported on the proposal trace. Category support admits a candidate for structural assessment; it does not legitimize or write meaning.

## Terminology (provisional)

- Architectural concept: contextual candidate admission
- Implementation state: `category_supported`
- Informal explanatory word: relevance (optional; not operational)

## Central sequence

available candidate → category-supported candidate (admitted) → legitimized or refused → extension or null

## Governing question

Does the existing category-supported admission mechanism exhibit its intended local behavior across the four baseline conditions, and what, if anything, do those observations reveal that is consequential for later assessment of S2M adequacy?

## Adequacy distinction

- Local adequacy: does the admission step behave as the current realization implements it?
- S2M adequacy: is that behavior sufficient for contextual evidence to play its required role in producing a finite customized composite?

The baseline observations below can establish local adequacy. They do not establish S2M adequacy.

## Execution qualification and case binding (required before formal execution)

The four baseline observations below define **abstract logical conditions**. They are not executable formal observations until each condition is bound to a realization-supported input/fixture.

Before authorizing execution of any baseline case, record or verify:

1. exact input/fixture;
2. required structural-floor condition;
3. expected candidate availability and candidate major(s);
4. required Category Selection condition;
5. expected category-derived `selected_space`;
6. the admission/non-admission transition the case is intended to observe;
7. evidence from the existing realization, qualified characterization references, or established fixtures that these preconditions can coexist in that case.

### Authorization rule

A case whose required preconditions cannot be established is ill-formed for formal execution and **SHALL NOT** be run as evidence for that baseline condition.

### Observation-validity rule

If an executed case fails to instantiate one or more required preconditions, that run is non-qualifying for the target baseline condition. It is not evidence for or against the behavior under test. Stop, identify the unmet precondition, and return for review before substituting another fixture or continuing the campaign.

## Baseline observations

(Sufficient to record the basic geometry of the handoff. Use existing runner and S2M record. No new fields or control-flow changes.)

1. **Expected admission**  
   Category evidence supports an available candidate major.  
   Expect: `selection_state` becomes `category_supported`; candidate enters legitimation; subsequent legitimized/refused outcome is recorded.

2. **Expected non-admission**  
   Available candidate exists but its major lies outside the category-derived `selected_space`.  
   Expect: `selection_state` remains `candidate_unselected`; candidate is excluded from legitimation.

3. **Admission followed by refusal**  
   Category evidence supports the candidate, but the licensed-region table rejects the tuple.  
   Expect: intermediate `category_supported` followed by final `refused`; no extension written.

4. **No usable category evidence**  
   Empty or absent `isc_category_result`, or a cue that matches nothing in the proposals.  
   Expect: `selected_space` empty; all proposals `candidate_unselected`; default meaning only; no extensions.

## Formal baseline execution record (qualified bindings)

Execution session:

- `session_id=category_supported_admission_baseline_qualified`
- `characterization.type=infra_smoke`
- `characterization.version=1.0`
- `enable_s2m_seed=True`
- `enable_category_selection=True`

Recorded cases and artifacts:

1. **Expected admission**  
   Fixture: `"The book is on the table."`  
   Artifact: `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/category_supported_admission_baseline_qualified/runs/000001__infra_smoke__1.0.tschar.json`  
   Recorded facts: structural floor present; category cue/top category `physical`; candidate interpretations entered legitimation and reached `legitimized`; extensions written.

2. **Expected non-admission**  
   Fixture: `"Where is the book?"`  
   Artifact: `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/category_supported_admission_baseline_qualified/runs/000002__infra_smoke__1.0.tschar.json`  
   Recorded facts: structural floor present; candidates available across majors (`mental`, `perspectival`, `physical`); category cue/top category `perspectival`; observable `candidate_unselected` states present for candidates outside selected space.  
   Review status: approved/closed.

3. **Admission followed by refusal**  
   Fixture: `"Where is the book?"`  
   Artifact: `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/category_supported_admission_baseline_qualified/runs/000003__infra_smoke__1.0.tschar.json`  
   Recorded facts: structural floor present; category cue/top category `perspectival`; admitted intermediate path observable and final `refused` state recorded; no extension written.

4. **No usable category evidence**  
   Fixture: `"The sky is blue."`  
   Artifact: `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_characterization/sessions/category_supported_admission_baseline_qualified/runs/000004__infra_smoke__1.0.tschar.json`  
   Recorded facts: structural floor present; `category_cue=[]`; `top_category=null`; selected space empty; candidates remained `candidate_unselected`; default-only outcome with no extension.

## Local-adequacy closeout claim (bounded)

Under the recorded qualified bindings above, the existing category-supported admission mechanism demonstrates the intended local baseline behavior across the four baseline conditions.

## Non-claim preserved

This baseline record does **not** establish broader S2M adequacy.

## Deferred Category Selection boundary preserved

No deferred Category Selection condition was forced open by these baseline observations.

## Execution-qualification lesson (from invalid initial Case 2)

The initial attempted Case 2 fixture (`"The sky is cold."`) was non-qualifying because it did not instantiate required preconditions (`written_relations=[]`, no proposals/candidates).  
This confirms the execution-qualification rule: abstract baseline conditions must be bound to realization-supported fixtures before formal execution evidence is admissible.

## Hard constraints

- No redesign of admission logic.
- No relevance score, distribution, envelope, or new primitive.
- No rename of `category_supported`.
- No change to IdOB ownership or the licensed-region table.
- No claim of sufficiency beyond the conditions actually observed.
- Characterization remains additive and non-mutating with respect to the structural floor.

## Stop condition

Record the four baseline observations. Then stop and examine only what the records show. Do not reopen deferred Category Selection items (ambiguity, competing evidence, weak confidence, inventory mismatch, etc.) unless the records themselves force the issue.

## Next step

Stop for research review. Do not propose or execute additional characterization from this document without new explicit authorization.
