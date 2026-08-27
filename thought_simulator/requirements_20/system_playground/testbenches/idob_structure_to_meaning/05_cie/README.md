# Slide 05 — Conversational Identity Envelope (CIE)

**Theory:** [../papers/idob_s2m_theory.md](../papers/idob_s2m_theory.md) §2.7  
**Construct:** C9 in [../papers/idob_s2m_constructs.md](../papers/idob_s2m_constructs.md)  
**Code step:** `modulate.py` — `M' = M + alpha * I`

## Objective (unchanged)

Feel identity as a **local pressure on M**, not as a new structure key and not as a life-story.

CIE in this bench:
- `identity_tags`
- `identity_vector` (aligned to the six fields, for this slide)
- `identity_importance` (alpha)

The only score formula specified in the IdOB papers and used here:

    M' = M + alpha * I

Clip to [0, 1] if you implement that; say so in the log.

## What CIE is

By Slide 04 you have a first M (prototype through a legal door). CIE asks: **same talk-shape, same legal groups — does how the projection is held move M without rewriting the key?**

Feel: stance = **from which conversational hold was this projection advanced?** Not: **who is this person?**

It is not a third geometry. It is not the map. It is not rank. It is a shove on the standing object.

| CIE is | CIE is not |
|--------|------------|
| Local stance / hold on the intended projection | Biography, persona, worldview |
| Perspective of the *utterance as put forward* | Optical "where they stood" (that may be spatiality) |
| Named envelope + vector I + strength alpha | Listener uptake or mood of the hearer |
| Proof two geometries stayed two (key unchanged) | A new semantic_field_id named fear |

## Two vocabularies (do not mix silently)

1. **Register / kind-of-talk** (this slide's official envelopes): `physical_stance`, `scientific_stance`, `neutral`. Lab-note vs wonder vs challenge belong here.
2. **Affect-as-pressure** (optional later named envelopes): inquisitive, exasperated, wonder, urgency, desperate. Same family (holds), not the current YAML list. Allowed only as named I / alpha, not as "the speaker is afraid."

## Why IdOB needs it

Without CIE, IdOB freezes the first prototype as if stance never touched the projection. "The rock burst open" as wonder and as lab note would be the same object after birth.

CIE brings:
- Stance can move the stand-in **after** road and door are fixed
- A second motion to log later (`identity_delta`) distinct from talk-shape change
- The test that identity did **not** leak into structure

CIE does not bring: a mind, psycho-analysis, new legal groups, a new key.

## Software architecture

IdOB **orchestrates**. CIE is a **named step it calls**. It does not live in the key builder, the map, or rank (rank may use a toy identity-alignment *score*; that is not this formula).

    idob.py  (or this bench's slide runner)
      structure / key
      map → candidates
      rank → selected group → M0
      modulate.py  → M' = M + α I     # CIE step
      log Δh / status

`idob.py` calling `modulate.py` is the intended shape. `apply_cie` may instead live as a function *inside* the IdOB module if the boundary stays visible: **that function must not change the key.**

If the formula changes (hysteresis, I not six-aligned), that is a **named machine revision**.

## This slide must do

- Hold M fixed (copy a group prototype).
- Swap envelopes.
- Print M vs M'.
- Print the structural_key and show it did not change.

## This slide must not do

- Change structural_key when CIE changes.
- Run the cycle loop (slide 06).
- Invent a group the map forbade.
- Claim it modeled a person's feelings.

## Boundary to feel

Same structure + different CIE → different M', same candidates, **same key**.
If CIE changes the key, identity leaked into structure.
If alpha = 0, M' = M (neutral envelope).

## Examples (same road, different hold)

Utterance: "The rock burst open." Same card / key / legal groups.

| Envelope | Feel of the hold | Typical shove |
|----------|------------------|---------------|
| neutral | just the event | α = 0; M' = M |
| physical_stance | body, impact, stuff coming apart | physicality / materiality up |
| scientific_stance | observation, mechanism | materiality / slight intentionality; sociality down |
| wonder | awe | intensity of presence; not a new key |
| lab_note | dry record | flatten social / affect-like push |
| challenge | "so you claim it burst?" | sociality may rise |
| instruction | "watch how it bursts" | intentionality up |
| inquisitive | "what made it burst?" | purpose-to-know |
| exasperated | "it burst *again*" | hold of fatigue; same object-id |
| intimate | said to someone close | sociality up |

Utterance: "The deadline is Friday."

| Envelope | Hold |
|----------|------|
| neutral | calendar fact |
| urgency / desperate | Friday as threat |
| bureaucratic | schedule language only |
| reproach | "you knew Friday" |
| planning | aimed use of the date |

Only the first three rows of the rock table are implemented in `cie.examples.yaml` this revision. The others are teaching holds for a later named envelope list.

## Run

    python run_05_modulate.py
