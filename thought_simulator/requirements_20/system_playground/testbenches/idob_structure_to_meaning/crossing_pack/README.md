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

The current README lists roles. It does not say **each `.py` reads X because … and writes Y because …**. Use this follow-up prompt.

---

### **2.1 Inputs and outputs per program**

#### place.py
Reads:
- seed/placements.yaml — gold answer key (exact utterance match)
- seed/hole_ledger.yaml — hole rows for gold ids (e.g. U03)
- seed/about_index.yaml, seed/talk_families.yaml — loaded if the code loads them; say so if unused for matching
Writes: nothing
Why no write: placement is a return value only; gold stays the fixture
Look for: returned dict + hole list on the terminal if you print

#### probe_log.py
Reads: whatever place() reads (Seed YAML via place.py)
Writes: logs/probe.log (default) or log_path you pass
Why write: Stop 1 diary so tally() can count gold vs unseen
Does not write: Seed YAML, live cards
Look for: one JSON line per probe(); tally dict on terminal

#### suggest_tags.py
Reads: place() / Seed YAML; allow-lists in the module (must match Seed about/family ids — if the code does not open those YAML files, say “allow-lists copied in suggest_tags.py, not read live”)
Writes: logs/suggest.log (default) or log_path
Why write: Stop 2 candidate diary; local .log not committed
Does not write: placements.yaml, cards, Door Table, $M$
Look for: suggested_about_id / suggested_family_id / needs_review / card_id None

#### test_*.py
Reads: the module under test + Seed YAML through place/suggest
Writes: temp logs only (pytest tmp_path)
Does not write: logs/probe.log, logs/suggest.log, seed/*
Look for: pytest “passed”, not a diary file

utterance → place.py (read seed/) → probe_log.py (write probe.log) and/or suggest_tags.py (write suggest.log)

---

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
