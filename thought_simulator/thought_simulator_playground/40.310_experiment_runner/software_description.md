# Software Description

## Purpose

Define deterministic experiment-run orchestration for single-run and batch-run scenarios with reproducible metadata capture.

## Approval State

Approved by human on 2026-05-28 (Phase A complete; eligible for 50.05 execution).

Phase B execution completed; promotion remains governed by canonical 10/30/50 artifacts.

## Source Index

- `20_requirements/20.30_ts_functional_model.md`
- `20_requirements/20.90_ib_requirements.md`
- `20_requirements/20.200_traceability_matrix.md`
- `20_requirements/20.40_ob_requirements.md`
- `../../40_thought_simulator_playground/40.05_master_program_guide.md`

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
