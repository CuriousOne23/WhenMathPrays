# 40.260_basin_prototypes / software_description.md

## Approval State

- Legacy baseline: **approved** (pre–Two-Phase policy)
- **W3 Phase A** (40.510-412 full redo): **approved** (CP W3 Phase A review, 2026-06-08 — no blockers)
- W3 Phase B (decompose/realign to normative A basins per 20.01 B2): **cleared to start** — pending implementation
- Program row: **40.510-412** (W3)

## W3 Full Redo Scope (40.510-412)

The generic pre-partition basin model SHALL be decomposed or realigned to normative Pipeline A basins per [20.01](../../20_requirements/20.01_architecture_map.md) B2 and [40.510](../40.510_refactor.md) A-chain bundle (405–411):

- RB / OB / DCB / TB / IB roles MUST NOT collapse into a single generic basin type
- Phase B may retain shared harness utilities but MUST split basin contracts to match 40.190, 40.200, 40.210, 40.230, 40.250 boundaries
- Strip-replay fixtures SHALL not depend on legacy generic basin IDs after W3 closure

**Agreement Statement (W3 Phase A)**: Aligned — CP review 2026-06-08 confirms W3 full redo scope: decompose generic basin model to normative A-basin boundaries per 20.01 B2; legacy verification artifacts retained until Phase B maps regression to 40.190/40.200/40.210/40.230/40.250 contracts.

## CP W3 Phase A Review Record (2026-06-08)

| Check | Result |
|-------|--------|
| W3 full redo scope vs 40.510-412 | Pass |
| 20.01 B2 normative A-basin decomposition | Pass |
| No collapse of RB/OB/DCB/TB/IB roles | Pass |
| Handoff to 40.190/200/210/230/250 boundaries | Pass |
| Legacy artifacts retained until Phase B regression map | Pass |
| Blockers | **None** — Phase B authorized |

## Two-Phase Execution Model (Global 40.* Rule)

- Phase A: generate and review `software_description.md` only.
- Mandatory stop after Phase A until explicit human approval.
- Phase B (only after approval): `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

## 1. Purpose

This module explores basin behavior prototypes for the Thought Simulator and establishes a verification-capsule-ready structure for future basin-specific implementation and validation.

## 2. Scope

- prototype basin state and transition semantics
- define expected basin invariants for later enforcement
- prepare deterministic verification workflow through `harness.py`
- align module artifacts with the canonical playground capsule structure

## 3. Source Index (Requirement Anchors)

This module derives its constraints from the existing canonical requirement set in  
`20_requirements/`.

Existing requirement sources relevant to basin behavior:

- `20.105_tp_requirements.md` - TP identity, lifecycle, and state rules
- `20.40_ob_requirements.md` - logging, evidence, and replayability
- `20.200_traceability_matrix.md` - deterministic-mode, negative-path, and verification rules
- `20.90_ib_requirements.md` - IO schema, serialization, and interoperability
- `20.170_safety_requirements.md` - stability and transition constraints
- `20.30_ts_functional_model.md` - system flow and phase-boundary rules
- `../../30_verification/30.160_verification_glossary.md` - canonical verification terminology
- `20.200_traceability_matrix.md` - requirement-to-test mapping obligations

Missing requirement coverage:
- No basin-specific requirement document currently exists.
  This module is expected to generate requirement deltas that may later justify a basin-focused design specification and, if needed, a basin requirement document.

## 4. IO Contract

The basin prototype uses JSON-compatible dictionary structures as its public contract.

Inbound variables:

- `basin_id` (`str`): required, non-empty, stable basin identifier
- `tp_id` (`str`): required, non-empty TP identity field preserved without transformation
- `state_counter` (`int`): required, non-negative monotonic counter
- `deterministic_mode` (`bool`): required, controls stable replay behavior
- `entropy_vector` (`list[float]`): required, non-empty numeric vector used for basin state evidence
- `provenance_ids` (`list[str]`): optional on create, required for provenance updates, unique non-empty values only
- `tags` (`list[str]`): optional, JSON-safe labels
- `metadata` (`dict[str, JSON]`): optional, JSON-compatible context payload

Outbound variables:

- `basin_id`, `tp_id`, and `state_counter`: preserved canonical identity fields
- `history` (`list[dict]`): ordered, JSON-compatible event ledger
- `last_event` (`str`): latest lifecycle action name
- `last_tick` (`int`): last applied tick value
- `verification_digest` (`str`): deterministic digest of the current snapshot
- `invariants` (`dict[str, bool]`): explicit invariant checks used by the harness

Public API functions:

- `BasinPrototype.from_contract(payload)` creates basin state from a validated inbound payload
- `BasinPrototype.apply_contract(payload)` mutates basin state using an event payload and returns a snapshot
- `BasinPrototype.snapshot()` returns a JSON-compatible read-only evidence payload

Formatting and interoperability rules:

- Inputs and outputs must remain JSON serializable
- Numeric vectors must remain plain lists of numbers
- Consumers must not depend on Python object identity
- Required identity fields must be preserved exactly
- Any future schema extension must remain backward-compatible where possible

## 5. Core Responsibilities

- model candidate basin behavior contracts before design promotion
- define basin entry/exit and processing assumptions for validation
- identify requirement-impact deltas produced by basin behavior decisions

## 6. Key Invariants (Current Baseline)

- basin behavior must be deterministic when deterministic mode is expected
- basin state changes must be observable and loggable for replay/audit
- basin prototype outputs must be compatible with canonical artifact storage under `artifacts/`

## 7. Current Implementation Status

- `prototype.py` is currently a scaffold (no basin logic implemented yet)
- `harness.py` is currently a template entrypoint (no validation scenarios implemented yet)
- verification status remains `NOT_STARTED` until executable scenarios and evidence are added

## 8. Verification Structure

Canonical module files:

- `software_description.md`
- `prototype.py`
- `harness.py`
- `verification_capsule.md`
- `requirements_delta.md`
- `artifacts/`

## 9. Open Questions

- Which basin state machine primitives should be standardized first?
- What minimum deterministic scenario set is required for first PASS verification?
- Which requirement documents should receive the first basin-specific deltas?

