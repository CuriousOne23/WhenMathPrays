# Debug Report

## Dimensions
- segment_geometry: [segment_geometry](debug/dimensions/segment_geometry.md)
- role_geometry: [role_geometry](debug/dimensions/role_geometry.md)
- constraint_geometry: [constraint_geometry](debug/dimensions/constraint_geometry.md)
- smoothing_geometry: [smoothing_geometry](debug/dimensions/smoothing_geometry.md)
- identity_geometry: [identity_geometry](debug/dimensions/identity_geometry.md)
- meaning_geometry: [meaning_geometry](debug/dimensions/meaning_geometry.md)

## Fields
- struct_segments: [struct_segments](debug/fields/struct_segments.md)
- struct_roles: [struct_roles](debug/fields/struct_roles.md)
- constraints_matched: [constraints_matched](debug/fields/constraints_matched.md)
- semantic_adjacent_cues: [semantic_adjacent_cues](debug/fields/semantic_adjacent_cues.md)
- idob_packet: [idob_packet](debug/fields/idob_packet.md)
- residue: [residue](debug/fields/residue.md)

## Primitives
- SOB: [SOB](debug/primitives/SOB.md)
- SROB: [SROB](debug/primitives/SROB.md)
- CnOB: [CnOB](debug/primitives/CnOB.md)
- SmOB: [SmOB](debug/primitives/SmOB.md)
- IdOB: [IdOB](debug/primitives/IdOB.md)

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

- ob_set_notes:
  - notes: [OB-Set] Segments: ['WQ', 'IQ', 'NP']; Segment tokens: [['why'], ['is'], ['the', 'sky', 'blue']]

See: [SOB](debug/primitives/SOB.md)

### SROB
- segments:
  - []

- segment_tokens:
  - []

- roles:
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

- ob_set_notes:
  - notes: [OB-Set] Roles: ['none', 'none', 'none']; Role segments: {}

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
  - relation-patient
  - action-relation
  - agent-action
  - state-location
  - copular_state_link
  - predicate-theme
  - locative_link
  - theme-state
  - relation-theme

- smoothing_operations:
  - []

- semantic_adjacent_cues:
  - []

- semantic_core:
  - {}

- token_relations:
  agent-action: ('', '')
  action-relation: ('', '')
  relation-patient: ('', '')
  state-location: ('', '')
  query-focus-predicate: ('', '')
  predicate-theme: ('', '')

- ob_set_notes:
  - notes: [OB-Set] matched=['query-focus-predicate']; unmatched=['none-none', 'none-none']; residue=['relation-patient', 'action-relation', 'agent-action', 'state-location', 'copular_state_link', 'predicate-theme', 'locative_link', 'theme-state', 'relation-theme']

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
  - smooth:interrogative_scope

- semantic_adjacent_cues:
  - interrogative_scope

- semantic_core:
  truth_relation: interrogative_open

- token_relations:
  agent->action: ('', '')
  action->relation: ('', '')
  relation->patient: ('', '')
  state->location: ('', '')
  query_focus->predicate: ('', '')

- ob_set_notes:
  - notes: [OB-Set] operations=['smooth:none->none', 'smooth:none->none', 'smooth:interrogative_scope']; semantic_adjacent_cues=['interrogative_scope']; residue=[]
  - notes: [OB-Set]

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
  query_focus: 
  predicate: 
  theme: 
  agent: 
  action: 
  relation: 
  patient: 
  modifiers:
    - interrogative_scope

See: [IdOB](debug/primitives/IdOB.md)
