# Slide 04 — Rank among candidates only

## Objective

See competition inside the candidate set.

Ranking may use (hand weights are legal):
- cue score
- invariant score
- identity alignment score

Output is final_rank_order: a list of group_id.

## This slide must not do

- Invent candidates that were not in the map.
- Apply M' = M + alpha I (slide 05).
- Freeze on meaning_delta_h (slide 06).

## Boundary to feel

If ranking can pull in a group the map did not allow, the wall is broken.

## Run (when implemented)

    python run_04_rank.py
