# IdOB Structure-to-Meaning Learning Bench

**Revision:** Slide-01 (learning instrument, not Path A product harness)
**Location:** `testbenches/idob_structure_to_meaning/`
**Date:** 2026-08-26

## Purpose

This bench is a research vehicle for *seeing* IdOB.

It is not the Path A PASS/FAIL harness in `testbenches/run.py`.
It does not claim that IdOB is cognition.
It asks the duck that can be answered: does this machine make the structure-to-meaning crossing visible?

Walk the numbered slides in order. Each slide teaches one named part of the present IdOB packet. Python and YAML here start as stubs; the markdown is the curriculum.

## What you should be able to witness by slide 08

- What structure is, and what is forbidden inside it
- What a meaning group is, and what the six fields are
- How structure bounds meaning space (candidates, not scores)
- What CIE changes, and what it must not change
- What meaning_delta_h and the four stop reasons are
- IdOB objective: structure -> admissible groups -> identity-conditioned six-vector -> named freeze

## How to walk

1. Read the slide README.md first.
2. Open the YAML (schema / examples). Field names matter more than values.
3. Run the run_0N_*.py stub when you are ready to implement that slide only.
4. Do not skip ahead to 07 until 01-06 each print one thing and refuse to print another.

## Design rules

1. Official IdOB field names only (see 00_contract/vocabulary.md).
2. One new idea per slide.
3. Hand-set tables are legal in this revision.
4. Same inputs -> same printed packet (replay).
5. No OuBA / truth / belief. Stop at IdOB handoff fields.
6. Changing epsilon or the six-axis layout is a new instrument revision, not a silent tweak.

## Slide map

- 00_contract: names and the contract wall
- 01_structure: structure as geometry; no meaning floats
- 02_meaning_groups: meaning as six named numbers on a group
- 03_map_lookup: structure -> which groups may compete
- 04_ranking: order among candidates only
- 05_cie: identity moves M; structure stays fixed
- 06_cycle_and_delta: delta, budget, named freeze
- 07_idob_slide: full crossing on official field names
- 08_witness: can you name every field and its job?

## Relation to papers

Source names live in primitives/idob/papers/structure_to_meaning/.
This bench does not replace those papers. It makes their field names inspectable.
