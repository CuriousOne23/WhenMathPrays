# Semantic Core Geometry
### *A canonical geometry document for Path-A structured world*

## 1. Purpose of This Geometry
- Semantic core geometry describes the stabilized identity-relevant semantic structure resolved at IdOB.
- The simulator needs this geometry to expose deterministic semantic stabilization used in final identity output.
- Activated by `IdOB`.

## 2. Canonical Definition
Semantic core geometry is the deterministic IdOB geometry that resolves the stabilized semantic set after segment, role, constraint, and basin processing. It is represented in the canonical `semantic_core` output and included in `idob_packet`.

## 3. Geometry Categories (if applicable)
| Category | Description | Activated By | Produces |
|---|---|---|---|
| not_applicable | No additional semantic_core geometry subtypes are defined in canonical Path-A documents. | IdOB | semantic_core, idob_packet |

## 4. Structural Function
- Resolves stabilized semantic structure after upstream processing.
- Interacts with canonical fields: `struct_segments`, `segment_tokens`, `struct_roles`, `constraints_matched`, `constraints_unmatched`, `constraint_residue`, `smoothing_operations`, `semantic_adjacent_cues`, `basin_residue`, `semantic_core`, `idob_packet`.
- Its outputs are consumed by final identity/routing consumers through `idob_packet`.

## 5. Minimal Example
- Minimal input:
```text
struct_segments = ["WQ", "NP", "LOC"]
struct_roles = {
	"WQ": "interrogative_head",
	"NP": "entity",
	"LOC": "locative_modifier"
}
semantic_adjacent_cues = ["interrogative_scope", "locative_adjacent"]
identity_geometry = "referential_identity"
```
- Geometry activation:
```text
IdOB activates semantic_core geometry during identity stabilization
```
- Output fields:
```text
semantic_core = ["entity", "locative_modifier"]
idob_packet = {
	"identity_geometry": "referential_identity",
	"semantic_core": ["entity", "locative_modifier"]
}
```

## 6. Cross-Primitive Interaction
- Activated by primitive: `IdOB`.
- Consumes outputs from primitives: `SOB`, `SROB`, `CnOB`, `SmOB`.
- Canonical field files produced in this flow: `../fields/idob_packet.md` containing `semantic_core`.

## 7. Glossary
- `semantic_core`: stabilized identity-relevant semantic structure.
- `semantic_adjacent_cues`: SmOB cues that support semantic stabilization.
- `idob_packet`: final packet containing semantic_core.
- `referential_identity`: identity type frequently paired with semantic_core stabilization.
