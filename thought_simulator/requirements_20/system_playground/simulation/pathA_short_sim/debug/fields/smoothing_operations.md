# smoothing_operations
## 1. Definition
`smoothing_operations` is the canonical field that records basin-level operations applied during stabilization.

## 2. Source Geometry
`semantic_core` geometry context from [../dimensions/semantic_core.md](../dimensions/semantic_core.md).

## 3. Primitive That Produces This Field
`SmOB`.

## 4. Structured-World Meaning
This field records deterministic operations used to stabilize semantic-adjacent structure before identity formation.

## 5. Token-World Intuition
From token-derived structure, this field records which smoothing step was needed to stabilize adjacency signals.

## 6. Example
```text
smoothing_operations = ["adjacency_smoothing"]
```

## 7. Downstream Effects
- Works with `semantic_adjacent_cues` to prepare identity input.
- Reduces unresolved basin output in `basin_residue`.
- Supports `IdOB` formation of stable packet outputs.

## 8. Notes for Debugging
- Empty operations with non-empty `constraint_residue` can indicate SmOB execution gaps.
- Validate with `semantic_adjacent_cues` and `basin_residue`.
