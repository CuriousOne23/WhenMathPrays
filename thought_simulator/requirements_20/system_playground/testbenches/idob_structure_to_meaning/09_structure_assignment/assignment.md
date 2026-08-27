# Structure assignment — algorithm, schema, expand, tests

**Status:** First revision. Lookup + miss. Not a parser. Not English.
**Slide:** 09_structure_assignment
**Interface into Path A:** utterance + loaded packs → structure card | unassigned

## Why this exists

Slide 01 inspects a card someone already filled. This slide is how a line **becomes** a card. The goal on the horizon is talk-shape coverage of English **by packs on disk**, working set in RAM. This revision only seeds the four toy lines.

Assignment is a separate science. IdOB does not implement it. IdOB consumes six IDs.

## Algorithm (this revision)

1. Normalize: lowercase, collapse whitespace, keep letters/digits/spaces.
2. Load **only** packs named in `packs_loaded` (disk library may hold more).
3. Sort packs by `precedence` (higher wins on collision).
4. **Templates first.** Longest matching `phrase` that fills all six IDs wins among templates.
5. **Slot cues** fill any still-empty slot. Longest phrase per slot. On two cues same length, higher pack precedence; if still tied → `collisions` log, do not invent a third ID.
6. If all six IDs present → `assigned`. If some but not all → `partial` (residue may record the gap). If none → `unassigned` (no key).
7. Dumb hasher: `make_structural_key` / `toy_structural_key` on the six IDs only.
8. Stop. No map, no rank, no CIE, no six-floats, no recursive residue search.

## Schema

See `assignment.schema.yaml`.

Card out (when not unassigned):

- six official structure IDs
- optional `residue_code`, `feature_tags`
- `packs_loaded` (replay)
- `assignment_status`: assigned | partial | unassigned
- `collisions`: list (may be empty)
- `structural_key` only if assigned or partial (six IDs present for partial? **No** — key only when all six IDs present)

Horizon (not coded): pack files on SSD, trigger table or COB chooses `packs_loaded`. Collision and miss rules stay.

## How to expand

- Add a phrase to `packs/base_en.yaml`.
- Add `packs/pack_<name>.yaml` and put its `pack_id` on `packs_loaded` for a run.
- Do not add a seventh structure slot without a named instrument revision.
- Do not put meaning axis names in a cue.
- After expand, run the tests below. If an old fixture key changes, that recut must be intentional and logged.

## Do

- Keep cues meaning-blind (talk-shape only).
- Keep miss visible.
- Log packs on the packet.
- Grow from utterances you actually run.
- Treat assignment failures as assigner science, not IdOB failure.

## Don't

- Invent an ID for an unknown phrase.
- Write physicality (or any meaning float).
- Load every pack into RAM because the library is large.
- Put triggers inside the hasher.
- Let 09 “improve” Slide 01 cards by meaning.
- Treat residue as a search that picks meaning groups (that is still open at Slide 03).

## Tests that expansion is still correct

| Test | Expect |
|------|--------|
| Replay | Same utterance + same packs → same six IDs + same key |
| Toy rock | "The rock burst open." + base_en → IDs of S_rock_burst |
| Toy deadline | "The project deadline is Friday." → IDs of S_deadline_friday |
| Toy sleepy | line containing sleepy → IDs of S_sleepy |
| Miss | "zzzzq no cue" → unassigned, no key |
| Disk but unloaded | geology pack on disk, not in packs_loaded; "the ore melted" → miss |
| Collision | two loaded packs, same phrase, different object_id → collision logged; precedence wins; no third ID |
| Meaning-blind | output has no physicality…spatiality fields |
| Fixture stability | new alias in base_en does not change old fixture keys unless the alias was meant to recut them |

Failed test → fix the pack or declare a named assignment revision. Do not patch IdOB.
