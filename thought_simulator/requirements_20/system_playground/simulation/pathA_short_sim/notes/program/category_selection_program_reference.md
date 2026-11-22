# Category Selection Program Reference

**Document:** notes/program/category_selection_program_reference.md  
**Status:** Draft bounded software-realization contract for category selection.  
**Date:** 2026-11-21

## 1) Purpose

Define the bounded implementation contract for category-selection realization on the Path A short simulator, including software boundaries, required observability outputs, verification discipline, and required documentation updates after implementation.

This reference covers category-selection realization behavior.  
Characterization instrumentation is specified separately in [category_selection_characterization_reference.md](category_selection_characterization_reference.md).

## 2) Category-selection document family

For the complete category-selection document map, document roles, authority relationships, software references, characterization documents, and observation records, see:

[category_selection_index.md](category_selection_index.md)

## 3) Required authorities and context

Normative authorities:

- [20.45_ts_isc_scoring.md](../../../20.45_ts_isc_scoring.md)
- [20.105_tp_requirements.md](../../../20.105_tp_requirements.md)
- [20.116.010_tp_envelope_index.md](../../../20.116.010_tp_envelope_index.md)
- [20.40.050_idob_prim.md](../../../20.40.050_idob_prim.md)

Program/research context:

- [category_selection_proposal.md](category_selection_proposal.md)
- [category_selection_research_plan.md](category_selection_research_plan.md)
- [category_selection_stage1_modification_map.md](category_selection_stage1_modification_map.md)
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md)
- [category_selection_characterization_milestone1_closeout.md](category_selection_characterization_milestone1_closeout.md)
- [category_selection_observation.md](category_selection_observation.md)
- [category_structure_observation.md](category_structure_observation.md)
- [user_guide.md](../../user_guide.md)

## 4) Responsibility split with characterization reference

Coordinated sibling references have distinct ownership:

- **This document** owns category-selection realization behavior on the main path (cue intake, scoring, commit, S2M consumption boundary, and realization observability surfaces required by the category-selection path).
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md) owns characterization orchestration/instrumentation, characterization session/artifact identity, and characterization experiment-support outputs.

This document does **not** define characterization artifact/session contract details beyond what the realization must expose for characterization to consume.

The characterization reference does **not** define the category-selection meaning path itself.

Boundary requirement:

- The category-selection realization SHALL expose the observation surfaces and measurements required by [category_selection_characterization_reference.md](category_selection_characterization_reference.md).
- Characterization-specific control and evidence-management responsibilities SHALL NOT be embedded into the category-selection mechanism itself.

The category-selection realization must not own:

- characterization-type dispatch,
- characterization sweep orchestration,
- characterization session management,
- characterization campaign orchestration,
- characterization artifact creation or naming,
- `.tschar.json` artifact persistence,
- characterization run numbering,
- characterization artifact collision/non-overwrite management,
- characterization-specific aggregation,
- characterization experiment sequencing.

Those responsibilities are defined by [category_selection_characterization_reference.md](category_selection_characterization_reference.md).

Characterization observes and exercises the category-selection realization; characterization does not become part of the category-selection or meaning-selection mechanism.
Milestone-1 characterization infrastructure completion status is recorded in [category_selection_characterization_milestone1_closeout.md](category_selection_characterization_milestone1_closeout.md).

Characterization must observe a caller-selected TS execution and must not own or alter sentence/input selection, prior context, category-selection control, S2M control, or other TS-affecting execution controls.

## 5) Realization scope

In scope for this contract:

- sentence-internal and prior-context cue intake along current path boundaries,
- category evidence scoring and result production,
- commit path into `TP.semantic.isc_category_result` under normative ownership,
- read-only category-result consumption by IdOB/S2M path,
- candidate relevance/consideration and legitimation/refusal separation behavior,
- required observation surfaces for replay/debug/inspection.

Out of scope for this contract:

- alternative/parallel meaning paths,
- characterization campaign/session management,
- final no-category decision-function design (threshold/region/hysteresis policy).

## 6) Non-mutation walls

Implementation under this contract must preserve:

- additive category-selection behavior relative to structural/default meaning path,
- non-mutation of structural writer responsibilities (SOB/SROB/CnOB/SmOB),
- read-only S2M consumption of committed category result,
- separation between candidate relevance and final legitimation/refusal.

Category support must not be treated as automatic meaning legitimation.

## 7) Required realization outputs

Category-selection realization must continue to expose inspectable outputs sufficient for bounded review, including:

- cue source and cue values (including provenance summary),
- category distribution and top category result,
- confidence and rationale outputs,
- committed `TP.semantic.isc_category_result`,
- downstream candidate selection states,
- legitimation/refusal result visibility,
- final participation/composite relation visibility.

If an output is unavailable in a run, absence must be explicit rather than silently omitted.

## 8) Implementation touchpoint discipline

Any implementation work performed under this contract must:

1. identify touched modules/functions explicitly before edit,
2. preserve normative ownership and envelope contracts,
3. keep category-specific knowledge in data where architecture allows,
4. avoid introducing silent fallback behavior for category-type logic,
5. preserve deterministic replay behavior for existing baseline fixtures unless explicitly reviewed.

## 9) Verification contract

Each implementation batch under this contract requires:

- targeted replay/verification commands covering changed behavior,
- confirmation that unchanged baseline category/S2M replay expectations still hold,
- explicit reporting of any divergence from prior replay outputs with rationale,
- no hidden requirement changes.

Known replay/baseline tools may be reused as appropriate to changed scope.

## 10) Stop/review gates

Before merging non-trivial realization changes:

1. **Contract gate:** normative ownership/field boundaries still respected.  
2. **Behavior gate:** relevance vs legitimation separation still observable.  
3. **Replay gate:** deterministic checks pass or divergence is explicitly reviewed/accepted.  
4. **Documentation gate:** required document updates completed (including [user_guide.md](../../user_guide.md)).  
5. **Observation gate:** no fabricated results inserted into [category_selection_observation.md](category_selection_observation.md).

## 11) Required post-implementation documentation update

After any approved implementation affecting user-visible category-selection behavior or workflow, [user_guide.md](../../user_guide.md) must be updated in the same change cycle.

At minimum, that update must reflect:

- how to run the relevant category-selection behavior,
- how to read category-selection outputs in normal run output,
- any added/changed observable fields on the category-selection path,
- any changed relationship between normal run output and debug workflow (`run_examples.py -> run.log -> pathA_dbug.py`),
- boundaries between realization output and characterization artifacts (if characterization integration is user-visible).
- terminology alignment with accepted category-selection documents, including removal of obsolete informal "floor" wording when it refers to the structural path (for example, use wording equivalent to "structural path established" and "structural-path-visible information").

If no user-visible behavior changed, the change report must explicitly state why no [user_guide.md](../../user_guide.md) update was required.

## 12) Explicit non-goals

This contract does **not**:

- define the final no-category decision rule,
- define threshold policy for unsupported-space determination,
- define hysteresis/persistence policy,
- replace the characterization reference,
- authorize normative requirement edits by itself.
