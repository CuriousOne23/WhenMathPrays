# Slide 04 — Rank among candidates only

**Theory:** [../papers/idob_s2m_theory.md](../papers/idob_s2m_theory.md) §2.6  
**Construct:** C8 in [../papers/idob_s2m_constructs.md](../papers/idob_s2m_constructs.md)  
**Previous:** [../03_map_lookup/README.md](../03_map_lookup/README.md)

## Objective (unchanged)

See competition **inside** the candidate set.

Ranking may use (hand weights are legal in this revision):
- cue score
- invariant score
- identity alignment score

Output is `final_rank_order`: a list of `group_id`.
**First id is the winner** — the prototype chosen as first M.
Later ids are still legal; they lost this pass.

## What ranking is

The map opened some doors. Ranking picks **which door is tried first**.

It is not:
- a new geometry
- a manifold neighborhood
- permission to add a group the map did not name
- CIE (`M' = M + α I` is Slide 05)
- freeze on `meaning_delta_h` (Slide 06)

Feel: several legal births; one is instantiated first. The others remain on the candidate list for visibility.

## Why it is needed

When the map is a filter (more than one group), IdOB still needs **one** prototype to become first M. Without rank, the packet would have a set of possible objects and no standing object.

When the map is a dictator (one group), rank is trivial — that id is first.
When the map is empty, rank must stay empty. Do not invent a winner.

## How it will be used

1. Take `candidate_group_ids` from Slide 03.
2. Score only those ids with this revision's weights (see `ranking_weights.slide.yaml`).
3. Emit `final_rank_order` (winner first).
4. `selected_group_id` = rank-1. That group's `group_dimensions` become first M.
5. CIE may then move M. Rank list does not have to be recomputed unless a later revision says so.

Weights here are **hand / toy** for the instrument. Changing them is a named revision if you want a different machine, not a silent retune of "cognition."

## Order: map vs rank

| List | Order means |
|------|-------------|
| Map `meaning_group_candidates` | Nothing (membership only) |
| Rank `final_rank_order` | Winner first, among map members only |

Rank must not add an id the map did not name.
Map must not pretend its YAML order is a score.

## No manifold constraint (this revision)

Group_ids 1001, 3001, 5001 have no implied nearness from their digits.
Rank need not vary smoothly from card to card.
If later traces show associations (near prototypes, co-legal nearby keys, smooth rank under small talk-shape change), a manifold or graph-plus-metric may be **investigated**. Not declared now.

## This slide must not do

- Invent candidates that were not in the map.
- Apply `M' = M + alpha I` (slide 05).
- Freeze on `meaning_delta_h` (slide 06).
- Treat group_id spelling as position.

## Boundary to feel

If ranking can pull in a group the map did not allow, the wall is broken.
If empty map yields a ranked winner, the door is fake.
If map order and rank order are always identical with no scores, rank is a copy of YAML spelling — not competition.

## Run

    python run_04_rank.py
