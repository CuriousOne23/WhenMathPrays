# Refactor Phase 3 Report

Generated: 2026-05-28

## Objective

Add migration-safe metadata governance checks and enforce them in CI.

## Executed Changes

### Frontmatter and ID Validator

Added script:

- `scripts/validate_doc_frontmatter_and_ids.py`

Current behavior:

- scans markdown files in `20_requirements/`, `30_verification/`, and `50_thought_simulator_design/`
- validates frontmatter shape when frontmatter is present
- warns when frontmatter is missing in target tiers when `--require-frontmatter` is used
- validates HLR/LLR token formats
- allows placeholder IDs (`HLR-?`, `LLR-?`) as warnings
- treats malformed IDs as warnings by default and as errors in `--strict-ids` mode

### CI Integration

Extended workflow:

- `.github/workflows/thought-simulator-doc-dependency-check.yml`

The workflow now runs:

1. `python thought_simulator/scripts/check_doc_dependencies.py`
2. `python thought_simulator/scripts/validate_doc_frontmatter_and_ids.py --require-frontmatter`

### Validation Baseline

- dependency lint passes
- frontmatter/ID validator passes with warnings (no errors)
- warnings represent migration backlog, not hard blockers

## Remaining Work (Phase 4+)

- introduce frontmatter to canonical docs in 20/30/50 tiers
- migrate legacy ID tokens to the new canonical format (`HLR-20.xx-###`, `LLR-30.xx-###`, `LLR-50.xx-###`)
- enable `--strict-ids` in CI after ID migration completes
- add relation semantics checks (`satisfies`, `proves`, `derived-from`, `supersedes`)
