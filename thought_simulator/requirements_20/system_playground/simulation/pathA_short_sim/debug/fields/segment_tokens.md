# segment_tokens
## 1. Definition
`segment_tokens` is the canonical field that stores token groups for each segment label.

## 2. Source Geometry
`segment_geometry` from [../dimensions/segment_geometry.md](../dimensions/segment_geometry.md).

## 3. Primitive That Produces This Field
`SOB`.

## 4. Structured-World Meaning
This field maps each segment in `struct_segments` to the exact token span used by structured processing.

## 5. Token-World Intuition
From the utterance token list, this field preserves which tokens belong to each segment group.

## 6. Example
```text
segment_tokens = {
  "WQ": ["Where"],
  "NP": ["the", "book"],
  "LOC": ["on", "the", "table"]
}
```

## 7. Downstream Effects
- Supports `SROB` role assignment over segmented token groups.
- Supports `CnOB` constraint evaluation against segment-token structure.
- Contributes to `IdOB` stabilization through upstream structure.

## 8. Notes for Debugging
- Keys should match entries in `struct_segments`.
- Empty token spans indicate segmentation failure at `SOB`.
