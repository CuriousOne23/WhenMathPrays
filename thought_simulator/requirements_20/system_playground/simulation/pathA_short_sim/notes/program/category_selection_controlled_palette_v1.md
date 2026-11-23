# Category Selection Controlled Experimental Palette v1

**Document:** notes/program/category_selection_controlled_palette_v1.md  
**Status:** Design record (non-normative). Implementation not yet authorized.  
**Date:** 2026-11-23  
**Governing context:** [category_selection_stage2_axis_and_coverage_reference.md](category_selection_stage2_axis_and_coverage_reference.md); [category_selection_research_plan.md](category_selection_research_plan.md) (8A, 8B, 13).  
**Purpose:** Own the first-generation controlled experimental palette designed to satisfy the Stage 2 minimum meaningful coverage requirements. Separates approved design from current implementation state.

## Purpose and scope

Provide a strategically varied, role-qualified palette sufficient to challenge Category Selection structure and accumulate meaningful confidence for continued TS development. Exhaustive characterization is not the objective.

## Relationship to Stage 2

Satisfies the core confidence skeleton:
- Ordered response (source-composition axis)
- Structural generality across categories
- Competition (discrete)
- Robustness to probe realization
- Edge pressure (placeholders deferred)

## Canonical categories and lexical probes

| Category | Canonical probe | Qualification status |
|----------|-----------------|----------------------|
| Affective | `cold` | Already qualified/available |
| Physical | `table` | Canonical; Category Selection mapping pending |
| Perspectival | `place` | Canonical and qualification-approved; token-class and cue configuration pending |

## Source-composition contract

Shared ordered axis for each canonical probe:

prior-only < sentence-only < both

(source-support contributions under fixed controls).

## Construction families

Category-appropriate scaffolds (experimental symmetry, not syntactic identity).

**Affective / `cold` (adjective)**  
- Canonical: "The sky is cold." / control "The sky is blue."  
- Alternate: "The sky stays cold." / control "The sky stays bright."  
- Status: implementation-ready as-is.

**Physical / `table` (noun/object)**  
- Canonical: "The book is on the table." / control "The book is on the desk."  
- Alternate: "The book rests on the table." / control "The book rests on the desk."  
- Status: design-qualified; pending `desk` and `rests` token-class support plus `table` cue mapping.

**Perspectival / `place` (noun/locative)**  
- Canonical: "The lamp is in the place." / control "The lamp is in the hall."  
- Alternate: "The lamp stays in the place." / control "The lamp stays in the hall."  
- Status: design-qualified; pending `lamp`, `place`, and `hall` token-class support plus `place` cue mapping.

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

Ordinary research/configuration content only:
- `token_classes.yaml`: `desk: NOUN`, `rests: VERB`, `lamp: NOUN`, `hall: NOUN`, `place: NOUN`
- `category_cues.yaml`: dual-source mapping of `table` → physical; dual-source mapping of `place` → perspectival

No Category Selection scoring, weight, threshold, or policy changes.

## Deferred edge-pressure requirements

Unmapped negative controls and inventory-unavailable cases are identified but outside the first implementation batch.

## Palette versioning / controlled evolution

This is Palette v1. Future generations may expand or revise research content under Section 8B. Ordinary growth is extension; substantial refactoring requires explicit motivation, scope, affected evidence, invariants, and revalidation.

## Non-claims

This document does not characterize Category Selection space, establish global axes, or authorize implementation. Design and implementation state remain distinct.
