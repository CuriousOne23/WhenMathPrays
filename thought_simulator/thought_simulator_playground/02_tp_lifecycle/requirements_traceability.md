# Requirements Traceability

## Module

- Module name: 02_tp_lifecycle
- Scope: ThoughtPoint lifecycle macro behavior (creation, basin movement, entropy update, tag operations, split/merge, provenance, state_counter determinism)

## Source Requirements

- thought_simulator_req/10_architecture/07_TS_state_machine.md
- thought_simulator_req/10_architecture/08_TS_data_model.md
- thought_simulator_req/20_requirements/14_testing_and_validation.md

| HLR Ref | Description | Source Doc | Section |
|---|---|---|---|
| HLR-ARCH-07 | Deterministic TP lifecycle transitions and traceable state updates | thought_simulator_req/10_architecture/07_TS_state_machine.md | §3, §8, §13, §14 |
| HLR-ARCH-08 | TP data model with lifecycle metadata and observability fields | thought_simulator_req/10_architecture/08_TS_data_model.md | §3.1, §6 |
| HLR-REQ-14 | Deterministic and reproducible verification requirements | thought_simulator_req/20_requirements/14_testing_and_validation.md | §4, §7, §12 |

| LLR Ref | Description | Source Doc | Section |
|---|---|---|---|
| LLR-T-LVL-02 | Integration-level lifecycle interactions (split/merge/provenance) | thought_simulator_req/20_requirements/14_testing_and_validation.md | §3 |
| LLR-T-OBS-01 | State/log completeness and monotonic counter observability | thought_simulator_req/20_requirements/14_testing_and_validation.md | §7 |
| LLR-T-DET-01 | Bitwise reproducibility under same deterministic inputs | thought_simulator_req/20_requirements/14_testing_and_validation.md | §4 |
| LLR-T-DET-04 | State counter drift detection across deterministic runs | thought_simulator_req/20_requirements/14_testing_and_validation.md | §4 |

## Design References

- software_description.md
- prototype.py public API and invariants
- harness.py scenario suite

## Current Impact Notes

- prototype.py now enforces deterministic TP ID generation when deterministic_mode=True.
- harness.py is now the sole executable entrypoint and emits HLR/LLR references at runtime.
- Evidence artifact tp_lifecycle_harness_artifact.json captures scenario-level verification details and TP snapshots.

## Test to Requirement Attachments

| Test Case | HLR Ref | LLR Ref | Req Doc | Req Section | Evidence / Artifacts | Verification Capsule Location |
|---|---|---|---|---|---|---|
| creation_movement_entropy | HLR-ARCH-07 | LLR-T-OBS-01 | thought_simulator_req/10_architecture/07_TS_state_machine.md | §3, §14 | harness output + tp_lifecycle_harness_artifact.json | verification_summary.md (Verification Ledger) |
| tags_split_merge_provenance | HLR-ARCH-07 | LLR-T-LVL-02 | thought_simulator_req/10_architecture/07_TS_state_machine.md | §8 | harness output + tp_lifecycle_harness_artifact.json | verification_summary.md (Verification Ledger) |
| determinism_and_monotonicity | HLR-REQ-14 | LLR-T-DET-01, T-DET-04 | thought_simulator_req/20_requirements/14_testing_and_validation.md | §4 | harness output + tp_lifecycle_harness_artifact.json | verification_summary.md (Verification Ledger) |

## Scenario to IO Field Mapping

| Scenario | Inbound Variables | Outbound Variables | Interoperability Notes |
|---|---|---|---|
| creation_movement_entropy | basin_id, entropy, embedding, created_at_tick, energy, deterministic_mode, deterministic_nonce, tick, d_rep, d_pred, d_struct | tp_id, current_basin_id, entropy, state_counter, history, last_updated_tick | Core lifecycle fields must serialize losslessly for external replay/checking tools. |
| tags_split_merge_provenance | tag, tick, child_count, sources, basin_id | tags, provenance.parent_ids, provenance.split_children, provenance.merge_sources, history, state_counter | Provenance IDs are canonical lineage keys and must remain unchanged across adapters. |
| determinism_and_monotonicity | deterministic_mode, deterministic_nonce, basin_id, entropy, embedding, created_at_tick | tp_id, state_counter, history | Determinism checks require byte-stable identity fields across reruns for identical inputs. |

## Open Traceability Questions

- HLR/LLR naming policy is now standardized in thought_simulator_req/20_requirements/24_traceability_matrix.md (v0.7); confirm rollout schedule for all playground modules.
- Should architecture documents introduce explicit machine-readable low-level IDs beyond section anchors?
