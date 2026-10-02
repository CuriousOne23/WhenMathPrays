**Official:** Structural Refinement Observation Block (SROB) — 20.40.020. Path-A-short realizes pre-semantic structural labels (`struct_roles`). Not semantic role labeling.

# SROB
### *A canonical primitive document for Path-A structured world*

## 1. Purpose
`SROB` performs deterministic structural-label assignment over segmented structure (pre-semantic; not meaning).

## 2. Inputs
- Geometry source: `role_geometry` from `../dimensions/role_geometry.md`.
- Canonical fields consumed:
- `struct_segments`
- `segment_tokens`

## 3. Outputs
- `struct_roles`

## 4. Structural Function
`SROB` maps segment labels to positional/structural cues using role geometry categories (`head`, `modifier`, `predicate`, `argument`). These labels are required for deterministic constraint evaluation. They are not IdOB meaning.

## 5. Deterministic Algorithm (Conceptual)
1. Read `struct_segments` and `segment_tokens`.
2. Apply `role_geometry` mapping rules.
3. Assign canonical structural labels to each segment.
4. Emit label map in `struct_roles`.
5. Forward state to `CnOB`.

## 6. Minimal Example
- input fields:
```text
struct_segments = ["WQ", "NP", "LOC"]
segment_tokens = {
  "WQ": ["Where"],
  "NP": ["the", "book"],
  "LOC": ["on", "the", "table"]
}
```
[see ../fields/struct_segments.md](../fields/struct_segments.md)

- primitive activation:
```text
SROB activates role_geometry = modifier
```
- output fields:
```text
struct_roles = {
  "WQ": "interrogative_head",
  "NP": "entity",
  "LOC": "locative_modifier"
}
```

## 7. Cross-Primitive Interaction
- Preceding primitive: `SOB`.
- Consuming primitive: `CnOB`; outputs influence `SmOB` and `IdOB` downstream.
- Pipeline position: second stage in `SOB -> SROB -> CnOB -> SmOB -> IdOB`.

## 8. Notes for Debugging
- Typical values: labels including `interrogative_head`, `entity`, `locative_modifier`.
- Edge cases: missing label for one or more segments.
- Common mistakes: treating `struct_roles` as IdOB `semantic_core`.
- Validate correctness: confirm complete label coverage for each segment in `struct_segments`.
