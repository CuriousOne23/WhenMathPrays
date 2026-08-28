# Slide 11 — IdOB core (realization kernel)

**Read this lesson:** [idob_core.md](idob_core.md)  
That file is meant to stand alone for `idob.py`: why, how, fields in, fields out, support files, how to extend.

## Objective

One hop: card or utterance → packet. Orchestrator only.

Keepers from `primitives/idob/idob.py` (not a second meaning geometry):

- first-pass Δh (`meaning_semantics_before` = zeros if no `prior_M`)
- write-boundary (`process` must not mutate `routing_filter`)
- `ready_for_ouba` vs `path_b_eligible` vs `idob_complete`
- `identity_residual` separate from `residue_code`
- `hold_geometry` default `formation` on birth
- `process(tp)` adapter around `run_hop`

## Risk vs Slide 07

Slide 07 teaches the wire of 01–06. Slide 11 is the realization kernel. Do not grow 11 into full Path A (TR/CTP/RB). Do not grow 07 into the product IdOB. Do not replace the six axes with the primitive 7-feature table.

## Run

    python run_11_idob_core.py
    python tests_walls.py
