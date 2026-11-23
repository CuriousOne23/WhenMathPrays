# Category-Supported Admission Characterization

**Document:** notes/program/category_supported_admission_characterization.md  
**Status:** Agreed working specification (non-normative). Observational only.  
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

Qualify and bind executable fixtures for all four baseline observations against the existing realization, execute only authorized qualified cases, then stop and review the evidence.
