# pipelines

Stage-named lineup directories. Not Path-A-branded lists.

Each stage:

```
<stage>/
    pipeline.yaml
    fixtures/
    tests/
    README.md
```

First stage: `lineup_idob_mcb`.
Next stages are earned by a successful freeze on the previous stage.

## Verbose runner mode

The lineup runner supports an observational debug flag:

```bash
python run_pipeline.py lineup_idob_mcb --verbose
```

When `--verbose` is enabled, the runner prints:

- per-primitive fields read (present read-set)
- per-primitive fields written
- contents of each written field
- per-primitive summary blocks with read count, write count, written paths, and mutated paths
- a final summary with total fields read/written, write-wall violations, and replay determinism hints

How this helps debugging:

- makes field-level TP transitions visible at each tick
- helps validate write-wall safety around protected paths
- helps explain why a lineup freeze changed between runs

`--verbose` is purely observational. It does not alter TP contents, legality behavior, replay behavior, or primitive semantics.
