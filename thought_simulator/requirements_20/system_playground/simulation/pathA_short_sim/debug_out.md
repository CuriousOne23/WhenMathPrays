# Debug Report

## Dimensions
- [segment_geometry:](debug/dimensions/segment_geometry.md) How the simulator divides an utterance into structural segments.
- [role_geometry:](debug/dimensions/role_geometry.md) How functional roles attach to segments.
- [constraint_geometry:](debug/dimensions/constraint_geometry.md) How structural and semantic constraints are evaluated.
- [smoothing_geometry:]() How smoothing operations resolve ambiguity and adjacency.
- [identity_geometry:](debug/dimensions/identity_geometry.md) How identity and referential structure propagate.
- [meaning_geometry:]() How semantic cues and meaning structures propagate.

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
### SOB
- struct_segments:
  - WQ
  - IQ
  - NP

- segment_tokens:
  - ['why']
  - ['is']
  - ['the', 'sky', 'blue']

- struct_roles:
  - []

- constraints_matched:
  - []

- constraints_unmatched:
  - []

- constraint_residue:
  - []

- basin_residue:
  - []

- smoothing_operations:
  - []

- semantic_adjacent_cues:
  - []

- semantic_core:
  - {}

- token_relations:
  - []

- ob_set_notes:
  - OB-Set: struct_segments = WQ, IQ, NP
  - OB-Set: segment_tokens = ['why'] | ['is'] | ['the', 'sky', 'blue']

See: [SOB](debug/primitives/SOB.md)

### SROB
- struct_segments:
  - []

- segment_tokens:
  - []

- struct_roles:
  - none
  - none
  - none

- constraints_matched:
  - []

- constraints_unmatched:
  - []

- constraint_residue:
  - []

- basin_residue:
  - []

- smoothing_operations:
  - []

- semantic_adjacent_cues:
  - []

- semantic_core:
  - {}

- token_relations:
  - []

- ob_set_notes:
  - OB-Set: Roles: ['none', 'none', 'none']
  - OB-Set: Role segments: {}

See: [SROB](debug/primitives/SROB.md)

### CnOB
- struct_segments:
  - []

- segment_tokens:
  - []

- struct_roles:
  - []

- constraints_matched:
  - query-focus-predicate
  - query-focus-predicate

- constraints_unmatched:
  - none-none
  - none-none
  - none-none
  - none-none

- constraint_residue:
  - locative_link
  - state-location
  - action-relation
  - relation-patient
  - agent-action
  - predicate-theme
  - theme-state
  - relation-theme
  - copular_state_link
  - locative_link
  - state-location
  - action-relation
  - relation-patient
  - agent-action
  - predicate-theme
  - theme-state
  - relation-theme
  - copular_state_link

- basin_residue:
  - []

- smoothing_operations:
  - []

- semantic_adjacent_cues:
  - []

- semantic_core:
  - {}

- token_relations:
  - []

- ob_set_notes:
  - OB-Set: constraints_matched=['query-focus-predicate']
  - OB-Set: constraints_unmatched=['none-none', 'none-none']
  - OB-Set: constraint_residue=['locative_link', 'state-location', 'action-relation', 'relation-patient', 'agent-action', 'predicate-theme', 'theme-state', 'relation-theme', 'copular_state_link']

See: [CnOB](debug/primitives/CnOB.md)

### SmOB
- struct_segments:
  - []

- segment_tokens:
  - []

- struct_roles:
  - []

- constraints_matched:
  - []

- constraints_unmatched:
  - []

- constraint_residue:
  - []

- basin_residue:
  - []

- smoothing_operations:
  - smooth:none->none
  - smooth:none->none
  - smooth:interrogative_scope
  - smooth:none->none
  - smooth:none->none
  - smooth:interrogative_scope

- semantic_adjacent_cues:
  - interrogative_scope
  - interrogative_scope

- semantic_core:
  truth_relation: interrogative_open

- token_relations:
  - []

- ob_set_notes:
  - OB-Set: smoothing_operations=['smooth:none->none', 'smooth:none->none', 'smooth:interrogative_scope']
  - OB-Set: semantic_adjacent_cues=['interrogative_scope']
  - OB-Set: basin_residue=[]
  - OB-Set: (no details)

See: [SmOB](debug/primitives/SmOB.md)

### IdOB
- struct_segments:
  - []

- segment_tokens:
  - []

- struct_roles:
  - []

- constraints_matched:
  - []

- constraints_unmatched:
  - []

- constraint_residue:
  - []

- basin_residue:
  - []

- smoothing_operations:
  - []

- semantic_adjacent_cues:
  - []

- semantic_core:
  selected_ops:
    - query_resolution
    - interrogative_identity_request
    - modifier_resolution
  query_focus: 
  predicate: 
  theme: 
  relation_modifiers: 
  complement: 
  agent: 
  state: 
  location: 
  action: 
  patient: 
  modifiers:
    - []

- token_relations:
  - []

- ob_set_notes:
  - []

See: [IdOB](debug/primitives/IdOB.md)

## Meaning Bundle Summary
- truth_relation: interrogative_open
- semantic_adjacent_cues:
  - interrogative_scope
  - interrogative_scope
- selected_ops:
  - query_resolution
  - interrogative_identity_request
  - modifier_resolution