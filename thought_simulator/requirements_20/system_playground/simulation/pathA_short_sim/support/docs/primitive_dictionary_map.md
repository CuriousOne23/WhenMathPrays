# Primitive to Dictionary Map

## Mapping

- `SOB` -> `segment_patterns.yaml`
- `SROB` -> `role_patterns.yaml`
- `CnOB` -> `constraint_rules.yaml`
- `IdOB` -> `semantic_rules.yaml`

## Data Flow

1. `SOB` sets:
   - `struct_segments`
   - `segment_tokens`
2. `SROB` sets:
   - `struct_roles`
   - `role_segments`
3. `CnOB` sets:
   - `constraints`
4. `IdOB` sets:
   - `semantic_core`

## Trace Additions

The simulator trace now surfaces `segment_tokens` and `role_segments` in notes for easier debugging.
