# Category Selection Characterization-Readiness Audit

**Document:** notes/program/category_selection_characterization_readiness_audit.md  
**Status:** Factual Stage 1 capability map (read-only inspection). Non-normative.  
**Date:** 2026-11-23  
**Governing context:** [category_selection_research_plan.md](category_selection_research_plan.md) sections 8A, 8B, and 13.  
**Purpose:** Record the factual determination of what the current Path A Category Selection realization can vary and measure. Owns the capability map; does not own the research roadmap.

## Verdict

**D. Local axis available.**

A bounded region of ordered control exists whose extent is unknown. Experiments can be constructed to expose the edge. Measurement qualification applies (see below).

## Probe readiness

Existing accepted experiments used a sparse cue set drawn from `category_cues.yaml`:

- sentence_internal: cold → affective, support → physical, where → perspectival
- prior_context: cold → affective, object → physical, support → physical, location → perspectival

Role-relative eligibility is limited by the maps. Scaffolding tokens outside these maps do not contribute category evidence. Upstream structural treatment (token classes, segment/role participation) remains uneven for several markers. No new probes were added.

## Palette extensibility

Architectural separation currently exists between configuration maps (`category_cues.yaml`) and the CE/ISc scoring mechanism. Adding markers that map to existing majors is data/configuration growth. Adding new majors requires inventory change plus map entries. Whether further palette growth remains purely data-driven for all desired roles is unclear by inspection for constructions that interact with upstream structural support. No palette was designed or proposed.

## Control readiness

Most present operations are discrete presence comparisons.

**Defensible local ordered axis (established by inspection):**

Discrete three-point weighted source-composition axis for one fixed major.

Ordered states (source-support contributions only):

- prior only: 0.25
- sentence only: 0.35
- both sources: 0.60

These figures are the varying `w_b * f_b` and `w_s * f_s` contributions. Constant terms (`w_i * f_i` and `w_cat * indicator`) remain present and identical across the three cued states when the target major remains in the combined cue set.

**Controls that can be held fixed by input construction:**

- target major identity
- indicator = 1 across all three cued states
- punctuation signal (`f_e` = 0, no trailing “?”)
- correction signal (`f_i` = 1 under normal “no_change”)
- competing majors’ scores (no markers for other majors in either source)
- category inventory

Because competing scores remain fixed, softmax preserves the ordering of the target probability. The sequence is therefore a justified ordered independent-variable relationship under these controls.

**Scope qualification:**

This is a discrete three-point weighted source-composition axis for one fixed major under the current realization. It is not a continuous axis, not general evidence strength, not a vocabulary-strength scale, not proof of global monotonicity, not established across every category, and not a characterization of competition. Extent is unknown.

**Cleanest initial probe realization:** affective via the marker `cold`, which is mapped in both sentence_internal and prior_context. Physical via `object` (prior) and `support` (sentence) is valid for source composition but introduces lexical asymmetry.

**Other candidates:**

- Punctuation-derived perspectival (`f_e`): binary, category-specific perturbation. Known score direction. Not a multi-point ordered axis.
- Same-source multiplicity / cue repetition: deduplicated; does not accumulate. Discrete presence only.
- Inventory changes: discrete comparison when evidence is held fixed.

## Measurement readiness

Presently observable with numerical resolution: category distribution (post-softmax probabilities), top category, category confidence (top probability), provenance, rationale, and downstream candidate state.

Unavailable: entropy, top-versus-second margin.

**Measurement qualification:** sufficient resolution for the three-point category distribution and confidence response on the local axis; insufficient resolution for finer ambiguity or interior-shape analysis.

## Controlled-evolution diagnostic

Clear separation exists between:

- Category Selection mechanism (CE/ISc scoring path)
- configuration/research content (`category_cues.yaml`, majors inventory)
- experimental definitions (currently external to the scoring path)
- measurement/instrumentation (distribution and confidence exposed; entropy/margin unavailable)

Likely research growth classifications:

- additional markers for existing majors: data/configuration growth
- additional experiment definitions using existing markers: repeatable experiment-definition growth
- new majors or changes to scoring weights/formula: coupled to mechanism/code or configuration requiring explicit review
- constructions requiring upstream structural support changes: unclear by inspection or coupled

No changes were proposed.

## Relationship to roadmap

Stage 1 is complete with verdict D and measurement qualification. Stage 3 (capability-gap resolution) is not indicated by this result. Next work is Stage 2: formal identification and experimental contract for the legitimate local axis(es).
