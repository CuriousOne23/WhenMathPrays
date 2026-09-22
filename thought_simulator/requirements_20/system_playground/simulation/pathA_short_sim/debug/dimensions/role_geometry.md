# Role Geometry
### *A canonical geometry document for Path-A structured world*

## 1. Purpose of This Geometry
- Role geometry describes how segments are assigned functional roles.
- The simulator needs this geometry to enable deterministic role-to-constraint and role-to-identity propagation.
- Activated by `SROB`.

## 2. Canonical Definition
Role geometry is the deterministic structural geometry used by `SROB` to assign functional roles to segmented units. It maps segment labels to role values and produces `struct_roles` for downstream constraint, basin, and identity processing.

## 3. Geometry Categories (if applicable)
| Category | Description | Activated By | Produces |
|---|---|---|---|
| head | Primary controlling role assignment class. | SROB | struct_roles |
| modifier | Role assignment class for modifying segments. | SROB | struct_roles |
| predicate | Role assignment class for predicate segments. | SROB | struct_roles |
| argument | Role assignment class for argument-bearing segments. | SROB | struct_roles |

## 4. Structural Function
- Determines role pattern activation in `SROB`.
- Interacts with canonical fields: `struct_segments`, `segment_tokens`, `struct_roles`.
- Produces role assignments consumed by `CnOB` (`constraints_matched`, `constraints_unmatched`, `constraint_residue`), then by `SmOB` (`semantic_adjacent_cues`, `smoothing_operations`, `basin_residue`), then by `IdOB` (`identity_geometry`, `truth_relation`, `semantic_core`, `idob_packet`).

## 5. Minimal Example
- Minimal input:
```text
struct_segments = ["WQ", "NP", "LOC"]
segment_tokens = {
  "WQ": ["Where"],
  "NP": ["the", "book"],
  "LOC": ["on", "the", "table"]
}
```
- Geometry activation:
```text
SROB activates role_geometry = modifier
```
- Output fields:
```text
struct_roles = {
  "WQ": "interrogative_head",
  "NP": "entity",
  "LOC": "locative_modifier"
}
semantic_adjacent_cues = ["interrogative_scope", "locative_adjacent"]
identity_geometry = "referential_identity"
```

## 6. Cross-Primitive Interaction
- Activated by primitive: `SROB`.
- Consumed by primitives: `CnOB`, `SmOB`, `IdOB`.
- Canonical field files produced in this flow: `../fields/struct_roles.md`, `../fields/constraints_matched.md`, `../fields/constraints_unmatched.md`, `../fields/constraint_residue.md`, `../fields/smoothing_operations.md`, `../fields/semantic_adjacent_cues.md`, `../fields/basin_residue.md`, `../fields/idob_packet.md`.

## 7. Glossary
- `role_geometry`: structural geometry for role assignment.
- `struct_roles`: canonical role map output by `SROB`.
- `interrogative_head`: role value used for a question head segment.
- `locative_modifier`: role value used for location-modifier segments.

