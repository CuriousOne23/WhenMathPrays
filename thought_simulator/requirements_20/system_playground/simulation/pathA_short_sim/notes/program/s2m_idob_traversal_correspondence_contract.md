# S2M IdOB Traversal Correspondence Contract (Research Joint)

**Date:** 2026-11-25  
**Status:** Research/design contract for next bounded traversal joint. Non-normative.  
**Upstream context:** [s2m_idob_traversal_proposal.md](s2m_idob_traversal_proposal.md), [s2m_idob_traversal_program_reference.md](s2m_idob_traversal_program_reference.md), [s2m_idob_traversal_observation.md](s2m_idob_traversal_observation.md).  
**Purpose:** Define the minimum representational contract for:

1. evidence-to-candidate correspondence; and
2. evidence-family provenance/dependency preservation.

This document does **not** define full traversal, `D_t/Q_t` formulas, `B_t`, traversal `P_t/H_t`, or continue/OuBA sufficiency.

## Local-utility success criterion

This bounded characterization is successful if it makes at least one currently ambiguous distinction mechanically inspectable, and/or makes a remaining Unknown/Unresolved/Unavailable boundary explicit and bounded without fabrication.  
Global validity is out of scope.

## Scope and anti-fabrication rules

Preserved invariants:

- missing correspondence != opposition
- missing evidence != contradiction
- mismatch != opposition
- structural legality != contextual support
- unknown dependency != independence
- repeated observation != automatically independent evidence
- absence of support != opposition

Explicit opposition is not permitted to be inferred from:

- absence of support;
- lexical negation alone;
- category mismatch;
- low score/probability;
- refusal/unselected state.

If the current realization lacks an explicit opposing-relation mechanism or affirmative conflict basis, opposition is unavailable; unresolved is reserved for cases where an applicable representation/evaluation mechanism exists but cannot yet complete.

## Contract A — Evidence-to-candidate correspondence

Minimum experimental correspondence record (conceptual schema):

```text
correspondence_record:
  evidence_id: string
  candidate_id: string
  candidate_reference_surface: enum{door_legal_candidate, current_surrogate_candidate}
  relation_basis_id: string|null
  relation_basis_fact: string|null
  correspondence_state: enum{supporting, opposing, no_established_relation, unresolved}
  provenance_ref: string
  notes: string|null
```

Critical distinction:

- **aggregate candidate support** is a candidate-level fact on cue/candidate surfaces;
- **evidence-specific support correspondence** is an evidence-to-candidate fact requiring a complete affirmative chain for a particular evidence observation.

Minimum conceptual evidence-specific chain:

`evidence_observation -> evidence_property_or_cue -> candidate_property_correspondence -> candidate`

Every link requires affirmative represented basis.

State intent:

- `supporting`: explicit represented relation establishes affirmative support.
- `opposing`: explicit represented relation establishes affirmative opposition (never residual).
- `no_established_relation`: correspondence evaluation is applicable/available for the pair, and no relation has been established.
- `unresolved`: required evidence/candidate properties are unresolved/unavailable, or correspondence evaluation has not legitimately occurred.

`supporting/opposing/no_established_relation` are conceptual targets for `(+ / - / 0)` without requiring literal symbols in storage.

Evidence-specific boundary:

- candidate cue membership, candidate selection state, category result, or aggregate cue set alone do not establish `supporting(evidence_id, candidate_id)`;
- if evidence->cue/property attachment is not represented, evidence-specific support is `UNAVAILABLE`, not `no_established_relation`.

### Opposition boundary (current realization)

Current surfaces do not provide a generic explicit opposing relation primitive for traversal candidates.  
Therefore, proposal-level explicit opposition remains **unresolved** in current realization.

Minimum conceptual target for explicit opposition correspondence:

```text
opposition_correspondence:
  evidence_id: string
  candidate_id: string
  property_of_evidence: string
  property_of_candidate: string
  basis_reference: string
```

In current realization, explicit opposition remains:

`UNAVAILABLE_NO_AFFIRMATIVE_CONFLICT_BASIS`

unless an already represented affirmative conflict fact exists.

## Contract B — Evidence family as information lineage + dependency

Minimum conceptual lineage/dependency record:

```text
evidence_observation:
  evidence_id: string
  lineage_id: string|null
  lineage_basis_reference: string|null
  derivation_edge: string|null
  derivation_basis_reference: string|null
  dependency_state: enum{Dependent, Unknown}
  dependency_basis_reference: string|null
```

Evidence-family identity in this contract means information lineage required to determine whether multiple observations are distinct evidence or repeated/derived manifestations of the same underlying evidence.

An originating source label may contribute to lineage representation but is not sufficient by itself.

Dependency class intent:

- `Dependent`: positive represented information establishes shared lineage/derivation/dependency.
- `Unknown`: neither dependence nor independence is positively established.

No weighting or scoring consequences are defined in this contract.

`Independent` remains out of scope for this realization pass and unavailable without an affirmative independence condition.

Independence must not be inferred from:

- missing dependency edge;
- different runtime containers/fields;
- different provenance labels alone;
- different immediate source IDs alone.

Duplicate linkage boundary:

- Direct repeated identical input observations may support a narrow local dependency fact when duplicate identity is mechanically inspectable.
- This is recorded narrowly as `PARTIAL_DUPLICATE_LINK_ONLY`.
- Duplicate linkage is not a generic lineage architecture.
- Direct duplicate linkage does not populate `derivation_edge` by itself.

## Engineering representability framing

For each concept:

1. concept;
2. represented fact that instantiates it;
3. observable TS surface;
4. Unknown/Unresolved/Unavailable boundary reason;
5. implementation class A/B/C/D.

Where a state must be created (not exposed/derived), classify as **D**.

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
| stable evidence identifier (`evidence_id`) | 2 | Mechanically derivable from run/case + evidence slot without semantic change. |
| candidate identifier normalization for surrogate candidates | 2 | Derivable from existing candidate tuple fields (`from`, `relation`, `to`, `major`). |
| explicit correspondence record object (support/opposition/no-relation/unresolved per evidence-candidate pair) | 3 | Requires read-only derived observability emission if generated from existing facts only. |
| aggregate candidate support status (candidate-level) | 1 | Present on existing cue/candidate/selection surfaces. |
| evidence-specific support chain reconstruction | 2 / 4 | Derivable only where evidence->cue attachment and cue/property->candidate correspondence are explicitly represented; otherwise unavailable. |
| evidence->cue/property attachment per evidence observation | 2 / 4 | Uniquely reconstructible in narrow single-source/single-observation conditions, but reconstruction is not an explicit represented attachment; generally unavailable without an explicit attachment fact.|
| cue/property->candidate correspondence basis | 1 / 2 | Aggregate candidate-level basis is available/derivable; evidence-specific basis depends on evidence attachment. |
| unresolved correspondence state surface | 2 | Derivable when candidate/evidence prerequisites are missing or evaluation not applicable. |
| direct duplicate linkage (`duplicate_of_evidence_id` for repeated identical input observation) | 2 | Derivable from repeated identical input observation in the same case configuration. |
| narrow duplicate-derived dependency state (`Dependent`) | 2 | Derivable only for mechanically inspectable duplicates; record as `PARTIAL_DUPLICATE_LINK_ONLY`. |
| residual dependency state (`Unknown`) | 2 | Derivable when no affirmative dependency fact exists. |
| `lineage_id` assignment beyond duplicate linkage | 4 | Requires architecture/research definition of lineage representation and assignment rule. |
| affirmative independence state | 4 | Requires explicit affirmative independence condition not currently represented. |
| door-legal candidate identity (`structural_key -> meaning_group_candidates`) | 4 | Not realized in current traversal surfaces. |
| explicit opposing relation primitive for traversal correspondence | 4 | Not represented in generic traversal mechanism today. |
| architecture-grounded evidence-family identity mechanism | 4 | Not currently defined; cannot be assumed from container/source alone. |
| proposal-level `D_t`, `Q_t` computation | 4 | Requires architecture decisions beyond representability. |
| traversal `B_t`, traversal-candidate `P_t`, traversal `H_t`, continue/OuBA sufficiency | 4 | Out of scope and unresolved by design. |

## Boundary discipline

If a required state must be *created* (not merely exposed from existing semantics), it is not observability-only instrumentation and must be treated as architecture/research scope.
