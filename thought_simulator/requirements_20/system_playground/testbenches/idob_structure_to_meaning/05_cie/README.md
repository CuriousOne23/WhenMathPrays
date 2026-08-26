# Slide 05 — Conversational Identity Envelope

## Objective

Feel identity as a local pressure on M, not as a new structure key and not as a life-story.

CIE in this bench:
- identity_tags
- identity_vector (aligned to the six fields, for this slide)
- identity_importance (alpha)

The only score formula specified in the IdOB papers and used here:

    M' = M + alpha * I

Clip to [0, 1] if you implement that; say so in the log.

## This slide must do

- Hold M fixed (copy a group prototype).
- Swap envelopes.
- Print M vs M'.

## This slide must not do

- Change structural_key when CIE changes.
- Run the cycle loop (slide 06).

## Boundary to feel

Same structure + different CIE -> different M', same candidates.
If CIE changes the key, identity leaked into structure.

## Run (when implemented)

    python run_05_modulate.py
