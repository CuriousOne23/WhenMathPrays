# simulation — machine-level lineup execution

This directory is the machine-level simulation layer for Path A (and later Path B).
It sits above primitive-level testbenches.

It does **not** replace `testbenches/run.py`. It does **not** replace conversation traces.
It extends what already lives here into a kernel that can walk more than one primitive
on one Thought Packet (TP).

## Layers

| Layer | Entry | Owns |
| --- | --- | --- |
| Primitive | `testbenches/run.py` | One primitive, grouped primitive benches |
| Machine | `simulation/run_pipeline.py` | Lineup yaml, TP across primitives, walls, replay |
| Trace | `simulation/conversations/` | Human/AI conversation artifacts and convert programs |
| Context bench | `simulation/context/` | Existing context testbench (untouched by the kernel) |

Primitives are the same implementations used by `run.py`:

```
system_playground/primitives/<name>/<name>.py
```

Import root:

```
thought_simulator.requirements_20.system_playground.primitives.<name>
```

## Directory layout (going forward)

```
simulation/
    README.md                 this file
    run_pipeline.py           machine-level entry (fills the former stub)
    pipeline_testing.md       doctrine for pipeline tests
    ts_kernel/
        README.md
        registry.py           load(name) — the one new object
        kernel.py             tick + call order
        pipeline_runner.py    yaml + fixture → kernel
        legality.py           names must load; refuse stubs/unknowns
        replay.py             freeze(tp); two runs must match
    pipelines/
        lineup_idob_mcb/      first real stage (not "full Path A")
            pipeline.yaml
            fixtures/
            tests/
            README.md
    conversations/            existing traces — stay artifacts, not the machine
    context/                  existing context bench — stays where it is
```

There is no `path_a_full/` directory. Stages are named after the primitives they
actually contain. A new name is added only after the previous stage freezes.

## First machine: `lineup_idob_mcb`

Schedule:

```yaml
pipeline:
  - idob
  - mcb
```

Prove:

- registry resolves `idob` and `mcb`
- kernel order is the yaml
- same fixture, two runs, identical freeze

Observe (do not assert on the first landing):

- IdOB packet vs MCB read-set
- write-wall canaries (`process.routing_filter`, `metadata.clarifying`, `metadata.geometric_state`)

## How to run

From repo root, with the repo on `PYTHONPATH` (or via the path bootstrap in `run_pipeline.py`):

```
python thought_simulator/requirements_20/system_playground/simulation/run_pipeline.py lineup_idob_mcb
python thought_simulator/requirements_20/system_playground/simulation/run_pipeline.py lineup_idob_mcb --replay
python thought_simulator/requirements_20/system_playground/simulation/run_pipeline.py lineup_idob_mcb --legality
```

## What this directory is not

- Not a second copy of primitives.
- Not a replacement for `testbenches/run.py`.
- Not an eight-name (or thirty-five-name) Path A list.
- Not a place that absorbs `conversations/convert_pgms` as the orchestrator.

Those convert programs remain convert programs. The kernel may later read their YAML
as fixtures. It does not become them.

## Historical note

An earlier version of this README described `03_simulation` as a per-primitive
`path_a/01_InB/` … `35_OuBA/` tree and listed a long Path A sequence. That tree
was never present under this directory. The sequence remains aspirational doctrine
elsewhere (`progressive_lineup_testing.md`, glossary). Realization here is
stage-named lineups that grow from convicted primitives.
