# Debug Report

## Dimensions
- [segment_geometry:](debug/dimensions/segment_geometry.md) How the simulator divides an utterance into structural segments.
- [role_geometry:](debug/dimensions/role_geometry.md) How functional roles attach to segments.
- [constraint_geometry:](debug/dimensions/constraint_geometry.md) How structural and semantic constraints are evaluated.
- [smoothing_geometry:](debug/dimensions/smoothing_geometry.md) How smoothing operations resolve ambiguity and adjacency.
- [identity_geometry:](debug/dimensions/identity_geometry.md) How identity and referential structure propagate.
- [meaning_geometry:](debug/dimensions/meaning_geometry.md) How semantic cues and meaning structures propagate.

## Fields
- [struct_segments:](debug/fields/struct_segments.md) The segments detected during structural parsing.
- [struct_roles:](debug/fields/struct_roles.md) The roles assigned to each segment.
- [constraints_matched:](debug/fields/constraints_matched.md) Constraints successfully satisfied.
- [semantic_adjacent_cues:](debug/fields/semantic_adjacent_cues.md) Semantic cues adjacent to structural elements.
- [idob_packet:](debug/fields/idob_packet.md) The identity packet produced by IdOB.
- [residue:](debug/fields/residue.md) Unmatched or leftover structural/semantic material.

## Primitives
- [SOB:](debug/primitives/SOB.md) Performs structural segmentation.
- [SROB:](debug/primitives/SROB.md) Assigns roles to segments.
- [CnOB:](debug/primitives/CnOB.md) Matches constraints and produces residue.
- [SmOB:](debug/primitives/SmOB.md) Applies smoothing and adjacency resolution.
- [IdOB:](debug/primitives/IdOB.md) Builds the identity packet and semantic core.

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
  - copular_state_link
  - action-relation
  - relation-patient
  - agent-action
  - locative_link
  - relation-theme
  - predicate-theme
  - state-location
  - theme-state

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
  - OB-Set: residue=['copular_state_link', 'action-relation', 'relation-patient', 'agent-action', 'locative_link', 'relation-theme', 'predicate-theme', 'state-location', 'theme-state']

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