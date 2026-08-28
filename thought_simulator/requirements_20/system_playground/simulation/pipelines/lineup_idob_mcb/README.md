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
