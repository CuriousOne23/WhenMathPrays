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

---

## Observation — Follow-on run (lineage/opposition refinement, 2026-11-25)

### What executed

- Frozen representability batch (`CR01`..`CR12`) executed after contract/plan refinement.
- Artifact:
  - `local_characterization/sessions/s2m_idob_lineage_opposition_exp/runs/20261125_085112__s2m_idob_lineage_opposition_exp.json`
- Record shape per evidence-candidate result now includes:
  - `evidence_id`, `candidate_id/reference`, provenance,
  - correspondence state + basis,
  - opposition status + basis,
  - `lineage_id`, lineage basis,
  - derivation edge + basis,
  - dependency state + basis,
  - independence status,
  - Unknown/Unresolved/Unavailable reason.

### Replay/drift controls

- `python support/tools/s2m_canonical_sentences_replay.py` → passed
- `python support/tools/s2m_category_selection_replay.py` → passed
- Per-case semantic-slice duplicate-run equality in artifact: all `true`.

### Case-level facts (compact)

| Case | Core result | Dependency result | Opposition result |
|---|---|---|---|
| `CR01_support_record` | supporting + no-established-relation both observed | `Unknown` | `UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS` |
| `CR02_no_relation_record` | no-established-relation only | `Unknown` | `UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS` |
| `CR03_unresolved_record` | unresolved (candidate surface missing) | `Unknown` | `UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS` |
| `CR04_opposition_unavailable` | supporting + no-established-relation observed | `Unknown` | `UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS` |
| `CR05_repeated_observation` | supporting + no-established-relation observed | `Dependent` (narrow duplicate linkage) + `Unknown` remainder | `UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS` |
| `CR06_duplicate_dependency` | supporting + no-established-relation observed | `Dependent` (narrow duplicate linkage) + `Unknown` remainder | `UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS` |
| `CR07_generic_dependency_unavailable` | supporting + no-established-relation observed | `Unknown` | `UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS` |
| `CR08_independence_unavailable` | supporting + no-established-relation observed | `Unknown`; independence unavailable | `UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS` |
| `CR09_unknown_dependency` | supporting + no-established-relation observed | `Unknown` | `UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS` |
| `CR10_provenance_preservation` | supporting observed | `Unknown` | `UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS` |
| `CR11_multi_candidate` | one supporting candidate, others no-established-relation | `Unknown` | `UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS` |
| `CR12_lineage_derivation_surface` | supporting + no-established-relation observed | duplicate-derived `Dependent` plus derivation edges; no lineage_id assignment | `UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS` |

## Bounded interpretation — Follow-on run

1. The three-way distinction `supporting` vs `no_established_relation` vs `unresolved` is now mechanically inspectable in one frozen run set.
2. Narrow duplicate-derived dependency (`PARTIAL_DUPLICATE_LINK_ONLY`) is mechanically inspectable without promoting to generic lineage architecture.
3. Lineage fields remain explicit null/unavailable unless affirmative basis exists; no fabricated lineage tokens were introduced.
4. Explicit opposition remains unavailable without affirmative conflict basis and is recorded as such rather than inferred from absence/negation.

## Not established — Follow-on run

- Generic lineage assignment rule and architecture remain not established.
- Affirmative independence condition remains not established.
- Explicit opposing relation primitive remains not established.
- Door-legal candidate correspondence remains not established.

## Anomaly / stop status — Follow-on run

- No semantic-policy code change was introduced.
- No stop condition requiring D-class architecture invention was crossed.
- D-class boundaries were preserved as explicit unavailable/unknown outputs.

---

## Observation — Evidence-specific correspondence audit correction run (2026-11-25)

### Method correction applied

The prior run established aggregate candidate-level support visibility, but that aggregate support does not by itself establish evidence-specific support for every evidence-candidate pair.  
This audit reclassifies outcomes by checking each chain link explicitly.

### OBSERVATION

- Audit artifact produced:
  - `local_characterization/sessions/s2m_idob_evidence_correspondence_audit/runs/20261125_090537__s2m_idob_evidence_correspondence_audit.json`
- Frozen audit cases executed: `EA01`..`EA08`.
- Link-level audit dimensions recorded per evidence-candidate record:
  - aggregate candidate-support status + basis;
  - evidence->cue/property attachment status + basis;
  - cue/property->candidate correspondence status + basis;
  - chain status (`COMPLETE_CHAIN`, `AGGREGATE_SUPPORT_ONLY`, `NO_ESTABLISHED_RELATION`, `UNRESOLVED`, `UNAVAILABLE`);
  - exact missing link when incomplete.
- Opposition status in all records:
  - `UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS`.
- Duplicate handling corrected:
  - direct repetition is recorded with `duplicate_of_evidence_id` / `duplicate_basis_reference`;
  - no direct-repetition `derivation_edge` was emitted.
- Replay controls:
  - `s2m_canonical_sentences_replay.py` passed;
  - `s2m_category_selection_replay.py` passed;
  - per-case semantic-slice duplicate-run equality in audit artifact: `true`.

### BOUNDED INTERPRETATION

1. Aggregate candidate support is observable in current TS.
2. Evidence-specific support is not yet established as an explicit represented correspondence chain. In narrow single-source/single-observation conditions, an evidence-to-cue association can be uniquely reconstructed from existing surfaces; that reconstruction is locally useful but is not equivalent to an explicit evidence-to-cue attachment fact.
3. The downstream cue/property-to-candidate step also remains grounded in aggregate candidate-support surfaces rather than a generic first-class correspondence fact. Therefore, the audit establishes narrow reconstructed chains, not explicit complete correspondence chains.
4. For many evidence-candidate pairs, the missing link is explicitly:
   - `missing_link:evidence_to_cue_attachment`.
5. This is a successful fog-clearing outcome even where evidence-specific support is unavailable.
6. Opposition remains unavailable due missing affirmative conflict basis and was not inferred from absence/negation/mismatch.

### NOT ESTABLISHED

- Generic evidence->cue attachment mechanism for all evidence observations.
- Generic evidence-specific correspondence primitive independent of aggregate candidate-support surfaces.
- Affirmative conflict/opposition representation.
- Generic lineage architecture and affirmative independence condition.

### Prior-run interpretation correction

Prior correspondence results are preserved as historical evidence.  
Their `supporting` outcomes should be interpreted as candidate-level aggregate support visibility unless a complete affirmative evidence-specific chain is demonstrated for the specific evidence-candidate pair.
