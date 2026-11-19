# S2M Program Reference

**Date:** 2026-11-19
**Branch:** `s2m-seed-experiment`
**Purpose:** Together with `s2m_relational_proposal.md`, this document supplies the concrete contracts an AI needs to implement the seed without destroying existing short-sim behavior.
**Status:** Implementation contract for the experimental branch. Not a requirements change.

## Non-mutation rule

Do not modify:
- `idob/sum.py`
- `primitives_pathA_short.py` (the IdOB call that does `tp.idob = packet`)
- existing claim ledger or connection writers
- any desk (`desks/`)
- existing tests or replays

All new code is additive and optional. The original teaching packet written to `tp.idob` must remain byte-for-byte identical when the seed is not requested.

## Attachment point

After the existing line in `primitives_pathA_short.py`:

```python
packet = sum_idob(tp, registry)
tp.idob = packet
```

add an optional call that does **not** replace `tp.idob`:

```python
if getattr(tp, "enable_s2m_seed", False):
    from idob.experimental_seed import apply_seed
    tp.s2m_seed = apply_seed(tp, packet)
```

The seed lives in a new attribute `tp.s2m_seed`. It never overwrites `tp.idob`.

## Data shapes

### Existing teaching packet (`tp.idob`)
Dict produced by `sum_idob`. Key fields used by the seed:
- `semantic_core`: dict
- `selected_ops`: list
- `truth_relation`: str
- `identity_geometry`: str
- `contributors`, `claimed_fields`, etc.

Crossing fields (six IDs, rank, M, CIE, `meaning_delta_h`) are absent from this packet. They are not zero; they are missing.

### Seed view (`tp.s2m_seed`)
New dict. Must contain:

```python
{
    "utterance": str,                    # tp.raw_text
    "written_relations": [               # only relations the floor established
        {
            "from": str,                 # endpoint, e.g. "sky"
            "relation": str,             # e.g. "is"
            "to": str,                   # e.g. "blue"
            "source": "floor"            # always "floor" for the seed
        }
    ],
    "null_relations": [                  # explicit markers, not missing keys
        {
            "from": str | None,
            "relation": str | None,
            "to": str | None,
            "reason": "unlegitimized"    # or "no_floor_source"
        }
    ],
    "crossing_fields": {                 # all None
        "structure_ids": None,
        "structural_key": None,
        "rank": None,
        "meaning_semantics": None,
        "cie_id": None,
        "meaning_delta_h": None
    },
    "seed_complete": True
}
```

Null markers must be present as list entries or dict values set to `None`. Absence of a key is not a null.

## First seed implementation (`idob/experimental_seed.py`)

```python
from typing import Any, Dict, List

def apply_seed(tp: Any, packet: Dict[str, Any]) -> Dict[str, Any]:
    """Additive seed. Does not mutate packet or tp.idob."""
    utterance = getattr(tp, "raw_text", "") or ""
    # Hard-coded first case for visibility. Later replace with floor extraction.
    written = []
    if "sky" in utterance.lower() and "blue" in utterance.lower():
        written.append({
            "from": "sky",
            "relation": "is",
            "to": "blue",
            "source": "floor"
        })

    nulls = [
        {"from": None, "relation": None, "to": None, "reason": "no_floor_source"}
    ]

    return {
        "utterance": utterance,
        "written_relations": written,
        "null_relations": nulls,
        "crossing_fields": {
            "structure_ids": None,
            "structural_key": None,
            "rank": None,
            "meaning_semantics": None,
            "cie_id": None,
            "meaning_delta_h": None
        },
        "seed_complete": True
    }
```

## Replay (`support/tools/seed_replay.py`)

Must:
1. Construct a TP with `raw_text = "The sky is blue."`
2. Run the normal floor + IdOB so `tp.idob` is populated exactly as today.
3. Set `tp.enable_s2m_seed = True` and call the optional path.
4. Assert `tp.idob` is unchanged from a control run without the flag.
5. Print `tp.s2m_seed` showing the one written relation and the null markers.
6. Exit 0 on success.

## Category stores (stubs only for first slice)

Create `stores/` with one file per category. Each exports:

```python
def propose(active_context: Dict[str, Any]) -> List[Dict[str, Any]]:
    return []  # empty until trained
```

The runtime loop (`mapping/loop.py`) may call them but must tolerate empty returns. No store is required to function for the first seed to be correct.

## What “correct” means for the first commit

- Existing `run_examples.py` and claim-ledger replay still pass with no flag set.
- `seed_replay.py` prints a seed containing exactly one written relation for “The sky is blue.” and explicit nulls for everything else.
- `tp.idob` is identical whether the seed flag is on or off.
- No new import errors on the normal path.

## Later slices (not required for first correctness)

- Replace the hard-coded relation with extraction from floor fields (`struct_segments`, roles, constraints).
- Implement `mapping/activate.py`, `deviate.py`, `legitimate.py`.
- Fill category stores.
- Add audit.

Until those exist, the seed view is the only required new behavior.

## Traceability

Linked from `s2m_relational_proposal.md`. All work stays on branch `s2m-seed-experiment`. `main` is the recovery point.
