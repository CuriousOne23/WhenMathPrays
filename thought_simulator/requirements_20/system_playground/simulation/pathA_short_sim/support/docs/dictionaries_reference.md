# Dictionaries Reference

This file consolidates dictionary documentation for the PathA short simulator.

## Dictionary Schema

```yaml
# token_classes.yaml
token_classes:
  <token>: <class>

# segment_patterns.yaml
segment_patterns:
  <segment_name>:
    - <token_class>
    - ...

# role_patterns.yaml
role_patterns:
  <segment_name>:
    - <role>
    - ...

# constraint_rules.yaml
constraint_rules:
  - <role1>-<role2>

# semantic_rules.yaml
semantic_rules:
  agent: <strategy>
  action: <strategy>
  patient: <strategy>
  modifiers: <strategy>
```

## token_classes.yaml

Defines lexical class lookup for normalized tokens.

Current intent example:

- the -> DET
- quick -> ADJ
- brown -> ADJ
- fox -> NOUN
- jumps -> VERB
- over -> PREP
- lazy -> ADJ
- dog -> NOUN

Impact on TP evolution:

- Drives SOB class sequence matching.
- Influences segment boundaries and resulting segment_tokens.

## segment_patterns.yaml

Defines segment templates consumed by SOB.

Current intent example:

- NP: DET, ADJ, NOUN
- VP: VERB
- PP: PREP

Impact on TP evolution:

- Determines struct_segments.
- Determines segment_tokens grouping.

## role_patterns.yaml

Defines role assignment options per segment label, consumed by SROB.

Current intent example:

- NP: agent, patient
- VP: action
- PP: relation

Impact on TP evolution:

- Determines struct_roles.
- Determines role_segments token aggregation.

## constraint_rules.yaml

Defines allowed role transitions consumed by CnOB.

Current intent example:

- agent-action
- action-relation
- relation-patient

Impact on TP evolution:

- Filters role transition pairs recorded in constraints.

## semantic_rules.yaml

Defines extraction strategies consumed by IdOB.

Current intent example:

- agent: first_np
- action: first_verb
- patient: last_np
- modifiers: between_agent_patient

Impact on TP evolution:

- Determines semantic_core fields and extraction behavior.

## Primitive to Dictionary Mapping

- SOB -> token_classes.yaml, segment_patterns.yaml
- SROB -> role_patterns.yaml
- CnOB -> constraint_rules.yaml
- IdOB -> semantic_rules.yaml

## Examples

Input: The quick brown fox jumps over the lazy dog.

Representative TP outputs after OB-Set primitives:

- struct_segments: [NP, VP, PP, NP]
- segment_tokens: [[the quick brown fox], [jumps], [over], [the lazy dog]]
- struct_roles: [agent, action, relation, patient]
- role_segments: {agent: [...], action: [...], relation: [...], patient: [...]}
- constraints: [agent-action, action-relation, relation-patient]

## How Dictionaries Influence TP Evolution

1. Token classes shape segment detection.
2. Segment patterns shape segment composition.
3. Role patterns shape semantic role assignment.
4. Constraint rules shape accepted structural transitions.
5. Semantic rules shape final semantic_core extraction.

## How to Extend Dictionaries

1. Add token classes for new vocabulary in token_classes.yaml.
2. Add new segment labels and patterns in segment_patterns.yaml.
3. Add matching role options for new segments in role_patterns.yaml.
4. Add or relax transitions in constraint_rules.yaml.
5. Add new extraction strategies in semantic_rules.yaml and implement strategy handling in IdOB.
6. Re-run run_examples.py and inspect trace deltas at SOB, SROB, CnOB, and IdOB.
