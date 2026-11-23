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

## 8A) Characterization-Space Research Roadmap

This section records the dependency structure required to characterize Category Selection space under the objective already stated in this plan (vary E and K while keeping M stable where architecture permits).

Each stage is gated. Continuation is not automatic merely because a later stage is listed.

**Local-readiness principle:** Local readiness is sufficient. Unknown global extent does not disqualify a bounded, experimentally defensible axis when subsequent controlled experimentation can expose where that local ordering ceases to hold. Local controllability must not be extrapolated into a global property.

Process:

establish local ordering → measure → extend → challenge → find the edge

**Stages:**

1. **Characterization-Readiness Audit** (read-only). Determine what the current realization can vary and measure (probe readiness, control readiness, measurement readiness). Exit with A/B/C/D verdict. No changes to the realization.
2. **Identify legitimate experimental axes.** Declare only axes the audit shows can move from x_i to x_{i+1} in a known direction while holding other important variables sufficiently constant. Discrete comparisons remain discrete.
3. **Resolve only demonstrated capability gaps (optional).** Skip if usable ordered controls already exist. Any extension of Category Selection requires independent architectural justification and becomes a new explicitly identified realization. Do not modify the mechanism merely to produce a hoped-for shape.
4. **Build the role-qualified probe set.** Produce the thin experimental-vocabulary reference for the axes that will actually be manipulated.
5. **Establish adequate measurement resolution.** Determine which required measurements already exist with useful resolution, which can be derived, and which require instrumentation. Unavailable quantities remain explicitly unavailable.
6. **Calibrate with small exploratory sweeps.** Discourse-side exploratory probes (not formal observations) on candidate axes. All outcomes are legitimate findings.
7. **Formal controlled sweeps.** GitHub Agent executes bounded batches on approved ordered sequences, preserves artifacts, stops on predefined anomalies.
8. **Characterize interactions among axes.** Only after individual axes are understood.
9. **Characterize interior, boundaries, and limits of Category Selection space.** Including the distinction between adequately supported evidence, weak/ambiguous support among available categories, and evidence poorly represented by the inventory itself. Inability to separate the latter conditions is recorded as an architectural gap.

Stage 1 findings are recorded in a separate document (`category_selection_characterization_readiness_audit.md`) once produced. That document owns the factual capability map; this section owns the roadmap.

## 8B) Controlled evolution of the characterization surface

Category Selection characterization should expect the experimental research surface to evolve. Vocabulary, sentences, constructions, controls, categories, probes, measurements, parameters, and experiment sets may expand or be revised as characterization progresses. The characterization foundation should favor scalable extension and bounded refactoring rather than repeated reconstruction of experimental infrastructure.

This principle does not prohibit major refactoring when controlled evidence requires it. When substantial refactoring is necessary, its empirical motivation, architectural scope, affected assumptions or prior evidence, preserved invariants, and required revalidation should be made explicit. Revalidation must identify what prior evidence remains applicable, what needs rechecking, what is superseded, and what invariants are intentionally preserved.

Strategic expansion of the experimental palette (words, sentences, constructions, controls, categories) should be driven by characterization needs. Progressively broader controlled palettes and category inventories are preferred when evidence supports extension, but revision, contraction, or replacement remains legitimate. The present palette and inventory are not treated as final. Conceptual progressions such as P1 ⊂ P2 ⊂ P3 … and K1 ⊂ K2 ⊂ K3 … are illustrative only and non-normative.

This principle applies primarily to research content and characterization infrastructure. It does not require the Category Selection mechanism or underlying architectural structure to remain unchanged; those remain subject to the structural-confidence criterion in Section 13. Evidence that the basic structural model is inadequate is a legitimate research result.

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

### Structural-confidence objective

Closeout does not require Category Selection to be complete, globally characterized, or frozen against later refinement.

The research program should establish sufficient controlled evidence that the underlying Category Selection structure is reasonably credible for continued downstream work.

Later revisions to boundaries, parameters, measurements, vocabulary, category inventories, and local behaviors are compatible with successful closeout.

Intended threshold: the accumulated controlled evidence indicates that remaining and reasonably anticipated limitations are more consistent with bounded extension, parameterization, measurement improvement, or local refinement than with the need for wholesale reconstruction of the Category Selection process.

If controlled characterization continues to leave the basic structural model materially in doubt, closeout is deferred and the structural question is investigated further.

This is a research-confidence and progression criterion, not proof that the architecture is correct, complete, or final.

### Closeout review

Closeout should require explicit review that:

- all planned experiment families were executed or explicitly deferred with reason
- observed behaviors were separated from interpretation
- B vs C separability was assessed and recorded
- architectural-generality evidence and mechanism-change accounting were recorded
- unresolved anomalies and confidence limits were explicitly listed
- the accumulated evidence does not indicate that the basic Category Selection structure may require fundamental reconstruction rather than bounded refinement

If the basic structural model remains materially in doubt, closeout is deferred. Do not close out Category Selection merely because the planned characterization work has been completed.

Confidence/closeout remains a review decision, not an automatic score threshold in this plan.

## 14) Current-software modification-map procedure (historical)

This procedure predates the Characterization-Space Research Roadmap in section 8A. It is retained for historical context. It is not the same as Stage 1 of that roadmap (the Characterization-Readiness Audit).

Before any bounded implementation contract is expanded:

1. Build a current-software modification map over current code/config pathways.  
2. Identify candidate touchpoints, ownership boundaries, and non-mutation walls.  
3. Map required observability outputs and fixture support needs.  
4. Identify required stop/review gates before implementation.

This mapping procedure is not created in this document.

## 15) Relationship to the later program reference

After the current-software mapping/review described in section 14, two coordinated software references carry distinct responsibilities:

- [category_selection_program_reference.md](category_selection_program_reference.md): bounded category-selection realization contract.
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md): bounded characterization instrumentation/framework contract for experiments and characterization support.

## 16) Post-category research gate

After confidence/closeout review, the next research question must be selected from observed evidence, limitations, and anomalies rather than prewritten conclusions.

## 17) Required future documents

- [category_selection_program_reference.md](category_selection_program_reference.md) (bounded realization contract; update as implementation evolves)
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md) (bounded characterization instrumentation/framework contract; update as implementation evolves)
- [category_selection_observation.md](category_selection_observation.md) (placeholder now; later empirical record from actual runs)
- [category_selection_characterization_milestone1_closeout.md](category_selection_characterization_milestone1_closeout.md) (Milestone-1 infrastructure closeout evidence)
- GitHub Agent implementation plan (after the current-software mapping described in section 14 and review)

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
