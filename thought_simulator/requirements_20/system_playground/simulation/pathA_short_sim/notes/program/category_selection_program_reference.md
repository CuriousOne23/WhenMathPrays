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
  - Classification: **Realization configuration** for cue evidence mapping.

- Category/inventory data involved downstream  
  - Sources: [majors.yaml](../../s2m/data/majors.yaml), [spaces/default.yaml](../../s2m/data/spaces/default.yaml), [associations/](../../s2m/data/associations)  
  - Used by: `CE`, `s2m.propose`, `s2m.active_space`, `s2m.loop`  
  - Classification: **Realization configuration/dependencies**.

- `enable_category_selection`  
  - Source: runtime call surface (`run_pathA_short`, CLI workflows in [run_examples.py](../../run_examples.py))  
  - Effect: gates TP commit in `TPU`  
  - Classification: **Realization runtime control**.

- `prior_context` input  
  - Source: runtime call surface  
  - Effect: optional cue evidence source via `CEx`  
  - Classification: **Realization runtime input/control**.

### 8.2 Normative vs realization vs experimental distinction

- **Normative:** scoring law form, output field requirements, commit path ownership rules (20.45/20.116/20.105/20.40.050).
- **Realization:** specific weight values, cue mappings, bounded inventory content, runtime gating choices in current `pathA_short_sim`.
- **Experimental:** characterization controls such as `--characterize`, `--char-type`, `--char-session-id`, `--char-run-index` in [run_examples.py](../../run_examples.py); these are not Category Selection mechanism parameters.

## 9) Inputs, outputs, ownership, and invariants

### 9.1 Inputs (bounded realization)

- `raw_text` (sentence under execution)
- optional `prior_context` list
- runtime control `enable_category_selection`
- cue/weight/major/inventory configuration files listed above

### 9.2 Category-result outputs (bounded realization)

- `category_cue`
- `category_weighted_distribution`
- `top_category`
- `category_confidence`
- `category_rationale`
- `provenance`

committed at `TP.semantic.isc_category_result` when enabled.

### 9.3 Ownership and commit behavior

- Canonical envelope path and writer authority for `TP.semantic.isc_category_result` are governed by [20.116.010_tp_envelope_index.md](../../../20.116.010_tp_envelope_index.md).
- Current bounded realization commit is implemented in `TPU` in [primitives_pathA_short.py](../../primitives_pathA_short.py), gated by `enable_category_selection`.
- Downstream consumption in [s2m/loop.py](../../s2m/loop.py) reads this envelope and does not write it.

### 9.4 Invariants preserved in current bounded realization

- Category result is additive and remains distinct from final meaning write.
- Category-supported relevance is distinct from legitimation/refusal.
- Structural/default path ownership is not reassigned by Category Selection.

## 10) Determinism/replay and observable surfaces

Current replay/check surfaces:

- [support/tools/s2m_category_selection_replay.py](../../support/tools/s2m_category_selection_replay.py)
- [support/tools/s2m_canonical_sentences_replay.py](../../support/tools/s2m_canonical_sentences_replay.py)
- [replay_parity_harness.py](../../replay_parity_harness.py)
- [support/tools/pipeline_readiness_check.py](../../support/tools/pipeline_readiness_check.py)

These verify bounded determinism/replay where implemented.  
They do not resolve unresolved research-policy questions.

## 11) Normative conformance gap: entropy / ΔH

Reviewed discrepancy:

1. [20.45_ts_isc_scoring.md](../../../20.45_ts_isc_scoring.md) HLR-20.45-097 requires category-cue scoring using resulting scores with entropy/ΔH behavior linked to HLR-20.45-089–091.  
2. Current bounded `pathA_short_sim` Category Selection realization does not perform entropy/ΔH computation on this category-result path.  
3. Current implementation does provide normalized distribution, `top_category`, `category_confidence`, `category_rationale`, and TP commit path behavior currently used for bounded Category Selection result handling.  
4. No repository authority identified in the completed audit authorizes omission of entropy/ΔH computation.  
5. Therefore this is recorded as a **known normative conformance gap**, not an accepted exception.  
6. This document does not resolve the gap.  
7. Resolution requires a separately authorized conformance task.

Path-A entropy ownership remains process-level (see [20.705_patha_pathb_flow.md](../../../20.705_patha_pathb_flow.md), §2.1). The fact that ISc performs a defined entropy/ΔH computation does not assign architectural ownership of entropy to ISc or Category Selection. Any future correction of this conformance gap must remain consistent with that Path-A principle and with the normative ISc entropy requirements in [20.45_ts_isc_scoring.md](../../../20.45_ts_isc_scoring.md). This reference does not define the missing entropy carrier, comparison-state contract, normalization convention, or first-cycle ownership.

## 12) Realization vs empirical characterization boundary

- Characterization artifacts may validate or challenge realization behavior.
- Empirical observations do not define mechanism equations, constants, or normative policy.
- Observed numeric outcomes (including confidence behavior in specific runs) are not promoted here into mechanism rules unless independently required by normative authority.

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
