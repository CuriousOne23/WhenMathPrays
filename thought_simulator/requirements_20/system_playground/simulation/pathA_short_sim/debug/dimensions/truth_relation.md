# Truth Relation Geometry
### *A canonical geometry document for Path-A structured world*

## 1. Purpose of This Geometry
- Truth relation geometry describes deterministic assertion-mode resolution at IdOB.
- The simulator needs this geometry to finalize interpretive mode in the identity output.
- Activated by `IdOB`.

## 2. Canonical Definition
Truth relation geometry is the deterministic IdOB geometry that resolves utterance truth mode from stabilized structural and basin inputs. It is represented as `truth_relation` and is included in `idob_packet`.

## 3. Geometry Categories (if applicable)
| Category | Description | Activated By | Produces |
|---|---|---|---|
| interrogative | Question-mode truth relation. | IdOB | truth_relation, idob_packet |
| declarative | Statement-mode truth relation. | IdOB | truth_relation, idob_packet |
| unknown | Unresolved truth relation mode when stabilization is incomplete. | IdOB | truth_relation, idob_packet |

## 4. Structural Function
- Resolves final truth mode from stabilized upstream outputs.
- Interacts with canonical fields: `struct_segments`, `struct_roles`, `constraints_matched`, `constraints_unmatched`, `constraint_residue`, `smoothing_operations`, `semantic_adjacent_cues`, `basin_residue`, `truth_relation`, `idob_packet`.
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
IdOB activates truth_relation geometry
```
- Output fields:
```text
truth_relation = "interrogative"
idob_packet = {
	"identity_geometry": "referential_identity",
	"truth_relation": "interrogative",
	"semantic_core": ["entity", "locative_modifier"]
}
```

## 6. Cross-Primitive Interaction
- Activated by primitive: `IdOB`.
- Consumes outputs from primitives: `SOB`, `SROB`, `CnOB`, `SmOB`.
- Canonical field files produced in this flow: `../fields/idob_packet.md` containing `truth_relation`.

## 7. Glossary
- `truth_relation`: deterministic IdOB truth mode.
- `interrogative`: truth mode for question structure.
- `declarative`: truth mode for statement structure.
- `idob_packet`: final packet containing truth_relation.
