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
- dependency-state representability (`Independent/Dependent/Unknown`) where legitimately derivable.

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

## Planned representability cases

| Case ID | Goal | Required state | Current representability expectation |
|---|---|---|---|
| `CR01_support_record` | Record explicit supporting correspondence where affirmative basis exists | evidence_id, candidate_id, supporting state, basis, provenance | Executable when category cue membership + candidate relation are represented |
| `CR02_no_relation_record` | Record no-established-relation without opposition inference | evidence_id, candidate_id, no-established-relation state | Executable where candidate is present but no positive correspondence basis is represented |
| `CR03_opposition_record` | Record explicit opposition only with positive opposing basis | opposing basis fact | **UNAVAILABLE unless explicit opposing relation is represented** |
| `CR04_unresolved_correspondence` | Preserve unresolved when correspondence cannot legitimately be determined | unresolved state + reason | Executable where required candidate/evidence surface is unavailable |
| `CR05_repeated_observation` | Preserve duplicate/repeat visibility | duplicate linkage, no auto-independence | Executable |
| `CR06_affirmative_dependency` | Preserve dependent only with positive basis | Dependent + dependency basis | Limited execution only for explicit duplicate linkage; lineage-level dependency otherwise unavailable |
| `CR07_affirmative_independence` | Preserve independent only with positive basis | Independent + basis | **UNAVAILABLE unless affirmative independence basis exists** |
| `CR08_unknown_dependency` | Preserve Unknown when dependence/independence not established | Unknown + reason | Executable |
| `CR09_provenance_preservation` | Preserve provenance through correspondence record | provenance fields retained | Executable |
| `CR10_multi_candidate_targeting` | Distinguish candidate-specific correspondence outcomes | evidence-candidate records across multiple candidates | Executable on surrogate candidate surface |

## Evidence output contract per case

Per case, capture:

- case ID
- input configuration
- candidate(s)
- available evidence/provenance
- correspondence state
- correspondence basis (if available)
- lineage information (if available)
- dependency state
- dependency basis (if available)
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
