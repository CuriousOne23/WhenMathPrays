---
status: verification
source_of_truth: this
contains:
  - LLR: [LLR-30.000-001]
---

# 30_verification

This folder is the authoritative verification tier for Thought Simulator modules.

## Purpose

- store promoted verification capsules
- store deterministic evidence artifacts
- separate verification evidence from exploratory playground work

## Promotion Policy

Promotion into this folder is intentional and manual.

Each promoted module should include:

- a verification capsule
- deterministic replay evidence
- JSON artifacts
- negative-path coverage evidence
- reviewer sign-off metadata

## Current Seeded Modules

- [30.10_math_prototypes/](30.10_math_prototypes/)
- [30.20_tp_lifecycle/](30.20_tp_lifecycle/)
- [30.30_basin_prototypes/](30.30_basin_prototypes/)
- [30.40_scheduler_prototypes/](30.40_scheduler_prototypes/)
- [30.50_regulator_prototypes/](30.50_regulator_prototypes/)
- [30.60_tick_cycle_skeleton/](30.60_tick_cycle_skeleton/)
- [30.70_snapshot_prototypes/](30.70_snapshot_prototypes/)
- [30.80_event_log_prototypes/](30.80_event_log_prototypes/)
- [30.90_experiment_runner/](30.90_experiment_runner/)
- [30.30_verification_glossary.md](30.30_verification_glossary.md)
- [glossary_term_registry.json](glossary_term_registry.json)

These were copied from the playground as the first phase of the refactor and should be treated as initial promoted evidence snapshots.
