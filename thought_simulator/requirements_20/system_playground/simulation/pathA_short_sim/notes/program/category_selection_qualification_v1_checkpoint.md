# Category Selection Qualification v1 Research Checkpoint

**Document:** notes/program/category_selection_qualification_v1_checkpoint.md  
**Status:** Non-normative research checkpoint.  
**Role:** Record the current Qualification v1 stopping point, open questions, and exact restart point.  
**Scope boundary:** This is not closeout and does not declare Qualification v1 complete.

## Completed progression (current cycle)

Framework v1 skeleton established  
↓  
current realization mapped onto Framework v1  
↓  
qualification identified as first meaningful hole  
↓  
Qualification Contract v1 defined  
↓  
`qualified` / `not_qualified` / `unresolved` conceptual states defined  
↓  
`not_evaluated` kept distinct from `unresolved`  
↓  
observability-only qualification instrumentation implemented  
↓  
five-condition controlled evidence set completed  
↓  
minimum Qualification Evidence Contract v1 defined  
↓  
weak inventory-vs-evidence hypothesis challenged  
↓  
positive-presence shadow hypothesis challenged

No final qualification predicate has been established.

## Established architectural state

### Qualification role

Qualification is an eligibility boundary:

`candidate construction -> qualification -> evaluation`

Qualification does not rank candidates and does not select a winner.

### Conceptual qualification states

Conceptual states remain:
- `qualified`
- `not_qualified`
- `unresolved`

No approved predicate currently assigns these states.

### Evaluation-status distinction

`not_evaluated` remains semantically distinct from `unresolved`:
- `not_evaluated`: no approved qualification predicate has executed;
- `unresolved`: reserved for a future condition where an approved predicate executes but available authorized evidence is insufficient to determine qualification.

## Qualification Evidence Contract v1 (semantic boundary)

At the candidate-construction → qualification boundary, each candidate carries:
1. candidate identity;
2. zero or more category-relevant evidence items;
3. authorized source attribution for every evidence item.

Empty evidence-item collection means no category-relevant evidence is represented at this boundary. It does not establish `not_qualified`, `unresolved`, rejection, or no-category.

Current Python fields (for example `f_s`, `f_b`, `f_e`, `f_i`, `in_current_category_cue`) remain realization/diagnostic fields rather than the architectural contract itself.

See:
- [category_selection_program_reference.md](category_selection_program_reference.md)
- [category_selection_framework_v1_realization_map.md](category_selection_framework_v1_realization_map.md)

## Qualification v1 implementation state

The first implementation remains observability-only.  
It observes pre-ISc candidate evidence at the CE→ISc boundary and currently reports the equivalent of:
- `qualification_evaluation_status = not_evaluated_predicate_open`
- `qualification_state = null`
- `qualification_rationale = null`

It has no authority to exclude candidates, alter scoring/competition, select or suppress categories, change committed TP semantic state, or influence downstream S2M behavior.

Existing replay verification passed after implementation.

## Controlled evidence coverage completed

Completed initial five-condition set:
- sentence-only
- prior-only
- both sentence + prior
- no-cue / inventory-only
- competition

The prior-only condition reused existing Palette v1 affective/`cold` construction (no new research case introduced).

## Bounded evidence findings

### Inventory versus evidence

Observed distinction:
- candidate exists through inventory/candidate construction;
- candidate carries identifiable category-relevant evidence from an authorized source.

### Source independence

Category-relevant evidence is separately observable from:
- current utterance/sentence evidence;
- prior-context evidence.

Both sources can coexist in one case.

### Competition

More than one candidate can independently carry authorized evidence before evaluation.

These observations do not establish qualification.

## Weak hypothesis status

Hypothesis: inventory membership establishes candidacy, while identifiable category-relevant evidence from an authorized source is observably separable from inventory membership before evaluation.

Status: **SUPPORTED FOR FURTHER CHALLENGE** (not proven).

## Positive-presence shadow hypothesis status

Hypothesis: a constructed candidate with one or more category-relevant evidence items attributable to an authorized source may be qualified for evaluation.

Status: **RESEARCH HYPOTHESIS / EXPERIMENTAL SHADOW POLICY**.  
It is not Qualification Predicate v1, not Framework v1 architecture, not bounded realization policy, and not a normative requirement.

Coverage used for challenge:
- sentence-only
- prior-only
- both
- no-cue/inventory-only
- competition
- one existing Palette v1 alternate/boundary-adjacent construction

Result: **SURVIVED INITIAL CHALLENGE** in that bounded set (no counterexample found there).

## Shadow interpretation boundary (current)

Current asymmetry preserved:
- evidence present → `may_be_qualified` (shadow result only)
- evidence absent → positive qualification not established

Evidence absence does not assign `not_qualified` or `unresolved`.  
Multiple competing candidates may simultaneously satisfy the positive-presence shadow condition.

## Explicitly open items

- whether evidence presence is actually sufficient for qualification;
- meaning of evidence absence;
- final role of `unresolved`;
- evidence compatibility/conflict;
- evidence strength;
- evidence semantic subtypes;
- source weighting;
- effects of multiple evidence items;
- qualification thresholds;
- final qualification predicate;
- enforcement;
- entropy's later evaluation/selection role;
- entropy normalization/carrier/continuity issues recorded elsewhere;
- generalized non-selection behavior.

## Current fog boundary

The positive-presence hypothesis has survived an initial bounded challenge, but no tested case has yet demonstrated whether an authorized evidence item can be present while still being insufficient or inappropriate for candidate qualification.

Next work should not automatically add evidence semantics merely because additional distinctions are possible.

Restart question:

**Has the current evidence exposed a reason that positive evidence presence is insufficient, or should the simple positive-presence hypothesis receive stronger edge pressure before another qualification dimension is introduced?**

## Restart point

Next research activity:
- critical review of whether positive-presence needs another semantic dimension, or should first receive stronger controlled edge pressure.

No qualification-predicate implementation is authorized.  
No qualification enforcement is authorized.  
Current runtime qualification remains observability-only.

## Authority/status boundaries

- [category_selection_program_reference.md](category_selection_program_reference.md): owns Framework v1 and Qualification/Evidence contracts.
- [category_selection_framework_v1_realization_map.md](category_selection_framework_v1_realization_map.md): owns factual current realization mapping.
- [category_selection_qualification_v1_checkpoint.md](category_selection_qualification_v1_checkpoint.md): records current research status and restart point.
- existing characterization/observation documents: remain historical/empirical evidence.

## Continuation: Deliberate edge-pressure probe defined (2026-11-24)

Direction A confirmed. No insufficiency of positive presence yet shown.

Chosen dimension: deliberately limited evidence (qualification-limited probe status).

Probe: `qual_v1_edge_limited_physical_support`
- Sentence: "The book is on the support."
- Prior: none
- Target: physical
- Expected evidence: sentence-attributed cue if `support` maps
- Independent limitation: Palette v1 records `support` as historical / qualification-limited (not canonical)

Matched control: "The book is on the table." (canonical physical, sentence-only)

Shadow hypothesis unchanged:
- evidence present → may_be_qualified
- evidence absent → positive qualification not established

Outcomes:
- Survives: both produce authorized evidence; limited status confirmed; shadow labels edge candidate may_be_qualified; no further ineligibility forced.
- Counterexample: authorized evidence present but limited status independently establishes ineligibility → positive presence insufficient; dimension earned.
- Invalid: evidence or limitation not established.

Tomorrow's Agent mission: compare "The book is on the support." against "The book is on the table.", first verify that `support` still produces authorized physical evidence and that its qualification-limited status is documented, apply the unchanged positive-presence shadow hypothesis, classify the result as survives / counterexample / invalid, verify zero semantic drift, and stop.

No enforcement. No new predicate. All other dimensions remain open.

The historical label “qualification-limited” does not by itself mean ineligible. The experiment asks whether that independently documented limitation is sufficient grounds to challenge eligibility.
