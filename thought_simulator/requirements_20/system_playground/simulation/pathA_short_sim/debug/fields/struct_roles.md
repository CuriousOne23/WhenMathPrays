# struct_roles
## 1. Definition
`struct_roles` is the canonical field that stores role assignments for segmented structure.

## 2. Source Geometry
`role_geometry` from [../dimensions/role_geometry.md](../dimensions/role_geometry.md).

## 3. Primitive That Produces This Field
`SROB`.

## 4. Structured-World Meaning
This field maps segment labels to functional roles used by constraint, basin, and identity stages.

## 5. Token-World Intuition
After segmentation, this field expresses which grouped span acts as question head, entity, or modifier.

## 6. Example
```text
struct_roles = {
  "WQ": "interrogative_head",
  "NP": "entity",
  "LOC": "locative_modifier"
}
```

## 7. Downstream Effects
- Direct input to `CnOB` for constraint evaluation.
- Affects `SmOB` semantic adjacency stabilization.
- Affects `IdOB` outputs via upstream role structure.

## 8. Notes for Debugging
- Verify role keys correspond to `struct_segments`.
- Missing role assignments reduce `CnOB` match quality.
