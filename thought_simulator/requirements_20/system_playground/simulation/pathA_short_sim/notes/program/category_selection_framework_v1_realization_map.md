# Category Selection Framework v1 Realization Map

**Document:** notes/program/category_selection_framework_v1_realization_map.md  
**Status:** Non-normative implementation evidence map.  
**Purpose:** Factual mapping of current bounded Category Selection realization to Framework v1 stages.

This document records what currently exists in software/configuration and what does not, without proposing new behavior.

## Framework v1 stage order

`authorized evidence -> candidate construction -> qualification -> evaluation -> competition/comparison -> selection policy -> result -> observability`

## Stage mapping matrix

| Stage | Current owner | Existing behavior | Available observability | Information computed but lost | Classification | Evidence/notes |
|---|---|---|---|---|---|---|
| authorized evidence | [primitives_pathA_short.py](../../primitives_pathA_short.py) (`CEx`, `CE`), [category_cues.yaml](../../support/dictionaries/category_cues.yaml), runtime inputs via [pathA_short_simulator.py](../../pathA_short_simulator.py) | Uses current utterance + optional prior context cue extraction | `tp.cex_output`, `tp.ce_output`, `cue_provenance`, run trace payloads | token-level cue-match evidence is not preserved | EXPLICITLY IMPLEMENTED | `CEx`/`CE` mapping and provenance summary are present |
| candidate construction | [primitives_pathA_short.py](../../primitives_pathA_short.py) (`CE`), majors inventory from [s2m/data/majors.yaml](../../s2m/data/majors.yaml) | Constructs one candidate row per major with `f_s/f_b/f_e/f_i` | `tp.ce_output.category_candidate_set` in trace/TP | richer candidate-construction rationale beyond feature values | EXPLICITLY IMPLEMENTED | inventory-oriented row generation is present |
| qualification | No explicit stage owner in current Category Selection path | No separate support/eligibility gate before evaluation/selection | none at Category Selection stage | qualification state/evidence/rationale before evaluation | ABSENT | first meaningful framework hole in current order |
| evaluation | [primitives_pathA_short.py](../../primitives_pathA_short.py) (`ISc`), [isc_weights.yaml](../../support/dictionaries/isc_weights.yaml) | Weighted scoring with cue indicator and softmax distribution | `category_weighted_distribution`, `category_confidence`, `category_rationale`, trace payloads | raw intermediate vectors (pre-sort, denominator, richer decomposition) | EXPLICITLY IMPLEMENTED | short realization includes scoring/distribution/top outputs |
| competition/comparison | [primitives_pathA_short.py](../../primitives_pathA_short.py) (`ISc`) | Candidate probabilities are compared; deterministic sorted distribution exposed | full distribution in `isc_output` and committed result | explicit competition labels (close/weak/unresolved), explicit margin field | PARTIALLY IMPLEMENTED | comparison exists numerically, but weak-differentiation state is not explicit |
| selection policy | [primitives_pathA_short.py](../../primitives_pathA_short.py) (`ISc`) | Selects top category by highest probability; cue-less path forces null result | `top_category`, `category_confidence`, rationale fields | policy-intent metadata beyond current rationale | EXPLICITLY IMPLEMENTED | current bounded selection policy is active in software |
| result | [primitives_pathA_short.py](../../primitives_pathA_short.py) (`TPU`) writing `TP.semantic.isc_category_result`; downstream reader [s2m/loop.py](../../s2m/loop.py) | Gated commit when `enable_category_selection=True`; read-only downstream consumption | committed TP field, trace `merge_output`/`isc_category_result` | none required by current bounded contract | EXPLICITLY IMPLEMENTED | aligns with bounded commit/read-only path |
| observability | Trace path in [pathA_short_simulator.py](../../pathA_short_simulator.py), S2M observational shaping in [s2m/record.py](../../s2m/record.py), downstream state in [s2m/loop.py](../../s2m/loop.py) | Exposes cue source summary, candidate set, score outputs, committed result, candidate `selection_state` transitions | trace entries, `candidate_interpretations`, `cue_state`, committed category result | explicit qualification-stage observables, unresolved-cause labels, entropy/info-resolution observables | PARTIALLY IMPLEMENTED | strong for current path; limited for framework-hole diagnosis |

## First meaningful framework hole

- **Stage:** qualification  
- **Classification:** ABSENT (explicit stage), with qualification mathematics/policy OPEN BY DESIGN  
- **Type:** implementation-stage hole in current framework execution order (not a new normative defect)  
- **Why this is first:** current path proceeds from candidate construction into scoring/evaluation without a distinct qualification eligibility boundary  
- **Evidence:** [primitives_pathA_short.py](../../primitives_pathA_short.py) `CE -> ISc -> TPU`; no qualification state emitted before scoring; downstream `category_supported/legitimized/refused` in [s2m/loop.py](../../s2m/loop.py) occurs after committed category result consumption and is not Category Selection qualification

## Open-by-design check

The following remain OPEN BY DESIGN and are not classified as defects in this map: qualification mathematics, binary vs graded qualification, evaluator mathematics, competition mathematics, selection mathematics, threshold/tie policy, generalized non-selection policy, entropy role in selection, entropy normalization/carrier/state continuity (`H_previous`, `TP.process.first_cycle`).

## Existing-behavior compatibility check

Current bounded realization can be described within Framework v1 without redefining existing behavior. The map preserves current behavior as-is and records missing/partial stages as factual evidence only.

