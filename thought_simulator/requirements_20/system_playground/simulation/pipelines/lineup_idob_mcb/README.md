# lineup_idob_mcb

This is the first machine-level lineup. It is not "full Path A".

## Schedule

```yaml
pipeline:
  - idob
  - mcb
```

Both names already have a non-stub `primitives/<name>/<name>.py` and testbench mass.

## What this stage is meant to prove

Machine facts (must pass):

- registry resolves `idob` and `mcb`
- kernel order is the yaml
- same fixture, two runs, identical freeze

## What this stage is meant to show (observe, do not assert yet)

Contract facts:

- TP after IdOB is still a TP
- MCB can run without crashing on that TP
- write-wall canaries hold (`process.routing_filter`, `metadata.clarifying`, `metadata.geometric_state`)
- whether MCB reads `tp.idob` or only `metadata` / `semantic` seeded by the fixture

IdOB writes a structure-to-meaning packet under `tp["idob"]` plus
`semantic.meaning_delta_h`. MCB reads `metadata` / `semantic.identity` / stance /
clarifying. The fixture pre-seeds MCB's read-set so an empty view after the hop
is a contract finding, not a missing-fixture bug.

## Files

- `pipeline.yaml` — two names
- `fixtures/fx_idob_mcb_01.yaml` — utterance + MCB read-set + wall canaries
- `tests/test_legality.yaml` — resolve + refuse junk
- `tests/test_replay.yaml` — identical freeze

## Verbose mode

Use verbose runner output to inspect field-level behavior for each primitive:

```bash
python run_pipeline.py lineup_idob_mcb --verbose
```

Verbose mode prints:

- fields read by `idob` and `mcb`
- fields written by `idob` and `mcb`
- contents of each written field
- a summary block after each primitive:
  - number of fields read
  - number of fields written
  - written field paths
  - mutated fields
- a final pipeline summary:
  - total fields written
  - total fields read
  - write-wall violations (if any)
  - replay determinism hints

Why this helps:

- confirms write-wall canaries are stable
- shows exactly which TP paths move at each tick
- supports faster contract debugging for IdOB -> MCB handoff

Verbose mode is observational only and does not affect legality checks, replay checks, or primitive behavior.
