# User Guide

## Purpose

The PathA short simulator uses YAML dictionaries to drive segmentation, role assignment, constraint checks, and semantic extraction.

## Dictionary Files

- `token_classes.yaml`: Maps tokens to coarse lexical classes.
- `segment_patterns.yaml`: Defines segment templates by class sequence.
- `role_patterns.yaml`: Defines role options for each segment type.
- `constraint_rules.yaml`: Defines valid role transitions.
- `semantic_rules.yaml`: Defines extraction strategy for semantic core fields.

## Execution Flow

1. `InB` tokenizes input text.
2. `IE` normalizes tokens.
3. `SOB` loads `segment_patterns.yaml` and computes `struct_segments` + `segment_tokens`.
4. `SROB` loads `role_patterns.yaml` and computes `struct_roles` + `role_segments`.
5. `CnOB` loads `constraint_rules.yaml` and builds role transition constraints.
6. `IdOB` loads `semantic_rules.yaml` and extracts semantic fields.

## Notes

- YAML dictionaries are read at runtime.
- Missing dictionary entries fall back to conservative defaults.
- Trace output includes both legacy fields and new segment/role detail fields.
