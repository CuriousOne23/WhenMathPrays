# 30.30_basin_prototypes / software_description.md

## 1. Purpose

This module explores basin behavior prototypes for the Thought Simulator and establishes a verification-capsule-ready structure for future basin-specific implementation and validation.

## 2. Scope

- prototype basin state and transition semantics
- define expected basin invariants for later enforcement
- prepare deterministic verification workflow through `harness.py`
- align module artifacts with the canonical playground capsule structure

## 3. Source Index (Requirement Anchors)

This module derives its constraints from the existing canonical requirement set in  
`10_thought_simulator_req/20_requirements/`.

Existing requirement sources relevant to basin behavior:

- `20.30_tp_requirements.md` — TP identity, lifecycle, and state rules
- `20.50_observability_requirements.md` — logging, evidence, and replayability
- `20.60_testing_and_validation.md` — deterministic-mode, negative-path, and verification rules
- `20.90_interfaces_and_io.md` — IO schema, serialization, and interoperability
- `20.120_stability_requirements.md` — stability and transition constraints
- `20.140_program_flow.md` — system flow and phase-boundary rules
- `20.150_glossary.md` — canonical terminology
- `20.160_traceability_matrix.md` — requirement-to-test mapping obligations

Missing requirement coverage:
- No basin-specific requirement document currently exists.
  This module is expected to generate requirement deltas that may later justify a basin-focused design specification and, if needed, a basin requirement document.

## 4. Core Responsibilities

- model candidate basin behavior contracts before design promotion
- define basin entry/exit and processing assumptions for validation
- identify requirement-impact deltas produced by basin behavior decisions

## 5. Key Invariants (Current Baseline)

- basin behavior must be deterministic when deterministic mode is expected
- basin state changes must be observable and loggable for replay/audit
- basin prototype outputs must be compatible with canonical artifact storage under `artifacts/`

## 6. Current Implementation Status

- `prototype.py` is currently a scaffold (no basin logic implemented yet)
- `harness.py` is currently a template entrypoint (no validation scenarios implemented yet)
- verification status remains `NOT_STARTED` until executable scenarios and evidence are added

## 7. Verification Structure

Canonical module files:

- `software_description.md`
- `prototype.py`
- `harness.py`
- `verification_capsule.md`
- `requirements_delta.md`
- `artifacts/`

## 8. Open Questions

- Which basin state machine primitives should be standardized first?
- What minimum deterministic scenario set is required for first PASS verification?
- Which requirement documents should receive the first basin-specific deltas?
