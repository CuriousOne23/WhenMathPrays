# Pipeline testing doctrine

A pipeline test exercises the **machine layer**: one lineup yaml, one fixture TP,
the kernel walking more than one primitive.

It is not a primitive testbench. Primitive benches stay under `testbenches/`
and are launched by `run.py`.

## Present test types (real now)

### Legality

A legality test asserts only:

1. Every name in `pipeline.yaml` resolves through `ts_kernel.registry.load`.
2. `get_primitive_name()` (or `PRIMITIVE_NAME`) equals the yaml key.
3. Module-level `process(tp, mode="general", **kwargs)` is callable.
4. Unknown names, name/folder mismatches, and stub modules fail legality.
5. The kernel walks names in yaml order. No implicit insert or skip.

A legality test does **not** assert meaning, ΔH, `next_context`, or
"MCB understood IdOB."

Allowed-order on the first landing is: the list in this stage's `pipeline.yaml`.
Broader Path A lineup tables are not encoded here until a second stage exists
to disagree with.

File convention: `pipelines/<stage>/tests/test_legality.yaml`.

### Replay

A replay test asserts only:

1. Same stage, same fixture, two `run_pipeline` calls.
2. `freeze(final_tp)` is identical across those two runs.

Freeze is a canonical dump of the TP the kernel returned — not a curated
meaning view. If IdOB→MCB leaves MCB's read-set empty, replay can still pass.
That pass is honest.

File convention: `pipelines/<stage>/tests/test_replay.yaml`.

## Future test types (named, not real)

Do not implement these files until the first freeze exists and the stage README
says what they would measure:

- `test_tp_flow.yaml` — field presence across hops
- `test_write_walls.yaml` — hard-fail on canary mutation (today: observe only)
- `test_freeze_commit.yaml` — commit semantics once the kernel owns freeze/commit
- `test_modes.yaml` — isolation / exploration / debug once modes exist

## Fixture rule

A fixture must carry:

- input the first primitive actually reads (for IdOB: `utterance` and/or `card_id`)
- the next primitive's read-set if emptiness would be a fixture bug rather than a finding

Wall canaries (`process.routing_filter`, `metadata.geometric_state`,
`metadata.clarifying`) belong on the fixture so mutation is visible.
