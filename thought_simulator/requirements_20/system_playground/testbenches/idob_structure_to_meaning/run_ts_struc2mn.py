#!/usr/bin/env python3
"""
run_ts_struc2mn.py
Driver for the IdOB structure-to-meaning learning bench.
Not testbenches/run.py.
Set RUN_* flags True/False (or comment the if-block) to choose lessons.
Variables passed into lessons are defined and commented below.
Run: python run_ts_struc2mn.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

BENCH_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH_ROOT))

# Which lessons to run
RUN_01_STRUCTURE = False   # six geometry IDs + structural_key; no meaning floats
RUN_02_GROUPS = False      # meaning groups and the six-field prototype
RUN_03_LOOKUP = False      # structure -> candidate group ids
RUN_04_RANK = False        # rank only inside the candidate set
RUN_05_CIE = False         # M' = M + alpha * I
RUN_06_CYCLE = False       # deltas, epsilon, named freeze
RUN_07_CROSSING = False    # teaching wire of 01-06
RUN_09_ASSIGN = False      # utterance + packs -> card or miss
RUN_10_RESIDUE_EXPAND = False  # leftover -> which file to expand
RUN_11_IDOB_CORE = True    # one-hop idob.py kernel

# card_id examples: S_rock_burst, S_deadline_friday, S_sleepy, S_unmapped
# group_id examples: 1001, 2001, 3001, 4001, 5001
# cie_id examples: physical_stance, scientific_stance, neutral
# utterance examples: "The rock burst open.", "zzzzq no cue"
# packs examples: ["base_en"], ["base_en", "pack_geology"]

VAR_01_CARD_ID = None          # None = all cards
VAR_02_GROUP_ID = None         # None = all groups
VAR_03_CARD_ID = "S_rock_burst"
VAR_04_CARD_ID = "S_rock_burst"
VAR_05_GROUP_ID = 1001
VAR_05_CIE_ID = None           # None = all envelopes
VAR_05_CLIP_TO_UNIT = True
VAR_06_GROUP_ID = 1001
VAR_06_CIE_ID = "physical_stance"
VAR_06_CLIP_TO_UNIT = True
VAR_07_CARD_ID = "S_rock_burst"
VAR_07_CIE_ID = "physical_stance"
VAR_07_CLIP_TO_UNIT = True
VAR_09_UTTERANCE = None        # None = default demo lines
VAR_09_PACKS = None            # None = each demo line carries its own pack list
VAR_10_CARD_ID = None          # None = all structure cards
VAR_11_CARD_ID = "S_rock_burst"  # None = four teaching cards
VAR_11_UTTERANCE = None         # if set, 09 assign path instead of card_id
VAR_11_PACKS = None
VAR_11_CIE_ID = "physical_stance"
VAR_11_CLIP_TO_UNIT = True


def _load_slide(module_name: str, relative_path: str):
    path = BENCH_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    print("\nIdOB structure-to-meaning learning bench")
    print("Driver: run_ts_struc2mn.py")
    print("This run is for visibility, not a cognition verdict.\n")

    if RUN_01_STRUCTURE:
        slide = _load_slide("run_01_inspect_structure", "01_structure/run_01_inspect_structure.py")
        slide.run(card_id=VAR_01_CARD_ID)

    if RUN_02_GROUPS:
        slide = _load_slide("run_02_inspect_groups", "02_meaning_groups/run_02_inspect_groups.py")
        slide.run(group_id=VAR_02_GROUP_ID)

    if RUN_03_LOOKUP:
        slide = _load_slide("run_03_lookup", "03_map_lookup/run_03_lookup.py")
        slide.run(card_id=VAR_03_CARD_ID)

    if RUN_04_RANK:
        slide = _load_slide("run_04_rank", "04_ranking/run_04_rank.py")
        slide.run(card_id=VAR_04_CARD_ID)

    if RUN_05_CIE:
        slide = _load_slide("run_05_modulate", "05_cie/run_05_modulate.py")
        slide.run(group_id=VAR_05_GROUP_ID, cie_id=VAR_05_CIE_ID, clip_to_unit=VAR_05_CLIP_TO_UNIT)

    if RUN_06_CYCLE:
        slide = _load_slide("run_06_cycle", "06_cycle_and_delta/run_06_cycle.py")
        slide.run(group_id=VAR_06_GROUP_ID, cie_id=VAR_06_CIE_ID, clip_to_unit=VAR_06_CLIP_TO_UNIT)

    if RUN_07_CROSSING:
        slide = _load_slide("run_07_idob_slide", "07_idob_slide/run_07_idob_slide.py")
        slide.run(card_id=VAR_07_CARD_ID, cie_id=VAR_07_CIE_ID, clip_to_unit=VAR_07_CLIP_TO_UNIT)

    if RUN_09_ASSIGN:
        slide = _load_slide("run_09_assign", "09_structure_assignment/run_09_assign.py")
        slide.run(utterance=VAR_09_UTTERANCE, packs_loaded=VAR_09_PACKS)

    if RUN_10_RESIDUE_EXPAND:
        slide = _load_slide("run_10_residue_expand", "10_residue_expand/run_10_residue_expand.py")
        slide.run(card_id=VAR_10_CARD_ID)

    if RUN_11_IDOB_CORE:
        slide = _load_slide("run_11_idob_core", "11_idob_core/run_11_idob_core.py")
        slide.run(
            card_id=VAR_11_CARD_ID,
            utterance=VAR_11_UTTERANCE,
            packs_loaded=VAR_11_PACKS,
            cie_id=VAR_11_CIE_ID,
            clip_to_unit=VAR_11_CLIP_TO_UNIT,
        )

    print("Driver finished. Next: 08_witness/checklist.md if you want to name what you saw.")


if __name__ == "__main__":
    main()
