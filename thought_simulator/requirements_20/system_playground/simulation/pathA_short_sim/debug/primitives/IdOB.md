# IdOB
### *A canonical primitive document for Path-A structured world*

## 1. Purpose
`IdOB` performs deterministic identity stabilization and emits the final Path-A identity packet.

## 2. Inputs
- Geometry sources:
- `identity_geometry` from `../dimensions/identity_geometry.md`
- `semantic_core` from `../dimensions/semantic_core.md`
- `truth_relation` from `../dimensions/truth_relation.md`
- Canonical fields consumed:
- `struct_segments`
- `segment_tokens`
- `struct_roles`
- `constraints_matched`
- `constraints_unmatched`
- `constraint_residue`
- `smoothing_operations`
- `semantic_adjacent_cues`
- `basin_residue`

## 3. Outputs
- `idob_packet`
- `identity_geometry`
- `truth_relation`
- `semantic_core`

## 4. Structural Function
`IdOB` integrates upstream structured, constraint, and basin state to resolve identity type, truth relation, and stabilized semantic core. It emits a deterministic packet representing final identity state.

## 5. Deterministic Algorithm (Conceptual)
1. Read upstream canonical structural fields.
2. Evaluate identity stabilization conditions.
3. Resolve identity type (`referential_identity`, `structural_identity`, `semantic_identity`, or `packet_identity`).
4. Resolve `truth_relation` state.
5. Resolve stabilized `semantic_core`.
6. Emit final `idob_packet` containing the resolved identity outputs.

## 6. Minimal Example
- input fields:
```text
struct_segments = ["WQ", "NP", "LOC"]
struct_roles = {
  "WQ": "interrogative_head",
  "NP": "entity",
  "LOC": "locative_modifier"
}
constraints_matched = ["adjacency_rule", "compatibility_rule"]
constraint_residue = ["interrogative_scope", "locative_adjacent"]
semantic_adjacent_cues = ["interrogative_scope", "locative_adjacent"]
basin_residue = []
```
- primitive activation:
```text
IdOB resolves identity stabilization
```
- output fields:
```text
identity_geometry = "referential_identity"
truth_relation = "interrogative"
semantic_core = ["entity", "locative_modifier"]
idob_packet = {
  "identity_geometry": "referential_identity",
  "truth_relation": "interrogative",
  "semantic_core": ["entity", "locative_modifier"]
}
```

## 7. Cross-Primitive Interaction
- Preceding primitive: `SmOB`.
- Consuming primitive: none inside the Path-A primitive chain; this is the terminal primitive output stage.
- Pipeline position: fifth stage in `SOB -> SROB -> CnOB -> SmOB -> IdOB`.

## 8. Notes for Debugging
- Typical values: identity type plus truth relation and semantic core set.
- Edge cases: unresolved identity state with incomplete upstream fields.
- Common mistakes: inconsistent packet values compared to resolved identity outputs.
- Validate correctness: verify internal consistency across `identity_geometry`, `truth_relation`, `semantic_core`, and `idob_packet`.
