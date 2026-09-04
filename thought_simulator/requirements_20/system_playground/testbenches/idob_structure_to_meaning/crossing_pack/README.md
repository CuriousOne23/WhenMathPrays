# crossing_pack

## 1. Purpose

Seed intake folder. Not the hop.

Law: 20.31.730, 20.31.731, 20.31.740.

Operator walkthroughs and command/output decode stay in
[stopx_def_examples.md](stopx_def_examples.md).

## 2. File inventory - every Python program

| File | Role |
|---|---|
| `place.py` | `place(utterance)` exact-match against `seed/placements.yaml`. No disk write. Gold returns stored tags; unseen returns null tags plus hole. Successful run returns a placement dict and hole list with expected fields. |
| `probe_log.py` | Stop 1. `probe()` wraps `place()` and appends `logs/probe.log`. `tally()` counts gold vs unseen. Successful run appends one row per call and returns matching counts. |
| `suggest_tags.py` | Stop 2. `suggest()` proposes Seed about/family only. Suggested `card_id` is always `None`. Unseen sets `needs_review: True`. Appends `logs/suggest.log`. Successful run returns a row with `kind`, `suggested_*`, `card_id: None`, and appends one line. |
| `test_place.py` | Contract tests for `place()`. Uses direct calls and temp expectations; does not fill `probe.log`. Successful run is all tests passing. |
| `test_probe_log.py` | Contract tests for `probe()` and `tally()`. Uses a temp log file path and does not fill `logs/probe.log`. Successful run is all tests passing with expected counts. |
| `test_suggest_tags.py` | Contract tests for `suggest()`. Uses temp log file fixture; does not fill `suggest.log`. Successful run is all tests passing with allowed-id and no-card checks. |

## 3. Support files

| File | Why |
|---|---|
| `seed/placements.yaml` | Gold answer key (committed). |
| `seed/about_index.yaml` | Allowed about ids. |
| `seed/talk_families.yaml` | Allowed family ids. |
| `seed/hole_ledger.yaml` | U03 open hole. |
| `logs/probe.log` | Local Stop 1 diary (`.log` not committed). |
| `logs/suggest.log` | Local Stop 2 diary (`.log` not committed). |
| `proposals/` | Empty; Card Proposer later. |
| `stopx_def_examples.md` | Command meaning and example output decode. |

Convention: running diaries = `.log` (local). Long-term fixtures = `.yaml` /
`.json` / `.jsonl` (may be committed).

## 4. Expected terminal flow

Run from `crossing_pack`, with `(.venv)` on.

```text
python -c "from place import place; p, h = place('The rock burst open.'); print(p); print(h)"
```

Look for: `family_id` `event_talk`, `card_id` `S_rock_burst`, empty holes.

```text
python -c "from probe_log import probe, tally, DEFAULT_LOG_PATH
for u in ['The rock burst open.', 'Hello there.', 'Why is the sky dark?']:
    probe(u)
print(tally(DEFAULT_LOG_PATH))"
```

Look for: tally with `n_gold` >= 1 and `n_unseen` >= 1 if those strings were
used; new lines in `logs/probe.log`.

```text
python -c "from suggest_tags import suggest; print(suggest('Why is the sky dark?'))"
```

Look for: `kind: unseen`, `suggested_family_id: ask_talk` (or `None`),
`card_id: None`, `needs_review: True`; line appended to `logs/suggest.log`.

```text
python -m pytest test_place.py test_probe_log.py test_suggest_tags.py
```

Look for: all tests passed. Pytest output is a test report, not the intake diary.

## 5. What `-m pytest` means

`python -m pytest file.py` runs test functions in that file; it is not Stop 2 suggesting tags.

## 6. Won't

No promote, no Door Table, no `$M$`, no new family/about ids from these scripts.
