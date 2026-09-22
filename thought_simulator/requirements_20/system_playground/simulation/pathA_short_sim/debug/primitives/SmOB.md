# SmOB
### *A canonical primitive document for Path-A structured world*

## 1. Purpose
`SmOB` performs deterministic basin stabilization over unresolved constraint-stage output.

## 2. Inputs
- Geometry source: semantic-core stabilization context from `../dimensions/semantic_core.md`.
- Canonical fields consumed:
- `constraint_residue`
- `constraints_matched`
- `constraints_unmatched`

## 3. Outputs
- `smoothing_operations`
- `semantic_adjacent_cues`
- `basin_residue`
- `smob_smoothing_residue` (compatibility field name)

## 4. Structural Function
`SmOB` applies named smoothing operations to unresolved constraint signals and emits stabilized semantic-adjacent cues plus unresolved basin output. This stage prepares deterministic identity input.

## 5. Deterministic Algorithm (Conceptual)
1. Read `constraint_residue` and related constraint state.
2. Select required smoothing operations.
3. Apply smoothing to unresolved signals.
4. Emit stabilized cues in `semantic_adjacent_cues`.
5. Emit operation list in `smoothing_operations`.
6. Emit unresolved basin output in `basin_residue` (and compatibility alias `smob_smoothing_residue`).
7. Forward stabilized state to `IdOB`.

## 6. Minimal Example
- input fields:
```text
constraint_residue = ["interrogative_scope", "locative_adjacent"]
constraints_matched = ["adjacency_rule", "compatibility_rule"]
constraints_unmatched = ["continuity_rule"]
```
- primitive activation:
```text
SmOB applies smoothing operations
```
- output fields:
```text
smoothing_operations = ["adjacency_smoothing"]
semantic_adjacent_cues = ["interrogative_scope", "locative_adjacent"]
basin_residue = []
smob_smoothing_residue = []
```

## 7. Cross-Primitive Interaction
- Preceding primitive: `CnOB`.
- Consuming primitive: `IdOB`.
- Pipeline position: fourth stage in `SOB -> SROB -> CnOB -> SmOB -> IdOB`.

## 8. Notes for Debugging
- Typical values: adjacency-focused cue lists and explicit smoothing operation names.
- Edge cases: non-empty `basin_residue` after smoothing.
- Common mistakes: treating SmOB output as final identity output.
- Validate correctness: confirm cues and basin residue are coherent with incoming `constraint_residue`.
