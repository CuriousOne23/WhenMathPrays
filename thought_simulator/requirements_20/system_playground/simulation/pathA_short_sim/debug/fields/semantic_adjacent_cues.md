# semantic_adjacent_cues
## 1. Definition
`semantic_adjacent_cues` is the canonical field that stores stabilized adjacency cues used before identity resolution.

## 2. Source Geometry
`semantic_core` geometry context from [../dimensions/semantic_core.md](../dimensions/semantic_core.md).

## 3. Primitive That Produces This Field
`SmOB`.

## 4. Structured-World Meaning
This field carries deterministic adjacency cues extracted and stabilized from constraint-stage outputs.

## 5. Token-World Intuition
From token-derived structure, this field captures adjacency signals such as interrogative scope and locative adjacency after smoothing.

## 6. Example
```text
semantic_adjacent_cues = ["interrogative_scope", "locative_adjacent"]
```

## 7. Downstream Effects
- Feeds `IdOB` semantic stabilization.
- Interacts with `smoothing_operations` and `basin_residue`.
- Influences `truth_relation` and `semantic_core` formation in `idob_packet`.

## 8. Notes for Debugging
- Verify cues are coherent with `constraint_residue`.
- Sudden cue drift usually indicates upstream role/constraint changes.
