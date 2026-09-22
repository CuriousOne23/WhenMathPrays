# SROB
### *A canonical primitive document for Path-A structured world*

## 1. Purpose
`SROB` performs deterministic role assignment over segmented structure.

## 2. Inputs
- Geometry source: `role_geometry` from `../dimensions/role_geometry.md`.
- Canonical fields consumed:
- `struct_segments`
- `segment_tokens`

## 3. Outputs
- `struct_roles`

## 4. Structural Function
`SROB` maps segment labels to role values using role geometry categories (`head`, `modifier`, `predicate`, `argument`). This role state is required for deterministic constraint evaluation.

## 5. Deterministic Algorithm (Conceptual)
1. Read `struct_segments` and `segment_tokens`.
2. Apply `role_geometry` mapping rules.
3. Assign canonical role values to each segment.
4. Emit role map in `struct_roles`.
5. Forward role state to `CnOB`.

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
- Typical values: role assignments including `interrogative_head`, `entity`, `locative_modifier`.
- Edge cases: missing role assignment for one or more segments.
- Common mistakes: role keys not matching segment labels.
- Validate correctness: confirm complete role coverage for each segment in `struct_segments`.
