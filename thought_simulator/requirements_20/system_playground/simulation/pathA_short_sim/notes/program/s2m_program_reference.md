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

Both parts run under `python run_examples.py` (seed enabled by default). Output is clearly labeled so each part can be found in a log file. Disable the seed with `--no-s2m-seed`.

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

## Output label
```
--- S2M Accountability (IdOB) ---
```

## Contents of the accountability record (`tp.s2m_seed`)
- `utterance`: the raw sentence
- `written_relations`: list of relations the floor established  
  Example: `{