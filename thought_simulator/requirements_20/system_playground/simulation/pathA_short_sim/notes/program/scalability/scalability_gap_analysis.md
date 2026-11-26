# Path A Scalability Gap Analysis

**Document:** notes/program/scalability/scalability_gap_analysis.md  
**Status:** Accepted gap/disposition basis for bounded scalability implementation decisions.  
**Date:** 2026-11-23  
**Purpose:** Convert the completed Path A scalability infrastructure audit into a decision-quality classification of reusable capability, adaptation needs, genuine gaps, unresolved items, and deferred concerns. This document does not design implementations.

## Scope and method

This gap analysis is grounded in:
- [scalability_program.md](scalability_program.md)
- the completed scalability infrastructure audit findings
- existing repository evidence already identified in that audit

Classifications used:
- `REUSE_AS_IS`
- `ADAPT_OR_INTEGRATE`
- `GAP`
- `UNRESOLVED`
- `DEFERRED`

## Capability map

| Capability area | Required scalability function | Existing Path A capability | Status | Evidence | Known boundary | Why boundary matters | Future design obligation (functional, non-implementation) |
|---|---|---|---|---|---|---|---|
| 1) Expansion detection | Detect that an expansion occurred and identify affected surfaces/combinations. | Program-level expansion definition and review discipline exist. | `ADAPT_OR_INTEGRATE` | [scalability_program.md](scalability_program.md), [README.md](../../../README.md) | No executable expansion-diff detector across seed/association/candidate/category/licensed-region/reference surfaces. | Scalability checks can miss newly created obligations unless expansion deltas are consistently identified. | Define a repeatable expansion-identification function that maps a change-set to affected scalability surfaces/obligations. |
| 2) Dependency alignment | Verify that expansion in one surface has required support in dependent surfaces. | Localized structural checks exist (schema-family enforcement, relation/schema replay checks). | `ADAPT_OR_INTEGRATE` | [../../../idob/registry.py](../../../idob/registry.py), [../../../support/idob_schemas/idob_object.v1.schema.json](../../../support/idob_schemas/idob_object.v1.schema.json), [../../../support/tools/s2m_schema_replay.py](../../../support/tools/s2m_schema_replay.py), [../../../support/tools/schema_enum_replay.py](../../../support/tools/schema_enum_replay.py) | Checks are targeted and local; no cross-surface dependency closure check. | Expansion can appear valid locally while downstream support is incomplete. | Define dependency-alignment obligations spanning expansion-sensitive surfaces and a way to evaluate them consistently. |
| 3) YAML/reference validation | Validate structural integrity/contract conformance of expansion-sensitive YAML/reference assets. | YAML loading/shape filtering and several schema-based replay checks exist. | `ADAPT_OR_INTEGRATE` | [../../../s2m/loader.py](../../../s2m/loader.py), [../../../support/idob_schemas/s2m_connection.v1.schema.json](../../../support/idob_schemas/s2m_connection.v1.schema.json), [../../../support/tools/s2m_schema_replay.py](../../../support/tools/s2m_schema_replay.py) | Validation coverage is uneven; some loaders drop invalid entries without unified diagnostics. | Silent filtering can obscure support gaps and reduce auditability. | Define unified validation expectations for relevant YAML/reference classes and explicit failure/report behavior for invalid structures. |
| 4) Regression | Re-check previously characterized behavior after expansion. | Extensive replay/check tooling already exists. | `REUSE_AS_IS` | [../../../support/tools/](../../../support/tools/), [../../../support/tools/pipeline_readiness_check.py](../../../support/tools/pipeline_readiness_check.py), [../../../support/tools/s2m_category_selection_replay.py](../../../support/tools/s2m_category_selection_replay.py), [../../../replay_parity_harness.py](../../../replay_parity_harness.py) | Current suite is broad but case-script-based rather than expansion-index-driven. | Regression can be run today; no need to rebuild core replay infrastructure. | Reuse existing replay infrastructure as the regression leg of scalability checks. |
| 5) Progression/new-coverage detection | Detect new reachable/unqualified combinations created by expansion. | Manual coverage/accounting discipline exists in program docs and coverage map process. | `GAP` | [../coverage_map.md](../coverage_map.md), [../status.md](../status.md), [scalability_program.md](scalability_program.md) | No implemented mechanism that computes new obligations from expansion deltas. | Green regression does not imply qualified new coverage. | Define a progression-obligation identification function that distinguishes prior-qualified vs newly-unqualified combinations. |
| 6) Characterization qualification | Determine whether newly created obligations are qualified, deferred, or require reopening characterization. | Explicit qualification discipline exists in bounded characterization program work. | `ADAPT_OR_INTEGRATE` | [../category_supported_admission_characterization.md](../category_supported_admission_characterization.md), [../category_selection_characterization_experiment_plan.md](../category_selection_characterization_experiment_plan.md) | Qualification discipline is campaign-specific, not generalized across Path A scalability surfaces. | Without generalized qualification handling, expansion decisions remain ad hoc. | Define a scalability-wide qualification/defer/reopen decision function that can reference existing characterization programs. |
| 7) Characterization/replay execution | Execute bounded checks/characterization runs and preserve reproducible evidence. | One-run characterization execution and replay flows are implemented and used. | `REUSE_AS_IS` | [../../../run_examples.py](../../../run_examples.py), [../category_selection_characterization_reference.md](../category_selection_characterization_reference.md), [../../../support/tools/characterization_artifact_replay.py](../../../support/tools/characterization_artifact_replay.py) | Current characterization implementation is bounded in scope/type. | Execution/persistence discipline is already operational and reusable as infrastructure. | Reuse existing bounded execution/persistence discipline where scalability checks require characterization evidence. |
| 8) Artifact persistence | Ensure canonical identity, no-overwrite writes, and stable evidence persistence. | Canonical identity and hard non-overwrite persistence are implemented. | `REUSE_AS_IS` | [../../../characterization/artifacts.py](../../../characterization/artifacts.py), [../../../run_examples.py](../../../run_examples.py) | Scope today is characterization artifact classes. | Proven persistence semantics should not be re-invented. | Reuse persistence invariants/discipline for any future scalability evidence artifacts. |
| 9) Generated/local-output handling | Keep generated session outputs local/ignored; preserve tracked-vs-generated boundary. | Repository-level and local characterization ignore rules and policy already exist. | `REUSE_AS_IS` | [../../../../../../../../.gitignore](../../../../../../../../.gitignore), [../../../local_characterization/.gitignore](../../../local_characterization/.gitignore), [../../../user_guide.md](../../../user_guide.md) | Existing conventions are centered on characterization outputs. | Output-discipline baseline already exists and is enforceable. | Reuse existing local/generated-output boundary discipline for scalability outputs. |
| 10) Machine-readable reporting | Emit consistent machine-readable status/evidence for scalability decisions. | `.tschar.json` evidence exists; some tools emit structured JSON/YAML outputs. | `ADAPT_OR_INTEGRATE` | [../../../characterization/artifacts.py](../../../characterization/artifacts.py), [../../../replay_parity_harness.py](../../../replay_parity_harness.py), [../../../generate_cutover_readiness_report.py](../../../generate_cutover_readiness_report.py) | Structured outputs are tool-specific; no unified scalability report contract is implemented. | Decision flow requires consistent machine-readable states across capability areas. | Define scalability report requirements that consistently represent expansion, regression, progression obligations, and disposition states. |
| 11) Human/Agent-readable reporting | Present clear operator/Agent-facing status, evidence location, and disposition rationale. | CHAR TRACE, debug workflow, and indexed program documentation already exist. | `ADAPT_OR_INTEGRATE` | [../../../run_examples.py](../../../run_examples.py), [../../../pathA_dbug.py](../../../pathA_dbug.py), [scalability_index.md](scalability_index.md), [../category_selection_index.md](../category_selection_index.md) | Scalability user guidance is still placeholder and not yet execution-ready. | Human/Agent execution consistency depends on explicit routing and interpretation guidance. | Complete scalability-facing operator/Agent guidance aligned with final gap classifications and decision states. |
| 12) Progression-decision support | Support `PROCEED` / `HOLD` / `REVISE` / `RETURN_TO_CHARACTERIZATION` decisions with evidence. | Decision-state vocabulary exists in program-level proposal and review-gate discipline in related plans. | `ADAPT_OR_INTEGRATE` | [scalability_program.md](scalability_program.md), [../category_selection_characterization_experiment_plan.md](../category_selection_characterization_experiment_plan.md) | No implemented evidence-aggregation path from checks to decision-state output. | Decision terms exist conceptually but cannot yet be produced consistently from current tooling. | Define functional decision-support flow that consumes regression/progression/qualification evidence and yields explicit disposition states. |

## Deferred concern migration

### Preconversation / contextual scaling

**Status:** `DEFERRED`.

**Current handling:**  
Bounded tests requiring preconversation may provide explicit prior context through the existing run-time `prior_context` surface. The supplied context is part of the qualified run condition and should be recorded with run evidence so the observation remains bounded and reproducible.

**Present non-goal:**  
Do not create a generalized preconversation fixture system, dedicated CIL/CEx scalability framework, or specialized preconversation tooling at this stage.

**Future trigger:**  
Revisit this issue if repeated, larger, or more complicated scalability work demonstrates that run-specific `prior_context` customization is insufficient to qualify, reproduce, maintain, or consistently evaluate contextual obligations affecting CIL/CEx and downstream Path A/S2M behavior.

**Future design obligation (if triggered):**  
Define reusable preconversation/context fixtures and CIL/CEx contextual-scaling checks only after the trigger condition is met and formally authorized.

## Closing synthesis

### Reuse as-is

- Regression replay/check infrastructure.
- Characterization/replay execution discipline.
- Artifact persistence invariants (canonical identity, hard non-overwrite).
- Generated/local-output handling discipline.

### Adapt/integrate

- Expansion detection.
- Dependency alignment.
- YAML/reference validation.
- Characterization qualification (generalized across scalability surfaces).
- Machine-readable reporting unification.
- Human/Agent-readable scalability reporting/guidance.
- Progression-decision support realization.

### New capability potentially required

- Progression/new-coverage detection that computes newly created obligations from expansion deltas and separates them from already-qualified behavior.

### Unresolved/deferred

- Preconversation/context scaling (`DEFERRED`) under current bounded `prior_context` handling and recorded trigger.
- Any unresolved requirement details for cross-surface dependency closure semantics and progression-obligation semantics pending design-phase definition.
