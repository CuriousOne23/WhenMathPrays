# S2M IdOB Door->Candidate Structural Observation

**Date:** 2026-11-25  
**Status:** Executed bounded structural characterization (`C1`-`C6`).  
**Plan authority:** [s2m_idob_door_candidate_structural_experiment_plan.md](s2m_idob_door_candidate_structural_experiment_plan.md).

## Observation

### Executed artifact

- `local_characterization/sessions/s2m_idob_door_candidate_structural_exp/runs/20261125_100807__s2m_idob_door_candidate_structural_exp.json`

### Frozen cases executed

- `C1_BASELINE`: normal producer.
- `C2_REDUCED_SUBSET`: two-record subset.
- `C3_SINGLE_CANDIDATE`: one record.
- `C4_EMPTY_SET`: empty list.
- `C5_REORDERED`: reversed list.
- `C6_ORIGIN_NEUTRAL`: fixture records with current required candidate shape.

All cases reported deterministic semantic-slice duplicate-run equality (`replay_same_semantic_slice=true`).

### Candidate-interface characterization

Current downstream seam remains candidate-record shaped:

- required fields consumed: `from`, `relation`, `to`, `major`
- optional pass-through field: `subcategory`
- downstream annotation field: `selection_state`

Observed from current consumer path:

- [apply](../../s2m/loop.py#L25) reads proposals and computes `selection_state`.
- [legitimate](../../s2m/legitimate.py#L19) consumes `from/relation/to/major` (and optional `subcategory`) for bounded license checks.
- [write_meaning_relations](../../s2m/write.py#L4) preserves relation payload for output.
- [build_record](../../s2m/record.py#L58) stores candidate interpretations and meaning relations.

No association-file origin/path metadata was required by consumers in this path.

### C1-C6 outcomes (bounded)

| Case | Candidate surface behavior | Meaning surface behavior | Structural inference |
|---|---|---|---|
| `C1_BASELINE` | 4 candidates | 1 legitimized meaning relation | Baseline surrogate behavior confirmed |
| `C2_REDUCED_SUBSET` | 2 candidates | no legitimized relation | Downstream handles reduced cardinality |
| `C3_SINGLE_CANDIDATE` | 1 candidate | no legitimized relation | Downstream handles singleton set |
| `C4_EMPTY_SET` | 0 candidates | no legitimized relation | Downstream handles empty set safely |
| `C5_REORDERED` | same set, different order | same meaning relation set as baseline | No semantic dependence on original producer order for this fixture |
| `C6_ORIGIN_NEUTRAL` | same set/order as baseline from fixture records | identical to baseline | Consumer path behaved producer-origin agnostically for proposal-shaped records |

### Structural-key preservation characterization

- [apply_seed](../../idob/experimental_seed.py#L34) emits `crossing_fields.structural_key: null`.
- Characterization artifact reported `seed_structural_key: null` for every case.
- [\_idob_structural_key](../../primitives_pathA_short.py#L925) exists as helper but is not on the current realized `s2m_seed.crossing_fields.structural_key` emission path.

Bounded conclusion: current path does not show "generated then destroyed" structural key behavior on this seam; structural_key is presently unrealized (null) for this path.

### Replay / zero-semantic-drift controls

- `python support/tools/s2m_canonical_sentences_replay.py` passed.
- `python support/tools/s2m_category_selection_replay.py` passed.

No production semantic code changed in this run.

## Structural verdict

`SAFE_TO_DEFER`

Rationale (bounded):

1. C1-C6 substitution was local to the producer boundary and downstream consumers accepted proposal-shaped records without producer-origin coupling.
2. Candidate interface contract is narrow and explicit.
3. Structural-key seam is explicitly unrealized (`null`) rather than silently transformed in this path.

## Not established

- Proposal-defined door legality semantics (`structural_key -> meaning_group_candidates`) are still not implemented.
- Structural-key construction and ownership contract remain unresolved.
- This run does not select a door algorithm, candidate weighting policy, or continue/OuBA policy.

## Explicit unresolved questions (handoff)

1. What concrete representation defines `structural_key` for door legality in this program family?
2. Where should door legality ownership live relative to current surrogate producer boundaries?
3. How should future door candidates map to current `from/relation/to/major[/subcategory]` contract (or explicit successor contract) without semantic drift?
4. Which deterministic replay fixtures become authoritative once a real door surface exists?

