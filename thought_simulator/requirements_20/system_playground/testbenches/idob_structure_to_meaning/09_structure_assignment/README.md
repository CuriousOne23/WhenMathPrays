# Slide 09 / Stop 9 — Structure assignment (utterance → card or miss)

**Doc:** [assignment.md](assignment.md)
**Theory:** two geometries stay two; this slide only fills structure IDs.
**Does not replace:** Slide 01 (inspect a given card).
**Next:** [../10_residue_expand/README.md](../10_residue_expand/README.md)

## Objective

Feel the **assigner** as its own science with a thin interface:

    utterance + loaded packs → {six IDs + residue} | unassigned

Then the existing dumb hasher spells the key. No meaning floats. No map. No CIE.

## Programs / YAML

- `assign.py` — `assign(utterance, packs_loaded)`
- `run_09_assign.py` — lesson printer
- `packs/base_en.yaml`, `packs/pack_geology.yaml`, `packs/pack_conflict.yaml`
- [assignment.schema.yaml](assignment.schema.yaml)

Pack file on disk but **not** in `packs_loaded` → cues in that file do not fire.

## Expect

| Line | Packs | Status |
|------|-------|--------|
| `The rock burst open.` | `base_en` | `assigned` (same six IDs as Slide 01 `S_rock_burst`) |
| `zzzzq no cue` | `base_en` | `unassigned`, `structural_key` is null |
| `The ore melted.` | `base_en` only | miss or partial vs geology cues |
| `The ore melted.` | `base_en` + `pack_geology` | geology pack may fill slots |

`packs_loaded` is always printed (replay).

## This slide must not print

- `physicality` … `spatiality`
- `candidate_group_ids` as if assignment were the map
- A key when status is `unassigned`

## Run

    python run_09_assign.py
    python ../run_ts_struc2mn.py   # with RUN_09_ASSIGN = True

Driver vars: `VAR_09_UTTERANCE`, `VAR_09_PACKS`.

Triggers / COB auto-load are **named later**, not coded here. Manual pack list only.
