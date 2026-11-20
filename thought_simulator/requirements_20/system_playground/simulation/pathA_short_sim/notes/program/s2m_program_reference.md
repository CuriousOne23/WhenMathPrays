# S2M Program Reference

**Date:** 2026-11-19
**Branch:** `s2m-seed-experiment`
**Purpose:** Concrete contracts for the two-part S2M realization: (I) accountability trail, (II) interpretive transfer to meaning.
**Status:** Implementation contract for the experimental branch. Not a requirements change.

## Intent

S2M is realized in two separable parts.

- **Part I — Accountability trail**  
  Establishes an inspectable record of what the floor wrote and what remains open. This is the seed already implemented. It does not yet claim interpreted meaning.

- **Part II — Interpretive transfer to meaning**  
  Selects a finite association from a bounded, extensible pool and writes it as a meaning relation against the trail. Meaning appears as that finite, legitimized composite (the customized story).

Both parts run under `python run_examples.py` (enabled by default). Output is clearly labeled so each part can be found in a log file. Disable with `--no-s2m-seed`.

## Non-mutation rule

Do not modify `idob/sum.py`, the core IdOB assignment that writes `tp.idob`, desks, or existing claim/connection writers. All new behavior is additive.

## CLI

```bash
python run_examples.py                  # Part I + Part II enabled
python run_examples.py --no-s2m-seed    # both disabled
python run_examples.py > run.log        # pipeline to log; labels remain findable
```

The primitive that attaches both parts is **IdOB**.

---

# Part I — Accountability trail

## Output label (easily found in log)
```
--- S2M Accountability (IdOB) ---
```

## Accounting output (`tp.s2m_seed`)
- `utterance`: raw sentence
- `written_relations`: relations the floor established  
  Example: `{"from": "sky", "relation": "is", "to": "blue", "source": "floor"}`
- `null_relations`: explicit markers for relations left open  
  Example: `{"from": null, "relation": null, "to": null, "reason": "no_floor_source"}`
- `crossing_fields`: reserved meaning slots, all null  
  (`structure_ids`, `structural_key`, `rank`, `meaning_semantics`, `cie_id`, `meaning_delta_h`)
- `seed_complete`: true

## How it is used
The accountability record is the inspectable starting point. Part II reads it and appends finite meaning relations beside it. It remains visible even if no interpretive selection is made.

## Example (The sky is blue.)
```
--- S2M Accountability (IdOB) ---
s2m_seed: {
  "utterance": "The sky is blue.",
  "written_relations": [{"from": "sky", "relation": "is", "to": "blue", "source": "floor"}],
  "null_relations": [{"from": null, "relation": null, "to": null, "reason": "no_floor_source"}],
  "crossing_fields": {"structure_ids": null, "structural_key": null, "rank": null, "meaning_semantics": null, "cie_id": null, "meaning_delta_h": null},
  "seed_complete": true
}
```

---

# Part II — Interpretive transfer to meaning

## Output label (easily found in log)
```
--- S2M Meaning (IdOB) ---
```

## Meaning output (`tp.s2m_meaning`)
- `meaning_relations`: finite, legitimized associations  
  Example: `{"from": "blue", "relation": "evokes", "to": "cold", "major": "affective", "legitimized": true}`
- `active_space`: majors that were live for this selection
- `story_id`: identifier for the composite
- `extendable`: true

## How it is used
Part II loads only the active majors from YAML, proposes associations for the seed endpoints, legitimates those inside the space of use, and writes the accepted ones as meaning relations. The result is appended to the trail so the customized story is inspectable.

## Data files (YAML)
- `s2m/data/majors.yaml` — open list of classifications
- `s2m/data/associations/<endpoint>.yaml` — tagged associations for each word
- `s2m/data/spaces/default.yaml` — active majors for the default space

New associations or majors are added by editing YAML; Python loop code does not change.

## Example meaning record
```
--- S2M Meaning (IdOB) ---
s2m_meaning: {
  "meaning_relations": [
    {"from": "blue", "relation": "evokes", "to": "cold", "major": "affective", "legitimized": true},
    {"from": "sky", "relation": "affords", "to": "openness", "major": "mental", "legitimized": true}
  ],
  "active_space": ["affective", "perceptual", "mental", "spiritual"],
  "story_id": "sky-blue-001",
  "extendable": true
}
```

## Realized sentences (examples)
1. "The sky is blue." → accountability writes sky–is–blue; meaning may add blue→cold, sky→openness.
2. "The book is on the table." → accountability writes book–is–on–table; meaning may add table→support, book→object.
3. "Where is the book?" → accountability writes query relation; meaning may add book→sought, location→unknown.

## Expandability
- Add a major: one line in `majors.yaml`.
- Add an association: one entry in the endpoint YAML.
- Add a space: new file under `spaces/`.
- The select–legitimate–write loop and both output labels stay unchanged.
- The structure is one workable accounting organization, not claimed to be the only or optimal one. It is sufficient to demonstrate the concept and can be refined or extended without breaking the trail.

## First implementation slice for Part II
- YAML files for sky and blue with the rudimentary associations.
- Loader, active-space, propose, legitimate, write, and record modules.
- Loop called from IdOB when the seed flag is on.
- Clear `--- S2M Meaning (IdOB) ---` block in `run_examples.py` output.

Until Part II is filled, only the Accountability block appears. Both blocks are labeled and pipeline cleanly to a log file.

## Traceability
Linked from the short-sim README and from `s2m_relational_proposal.md`. All work remains on `s2m-seed-experiment`. `main` is the recovery point.

## Commentary of S2M
For commentary on S2M see [observations_of_s2m.md](../../observations_of_s2m.md).
