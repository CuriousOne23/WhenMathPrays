# semantic_rules.yaml

## Schema

```yaml
semantic_rules:
  agent: <strategy>
  action: <strategy>
  patient: <strategy>
  modifiers: <strategy>
```

## Current Rules

- `agent`: `first_np`
- `action`: `first_verb`
- `patient`: `last_np`
- `modifiers`: `between_agent_patient`

## Usage

`IdOB` applies these strategies over `segment_tokens` and `role_segments` to construct `semantic_core`.
