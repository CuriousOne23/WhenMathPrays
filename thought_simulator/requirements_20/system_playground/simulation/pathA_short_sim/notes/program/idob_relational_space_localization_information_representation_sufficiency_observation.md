# IdOB Relational-Space Localization Observation (Information/Representation Sufficiency Characterization)

**Date:** 2026-11-27  
**Status:** Executed characterization observation record (non-normative).  
**Method authority:** [idob_relational_space_localization_information_representation_sufficiency_proposal.md](idob_relational_space_localization_information_representation_sufficiency_proposal.md).  
**Mechanical design authority:** [idob_relational_space_localization_information_representation_sufficiency_design.md](idob_relational_space_localization_information_representation_sufficiency_design.md).

## 0) Review state

Review state: **BEING REVIEWED**

Only the human may establish APPROVED.

## 1) Fixture reference

Characterization implementation:

- [idob_relational_space_localization_information_representation_sufficiency_characterization.py](../../support/tools/idob_relational_space_localization_information_representation_sufficiency_characterization.py)

Machine-readable evidence artifact:

- `local_characterization/sessions/idob_relational_space_localization_information_representation_sufficiency/runs/20261127_194331__idob_rel_space_localization_info_repr_sufficiency.json`

## 2) Executed conditions and completeness

Executed frozen fixture domain:

- `n in {32, 64, 128, 256}`
- `o in {0, 0.10, 0.25, 0.50}`
- `k in {1, 2, 3, 4}`
- representation levels `R0..R4`

Artifact summary:

- applicable fixture-domain condition count: `64`
- Gate A-qualified leverage-domain condition count: `3`
- expected level-condition count: `320`
- actual level-condition count: `320`
- exhaustive matched baselines completed: `true`
- replay pass: `true`
- required controls ok: `true`
- insufficient evidence reasons: `[]`

## 3) Frozen Gate A map and R0 contract checks

Frozen Gate A fixture-map checks:

- map entry count: `64`
- duplicate tokens: `[]`
- canonical token scheme used as frozen:
  - `gatea-oracle::<fixture_id>::k<k>::fp::<deterministic_fingerprint>`

R0 exact-reproduction checks:

- R0 exact-reproduction pass count: `64/64`
- R0 exact-reproduction fail count: `0`

This confirms exact-reproduction/plumbing and leverage were reported separately.

## 4) Domain separation (preserved)

Primary sufficiency domain (Gate A-qualified):

- `phase3_n256_o0.5_k1`
- `phase3_n32_o0.1_k2`
- `phase3_n32_o0.5_k3`

Supplemental out-of-domain conditions:

- `61` conditions (reported separately, not used for primary sufficiency interpretation).

## 5) Per-level outcomes (primary domain)

- `R0`: **SUFFICIENT_WITHIN_FIXTURE** (`3/3` primary-domain dominance success)
- `R1`: **SUFFICIENT_WITHIN_FIXTURE** (`3/3`)
- `R2`: **INSUFFICIENT_WITHIN_FIXTURE** (`1/3`)
- `R3`: **INSUFFICIENT_WITHIN_FIXTURE** (`1/3`)
- `R4`: **INSUFFICIENT_WITHIN_FIXTURE** (`2/3`)

Supplemental out-of-domain dominance success counts (reported separately):

- `R0`: `1/61`
- `R1`: `1/61`
- `R2`: `0/61`
- `R3`: `0/61`
- `R4`: `0/61`

## 6) R0 exact reproduction versus R0 leverage (separated)

R0 exact-reproduction/plumbing:

- `64/64` pass (`R0_EXACT_REPRODUCTION_PASS`)

R0 leverage on primary domain:

- `3/3` dominance success

A reproduction pass and leverage success were treated as separate evaluations.

## 7) R2 separation: `k=1` control vs `k>1` information reduction

R2 `k=1` control/equivalence:

- condition count: `16`
- exact-reproduction match count: `16`
- dominance success count: `1`

R2 `k>1` information-reduction segment:

- condition count: `48`
- exact-reproduction match count: `9`
- primary-domain dominance success count: `0`

`k=1` R2 behavior was reported as control/equivalence only, not generalized to multi-group sufficiency.

## 8) R3 separation: `k=1` behavior vs `k>1` evidence

R3 `k=1` behavior:

- condition count: `16`
- exact-reproduction match count: `16`
- dominance success count: `1`

R3 `k>1` evidence segment:

- condition count: `48`
- exact-reproduction match count: `9`
- primary-domain dominance success count: `0`

`k=1` R3 behavior was kept separate from `k>1` evidence.

## 9) Bounded interpretation

Within this frozen fixture and corrected frozen design:

- lossless representation controls (`R0`, `R1`) preserved Gate A-qualified leverage in the primary domain;
- reduced/coarsened representations (`R2`, `R3`, `R4`) did not uniformly preserve that leverage in the primary domain.

This does not establish production availability/generatability of successful representations and does not authorize HOW-2, Gate C, production selector work, or Category/YAML integration.

## 10) Explicit non-claims

This observation does not establish:

- production Path A selector realization;
- production availability of successful information;
- meaning claims;
- HOW-2 authorization;
- Gate C authorization;
- production selector or Category/YAML integration authorization.
