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
- [IE:](debug/primitives/IE.md) Builds IE-compatible token intake structures.
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

## Final TP Intake Geometry
- tp_ie_tokens:
  - Why
  - does
  - the
  - rain
  - in
  - Spain
  - stay
  - mainly
  - in
  - the
  - plain
  - ?
- tp_ie_normalized_tokens:
  - why
  - does
  - the
  - rain
  - in
  - spain
  - stay
  - mainly
  - in
  - the
  - plain
  - ?
- tp_ie_token_classes:
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - PUNCT
- tp_ie_roles:
  - none
  - none
  - none
  - none
  - none
  - none
  - none
  - none
  - none
  - none
  - none
  - none
- tp_ie_segments:
  - 1
- tp_ie_segment_tokens:
  - ['Why', 'does', 'the', 'rain', 'in', 'Spain', 'stay', 'mainly', 'in', 'the', 'plain', '?']

## Stage Interpretations
### IE
- ie_tokens:
  - Why
  - does
  - the
  - rain
  - in
  - Spain
  - stay
  - mainly
  - in
  - the
  - plain
  - ?

- ie_normalized_tokens:
  - why
  - does
  - the
  - rain
  - in
  - spain
  - stay
  - mainly
  - in
  - the
  - plain
  - ?

- ie_token_classes:
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - WORD
  - PUNCT

- ie_roles:
  - none
  - none
  - none
  - none
  - none
  - none
  - none
  - none
  - none
  - none
  - none
  - none

- ie_segments:
  - 1

- ie_segment_tokens:
  - ['Why', 'does', 'the', 'rain', 'in', 'Spain', 'stay', 'mainly', 'in', 'the', 'plain', '?']


See: [IE](debug/primitives/IE.md)

### SOB
- sob_tokens:
  - Why
  - does
  - the
  - rain
  - in
  - Spain
  - stay
  - mainly
  - in
  - the
  - plain
  - ?

- sob_struct_segments:
  - WQ
  - IQ
  - NP
  - LOC
  - ST
  - AP
  - LOC

- sob_segment_tokens:
  - ['why']
  - ['does']
  - ['the', 'rain']
  - ['in', 'spain']
  - ['stay']
  - ['mainly']
  - ['in', 'the', 'plain']


See: [SOB](debug/primitives/SOB.md)

### SROB
- struct_roles:
  - []


See: [SROB](debug/primitives/SROB.md)

### CnOB
- constraints_matched:
  - structural_rule
  - adjacency_rule

- constraints_unmatched:
  - compatibility_rule
  - continuity_rule

- constraint_residue:
  - interrogative_scope
  - locative_adjacent


See: [CnOB](debug/primitives/CnOB.md)

### SmOB
- smoothing_operations:
  - adjacency_smoothing
  - role_smoothing
  - segment_smoothing
  - continuity_smoothing

- semantic_adjacent_cues:
  - interrogative_scope
  - locative_adjacent

- basin_residue:
  - []


See: [SmOB](debug/primitives/SmOB.md)

### IdOB
- idob_packet:
  identity_geometry: referential_identity
  truth_relation: interrogative
  truth_relation_family: interrogative_polar
  semantic_core:
    selected_ops: ['modifier_resolution']
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
    modifiers: ['locative_adjacent']
  selected_ops:
    - modifier_resolution
  claimed_fields:
    - truth_relation
    - truth_relation_family_hint
    - semantic_core_tokens
    - selected_ops
    - semantic_core
    - identity_geometry
  contributors:
    - interrogative_polar
    - locative
    - agent_action
    - modifier_resolution
    - residual_identity
  contributions:
    - {'name': 'interrogative_polar', 'family': 'interrogative_polar', 'priority': 11, 'fragment': {'truth_relation': 'interrogative', 'truth_relation_family_hint': 'interrogative_polar'}}
    - {'name': 'locative', 'family': 'locative', 'priority': 30, 'fragment': {'semantic_core_tokens': ['locative_modifier'], 'truth_relation_family_hint': 'descriptive_locative'}}
    - {'name': 'agent_action', 'family': 'residual_identity', 'priority': 50, 'fragment': {}}
    - {'name': 'modifier_resolution', 'family': 'mixed_descriptive', 'priority': 60, 'fragment': {'selected_ops': ['modifier_resolution'], 'semantic_core': {'selected_ops': ['modifier_resolution'], 'query_focus': '', 'predicate': '', 'theme': '', 'relation_modifiers': '', 'complement': '', 'agent': '', 'state': '', 'location': '', 'action': '', 'patient': '', 'modifiers': ['locative_adjacent']}, 'semantic_core_tokens': ['locative_modifier']}}
    - {'name': 'residual_identity', 'family': 'residual_identity', 'priority': 90, 'fragment': {'identity_geometry': 'referential_identity', 'truth_relation': 'interrogative'}}
  activation_set:
    - interrogative_polar
    - locative
    - agent_action
    - modifier_resolution
    - residual_identity
  inactive_objects:
    - interrogative_wh
    - copular_state
    - mixed_descriptive
  residual_activated: True
  overlap_events:
    - {'a': 'residual_identity', 'b': 'locative', 'mode': 'coexist', 'fields': []}
  meaning_delta:
  psc_violations:
    - []
  registry_digest: 693600ce4cab15ee344e89e070a490b2b82f6d7d490f244d314c23fd5497c453
  complete: True
  tru_hint: interrogative


See: [IdOB](debug/primitives/IdOB.md)

## Meaning Bundle Summary
- truth_relation: interrogative
- semantic_adjacent_cues:
  - interrogative_scope
  - locative_adjacent
- semantic_core:
  - []
- idob_packet:
  identity_geometry: referential_identity
  truth_relation: interrogative
  truth_relation_family: interrogative_polar
  semantic_core:
    selected_ops: ['modifier_resolution']
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
    modifiers: ['locative_adjacent']
  selected_ops:
    - modifier_resolution
  claimed_fields:
    - truth_relation
    - truth_relation_family_hint
    - semantic_core_tokens
    - selected_ops
    - semantic_core
    - identity_geometry
  contributors:
    - interrogative_polar
    - locative
    - agent_action
    - modifier_resolution
    - residual_identity
  contributions:
    - {'name': 'interrogative_polar', 'family': 'interrogative_polar', 'priority': 11, 'fragment': {'truth_relation': 'interrogative', 'truth_relation_family_hint': 'interrogative_polar'}}
    - {'name': 'locative', 'family': 'locative', 'priority': 30, 'fragment': {'semantic_core_tokens': ['locative_modifier'], 'truth_relation_family_hint': 'descriptive_locative'}}
    - {'name': 'agent_action', 'family': 'residual_identity', 'priority': 50, 'fragment': {}}
    - {'name': 'modifier_resolution', 'family': 'mixed_descriptive', 'priority': 60, 'fragment': {'selected_ops': ['modifier_resolution'], 'semantic_core': {'selected_ops': ['modifier_resolution'], 'query_focus': '', 'predicate': '', 'theme': '', 'relation_modifiers': '', 'complement': '', 'agent': '', 'state': '', 'location': '', 'action': '', 'patient': '', 'modifiers': ['locative_adjacent']}, 'semantic_core_tokens': ['locative_modifier']}}
    - {'name': 'residual_identity', 'family': 'residual_identity', 'priority': 90, 'fragment': {'identity_geometry': 'referential_identity', 'truth_relation': 'interrogative'}}
  activation_set:
    - interrogative_polar
    - locative
    - agent_action
    - modifier_resolution
    - residual_identity
  inactive_objects:
    - interrogative_wh
    - copular_state
    - mixed_descriptive
  residual_activated: True
  overlap_events:
    - {'a': 'residual_identity', 'b': 'locative', 'mode': 'coexist', 'fields': []}
  meaning_delta:
  psc_violations:
    - []
  registry_digest: 693600ce4cab15ee344e89e070a490b2b82f6d7d490f244d314c23fd5497c453
  complete: True
  tru_hint: interrogative

## IdOB Space Summary
- contributors: ['interrogative_polar', 'locative', 'agent_action', 'modifier_resolution', 'residual_identity']
- contributor_labels: ['interrogative_polar -> Interrogative Polar', 'locative -> Locative', 'agent_action -> Agent Action', 'modifier_resolution -> Modifier Resolution', 'residual_identity -> Residual Identity']
- contributions: [{'name': 'interrogative_polar', 'family': 'interrogative_polar', 'priority': 11, 'fragment': {'truth_relation': 'interrogative', 'truth_relation_family_hint': 'interrogative_polar'}}, {'name': 'locative', 'family': 'locative', 'priority': 30, 'fragment': {'semantic_core_tokens': ['locative_modifier'], 'truth_relation_family_hint': 'descriptive_locative'}}, {'name': 'agent_action', 'family': 'residual_identity', 'priority': 50, 'fragment': {}}, {'name': 'modifier_resolution', 'family': 'mixed_descriptive', 'priority': 60, 'fragment': {'selected_ops': ['modifier_resolution'], 'semantic_core': {'selected_ops': ['modifier_resolution'], 'query_focus': '', 'predicate': '', 'theme': '', 'relation_modifiers': '', 'complement': '', 'agent': '', 'state': '', 'location': '', 'action': '', 'patient': '', 'modifiers': ['locative_adjacent']}, 'semantic_core_tokens': ['locative_modifier']}}, {'name': 'residual_identity', 'family': 'residual_identity', 'priority': 90, 'fragment': {'identity_geometry': 'referential_identity', 'truth_relation': 'interrogative'}}]
- activation_set: ['interrogative_polar', 'locative', 'agent_action', 'modifier_resolution', 'residual_identity']
- inactive_objects: ['interrogative_wh', 'copular_state', 'mixed_descriptive']
- residual_activated: True
- overlap_events: [{'a': 'residual_identity', 'b': 'locative', 'mode': 'coexist', 'fields': []}]
- meaning_delta: {}
- psc_violation_count: 0
- psc_violations: []
- registry_digest: 693600ce4cab15ee344e89e070a490b2b82f6d7d490f244d314c23fd5497c453
- truth_relation_family: interrogative_polar
- tru_hint: interrogative
- complete: True

Freeze Version: pathA_v1