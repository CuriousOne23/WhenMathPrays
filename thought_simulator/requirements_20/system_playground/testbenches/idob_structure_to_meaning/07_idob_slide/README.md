# Slide 07 / Stop 7 — Full IdOB crossing (still a slide)

**Previous:** [../06_cycle_and_delta/README.md](../06_cycle_and_delta/README.md)
**Next:** [../08_witness/README.md](../08_witness/README.md)
**Schema:** [packet_out.schema.yaml](packet_out.schema.yaml)
**Scenarios:** [scenarios.md](scenarios.md)

## Objective

Wire slides 01–06 into one run that emits an `idob_object_min` packet.

    structure card → structural_key → candidates → rank → M from group → CIE / cycle → packet

This is IdOB-Slide-01, not full Path A IdOB. Slide 11 is the realization kernel. Do not grow this folder into product IdOB.

## Program

`run_07_idob_slide.py`

- Reads the 01 card, hashes the toy key, looks up the 03 map.
- Calls `run_04_rank.run(card_id)` for `final_rank_order` (list; winner first).
- Births M from the rank-1 group's `group_dimensions`.
- Calls `run_06_cycle.run(group_id, cie_id)` for M', deltas, freeze.
- Empty map → no six-vector; status must not pretend `stable`.

## Expect (default `S_rock_burst` + `physical_stance`)

- `candidate_group_ids`: `[1001, 3001, 5001]`
- `final_rank_order`: `[3001, 1001, 5001]`
- `selected_group_id`: `3001`
- Packet fields listed in `packet_out.schema.yaml`
- `S_unmapped`: no group, no fake M

## This slide must print

The packet fields in `packet_out.schema.yaml`.

## This slide must not print

Truth, belief, OuBA module names, or nested example-paper score bags.

## Risk vs Slide 11

Slide 07 is the **teaching wire** of 01–06. Slide 11 `11_idob_core/` is the **realization kernel** (`idob.py`). If 11 starts swallowing 07's lesson job, or 07 starts becoming the kernel, the bench has mixed teaching with realization.

## Note — leftover stays visible (Slide 10)

The crossing packet should keep `residue_code` visible when present. Next-hop / expand recipe is not this slide: [../10_residue_expand/residue_expand.md](../10_residue_expand/residue_expand.md).

## Run

    python run_07_idob_slide.py
    python ../run_ts_struc2mn.py   # with RUN_07_CROSSING = True

Driver vars: `VAR_07_CARD_ID`, `VAR_07_CIE_ID`, `VAR_07_CLIP_TO_UNIT`.
