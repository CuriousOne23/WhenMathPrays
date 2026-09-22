# smob_smoothing_residue
## 1. Definition
`smob_smoothing_residue` is a compatibility field name for unresolved SmOB output.

## 2. Source Geometry
`semantic_core` geometry context from [../dimensions/semantic_core.md](../dimensions/semantic_core.md).

## 3. Primitive That Produces This Field
`SmOB`.

## 4. Structured-World Meaning
This field corresponds to unresolved basin-stage output and maps to canonical `basin_residue` semantics.

## 5. Token-World Intuition
From token-derived structure, this field indicates leftover stabilization gaps after smoothing.

## 6. Example
```text
smob_smoothing_residue = []
```

## 7. Downstream Effects
- Same downstream interpretation as `basin_residue` in compatibility contexts.
- Affects `IdOB` stabilization when non-empty.
- Should be reconciled with canonical basin output during debug review.

## 8. Notes for Debugging
- Prefer canonical `basin_residue` for new debug interpretation.
- If both names appear, values should agree semantically.
