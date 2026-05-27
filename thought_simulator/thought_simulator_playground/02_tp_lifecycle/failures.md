# Failures

## Run status

| Timestamp | Command | Status | Detail |
|---|---|---|---|
| 2026-05-26 | c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe harness.py | FAIL | Environment dependency failure: ModuleNotFoundError: No module named numpy. |
| 2026-05-26 | python harness.py | PASS | Deterministic verification suite completed. 3/3 scenarios passed. Artifact generated: tp_lifecycle_harness_artifact.json. |
| 2026-05-26 | c:/Users/jeffg/Documents/GitHub/WhenMathPrays/.venv/Scripts/python.exe harness.py | PASS | After installing numpy in active venv, deterministic reruns succeeded and reproducibility evidence artifacts were generated. |

## Failed Attempts

- One failed attempt due to missing numpy in the selected venv; resolved by installing numpy and rerunning.

## Invalidated Assumptions

- None in this run.

## Lessons Learned

- Requirement IDs must be printed during harness execution to keep test-to-requirement attachment explicit.
- Deterministic mode should include deterministic TP identity generation, not only deterministic state transitions.

## Failure Taxonomy

Use this taxonomy whenever a failure is recorded so recurring issues can be categorized and prevented.

| Category | Typical Trigger | Detection Point | Containment | Corrective Action |
|---|---|---|---|---|
| Environment Dependency | Missing package/interpreter mismatch | harness startup/import | stop run, log missing dependency | install/lock dependency; record environment baseline |
| Determinism Drift | non-reproducible IDs/counters/artifacts | rerun comparison | block promotion | fix deterministic inputs/state transitions; add regression check |
| API Contract Violation | invalid type/range/shape input | function validation/assertion | reject input, preserve prior state | tighten preconditions and caller validation |
| Provenance Integrity | parent/merge lineage mismatch | provenance assertion or artifact review | halt traceability sign-off | repair lineage construction and add invariant test |
| Serialization Compatibility | non-JSON-safe or schema-breaking output | artifact write/load phase | mark output incompatible | version schema and implement migration/backward compatibility |
| Requirement Attachment Gap | missing HLR/LLR or unmapped test | run record / ledger review | block verification closure | map requirement or record HLR-?/LLR-? and propose update |
