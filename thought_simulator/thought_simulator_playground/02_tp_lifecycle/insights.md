# Insights

## Run Record (Standard)

Use one row per execution attempt.

| Date | Module | Command | Inputs / Config | Result | Exit Code | Artifacts | HLR Ref | LLR Ref | Req Doc | Req Section | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-05-26 | 02_tp_lifecycle | python harness.py | deterministic_mode=True; scenario_set=creation,movement,entropy,tags,split,merge,provenance,monotonicity | PASS | 0 | tp_lifecycle_harness_artifact.json | HLR-ARCH-07, HLR-REQ-14 | LLR-T-OBS-01, LLR-T-LVL-02, LLR-T-DET-01, T-DET-04 | thought_simulator_req/10_architecture/07_TS_state_machine.md; thought_simulator_req/20_requirements/14_testing_and_validation.md | §3, §8, §14; §4 | All deterministic scenarios passed and requirement IDs were emitted during execution. |

## What worked well

- Pure macro import from prototype.py executed cleanly through harness.py as the sole entrypoint.
- Deterministic TP IDs were stable for identical seeded inputs.
- State counter monotonicity held across create, move, entropy update, tag, split, and merge events.
- Provenance and history were captured and serialized into the artifact.

## What felt awkward or missing

- HLR naming is currently document-oriented (HLR-ARCH-07, HLR-REQ-14) rather than a centralized formal ID registry.
- Provenance records currently log creation note as seed before split/merge provenance override; behavior is valid but could be made semantically cleaner.

## Determinism Evidence Snapshot

Two additional deterministic reruns were executed and archived:

- tp_lifecycle_harness_artifact_run2.json
- tp_lifecycle_harness_artifact_run3.json

| Evidence Field | Run2 | Run3 | Match |
|---|---|---|---|
| result | PASS | PASS | YES |
| seed_tp_id | 6c1062c3-e03b-5e24-98c0-9af169cda865 | 6c1062c3-e03b-5e24-98c0-9af169cda865 | YES |
| seed_state_counter | 6 | 6 | YES |
| merged_tp_id | 6c756eaf-a928-5fe4-9b25-c6a8e159e47b | 6c756eaf-a928-5fe4-9b25-c6a8e159e47b | YES |
| merged_state_counter | 2 | 2 | YES |

Conclusion: deterministic identity and key lifecycle counters remained stable across consecutive reruns.

## Open questions for next iteration

- HLR/LLR naming normalization has now been defined globally in thought_simulator_req/20_requirements/24_traceability_matrix.md (Version 0.7). Next step is adoption across other modules.
- Do we want a stricter invariant that merged TP creation history note is merge at initial creation event?
