# IdOB upstream relationships (S2M / 11)

What must exist **before** `idob.py` can run a hop.  
IdOB does not invent six IDs from Path A routing fields. It does not write `routing_filter`.

---

## 1. Direct inputs to the hop

| Source | Gives IdOB | If missing |
|--------|------------|------------|
| Caller / TP | `utterance` and/or `card_id` | Miss unless a card is supplied |
| 09 packs + `assign.py` | Six IDs + key, or miss | `unassigned`; utterance still stored |
| 01 structure card | Same six IDs when `card_id` is used | Unknown card → unassigned |
| 02 meaning_groups | Prototypes for legal `group_id`s | Rank cannot birth \(M\) |
| 03 map | Legal candidate set for this key | Empty map → no birth |
| 04 ranking | Order among **legal** ids only | First legal / documented fallback |
| 05 CIE | `cie_id` → \(I\), \(\alpha\) | Default `neutral` |
| Prior packet / kwargs | `prior_M` | First-pass zeros |
| TP `process.routing_filter` | Pass-through only | Must be unchanged after process |

---

## 2. Structure primitives (IDs, not meaning scores)

These feed **09** and the six fields on the card. They do not feed \(M\) directly.

| Primitive | Field |
|-----------|--------|
| SOB | `semantic_object_id` / object geometry the object slot can name |
| SROB | leftovers that may become `residue_code` |
| CnOB | continuity cues that 09 may encode in role/gradient |
| SmOB | semantic field / subfield inventory |

Dictionaries: `primitives/idob/semantic_*.yaml`. See handbook.

---

## 3. Routing chain (not IdOB inputs)

`InB … RB → TR → CTP → RTU → IdOB` is Path A **order**.  
RB decides *that* IdOB runs and *which* TP. TR/CTP/RTU may wrap the TP.  
Those modules must **not** be read as meaning axes. After the hop, **RB** reads residue + flags to choose the next IdOB, if any.

DCB `geometric_state` is owned by DCB. IdOB must not write it.

---

## 4. Missing upstream

| Gap | Hop behavior |
|-----|----------------|
| No utterance and no card | Unassigned / refuse birth |
| 09 miss | Unassigned; record utterance |
| Empty map | `empty_map`; no \(M\) |
| Missing group prototype | Cannot birth; treat as map hole |
| Missing CIE row | Use `neutral` or refuse CIE |
| Broken YAML | Load error (revision problem) |

No “identity collapse freeze” from this hop. That language is lifecycle (`lifecycle/`).
