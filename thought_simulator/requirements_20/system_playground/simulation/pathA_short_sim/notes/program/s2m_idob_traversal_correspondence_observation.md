# S2M IdOB Traversal Correspondence Observation

**Date:** 2026-11-25  
**Status:** Executed correspondence/lineage representability observation (bounded, local utility).  
**Plan authority:** [s2m_idob_traversal_correspondence_experiment_plan.md](s2m_idob_traversal_correspondence_experiment_plan.md).  
**Contract authority:** [s2m_idob_traversal_correspondence_contract.md](s2m_idob_traversal_correspondence_contract.md).  

## Observation

### What executed

- Correspondence representability batch executed against existing TS surfaces only (no semantic/code changes).
- Artifact:
  - `local_characterization/sessions/s2m_idob_correspondence_exp/runs/20261125_083313__s2m_idob_correspondence_exp.json`

### Replay/drift controls

- `python support/tools/s2m_canonical_sentences_replay.py` → passed
- `python support/tools/s2m_category_selection_replay.py` → passed
- Per-case semantic-slice duplicate-run check inside artifact: all cases `true`.
- Full-object equality not required; runtime metadata/timestamps may differ.

### Case-level facts

| Case | Input/evidence configuration | Candidate(s) | Correspondence state(s) | Basis availability | Lineage info | Dependency state | Unknown/Unresolved/Unavailable reason |
|---|---|---|---|---|---|---|---|
| `CR01_support_record` | `"The sky is blue."` + prior `["cold"]` | 4 surrogate candidates | one `supporting`, others `no_established_relation` | supporting basis present (`major_in_category_cue + selection_state`) | unavailable | `Unknown` | no generic lineage architecture; no opposing relation primitive |
| `CR02_no_relation_record` | `"The sky is blue."` + no prior | 4 surrogate candidates | all `no_established_relation` | no positive/negative basis for any candidate | unavailable | `Unknown` | no active cue evidence; no opposing relation primitive |
| `CR03_opposition_record` | `"The sky is blue."` + prior `["not cold"]` | 4 surrogate candidates | one `supporting`, others `no_established_relation` | opposition basis absent | unavailable | `Unknown` | explicit opposition `UNAVAILABLE` (no explicit opposing relation) |
| `CR04_unresolved_correspondence` | `"The sky is cold."` + prior `["cold"]` | candidate surface unavailable | `unresolved` | unresolved basis recorded (`candidate_surface_unavailable_for_case`) | unavailable | `Unknown` | correspondence cannot be evaluated without candidate surface |
| `CR05_repeated_observation` | `"The sky is blue."` + prior `["cold","cold","cold"]` | 4 surrogate candidates | one `supporting`, others `no_established_relation` | supporting basis present | unavailable | `Dependent` (partial) | dependent basis limited to duplicate input linkage only |
| `CR06_affirmative_dependency` | `"The sky is blue."` + prior `["cold","cold"]` | 4 surrogate candidates | one `supporting`, others `no_established_relation` | supporting basis present | unavailable | `Dependent` (partial) | dependent basis limited to duplicate input linkage only |
| `CR07_affirmative_independence` | `"The sky is blue."` + prior `["cold from source a","cold from source b"]` | 4 surrogate candidates | one `supporting`, others `no_established_relation` | supporting basis present | unavailable | `Unknown` | independence `UNAVAILABLE` (no affirmative independence basis) |
| `CR08_unknown_dependency` | `"The sky is blue."` + prior `["cold from source a","cold from source b"]` | 4 surrogate candidates | one `supporting`, others `no_established_relation` | supporting basis present | unavailable | `Unknown` | no positive dependency or independence basis represented |
| `CR09_provenance_preservation` | `"The book is on the table."` + prior `["table"]` | 2 surrogate candidates | both `supporting` | supporting basis present for both | unavailable | `Unknown` | provenance preserved; lineage/dependency unresolved |
| `CR10_multi_candidate_targeting` | `"Where is the book?"` + no prior | 3 surrogate candidates | one `supporting`, two `no_established_relation` | supporting basis present for one candidate | unavailable | `Unknown` | candidate-specific outcomes visible; no opposition primitive |

## Interpretation (bounded)

1. The distinction between `supporting` and `no_established_relation` is now mechanically inspectable at surrogate-candidate level using represented cue-major/candidate-major relation plus candidate state.
2. `unresolved` correspondence was also made inspectable in the case where correspondence prerequisites (candidate surface) were absent.
3. Explicit opposition remains unavailable without an explicit opposing relation primitive; this is now recorded as a bounded unavailable state, not inferred from negation/absence.
4. Dependency classification gained a narrow inspectable case: repeated identical input observations can be tagged as dependent via explicit duplicate linkage only.
5. Affirmative independence remained unavailable and was preserved as unavailable/unknown rather than fabricated.

## Not established

- No door-legal candidate correspondence (`structural_key -> meaning_group_candidates`) was established.
- No explicit generic opposing relation primitive was established.
- No lineage architecture (`family_id` semantics/representation) was established.
- No generic affirmative dependency/independence condition over information lineage was established.
- No `D_t`, `Q_t`, `B_t`, traversal-candidate `P_t`, traversal `H_t`, or continue/OuBA sufficiency behavior was established.

## Anomaly / stop status

- No stop condition requiring semantic architecture invention was crossed in this pass.
- Opposition, lineage identity, and affirmative independence were recorded as unavailable where required by boundary discipline.
