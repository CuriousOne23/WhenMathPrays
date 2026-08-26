# Slide 03 — Structure bounds meaning (lookup)

## Objective

Feel the bound: structure does not score meaning; it restricts the candidate set.

    structural_key -> candidate group_ids

That is the whole slide.

## This slide must print

- Input card_id / structural_key
- candidate_group_ids
- empty map if none

## This slide must not print

- Rank order (slide 04)
- Six-float modulation
- meaning_delta_h

## Boundary to feel

- Thin map -> structure looks like a dictator (few candidates).
- Dense map -> structure is a filter.
- Empty map -> no legal meaning yet (machine halt later, not cognition failed).

## Run (when implemented)

    python run_03_lookup.py
