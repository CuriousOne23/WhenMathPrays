# Constraint Geometry
### *A canonical geometry document for Path-A structured world*

## 1. Purpose of This Geometry
- Constraint geometry describes rule-level coherence checks across segments and roles.
- The simulator needs this geometry to separate matched constraints from unresolved constraint output before basin processing.
- Activated by `CnOB`.

## 2. Canonical Definition
Constraint geometry is the deterministic structural geometry used by `CnOB` to evaluate structural compatibility, adjacency, and continuity across `struct_segments` and `struct_roles`. It emits matched constraints, unmatched constraints, and `constraint_residue`.

## 3. Geometry Categories (if applicable)
| Category | Description | Activated By | Produces |
|---|---|---|---|
| adjacency_rule | Checks required adjacency relations. | CnOB | constraints_matched, constraints_unmatched, constraint_residue |
| compatibility_rule | Checks role and segment compatibility. | CnOB | constraints_matched, constraints_unmatched, constraint_residue |
| structural_rule | Checks structural organization requirements. | CnOB | constraints_matched, constraints_unmatched, constraint_residue |
| continuity_rule | Checks continuity across linked structure. | CnOB | constraints_matched, constraints_unmatched, constraint_residue |

## 4. Structural Function
- Governs deterministic constraint satisfaction in `CnOB`.
- Interacts with canonical fields: `struct_segments`, `struct_roles`, `constraints_matched`, `constraints_unmatched`, `constraint_residue`.
- Its outputs are consumed by `SmOB` for `semantic_adjacent_cues`, `smoothing_operations`, and `basin_residue`, then by `IdOB` for `identity_geometry`, `truth_relation`, `semantic_core`, and `idob_packet`.

## 5. Minimal Example
- Minimal input:
```text
struct_segments = ["WQ", "NP", "LOC"]
struct_roles = {
  "WQ": "interrogative_head",
  "NP": "entity",
  "LOC": "locative_modifier"
}
```
- Geometry activation:
```text
CnOB activates constraint_geometry = adjacency_rule
```
- Output fields:
```text
constraints_matched = ["adjacency_rule", "compatibility_rule"]
constraints_unmatched = ["continuity_rule"]
constraint_residue = ["interrogative_scope", "locative_adjacent"]
semantic_adjacent_cues = ["interrogative_scope", "locative_adjacent"]
identity_geometry = "referential_identity"
```

## 6. Cross-Primitive Interaction
- Activated by primitive: `CnOB`.
- Consumed by primitives: `SmOB`, `IdOB`.
- Canonical field files produced in this flow: `../fields/constraints_matched.md`, `../fields/constraints_unmatched.md`, `../fields/constraint_residue.md`, `../fields/smoothing_operations.md`, `../fields/semantic_adjacent_cues.md`, `../fields/basin_residue.md`, `../fields/idob_packet.md`.

## 7. Glossary
- `constraint_geometry`: rule geometry evaluated by `CnOB`.
- `constraints_matched`: constraints resolved as satisfied.
- `constraints_unmatched`: constraints not resolved as satisfied.
- `constraint_residue`: unresolved rule-level output from `CnOB`.

