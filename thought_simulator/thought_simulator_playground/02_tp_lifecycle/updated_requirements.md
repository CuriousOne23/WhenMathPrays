# Updated Requirements

## Proposed Requirement Changes

- Add requirement that ThoughtPoint identity generation must be deterministic under deterministic_mode.
- Add requirement that harness.py is the only execution entrypoint for module verification.
- Add requirement that each executed scenario emits HLR/LLR references at runtime and records them in insights.md.
- Add requirement that verification artifacts include serialized TP state, provenance, and history for replay/audit.

## Rationale

- Deterministic execution is incomplete if TP IDs vary across equivalent runs.
- A single execution entrypoint prevents drift between ad hoc scripts and official verification flow.
- Runtime requirement emission enforces end-to-end traceability from test to requirement.
- Artifact-backed evidence improves auditability and accelerates regression debugging.

## Impacted Documents

- software_description.md
- prototype.py
- harness.py
- insights.md
- verification_summary.md
- requirements_traceability.md

## Open Validation Needed

- Confirm whether HLR document-based IDs should be replaced with a centralized HLR registry in thought_simulator_req.
- Validate whether provenance creation notes should be normalized for split/merge-created TPs.
