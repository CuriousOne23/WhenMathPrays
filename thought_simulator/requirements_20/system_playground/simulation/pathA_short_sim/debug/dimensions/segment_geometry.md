# Segment Geometry
### *A canonical geometry document for Path-A structured world*

## 1. Purpose of This Geometry
- Segment geometry describes how tokens are grouped into stable structural segments.
- The simulator needs this geometry to produce deterministic segmentation before role, constraint, basin, and identity stages.
- Activated by `SOB`.

## 2. Canonical Definition
Segment geometry is the deterministic structural geometry used by `SOB` to map token spans into `struct_segments` and `segment_tokens`. It defines admissible segment forms and provides the segmentation envelope consumed by downstream primitives.

## 3. Geometry Categories (if applicable)
| Category | Description | Activated By | Produces |
|---|---|---|---|
| atomic | Single structural unit segment form. | SOB | struct_segments, segment_tokens |
| composite | Multi-token grouped segment form. | SOB | struct_segments, segment_tokens |
| recursive | Nested segment form. | SOB | struct_segments, segment_tokens |
| discontinuous | Non-contiguous segment form handled structurally. | SOB | struct_segments, segment_tokens |

## 4. Structural Function
- Constrains admissible segment forms during `SOB` evaluation.
- Interacts with canonical fields: `struct_segments`, `segment_tokens`.
- Provides segmentation state consumed by `SROB` (`struct_roles` assignment), `CnOB` (`constraints_matched`, `constraints_unmatched`, `constraint_residue`), `SmOB` (`semantic_adjacent_cues`, `smoothing_operations`, `basin_residue`), and `IdOB` (`identity_geometry`, `truth_relation`, `semantic_core`, `idob_packet`).

## 5. Minimal Example
- Minimal input:
```text
tokens = ["Where", "is", "the", "book", "on", "the", "table", "?"]
```
- Geometry activation:
```text
SOB activates segment_geometry = composite
```
- Output fields:
```text
struct_segments = ["WQ", "NP", "LOC"]
segment_tokens = {
  "WQ": ["Where"],
  "NP": ["the", "book"],
  "LOC": ["on", "the", "table"]
}
struct_roles = {
  "WQ": "interrogative_head",
  "NP": "entity",
  "LOC": "locative_modifier"
}
semantic_adjacent_cues = ["interrogative_scope", "locative_adjacent"]
identity_geometry = "referential_identity"
```

## 6. Cross-Primitive Interaction
- Activated by primitive: `SOB`.
- Consumed by primitives: `SROB`, `CnOB`, `SmOB`, `IdOB`.
- Canonical field files produced in this flow: `../fields/struct_segments.md`, `../fields/segment_tokens.md`, `../fields/struct_roles.md`, `../fields/constraints_matched.md`, `../fields/constraints_unmatched.md`, `../fields/constraint_residue.md`, `../fields/smoothing_operations.md`, `../fields/semantic_adjacent_cues.md`, `../fields/basin_residue.md`, `../fields/idob_packet.md`.

## 7. Glossary
- `segment_geometry`: structural geometry for segmentation.
- `struct_segments`: canonical segment labels.
- `segment_tokens`: token groups per segment.
- `SOB`: primitive that performs segmentation.
