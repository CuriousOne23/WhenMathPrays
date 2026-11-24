# Category Selection Program Reference

**Document:** notes/program/category_selection_program_reference.md  
**Status:** Authoritative realization/process reference for the current bounded Category Selection mechanism (non-normative).  
**Date:** 2026-11-24

## 1) Purpose

Define the current bounded Category Selection realization on the Path A short simulator so a future agent can reconstruct:

1. how the mechanism currently works,  
2. which normative requirements govern it,  
3. where implementation/configuration ownership resides,  
4. which parameters and dependencies are active in this realization,  
5. which inputs/outputs and commit boundaries are present, and  
6. where known conformance gaps and unresolved scope boundaries remain.

This document is realization/process authority for the bounded software mechanism.  
Normative equations and SHALL-level requirements remain owned by the 20-series authorities listed below.

## 2) Category-selection document family

For the complete category-selection document map, document roles, authority relationships, software references, characterization documents, and observation records, see:

[category_selection_index.md](category_selection_index.md)

## 3) Authority hierarchy and scope

### 3.1 Normative requirements authorities (own requirements/equations/field authority)

- [20.45_ts_isc_scoring.md](../../../20.45_ts_isc_scoring.md)
- [20.105_tp_requirements.md](../../../20.105_tp_requirements.md)
- [20.116.010_tp_envelope_index.md](../../../20.116.010_tp_envelope_index.md)
- [20.40.050_idob_prim.md](../../../20.40.050_idob_prim.md)

### 3.2 Program reference authority (this document)

This document owns the current bounded realization/process description and traceability to software/configuration evidence.  
It does not replace or amend normative authorities.

### 3.3 Implementation/configuration authorities (what current software does)

- Runtime orchestration: [pathA_short_simulator.py](../../pathA_short_simulator.py), [primitives_pathA_short.py](../../primitives_pathA_short.py)
- Category/S2M consumption path: [s2m/loop.py](../../s2m/loop.py), [s2m/propose.py](../../s2m/propose.py), [s2m/active_space.py](../../s2m/active_space.py), [s2m/legitimate.py](../../s2m/legitimate.py)
- Category cue and weight config: [support/dictionaries/category_cues.yaml](../../support/dictionaries/category_cues.yaml), [support/dictionaries/isc_weights.yaml](../../support/dictionaries/isc_weights.yaml)
- Category/candidate inventory config: [s2m/data/majors.yaml](../../s2m/data/majors.yaml), [s2m/data/spaces/default.yaml](../../s2m/data/spaces/default.yaml), [s2m/data/associations/](../../s2m/data/associations/)

### 3.4 Characterization/observation context (empirical; not mechanism definition)

- [category_selection_characterization_reference.md](category_selection_characterization_reference.md)
- [category_selection_controlled_palette_v1.md](category_selection_controlled_palette_v1.md)
- [category_selection_observation.md](category_selection_observation.md)
- [category_selection_characterization_program_closeout.md](category_selection_characterization_program_closeout.md)

Observed behavior in these documents does not define the algorithm or normative constants.

## 4) Related program context documents

- [category_selection_proposal.md](category_selection_proposal.md)
- [category_selection_research_plan.md](category_selection_research_plan.md)
- [category_selection_stage1_modification_map.md](category_selection_stage1_modification_map.md)
- [category_selection_characterization_milestone1_closeout.md](category_selection_characterization_milestone1_closeout.md)
- [category_structure_observation.md](category_structure_observation.md)
- [s2m_program_reference.md](s2m_program_reference.md)
- [user_guide.md](../../user_guide.md)

## 5) Realization relationship to characterization

Coordinated sibling references have distinct ownership:

- **This document** owns Category Selection realization/process description on the main path (cue intake, scoring, commit, read-only consumption boundary, and conformance traceability).
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md) owns characterization orchestration/instrumentation and characterization artifact/session discipline.

This document does **not** define characterization artifact/session contract details beyond realization surfaces characterization can observe.

Characterization documents record controlled empirical observations.  
They do not define mechanism equations, normative requirements, or realization constants.

## 6) Bounded realization scope

In scope:

- sentence-internal and prior-context cue intake on the current path,
- category scoring and normalized distribution,
- category result commitment into `TP.semantic.isc_category_result`,
- downstream read-only consumption by S2M/IdOB-adjacent flow,
- deterministic replay/inspection surfaces currently implemented.

Out of scope:

- generalized no-category policy design,
- weak-confidence threshold policy,
- hysteresis/persistence policy,
- unsupported/inventory-inadequate policy formalization,
- global Category Selection geometry claims,
- cross-language (Python/C++) equivalence scope decisions,
- characterization campaign/session management.

## 6A) Category Selection Framework v1 skeleton (structural, non-algorithmic)

### 6A.1 Purpose

Framework v1 records a stable process skeleton for Category Selection development/characterization without freezing final decision mathematics. It separates architectural structure from realization policy and research hypotheses, preserves unresolved behavior as information, keeps deterministic/replayable realization as a boundary condition, and provides a controlled extension boundary so future agents do not fill unresolved architecture by inference.

Guiding principle: freeze the structure of inquiry before freezing the answer that inquiry is intended to discover.

### 6A.2 Stage skeleton

`available authorized evidence -> candidate construction -> qualification -> evaluation -> competition/comparison -> selection policy -> result -> observability`

### 6A.3 Stage responsibilities (bounded)

1. **Available authorized evidence**  
   Owns the evidence Category Selection is permitted to consider (currently established: current utterance evidence and applicable prior-context/prior-utterance evidence), with reconstructable provenance.

2. **Candidate construction**  
   Constructs candidates from inventory + authorized evidence. Framework growth is inventory-oriented rather than category-specific procedural branching in the core selection framework.

3. **Qualification**  
   Determines whether candidate support is sufficient for eligibility in subsequent comparison. Qualification precedes information-resolution/numerical influence on selection.

4. **Evaluation**  
   Provides a reconstructable per-candidate evaluation surface. Framework v1 does not freeze final evaluator mathematics.

5. **Competition/comparison**  
   Preserves observable relationships among qualified candidates (clear separation, close competition, weak differentiation, unresolved comparison) rather than hiding them inside an opaque final scalar.

6. **Selection policy**  
   Consumes the qualified/evaluated set and produces current selection outcome. Framework v1 defines stage boundary/existence only; policy mathematics remain open.

7. **Result**  
   Keeps committed Category Selection result bounded to downstream Path A operational needs and preserves existing accepted result contract.

8. **Observability**  
   Preserves reconstructability/characterizability (including uncertainty/competition/unsupported/unresolved behavior) without changing committed selection semantics.

### 6A.3A Qualification Contract v1 (conceptual contract)

Definition:

Qualification determines whether a constructed category candidate has sufficient legitimate support from authorized evidence to remain eligible for evaluation and later selection. Qualification itself does not select a winner.

Ordering boundary:

`candidate construction -> qualification -> evaluation`

Qualification is an eligibility boundary, not a preference mechanism.

Minimum conceptual qualification states:
- `qualified`: sufficient legitimate support is established for evaluation eligibility.
- `not qualified`: sufficient basis exists to determine support is not legitimate for evaluation eligibility.
- `unresolved`: available authorized evidence is insufficient to determine qualification.

`unresolved` is not: partially qualified, low confidence, tied, rejected, no-category, or final non-selection.

### 6A.3B Qualification Evidence Contract v1 (semantic boundary contract)

At the `candidate construction -> qualification` boundary, the architectural evidence contract for each constructed candidate is:

1. **Candidate identity** (which category the candidate represents).
2. **Zero or more category-relevant evidence items** currently represented for that candidate.
3. **Authorized source attribution for every evidence item**.

This contract defines what information crosses the boundary, not what qualification does with that information.

Empty evidence collection rule:
- an empty category-relevant evidence collection means no category-relevant evidence is represented for that candidate at this boundary;
- it does **not** mean `not qualified`, `unresolved`, rejected, no-category, or any other qualification judgment.

Inventory relationship:
- candidate construction establishes candidacy (including inventory membership preconditions in the current realization);
- inventory membership is therefore not duplicated as qualification evidence;
- keep distinct:
  - candidate exists via candidate construction,
  - candidate has zero-or-more category-relevant evidence items.

Authorized-source provenance invariant:
- every category-relevant evidence item must remain attributable to an authorized source;
- sentence and prior context are currently realized authorized sources;
- the architectural contract remains extensible to additional authorized sources.

Current realized qualification observability fields are **not themselves** the Qualification Evidence Contract:
- `f_s`
- `f_b`
- `f_e`
- `f_i`
- `in_current_category_cue`

These remain legitimate current realization/diagnostic fields. In the current realization, `f_s`/`f_b` help manifest source contributions, cue-membership helps expose current cue relationship, and other feature fields remain realization/evaluation detail. For current field-level realization mapping, see [category_selection_framework_v1_realization_map.md](category_selection_framework_v1_realization_map.md).

Portability/growth boundary:
- this evidence contract is semantic, not language-specific;
- it must support equivalent realization in Python and C++ without requiring today's Python trace-field representation;
- ordinary growth (new inventory categories, additional authorized evidence sources, evolving evidence representation) should not require redefining the candidate-construction -> qualification boundary.

Relationship to current observability implementation:
- current Qualification v1 observability already exposes enough information to reconstruct this semantic evidence contract;
- current trace representation remains realization evidence, not normative architecture.

Explicitly excluded from Qualification v1:
- entropy/information-resolution quantities;
- downstream S2M legitimation results;
- quantities produced by candidate evaluation/scoring itself.

Minimum conceptual reconstructability surface for qualification:
- candidate identity;
- qualification state;
- support evidence used;
- evidence provenance;
- qualification rationale.

This is a conceptual observability contract only; it does not define TP schema, does not add fields to `TP.semantic.isc_category_result`, and does not make qualification records committed downstream semantic state.

Qualification Contract v1 preserves these open slots (not defined here):
- presence-of-evidence predicate;
- qualification-state assignment (`qualified`, `not qualified`, `unresolved`);
- qualification predicate/mathematics;
- binary vs graded internal support model;
- thresholds;
- evidence weights and evidence-combination mathematics;
- evidence counting or evidence strength interpretation;
- source preference policy;
- mathematical determination of `unresolved`;
- interaction with entropy;
- selection mathematics;
- generalized non-selection behavior.

Entropy boundary at qualification:
- entropy has no qualification authority;
- qualification precedes information-resolution influence;
- an unsupported candidate cannot become qualified because it might reduce entropy;
- entropy may later be an evaluation observable when measurement semantics are established.

First realization posture (future implementation, separately authorized):

Qualification v1 starts as observability-only and must preserve current behavior unchanged, including:
- current scores,
- current softmax distribution,
- current top_category,
- current category_confidence,
- current category_rationale,
- current committed TP result,
- current downstream S2M behavior.

### 6A.4 Framework invariants

- **Qualification ordering:** qualification precedes any potential information-resolution influence on selection.
- **Unsupported candidates:** unsupported categories cannot become selected solely because of favorable numerical evaluation.
- **Inventory-oriented growth:** category inventory is the growth mechanism, not category-specific core procedural branching.
- **Provenance traceability:** evidence used in construction/evaluation remains sufficiently traceable to reconstruct authorized source.
- **Competition visibility:** ambiguity and competition remain observable.
- **Characterization separation:** characterization instrumentation/records remain outside committed semantic state.
- **Determinism:** identical authorized inputs/configuration/inventory/realization policy must yield deterministic/replayable committed result.
- **Entropy ownership boundary:** entropy characterizes unresolved information in evolving utterance/TP state under the governing Path A entropy principle; Category Selection/ISc do not thereby own entropy architecturally.
- **Hole preservation:** unresolved conditions must remain observable rather than being erased by forced winner behavior.

### 6A.5 Hole/unresolved-condition boundary

Framework v1 preserves the possibility of observing (illustrative, not a frozen taxonomy): genuine competition, weak differentiation, inadequate evidence, inadequate inventory representation, conflicting evidence, weak information resolution, and unresolved conditions with not-yet-understood cause.

Framework v1 does not require runtime to classify every unresolved condition, does not define a default unresolved category, and does not define final committed non-selection representation/policy.

### 6A.6 Minimum conceptual per-candidate reconstructability surface

Framework v1 per-candidate evaluation must be capable of reconstructing, conceptually: category identity, evidence used, evidence provenance, qualification state, support summary available from current realization, optional information-resolution observations when legitimately available, and competition/separation context where computed.

This is a conceptual/reconstructability requirement, not authorization to add TP fields or force unavailable measurements.

### 6A.7 Entropy boundary in Framework v1

Established boundary preserved here:
- entropy concerns unresolved information in evolving utterance/TP state;
- entropy is not owned by Category Selection or ISc;
- historical Path A interpretation is bounded (`0 <= H <= 1`) with historical complement `1-H`;
- historical `H <= 0.25` was successful simulation behavior, not frozen architecture.

Framework v1 treatment:
- entropy is permitted as a characterization observable when properly defined;
- entropy is permitted as optional candidate-evaluation output once measurement semantics exist;
- entropy is **not** currently authorized to override qualification;
- entropy is **not** currently authorized as selection-policy input;
- entropy is **not** currently a qualification signal.

### 6A.8 Open policy slots (explicitly open)

- qualification mathematics;
- binary vs graded qualification;
- evaluation mathematics;
- entropy’s eventual role in candidate evaluation/selection;
- candidate-specific entropy semantics;
- information-resolution measurement semantics;
- competition mathematics;
- selection mathematics;
- thresholds;
- deterministic tie policy;
- generalized non-selection policy;
- representation of “no sufficiently differentiated winner”;
- additional future evidence sources;
- final characterization observables;
- entropy normalization;
- entropy carrier/state continuity;
- `H_previous`;
- `TP.process.first_cycle`.

These are open policy slots, not implementation omissions. Future agents must not choose defaults for them autonomously.

### 6A.9 Agent stop boundary for Framework v1

A future agent must stop and return for research/architecture review (rather than resolve autonomously) when a task would require inventing qualification/evaluation/selection mathematics, deciding entropy selection authority, inventing entropy normalization/carriers/state ownership, inventing `H_previous` or `TP.process.first_cycle`, forcing unresolved competition into a winner, defining generalized non-selection behavior, promoting characterization observations into requirements, adding characterization-only information to committed semantic state, or introducing category-specific procedural branching as the category-growth mechanism.

### 6A.10 Initial characterization questions (for separately authorized implementation stage)

1. Under existing Palette v1 source-composition conditions, does Framework v1 preserve the qualified-candidate set and committed result of the current bounded realization?
2. When supported candidates are close/near-equal, does observability preserve competition/separation visibility rather than letting the final winner hide it?
3. If a candidate has favorable numerical behavior but fails legitimate support/qualification, is it prevented from being selected?
4. When inventory membership and evidence support diverge, does observability preserve the distinction without silently changing committed result?
5. Can added characterization observation remain behaviorally independent from committed outputs (scores/distribution/selected category/other committed behavior)?

These are characterization questions, not normative equations.

### 6A.11 Category relational role

In Path A, a category is more than an index or label. It identifies a major relational region within which objects, structures, defined basins, and relational possibilities may become relevant to interpretation. Category Selection determines which such region is supported by the available authorized evidence and current TP/context. Selection of a category does not predefine the relationships that must occur within that region, nor does it determine final meaning or downstream conversational emphasis. Specific relationships remain constrained by the available structure, evidence, context, and applicable downstream processing.

## 7) Current computational path (reconstructable)

Current bounded path:

`inputs -> evidence/cues -> candidate categories -> category scoring -> normalized distribution -> selection/result -> TP commitment -> downstream read-only consumption`

Runtime order includes:

`InB -> IIInB -> IE -> CEx -> CE -> ISc -> TPU -> ... -> IdOB`

in [pathA_short_simulator.py](../../pathA_short_simulator.py).

### 7.1 Stage traceability table

| Stage | Purpose | Normative authority | Software owner | Config/data owner | Inputs and parameters | Transformation | Outputs/provenance | Invariants/downstream | Verification surface |
|---|---|---|---|---|---|---|---|---|---|
| Inputs | Collect runtime controls and optional prior context | 20.105 TP carriage boundaries | [pathA_short_simulator.py](../../pathA_short_simulator.py) `run_pathA_short` | Caller arguments | `raw_text`, `enable_category_selection`, `prior_context` | Initializes TP and flags | TP initialized; `prior_context` attached | No category result committed at this stage | [run_examples.py](../../run_examples.py), replay scripts |
| Evidence/cues | Extract cue evidence from prior context and sentence | 20.45 cue-source allowance (HLR-20.45-096) | [primitives_pathA_short.py](../../primitives_pathA_short.py) `CEx`, `CE` | [category_cues.yaml](../../support/dictionaries/category_cues.yaml) | `tp.prior_context`, `tp.raw_text`, cue maps | Substring-based mapping to cue majors; merges cue sources | `tp.cex_output.category_cue`; `tp.ce_output.category_cue`; `cue_provenance` (`sentence`, `prior_context_cex`) | Cue evidence remains pre-meaning | [s2m_category_selection_replay.py](../../support/tools/s2m_category_selection_replay.py), trace output |
| Candidate categories | Build per-major candidate category rows for scorer | 20.45 scorer-input context | [primitives_pathA_short.py](../../primitives_pathA_short.py) `CE` | [majors.yaml](../../s2m/data/majors.yaml) | Known majors + local features (`f_s`,`f_b`,`f_e`,`f_i`) | Iterates majors to build `category_candidate_set` | `tp.ce_output.category_candidate_set` | Bounded major-level synthetic candidate rows | Trace output; code inspection |
| Category scoring | Score category candidates with additive cue term | 20.45 HLR-20.45-097 | [primitives_pathA_short.py](../../primitives_pathA_short.py) `ISc` | [isc_weights.yaml](../../support/dictionaries/isc_weights.yaml) | `w_s,w_b,w_e,w_i,w_cat`, candidate set, cue set | Linear score + cue indicator term | Raw score list (internal) | No meaning write at scorer stage | Trace output; replay |
| Normalized distribution | Convert scores to probability distribution | 20.45 HLR-20.45-090 | [primitives_pathA_short.py](../../primitives_pathA_short.py) `ISc` | same as above | Scored candidates | Softmax + stable sort (`-probability`, `major`) | `category_weighted_distribution` | Deterministic ordering for ties | Replay determinism checks |
| Selection/result | Produce category result envelope fields | 20.45 HLR-20.45-098/099 | [primitives_pathA_short.py](../../primitives_pathA_short.py) `ISc` | cue/weight/major data above | Distribution + cue set | Computes `top_category`, `category_confidence`, `category_rationale`; includes provenance summary | `tp.isc_output` with required category-result fields | Result is scored cue only, not final meaning selection | Replay + run trace |
| TP commitment | Commit category result to TP envelope | 20.45 HLR-20.45-100; 20.116.010 path/owner | [primitives_pathA_short.py](../../primitives_pathA_short.py) `TPU` | N/A | `enable_category_selection`, merged isc output | Condensed merge then gated commit | `TP.semantic.isc_category_result` | Commit path is TPU-only in current realization; commit gated by runtime flag | Trace output; code inspection |
| Downstream read-only consumption | Use category result to filter candidate consideration before legitimation | 20.40.050 read-only IdOB-side behavior context; 20.45 no-meaning-write at scorer | [s2m/loop.py](../../s2m/loop.py), [s2m/propose.py](../../s2m/propose.py), [s2m/active_space.py](../../s2m/active_space.py), [s2m/legitimate.py](../../s2m/legitimate.py) | [spaces/default.yaml](../../s2m/data/spaces/default.yaml), [associations/](../../s2m/data/associations), bounded license table in [s2m/legitimate.py](../../s2m/legitimate.py) | `TP.semantic.isc_category_result`, proposed candidates, active space | Read-only category gating -> candidate state transitions -> legitimation/refusal | `selection_state`, `meaning_relations`, default+extension visibility | Category support and legitimation remain distinct | [s2m_category_selection_replay.py](../../support/tools/s2m_category_selection_replay.py), [s2m_canonical_sentences_replay.py](../../support/tools/s2m_canonical_sentences_replay.py) |

## 8) Parameter and dependency traceability

### 8.1 Mechanism parameters in current bounded realization

- `w_s`, `w_b`, `w_e`, `w_i`, `w_cat`  
  - Source: [isc_weights.yaml](../../support/dictionaries/isc_weights.yaml)  
  - Used by: `ISc` in [primitives_pathA_short.py](../../primitives_pathA_short.py)  
  - Classification: **Realization parameters** constrained by normative scoring form.

- Category cue mappings (sentence/prior-context)  
  - Source: [category_cues.yaml](../../support/dictionaries/category_cues.yaml)  
  - Used by: `CEx` and `CE`  
  - Classification: **Realization config** (data-driven cue inventory).

- Major inventory  
  - Source: [majors.yaml](../../s2m/data/majors.yaml)  
  - Used by: `CE` candidate construction  
  - Classification: **Realization config** (inventory).

- Active space and associations  
  - Source: [spaces/default.yaml](../../s2m/data/spaces/default.yaml), [associations/](../../s2m/data/associations/)  
  - Used by: S2M path  
  - Classification: **Realization config** (downstream consumption context).

- Licensed-region table  
  - Source: bounded table in [s2m/legitimate.py](../../s2m/legitimate.py)  
  - Used by: S2M legitimation  
  - Classification: **Realization scaffolding** (not generalized licensing).

### 8.2 Runtime flags

- `enable_category_selection`  
  - Source: caller of `run_pathA_short`  
  - Used by: TPU commit gate  
  - Classification: **Realization control**.

## 9) Input / output contract (current bounded realization)

### 9.1 Inputs

- `raw_text` (sentence)
- optional `prior_context`
- `enable_category_selection` flag
- configuration: cue maps, weights, majors, spaces, associations

### 9.2 Outputs (committed)

- `TP.semantic.isc_category_result` containing:
  - `category_cue`
  - `category_weighted_distribution`
  - `top_category`
  - `category_confidence`
  - `category_rationale`
  - `provenance`

### 9.3 Non-committed observability

- trace output of intermediate stages
- characterization artifacts (when characterization is active; owned by characterization reference)

## 10) Non-mutation walls

Implementation under this contract must preserve:

- additive category-selection behavior relative to structural/default meaning path,
- non-mutation of structural writer responsibilities (SOB/SROB/CnOB/SmOB),
- read-only S2M consumption of committed category result,
- separation between candidate relevance and final legitimation/refusal.

Category support must not be treated as automatic meaning legitimation.

## 11) Required realization outputs

Category-selection realization must continue to expose inspectable outputs sufficient for bounded review, including:

- cue source and cue values (including provenance summary),
- category distribution and top category result,
- confidence and rationale outputs,
- committed `TP.semantic.isc_category_result`,
- downstream candidate selection states,
- legitimation/refusal result visibility,
- final participation/composite relation visibility.

If an output is unavailable in a run, absence must be explicit rather than silently omitted.

## 12) Implementation touchpoint discipline

Any implementation work performed under this contract must:

1. identify touched modules/functions explicitly before edit,
2. preserve normative ownership and envelope contracts,
3. keep category-specific knowledge in data where architecture allows,
4. avoid introducing silent fallback behavior for category-type logic,
5. preserve deterministic replay behavior for existing baseline fixtures unless explicitly reviewed.

## 13) Compact conformance/verification map

| Normative authority | Realization rule | Implementation/config owner | Observable/test surface | Current conformance |
|---|---|---|---|---|
| 20.45 HLR-20.45-096/097 | Optional cue + additive cue term in scoring | [primitives_pathA_short.py](../../primitives_pathA_short.py), [isc_weights.yaml](../../support/dictionaries/isc_weights.yaml), [category_cues.yaml](../../support/dictionaries/category_cues.yaml) | [s2m_category_selection_replay.py](../../support/tools/s2m_category_selection_replay.py), trace output | Conforming in bounded realization |
| 20.45 HLR-20.45-090 | Softmax normalization for distribution | [primitives_pathA_short.py](../../primitives_pathA_short.py) | Trace output, replay | Conforming in bounded realization |
| 20.45 HLR-20.45-098/100 + 20.116.010 | Category-result fields and TPU commit into `TP.semantic.isc_category_result` | [primitives_pathA_short.py](../../primitives_pathA_short.py) | Trace output, code inspection, replay | Conforming in bounded realization |
| 20.45 HLR-20.45-099 + 20.40.050 context | Category result is not final meaning write; downstream read-only consumption boundary | [s2m/loop.py](../../s2m/loop.py) and S2M path files | Category/S2M replay surfaces | Conforming in bounded realization |
| 20.45 HLR-20.45-089/091 (via HLR-20.45-097 linkage) | Entropy/ΔH computation from resulting category-cue scores | Category scoring path in [primitives_pathA_short.py](../../primitives_pathA_short.py) | Code inspection + replay/trace outputs | **Known nonconformance (open)** |

## 14) Explicit unresolved items preserved by scope

Unresolved by current bounded realization and not resolved by this reference:

- generalized no-category policy,
- weak-confidence/threshold policy,
- hysteresis/persistence behavior,
- unsupported/inventory-inadequate formal policy,
- global Category Selection geometry/space conclusions,
- Python/C++ equivalence scope decision.

## 15) Change-control and review gates for future realization updates

Any future mechanism change should continue to require:

1. explicit mapping to normative authority,  
2. explicit implementation/configuration ownership,  
3. replay/determinism check evidence,  
4. documentation alignment updates (including [user_guide.md](../../user_guide.md) when user-visible behavior changes),  
5. explicit treatment of conformance impacts (including whether a gap is opened, closed, or unchanged).
