# crossing_pack stop definitions and examples

Operator notes for each inquiry stop. Law stays in 730 / 731 / 740.
Run commands from this folder with `(.venv)` active.

---

## Shared: what `python -c` means

These are shell/Python facts, not Path A objects.

1. **`python -c`** — run the next argument as Python code, then exit. No `.py` file is opened.
2. **`python`** — the executable. With `(.venv)` that is the venv interpreter on `PATH`.
3. **Quotes `"..."`** — one shell argument. That text is the program.
4. **`from place import place`** — load function `place` from file `place.py`. Not an `.exe`.
5. **`p`** — a variable name you choose. Example: `p, h = place(...)`.

---

## Stop 1 — Probe log

### What is going on

`place(utterance)` files a sentence onto Seed shelves or writes a hole. It does **not** write a diary.

`probe(utterance)` calls `place()`, then appends one JSON line to a **local** log so you can count gold vs unseen.

**Gold** = one of the three answer-key sentences in `seed/placements.yaml` (not “good”).  
**Unseen** = any other exact string.

Where gold is defined:

| Layer | File | Directory |
|---|---|---|
| Answer key | `placements.yaml` | `crossing_pack/seed/` |
| Full path | `thought_simulator/requirements_20/system_playground/testbenches/idob_structure_to_meaning/crossing_pack/seed/placements.yaml` | |
| U03 hole | `hole_ledger.yaml` | same `seed/` |
| Named in prose | `20.31.731_crossing_pack_seed.md` §5 | `requirements_20/` |
| `kind` in the log | `probe_log.py` | `crossing_pack/` |

### Run command (example Jeff ran)

```text
python -c "from probe_log import probe, tally, DEFAULT_LOG_PATH
for u in ['The rock burst open.', 'Hello there.', 'Why is the sky dark?']:
    probe(u)
print(tally(DEFAULT_LOG_PATH))"
```

| Piece | Meaning |
|---|---|
| `python` | venv interpreter |
| `-c` | run the quoted block as code |
| `from probe_log import probe, tally, DEFAULT_LOG_PATH` | load functions and default log path from `probe_log.py` |
| `for u in [...]` | three sentences: one gold, two unseen |
| `probe(u)` | place + append one log line |
| `print(tally(...))` | count gold vs unseen |

Look at `place()` only (no log):

```text
python -c "from place import place; p, h = place('The rock burst open.'); print(p); print(h)"
```

### Where the output is

- Terminal: the `tally(...)` dict (and anything you `print`).
- Diary file: `logs/probe.log` (`.log` = local only, not committed).
- Tests use a temp path and do not fill `probe.log`.

Default path name in code: `DEFAULT_LOG_PATH` → `crossing_pack/logs/probe.log`.

### How to read the output

`tally` from that run:

```text
{'n': 3, 'n_gold': 1, 'n_unseen': 2, 'unseen_rate': 0.6666666666666666}
```

Three calls, one answer-key sentence, two unknowns, unseen rate 2/3.

Each line in `logs/probe.log` is one JSON object.

### Example log lines and what they mean

```json
{"about_id": "material_event_anchor", "card_id": "S_rock_burst", "family_id": "event_talk", "hole_ids": [], "kind": "gold", "n_holes": 0, "pattern_id": null, "placement_id": "P_rock_burst", "source": "probe", "ts": "2026-09-01T19:28:26.111561+00:00", "utterance": "The rock burst open."}
{"about_id": null, "card_id": null, "family_id": null, "hole_ids": ["H_unseen_hello_there"], "kind": "unseen", "n_holes": 1, "pattern_id": null, "placement_id": "P_unseen_hello_there", "source": "probe", "ts": "2026-09-01T19:28:26.116341+00:00", "utterance": "Hello there."}
{"about_id": null, "card_id": null, "family_id": null, "hole_ids": ["H_unseen_why_is_the_sky_dark"], "kind": "unseen", "n_holes": 1, "pattern_id": null, "placement_id": "P_unseen_why_is_the_sky_dark", "source": "probe", "ts": "2026-09-01T19:28:26.119993+00:00", "utterance": "Why is the sky dark?"}
```

| Line | Sentence | kind | Meaning |
|---|---|---|---|
| 1 | The rock burst open. | gold | Known Seed row. World shelf `material_event_anchor`, talk-move `event_talk`, live card `S_rock_burst`, no hole. |
| 2 | Hello there. | unseen | Not in `placements.yaml`. No tags invented. One open hole. |
| 3 | Why is the sky dark? | unseen | Same: refused to invent a category. |

Nothing here wrote IdOB YAML. The log is only the intake diary.

---

## Stop 2 — Suggest tags only

### What is going on

An unseen sentence is still a hole after Stop 1. Stop 2 may **propose** `suggested_about_id` and `suggested_family_id` from Seed allow-lists only.

- About = world filing (not six IDs).
- Family = talk-move (not six IDs, not meaning axes).
- `card_id` on the suggestion is always `null`.
- Unseen rows have `needs_review: true`.
- Does not edit `seed/placements.yaml`, live cards, Door Table, or `$M$`.
- Not NLP. Rules are the visible keyword list in `suggest_tags.py`.

Gold sentences: Stop 2 **echoes** stored tags; it does not invent them.

### Run command (example Jeff ran)

```text
python -c "from suggest_tags import suggest; print(suggest('Why is the sky dark?'))"
python -m pytest test_suggest_tags.py
```

| Piece | Meaning |
|---|---|
| `python -c "..."` | run one suggestion and print the dict |
| `from suggest_tags import suggest` | load `suggest()` from `suggest_tags.py` |
| `suggest('Why is the sky dark?')` | unseen question; propose tags; append `logs/suggest.log` |
| `print(...)` | show the row on the terminal (pipe-able) |
| `python -m pytest test_suggest_tags.py` | seven contract tests; they use a temp log, not `suggest.log` |

Suggest without printing (file only):

```text
python -c "from suggest_tags import suggest; suggest('Hello there.'); suggest('Why is the sky dark?')"
```

### Where the output is

- Terminal: the printed dict (if you used `print`).
- Diary file: `logs/suggest.log` (local only).
- Pytest report stays on the terminal unless you redirect it.

PowerShell quiet tests:

```text
python -m pytest test_suggest_tags.py > logs\pytest_suggest.log 2>&1
```

### How to read the output

Printed row from the question example:

```text
{'ts': '2026-09-01T20:31:41.321061+00:00', 'utterance': 'Why is the sky dark?', 'source': 'suggest', 'place_card_id': None, 'place_hole_ids': ['H_unseen_why_is_the_sky_dark'], 'suggested_about_id': None, 'suggested_family_id': 'ask_talk', 'card_id': None, 'needs_review': True, 'rationale': 'question shape', 'kind': 'unseen', 'n_place_holes': 1}
```

| Field | Value | Meaning |
|---|---|---|
| `kind` | `unseen` | not a gold sentence |
| `place_hole_ids` | `H_unseen_why_is_the_sky_dark` | Stop 1 already recorded a hole |
| `suggested_family_id` | `ask_talk` | candidate talk-move (question shape) |
| `suggested_about_id` | `None` | no world-shelf guess from Seed rules |
| `card_id` | `None` | did not invent or attach a live card |
| `needs_review` | `True` | human must accept or reject |
| `rationale` | `question shape` | why it guessed `ask_talk` |

`Hello there.` should look similar with both suggestions `None` and rationale `no Seed rule fired`.

### Example and what it means

Same three sentences as Stop 1:

| Sentence | Stop 1 | Stop 2 |
|---|---|---|
| The rock burst open. | gold place + card `S_rock_burst` | echo gold tags; `card_id` on suggestion still `None`; `place_card_id` is `S_rock_burst` |
| Hello there. | unseen hole | no rule fired; `needs_review` |
| Why is the sky dark? | unseen hole | suggest `ask_talk` only; `needs_review` |

Stop 2 success = unseen noted, tags only from Seed lists or null, hop untouched.

---

## Later stops

Stop 3+ examples go in this file when those stops exist. Do not grow `README.md` with run walkthroughs.
