# Slide 07 — Full IdOB crossing (still a slide)

## Objective

Wire slides 01-06 into one run that emits an idob_object_min packet.

    structure card -> structural_key -> candidates -> rank -> M from group -> CIE / cycle -> packet

This is IdOB-Slide-01, not full Path A IdOB.

## This slide must print

The packet fields in packet_out.schema.yaml.

## This slide must not print

Truth, belief, OuBA module names, or nested example-paper score bags.

## Scenarios

See scenarios.md. Run at least:
- same structure, two CIEs
- two structures, one CIE

## Note — packet should still show leftover (Slide 10)

The crossing packet should keep `residue_code` visible when present. Next-hop / expand recipe is not this slide: [../10_residue_expand/residue_expand.md](../10_residue_expand/residue_expand.md).

## Risk vs Slide 11

Slide 07 is the **teaching wire** of 01–06. Slide 11 `11_idob_core/` is the **realization kernel** (`idob.py`). Do not grow 07 into product IdOB. Do not grow 11 into full Path A (TR / CTP / RB). If 11 starts swallowing 07's lesson job, or 07 starts becoming the kernel, the bench has mixed teaching with realization.

## Run (when implemented)

    python run_07_idob_slide.py
