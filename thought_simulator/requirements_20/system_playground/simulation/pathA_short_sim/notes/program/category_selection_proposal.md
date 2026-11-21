# Category selection proposal

**Document:** notes/program/category_selection_proposal.md  
**Status:** Draft / discussion — aligned with stabilized S2M and normative ISc/TP/IdOB path  
**Date:** 2026-11-20  
**Points from:** short-sim status (prior S2M seed goal is now historical); s2m_relational_proposal.md; s2m_program_reference.md (Phase III/IV); 20.45, 20.105, 20.116.010, 20.40.050

For reader-facing interpretation of displayed category fields and observation scenarios in normal `run_examples.py` output, see [user_guide.md](../../user_guide.md).

## Purpose

Category selection answers: how can available information cause a non-default interpretive category to become relevant to S2M while preserving the structurally licensed default meaning?

It is additive. It does not replace the five-stage S2M model (structural relation → default meaning → candidate interpretation space → selected interpretive extension(s) → finite customized composite). When no usable category cue is active, the structurally licensed default meaning remains the S2M result and candidates remain unselected (no-cue = default meaning only).

A category result is not itself meaning. A category cue, score, top_category, or matching candidate is not automatically a written meaning relation.

## Baseline

When no usable category cue is active:
- Structural relation is established by the structural path.
- Default meaning is derived from that relation.
- Candidate interpretations remain available but unselected.
- No interpretive extension is written.

Category influence, when present, is additive to this baseline. It does not overwrite default meaning.

## Category-selection distinction

Stages remain distinct:

cue evidence → category scoring → committed category result → candidate relevance/consideration → S2M legitimation or refusal → selected interpretive extension (if any)

This enters the existing S2M process. It does not replace it. Selection (making a candidate relevant) is distinct from legitimation (writing it as an extension after licensed-region and cue-supported assessment).

## Cue sources

Two origins remain; their provenance stays visible. Downstream they converge on the same committed category-result interface.

### Sentence-internal information
Sentence-internal evidence → CE supplies optional `category_cue` → ISc category-aware scoring → Merge / TPU → `TP.semantic.isc_category_result` → IdOB (read-only) / S2M

Ordinary semantic endpoints are not, merely by being endpoints, sentence-internal category cues. Sentence-internal category cues require independently directing evidence such as modifiers, adverbs, structural markers, or equivalent structural-path-visible information.

### Prior-conversation / context information
Prior conversation / CIL → CEx / CE supplies optional `category_cue` → ISc → Merge / TPU → `TP.semantic.isc_category_result` → IdOB (read-only) / S2M

IdOB does not reach backward into raw CIL, CEx internals, or sentence markers as an alternative category-selection mechanism. Absence of a category result does not block ordinary S2M / default meaning.

## Common downstream path

```
cue source
  ↓
CE category_cue
  ↓
ISc category-aware scoring
  ↓
isc_output{}
  ↓
Merge
  ↓
TPU commit
  ↓
TP.semantic.isc_category_result
  ↓
IdOB read-only category cue
  ↓
S2M candidate consideration
  ↓
licensed-region / legitimation decision
  ↓
default meaning + any legitimized extension
```

Terminology follows the normative requirements for ownership and field names. No parallel category-result mechanism is introduced.

## Category-result interface

The committed category result is the envelope specified by the requirements:

```
TP.semantic.isc_category_result {
    category_cue,
    category_weighted_distribution,
    top_category,
    category_confidence,
    category_rationale,
    provenance
}
```

Only TPU writes this block (from ISc via Merge). IdOB may read it as a read-only cue when performing category-aware meaning selection. It does not write the block. The fields represent scored cue evidence, not meaning.

`top_category` is the primary scoring summary (major of the highest-probability candidate, or null). Candidate relevance may use other category evidence contained in the committed result (for example the full weighted distribution or majors present in `category_cue`) according to the bounded realization policy. `top_category` is not itself a final meaning-selection command.

With an empty cue, the short realization should prefer `top_category: null` rather than expose an arbitrary tie-break winner as apparent category evidence.

Default-versus-selected comparison is observable through S2M Phase IV rather than stored as an additional field inside this envelope.

## S2M selection and legitimation

A committed category result may cause some candidate interpretation to become relevant for consideration. That does not mean a candidate tagged with `top_category` is automatically written as a meaning relation.

Progression:

committed category result → candidate becomes relevant → proposed extension → licensed-region / cue-supported assessment → legitimate or refuse → write extension or remain unselected/null

Conceptually:

default meaning + legitimized category-supported extension(s) = finite customized composite

The initial short-simulator licensed-region table (exact endpoint/relation/target tuples for the canonical examples) is acknowledged as bounded realization scaffolding, not a generalized structural licensing mechanism.

Context stores (sources/regions of contextual information) remain distinct from interpretation majors (taxonomy that tags candidates). “Category” here refers to the scored cue that can influence relevance within that taxonomy, not a collapse of the two.

Successful category scoring does not guarantee an interpretive extension. Legitimate outcomes include: no usable cue, ambiguous evidence, category result but no applicable candidate, candidate available but unselected, proposed but refused, extension remaining null, or default meaning only.

## Observation through S2M Phase IV

Category-selection realization remains inspectable through the Phase IV — Category Structure Observation framework in s2m_program_reference.md. The category-specific phenomena of interest include: no-cue baseline; cue and provenance; candidate state before category influence; category evidence and scoring/result; top_category, confidence, and rationale; selected versus unselected candidates; S2M legitimation or refusal; default meaning versus category-extended meaning; sentence-internal versus prior-context cue paths; deterministic replay.

The bounded three-experiment Phase IV program that uses this realization as its instrument is recorded in [category_structure_observation.md](category_structure_observation.md). That paper is an experimental/observational record of controlled observations; it does not establish new requirements or architectural claims.

This proposal does not duplicate the detailed nine-window methodology. An observation characterizes behavior of the current realization. It does not independently establish a new requirement, semantic truth, or architectural claim. Observed behavior can motivate later review; it does not automatically modify architecture or requirements.

## Boundaries

- Category choice is additive and optional. Floor writers (SOB–SmOB) are not mutated.
- Crossing fields stay null until a later, explicit stage writes them.
- Requirements remain unchanged until realization is shown to be legitimate.
- No new TP fields, scoring equations, ownership, cue sources, or canonical categories are introduced here.
- Normative ownership, commit path, and field contents are defined in 20.45 (ISc), 20.105 (TP), 20.116.010 (envelope index), and 20.40.050 (IdOB).

## Next realization step

Successor sequence for this proposal:

[category_selection_research_plan.md](category_selection_research_plan.md) → Stage-1 current-software modification map → [category_selection_program_reference.md](category_selection_program_reference.md) → reviewed implementation.

Successor documents:
- [category_selection_research_plan.md](category_selection_research_plan.md)
- [category_selection_program_reference.md](category_selection_program_reference.md)
- [category_selection_observation.md](category_selection_observation.md)

## Relation to prior work

This proposal follows the successfully realized narrow S2M seed (accountability trail + interpretive transfer). That prior goal is historical. The present revision replaces the earlier sketch in which IdOB directly read sentence or CEx information and independently chose a category.
