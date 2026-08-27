# Slide 09 — Structure assignment (utterance → card or miss)

**Doc:** [assignment.md](assignment.md)  
**Theory:** two geometries stay two; this slide only fills structure IDs.  
**Does not replace:** Slide 01 (inspect a given card).

## Objective

Feel the **assigner** as its own science with a thin interface:

    utterance + loaded packs → {six IDs + residue} | unassigned

Then the existing dumb hasher spells the key. No meaning floats. No map. No CIE.

## What you should see

- Known toy lines get the same six IDs as Slide 01 cards.
- Unknown line → `unassigned` (or `partial`), never a silent invented ID.
- `packs_loaded` printed (replay).
- Pack file on disk but **not** in `packs_loaded` → cues in that file do not fire.

## This slide must not print

- physicality … spatiality
- candidate_group_ids as if assignment were the map
- A key when status is `unassigned`

## Run

    python run_09_assign.py

or enable `RUN_09_ASSIGN` in `run_ts_struc2mn.py`.

Triggers / COB auto-load are **named later**, not coded here. Manual pack list only.
