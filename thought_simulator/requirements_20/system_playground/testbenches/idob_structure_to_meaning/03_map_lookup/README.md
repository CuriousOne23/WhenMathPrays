# Slide 03 — Structure bounds meaning (lookup)

**Theory:** [../papers/idob_s2m_theory.md](../papers/idob_s2m_theory.md) §2.3, §2.6  
**Construct:** C5 in [../papers/idob_s2m_constructs.md](../papers/idob_s2m_constructs.md)  
**Next:** [../04_ranking/README.md](../04_ranking/README.md)

## Objective (unchanged)

Feel the bound: structure does not score meaning; it restricts the candidate set.

    structural_key  (or card_id in this slide)  ->  candidate group_ids

That is the whole slide.

## What the map is

The map is the **door between the two geometries**. It is not a third geometry.

- Structure already placed you on a road (six IDs → key / card).
- Meaning will be a point M in six-weight space.
- The map only answers: **from this road-place, which births are legal to attempt?**

Feel:

| Picture | Map does |
|---------|----------|
| Roads vs object | Names which **exits** off this road may lead to a thought-object |
| Birth | Which prototypes are **allowed to be born** from this talk-shape |
| Filter, not judge | "These groups may compete." Not "this *is* the meaning." |

Empty list is a real answer. `S_unmapped` → `[]`. Structure succeeded. Meaning has not been instantiated. Not "cognition failed."

## Why it is needed

Without a map, either:

- every meaning group is legal after every key (structure does no bounding), or
- structure would have to *be* meaning (names trade places).

IdOB must not invent a group the map forbade. The map is how that law is visible.

## How it will be used

1. Slide 01 produces a card / key.
2. Slide 03 looks up `meaning_group_candidates`.
3. Slide 04 ranks **only** those ids.
4. Rank-1 group's prototype becomes first M (Slide 02 / 05).
5. CIE may move M; the map row and the key stay put.

This revision keys the YAML by `card_id` so the slide can run before live hashing. The theory key remains `structural_key → group_ids`.

## Order on the map list means nothing

`meaning_group_candidates: [1001, 3001, 5001]` is a **set** written as a list.

- First on the map line is **not** the winner.
- Id numbers are **names**, not coordinates. 3001 is not "between" 1001 and 5001.
- No smoothness, geodesic, or manifold neighborhood is implied.

If YAML spelling order starts to mean rank, this slide has stolen Slide 04.

## This revision's rows (teaching assignment, not a field)

| Card | Legal groups | Feel |
|------|----------------|------|
| S_rock_burst | 1001, 3001, 5001 | Several exits. Structure is a **filter**. Rank works later. |
| S_deadline_friday | 3001 | One exit. Structure is almost a **dictator**. |
| S_sleepy | 4001 | Different road, different birth. |
| S_unmapped | [] | Road exists. **No birth.** |

3001 can sit on two roads (rock and deadline). Same prototype, different admissibility neighborhoods. That is map work — not structure scoring M, not group_id placement on a manifold.

Hand assignment: stipulated legality. **Arbitrary with respect to smoothness.** Not random nonsense; not geometrically forced.

## This slide must print

- Input card_id / structural_key
- candidate_group_ids
- empty map if none

## This slide must not print

- Rank order (slide 04)
- Six-float modulation
- meaning_delta_h
- A claim that group_id digits are positions

## Boundary to feel

- Thin map → structure looks like a dictator (few candidates).
- Dense map → structure is a filter.
- Empty map → no legal meaning yet (machine halt later, not cognition failed).
- Shared group across cards → roads can share a prototype.
- Disjoint groups → structure split meaning-space before rank.

## Geometry word (descriptive)

"Geometry" here is working language for two representation spaces. It is not charts, curvature, or Newton. A manifold description of groups may be **investigated later** if traces show associations (co-legal nearby keys, near prototypes, smooth rank under small talk-shape change). Declaring one now is wearing that coat early.

## Note — next IdOB vs this door (Slide 10)

This map is legality **for this key only**. An empty map or a leftover `residue_code` does **not** fill the next six-tuple. That recipe is [../10_residue_expand/residue_expand.md](../10_residue_expand/residue_expand.md): a human expands 03 (or 02/09/10), Path A RB is not this slide.

## Run

    python run_03_lookup.py

Exercises: [exercises.md](exercises.md)
