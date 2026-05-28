# Software Description

## Purpose

Define a deterministic tick-cycle skeleton with explicit phase ordering and replay-safe state transition boundaries.

## Approval State

Phase A status: pending human approval.

Phase B execution (prototype/harness/capsule evidence updates) must not be treated as promotable until this description is explicitly approved.

## Source Index

- `20_requirements/20.140_program_flow.md`
- `20_requirements/20.50_observability_requirements.md`
- `20_requirements/20.60_testing_and_validation.md`
- `20_requirements/20.90_interfaces_and_io.md`
- `../40.20_master_program_guide.md`

## Core Responsibilities

- Define canonical phase sequencing for each tick.
- Enforce monotonic tick advancement and no phase re-entry within a tick.
- Emit phase-boundary evidence fields for replay and diagnostics.

## Key Invariants

- Tick index is monotonic and non-negative.
- Phase order is fixed and deterministic.
- Phase outputs are JSON-compatible and traceable per tick.

## Data Structures / Interfaces (tentative)

- `tick_input` (json object): previous state digest, current tick index, enabled phases.
- `tick_output` (json object): next state digest, executed phase list, phase-level diagnostics.

## Open Questions

- What is the minimal mandatory phase set for canonical promotion?
- Should phase hooks be strict functions or pluggable adapters with constraints?
- Which phase-level failures are recoverable versus terminal?
