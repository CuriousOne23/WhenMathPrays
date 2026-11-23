# Category Selection Stage 7: Batch 1–4A Formal Campaign

**Document:** notes/program/category_selection_stage7_batch1_4a_campaign.md  
**Status:** Frozen execution matrix (non-normative). Batch 1 authorized for formal execution; later batches not yet authorized.  
**Date:** 2026-11-23  
**Governing context:** [category_selection_controlled_palette_v1.md](category_selection_controlled_palette_v1.md); [category_selection_stage2_axis_and_coverage_reference.md](category_selection_stage2_axis_and_coverage_reference.md).  
**Purpose:** Own the frozen Stage 7 formal characterization campaign (Batches 1–4A) that uses Palette v1. Separates campaign specification from empirical observation records.

## Authorization rule

Batches are authorized and reviewed one at a time. Completion of a batch does not automatically authorize the next. Batch 4B and inventory composition remain deferred.

## Measurement limits

Authorized measurements: post-softmax distribution, top category, category confidence, rationale, provenance.  
Not authorized: entropy, top-versus-second margin, fine interior geometry, separation of weak-support versus inventory-inadequate conditions.

## Batch 1 — Reference ordered response (`cold` / affective)

| ID | Category | Probe | Source state | Sentence | Prior context | Control | Controlled variable | Invariants | Measurements | Authorized interpretation | Stop condition |
|----|----------|-------|--------------|----------|---------------|---------|---------------------|------------|--------------|---------------------------|----------------|
| B1-1 | affective | cold | prior-only | The sky is blue. | cold | — | source composition | no sentence cue, inventory fixed | distribution, top, confidence, provenance | local ordering start | cue contamination or missing prior cue |
| B1-2 | affective | cold | sentence-only | The sky is cold. | (empty) | — | source composition | no prior cue | same | local ordering middle | cue contamination or missing sentence cue |
| B1-3 | affective | cold | both | The sky is cold. | cold | — | source composition | both cues present | same | local ordering end | ordering collapses relative to B1-1/B1-2 |
| B1-4 | affective | cold | sentence-only | The sky stays cold. | (empty) | blue | construction robustness | same major, alternate scaffold | same | limited construction robustness for sentence-only affective evidence | alternate scaffold changes cue identity/source unexpectedly, changes the selected category unexpectedly, or produces a materially inconsistent response requiring research review |
| B1-5 | affective | (control) | sentence-only | The sky is blue. | (empty) | blue | non-cue baseline | no category cue | same | mapped vs unmapped baseline | control produces category cue |

**Batch 1 stop:** any case fails its stop condition, or the three-point ordering prior < sentence < both is not observed.

## Batch 2 — Cross-category generality

| ID | Category | Probe | Source state | Sentence | Prior context | Control | Controlled variable | Invariants | Measurements | Authorized interpretation | Stop condition |
|----|----------|-------|--------------|----------|---------------|---------|---------------------|------------|--------------|---------------------------|----------------|
| B2-1 | physical | table | prior-only | The book is on the desk. | table | — | source composition | no sentence cue | distribution, top, confidence, provenance | category generality | missing or wrong cue |
| B2-2 | physical | table | sentence-only | The book is on the table. | (empty) | — | source composition | no prior cue | same | category generality | missing or wrong cue |
| B2-3 | physical | table | both | The book is on the table. | table | — | source composition | both cues | same | category generality | ordering collapses |
| B2-4 | perspectival | place | prior-only | The lamp is in the hall. | place | — | source composition | no sentence cue | same | category generality | missing or wrong cue |
| B2-5 | perspectival | place | sentence-only | The lamp is in the place. | (empty) | — | source composition | no prior cue | same | category generality | missing or wrong cue |
| B2-6 | perspectival | place | both | The lamp is in the place. | place | — | source composition | both cues | same | category generality | ordering collapses |

**Batch 2 stop:** either major fails to show the local three-point ordering under the same controls used for `cold`.

## Batch 3 — Robustness + competition

| ID | Categories | Probes | Source state | Sentence | Prior context | Controlled variable | Invariants | Measurements | Authorized interpretation | Stop condition |
|----|------------|--------|--------------|----------|---------------|---------------------|------------|--------------|---------------------------|----------------|
| B3-1 | physical | table | both | The book rests on the table. | table | construction robustness | alternate scaffold | distribution, top, confidence | robustness | alternate scaffold changes the intended cue/provenance, changes the expected category identity, or produces a materially inconsistent distribution/confidence response relative to the canonical both-source condition that requires research review |
| B3-2 | perspectival | place | both | The lamp stays in the place. | place | construction robustness | alternate scaffold | same | robustness | alternate scaffold changes the intended cue/provenance, changes the expected category identity, or produces a materially inconsistent distribution/confidence response relative to the canonical both-source condition that requires research review |
| B3-3 | affective+physical | cold, table | mixed | The book is on the table. | cold | competition | one direction | same | first-order competition | non-interpretable collapse |
| B3-4 | affective+perspectival | cold, place | mixed | The lamp is in the place. | cold | competition | one direction | same | first-order competition | non-interpretable collapse |
| B3-5 | physical+perspectival | table, place | mixed | The lamp is in the place. | table | competition | one direction | same | first-order competition | non-interpretable collapse |

**Batch 3 stop:** any alternate scaffold fails its stop condition, or any competition pair produces non-interpretable distribution collapse.

## Batch 4A — Clean representability boundary

| ID | Category | Probe | Source state | Sentence | Prior context | Control | Controlled variable | Invariants | Measurements | Authorized interpretation | Stop condition |
|----|----------|-------|--------------|----------|---------------|---------|---------------------|------------|--------------|---------------------------|----------------|
| B4A-1 | affective | cold | sentence-only | The sky is cold. | (empty) | — | mapped evidence | clean scaffold | distribution, top, confidence | mapped baseline | — |
| B4A-2 | (none) | (control) | sentence-only | The sky is blue. | (empty) | blue | unmapped control | identical scaffold | same | clean local mapped/unmapped representability boundary | control produces category cue |

**Batch 4A stop:** mapped and unmapped cases cannot be distinguished with available measurements.

## Deferred

- Batch 4B (deeper edge pressure: weak/ambiguous, qualification-limited, or inventory-inadequate conditions)
- Inventory composition

## Non-claims

This campaign does not characterize Category Selection space exhaustively, establish global axes, or authorize Batch 4B. Stage 6 calibration confirmed operational expressibility only; formal characterization begins with Batch 1.
