# Promotion Protocol

Version: 1.0
Status: Active
Owner: Thought Simulator Governance
Last Updated: 2026-05-28

## 1. Purpose and Scope

This protocol governs promotion of exploratory ideas into canonical artifacts.

It applies to transitions from:

- `20_requirements` (exploratory reasoning)
- `40_thought_simulator_playground` (exploratory implementation)

into canonical layers:

- `10_thought_simulator_req` (canonical requirements)
- `50_thought_simulator_design` (canonical design)
- `30_verification` (canonical evidence)

This protocol is governance policy. It is not a requirement specification.

## 2. Epistemic Boundary (Normative)

- Exploratory layers may influence canonical artifacts through human judgment.
- Exploratory layers are not ground truth and do not participate in formal traceability edges.
- Canonical layers are authoritative and trace only to canonical layers.
- Verification points only upward into canonical governance.

## 3. Entry Criteria for Promotion

A candidate may be promoted only when all criteria are met:

1. The candidate has a clear problem statement and intended canonical destination.
2. The candidate is reproducible enough for reviewer inspection (notes, artifacts, or replayable method).
3. The candidate includes explicit rationale for why promotion is needed now.
4. The canonical target can absorb the change without structural reorganization.
5. The promotion does not require formal trace edges from exploratory artifacts.

For all new `40.*` playground modules, an additional gate applies:

6. The module `software_description.md` must be explicitly human-approved before any verification artifacts, prototype code, harness code, requirement deltas, or promotion artifacts are generated.

## 4. Required Evidence Package

Each promotion submission must include:

1. Rationale summary: concise explanation of decision intent and expected impact.
2. Prototype notes: key implementation observations from exploratory work.
3. Reasoning trail: alternatives considered, rejected options, and tradeoffs.
4. Verification intent: how canonical verification will evidence the promoted decision.

Evidence may originate in exploratory docs, but canonical decisions are approved from the summarized package, not from direct trace links.

## 5. Review and Approval

Review steps:

1. Submission completeness check against Sections 3 and 4.
2. Boundary check: confirm no exploratory-to-canonical trace edges are introduced.
3. Canonical fit check: confirm destination layer and file scope are correct.
4. ID integrity check: confirm canonical IDs remain valid and stable.
5. Verification fit check: confirm evidence plan points upward within canonical layers.

Approval conditions:

1. All review steps pass.
2. At least one designated reviewer approves.
3. No unresolved boundary or traceability violations remain.

## 6. Non-Promotable Content

The following must not be promoted directly:

1. Raw exploratory contradictions without resolved decision framing.
2. Incomplete or non-reproducible claims.
3. Speculative notes lacking rationale and impact statement.
4. Exploratory links presented as canonical trace dependencies.
5. Changes that mutate canonical structure without explicit governance approval.
6. Verification or promotion artifacts generated from a new `40.*` module before explicit approval of that module `software_description.md`.

## 7. Rationale Recording Requirements

Promotion rationale must be recorded in human-readable governance channels:

1. ADR-style decision note (recommended for non-trivial promotions).
2. Promotion summary in relevant docs context.
3. Commit messages that clearly state rationale and boundary compliance.

These records preserve why without elevating exploratory artifacts into formal trace dependencies.

## 8. Canonical ID and Traceability Integrity

1. Canonical IDs are created and maintained only in canonical layers.
2. Existing canonical IDs must not be repurposed to mean different concepts.
3. Supersession must be explicit and canonical-to-canonical.
4. Formal trace edges must remain canonical-to-canonical only.
5. Exploratory references may appear as narrative context but never as formal trace keys.

## 9. Anti-Pollution Controls

To prevent trace pollution from exploratory layers:

1. Do not add `satisfies`, `proves`, `derived-from`, or `supersedes` edges that target exploratory paths.
2. Do not treat exploratory file paths as traceable authorities.
3. Keep exploratory references in rationale prose, not in canonical relation metadata.
4. Reject any promotion that weakens canonical asymmetry.

## 10. Roles and Responsibilities

Contributors:

1. Prepare complete evidence package.
2. Preserve asymmetry and avoid exploratory trace edges.
3. Propose canonical changes with minimal scope and clear rationale.

Reviewers:

1. Enforce boundary and traceability integrity.
2. Validate canonical destination and ID stability.
3. Approve only when evidence, rationale, and governance checks are complete.

Governance maintainers:

1. Maintain this protocol as stable policy.
2. Version changes explicitly.
3. Update related governance guidance when boundary rules evolve.

## 11. Change Control

- This protocol is versioned governance policy.
- Revisions require explicit version increment and short revision summary.
- Any revision that changes epistemic boundary rules requires governance-level review.
