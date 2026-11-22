# Schema families

- schema families: copular_state, locative, mixed_descriptive, interrogative_wh, interrogative_polar, agent_action, imperative, exclamative, modifier_resolution, residual_identity
- card families: agent_action=agent_action, copular_state=copular_state, exclamative=exclamative, imperative=imperative, interrogative_polar=interrogative_polar, interrogative_wh=interrogative_wh, locative=locative, mixed_descriptive=mixed_descriptive, modifier_resolution=mixed_descriptive, residual_identity=residual_identity
- missing from schema: none
- schema families: matched

# Debug Report

## Dimensions
- [segment_geometry:](debug/dimensions/segment_geometry.md) How the simulator divides an utterance into structural segments.
- [role_geometry:](debug/dimensions/role_geometry.md) How functional roles attach to segments.
- [constraint_geometry:](debug/dimensions/constraint_geometry.md) How structural and semantic constraints are evaluated.
- [identity_geometry:](debug/dimensions/identity_geometry.md) How identity and referential structure propagate.
- [semantic_core:](debug/dimensions/semantic_core.md) How IdOB stabilizes canonical semantic_core.
- [truth_relation:](debug/dimensions/truth_relation.md) How IdOB stabilizes canonical truth_relation.

## Fields
- [struct_segments:](debug/fields/struct_segments.md) The segments detected during structural parsing.
- [segment_tokens:](debug/fields/segment_tokens.md) Token groups attached to each structural segment.
- [struct_roles:](debug/fields/struct_roles.md) The roles assigned to each segment.
- [constraints_matched:](debug/fields/constraints_matched.md) Constraints successfully satisfied.
- [constraints_unmatched:](debug/fields/constraints_unmatched.md) Constraints that remained unsatisfied.
- [constraint_residue:](debug/fields/constraint_residue.md) Residual mismatch material from CnOB.
- [smoothing_operations:](debug/fields/smoothing_operations.md) Smoothing transforms applied by SmOB.
- [semantic_adjacent_cues:](debug/fields/semantic_adjacent_cues.md) Semantic cues adjacent to structural elements.
- [smoothing_residue:](debug/fields/smob_smoothing_residue.md) Residual unresolved smoothing-stage material from SmOB.
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
  - The
  - sky
  - is
  - blue
  - .
- tp_ie_normalized_tokens:
  - the
  - sky
  - is
  - blue
  - .
- tp_ie_token_classes:
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
- tp_ie_segments:
  - 1
- tp_ie_segment_tokens:
  - ['The', 'sky', 'is', 'blue', '.']

## Stage Interpretations
### IE
- ie_tokens:
  - The
  - sky
  - is
  - blue
  - .

- ie_normalized_tokens:
  - the
  - sky
  - is
  - blue
  - .

- ie_token_classes:
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

- ie_segments:
  - 1

- ie_segment_tokens:
  - ['The', 'sky', 'is', 'blue', '.']


See: [IE](debug/primitives/IE.md)

### SOB
- sob_tokens:
  - The
  - sky
  - is
  - blue
  - .

- sob_struct_segments:
  - NP
  - CP
  - AP

- sob_segment_tokens:
  - ['the', 'sky']
  - ['is']
  - ['blue']


See: [SOB](debug/primitives/SOB.md)

### SROB
- struct_roles:
  - []


See: [SROB](debug/primitives/SROB.md)

### CnOB
- constraints_matched:
  - structural_rule
  - compatibility_rule

- constraints_unmatched:
  - adjacency_rule
  - continuity_rule

- constraint_residue:
  - []


See: [CnOB](debug/primitives/CnOB.md)

### SmOB
- smoothing_operations:
  - adjacency_smoothing
  - role_smoothing
  - basin_compression_smoothing
  - continuity_smoothing

- semantic_adjacent_cues:
  - []

- smoothing_residue:
  - []


See: [SmOB](debug/primitives/SmOB.md)

### IdOB
- idob_packet:
  identity_geometry: structural_identity
  truth_relation: declarative
  truth_relation_family: descriptive_state
  semantic_core:
    selected_ops: ['state']
    query_focus: 
    speaker: 
    recipient: 
    relative_subject: 
    adverb: 
    predicate: 
    theme: the sky
    copula: is
    relation_modifiers: 
    complement: blue
    agent: the sky
    state: blue
    location: 
    action: 
    patient: 
    modifiers: []
  selected_ops:
    - state
  claimed_fields:
    - truth_relation
    - truth_relation_family_hint
    - identity_geometry
    - semantic_core
    - selected_ops
  contributors:
    - copular_state
    - residual_identity
  contributions:
    - {'name': 'copular_state', 'family': 'copular_state', 'priority': 20, 'fragment': {'truth_relation': 'declarative', 'truth_relation_family_hint': 'descriptive_state'}}
    - {'name': 'residual_identity', 'family': 'residual_identity', 'priority': 90, 'fragment': {'identity_geometry': 'structural_identity', 'truth_relation': 'declarative', 'semantic_core': {'selected_ops': ['state'], 'query_focus': '', 'speaker': '', 'recipient': '', 'relative_subject': '', 'adverb': '', 'predicate': '', 'theme': 'the sky', 'copula': 'is', 'relation_modifiers': '', 'complement': 'blue', 'agent': 'the sky', 'state': 'blue', 'location': '', 'action': '', 'patient': '', 'modifiers': []}, 'selected_ops': ['state']}}
  activation_set:
    - copular_state
    - residual_identity
  inactive_objects:
    - interrogative_wh
    - interrogative_polar
    - imperative
    - exclamative
    - locative
    - mixed_descriptive
    - agent_action
    - modifier_resolution
  residual_activated: True
  overlap_events:
    - {'a': 'residual_identity', 'b': 'copular_state', 'mode': 'coexist', 'fields': []}
  meaning_delta:
    semantic_core_tokens: {'legacy': ['entity'], 'split': []}
  psc_violations:
    - {'object': 'residual_identity', 'invariant': 'I8', 'field': 'semantic_core', 'rule': 'writes_only_declared_fields', 'detail': "unlisted semantic_core keys: ['adverb', 'copula', 'recipient', 'relative_subject', 'speaker']"}
  registry_digest: ddd6334c681e5278723527c3515d4e87c4455fce6fa6e6e10ec8a6d9457ed1c7
  complete: True
  tru_hint: declarative


See: [IdOB](debug/primitives/IdOB.md)

## Meaning Bundle Summary
- truth_relation: declarative
- semantic_adjacent_cues:
  - []
- semantic_core:
  - []
- idob_packet:
  identity_geometry: structural_identity
  truth_relation: declarative
  truth_relation_family: descriptive_state
  semantic_core:
    selected_ops: ['state']
    query_focus: 
    speaker: 
    recipient: 
    relative_subject: 
    adverb: 
    predicate: 
    theme: the sky
    copula: is
    relation_modifiers: 
    complement: blue
    agent: the sky
    state: blue
    location: 
    action: 
    patient: 
    modifiers: []
  selected_ops:
    - state
  claimed_fields:
    - truth_relation
    - truth_relation_family_hint
    - identity_geometry
    - semantic_core
    - selected_ops
  contributors:
    - copular_state
    - residual_identity
  contributions:
    - {'name': 'copular_state', 'family': 'copular_state', 'priority': 20, 'fragment': {'truth_relation': 'declarative', 'truth_relation_family_hint': 'descriptive_state'}}
    - {'name': 'residual_identity', 'family': 'residual_identity', 'priority': 90, 'fragment': {'identity_geometry': 'structural_identity', 'truth_relation': 'declarative', 'semantic_core': {'selected_ops': ['state'], 'query_focus': '', 'speaker': '', 'recipient': '', 'relative_subject': '', 'adverb': '', 'predicate': '', 'theme': 'the sky', 'copula': 'is', 'relation_modifiers': '', 'complement': 'blue', 'agent': 'the sky', 'state': 'blue', 'location': '', 'action': '', 'patient': '', 'modifiers': []}, 'selected_ops': ['state']}}
  activation_set:
    - copular_state
    - residual_identity
  inactive_objects:
    - interrogative_wh
    - interrogative_polar
    - imperative
    - exclamative
    - locative
    - mixed_descriptive
    - agent_action
    - modifier_resolution
  residual_activated: True
  overlap_events:
    - {'a': 'residual_identity', 'b': 'copular_state', 'mode': 'coexist', 'fields': []}
  meaning_delta:
    semantic_core_tokens: {'legacy': ['entity'], 'split': []}
  psc_violations:
    - {'object': 'residual_identity', 'invariant': 'I8', 'field': 'semantic_core', 'rule': 'writes_only_declared_fields', 'detail': "unlisted semantic_core keys: ['adverb', 'copula', 'recipient', 'relative_subject', 'speaker']"}
  registry_digest: ddd6334c681e5278723527c3515d4e87c4455fce6fa6e6e10ec8a6d9457ed1c7
  complete: True
  tru_hint: declarative

## IdOB Space Summary
- contributors: ['copular_state', 'residual_identity']
- contributor_labels: ['copular_state -> Copular State', 'residual_identity -> Residual Identity']
- contributions: [{'name': 'copular_state', 'family': 'copular_state', 'priority': 20, 'fragment': {'truth_relation': 'declarative', 'truth_relation_family_hint': 'descriptive_state'}}, {'name': 'residual_identity', 'family': 'residual_identity', 'priority': 90, 'fragment': {'identity_geometry': 'structural_identity', 'truth_relation': 'declarative', 'semantic_core': {'selected_ops': ['state'], 'query_focus': '', 'speaker': '', 'recipient': '', 'relative_subject': '', 'adverb': '', 'predicate': '', 'theme': 'the sky', 'copula': 'is', 'relation_modifiers': '', 'complement': 'blue', 'agent': 'the sky', 'state': 'blue', 'location': '', 'action': '', 'patient': '', 'modifiers': []}, 'selected_ops': ['state']}}]
- activation_set: ['copular_state', 'residual_identity']
- inactive_objects: ['interrogative_wh', 'interrogative_polar', 'imperative', 'exclamative', 'locative', 'mixed_descriptive', 'agent_action', 'modifier_resolution']
- residual_activated: True
- overlap_events: [{'a': 'residual_identity', 'b': 'copular_state', 'mode': 'coexist', 'fields': []}]
- meaning_delta: {'semantic_core_tokens': {'legacy': ['entity'], 'split': []}}
- psc_violation_count: 1
- psc_violations: ["residual_identity (Residual Identity) | invariant=I8 field=semantic_core rule=writes_only_declared_fields detail=unlisted semantic_core keys: ['adverb', 'copula', 'recipient', 'relative_subject', 'speaker']"]
- registry_digest: ddd6334c681e5278723527c3515d4e87c4455fce6fa6e6e10ec8a6d9457ed1c7
- truth_relation_family: descriptive_state
- tru_hint: declarative
- complete: True

Freeze Version: pathA_v1