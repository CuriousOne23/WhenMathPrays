# Slide 10 / Stop 10 — Residue expand (leftover → which file to touch)

**Read this lesson:** [residue_expand.md](residue_expand.md)
That file is meant to stand alone for this subject.
**Previous:** [../09_structure_assignment/README.md](../09_structure_assignment/README.md)
**Next:** [../11_idob_core/README.md](../11_idob_core/README.md)

## Objective

Feel the leftover after one IdOB hop: if tension remains, a **human** expands a named file. This slide does not invent a six-tuple and does not run RB.

## Programs / YAML

- `expand.py` — `classify` + `expand_card`
- `run_10_residue_expand.py`
- `residue_next.examples.yaml` (hand table; `next_key` is suggestion or null)

## Expect

| Card / case | `after_status` | `expand_target` |
|-------------|----------------|-----------------|
| `S_rock_burst` (has `static_object_vs_dynamic_action`) | `leftover_after_map` | this table |
| `S_unmapped` | `empty_map` | `03_map_lookup` |
| unassigned utterance | `unassigned` | `09_structure_assignment` |
| mapped card, no residue | `digested_stop` | `stop` |

`next_key` stays null unless a human wrote it in the YAML.

## Must print

`residue_code`, `after_status`, digested|undigested, `expand_target`, `next_key` (or null)

## Must not print

`physicality`…`spatiality` as scores; a new `structural_key` invented here; RB `firing_order` as if implemented.

## Run

    python run_10_residue_expand.py
    python ../run_ts_struc2mn.py   # with RUN_10_RESIDUE_EXPAND = True

Driver var: `VAR_10_CARD_ID` (None = all structure cards).
