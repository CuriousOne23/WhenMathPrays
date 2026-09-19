# segment_patterns.yaml

## Schema

```yaml
segment_patterns:
  <segment_name>:
    - <token_class>
    - ...
```

## Current Patterns

- `NP`: `DET`, `ADJ`, `NOUN`
- `VP`: `VERB`
- `PP`: `PREP`

## Usage

`SOB` reads these templates to identify structural segment labels and the token groups that belong to each segment.
