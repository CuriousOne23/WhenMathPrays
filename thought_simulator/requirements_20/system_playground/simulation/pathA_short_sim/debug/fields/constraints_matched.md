# constraints_matched
## 1. Definition
`constraints_matched` is the canonical field that stores constraints resolved as satisfied.

## 2. Source Geometry
`constraint_geometry` from [../dimensions/constraint_geometry.md](../dimensions/constraint_geometry.md).

## 3. Primitive That Produces This Field
`CnOB`.

## 4. Structured-World Meaning
This field records deterministic success of rule checks such as `adjacency_rule`, `compatibility_rule`, `structural_rule`, and `continuity_rule`.

## 5. Token-World Intuition
From the same token sequence, this field marks which structured checks actually stabilized.

## 6. Example
```text
constraints_matched = ["adjacency_rule", "compatibility_rule"]
```

## 7. Downstream Effects
- Drives how `SmOB` performs `smoothing_operations`.
- Influences `semantic_adjacent_cues` and `basin_residue`.
- Contributes to `IdOB` identity stabilization quality.

## 8. Notes for Debugging
- A low match count usually pairs with non-empty `constraints_unmatched`.
- Validate together with `constraint_residue` for unresolved structure.
