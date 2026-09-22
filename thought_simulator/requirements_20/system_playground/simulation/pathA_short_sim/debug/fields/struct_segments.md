# struct_segments
## 1. Definition
`struct_segments` is the canonical field that stores segment labels produced by structured segmentation.

## 2. Source Geometry
`segment_geometry` from [../dimensions/segment_geometry.md](../dimensions/segment_geometry.md).

## 3. Primitive That Produces This Field
`SOB`.

## 4. Structured-World Meaning
This field is the deterministic segment-layer state used by downstream primitives.
Typical values are segment labels such as `WQ`, `NP`, and `LOC`.

## 5. Token-World Intuition
From tokens such as `Where is the book on the table ?`, this field records the grouped segment structure before role assignment.

## 6. Example
```text
struct_segments = ["WQ", "NP", "LOC"]
```

## 7. Downstream Effects
- Consumed by `SROB` to produce `struct_roles`.
- Constrains `CnOB` evaluation for `constraints_matched`, `constraints_unmatched`, and `constraint_residue`.
- Indirectly affects `SmOB` and `IdOB` outputs.

## 8. Notes for Debugging
- If this field is empty, downstream canonical fields are unreliable.
- Verify alignment with `segment_tokens` for the same segment labels.
