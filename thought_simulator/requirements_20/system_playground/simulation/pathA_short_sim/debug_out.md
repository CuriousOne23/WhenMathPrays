# Debug Report

## Dimensions
- [segment_geometry:](debug/dimensions/segment_geometry.md) Definition of segment geometry.
- [role_geometry:](debug/dimensions/role_geometry.md) Definition of role geometry.
- [constraint_geometry:](debug/dimensions/constraint_geometry.md) Definition of constraint geometry.
- [smoothing_geometry:](debug/dimensions/smoothing_geometry.md) Definition of smoothing geometry.
- [identity_geometry:](debug/dimensions/identity_geometry.md) Definition of identity geometry.
- [meaning_geometry:](debug/dimensions/meaning_geometry.md) Definition of meaning geometry.

## Fields
- [struct_segments:](debug/fields/struct_segments.md) Structural segments recognized by the simulator.
- [struct_roles:](debug/fields/struct_roles.md) Roles assigned to segments.
- [constraints_matched:](debug/fields/constraints_matched.md) Constraints successfully matched.
- [semantic_adjacent_cues:](debug/fields/semantic_adjacent_cues.md) Semantic cues adjacent to structural elements.
- [idob_packet:](debug/fields/idob_packet.md) Identity packet produced by IdOB.
- [residue:](debug/fields/residue.md) Residual structural or semantic material.

## Primitives
- [SOB:](debug/primitives/SOB.md) Segment Observation Block.
- [SROB:](debug/primitives/SROB.md) Segment Role Observation Block.
- [CnOB:](debug/primitives/CnOB.md) Constraint Observation Block.
- [SmOB:](debug/primitives/SmOB.md) Smoothing Observation Block.
- [IdOB:](debug/primitives/IdOB.md) Identity Observation Block.

## Primitive Summary
- SOB: structural segmentation
- SROB: role assignment
- CnOB: constraint matching
- SmOB: smoothing + semantic adjacency
- IdOB: semantic core + truth relation

## Interpreted Blocks
### SOB
- segments:
  - WQ
  - IQ
  - NP

- segment_tokens:
  - ['why']
  - ['is']
  - ['the', 'sky', 'blue']

- roles:
  - []

- constraints_matched:
  - []

- residue:
  - []

- smoothing_residue:
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
  - OB-Set: Segments = WQ, IQ, NP
  - OB-Set: Segment tokens = ['why'] | ['is'] | ['the', 'sky', 'blue']

See: [SOB](debug/primitives/SOB.md)

### SROB
- segments:
  - []

- segment_tokens:
  - []

- roles:
  - none
  - none
  - none

- constraints_matched:
  - []

- residue:
  - []

- smoothing_residue:
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
- segments:
  - []

- segment_tokens:
  - []

- roles:
  - []

- constraints_matched:
  - query-focus-predicate

- residue:
  - relation-patient
  - action-relation
  - agent-action
  - state-location
  - copular_state_link
  - predicate-theme
  - locative_link
  - theme-state
  - relation-theme

- smoothing_residue:
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
  - OB-Set: matched=['query-focus-predicate']
  - OB-Set: unmatched=['none-none', 'none-none']
  - OB-Set: residue=['relation-patient', 'action-relation', 'agent-action', 'state-location', 'copular_state_link', 'predicate-theme', 'locative_link', 'theme-state', 'relation-theme']

See: [CnOB](debug/primitives/CnOB.md)

### SmOB
- segments:
  - []

- segment_tokens:
  - []

- roles:
  - []

- constraints_matched:
  - []

- residue:
  - []

- smoothing_residue:
  - []

- smoothing_operations:
  - smooth:none->none
  - smooth:none->none
  - smooth:interrogative_scope

- semantic_adjacent_cues:
  - interrogative_scope

- semantic_core:
  truth_relation: interrogative_open

- token_relations:
  - []

- ob_set_notes:
  - OB-Set: operations=['smooth:none->none', 'smooth:none->none', 'smooth:interrogative_scope']
  - OB-Set: semantic_adjacent_cues=['interrogative_scope']
  - OB-Set: residue=[]
  - OB-Set: (no details)

See: [SmOB](debug/primitives/SmOB.md)

### IdOB
- segments:
  - []

- segment_tokens:
  - []

- roles:
  - []

- constraints_matched:
  - []

- residue:
  - []

- smoothing_residue:
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

## Semantic Summary
- truth_relation: interrogative_open
- semantic_adjacent_cues:
  - interrogative_scope
- selected_ops:
  - query_resolution
  - interrogative_identity_request
  - modifier_resolution