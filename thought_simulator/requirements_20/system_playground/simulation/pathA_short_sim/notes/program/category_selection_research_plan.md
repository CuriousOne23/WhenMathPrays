# Category Selection Research Plan

**Document:** notes/program/category_selection_research_plan.md  
**Status:** Research / experimental plan. Non-normative. Not an implementation contract.  
**Date:** 2026-11-21  
**Purpose of this document:** Freeze the research questions and experimental discipline for the next category-selection cycle, not the answers.

## 1) Purpose

Define a controlled, replayable, and challengeable category-selection characterization program that can produce positive, negative, ambiguous, or architecture-limiting outcomes.

## 2) Background and relationship to completed Phase IV category-structure observations

The prior bounded Phase IV cycle is closed in [category_structure_observation.md](category_structure_observation.md).  
This plan starts the successor cycle for category selection while preserving the completed Phase IV observations and conclusions as historical record.

## 3) Normative authorities

Normative behavior and ownership remain in:

- [20.45_ts_isc_scoring.md](../../../20.45_ts_isc_scoring.md)
- [20.105_tp_requirements.md](../../../20.105_tp_requirements.md)
- [20.116.010_tp_envelope_index.md](../../../20.116.010_tp_envelope_index.md)
- [20.40.050_idob_prim.md](../../../20.40.050_idob_prim.md)

Related program context:

- [category_selection_proposal.md](category_selection_proposal.md)
- [category_structure_observation.md](category_structure_observation.md)
- [s2m_relational_proposal.md](s2m_relational_proposal.md)
- [s2m_program_reference.md](s2m_program_reference.md)

This plan does not modify normative requirements.

## 4) Central research question

“Can a stable, observable mechanism discriminate among changing category spaces, expose the limits of those spaces, preserve uncertainty when warranted, remain separate from meaning legitimation, and tell us through observation when its existing representation is no longer adequate?”

## 5) Claim / epistemic boundary

- Objective is characterization, not proof.
- Observations characterize current architecture behavior under controlled conditions.
- This plan does not pre-commit scientific conclusions.
- This plan does not authorize requirement changes by itself.

## 6) Experimental principles

This program requires explicit and separate treatment of:

- tractability
- measurability
- understandability
- determinism
- falsifiability/challengeability
- architectural boundedness
- provenance preservation
- generalization
- architectural generality

Generalization asks whether behavior remains coherent on new examples within a substantially fixed category/candidate space.

Architectural generality asks whether category/candidate content can be added, removed, or reorganized without category-specific redesign of the core mechanism.

Conceptual expression:

M(E,K) -> D_K

Where M = selection mechanism, E = evidence, K = available category/candidate space, D_K = resulting distribution.

Experimental objective: vary E and K while attempting to keep M unchanged where architecture permits, and record exactly how much M had to change.

## 7) Confidence dimensions

Confidence is multi-dimensional, not a single percentage:

- contract adherence
- selection behavior consistency
- meaning-transition discipline
- preservation of default-versus-extension distinctions
- provenance distinguishability
- architectural-generality/change-accounting robustness
- boundary/stability behavior near support transitions

## 8) Experimental program

Required controlled families:

A. No-cue baseline / non-interference  
B. Single clear cue  
C. Cue reversal / controlled evidence variation (necessary but weak alone)  
D. Sentence-internal versus prior-context provenance  
E. Competing evidence / ambiguity  
F. Weak or insufficient evidence  
G. Category result but no applicable candidate  
H. Category relevance but S2M refusal (critical: category relevance != meaning legitimation)  
I. Distractor robustness  
J. Minimal perturbation / boundary sweeps  
K. Deterministic replay  
L. Controlled expansion/generalization  
M. Withheld-from-development / added-as-data category  
N. Runtime-unavailable category / inventory inadequacy experiment

The architecture distinction remains explicit:

cue evidence -> category scoring -> committed category result -> candidate relevance/consideration -> S2M legitimation or refusal -> selected interpretive extension (if any)

## 9) Category-support boundary and unsupported-space characterization

Research sequence is:

observe -> characterize -> design

Not:

design threshold -> run experiments that rediscover threshold

This plan investigates whether support boundary behavior is threshold-like, gradient-like, broad-ambiguous, inventory-sensitive, multi-dimensional, overlapping, unstable over sequences, or otherwise unanticipated.

Controlled runs should vary where practical:

- evidence strength
- competing evidence
- candidate composition
- category inventory composition
- category availability
- repeated/sequential evaluations near apparent transition regions

Observe existing quantities such as:

- normalized distribution
- top category
- top-versus-second margin
- entropy
- confidence
- rationale
- provenance
- downstream candidate relevance
- legitimation/refusal
- final participation/composite

Conceptual distinctions to test (without assuming current realization can fully separate them):

A. Category exists and evidence adequately supports it.  
B. Evidence exists but support among available categories is weak/ambiguous/inadequate.  
C. Evidence appears poorly represented by available category inventory itself.

If current outputs cannot separate B from C, record that as an architectural observation/gap.

## 10) Architectural-generality experiments

Explicitly investigate:

- withheld categories
- later addition solely through data
- category inventory expansion
- category inventory removal
- unfamiliar combinations
- candidate inventory changes
- whether category-specific procedural code was required
- whether category-specific knowledge remains data wherever normative architecture permits

Desired invariant:

Category-specific knowledge should be represented as data wherever the existing normative architecture permits. The core category-selection mechanism should not contain category-specific procedural branches unless explicitly required by normative architecture.

If current implementation/requirements force otherwise, record it as an architectural observation.

## 11) Measurement framework

Measurements are grouped as:

1. Contract measurements  
2. Selection measurements  
3. Meaning-transition measurements  
4. Preservation measurements  
5. Provenance measurements  
6. Architectural-generality/change-accounting measurements  
7. Boundary/stability measurements

No new normative TP fields are defined by this plan.

## 12) Failure/anomaly classification

Classify and preserve:

- contract violations
- deterministic replay failures
- provenance collapse/erasure
- relevance/legitimation boundary confusions
- unsupported-inventory indications
- boundary-instability oscillations
- architecture-forcing anomalies (required category-specific mechanism changes)

Anomalies are findings, not silent noise.

## 13) Category-selection confidence / closeout gate

Closeout should require explicit review that:

- all planned experiment families were executed or explicitly deferred with reason
- observed behaviors were separated from interpretation
- B vs C separability was assessed and recorded
- architectural-generality evidence and mechanism-change accounting were recorded
- unresolved anomalies and confidence limits were explicitly listed

Confidence/closeout remains a review decision, not an automatic score threshold in this plan.

## 14) Stage-1 current-software modification-map procedure

Before any bounded implementation contract is expanded:

1. Build a Stage-1 current-software modification map over current code/config pathways.  
2. Identify candidate touchpoints, ownership boundaries, and non-mutation walls.  
3. Map required observability outputs and fixture support needs.  
4. Identify required stop/review gates before implementation.

This Stage-1 map is the next task after this plan. It is not created in this document.

## 15) Relationship to the later program reference

After Stage-1 mapping/review, two coordinated placeholder software references carry distinct responsibilities:

- [category_selection_program_reference.md](category_selection_program_reference.md): bounded category-selection realization contract.
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md): bounded characterization instrumentation/framework contract for experiments and characterization support.

## 16) Post-category research gate

After confidence/closeout review, the next research question must be selected from observed evidence, limitations, and anomalies rather than prewritten conclusions.

## 17) Required future documents

- [category_selection_program_reference.md](category_selection_program_reference.md) (placeholder now; later bounded realization contract)
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md) (placeholder now; later characterization instrumentation/framework contract)
- [category_selection_observation.md](category_selection_observation.md) (placeholder now; later empirical record from actual runs)
- GitHub Agent implementation plan (after Stage-1 map and review)

## Category-selection document family

For the complete category-selection document map, document roles, authority relationships, software references, characterization documents, and observation records, see:

[category_selection_index.md](category_selection_index.md)

## 18) Explicit non-goals

This plan does **not**:

- implement category selection
- implement a no-category decision function
- select thresholds, confidence regions, entropy/margin formulas, hysteresis, or persistence mechanisms
- prescribe final unsupported-space handling behavior
- alter executable code, YAML/JSON data, schemas, tests, simulator behavior, or normative requirements
- fabricate experimental outcomes or expected observations
