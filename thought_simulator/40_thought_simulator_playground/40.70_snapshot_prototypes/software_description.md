# Software Description

## Purpose

Define deterministic snapshot save/load patterns with schema stability, integrity checks, and replay compatibility.

## Approval State

Phase A status: pending human approval.

Phase B execution (prototype/harness/capsule evidence updates) must not be treated as promotable until this description is explicitly approved.

## Source Index

- `20_requirements/20.90_interfaces_and_io.md`
- `20_requirements/20.80_security_and_safety_requirements.md`
- `20_requirements/20.50_observability_requirements.md`
- `20_requirements/20.60_testing_and_validation.md`
- `../40.20_master_program_guide.md`

## Core Responsibilities

- Define snapshot schema envelope and version tagging.
- Ensure deterministic serialization for equivalent state payloads.
- Validate snapshot integrity and load-compatibility behavior.

## Key Invariants

- Snapshot payloads are JSON-compatible and schema-versioned.
- Integrity verification occurs before state import.
- Round-trip snapshot load preserves required identity fields.

## Data Structures / Interfaces (tentative)

- `snapshot_payload` (json object): schema version, state body, digest, metadata.
- `snapshot_load_result` (json object): status, normalized state, diagnostics.

## Open Questions

- What backward-compatibility window is required between schema versions?
- Which fields are mandatory for promotion-grade replayability?
- Should snapshot digest include metadata or state body only?
