# role_patterns.yaml

## Schema

```yaml
role_patterns:
  <segment_name>:
    - <role>
    - ...
```

## Current Patterns

- `NP`: `agent`, `patient`
- `VP`: `action`
- `PP`: `relation`

## Usage

`SROB` maps each detected segment to a role. For repeated segment labels, role assignment advances through the configured role list.
