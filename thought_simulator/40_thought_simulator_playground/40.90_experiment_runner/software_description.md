# Software Description

## Purpose

Define deterministic experiment-run orchestration for single-run and batch-run scenarios with reproducible metadata capture.

## Approval State

Phase A status: pending human approval.

Phase B execution (prototype/harness/capsule evidence updates) must not be treated as promotable until this description is explicitly approved.

## Source Index

- `20_requirements/20.110_experiment_requirements.md`
- `20_requirements/20.90_interfaces_and_io.md`
- `20_requirements/20.60_testing_and_validation.md`
- `20_requirements/20.50_observability_requirements.md`
- `20_requirements/20.140_program_flow.md`
- `../40.20_master_program_guide.md`

## Core Responsibilities

- Define run configuration envelope and deterministic execution identity.
- Record batch execution metadata and per-run status evidence.
- Provide replay-safe output contracts for experiment analysis.

## Key Invariants

- Equivalent experiment definitions produce equivalent execution identities in deterministic mode.
- Batch results are order-stable and fully traceable.
- Run metadata includes configuration hash and result summary.

## Data Structures / Interfaces (tentative)

- `experiment_request` (json object): experiment id, config ref, seed, limits, metadata.
- `experiment_result` (json object): run id, status, metrics summary, artifact pointers.

## Open Questions

- What batching policies are required for deterministic merge ordering?
- Which experiment metadata fields are mandatory for promotion-grade auditability?
- Should failed-run artifacts be mandatory for every failure class?
