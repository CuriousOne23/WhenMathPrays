# Structure to Meaning: IdOB Constructs

**Status:** Definitions for the present learning-bench revision. Unproven with the theory.
**Companion theory:** [idob_s2m_theory.md](idob_s2m_theory.md)
**Glossary:** Appendix A of this file.
**Date:** 2026-08-27

This paper names the constructs the machine already uses. Each card is: identity, why IdOB needs it, boundary, example, packet/slide.

IdOB is the last card. Everything before it exists so that card is thinkable.

## Hierarchy of the crossing

    structure card (six IDs + optional residue/features)
        -> structural_key / structural_hash
        -> struct_to_meaning_map   (legality)
        -> ranking                 (order among legal groups only)
        -> meaning group prototype M
        -> CIE modulation          M' = M + alpha I
        -> cycle / meaning_delta_h / identity_delta
        -> resolution_status
        -> ready_for_ouba          (handoff; this bench stops)

Theory: structure admits; IdOB instantiates the speaker-object stand-in; identity pressures; freeze is named.

## Construct cards

### C1. Structure card

**Identity.** Meaning-blind geometry record: six slots plus optional residue and feature tags.

**Why IdOB needs it.** Without a card there is no key, no map lookup, no legality.

**Boundary.** Must not contain the six meaning floats, CIE, literals-as-meaning, truth, or belief.

**Example.** S_rock_burst: field=12, role=3, object=44, gradient=2, universe=1, subfield=7, residue=static_object_vs_dynamic_action.

**Field / slide.** 01_structure/structure_card.examples.yaml. Slide 01.

### C2. Six structural IDs

**Identity.** semantic_field_id, semantic_role_id, semantic_object_id, gradient_id, universe_id, subfield_id. Present instrument cut. Not proven complete.

**Why IdOB needs them.** Only inputs allowed into the structural key. Levers for meaning-group legality.

**Boundary.** Geometry labels, not six-axis scores.

**Example.** Deadline card six-tuple differs from the rock card.

**Field / slide.** Slide 01. Coverage and discrimination are open checks.

### C3. structural_key / structural_hash

**Identity.** Deterministic fingerprint of the six IDs only. This bench: SK|field|role|object|gradient|universe|subfield.

**Why IdOB needs it.** Replay. Candidate lookup. Collision visibility.

**Boundary.** No CIE, no six-floats. Same six IDs -> same key always.

**Example.** Rock SK|12|3|44|2|1|7. Sleepy SK|401|7|30|1|1|0.

**Field / slide.** Slides 01, 07.

### C4. Residue and feature tags

**Identity.** Optional constraint-tension (residue_code / residue_hash) and ranking signals (feature_tags, routing_signature parts).

**Why IdOB needs them.** Ranking and geometry-under-tension without turning structure into meaning.

**Boundary.** Not six-float meaning. Not CIE.

**Example.** Rock residue static_object_vs_dynamic_action; tags object_rock, gradient_dynamic.

**Field / slide.** Slides 01, 04.

### C5. Struct-to-meaning map

**Identity.** Structure identity -> list of legal group_ids.

**Why IdOB needs it.** How structure bounds meaning space. IdOB must not invent groups the map forbade.

**Boundary.** Does not assign physicality. Empty list is legal.

**Example.** S_rock_burst -> [1001, 3001, 5001]. S_unmapped -> [].

**Field / slide.** candidate_group_ids. Slide 03.

### C6. Meaning group

**Identity.** Named prototype of a speaker-object in six-space: group_id, group_name, primitive, group_dimensions.

**Why IdOB needs it.** First M comes from an assigned prototype in this revision, not a word-to-score formula.

**Boundary.** Not a sentence, not a dictionary of words, not truth.

**Example.** Group 1001 ACTION.physical.motion (physicality 0.95, ...).

**Field / slide.** meaning_groups.slide.yaml. Slide 02.

### C7. Six meaning axes / meaning_semantics (M)

**Identity.** One vector: physicality, sociality, temporality, intentionality, materiality, spatiality. Official meaning_semantics is this vector, not a literal string.

**Why IdOB needs it.** Stand-in speaker-object. Without named axes there is nothing to pressure or freeze.

**Boundary.** Not six dictionaries. Not listener state. Not proven complete.

**Example.** After CIE, physicality may clip to 1.00 while materiality moves a little.

**Field / slide.** Slides 02, 05-07. Theory section 2.

### C8. Ranking

**Identity.** Order inside the candidate set only -> final_rank_order.

**Why IdOB needs it.** When several groups are legal, one prototype becomes first M.

**Boundary.** Must not add a group the map forbade.

**Example.** Rock order [1001, 3001, 5001].

**Field / slide.** Slide 04.

### C9. CIE (Conversational Identity Envelope)

**Identity.** Local identity pressure on the stand-in speaker-object. M' = M + alpha * I.

**Why IdOB needs it.** Stance can move meaning without a new structural key.

**Boundary.** Not listener uptake. Not life-story. Not baked into the key. Intent != motive/deception/force.

**Example.** Same group 1001, envelopes physical_stance vs scientific_stance vs neutral.

**Field / slide.** Slide 05.

### C10. meaning_delta_h and identity_delta

**Identity.** Machine motion ||M_i - M_{i-1}|| and the same for I. Analogue of consequence, not a person's change.

**Why IdOB needs them.** Freeze and visibility need a number that moved.

**Boundary.** Not how much the listener changed. Not truth.

**Field / slide.** Slide 06.

### C11. Search budget and resolution_status

**Identity.** Cycles min 4 / max 6 here. Halt names: stable, identity_stable, budget_exhausted, time_exhausted.

**Why IdOB needs them.** Without a name, budget poses as meaning.

**Boundary.** Packet string must match the predicate that halted. Budget halt labeled stable is improper.

**Field / slide.** Slides 06-07. stop_reasons.md.

### C12. ready_for_ouba

**Identity.** Handoff flag. This bench stops. Truth/belief not computed.

**Boundary.** Does not imply OuBA ran. True only for stable / identity_stable in this slide.

**Field / slide.** Slide 07.

### C13. IdOB

**Identity.** Path A site of the crossing: first place the speaker meaning-object stand-in may exist, given only structure, optionally pressured by CIE, frozen under a named reason.

**Why the theory needs it.** Without a named site, structure and meaning collapse into one foggy box.

**Boundary.** Not cognition. Not OuBA. Not the listener. Does not invent geometry.

**Example.** Slide 07 packet for S_rock_burst.

**Field / slide.** Whole min packet. Theory section 5.

## Supporting notes (not a second spine)

- 01_structure/structure.md
- 02_meaning_groups/dimensions.md
- 00_contract/vocabulary.md (short table; official long definitions are this paper + Appendix A)
- papers/ts_sob2srob_req4idob.md

## Appendix A — IdOB glossary (this revision)

| Name | One line |
|------|----------|
| Structure card | Meaning-blind geometry record (six IDs + optional residue/features). |
| semantic_field_id | Which field the geometry sits in. |
| semantic_role_id | Role slot in that field. |
| semantic_object_id | Object slot in the geometry. |
| gradient_id | Dynamic / gradient class. |
| universe_id | Universe of discourse for the geometry (not meaning). |
| subfield_id | Subfield inside the field. |
| structural_key / structural_hash | Fingerprint of the six IDs only. |
| residue_code / residue_hash | Constraint-tension fingerprint; not meaning. |
| feature_tags / routing_signature | Ranking / routing signals; not six-float meaning. |
| Struct-to-meaning map | Structure -> legal group_id list. |
| candidate_group_ids | Those legal ids on the packet. |
| Meaning group | Prototype speaker-object in six-space. |
| group_id / group_name / primitive | Group identity labels. |
| group_dimensions | Prototype six-vector. |
| Six axes | physicality, sociality, temporality, intentionality, materiality, spatiality. |
| meaning_semantics (M) | Current six-vector stand-in (not a literal name string). |
| Ranking / final_rank_order | Order among map candidates only. |
| selected_group_id | Rank-1 group used as first M. |
| CIE / identity_envelope | Local pressure on M; not listener uptake. |
| identity_tags | Coarse stance tags. |
| identity_vector (I) | Numeric pressure in M' = M + alpha I. |
| identity_importance (alpha) | How hard CIE pushes. |
| identity_delta | Change of I across cycles. |
| meaning_delta_h | ||M_i - M_{i-1}||; machine analogue of consequence. |
| Search budget | Cycle bounds (4-6 here). |
| resolution_status | Named halt: stable / identity_stable / budget_exhausted / time_exhausted. |
| ready_for_ouba | Handoff flag; bench stops. |
| IdOB | Crossing site: structure in, speaker-object stand-in out. |
| Path A (this bench) | Machine realizing the unproven structure-to-meaning theory. |

Lesson nicknames that are not packet fields stay out of this glossary.
