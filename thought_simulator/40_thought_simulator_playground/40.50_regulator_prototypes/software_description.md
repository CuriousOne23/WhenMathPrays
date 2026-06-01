# Software Description

## Purpose

Define exploratory regulator behaviors that can adjust ThoughtPoint trajectory pressure while preserving deterministic execution rules.

## Approval State

Approved by human on 2026-05-28 (Phase A complete; eligible for 50.05 execution).

Phase B execution completed; promotion remains governed by canonical 10/30/50 artifacts.

## Source Index

- `20_requirements/archive/20.20_error_and_stability_requirements.md`
- `20_requirements/archive/20.120_stability_requirements.md`
- `20_requirements/archive/20.140_program_flow.md`
- `20_requirements/archive/20.60_testing_and_validation.md`
- `20_requirements/archive/20.90_interfaces_and_io.md`
- `../40.20_master_program_guide.md`

## Core Responsibilities

- Define deterministic regulator policy hooks for suppression, attenuation, and stabilization.
- Preserve clear separation between regulator decisions and core basin state mutation.
- Emit regulator decision evidence fields suitable for replay and audit.

## Key Invariants

- Regulator outputs are deterministic for equivalent inputs in deterministic mode.
- Regulator actions are explicit and observable; no hidden side effects.
- Regulator processing does not mutate unrelated module state.

## Data Structures / Interfaces (tentative)

- `regulator_input` (json object): policy context, tick, TP snapshot, pressure indicators.
- `regulator_decision` (json object): action, rationale code, applied limits, observability fields.

## Open Questions

- Which regulator actions must be hard-fail vs soft-fail under instability conditions?
- Should regulator policies be ordered by fixed precedence or weighted tie-break?
- What minimum evidence fields are required for promotion-grade regulator verification?
