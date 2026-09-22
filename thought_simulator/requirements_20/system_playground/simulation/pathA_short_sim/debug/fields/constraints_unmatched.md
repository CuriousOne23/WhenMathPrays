# constraints_unmatched
## 1. Definition
`constraints_unmatched` is the canonical field that stores constraints not resolved as satisfied.

## 2. Source Geometry
`constraint_geometry` from [../dimensions/constraint_geometry.md](../dimensions/constraint_geometry.md).

## 3. Primitive That Produces This Field
`CnOB`.

## 4. Structured-World Meaning
This field records deterministic rule checks that remained unresolved at the constraint stage.

## 5. Token-World Intuition
From the token sequence after segmentation and role assignment, this field marks unresolved structural checks.

## 6. Example
```text
constraints_unmatched = ["continuity_rule"]
```

## 7. Downstream Effects
- Increases likelihood of non-empty `constraint_residue`.
- Affects `SmOB` smoothing burden and `basin_residue`.
- Can reduce stability of `IdOB` outputs.

## 8. Notes for Debugging
- Review with `constraints_matched` to see full constraint split.
- Persistent unmatched values indicate upstream segmentation/role issues.
