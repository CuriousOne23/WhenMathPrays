# Debug Report

## Dimensions
- [segment_geometry:](debug/dimensions/segment_geometry.md) How the simulator divides an utterance into structural segments.
- [role_geometry:](debug/dimensions/role_geometry.md) How functional roles attach to segments.
- [constraint_geometry:](debug/dimensions/constraint_geometry.md) How structural and semantic constraints are evaluated.
- [identity_geometry:](debug/dimensions/identity_geometry.md) How identity and referential structure propagate.

## Fields
- [struct_segments:](debug/fields/struct_segments.md) The segments detected during structural parsing.
- [segment_tokens:](debug/fields/segment_tokens.md) Token groups attached to each structural segment.
- [struct_roles:](debug/fields/struct_roles.md) The roles assigned to each segment.
- [constraints_matched:](debug/fields/constraints_matched.md) Constraints successfully satisfied.
- [constraints_unmatched:](debug/fields/constraints_unmatched.md) Constraints that remained unsatisfied.
- [constraint_residue:](debug/fields/constraint_residue.md) Residual mismatch material from CnOB.
- [smoothing_operations:](debug/fields/smoothing_operations.md) Smoothing transforms applied by SmOB.
- [semantic_adjacent_cues:](debug/fields/semantic_adjacent_cues.md) Semantic cues adjacent to structural elements.
- [basin_residue:](debug/fields/basin_residue.md) Residual unresolved basin-level material from SmOB.
- [truth_relation:](debug/dimensions/truth_relation.md) Truth relation selected for meaning resolution.
- [semantic_core:](debug/dimensions/semantic_core.md) Identity-conditioned semantic bundle emitted by IdOB.
- [idob_packet:](debug/fields/idob_packet.md) The identity packet produced by IdOB.

## Primitives
- [SOB:](debug/primitives/SOB.md) Performs structural segmentation.
- [SROB:](debug/primitives/SROB.md) Assigns roles to segments.
- [CnOB:](debug/primitives/CnOB.md) Matches constraints and emits canonical constraint fields.
- [SmOB:](debug/primitives/SmOB.md) Applies smoothing and adjacency resolution.
- [IdOB:](debug/primitives/IdOB.md) Builds the identity packet and semantic core.

## Canonical Routing Ladder Summary
- Tokens -> Segments -> Roles -> Constraints/Cues -> Basin -> Identity
- SOB: structural segmentation stage
- SROB: role assignment stage
- CnOB: constraint matching stage
- SmOB: smoothing and basin-adjacency stage
- IdOB: identity and meaning-bundle stage

## Stage Interpretations
## Meaning Bundle Summary
- truth_relation: 
- semantic_adjacent_cues:
  - []
- semantic_core:
  - []
- idob_packet:
  - {}