# 30.30_basin_prototypes / software_description.md

## 1. Purpose

This module explores basin behavior prototypes for the Thought Simulator and establishes a verification-capsule-ready structure for future basin-specific implementation and validation.

## 2. Scope

- prototype basin state and transition semantics
- define expected basin invariants for later enforcement
- prepare deterministic verification workflow through `harness.py`
- align module artifacts with the canonical playground capsule structure

## 3. Core Responsibilities

- model candidate basin behavior contracts before design promotion
- define basin entry/exit and processing assumptions for validation
- identify requirement-impact deltas produced by basin behavior decisions

## 4. Key Invariants (Current Baseline)

- basin behavior must be deterministic when deterministic mode is expected
- basin state changes must be observable and loggable for replay/audit
- basin prototype outputs must be compatible with canonical artifact storage under `artifacts/`

## 5. Current Implementation Status

- `prototype.py` is currently a scaffold (no basin logic implemented yet)
- `harness.py` is currently a template entrypoint (no validation scenarios implemented yet)
- verification status remains `NOT_STARTED` until executable scenarios and evidence are added

## 6. Verification Structure

Canonical module files:

- `software_description.md`
- `prototype.py`
- `harness.py`
- `verification_capsule.md`
- `requirements_delta.md`
- `artifacts/`

## 7. Open Questions

- Which basin state machine primitives should be standardized first?
- What minimum deterministic scenario set is required for first PASS verification?
- Which requirement documents should receive the first basin-specific deltas?
