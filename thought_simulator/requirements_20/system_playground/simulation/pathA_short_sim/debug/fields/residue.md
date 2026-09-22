# residue
## 1. Definition
`residue` is a compatibility field name for unresolved CnOB output.

## 2. Source Geometry
`constraint_geometry` from [../dimensions/constraint_geometry.md](../dimensions/constraint_geometry.md).

## 3. Primitive That Produces This Field
`CnOB`.

## 4. Structured-World Meaning
This field corresponds to unresolved rule-level output and maps to canonical `constraint_residue` semantics.

## 5. Token-World Intuition
From token-derived structure after constraint evaluation, this field marks unresolved structural checks.

## 6. Example
```text
residue = ["interrogative_scope", "locative_adjacent"]
```

## 7. Downstream Effects
- Same downstream interpretation as `constraint_residue` in compatibility contexts.
- Feeds SmOB stabilization behavior when present.
- Influences final identity stability indirectly through basin processing.

## 8. Notes for Debugging
- Prefer canonical `constraint_residue` for new debug interpretation.
- If both names appear, values should agree semantically.
