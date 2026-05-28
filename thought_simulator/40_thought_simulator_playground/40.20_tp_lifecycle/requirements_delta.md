# Requirements Delta

## Purpose

This file records requirement changes, implementer feedback, and migration notes for the `40.20_tp_lifecycle` module.
It replaces the legacy `updated_requirements.md` report while preserving its content and adding the structural corrections discovered during the refactor.

## Migrated Requirement Changes

- Add requirement that ThoughtPoint identity generation must be deterministic under `deterministic_mode`.
- Add requirement that `harness.py` is the only execution entrypoint for module verification.
- Add requirement that each executed scenario emits HLR/LLR references at runtime and records them in the verification report.
- Add requirement that verification artifacts include serialized TP state, provenance, and history for replay/audit.

## Additional Structural Requirements Discovered During Refactor

- Add requirement that `verification_capsule.md` is the canonical verification report for the module.
- Add requirement that `requirements_delta.md` is the canonical implementer feedback and requirement-change report.
- Add requirement that `40.30_verification_glossary.md` is the canonical shared vocabulary for verification terms.
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
- `40.30_verification_glossary.md`
- `40.20_master_program_guide.md`

## Open Validation Needed

- Confirm whether HLR document-based IDs should be replaced with a centralized HLR registry in `thought_simulator_req`.
- Validate whether provenance creation notes should be normalized for split/merge-created TPs.
- Validate whether all legacy traceability content from `requirements_traceability.md` should be folded into `verification_capsule.md`.
- Confirm whether the new artifact naming convention should be extended to all modules immediately.

## Migration Notes

- Content from the legacy `updated_requirements.md` has been preserved here.
- Any future deltas should be appended here rather than reintroducing the deleted legacy file.
- Legacy filename references are retained as historical migration markers only and are not active canonical files.

## Change Integration Log

- Delta: Deterministic TP identity generation under `deterministic_mode`
	- Document modified: `20_requirements/20.30_tp_requirements.md`
	- Version/date of modification: updated May 27, 2026
	- Change: confirmed the deterministic TP identity requirement remains in the canonical TP requirements while updating the Purpose anchor.
	- Status: incorporated
- Delta: `harness.py` is the only execution entrypoint for module verification
	- Document modified: `20_requirements/20.30_tp_requirements.md`; `20_requirements/20.60_testing_and_validation.md` v0.3 (May 27, 2026)
	- Version/date of modification: updated May 27, 2026
	- Change: added harness-only verification entrypoint requirements and import-without-side-effects constraints.
	- Status: incorporated
- Delta: Each executed scenario emits HLR/LLR references at runtime and records them in the verification report
	- Document modified: `20_requirements/20.30_tp_requirements.md`; `20_requirements/20.60_testing_and_validation.md` v0.3 (May 27, 2026)
	- Version/date of modification: updated May 27, 2026
	- Change: added runtime HLR/LLR emission and persistence requirements for canonical verification records.
	- Status: incorporated
- Delta: Verification artifacts include serialized TP state, provenance, and history for replay/audit
	- Document modified: `20_requirements/20.30_tp_requirements.md`; `20_requirements/20.50_observability_requirements.md` v0.3 (May 27, 2026)
	- Version/date of modification: updated May 27, 2026
	- Change: required TP verification artifacts and snapshot content to include serialized state, provenance, and history for replay and audit fidelity.
	- Status: incorporated
- Delta: `verification_capsule.md` is the canonical verification report for the module
	- Document modified: `20_requirements/20.30_tp_requirements.md`; `20_requirements/20.60_testing_and_validation.md` v0.3 (May 27, 2026)
	- Version/date of modification: updated May 27, 2026
	- Change: designated the TP lifecycle verification capsule as the canonical module verification report.
	- Status: incorporated
- Delta: `requirements_delta.md` is the canonical implementer feedback and requirement-change report
	- Document modified: `20_requirements/20.30_tp_requirements.md`; `20_requirements/20.60_testing_and_validation.md` v0.3 (May 27, 2026)
	- Version/date of modification: updated May 27, 2026
	- Change: designated the TP lifecycle delta file as the canonical requirement-change log and preserved it as an audit artifact.
	- Status: incorporated
- Delta: `40.30_verification_glossary.md` is the canonical shared vocabulary for verification terms
	- Document modified: `20_requirements/20.30_tp_requirements.md`; `20_requirements/20.60_testing_and_validation.md` v0.3 (May 27, 2026)
	- Version/date of modification: updated May 27, 2026
	- Change: required TP verification terminology and module verification records to align with the canonical verification glossary.
	- Status: incorporated
- Delta: Verification artifacts are written into `artifacts/` instead of the module root
	- Document modified: `20_requirements/20.30_tp_requirements.md`; `20_requirements/20.90_interfaces_and_io.md` v0.3 (May 27, 2026)
	- Version/date of modification: updated May 27, 2026
	- Change: added artifact directory discipline for TP verification outputs and module interface documentation.
	- Status: incorporated
- Delta: The module preserves all migrated history when legacy report files are removed
	- Document modified: `20_requirements/20.60_testing_and_validation.md` v0.3 (May 27, 2026)
	- Version/date of modification: updated May 27, 2026
	- Change: added migration-history preservation requirements for canonical verification and requirement-change records.
	- Status: incorporated
- Delta: Negative-path coverage is reported alongside positive-path verification scenarios
	- Document modified: `20_requirements/20.30_tp_requirements.md`; `20_requirements/20.60_testing_and_validation.md` v0.3 (May 27, 2026)
	- Version/date of modification: updated May 27, 2026
	- Change: retained TP negative-path reporting requirements and added paired positive/negative coverage reporting in the general testing requirements.
	- Status: incorporated
- Delta: IO schema compatibility and artifact path expectations are documented in `software_description.md`
	- Document modified: `40_thought_simulator_playground/40.20_tp_lifecycle/software_description.md`; `20_requirements/20.90_interfaces_and_io.md` v0.3 (May 27, 2026)
	- Version/date of modification: updated May 27, 2026
	- Change: added the canonical TP requirements cross-reference to the lifecycle software description and required module IO schema and artifact path documentation in canonical I/O requirements.
	- Status: incorporated

All deltas listed above have been incorporated into the corresponding requirement documents as of May 27, 2026. No outstanding deltas remain.




