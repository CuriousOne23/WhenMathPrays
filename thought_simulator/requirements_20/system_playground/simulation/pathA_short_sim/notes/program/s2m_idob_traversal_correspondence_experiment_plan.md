# S2M IdOB Traversal Correspondence Representability Plan

**Date:** 2026-11-25  
**Status:** Frozen bounded plan for correspondence/lineage representability.  
**Contract authority:** [s2m_idob_traversal_correspondence_contract.md](s2m_idob_traversal_correspondence_contract.md).  
**Purpose:** Test representability of correspondence/provenance/dependency surfaces only.

## Local-utility success criterion

This experiment is successful if it either:

1. turns a currently ambiguous distinction into an inspectable represented state; or
2. narrows and clarifies an Unknown/Unresolved/Unavailable boundary without fabrication.

## Scope

In scope:

- representability of support/no-established-relation/unresolved correspondence records;
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

## Planned representability cases (frozen)

| Case ID | Goal | Required state | Current representability expectation |
|---|---|---|---|
| `CR01_support_record` | Affirmative support | evidence_id, candidate_id, supporting, basis, provenance | Executable |
| `CR02_no_relation_record` | No established correspondence | no-established-relation without opposition inference | Executable |
| `CR03_unresolved_record` | Unresolved correspondence | unresolved + prerequisite-missing reason | Executable |
| `CR04_opposition_unavailable` | Opposition unavailable boundary | explicit conflict basis absent | Executable as unavailable finding |
| `CR05_repeated_observation` | Direct repeated observation visibility | repeated evidence observations preserved | Executable |
| `CR06_duplicate_dependency` | Narrow duplicate-derived dependency | `Dependent` with duplicate linkage basis | Executable (narrow/local only) |
| `CR07_generic_dependency_unavailable` | Generic dependency unavailable without lineage basis | no affirmative lineage/derivation fact | Executable as unavailable finding |
| `CR08_independence_unavailable` | Affirmative independence unavailable | missing affirmative independence basis | Executable as unavailable finding |
| `CR09_unknown_dependency` | Residual Unknown dependency | Unknown + explicit reason | Executable |
| `CR10_provenance_preservation` | Provenance retention | provenance fields retained into record | Executable |
| `CR11_multi_candidate` | Multi-candidate correspondence separation | distinguishable candidate outcomes | Executable |
| `CR12_lineage_derivation_surface` | Lineage/derivation fields only when justified | lineage/derivation null-or-filled with basis | Executable |

## Evidence output contract per case

Per case, capture:

- case ID
- input configuration
- evidence ID
- candidate ID/reference
- candidate(s)
- available evidence/provenance
- correspondence state (`supporting` / `no_established_relation` / `unresolved`)
- correspondence basis or missing-basis explanation
- opposition status and missing-basis explanation
- lineage ID only if affirmatively justified
- lineage basis
- derivation edge only if affirmatively justified
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
