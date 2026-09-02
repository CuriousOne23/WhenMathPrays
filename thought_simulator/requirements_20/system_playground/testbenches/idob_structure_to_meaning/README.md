# IdOB Structure-to-Meaning Learning Bench

**Revision:** Slide-01 (learning instrument, not Path A product harness)
**Location:** `testbenches/idob_structure_to_meaning/`
**Date:** 2026-08-26; spine papers 2026-08-27; Slides 09–11 2026-08-27

## Purpose

This bench is a research vehicle for *seeing* IdOB.

It is not the Path A PASS/FAIL harness in `testbenches/run.py`.
It does not claim that IdOB is cognition.
It asks the duck that can be answered: does this machine make the structure-to-meaning crossing visible?

Walk the numbered slides in order. Each slide teaches one named part of the present IdOB packet. Python and YAML are filled for this learning revision.

## Understanding path (read before or beside the slides)

The machine was being built by feel. These two papers state the unproven theory and define the constructs the lessons use:

1. **Theory stake** — [papers/idob_s2m_theory.md](papers/idob_s2m_theory.md)
   What Path A / IdOB claims and refuses about structure to speaker meaning-object.
2. **Constructs + glossary** — [papers/idob_s2m_constructs.md](papers/idob_s2m_constructs.md)
   Identity, boundary, example, field, and slide for each named part. Glossary is Appendix A of that file.

Supporting notes (not a second spine): `01_structure/structure.md`, `02_meaning_groups/dimensions.md`, `03_map_lookup/README.md`, `04_ranking/README.md`, `05_cie/README.md`, `09_structure_assignment/assignment.md`, `10_residue_expand/residue_expand.md`, `11_idob_core/idob_core.md`, `papers/ts_patha_theory.md`, `papers/ts_sob2srob_req4idob.md`.

Short field list for Slide 00: [00_contract/vocabulary.md](00_contract/vocabulary.md).

Then: slides 00-11, then `run_ts_struc2mn.py`. Sibling indexes (not on that walk): [`12_reduction/`](12_reduction/README.md), [`crossing_pack/`](crossing_pack/README.md).

## How to run

`run_ts_struc2mn.py` is the driver for every lesson script in this folder.

From this directory:

    python run_ts_struc2mn.py

Inside `run_ts_struc2mn.py`:

- `RUN_01_STRUCTURE` … `RUN_07_CROSSING`, `RUN_09_ASSIGN`, `RUN_10_RESIDUE_EXPAND`, `RUN_11_IDOB_CORE` turn each lesson on or off.
  Set a flag to `False`, or comment that `if RUN_…` block, to skip a lesson.
- Variables passed into a lesson (`card_id`, `group_id`, `cie_id`, `clip_to_unit`, `utterance`, `packs_loaded`)
  are defined and commented at the top of `run_ts_struc2mn.py`.
  Change them there. Each lesson prints what that slide is for.

You can still run a single slide file directly, e.g.

    python 01_structure/run_01_inspect_structure.py
    python 09_structure_assignment/run_09_assign.py
    python 10_residue_expand/run_10_residue_expand.py
    python 11_idob_core/run_11_idob_core.py
    python 11_idob_core/tests_walls.py

## How to walk

1. Skim the theory paper, then the construct card for the slide you will run.
2. Read the slide README.md.
3. Open the YAML. Field names matter more than values.
4. Run via run_ts_struc2mn.py, enabling one lesson if you want to go slowly.
5. Do not skip ahead to 07 until 01-06 each print one thing and refuse to print another.
6. Slide 09 is the assigner (utterance → card). It does not replace Slide 01.
7. Slide 10 is leftover → which file to expand. It does not replace RB or 03.
8. Slide 11 is the one-hop kernel (`idob.py`). It does not replace Slide 07's teaching wire.

## Design rules

1. Official IdOB field names only (see 00_contract/vocabulary.md and the constructs glossary).
2. One new idea per slide.
3. Hand-set tables are legal in this revision.
4. Same inputs -> same printed packet (replay).
5. No OuBA / truth / belief. Stop at IdOB handoff fields.
6. Changing epsilon or the six-axis layout is a new instrument revision.

## Slide map

| Slide | Folder | You gain a feel for |
|------:|--------|---------------------|
| 00 | `00_contract/` | Names and the contract wall |
| 01 | `01_structure/` | Structure as geometry; no meaning floats |
| 02 | `02_meaning_groups/` | Meaning as six named numbers on a group |
| 03 | `03_map_lookup/` | Structure -> which groups may compete |
| 04 | `04_ranking/` | Order among candidates only |
| 05 | `05_cie/` | Identity moves M; structure stays fixed |
| 06 | `06_cycle_and_delta/` | delta_h, budget, named freeze |
| 07 | `07_idob_slide/` | Teaching wire of 01–06 on official field names |
| 08 | `08_witness/` | Can you name every field and its job? |
| 09 | `09_structure_assignment/` | Utterance + packs → six IDs or miss |
| 10 | `10_residue_expand/` | Leftover → which file a human expands |
| 11 | `11_idob_core/` | One-hop `idob.py` kernel + wall tests |

Sibling folders (not on the `run_ts_struc2mn.py` 00–11 walk):

| Folder | Index |
|--------|-------|
| `12_reduction/` | [12_reduction/README.md](12_reduction/README.md) — reduction harness vs cheap rivals |
| `crossing_pack/` | [crossing_pack/README.md](crossing_pack/README.md) — seed intake / crossing inquiry pack |

## 07 vs 11

07 teaches the crossing by walking prior slides. 11 realizes the same hop as a callable packet builder. Neither is Path A routing. Growing 11 into TR/CTP/RB, or growing 07 into the product kernel, mixes jobs.

## Relation to papers (IdOB primitive suite)

Source names and contracts also live in:

`thought_simulator/requirements_20/system_playground/primitives/idob/papers/structure_to_meaning/`

This bench does not replace those papers. It makes their field names inspectable and states the theory-stake for the crossing.
