# S2M IdOB Traversal Observation

**Date:** 2026-11-25  
**Status:** Executed-facts record for the frozen traversal experiment plan.  
**Plan authority:** [s2m_idob_traversal_experiment_plan.md](s2m_idob_traversal_experiment_plan.md).  
**Program mapping context:** [s2m_idob_traversal_program_reference.md](s2m_idob_traversal_program_reference.md).  

## Execution record

### What executed

- Frozen case matrix execution via `run_pathA_short` using existing realization surfaces only.
- Artifact written:
  - `local_characterization/sessions/s2m_idob_traversal_exp/runs/20261125_073021__s2m_idob_traversal_exp.json`

### Drift checks executed

- `python support/tools/s2m_canonical_sentences_replay.py` → passed
- `python support/tools/s2m_category_selection_replay.py` → passed

Replay interpretation boundary:

- **Full-object duplicate-run equality:** not expected; unequal because runtime-generated timestamp fields change between runs (for example `committed_stream.source.created_at_utc`).
- **Dedicated semantic replay controls:** passed (`s2m_canonical_sentences_replay.py`, `s2m_category_selection_replay.py`).

## Case facts (compact)

Legend:
- `Door`: observed `s2m_seed.written_relations` count.
- `C_t`: observed candidate count in `s2m_meaning.candidate_interpretations`.
- `Corr`: observed cue/candidate-state surface only (not proposal-level `+/-/0` primitive).
- `D_t/Q_t/B_t/H_t`: unavailable unless otherwise stated.
- `P_t(obs)`: observed category-scoring softmax distribution (non-traversal candidate surface).

| Case | Input/evidence configuration | Door | C_t | Corr observation | Provenance/dependency observation | D_t | Q_t | B_t | P_t(obs) | H_t | Replay result | Stop/anomaly |
|---|---|---:|---:|---|---|---|---|---|---|---|---|---|
| `TC01_support` | `"The sky is blue."`, prior `["cold"]` | 1 | 4 | cues=`["affective"]`; states=`candidate_unselected:3, legitimized:1`; meaning_relations=1 | sentence/prior provenance visible; dependency class unavailable | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | top=`affective` p=0.2505069933606234 | UNAVAILABLE | full-object replay mismatch | Timestamp field changes (`committed_stream.source.created_at_utc`) |
| `TC02_no_correspondence` | `"The sky is blue."`, no prior | 1 | 4 | cues=`[]`; states=`candidate_unselected:4`; meaning_relations=0 | provenance source empty; dependency class unavailable | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | top=`affective` p=0.125 (tie-ordered distribution) | UNAVAILABLE | full-object replay mismatch | same timestamp-only mismatch |
| `TC03_opposition_probe` | `"The sky is blue."`, prior `["not cold"]` | 1 | 4 | cues=`["affective"]`; states=`candidate_unselected:3, legitimized:1`; meaning_relations=1 | prior provenance present; no explicit opposition relation field | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | top=`affective` p=0.2505069933606234 | UNAVAILABLE | full-object replay mismatch | “not cold” still triggers `cold` cue substring |
| `TC04_multi_source_support` | `"The sky is cold."`, prior `["cold"]` | 0 | 0 | cues=`["affective"]`; no S2M candidates/relations emitted | multi-source cue provenance visible; dependency class unavailable | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | top=`affective` p=0.32171311115883794 | UNAVAILABLE | full-object replay mismatch | seed relation not built for this utterance pattern |
| `TC05_duplicate_prior` | `"The sky is blue."`, prior `["cold","cold","cold"]` | 1 | 4 | cues=`["affective"]`; states=`candidate_unselected:3, legitimized:1`; meaning_relations=1 | prior-only provenance retained; duplicates not represented as separate families | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | top=`affective` p=0.2505069933606234 | UNAVAILABLE | full-object replay mismatch | duplicate observations collapse at cue level |
| `TC06_unknown_dependency_probe` | `"The sky is blue."`, prior `["cold from source a","cold from source b"]` | 1 | 4 | cues=`["affective"]`; states=`candidate_unselected:3, legitimized:1`; meaning_relations=1 | source bucket only (`prior_context_cex`); dependency unresolved but not explicitly typed | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | top=`affective` p=0.2505069933606234 | UNAVAILABLE | full-object replay mismatch | unknown dependency not explicitly representable |
| `TC07_internal_conflict_probe` | `"The book is on the table."`, prior `["cold"]` | 1 | 2 | cues=`["physical","affective"]`; states=`legitimized:2`; meaning_relations=2 | mixed-source provenance visible; internal conflict qualifier absent | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | top=`physical` p=0.23667050650980903 | UNAVAILABLE | full-object replay mismatch | no explicit conflict marker despite mixed cues |
| `TC08_balance_probe` | `"The book is on the table."`, prior `["cold table"]` | 1 | 2 | cues=`["physical","affective"]`; states=`legitimized:2`; meaning_relations=2 | mixed-source provenance visible; no directional tuple | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | top=`physical` p=0.2847499303503376 | UNAVAILABLE | full-object replay mismatch | equal S/O test unavailable (no S/O representation) |
| `TC09_unequal_direction_probe` | `"The book is on the table."`, prior `["table"]` | 1 | 2 | cues=`["physical"]`; states=`legitimized:2`; meaning_relations=2 | sentence+prior provenance visible; no directional tuple | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | top=`physical` p=0.32171311115883794 | UNAVAILABLE | full-object replay mismatch | directional discrimination not separately modeled |
| `TC10_multi_candidate` | `"Where is the book?"`, no prior | 1 | 3 | cues=`["perspectival"]`; states=`candidate_unselected:2, refused:1`; meaning_relations=0 | sentence provenance visible; dependency class unavailable | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | top=`perspectival` p=0.31090105669062545 | UNAVAILABLE | full-object replay mismatch | refusal visible without opposition primitive |

## Bounded interpretation

1. Finite candidate sets are observable on the current S2M endpoint-association surface (`C_t` surrogate), but traversal-door legality (`structural_key -> meaning_group_candidates`) is not realized.
2. Current outputs preserve support-like and no-cue states, but do not realize explicit opposition correspondence semantics.
3. Provenance is visible at source-bucket level; dependency family typing (Independent/Dependent/Unknown) is not represented.
4. Proposal-level directional tuples and qualifier tuples (`D_t`, `Q_t`) are not computable from current fields.
5. Category softmax is observable (`ISc`) but remains a category-scoring surface, not validated traversal normalization over door-legal candidates.
6. Entropy for this bounded characterization surface remains unavailable.

## Not established

- Proposal-level `door`, `E_t (+/-/0)`, `L_t` dependency typing, `D_t`, `Q_t`, `B_t`, traversal `P_t`, traversal `H_t`, and continue/OuBA sufficiency rule are not established by these runs.
- No architectural promotion claim is established.

## Stop/anomaly status

- Stop conditions were monitored; no architecture-inventing code change was performed.
- Observed anomalies/boundaries were recorded as evidence and not repaired:
  - negation text (`"not cold"`) still maps to `cold` cue via substring cue extraction;
  - full-object replay inequality is attributable to runtime timestamp field churn; dedicated semantic replay controls passed;
  - some utterances (for example `"The sky is cold."`) do not enter the bounded seed relation set and therefore expose zero S2M candidates in this surface.
