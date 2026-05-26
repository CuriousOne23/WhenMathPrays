# Failures

## Run status

| Timestamp | Command | Status | Detail |
|---|---|---|---|
| 2026-05-26 | python harness.py | PASS | Deterministic verification suite completed. 3/3 scenarios passed. Artifact generated: tp_lifecycle_harness_artifact.json. |

## Failed Attempts

- No failed harness attempts in this iteration.

## Invalidated Assumptions

- None in this run.

## Lessons Learned

- Requirement IDs must be printed during harness execution to keep test-to-requirement attachment explicit.
- Deterministic mode should include deterministic TP identity generation, not only deterministic state transitions.
