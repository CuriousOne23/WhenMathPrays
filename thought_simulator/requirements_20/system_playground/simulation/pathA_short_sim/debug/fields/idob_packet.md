# idob_packet
## 1. Definition
`idob_packet` is the canonical final identity bundle emitted by `IdOB`.

## 2. Source Geometry
`identity_geometry`, `semantic_core`, and `truth_relation` from:
- [../dimensions/identity_geometry.md](../dimensions/identity_geometry.md)
- [../dimensions/semantic_core.md](../dimensions/semantic_core.md)
- [../dimensions/truth_relation.md](../dimensions/truth_relation.md)

## 3. Primitive That Produces This Field
`IdOB`.

## 4. Structured-World Meaning
This field packages stabilized identity outputs, including identity type, truth mode, and semantic core state.

## 5. Token-World Intuition
From token-derived structured processing, this field is the final deterministic representation of utterance identity state.

## 6. Example
```text
idob_packet = {
  "identity_geometry": "referential_identity",
  "truth_relation": "interrogative",
  "semantic_core": ["entity", "locative_modifier"]
}
```

## 7. Downstream Effects
- Provides final identity output for downstream routing/consumption.
- Encodes stabilized results from all prior primitives.
- Serves as the terminal debug artifact for identity state.

## 8. Notes for Debugging
- Verify internal consistency between identity type, truth relation, and semantic core.
- Instability usually traces to upstream constraint or basin fields.
