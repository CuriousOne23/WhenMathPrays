# IdOB Relational-Space Localization: Information/Representation Sufficiency Characterization Proposal

**Date:** 2026-11-27  
**Status:** Authorized research question/proposal (non-normative).  
**Purpose:** Open the next bounded localization cycle at proposal and mechanical-design stage only.

This document does not authorize implementation, execution, HOW-2, Gate C, production selector realization, or Category/YAML integration.

## 1) Frozen research question

Under the same frozen organizational layer, what information, if any, must a bounded runtime representation preserve for organizational localization leverage of the kind demonstrated by Gate A to remain recoverable in principle?

## 2) Operational definition

For this characterization, **recoverable in principle** means that a deterministic decoder, receiving only the frozen runtime representation, fixed group IDs, and `k`, emits an activation satisfying the same frozen leverage/dominance criterion used for the comparable Gate A/Gate B fixture.

This does **not** mean:

- Path A can generate the representation;
- the representation is available from permitted production inputs;
- a production selector exists;
- HOW-2 has been identified;
- the representation constitutes meaning;
- a satisfactory non-oracle realization necessarily exists.

## 3) Relationship to any future HOW-2

This characterization does not define or authorize HOW-2. It establishes the information and representation boundary that any future HOW-2 would have to respect and characterizes which tested distinctions, if any, must cross that boundary for localization leverage to remain recoverable within the frozen fixture.

A successful representation condition may become a constraint or research target for a later, separately authorized cycle. It is not itself a selector design.

## 4) Frozen controls and intended variable

Hold fixed:

- the same eight organizational groups;
- stable relation identities;
- cardinality, overlap, and `k` schedules;
- necessary-set construction;
- active-surface union;
- exhaustive matched size-`k` baselines;
- coverage and reduction measurements;
- ordered trace requirements;
- exact replay requirements;
- runtime information boundary;
- the same comparable leverage/dominance criterion used in Gate A/Gate B.

Intended variable:

- activation-relevant distinction preserved by runtime representation.

## 5) Outcome model

Per tested representation level, classify as:

- **SUFFICIENT_WITHIN_FIXTURE**
- **INSUFFICIENT_WITHIN_FIXTURE**
- **INCONCLUSIVE**

Do not replace per-level outcomes with a single aggregate label that hides where distinctions were lost.

The null outcome is explicitly allowed:

No tested reduced representation preserved enough distinction to recover the frozen leverage.

Even success for lossless controls establishes only that oracle-derived exact activation information can be represented across the runtime boundary within the fixture. It does not establish production availability or producibility of that information.

## 6) Explicit non-claims

This characterization cannot establish:

- that Path A can generate a successful representation;
- that successful information is available from production inputs;
- that a production selector exists;
- that the frozen organizational layer is optimal or necessary;
- that the representation is meaning;
- that a satisfactory non-oracle solution necessarily exists;
- that HOW-2 should begin;
- that Gate C should begin.

## 7) Authorization state for this cycle

- **Research question/proposal: AUTHORIZED**
- **Mechanical-design development: AUTHORIZED**
- **Pre-execution design review: REQUIRED**
- **Implementation: NOT AUTHORIZED**
- **Execution: NOT AUTHORIZED**
- **HOW-2: NOT AUTHORIZED**
- **Gate C: NOT AUTHORIZED**
- **Production selector / Category / YAML integration: NOT AUTHORIZED**

This authorization is intentionally limited to documentation and mechanical experimental design.
