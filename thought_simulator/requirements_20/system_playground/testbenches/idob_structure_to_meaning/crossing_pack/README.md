# crossing_pack

Seed intake folder. Not the IdOB hop.

Law: 20.31.730 interface, 20.31.731 Seed schemas, 20.31.740 inquiry path.

How to run Stop 1 and Stop 2, what commands mean, and how to read output:
see [stopx_def_examples.md](stopx_def_examples.md).

## Directory map

```text
crossing_pack/
  README.md
  stopx_def_examples.md   # operator examples per stop (keep README short)
  place.py
  probe_log.py
  suggest_tags.py
  test_place.py
  test_probe_log.py
  test_suggest_tags.py
  seed/
    about_index.yaml
    talk_families.yaml
    placements.yaml       # gold answer key (committed)
    hole_ledger.yaml
  proposals/
  logs/
    .gitkeep
    probe.log             # local diary (.log is not committed)
    suggest.log           # local diary (.log is not committed)
```

## File types

| Kind | Extension | GitHub |
|---|---|---|
| Running diary | `.log` | local only |
| Long-term fixture | `.yaml` / `.json` / `.jsonl` | may be committed |

## Won't

No promote, no Door Table edits, no `$M$`, no new families from these scripts.
