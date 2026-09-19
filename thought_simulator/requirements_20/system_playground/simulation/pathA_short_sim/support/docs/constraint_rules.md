# constraint_rules.yaml

## Schema

```yaml
constraint_rules:
  - <role1>-<role2>
```

## Current Rules

- `agent-action`
- `action-relation`
- `relation-patient`

## Usage

`CnOB` derives role transitions from `struct_roles` and intersects them with these allowed constraints.
