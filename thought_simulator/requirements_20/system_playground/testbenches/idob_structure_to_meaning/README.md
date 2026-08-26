# IdOB Structure-to-Meaning Learning Bench

**Revision:** Slide-01 (learning instrument, not Path A product harness)
**Location:** `testbenches/idob_structure_to_meaning/`
**Date:** 2026-08-26

## Purpose

This bench is a research vehicle for *seeing* IdOB.

It is not the Path A PASS/FAIL harness in `testbenches/run.py`.
It does not claim that IdOB is cognition.
It asks the duck that can be answered: does this machine make the structure-to-meaning crossing visible?

Walk the numbered slides in order. Each slide teaches one named part of the present IdOB packet. Python and YAML are filled for this learning revision.

## How to run

`run_ts_struc2mn.py` is the driver for every lesson script in this folder.

From this directory:

    python run_ts_struc2mn.py

Inside `run_ts_struc2mn.py`:

- `RUN_01_STRUCTURE` … `RUN_07_CROSSING` turn each lesson on or off.
  Set a flag to `False`, or comment that `if RUN_…` block, to skip a lesson.
- Variables passed into a lesson (`card_id`, `group_id`, `cie_id`, `clip_to_unit`)
  are defined and commented at the top of `run_ts_struc2mn.py`.
  Change them there. Each lesson prints what that slide is for.

You can still run a single slide file directly, e.g.

    python 01_structure/run_01_inspect_structure.py

## How to walk

1. Read the slide README.md first.
2. Open the YAML. Field names matter more than values.
3. Run via run_ts_struc2mn.py, enabling one lesson if you want to go slowly.
4. Do not skip ahead to 07 until 01-06 each print one thing and refuse to print another.

## Design rules

1. Official IdOB field names only (see 00_contract/vocabulary.md).
2. One new idea per slide.
3. Hand-set tables are legal in this revision.
4. Same inputs -> same printed packet (replay).
5. No OuBA / truth / belief. Stop at IdOB handoff fields.
6. Changing epsilon or the six-axis layout is a new instrument revision.
