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

- [30.20_tp_lifecycle/](30.20_tp_lifecycle/)
- [30.30_basin_prototypes/](30.30_basin_prototypes/)
- [30.40_scheduler_prototypes/](30.40_scheduler_prototypes/)
- [30.30_verification_glossary.md](30.30_verification_glossary.md)
- [glossary_term_registry.json](glossary_term_registry.json)

These were copied from the playground as the first phase of the refactor and should be treated as initial promoted evidence snapshots.
