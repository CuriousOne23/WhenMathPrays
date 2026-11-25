# S2M IdOB Traversal Correspondence Representability Plan

**Date:** 2026-11-25  
**Status:** Frozen bounded plan for correspondence/lineage representability.  
**Contract authority:** [s2m_idob_traversal_correspondence_contract.md](s2m_idob_traversal_correspondence_contract.md).  
**Purpose:** Pure audit of evidence-specific support correspondence representability using existing TS represented facts only.

## Local-utility success criterion

This experiment is successful if it either:

1. turns a currently ambiguous distinction into an inspectable represented state; or
2. narrows and clarifies an Unknown/Unresolved/Unavailable boundary without fabrication.

## Scope

In scope:

- aggregate candidate-support vs evidence-specific support distinction;
- representability of support/no-established-relation/unresolved/unavailable correspondence outcomes;
- provenance retention and source attribution;
- repeated-observation handling visibility;
- dependency-state representability (`Dependent/Unknown`) where legitimately derivable.

Out of scope:

- traversal algorithm;
- `D_t/Q_t` formulas;
- `B_t`, traversal `P_t/H_t`;
- continue/OuBA sufficiency;
- Category Selection policy changes.

## Execution gate (must pass before run)

Only execute if all required test quantities are either:

1. already available; or
2. derivable without semantic/architectural change.

If explicit opposition, lineage identity, or dependency typing requires creating new semantics/mechanisms, mark affected cases `UNAVAILABLE` and keep boundary reporting explicit.

Primary audit question:

Can TS reconstruct, for a particular evidence observation and candidate, the full affirmative chain:

`evidence_observation -> evidence_property_or_cue -> candidate_property_correspondence -> candidate`?

If any required link is missing, classify the chain as incomplete and record the exact missing link.

Audit labels (frozen):

- `COMPLETE_CHAIN`
- `AGGREGATE_SUPPORT_ONLY`
- `NO_ESTABLISHED_RELATION`
- `UNRESOLVED`
- `UNAVAILABLE`

## Planned representability cases (frozen)

| Case ID | Goal | Required state | Current representability expectation |
|---|---|---|---|
| `EA01_aggregate_vs_evidence` | Distinguish aggregate candidate support from evidence-specific support | aggregate support basis + per-evidence chain audit | Executable |
| `EA02_no_relation_audit` | Audit no-established relation on available surfaces | mechanism applicability + no affirmative relation | Executable |
| `EA03_unresolved_audit` | Audit unresolved where prerequisites missing | missing candidate/evidence prerequisite | Executable |
| `EA04_opposition_unavailable` | Audit opposition unavailable boundary | no affirmative conflict basis | Executable as unavailable finding |
| `EA05_duplicate_linkage` | Audit direct duplicate linkage without derivation claim | `duplicate_of_evidence_id` + narrow dependency basis | Executable |
| `EA06_dependency_unknown` | Audit residual Unknown dependency | no affirmative lineage/independence basis | Executable |
| `EA07_provenance_preservation` | Audit provenance retention through correspondence record | provenance surfaces retained | Executable |
| `EA08_multi_candidate_audit` | Audit per-candidate chain status separation | different outcomes across candidates | Executable |

## Evidence output contract per case

Per case, capture:

- case ID
- input configuration
- aggregate candidate-support status
- aggregate-support basis
- evidence ID
- candidate ID/reference
- candidate(s)
- available evidence/provenance
- correspondence state (`supporting` / `no_established_relation` / `unresolved`)
- correspondence basis or missing-basis explanation
- evidence->cue/property attachment status + basis
- cue/property->candidate correspondence status + basis
- complete-chain audit label
- exact missing link when chain incomplete
- opposition status and missing-basis explanation
- lineage ID only if affirmatively justified
- lineage basis
- duplicate_of_evidence_id / duplicate_basis_reference (for direct repetition only)
- derivation edge only if affirmatively justified by explicit derivation fact
- dependency state
- dependency basis
- independence status
- provenance fields
- Unknown/Unresolved/Unavailable reason
- family/dependency fields
- artifact identity
- unavailable quantities
- replay status
- stop/anomaly status

## Plan freeze and execution discipline

This plan is frozen before formal evidence generation.  
Execute only cases whose required quantities are A/B/C under the contract gate.  
For D-class requirements, keep cases explicitly `UNAVAILABLE`.
