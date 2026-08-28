# World → TS (intake / encoder) — not IdOB

This note sits under `papers/intake/encoder/` on purpose.  
IdOB does **not** own world-to-TS. The hop reads a **carrier** (`utterance`) and/or a `card_id` after intake and (usually) 09.

## Boundary

| Stage | Owner |
|-------|--------|
| World event → symbols / text | Intake / encoder |
| Text → six structure IDs | 09 + `semantic_*.yaml` + packs |
| IDs → \(M\), Δh, flags | IdOB (`11_idob_core`) |
| Next IdOB | RB |

## What IdOB must not do here

- Invent the utterance from sensors.
- Treat encoder features as meaning axes.
- Write routing or DCB geometry.

If an encoder later emits feature tags, they ride **beside** the structural key (`feature_tags` on a card), not inside \(M\).

The long historical essay that lived at `papers/world_to_ts_process.md` is in git. Recover it only as intake history, not as the IdOB contract.
