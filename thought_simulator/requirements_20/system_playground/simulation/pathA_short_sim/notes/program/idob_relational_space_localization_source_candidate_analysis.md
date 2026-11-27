# IdOB Relational-Space Localization Source-Candidate Analysis

**Date:** 2026-11-27  
**Status:** Completed and recorded research analysis (non-normative).  
**Purpose:** Record candidate-source inventory and independent status dimensions without selecting a localization source or granting localization authorization.

This document is analysis only. It does not authorize localization access, source selection, representation design, experiment design, or implementation.

## 1) Governing distinctions

`present != readable != research-eligible != localization-authorized != sufficient`

and

`present before localization != authorized for localization != sufficient for localization`

No dimension is inferred from another.

## 2) Candidate-source inventory

Candidate classes inventoried as known pre-IdOB information or established prior-cycle state, subject to current authority boundaries:

- intake / IE envelope;
- correction-selected TP state, when present;
- utterance carrier;
- structural substrate through `SOB -> SROB -> CnOB -> SmOB -> SSG`;
- frozen structural vector / six IDs / structural-key components, where assigned;
- routing metadata / `routing_filter` / `routing_update` / committed routing context;
- CIE material, when present;
- prior-cycle IdOB / lineage state;
- continuity / COB / CIL / CST state.

## 3) Independent status dimensions by candidate class

| Candidate class | Presence before IdOB | Existing read authority | Research eligibility | Localization authorization | Experimentally demonstrated sufficiency | Provenance classification |
|---|---|---|---|---|---|---|
| Intake / IE envelope | Yes | Existing per-envelope readers under current contracts | Yes (research candidate class) | No | No | CLEAN_PRE_LOCALIZATION |
| Correction-selected TP state (when present) | Conditional (when produced) | Existing per-envelope readers under current contracts | Not currently selected as active class | No | No | CLEAN_PRE_LOCALIZATION (when present) |
| Utterance carrier | Yes | Existing readers under current contracts | Yes (research candidate class) | No | No | CLEAN_PRE_LOCALIZATION |
| Structural substrate (`SOB -> SROB -> CnOB -> SmOB -> SSG`) | Yes | Existing readers under current contracts (including IdOB context reads where authorized) | Yes (research candidate class) | No | No | CLEAN_PRE_LOCALIZATION |
| Frozen structural identifiers/components (where assigned) | Conditional by fixture/runtime assignment | Existing reads only where already defined | Included with structural class; not selected separately | No | No | CLEAN_PRE_LOCALIZATION (when present) |
| Routing metadata / committed routing context | Yes | Existing readers under current contracts (IdOB read-only where specified) | Yes (research candidate class) | No | No | CLEAN_PRE_LOCALIZATION |
| CIE material (row presence vs application) | Row/data may be present in relevant state | Read per existing envelope boundaries | Candidate/hypothetical for this question | No | No | Temporal-dependent; not promoted to current-cycle localization input |
| Prior-cycle IdOB / lineage state | Prior-cycle / historical class | Read as continuity/replay lineage where authorized | Inventory only (separate temporal class) | No | No | CLEAN_PRE_LOCALIZATION (historical/prior-cycle provenance) |
| Continuity / COB / CIL / CST state | May exist pre-IdOB depending on flow point and envelope | Read/write limited by strict ownership walls | Inventory only (separate temporal class for this cycle) | No | No | CLEAN_PRE_LOCALIZATION where established |

Notes:

- Historical/prior-cycle sources remain temporal/prior-cycle and are not collapsed into current-cycle candidate classes.
- CIE retains the distinction between row existence and later application inside IdOB.

## 4) Research-eligible current-cycle candidate classes

Identified for deeper research-only consideration:

- structural substrate / frozen structural identifiers;
- routing metadata / committed routing context;
- intake / utterance carrier.

These are research-eligible candidates only. They are not localization inputs.

No ranking is assigned. No selection is made.

## 5) Boundary and non-authorization record

Characterization may identify a required architectural change. It must not silently make that change.

This analysis does not:

- grant localization read/access authority;
- select a localization source;
- establish sufficiency;
- modify Path A normative architecture.
