# IdOB Relational-Space Localization Observation (S2M Structure Observation Surface)

**Date:** 2026-11-28  
**Status:** EXECUTED / PENDING REVIEW (characterization observation record; non-normative).  
**Proposal authority:** [idob_relational_space_localization_s2m_structure_observation_surface_proposal.md](idob_relational_space_localization_s2m_structure_observation_surface_proposal.md).  
**Design authority:** [idob_relational_space_localization_s2m_structure_observation_surface_design.md](idob_relational_space_localization_s2m_structure_observation_surface_design.md).

Review state: **BEING REVIEWED**  
Note: This edit corrects interpretation of existing evidence only. It is not a new experiment and does not change the evidence itself.

## 1) Scope

Executed one bounded run of the frozen M1-M6 scientific characterization matrix only.

- Primary objective: characterize observable organization in retained S2M observation surfaces under controlled structural variation.
- Secondary objective: record any bounded leverage indications separately.
- No architecture change, no localization-source selection, no new read edge, no HOW-2, no Gate C, no production integration.

## 2) Characterization implementation and machine-readable evidence

Characterization implementation:

- [idob_relational_space_localization_s2m_structure_observation_surface_characterization.py](../../support/tools/idob_relational_space_localization_s2m_structure_observation_surface_characterization.py)

Evidence artifact:

- `local_characterization/sessions/idob_relational_space_localization_s2m_structure_observation_surface/runs/20261128_001205__idob_rel_space_localization_s2m_structure_observation_surface.json`

Source artifacts referenced by the bounded run:

- traversal: `local_characterization/sessions/s2m_idob_traversal_exp/runs/20261125_073021__s2m_idob_traversal_exp.json`
- correspondence: `local_characterization/sessions/s2m_idob_correspondence_exp/runs/20261125_083313__s2m_idob_correspondence_exp.json`
- lineage/opposition: `local_characterization/sessions/s2m_idob_lineage_opposition_exp/runs/20261125_085112__s2m_idob_lineage_opposition_exp.json`

## 3) Frozen M1-M6 cell realization (underlying bounded matrix)

| Cell | Condition class | Seed surface | Candidate surface | Support surface |
|---|---|---|---|---|
| M1 | cue absent, sentence-only, candidate available | available (`written_relations_count=1`) | available (`candidate_count=4`) | available (`supporting=0`, `no_established_relation=4`) |
| M2 | cue present, sentence-only, candidate available | available (`written_relations_count=1`) | available (`candidate_count=3`) | available (cue-present; bounded support-state representation not established in this cell) |
| M3 | cue present, prior single-source, candidate available | available (`written_relations_count=1`) | available (`candidate_count=4`, `legitimized=1`) | available (`supporting=1`, `no_established_relation=3`) |
| M4 | cue present, prior repeated evidence, candidate available | available | available (`candidate_count=4`) | available (`supporting=3`, `no_established_relation=9`, dependency states include `Dependent`) |
| M5 | cue present, prior mixed source, candidate available | available | available (`candidate_count=4`) | available (`supporting=3`, `no_established_relation=9`, dependency states all `Unknown`) |
| M6 | candidate surface unresolved/unavailable boundary condition | available | unresolved (`candidate_count=0`) | unresolved (`unresolved=2`) |

## 4) Frozen controls and audits

### 4.1 Removal control (M3 vs M1)

- seed written-relation delta: `0`
- candidate-count delta: `0`
- supporting-state delta: `+1`
- legitimized-selection delta: `+1`

### 4.2 Boundary control (available cells vs M6)

- M1-M5 candidate-surface state: all `available`
- M6 candidate-surface state: `unresolved`
- M6 unresolved support count: `2`

### 4.3 Provenance-variation control (M3 vs M4 vs M5)

- M3 dependency-state representation: `{}` (none represented in this bounded slice)
- M4 dependency states: `Dependent=8`, `Unknown=4`
- M5 dependency states: `Unknown=12`

### 4.4 Anti-shortcut / leakage checks

- oracle/privileged information exclusion: pass
- post-transition leakage exclusion: pass
- evaluator isolation: pass
- unresolved/unavailable handling integrity: pass
- position/name shortcut permutation check: not applicable (`UNAVAILABLE_PER_FROZEN_DESIGN`)

## 5) Primary observations (bounded to retained surfaces)

- M1 vs M3 shows a cue-related difference in represented legitimized/supporting signal.
- M3 vs M4 vs M5 shows provenance/repetition/mixed-source-related differences in represented dependency organization.
- M6 exposes an unresolved/availability boundary under the retained observation surfaces.

Underlying cell notes (unchanged evidence):

- Cue-absent M1 showed no legitimized/supporting signal.
- Cue-present M3 showed a bounded legitimized/supporting signal.
- M4 and M5 separated on dependency-state organization (`Dependent` represented in M4, not in M5).
- M6 realized the expected unresolved boundary condition (intentionally frozen as unresolved/unavailable).

These are case-bounded characterization observations on the selected TC/CR anchor records under the frozen contrasts, in retained surfaces only. They are not architectural claims.

## 6) Secondary utility channel (separate, subordinate)

Secondary S2M leverage findings remain explicitly subordinate to primary structure characterization.

Bounded indications recorded:

- `M3 vs M1`: legitimized/supporting signal increase under cue-presence contrast.
- `M4 vs M3`: dependency-state constraint signal appears in repeated-evidence condition.

Non-findings retained:

- no localization mechanism claim;
- no basis-parameter claim;
- no monotonic narrowing claim.

## 7) Completeness and replay

- completeness: pass (all frozen cells/surfaces/controls present)
- semantic-slice exact replay: pass (matching fingerprint on duplicate extraction pass)
- integrity: `PASS`

## 8) Interpretation of outcomes (evidence unchanged)

Global interpretation of this executed package:

- `PARTIAL_PRIMARY_CHARACTERIZATION_WITH_UNRESOLVED_BOUNDARY`

Localized M6 limitation (not a global surface-coarseness verdict):

- `SURFACE_TOO_COARSE_AT_M6_BOUNDARY`
  - M6 was intentionally frozen as an unresolved/unavailable boundary condition. Its remaining unresolved state is evidence of that observational boundary represented by M6, not by itself evidence that all retained S2M observation surfaces are too coarse for the primary objective.
  - The previous global label `SURFACE_TOO_COARSE_FOR_PRIMARY_OBJECTIVE` is withdrawn as the package-level result; it overstated the M6 boundary as a global primary-objective failure.

This interpretive correction does not change underlying experimental evidence, cell membership, controls, audits, completeness, replay, or integrity results.

## 9) Explicit claim boundary

This run supports only bounded surface-level organization characterization under the frozen matrix and retained authority.

M1-M5 findings are case-bounded evidence of distinguishable organization across the selected TC/CR anchor records under the frozen contrasts. They do **not** establish that the observed organization generalizes across other members of the corresponding natural condition classes.

It does **not** establish:

- localization-source authorization;
- architecture requirements or architecture change;
- a realized localization mechanism;
- basis-parameter structure as a required form;
- monotonic narrowing claim / localization claim / general S2M structure claim;
- natural-structure discovery closeout.
