# crossing_pack

Seed intake plus probe log operator guide.
This folder is not the hop.

Law:
- 20.31.730 interface
- 20.31.731 Seed schemas/tests
- 20.31.740 inquiry path

This is the first mile from world-talk toward IdOB inputs.
Live cards and Door Table remain elsewhere.

## Directory map

```text
crossing_pack/
	README.md
	place.py              # place(utterance) -> (placement, holes); no disk write
	probe_log.py          # probe() wraps place(); appends JSONL; tally()
	suggest_tags.py       # suggest(utterance) -> candidate about/family; no live writes
	test_place.py
	test_probe_log.py
	test_suggest_tags.py
	seed/
		about_index.yaml
		talk_families.yaml
		placements.yaml     # gold oracle
		hole_ledger.yaml
	proposals/            # empty; Card Proposer later
	logs/
		.gitkeep
		probe.jsonl         # created when you run probe(); local tally
		suggest.jsonl       # optional; only if you pass log_path
```

## What place.py is

`place.py` is a function module, not a CLI program.
It is an exact-match stub against Seed gold utterances.
It does not run IdOB and does not write files.

Signature:
`place(utterance: str, source: str = "test") -> tuple[dict, list[dict]]`

Input:
- `utterance` string
- optional `source` (default `"test"`)

Output:
- item 1: Placement Record (`about_id`, `family_id`, `pattern_id`, `card_id`, `hole_ids`, ...)
- item 2: hole rows list (possibly empty)

Gold means answer key (not "good").
- Gold three: known tags; U03 has `card_id` null plus open hole.
- Unseen utterance: all tags null plus one unseen hole row.

Run from this directory (venv active):

```text
python -c "from place import place; print(place('The rock burst open.'))"
```

No CLI options are defined for `place.py`.

## probe vs place

`place()` returns data only.
`probe()` calls `place()`, writes one JSONL row, then returns the same tuple.

Jeff command:

```text
python -c "from probe_log import probe, tally, DEFAULT_LOG_PATH
for u in ['The rock burst open.', 'Hello there.', 'Why is the sky dark?']:
		probe(u)
print(tally(DEFAULT_LOG_PATH))"
```

Observed tally for that run:
`{n: 3, n_gold: 1, n_unseen: 2, unseen_rate: 0.67}`

## Q&A quick decode

1. What `python -c` does
- Runs the quoted text as Python source code.

2. `python` is the executable
- Usually the venv interpreter on PATH.

3. Quotes
- The whole quoted block is one shell argument containing source code.

4. `from place import place`
- Python import statement, not an `.exe`.

5. `p` in examples
- A normal variable name that can hold the placement dict.

## Where output goes

`logs/probe.jsonl` (one JSON object per line).
Tests use a temp path and do not write the default file.
This folder does not write IdOB YAML.

## Three JSONL lines from logs/probe.jsonl

```json
{"about_id": "material_event_anchor", "card_id": "S_rock_burst", "family_id": "event_talk", "hole_ids": [], "kind": "gold", "n_holes": 0, "pattern_id": null, "placement_id": "P_rock_burst", "source": "probe", "ts": "2026-09-01T19:28:26.111561+00:00", "utterance": "The rock burst open."}
{"about_id": null, "card_id": null, "family_id": null, "hole_ids": ["H_unseen_hello_there"], "kind": "unseen", "n_holes": 1, "pattern_id": null, "placement_id": "P_unseen_hello_there", "source": "probe", "ts": "2026-09-01T19:28:26.116341+00:00", "utterance": "Hello there."}
{"about_id": null, "card_id": null, "family_id": null, "hole_ids": ["H_unseen_why_is_the_sky_dark"], "kind": "unseen", "n_holes": 1, "pattern_id": null, "placement_id": "P_unseen_why_is_the_sky_dark", "source": "probe", "ts": "2026-09-01T19:28:26.119993+00:00", "utterance": "Why is the sky dark?"}
```

Line-by-line reading:
- line 1: gold hit for the rock utterance; existing card `S_rock_burst`; no holes.
- line 2: unseen utterance; no tags invented; one open unseen hole id.
- line 3: unseen utterance; no tags invented; one open unseen hole id.

## Where gold is defined

| Layer | File | Directory |
|---|---|---|
| Answer key (use this) | placements.yaml | crossing_pack/seed/ |
| Full path placements.yaml | thought_simulator/requirements_20/system_playground/testbenches/idob_structure_to_meaning/crossing_pack/seed/placements.yaml | repository path |
| U03 hole | hole_ledger.yaml | same seed/ folder |
| Named in prose | 20.31.731_crossing_pack_seed.md §5 | thought_simulator/requirements_20/ |
| `kind: gold` in the log | probe_log.py | crossing_pack/ |

Gold terms (the three sentences plus their tags) live in `seed/placements.yaml`.
That is what `place()` looks up.
Papers name those rows but do not execute placement.

If a sentence is not an `utterance` in `placements.yaml`, it is unseen.

## Stop 2: suggest_tags.py

Function, not a CLI. Proposes `suggested_about_id` and `suggested_family_id` from Seed allow-lists only.
Does not write live cards, Door Table, `$M$`, or `seed/placements.yaml`.
Unseen suggestions always have `needs_review: true` and `card_id: null`.

```text
python -c "from suggest_tags import suggest; print(suggest('Why is the sky dark?'))"
```

Optional log only if you pass `log_path`. Default is no disk write.

This is not NLP. Rules are the visible keyword list in `suggest_tags.py`.

## Won't

- No promote
- No Door Table edits
- No $M$
- No new families from these scripts
