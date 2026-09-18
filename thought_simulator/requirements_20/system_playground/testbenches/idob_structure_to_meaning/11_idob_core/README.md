# Slide 11 / Stop 11 — IdOB core (realization kernel)

**Read this lesson:** [idob_core.md](idob_core.md)
That file is meant to stand alone for `idob.py`: why, how, fields in, fields out, support files, how to extend.
**Schema:** [packet.schema.yaml](packet.schema.yaml)
**Walls:** [tests_walls.py](tests_walls.py)
**Previous:** [../10_residue_expand/README.md](../10_residue_expand/README.md)

## Objective

One hop: card or utterance → packet. Orchestrator only.

Keepers from `primitives/idob/idob.py` (not a second meaning geometry):

- first-pass Δh (`meaning_semantics_before` = zeros if no `prior_M`)
- write-boundary (`process` must not mutate `routing_filter`)
- `ready_for_ouba` vs `path_b_eligible` vs `idob_complete`
- `identity_residual` separate from `residue_code`
- `hold_geometry` default `formation` on birth
- `process(tp)` adapter around `run_hop`

## Expect

Default `run_hop(card_id=S_rock_burst, cie_id=physical_stance)`:

- map set `{1001, 3001, 5001}`, rank winner `3001`
- `first_meaning_cycle` True, before-vector zeros
- CIE does not change `structural_key`
- `ready_for_ouba` True on birth; `path_b_eligible` False while card residue remains
- `next_key` is null (not invented)
- `tests_walls.py` prints PASS on every wall

`S_unmapped` → `resolution_status=empty_map`, no winner, no M.

## Risk vs Slide 07

Slide 07 teaches the wire of 01–06. Slide 11 is the realization kernel. Do not grow 11 into full Path A (TR/CTP/RB). Do not grow 07 into the product IdOB. Do not replace the six axes with the primitive 7-feature table.

## Run

    python run_11_idob_core.py
    python tests_walls.py
    python ../run_ts_struc2mn.py   # with RUN_11_IDOB_CORE = True

Driver vars: `VAR_11_CARD_ID`, `VAR_11_UTTERANCE`, `VAR_11_PACKS`, `VAR_11_CIE_ID`, `VAR_11_CLIP_TO_UNIT`.
