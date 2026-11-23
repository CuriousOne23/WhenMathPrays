# Category Selection Controlled Experimental Palette v1

**Document:** notes/program/category_selection_controlled_palette_v1.md  
**Status:** Implemented and configuration-verified (non-normative). Not yet experimentally characterized.  
**Date:** 2026-11-23  
**Governing context:** [category_selection_stage2_axis_and_coverage_reference.md](category_selection_stage2_axis_and_coverage_reference.md); [category_selection_research_plan.md](category_selection_research_plan.md) (8A, 8B, 13).  
**Purpose:** Own the first-generation controlled experimental palette designed to satisfy the Stage 2 minimum meaningful coverage requirements. Separates approved design from current implementation state.

## Purpose and scope

Provide a strategically varied, role-qualified palette sufficient to challenge Category Selection structure and accumulate meaningful confidence for continued TS development. Exhaustive characterization is not the objective.

## Experimental Palette Space

The controlled palette is not limited to the current canonical probes. The allowable research surface includes qualified variation in:

- category identity
- lexical cue identity
- sentence-internal versus prior-context source
- source composition
- construction/scaffold
- matched non-cue controls
- competing-category combinations
- deliberately limited or boundary-adjacent probes
- category inventory composition where separately authorized

A palette member is allowable only when its experimental role, source compatibility, upstream structural treatment, cue mapping, known limitations, and applicable controls are explicitly qualified.

Expansion of this space does not itself authorize changes to Category Selection scoring, weights, thresholds, selection policy, or mechanism behavior. Such changes require independent architectural justification.

Palette v1 occupies a deliberately bounded subset of this allowable space. Future palette versions may expand, revise, contract, or replace portions of that subset as characterization evidence requires.

Relationship:

allowable experimental palette space ⊃ Palette v1 ⊃ particular experiment batch

## Relationship to Stage 2

Satisfies the core confidence skeleton:
- Ordered response (source-composition axis)
- Structural generality across categories
- Competition (discrete)
- Robustness to probe realization
- Edge pressure (placeholders deferred; clean mapped/unmapped boundary is addressable with existing controls; deeper edge pressure remains separately designed)

## Canonical categories and lexical probes

| Category | Canonical probe | Qualification status |
|----------|-----------------|----------------------|
| Affective | `cold` | Qualified and available |
| Physical | `table` | Canonical; dual-source mapping implemented |
| Perspectival | `place` | Canonical; dual-source mapping and token-class support implemented |

## Source-composition contract

Shared ordered axis for each canonical probe:

prior-only < sentence-only < both

(source-support contributions under fixed controls).

## Construction families

Category-appropriate scaffolds (experimental symmetry, not syntactic identity).

**Affective / `cold` (adjective)**  
- Canonical: "The sky is cold." / control "The sky is blue."  
- Alternate: "The sky stays cold." / control "The sky stays bright."  
- Status: implementation-ready.

**Physical / `table` (noun/object)**  
- Canonical: "The book is on the table." / control "The book is on the desk."  
- Alternate: "The book rests on the table." / control "The book rests on the desk."  
- Status: configuration-verified (`desk`, `rests`, `table` mapping present).

**Perspectival / `place` (noun/locative)**  
- Canonical: "The lamp is in the place." / control "The lamp is in the hall."  
- Alternate: "The lamp stays in the place." / control "The lamp stays in the hall."  
- Status: configuration-verified (`lamp`, `place`, `hall`, `place` mapping present).

## Matched controls

Controls are chosen per construction family and remain unmapped:
- Affective: `blue`, `bright`
- Physical: `desk`
- Perspectival: `hall`

## Competition contract

Discrete pairwise challenges (both source directions):

- Affective + Physical  
- Affective + Perspectival  
- Physical + Perspectival  

Residual lexical/structural differences are declared. Single-category versions of the same constructions serve as baselines.

## Historical / qualification-limited probes (retained, not canonical)

- Physical: `support`, `object`  
- Perspectival: `where`, `location`

## Candidate reserve (not added)

- Affective: `warm`, `sad`, `happy`  
- Physical: `stone`, `box`  
- Perspectival: `here`, `there`

## Required configuration additions

Completed in the bounded implementation batch:
- `token_classes.yaml`: `desk: NOUN`, `rests: VERB`, `lamp: NOUN`, `hall: NOUN`, `place: NOUN`
- `category_cues.yaml`: dual-source mapping of `table` → physical; dual-source mapping of `place` → perspectival

No Category Selection scoring, weight, threshold, or policy changes were made.

## Deferred edge-pressure requirements

Clean mapped/unmapped boundary is addressable with existing controls. Deeper edge pressure (weak/ambiguous support, inventory-inadequate cases, deliberately limited probes) remains separately designed and is not claimed as satisfied by ordinary non-cue controls.

## Palette versioning / controlled evolution

This is Palette v1. Future generations may expand or revise research content under Section 8B. Ordinary growth is extension; substantial refactoring requires explicit motivation, scope, affected evidence, invariants, and revalidation.

## Non-claims

This document does not characterize Category Selection space or establish global axes. Palette v1 is implemented and configuration-verified; it is not yet experimentally characterized.
