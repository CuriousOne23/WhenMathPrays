# Identity Geometry
### *A canonical geometry document for Path-A structured world*

## 1. Purpose of This Geometry
- Identity geometry describes how structured signals are stabilized as a deterministic identity state.
- The simulator needs this geometry to form final identity outputs and packet-level interpretive state.
- Activated by `IdOB`.

## 2. Canonical Definition
Identity geometry is the deterministic integration geometry in `IdOB` that consumes structural and basin outputs and resolves final identity state across `identity_geometry`, `truth_relation`, `semantic_core`, and `idob_packet`.

## 3. Geometry Categories (if applicable)
| Category | Description | Activated By | Produces |
|---|---|---|---|
| referential_identity | Identity resolved by referent-level stabilization. | IdOB | identity_geometry, semantic_core, truth_relation, idob_packet |
| structural_identity | Identity resolved by structural relation stabilization. | IdOB | identity_geometry, semantic_core, truth_relation, idob_packet |
| semantic_identity | Identity resolved by semantic stabilization. | IdOB | identity_geometry, semantic_core, truth_relation, idob_packet |
| packet_identity | Identity resolved at packet-level completion. | IdOB | identity_geometry, semantic_core, truth_relation, idob_packet |

## 4. Structural Function
- Activates final identity confirmation in `IdOB`.
- Interacts with canonical fields: `struct_segments`, `segment_tokens`, `struct_roles`, `constraints_matched`, `constraints_unmatched`, `constraint_residue`, `smoothing_operations`, `semantic_adjacent_cues`, `basin_residue`, `identity_geometry`, `truth_relation`, `semantic_core`, `idob_packet`.
- Its outputs are consumed by downstream identity/routing consumers through `idob_packet`.

## 5. Minimal Example
- Minimal input:
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
```
- Geometry activation:
```text
IdOB activates identity_geometry = referential_identity
```
- Output fields:
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

## 6. Cross-Primitive Interaction
- Activated by primitive: `IdOB`.
- Consumes outputs from primitives: `SOB`, `SROB`, `CnOB`, `SmOB`.
- Canonical field files produced in this flow: `../fields/idob_packet.md` with internal fields `identity_geometry`, `truth_relation`, and `semantic_core`.

## 7. Glossary
- `identity_geometry`: IdOB identity-resolution geometry.
- `truth_relation`: resolved assertion mode for the identity state.
- `semantic_core`: stabilized identity-relevant semantic set.
- `idob_packet`: final canonical identity output bundle.

