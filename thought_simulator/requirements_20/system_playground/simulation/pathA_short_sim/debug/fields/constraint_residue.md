# constraint_residue
## 1. Definition
`constraint_residue` is the canonical field for unresolved rule-level output from `CnOB`.

## 2. Source Geometry
`constraint_geometry` from [../dimensions/constraint_geometry.md](../dimensions/constraint_geometry.md).

## 3. Primitive That Produces This Field
`CnOB`.

## 4. Structured-World Meaning
This field carries unresolved constraint signals forward to basin stabilization.

## 5. Token-World Intuition
From the token sequence after structural checks, this field contains unresolved items such as interrogative scope or locative adjacency stabilization gaps.

## 6. Example
```text
constraint_residue = ["interrogative_scope", "locative_adjacent"]
```

## 7. Downstream Effects
- Primary upstream input for `SmOB`.
- Affects `semantic_adjacent_cues`, `smoothing_operations`, and `basin_residue`.
- Indirectly affects `IdOB` stability.

## 8. Notes for Debugging
- Non-empty values are expected when some constraints remain unresolved.
- Compare with `constraints_unmatched` for causal traceability.
