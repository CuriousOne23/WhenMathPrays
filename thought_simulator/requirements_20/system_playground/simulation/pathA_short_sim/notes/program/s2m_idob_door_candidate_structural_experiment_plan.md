# S2M IdOB Door->Candidate Structural Experiment Plan

**Date:** 2026-11-25  
**Status:** Frozen bounded structural characterization plan.  
**Scope:** Structural extensibility only (`structural_key -> door -> C_t` seam).  
**Non-goals:** door legality, door semantics, structural_key definition, proposal-defined door implementation.

## Hypothesis

A future door-legal candidate producer can replace or wrap the current candidate producer at one local boundary while emitting the existing proposal-shaped candidate record contract, allowing downstream consumers to remain unchanged and producer-agnostic.

## Current boundary assumptions to test

1. Current candidate surface is an endpoint-association surrogate, not proposal-defined door-legal `C_t`.
2. Downstream path consumes candidate record shape, not producer origin.
3. Producer substitution at the candidate-production boundary should be characterizable via test-only injection.

## Test-only substitution method

1. Capture baseline candidate list from normal producer run.
2. For characterization cases, substitute test candidate list at producer boundary only.
3. Run existing downstream path unchanged.
4. Observe outputs and invariants.
5. Restore normal producer behavior for replay checks.

No production semantic code change is authorized.

## Frozen C1-C6 matrix

| Case | Description | Candidate input to downstream |
|---|---|---|
| `C1_BASELINE` | Normal producer | Normal propose output |
| `C2_REDUCED_SUBSET` | Proper subset of valid proposal-shaped records | Subset of baseline proposals |
| `C3_SINGLE_CANDIDATE` | Single valid proposal-shaped record | One baseline proposal |
| `C4_EMPTY_SET` | Empty candidate set | `[]` |
| `C5_REORDERED` | Reordered proposal list | Reversed baseline proposals |
| `C6_ORIGIN_NEUTRAL` | Test-only records independent of association loader origin | Fixture records with required current candidate shape, derived from baseline values |

## Candidate-interface audit requirements

Characterize which fields downstream consumers require:

- required: `from`, `relation`, `to`, `major`
- optional: `subcategory`
- downstream-added annotation: `selection_state`

Audit for dependencies on:

- association-file origin/path/metadata
- fixed cardinality
- ordering assumptions
- producer-specific metadata

## Structural-information preservation audit requirements

Characterize:

- whether `crossing_fields.structural_key` is null/unrealized in current seed surface;
- whether structural information needed for future key research appears available upstream/local to candidate seam;
- whether structural_key was generated then destroyed on this path.

## Pass/Failure labels

- `SAFE_TO_DEFER`
- `STOP_AND_REPAIR`
- `INSUFFICIENT_EVIDENCE`

`SAFE_TO_DEFER` requires evidence that substitution is local, downstream interfaces remain stable, and surrogate boundary remains explicit.

## Execution controls

After characterization:

1. restore normal producer behavior;
2. run:
   - `python support/tools/s2m_canonical_sentences_replay.py`
   - `python support/tools/s2m_category_selection_replay.py`
3. verify generated artifact remains ignored/untracked.
