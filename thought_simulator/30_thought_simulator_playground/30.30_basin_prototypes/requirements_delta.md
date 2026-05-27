# Requirements Delta

## Purpose

This file records requirement-change proposals, implementer feedback, and migration notes for `30.30_basin_prototypes`.

## Migrated Structural Changes

- Renamed legacy verification report to canonical `verification_capsule.md`.
- Renamed legacy requirement report to canonical `requirements_delta.md`.
- Added canonical `artifacts/` directory for future verification outputs.
- Removed legacy split-note files after migration to canonical capsule structure.

## Proposed Requirement Changes

- Basin-specific behavioral requirements are pending implementation of executable scenarios.
- Determinism and traceability requirement mappings will be added after first scenario run evidence is available.

## Rationale

- Canonical naming and folder structure are prerequisites for consistent cross-module verification.
- Requirement deltas should be evidence-backed; scenario execution is required before normative requirement additions.

## Impacted Documents

- `software_description.md`
- `verification_capsule.md`
- `prototype.py`
- `harness.py`

## Open Validation Needed

- Define first executable positive and negative basin scenarios.
- Attach initial HLR/LLR mappings after scenario implementation.
- Confirm target requirement documents/sections for basin requirement deltas.

## Migration Notes

- Legacy report filenames were replaced with canonical capsule filenames on May 27, 2026.
- Future deltas should be appended here.

