# IdOB Relational-Space Localization Observation (Gate B)

**Date:** 2026-11-27  
**Status:** Executed characterization observation record (non-normative).  
**Method authority:** [idob_relational_space_localization_research_plan.md](idob_relational_space_localization_research_plan.md).  
**Mechanical design:** [idob_relational_space_localization_gate_b_design.md](idob_relational_space_localization_gate_b_design.md).

## 1) Fixture reference

This record reports execution of the frozen Gate B characterization exactly as specified in the research plan and mechanical design. It does not redesign the provisional HOW, create HOW-2, begin Gate C, or promote results into requirements.

Characterization implementation:

- [idob_relational_space_localization_gate_b_characterization.py](../../support/tools/idob_relational_space_localization_gate_b_characterization.py)

Inherited Gate A fixture machinery:

- [idob_relational_space_localization_phase3_characterization.py](../../support/tools/idob_relational_space_localization_phase3_characterization.py)

Machine-readable evidence artifact:

- `local_characterization/sessions/idob_relational_space_localization_gate_b/runs/20261127_182357__idob_rel_space_localization_gate_b.json`

## 2) Executed conditions

Predeclared frozen families executed:

- cardinality: `n in {32, 64, 128, 256}`
- overlap: `o in {0, 0.10, 0.25, 0.50}`
- activation count: `k in {1, 2, 3, 4}`
- signal quality: `q in {q0, q1, q2, q3, q4}`
- false exclusion: `f in {0, 1, 2, floor(|R_necessary|/2)}` with frozen `NOT_CONSTRUCTIBLE` rule

Execution totals from artifact summary:

- base conditions: `320` (exact `4×4×4×5`)
- false-exclusion derivative conditions: `1200`
- constructible false-exclusion conditions: `961`
- `NOT_CONSTRUCTIBLE` false-exclusion conditions: `239`
- exhaustive matched baselines completed: `true`
- quality levels complete: `true`

## 3) Observations

### 3.1 q0 dominance / nontrivial useful-domain findings

- Nontrivial `q0` conditions satisfying the frozen dominance predicate: `0`
- `q0` conditions with dominance over every non-identical matched activation: `0`
- `q0` conditions with non-deteriorating improvement vs all matched baselines: `0`
- Therefore Gate B did **not** observe the CONTINUE/PARTIAL entry condition under `q0`.

### 3.2 Signal-quality, overlap, and activation pressures

Artifact distinguishability flags:

- `quality_pressure_distinguishable=true`
- `overlap_pressure_distinguishable=true`
- `activation_pressure_distinguishable=true`
- `pressures_distinguishable=true`

Lower-q schedule hold flags (dominance or non-deteriorating improvement at that level, without requiring nontrivial `q0` entry): `q1=true`, `q2=true`, `q3=true`, `q4=true`. These do not override the frozen `q0` dominance requirement.

### 3.3 False-exclusion pressure

- Constructible derivatives observed measurable coverage impact (`false_exclusion_distinguishable=true`).
- Gate B candidate activation was preserved; oracle was not re-run.
- `NOT_CONSTRUCTIBLE` derivatives were recorded under the frozen rule and not improvised.

### 3.4 Deterministic replay

Frozen replay requirement passed (`replay_pass=true`) with exact Gate B trace/fingerprint replay from identical inputs (including `X_base`, q transform, `X_t`, scores, ranking, activation, metrics).

### 3.5 Runtime information contract

Runtime selector `S` invoked with allowed inputs only (`X_t`, eight group IDs, `k`). Fixture-only `X_base` construction remained outside runtime `S` (`runtime_selector_contract_ok=true`).

## 4) Measured evidence summary

Artifact summary fields reported:

- `exhaustive_matched_baselines_completed=true`
- `quality_levels_complete=true`
- `replay_pass=true`
- `runtime_selector_contract_ok=true`
- `pressures_distinguishable=true`
- `false_exclusion_distinguishable=true`
- `nontrivial_q0_dominance_count=0`
- `insufficient_evidence_reasons=[]`

## 5) Gate B mechanical evaluation

Gate B classification: **NEGATIVE**

Mechanical reason (artifact):

> no tested nontrivial q0 condition satisfied frozen dominance predicate

Evaluation followed the frozen mechanical sequence (contract/trace/replay completeness first; then `q0` dominance). This classification is fixture-relative and provisional-HOW-relative per frozen authority.

## 6) Limitations (bounded)

1. Results are bounded to this frozen provisional non-oracle HOW and fixture-derived `X_t` schedule; they do not establish production Path A selector capability.
2. `NOT_CONSTRUCTIBLE` false-exclusion derivatives occurred under frozen construction and are retained as evidence, not repaired.
3. Observed limitations do not authorize HOW-2, retuning, post-hoc q levels, baseline changes, or dominance-rule changes within this research cycle.
4. This record does not perform Gate C work.

## 7) Explicit non-claims

This Gate B observation does not establish:

- a production Path A selector;
- that Path A can generate `X_base`;
- that Path A possesses equivalent signal information;
- meaning;
- semantic regions;
- contextual support;
- evidence-specific correspondence;
- door legality;
- traversal legality;
- final interpretation;
- Category dependence;
- final IdOB organization;
- final YAML structure;
- global signal thresholds;
- globally valid localization.
