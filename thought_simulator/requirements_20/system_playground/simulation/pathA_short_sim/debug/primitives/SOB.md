# SOB
### *A canonical primitive document for Path-A structured world*

## 1. Purpose
`SOB` performs deterministic segmentation of structured input into canonical segment fields.

## 2. Inputs
- Geometry source: `segment_geometry` from `../dimensions/segment_geometry.md`.
- Upstream state: token stream context required for segmentation.

## 3. Outputs
- `struct_segments`
- `segment_tokens`

## 4. Structural Function
`SOB` applies segment geometry categories (`atomic`, `composite`, `recursive`, `discontinuous`) to form canonical segment labels and token-group mappings. This establishes the structural state consumed by all downstream primitives.

## 5. Deterministic Algorithm (Conceptual)
1. Read token stream state.
2. Apply `segment_geometry` rules to identify admissible segment boundaries.
3. Emit canonical segment labels into `struct_segments`.
4. Emit token group mapping into `segment_tokens`.
5. Forward structured state to `SROB`.

## 6. Minimal Example
- input fields:
```text
tokens = ["Where", "is", "the", "book", "on", "the", "table", "?"]
```
- primitive activation:
```text
SOB activates segment_geometry = composite
```
- output fields:
```text
struct_segments = ["WQ", "NP", "LOC"]
segment_tokens = {
  "WQ": ["Where"],
  "NP": ["the", "book"],
  "LOC": ["on", "the", "table"]
}
```

## 7. Cross-Primitive Interaction
- Preceding primitive: none in Path-A pipeline.
- Consuming primitive: `SROB` directly; state also constrains `CnOB`, `SmOB`, and `IdOB` downstream.
- Pipeline position: first stage in `SOB -> SROB -> CnOB -> SmOB -> IdOB`.

## 8. Notes for Debugging
- Typical values: `struct_segments` entries such as `WQ`, `NP`, `LOC`.
- Edge cases: empty segmentation or unmatched segment boundaries.
- Common mistakes: segment labels not aligned with `segment_tokens` keys.
- Validate correctness: confirm one-to-one coverage of grouped tokens by emitted segment labels.
