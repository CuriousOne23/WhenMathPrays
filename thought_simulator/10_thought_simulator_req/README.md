# Canonical Requirement Governance Root

This directory is the canonical requirement-governance root for promoted requirement anchors.

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

- Exploratory requirement reasoning remains in [../20_requirements/](../20_requirements/).
- Canonical requirement anchors in this directory are the authoritative requirement source for canonical design and verification flow.
- Terminology alignment baseline is [../20_requirements/20.02_design_constraints.md](../20_requirements/20.02_design_constraints.md), including the current use of Routing Basin (RB) naming.

## 10-Layer Disambiguation (Required)

To prevent namespace confusion between 10-layer directories:

- `10_thought_simulator_req/` = canonical requirement anchors and promotion/backward-flow control source.
- `10_program_governance/` = program/foundation/architecture guidance references.

Flow-control rule:

- When a process step says "update 10" for promotion or backward-flow propagation, it means `10_thought_simulator_req/` unless explicitly stated otherwise.







