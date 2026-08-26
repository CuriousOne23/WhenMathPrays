# Slide 06 — Cycle, delta, named freeze

## Objective

See time as bounded search, not as it settled.

Each cycle:
1. Start from current M (and identity vector).
2. Apply CIE (or a tiny refinement rule you name in the log).
3. Compute meaning_delta_h = ||M_i - M_{i-1}|| and identity_delta = ||I_i - I_{i-1}||.
4. Halt if a stop condition fires. Write resolution_status from the same predicate that halted.

## Stop order (papers)

1. meaning stable (delta < epsilon)
2. identity stable
3. budget exhausted
4. time exhausted

Defaults in this revision: epsilon = 0.05, min 4 / max 6 cycles.

## This slide must print

- Cycle number
- M
- both deltas
- resolution_status

## This slide must not do

- Full map+rank pipeline (slide 07).
- Label stable when the halt was budget.

## Run (when implemented)

    python run_06_cycle.py
