# Structural key (S2M)

How the six structure IDs become one replayable key.  
This is **not** a hash of meaning scores and not `identity_delta`.

## Key

```
SK|{field}|{role}|{object}|{gradient}|{universe}|{subfield}
```

Same six integers → same key. Key ignores `residue_code` and feature tags (those ride beside the key).

Toy implementation: `01_structure/make_structural_key.py`.  
Production hash (if you replace the string key) must be deterministic, collision-aware, and a **named revision**.

## What may mint IDs

- Hand card (01)
- 09 assignment from packs + `primitives/idob/semantic_*.yaml`

## What must not mint IDs

- CIE / stance
- Rank scores
- Δh
- RB routing_filter

## Tests

Two utterances that 09 maps to the same six IDs share a key (same road).  
Two that differ in one ID must not share a key.  
CIE pair: same key before and after modulate.
