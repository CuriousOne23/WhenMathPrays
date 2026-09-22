# CnOB
### *A canonical primitive document for Path-A structured world*

## 1. Purpose
`CnOB` performs deterministic constraint evaluation over segmented and role-assigned structure.

## 2. Inputs
- Geometry source: `constraint_geometry` from `../dimensions/constraint_geometry.md`.
- Canonical fields consumed:
- `struct_segments`
- `struct_roles`

## 3. Outputs
- `constraints_matched`
- `constraints_unmatched`
- `constraint_residue`
- `residue` (compatibility field name)

## 4. Structural Function
`CnOB` evaluates rule categories (`adjacency_rule`, `compatibility_rule`, `structural_rule`, `continuity_rule`) and separates satisfied constraints from unresolved constraints. Unresolved rule-level output is emitted as canonical `constraint_residue`.

## 5. Deterministic Algorithm (Conceptual)
1. Read `struct_segments` and `struct_roles`.
2. Apply `constraint_geometry` rule checks.
3. Emit satisfied rules to `constraints_matched`.
4. Emit unresolved rules to `constraints_unmatched`.
5. Emit unresolved rule-level signals to `constraint_residue` (and compatibility alias `residue`).
6. Forward state to `SmOB`.

## 6. Minimal Example
- input fields:
```text
struct_segments = ["WQ", "NP", "LOC"]
struct_roles = {
  "WQ": "interrogative_head",
  "NP": "entity",
  "LOC": "locative_modifier"
}
```
- primitive activation:
```text
CnOB activates constraint_geometry = adjacency_rule
```
- output fields:
```text
constraints_matched = ["adjacency_rule", "compatibility_rule"]
constraints_unmatched = ["continuity_rule"]
constraint_residue = ["interrogative_scope", "locative_adjacent"]
residue = ["interrogative_scope", "locative_adjacent"]
```

## 7. Cross-Primitive Interaction
- Preceding primitive: `SROB`.
- Consuming primitive: `SmOB`; outputs influence `IdOB` through basin stabilization.
- Pipeline position: third stage in `SOB -> SROB -> CnOB -> SmOB -> IdOB`.

## 8. Notes for Debugging
- Typical values: rule names in matched/unmatched sets and adjacency-oriented residue entries.
- Edge cases: all rules unmatched or empty rule sets.
- Common mistakes: using non-canonical residue naming instead of `constraint_residue`.
- Validate correctness: check matched/unmatched split consistency and residue alignment with unresolved rules.
