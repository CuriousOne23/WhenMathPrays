# Formal Requirement Anchor Layer

This directory is the formal requirement-anchor layer used to realize architecture and coding contracts after direction-controlled flow from 20/40.

## Internal Series Directories

All numbered series directories in this layer are subdirectories under `thought_simulator_req/`:

- `10_system_architecture/` = system architecture
- `20_requirements/` = requirements
- `30_verification/` = verification
- `40_playground/` = playground
- `50_design/` = design
- `60_review/` = review
- `70_measurement/` = measurement
- `80_safety/` = safety
- `90_validation/` = validation

The `10.50.xx` files are stored in `50_design/`.

## Canonical Anchors

- [50_design/10.50.270_math_requirements.md](50_design/10.50.270_math_requirements.md)
- [50_design/10.50.150_tp_requirements.md](50_design/10.50.150_tp_requirements.md)
- [50_design/10.50.160_basin_requirements.md](50_design/10.50.160_basin_requirements.md)
- [50_design/10.50.210_scheduler_requirements.md](50_design/10.50.210_scheduler_requirements.md)
- [50_design/10.50.220_regulator_requirements.md](50_design/10.50.220_regulator_requirements.md)
- [50_design/10.50.230_tick_cycle_requirements.md](50_design/10.50.230_tick_cycle_requirements.md)
- [50_design/10.50.240_snapshot_requirements.md](50_design/10.50.240_snapshot_requirements.md)
- [50_design/10.50.250_event_log_requirements.md](50_design/10.50.250_event_log_requirements.md)
- [50_design/10.50.260_experiment_runner_requirements.md](50_design/10.50.260_experiment_runner_requirements.md)
- [50_design/10.50.50_inb_design_requirements.md](50_design/10.50.50_inb_design_requirements.md)
- [50_design/10.50.60_iiinb_design_requirements.md](50_design/10.50.60_iiinb_design_requirements.md)
- [50_design/10.50.70_replay_design_requirements.md](50_design/10.50.70_replay_design_requirements.md)

## Governance Artifacts

- [docs/promotion_protocol.md](docs/promotion_protocol.md)
- [docs/adrs/ADR-template.md](docs/adrs/ADR-template.md)
- [docs/](docs/)

## Boundary Note

- Primary requirement collaboration remains in [../requirements_20/](../requirements_20/).
- This 10-layer stores formalized realization anchors used by canonical design and verification flow.
- Terminology alignment baseline is [../requirements_20/archive/20.02_design_constraints.md](../requirements_20/archive/20.02_design_constraints.md), including the current use of Routing Basin (RB) naming.

Direction control (from USER_GUIDE policy):

- forward flow (typical): 20 -> 40 -> 10
- backward flow (when selected): 20 -> 10 -> 40

## 10-Layer Disambiguation (Required)

To prevent namespace confusion between 10-layer directories:

- `thought_simulator_req/` = canonical requirement anchors and promotion/backward-flow control source.
- `00_program_governance/` = program/foundation/architecture guidance references.

Flow-control rule:

- When a process step says "update 10" for promotion or backward-flow propagation, it means `thought_simulator_req/` unless explicitly stated otherwise.

## Directory index (coverage-aligned)

- [10_system_architecture](10_system_architecture/)
- [20_requirements](20_requirements/)
- [30_verification](30_verification/)
- [40_playground](40_playground/)
- [50_design](50_design/)
- [60_review](60_review/)
- [70_measurement](70_measurement/)
- [80_safety](80_safety/)
- [90_validation](90_validation/)
