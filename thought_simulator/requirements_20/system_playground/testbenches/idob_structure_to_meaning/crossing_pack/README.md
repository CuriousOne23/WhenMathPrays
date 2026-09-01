# crossing_pack

Seed intake plus probe log for crossing-pack first-mile operations.
This folder is not the hop.

Law:
- 20.31.730 interface
- 20.31.731 Seed schemas/tests
- 20.31.740 inquiry path

This is the first mile from world-talk toward IdOB inputs.
Live cards and Door Table remain in their existing files.

## Directory map

```text
crossing_pack/
	README.md
	place.py              # place(utterance) -> (placement, holes); no disk write
	probe_log.py          # probe() wraps place(); appends JSONL; tally()
	test_place.py
	test_probe_log.py
	seed/
		about_index.yaml
		talk_families.yaml
		placements.yaml     # gold oracle
		hole_ledger.yaml
	proposals/            # empty; Card Proposer later
	logs/
		.gitkeep
		probe.jsonl         # created when you run probe(); local tally
```

## What place.py is

`place.py` is a function module, not a program with options.
It is an exact-match stub against Seed gold utterances.
It does not run IdOB and does not write files.

Signature:
`place(utterance: str, source: str = "test") -> tuple[dict, list[dict]]`

## How to run place()

From this directory with venv active:

```text
python -c "from place import place; print(place('The rock burst open.'))"
```

There are no CLI options.
Input is the utterance string; `source` defaults to `"test"`.

## What the return means

- First item: Placement Record (`about_id`, `family_id`, `pattern_id`, `card_id`, `hole_ids`, ...)
- Second item: hole rows (possibly empty)
- Gold three: known tags; U03 has `card_id` null plus open hole
- Anything else: all tags null plus one unseen hole

## What probe_log.py is and why

Stop 1 probe layer.
Same placement result as `place()`, plus a JSONL log for counting gold vs unseen.

```text
python -c "from probe_log import probe, tally, DEFAULT_LOG_PATH
probe('The rock burst open.')
probe('Hello there.')
print(tally(DEFAULT_LOG_PATH))"
```

## Where output goes

`logs/probe.jsonl` with one JSON object per line.
Tests pass a temp path and do not write the default file.
Do not treat probe JSONL as hop output.

## How to read a log row

- `kind`: `gold` or `unseen`
- `unseen` means intake refused to invent tags
- `tally()` returns `n`, `n_gold`, `n_unseen`, `unseen_rate`

## Won't

- No promote
- No Door Table edits
- No $M$
- No new families from these scripts
