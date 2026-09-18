# Slide 04 / Stop 4 — Rank among candidates only

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

## Ranking implemented this revision

Program: `run_04_rank.py`  
Weights: `ranking_weights.slide.yaml`

### Formula

Each helper is clipped to $[0, 1]$. Then:
  
$$
\mathrm{score}(g) = 
w_\mathrm{cue}\cdot\mathrm{invariant}(g)
\mathrm{+} w_{\mathrm{inv}}\cdot\mathrm{invariant}(g)
\mathrm{+} w_{\mathrm{id}}\cdot\mathrm{identity}(g)
$$

Sort descending by score. Tie-break: smaller `group_id` first.  
Empty candidate set → empty `final_rank_order`, `selected_group_id = None`.

### Weights (hand / toy)

| Weight | Value |
|--------|------:|
| `cue_weight` | 0.4 |
| `invariant_weight` | 0.3 |
| `identity_weight` | 0.3 |

### Scoring helpers

Named functions in `run_04_rank.py`:

| Helper | Job this revision |
|--------|-------------------|
| `cue_score` | How well the prototype matches talk-shape cues |
| `invariant_score` | How stable the prototype stays under small talk-shape change |
| `identity_alignment_score` | How well the prototype sits with the current identity/stance envelope |

This revision does **not** compute those from live SOB / SROB / CnOB / SmOB residue. The three helpers read `group_toy_scores` in the weights YAML. That is an instrument stub, not a claim that ranking replaces the upstream packet builders.

### Toy helper table

| group_id | cue | invariant | identity | score at current weights |
|---------:|----:|----------:|---------:|-------------------------:|
| 1001 | 0.8 | 0.7 | 0.4 | 0.650 |
| 3001 | 0.9 | 0.7 | 0.8 | 0.810 |
| 4001 | 0.5 | 0.6 | 0.3 | 0.470 |
| 5001 | 0.4 | 0.8 | 0.2 | 0.460 |

Worked `S_rock_burst` (map set `{1001, 3001, 5001}`):

- `final_rank_order` = `[3001, 1001, 5001]`
- `selected_group_id` = `3001`

Map YAML spelling on that card is `[1001, 3001, 5001]`. Rank is different on purpose so the door and the contest stay separate.

### API

- `rank(card_id)` → full record (`candidate_group_ids`, `scored`, `final_rank_order`, `selected_group_id`).
- `run(card_id)` prints the lesson and returns `final_rank_order` as a list (Slide 07 still consumes that list).

Changing weights or the toy table is a **named revision**, not a silent retune of cognition.

## What ranking is

The map opened some doors. Ranking picks **which door is tried first**.

It is not:
- a new geometry
- a manifold neighborhood
- permission to add a group the map did not name
- CIE (`M' = M + \alpha I` is Slide 05)
- freeze on `meaning_delta_h` (Slide 06)
- Path A routing to IdOB (SOB → SROB → CnOB → SmOB still builds the structural packet)

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

## Note — rank leftovers are not RB next (Slide 10)

Ids after rank-1 are still **this card's** legal set. They are not Path A `firing_order`. Next IdOB / leftover expansion is [../10_residue_expand/residue_expand.md](../10_residue_expand/residue_expand.md).

## Run

    python run_04_rank.py
    python ../run_ts_struc2mn.py   # with RUN_04_RANK = True
