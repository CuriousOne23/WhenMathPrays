# Slide 05 / Stop 5 — Conversational Identity Envelope (CIE)

**Theory:** [../papers/idob_s2m_theory.md](../papers/idob_s2m_theory.md) §2.7
**Construct:** C9 in [../papers/idob_s2m_constructs.md](../papers/idob_s2m_constructs.md)
**Code step:** `modulate.py` — $M' = M + \alpha I$
**Previous:** [../04_ranking/README.md](../04_ranking/README.md)
**Next:** [../06_cycle_and_delta/README.md](../06_cycle_and_delta/README.md)

## Objective

Feel identity as a **local pressure on M**, not as a new structure key and not as a life-story.

CIE in this bench:

- `identity_tags`
- `identity_vector` (aligned to the six fields, for this slide)
- `identity_importance` (alpha)

## Formula implemented this revision

Program: `run_05_modulate.py` + `modulate.py`
Table: `cie.examples.yaml`

    M' = clip_[0,1](M + alpha * I)

Clip is on by default (`clip_to_unit=True`). Neutral envelope has alpha = 0, so M' = M.

CIE does **not** rewrite `structural_key`, does **not** change the map row, and does **not** invent a group.

## Worked group_id=1001 (ACTION.physical.motion)

M = (0.95, 0.10, 0.30, 0.60, 0.20, 0.70) in axis order physicality … spatiality.

| Envelope | alpha | Feel | |M'-M|_2 (clipped) |
|----------|------:|------|------------------:|
| `neutral` | 0.00 | no shove | 0.0000 |
| `physical_stance` | 0.20 | body / impact | ~0.067 (phys clips at 1.0) |
| `scientific_stance` | 0.15 | observation | ~0.044 |

Same group, same (absent) key. Only M moves.

## What CIE is

By Slide 04 you have a first M (prototype through a legal door). CIE asks: **same talk-shape, same legal groups — does how the projection is held move M without rewriting the key?**

| CIE is | CIE is not |
|--------|------------|
| Local stance / hold on the intended projection | Biography, persona, worldview |
| Named envelope + vector I + strength alpha | Listener uptake or mood of the hearer |
| Proof two geometries stayed two (key unchanged) | A new `semantic_field_id` named fear |
| Rank's toy `identity_alignment_score` is a **different** helper | This formula |

## Why IdOB needs it

Without CIE, IdOB freezes the first prototype as if stance never touched the projection. "The rock burst open" as wonder and as lab note would be the same object after birth.

## This slide must print

- Fixed `group_id` and unmoved M
- Each chosen `cie_id`, alpha, I, M', |M'-M|
- `structural_key changed: NO`

## This slide must not print

- Cycle / `resolution_status` (slide 06)
- `final_rank_order` (slide 04)
- A claim that CIE modeled a person's feelings
- A new map candidate

## Run

    python run_05_modulate.py
    python ../run_ts_struc2mn.py   # with RUN_05_CIE = True

Driver vars: `VAR_05_GROUP_ID`, `VAR_05_CIE_ID` (None = all envelopes), `VAR_05_CLIP_TO_UNIT`.
