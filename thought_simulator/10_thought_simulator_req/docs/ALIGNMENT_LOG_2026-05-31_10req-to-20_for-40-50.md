# 10_thought_simulator_req Alignment Log (2026-05-31)

## Purpose
Record canonical-anchor refactor changes made in 10_thought_simulator_req to align with 20-series terminology and architectural boundaries, and capture required follow-on impacts for 40/50 refactors.

## Alignment Baseline
- 20-series architectural baseline: ../../20_requirements/20.05_design_constraints.md
- Key alignment targets:
  - Routing Basin (RB) terminology
  - Basin family coverage (OB, RB, GB, IB, TB, InB, OuB, MB)
  - Control component taxonomy (Regulator, Watchdog, Flow Modulator)
  - Observer/orchestration boundary language
  - Deterministic split/merge arbitration phase framing

## Files Changed in 10_thought_simulator_req

1. README.md
- Added explicit boundary note that terminology alignment follows 20.05.
- Added explicit mention that RB naming baseline is Routing Basin.

2. 10.30_basin_requirements.md
- Added purpose-level note that RB naming follows Routing Basin terminology.
- Expanded canonical scope to explicitly cover basin-family contract applicability across OB, RB, GB, IB, TB, InB, OuB, MB variants.

3. 10.50_regulator_requirements.md
- Expanded canonical scope to explicitly include control-component compatibility language for Regulator, Watchdog-class actions, and Flow Modulator actions.

4. 10.60_tick_cycle_requirements.md
- Expanded canonical scope to include deterministic phase-boundary compatibility for observer-signal ingestion and split/merge arbitration ordering.

5. 10.90_experiment_runner_requirements.md
- Expanded canonical scope to include observer/orchestration boundary preservation for experiment control surfaces.

## What Was Intentionally Not Changed
- No HLR IDs changed.
- No verification capsule paths changed.
- No canonical requirement numbering changed.
- No changes to 10_program_governance in this pass (that alignment was completed separately).

## Required Follow-On Changes for 40 and 50 Refactors

### 40_thought_simulator_playground
1. Update RB naming in all prototype docs/code/comments to Routing Basin (RB).
2. Ensure basin prototypes and fixtures cover GB, IB, TB, InB, OuB, MB where applicable.
3. Add/verify deterministic split/merge arbitration ordering in tick-cycle playground scaffolds.
4. Add/verify observer-signal ingestion only at fixed tick boundaries in experimental runners.
5. Add/verify control component traces include Regulator/Watchdog/Flow Modulator source attribution.
6. Keep backward-compatible parsing/labels for legacy Relational Basin alias where historical artifacts are consumed.

### 50_thought_simulator_design
1. Align design docs to canonical scope additions from 10.30/10.50/10.60/10.90.
2. Add explicit section language for control component taxonomy (Regulator + Watchdog + Flow Modulator).
3. Add design-level statement for observer/orchestration boundary compatibility in experiment orchestration docs.
4. Add design-level split/merge arbitration phase ordering notes where tick-cycle behavior is specified.
5. Ensure diagrams and tables use Routing Basin naming consistently.

## Migration Safety Notes
- Preserve legacy term compatibility in transitional documentation by noting: RB historical alias = Relational Basin.
- Prioritize semantic equivalence over broad text-only replacement in 40/50 where historical references are explicit.

## Status
- 10_thought_simulator_req alignment pass complete for requested scope.
- Ready for 40/50 refactor planning and execution using this log.
