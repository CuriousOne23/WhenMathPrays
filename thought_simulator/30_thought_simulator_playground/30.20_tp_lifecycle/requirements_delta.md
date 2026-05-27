# Requirements Delta

## Purpose

This file records requirement changes, implementer feedback, and migration notes for the `30.20_tp_lifecycle` module.
It replaces the legacy `updated_requirements.md` report while preserving its content and adding the structural corrections discovered during the refactor.

## Migrated Requirement Changes

- Add requirement that ThoughtPoint identity generation must be deterministic under `deterministic_mode`.
- Add requirement that `harness.py` is the only execution entrypoint for module verification.
- Add requirement that each executed scenario emits HLR/LLR references at runtime and records them in the verification report.
- Add requirement that verification artifacts include serialized TP state, provenance, and history for replay/audit.

## Additional Structural Requirements Discovered During Refactor

- Add requirement that `verification_capsule.md` is the canonical verification report for the module.
- Add requirement that `requirements_delta.md` is the canonical implementer feedback and requirement-change report.
- Add requirement that `30.30_verification_glossary.md` is the canonical shared vocabulary for verification terms.
- Add requirement that verification artifacts are written into `artifacts/` instead of the module root.
- Add requirement that the module preserve all migrated history when legacy report files are removed.
- Add requirement that negative-path coverage is reported alongside positive-path verification scenarios.
- Add requirement that IO schema compatibility and artifact path expectations be documented in `software_description.md`.

## Rationale

- Deterministic execution is incomplete if TP IDs vary across equivalent runs.
- A single execution entrypoint prevents drift between ad hoc scripts and official verification flow.
- Runtime requirement emission enforces end-to-end traceability from test to requirement.
- Artifact-backed evidence improves auditability and accelerates regression debugging.
- A single canonical verification capsule reduces fragmentation and makes migration safer.
- A shared glossary prevents terminology drift across modules and tools.
- Storing artifacts in `artifacts/` separates canonical outputs from source files and supports repeatable reruns.

## Impacted Documents

- `software_description.md`
- `prototype.py`
- `harness.py`
- `verification_capsule.md`
- `30.30_verification_glossary.md`
- `30.20_master_program_guide.md`

## Open Validation Needed

- Confirm whether HLR document-based IDs should be replaced with a centralized HLR registry in `thought_simulator_req`.
- Validate whether provenance creation notes should be normalized for split/merge-created TPs.
- Validate whether all legacy traceability content from `requirements_traceability.md` should be folded into `verification_capsule.md`.
- Confirm whether the new artifact naming convention should be extended to all modules immediately.

## Migration Notes

- Content from the legacy `updated_requirements.md` has been preserved here.
- Any future deltas should be appended here rather than reintroducing the deleted legacy file.


