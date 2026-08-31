# Status: lineup_idob_mcb

## 1. Implemented Functionality

Current implementation snapshot:

- [thought_simulator/requirements_20/system_playground/primitives/idob/idob.py](thought_simulator/requirements_20/system_playground/primitives/idob/idob.py)
  - Produces an IdOB hop packet under tp.idob from utterance or card path.
  - Supports six-ID assignment flow, structural key generation, candidate map lookup, ranking, meaning birth, CIE modulation, and deterministic-style delta calculations.
  - Writes tp.idob fields including assignment status, candidate/rank/selection fields, meaning_semantics, meaning_semantics_prime, meaning_delta_h, meaning_cie_delta, resolution and eligibility flags.
  - Writes semantic.meaning_delta_h.
  - Writes root flags idob_complete, path_b_eligible, ready_for_ouba.
  - Preserves process.routing_filter by restoring pre-hop value and sets packet diagnostic routing_filter_mutated when mutation is detected.

- [thought_simulator/requirements_20/system_playground/primitives/mcb/mcb.py](thought_simulator/requirements_20/system_playground/primitives/mcb/mcb.py)
  - Performs first-order meaning-clarifying reconciliation using extracted meaning and clarifying views.
  - Computes semantic.mcb_delta_h and semantic.mcb_semantics.
  - Computes semantic.mcb_context_coherence and semantic.mcb_context_shift_required.
  - Appends lightweight cues into semantic.meaning_semantics when reinforcement/conflict is detected.
  - Writes next_context block at TP root with topic, stance, intent, register, politeness, epistemic_shading, continuity, direction, coherence, shift_required, importance.
  - Writes mcb_complete and mcb_next_ob_candidates.
  - Writes tpu.mcb_update payload.
  - Includes diagnostic write-wall checks for process.routing_filter, metadata.geometric_state, and current-turn clarifying block.

- [thought_simulator/requirements_20/system_playground/simulation/pipelines/lineup_idob_mcb/fixtures/fx_idob_mcb_01.yaml](thought_simulator/requirements_20/system_playground/simulation/pipelines/lineup_idob_mcb/fixtures/fx_idob_mcb_01.yaml)
  - Seeds utterance.
  - Seeds semantic.identity and metadata.identity.
  - Seeds metadata stance, direction, importance, context, and clarifying blocks.
  - Seeds write-wall canaries for metadata.geometric_state and process.routing_filter.
  - Declares expected observations (non-assertive) for meaning delta presence, read behavior, and write-wall invariance.

- [thought_simulator/requirements_20/system_playground/simulation/pipelines/lineup_idob_mcb/pipeline.yaml](thought_simulator/requirements_20/system_playground/simulation/pipelines/lineup_idob_mcb/pipeline.yaml)
  - Defines lineup stage lineup_idob_mcb.
  - Defines ordered primitive sequence: idob then mcb.

- [thought_simulator/requirements_20/system_playground/simulation/pipelines/lineup_idob_mcb/tests/test_legality.yaml](thought_simulator/requirements_20/system_playground/simulation/pipelines/lineup_idob_mcb/tests/test_legality.yaml)
  - Verifies name resolution for idob and mcb.
  - Verifies refusal of invalid names including unknown_name, cex, RB_reader, IdOB.
  - Verifies order_is_yaml.
  - Keeps no_meaning_assertions true.

- [thought_simulator/requirements_20/system_playground/simulation/pipelines/lineup_idob_mcb/tests/test_replay.yaml](thought_simulator/requirements_20/system_playground/simulation/pipelines/lineup_idob_mcb/tests/test_replay.yaml)
  - Runs replay for the lineup fixture.
  - Requires identical_freeze true.
  - Keeps no_meaning_assertions true.

## 2. Required Minimal Functionality (To Be Implemented)

### IdOB must write:
- tp.idob (minimal packet)
- semantic.meaning_delta_h (minimal deterministic delta)

### IdOB must read:
- semantic.identity
- semantic.stance
- semantic.clarifying
- semantic.semantic_core
- metadata.identity_metadata
- metadata.clarifying_metadata
- metadata.semantic_layer_metadata
- metadata.expressive_metadata
- metadata.normalization_metadata

### MCB must write:
- semantic.clarifying_out (minimal)
- next_context_metadata.* (minimal)

### MCB must read:
- tp.idob (read-only)
- semantic.identity
- semantic.stance
- semantic.clarifying
- semantic.semantic_core
- metadata.identity_metadata
- metadata.clarifying_metadata

### Fixture must seed:
- identity metadata
- stance metadata
- clarifying metadata
- semantic_core
- expressive metadata
- normalization metadata
- write-wall canaries
- utterance

## 3. Write-Wall and Separation Constraints

Fields that MUST NOT be written in this lineup:

- metadata.clarifying
- metadata.geometric_state
- process.routing_filter
- tp.idob (MCB must not write)
- semantic.meaning_delta_h (MCB must not write)

Separation rules relevant to lineup_idob_mcb:

- meaning delta fields and entropy delta fields are distinct and must not be conflated.
- CIE and next-turn stance are distinct slots and must not be treated as interchangeable.
- CIE and MSL stance are distinct and must not be treated as interchangeable.
- tp.idob is a crossing packet and is distinct from identity lifecycle exports and COB snapshot structures.
- six structural IDs and structural_key are distinct from six meaning-axis values.
- residue_code and expand_target are hints and not routing authority for a next six-tuple.
- IdOB owns tp.idob and crossing meaning delta for the hop; MCB is read-only on those fields.

## 4. Verification Requirements

The following must pass:

- [thought_simulator/requirements_20/system_playground/simulation/pipelines/lineup_idob_mcb/tests/test_legality.yaml](thought_simulator/requirements_20/system_playground/simulation/pipelines/lineup_idob_mcb/tests/test_legality.yaml)
- [thought_simulator/requirements_20/system_playground/simulation/pipelines/lineup_idob_mcb/tests/test_replay.yaml](thought_simulator/requirements_20/system_playground/simulation/pipelines/lineup_idob_mcb/tests/test_replay.yaml)

Verification expectations for this lineup:

- Replay must be deterministic.
- Write-walls must not be violated.
- Primitive resolution and declared YAML order must remain valid.

## 5. Gap Analysis

Current gaps between required behavior and current implementation:

- Missing IdOB semantic alias fields:
  - IdOB currently writes semantic.meaning_delta_h and tp.idob, but does not currently materialize the expected IdOB alias arrays for this lineup status target.

- Missing MCB read of tp.idob:
  - MCB currently derives meaning/clarifying views from semantic and metadata blocks and does not explicitly consume tp.idob as a primary read input.

- Fixture missing full metadata set:
  - Fixture seeds identity/context/clarifying-style blocks and canaries, but does not seed the full required minimal set including semantic.semantic_core plus expressive and normalization metadata blocks.

- Naming mismatches:
  - Implementation writes tpu.mcb_update, while requirement language refers to TPU.mcb_update naming.

- Playground simplifications vs full TP catalog:
  - Lineup fixture and primitive shapes use simplified local field forms relative to the full canonical TP envelope catalog and naming separations.

## 6. Recommended Next Steps

- Implement minimal IdOB outputs.
- Implement minimal MCB outputs.
- Expand fixture to seed required fields.
- Ensure legality and replay pass.
- Do NOT implement full TP catalog at this stage.
- After this lineup is stable, proceed to lineup_mcb_rbu.
