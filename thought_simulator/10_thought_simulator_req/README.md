# Formal Requirement Anchor Layer

This directory is the formal requirement-anchor layer used to realize architecture and coding contracts after direction-controlled flow from 20/40.

## Canonical Anchors

- [10.10_math_requirements.md](10.10_math_requirements.md)
- [10.20_tp_requirements.md](10.20_tp_requirements.md)
- [10.30_basin_requirements.md](10.30_basin_requirements.md)
- [10.40_scheduler_requirements.md](10.40_scheduler_requirements.md)
- [10.50_regulator_requirements.md](10.50_regulator_requirements.md)
- [10.60_tick_cycle_requirements.md](10.60_tick_cycle_requirements.md)
- [10.70_snapshot_requirements.md](10.70_snapshot_requirements.md)
- [10.80_event_log_requirements.md](10.80_event_log_requirements.md)
- [10.90_experiment_runner_requirements.md](10.90_experiment_runner_requirements.md)

## Governance Artifacts

- [docs/promotion_protocol.md](docs/promotion_protocol.md)
- [docs/adrs/ADR-template.md](docs/adrs/ADR-template.md)
- [docs/](docs/)

## Boundary Note

- Primary requirement collaboration remains in [../20_requirements/](../20_requirements/).
- This 10-layer stores formalized realization anchors used by canonical design and verification flow.
- Terminology alignment baseline is [../20_requirements/archive/20.02_design_constraints.md](../20_requirements/archive/20.02_design_constraints.md), including the current use of Routing Basin (RB) naming.

Direction control (from USER_GUIDE policy):

- forward flow (typical): 20 -> 40 -> 10
- backward flow (when selected): 20 -> 10 -> 40

## 10-Layer Disambiguation (Required)

To prevent namespace confusion between 10-layer directories:

- `10_thought_simulator_req/` = canonical requirement anchors and promotion/backward-flow control source.
- `00_program_governance/` = program/foundation/architecture guidance references.

Flow-control rule:

- When a process step says "update 10" for promotion or backward-flow propagation, it means `10_thought_simulator_req/` unless explicitly stated otherwise.







