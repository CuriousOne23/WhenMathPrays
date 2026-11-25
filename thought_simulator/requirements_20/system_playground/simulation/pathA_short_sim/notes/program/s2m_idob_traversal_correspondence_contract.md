# S2M IdOB Traversal Correspondence Contract (Research Joint)

**Date:** 2026-11-25  
**Status:** Research/design contract for next bounded traversal joint. Non-normative.  
**Upstream context:** [s2m_idob_traversal_proposal.md](s2m_idob_traversal_proposal.md), [s2m_idob_traversal_program_reference.md](s2m_idob_traversal_program_reference.md), [s2m_idob_traversal_observation.md](s2m_idob_traversal_observation.md).  
**Purpose:** Define the minimum representational contract for:

1. evidence-to-candidate correspondence; and
2. evidence-family provenance/dependency preservation.

This document does **not** define full traversal, `D_t/Q_t` formulas, `B_t`, traversal `P_t/H_t`, or continue/OuBA sufficiency.

## Scope and anti-fabrication rules

Preserved invariants:

- missing correspondence != opposition
- missing evidence != contradiction
- mismatch != opposition
- structural legality != contextual support
- unknown dependency != independence
- repeated observation != automatically independent evidence

Explicit opposition is not permitted to be inferred from:

- absence of support;
- lexical negation alone;
- category mismatch;
- low score/probability;
- refusal/unselected state.

If no explicit opposing relation is represented, opposition remains unresolved.

## Contract A — Evidence-to-candidate correspondence

Minimum experimental correspondence record (conceptual schema):

```text
correspondence_record:
  evidence_id: string
  candidate_id: string
  candidate_reference_surface: enum{door_legal_candidate, current_surrogate_candidate}
  relation_basis_id: string|null
  correspondence_state: enum{supporting, opposing, no_established_relation, unresolved}
  provenance_ref: string
  notes: string|null
```

State intent:

- `supporting`: explicit represented relation establishes support.
- `opposing`: explicit represented relation establishes opposition.
- `no_established_relation`: evidence and candidate are both present, but no established relation is represented.
- `unresolved`: record cannot yet determine state from represented information.

`supporting/opposing/no_established_relation` are conceptual targets for `(+ / - / 0)` without requiring literal symbols in storage.

### Opposition boundary (current realization)

Current surfaces do not provide a generic explicit opposing relation primitive for traversal candidates.  
Therefore, proposal-level explicit opposition remains **unresolved** in current realization.

## Contract B — Evidence family / provenance / dependency

Minimum experimental evidence-family record:

```text
evidence_record:
  evidence_id: string
  provenance_source: string
  provenance_path: string|null
  candidate_id: string
  correspondence_state: enum{supporting, opposing, no_established_relation, unresolved}
  family_id: string|null
  family_id_status: enum{established, unknown}
  dependency_class: enum{Independent, Dependent, Unknown}
  dependency_basis_id: string|null
  duplicate_of_evidence_id: string|null
```

Dependency class intent:

- `Independent`: established as not sharing decisive provenance/dependency basis with other counted evidence.
- `Dependent`: established as sharing a dependency basis with other evidence.
- `Unknown`: dependency relation not established.

No weighting or scoring consequences are defined in this contract.

## D_t / Q_t boundary (non-formula)

This contract only defines what would be required later for reconstructability:

- directional tuple-like reconstruction would require correspondence records showing which candidate-addressed evidence is supporting/opposing;
- qualifier tuple-like reconstruction would require explicit dependency-state and conflict-state observability.

This contract does not define aggregation formulas, thresholds, or weighting.

## Implementation-decision gate classification

Classification levels:

1. **ALREADY AVAILABLE**
2. **DERIVABLE WITHOUT SEMANTIC CHANGE**
3. **REQUIRES BEHAVIORALLY INERT OBSERVABILITY**
4. **REQUIRES NEW ARCHITECTURE / RESEARCH DECISION**

| Required field/state | Classification | Current basis / reason |
|---|---|---|
| bounded structural seed relation surface (`s2m_seed.written_relations`) | 1 | Present in [idob/experimental_seed.py](../../idob/experimental_seed.py). |
| finite surrogate candidates (`s2m_meaning.candidate_interpretations`) | 1 | Present in [s2m/propose.py](../../s2m/propose.py), [s2m/loop.py](../../s2m/loop.py). |
| cue provenance buckets (`sentence`, `prior_context_cex`) | 1 | Present in `CE/CEx/ISc` outputs in [primitives_pathA_short.py](../../primitives_pathA_short.py). |
| candidate state outcomes (`candidate_unselected`, `category_supported`, `legitimized`, `refused`) | 1 | Present in [s2m/loop.py](../../s2m/loop.py). |
| deterministic category-scoring distribution surface (`category_weighted_distribution`) | 1 | Present in [primitives_pathA_short.py](../../primitives_pathA_short.py). |
| stable evidence identifier (`evidence_id`) | 2 | Derivable from existing trace context if deterministic identity convention is defined without changing semantics. |
| candidate identifier normalization for surrogate candidates | 2 | Derivable from existing candidate tuple fields (`from`, `relation`, `to`, `major`). |
| explicit correspondence record object (support/opposition/no-relation/unresolved per evidence-candidate pair) | 3 | Requires new observability emission surface but can be behaviorally inert if read-only/derived. |
| `family_id` and `family_id_status` surfaces | 3 | Requires explicit observability fields; currently absent. |
| explicit dependency classification field (`Independent/Dependent/Unknown`) | 3 | Needs emitted classification result surface if derived from existing evidence links only. |
| door-legal candidate identity (`structural_key -> meaning_group_candidates`) | 4 | Not realized in current traversal surfaces. |
| explicit opposing relation primitive for traversal correspondence | 4 | Not represented in generic traversal mechanism today. |
| architecture-grounded evidence-family identity mechanism | 4 | Not currently defined; cannot be assumed from container/source alone. |
| proposal-level `D_t`, `Q_t` computation | 4 | Requires architecture decisions beyond representability. |
| traversal `B_t`, traversal-candidate `P_t`, traversal `H_t`, continue/OuBA sufficiency | 4 | Out of scope and unresolved by design. |

## Boundary discipline

If a required state must be *created* (not merely exposed from existing semantics), it is not observability-only instrumentation and must be treated as architecture/research scope.
