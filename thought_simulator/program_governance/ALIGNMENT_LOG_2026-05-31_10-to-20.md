# 10-to-20 Alignment Log (2026-05-31)

## Purpose
Record terminology and concept alignment updates made in 10-program-governance to match the current 20-series baseline, especially `20.02_design_constraints.md`.

## Summary
- Primary migration: RB naming aligned to **Routing Basin (RB)**.
- Historical continuity preserved with explicit alias note: **Relational Basin (RB)** in legacy docs.
- Basin variant coverage aligned with 20.05 (IB/GB/TB/InB/OuB/MB).
- Control-component language aligned with 20.05 (Flow Modulator, Watchdog-class behavior).

## Files Updated

1. `00_program_governance/00_foundations/00.00.10_vision_and_objectives.md`
- Updated definition language from Relational Basins to Routing Basins.
- Updated TS core bullet to use Routing Basins.
- Renamed section heading to `Routing Basins (RBs)`.
- Added historical alias note.

2. `00_program_governance/00_foundations/00.00.20_core_philosophy_and_principles.md`
- Updated TS primacy statement to use Routing Basins.
- Renamed section heading to `Object Basins and Routing Basins`.
- Updated RB definition bullet to Routing Basins.
- Added historical alias note.

3. `00_program_governance/00_foundations/00.00.30_core_conceptual_requirements.md`
- Updated TS core update responsibilities to Routing Basins.
- Updated damping comparison phrase to Routing Basins.
- Renamed section heading to `Routing Basins (RBs)`.
- Added historical alias note.
- Updated OB vs RB table column title to Routing Basins.

4. `00_program_governance/10_architecture/00.10.10_system_architecture.md`
- Expanded TS Core layer description to explicitly include control components terminology:
  - `Flow Modulators`
  - `Watchdog behaviors`

5. `00_program_governance/10_architecture/00.10.20_manifold_specification.md`
- Renamed manifold geometry subheading:
  - `Relational Basin (RB) Geometry` -> `Routing Basin (RB) Geometry`

6. `00_program_governance/10_architecture/00.10.30_basins.md`
- Updated opening basin taxonomy to Routing Basins.
- Added historical alias note.
- Updated damping comparison phrase to Routing Basins.
- Renamed section `3.2` to `Routing Basins (RBs)`.
- Expanded `3.3 Other Basin Variants` list to include:
  - `Inquiry Basins (IB)`
  - `Governing Basins (GB)`
  - `Truth Basins (TB)`
  - `Input Basins (InB)`
  - `Output Basins (OuB)`
  - `Monitoring Basins (MB)`

7. `00_program_governance/10_architecture/00.10.40_TS_state_machine.md`
- Updated entropy update line to Routing Basins.
- Updated regulator line to explicitly include:
  - `Flow Modulators`
  - `Watchdog class behaviors`

## Validation Notes
- Search across `00_program_governance/**/*.md` shows no remaining active use of `Relational Basin(s)` except in explicit historical-note alias lines.
- No changes were required in `10_thought_simulator_req` for this alignment pass.

## Intended Follow-On Use
This log is intended to be used as direct input for subsequent terminology/concept refactors in:
- `40_thought_simulator_playground`
- `50_thought_simulator_design`



