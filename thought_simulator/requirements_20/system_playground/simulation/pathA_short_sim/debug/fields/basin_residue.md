# basin_residue
## 1. Definition
`basin_residue` is the canonical field for unresolved basin-stage output after SmOB stabilization.

## 2. Source Geometry
`semantic_core` geometry context from [../dimensions/semantic_core.md](../dimensions/semantic_core.md).

## 3. Primitive That Produces This Field
`SmOB`.

## 4. Structured-World Meaning
This field records what remains unresolved after smoothing operations and cue stabilization.

## 5. Token-World Intuition
From token-derived structure, this field marks leftover adjacency-related instability after smoothing.

## 6. Example
```text
basin_residue = []
```

## 7. Downstream Effects
- Directly affects confidence of `IdOB` stabilization.
- Non-empty values can weaken `semantic_core` and `truth_relation` stability.
- Reflected in final `idob_packet` quality.

## 8. Notes for Debugging
- Empty residue indicates successful SmOB stabilization for the current pass.
- Non-empty residue should be reviewed with `smoothing_operations` and `semantic_adjacent_cues`.
