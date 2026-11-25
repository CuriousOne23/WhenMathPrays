# S2M IdOB Traversal Correspondence Representability Plan

**Date:** 2026-11-25  
**Status:** Draft/frozen follow-on plan; not executed in this pass.  
**Contract authority:** [s2m_idob_traversal_correspondence_contract.md](s2m_idob_traversal_correspondence_contract.md).  
**Purpose:** Test representability of correspondence/provenance/dependency surfaces only.

## Scope

In scope:

- representability of support/no-established-relation records;
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

If explicit opposition, family identity, or dependency typing requires creating new semantics/mechanisms, mark affected cases `UNAVAILABLE` and stop at boundary report.

## Planned representability cases

| Case ID | Goal | Required state | Current status |
|---|---|---|---|
| `CR01_support_record` | Record explicit support correspondence for candidate pair | evidence_id, candidate_id, supporting state, provenance | Ready if observability record exists |
| `CR02_no_relation_record` | Record no-established-relation without opposition inference | evidence_id, candidate_id, no-established-relation state | Ready if observability record exists |
| `CR03_opposition_record` | Record explicit opposition only when explicit opposing relation exists | opposing relation basis | **UNAVAILABLE unless explicit opposing relation is represented** |
| `CR04_repeated_observation` | Verify repeated observation does not auto-create independent families | duplicate link + dependency class not auto-independent | Ready for boundary check |
| `CR05_known_shared_family` | Verify shared family can be represented when known | family_id + Dependent | **UNAVAILABLE unless family identity exists** |
| `CR06_known_independent_families` | Verify independent families can be represented when justified | family_id + Independent | **UNAVAILABLE unless independence basis exists** |
| `CR07_unknown_dependency` | Preserve Unknown when dependency not established | dependency class = Unknown | Ready if class field exists |
| `CR08_multi_candidate_targeting` | Preserve distinct candidate addressing by evidence | evidence-to-multiple-candidate records | Ready if record surface exists |

## Evidence output contract per case

Per case, capture:

- case ID
- input configuration
- emitted correspondence records (if any)
- provenance fields
- family/dependency fields
- unavailable quantities
- stop/anomaly status
- replay status for unchanged semantic controls

## Execution status

Not executed in this pass.  
Await human review/authorization on whether category-3 observability surfaces are acceptable as behaviorally inert and whether any category-4 gaps should remain unresolved.
