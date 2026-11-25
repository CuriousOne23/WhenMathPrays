# IdOB Relational-Space Localization Observation (Gate A / Phase 3)

**Date:** 2026-11-25  
**Status:** Executed characterization observation record (non-normative).  
**Method authority:** [idob_relational_space_localization_research_plan.md](idob_relational_space_localization_research_plan.md).

## 1) Fixture reference

This record reports execution of the frozen Gate A / Phase 3 fixture exactly as defined in the research plan authority.

Characterization implementation:

- [idob_relational_space_localization_phase3_characterization.py](../../support/tools/idob_relational_space_localization_phase3_characterization.py)

Machine-readable evidence artifact:

- `local_characterization/sessions/idob_relational_space_localization_phase3/runs/20261125_190620__idob_rel_space_localization_phase3.json`

## 2) Executed conditions

Predeclared frozen families executed:

- cardinality: `n in {32, 64, 128, 256}`
- overlap: `o in {0, 0.10, 0.25, 0.50}`
- activation count: `k in {1, 2, 3, 4}`
- false exclusion: `f in {0, 1, 2, floor(|R_necessary|/2)}` with frozen `NOT_CONSTRUCTIBLE` rule

Execution totals from artifact summary:

- base conditions: `64`
- false-exclusion derivative conditions: `240`
- constructible false-exclusion conditions: `210`
- `NOT_CONSTRUCTIBLE` false-exclusion conditions: `30`
- exhaustive matched baselines completed: `true`

## 3) Observations

### 3.1 Gate A dominance / nontrivial useful-domain findings

- Nontrivial useful-domain conditions satisfying frozen dominance predicate were observed (`3` conditions).
- Therefore, “no nontrivial dominance even under oracle-only surrogate” was **not** observed.

### 3.2 Overlap pressure

Candidate active-surface size increased under overlap schedule in aggregate:

- average candidate `|R_active|` by overlap:
  - `o=0.0 -> 37.5`
  - `o=0.10 -> 40.4375`
  - `o=0.25 -> 46.3125`
  - `o=0.50 -> 55.375`

Pressure effect was mechanically distinguishable (`overlap_pressure_distinguishable=true`).

### 3.3 Activation-count pressure

Candidate active-surface size increased with activated-group count in aggregate:

- average candidate `|R_active|` by k:
  - `k=1 -> 18.1875`
  - `k=2 -> 36.125`
  - `k=3 -> 54.0625`
  - `k=4 -> 71.25`

Pressure effect was mechanically distinguishable (`activation_pressure_distinguishable=true`).

### 3.4 False-exclusion pressure

- Constructible derivatives observed measurable coverage impact (`false_exclusion_distinguishable=true`).
- Constructible derivative coverage-drop summary (candidate under derivative vs base candidate for same fixture):
  - mean drop: `0.15119047619047618`
  - min drop: `0.0`
  - max drop: `0.5`
- `NOT_CONSTRUCTIBLE` was present and explicitly recorded per frozen rule:
  - by `f`: `{2: 5, 4: 7, 8: 8, 16: 10}`
  - by `n`: `{32: 4, 64: 8, 128: 8, 256: 10}`

### 3.5 Deterministic replay

Frozen replay requirement passed (`replay_pass=true`) with exact candidate-condition trace/fingerprint replay from identical inputs.

### 3.6 Identity stability under reorganization

Identity-stability checks were executed for each frozen cardinality (`n=32,64,128,256`) and passed:

- admitted-identity stability: true for all checks;
- active-surface change attribution check: true for all checks.

## 4) Measured evidence summary

Artifact summary fields reported:

- `exhaustive_matched_baselines_completed=true`
- `replay_pass=true`
- `identity_stability_pass=true`
- `overlap_pressure_distinguishable=true`
- `activation_pressure_distinguishable=true`
- `false_exclusion_distinguishable=true`
- `nontrivial_dominance_exists=true`

## 5) Gate A mechanical evaluation

Gate A classification: **CONTINUE**

Mechanical reason (artifact):

> at least one nontrivial condition satisfied frozen dominance predicate and fixture mechanically distinguished false exclusion, overlap pressure, activation-count pressure, deterministic replay, and identity preservation

This classification is fixture-relative and oracle-relative per frozen authority.

## 6) Limitations (bounded)

1. Results are bounded to this frozen oracle-only surrogate fixture and do not establish production Path A selector capability.
2. `NOT_CONSTRUCTIBLE` false-exclusion derivatives occurred under frozen construction and are retained as evidence, not repaired.
3. This record does not perform Gate B work.

## 7) Explicit non-claims

This Phase 3 observation does not establish:

- production Path A selector realization;
- possession of oracle information by production Path A;
- meaning, semantic regions, contextual support, or evidence-specific correspondence;
- door legality or traversal legality;
- final IdOB organization or final YAML representation;
- global thresholds or globally valid localization utility.

