# Scalability Document Family Index

**Document:** notes/program/scalability/scalability_index.md  
**Status:** Navigation/governance index (non-normative).  
**Purpose:** Decide which scalability document(s) to open for a specific question. Scalability is a Path A / S2M program; Category Selection is one affected subsystem.

## How to use this index

Use this page to route questions by document role and authority.

- Open the program document for governing principles, expansion definition, regression versus progression, and decision states.
- Open the design document for the scalability software/reference design boundaries and analysis model.
- Open the gap analysis for current reuse/adapt/gap/deferred classification by capability area.
- Open the implementation plan for the bounded implementation envelope and acceptance-test scope.
- Open the implementation mapping for the approved first-pass module/test/output mapping used for bounded implementation.
- Open the user guide for practical operator or Agent steps for the accepted first bounded implementation.
- Open **implementation programs** below for the runner, the `scalability/` package, and the first-pass replay checks. Operator how-to for `run_scalability.py` lives in [scalability_user_guide.md](scalability_user_guide.md).

This index is intentionally brief and does not duplicate technical detail from the linked documents.

## Governance rule

This is the authoritative navigation index for the scalability document family.

Each family document should declare:
- what it is (role),
- authority/status,
- when it should be consulted,
- direct dependencies/successors.

New scalability documents should be registered here.

## Document family by role

### Program authority

- [scalability_program.md](scalability_program.md)  
  **What it is:** Governing Path A scalability and expansion-assurance program document.  
  **Status/authority:** Accepted program basis with first bounded implementation closeout recorded.  
  **Open when:** You need the definition of expansion, the regression/progression distinction, progression decisions, output discipline, or the phased plan.  
  **Relationship:** Receives the handoff from the Category Selection characterization program closeout; owns the Path A scalability concern; does not implement tooling.

### Gap/disposition mapping

- [scalability_gap_analysis.md](scalability_gap_analysis.md)  
  **What it is:** Audit-derived capability/disposition map for reuse, adaptation, gaps, unresolved items, and deferred concerns.  
  **Status/authority:** Accepted basis for reuse/gap/deferred classification and deferred-issue routing.  
  **Open when:** You need to determine current capability classification by area, including deferred preconversation/context scaling.  
  **Relationship:** Downstream of the program document and completed infrastructure audit; informs later design planning without prescribing implementations.

### Design authority (software/reference)

- [scalability_design.md](scalability_design.md)  
  **What it is:** Scalability software/reference design defining three-space separation, resource roles, relationship classifications, progression obligations, and reporting/disposition boundaries.  
  **Status/authority:** Accepted architecture/design authority for bounded implementation behavior.  
  **Open when:** You need the governing design model for analysis behavior, finding structure, and disposition logic before implementation decisions.  
  **Relationship:** Downstream of program/gap analysis; upstream of implementation plan and implementation mapping.

### Implementation envelope

- [scalability_implementation_plan.md](scalability_implementation_plan.md)  
  **What it is:** Bounded implementation envelope specifying first-pass scope, constraints, required reuse, output rules, and acceptance tests.  
  **Status/authority:** Accepted first-pass implementation envelope.  
  **Open when:** You are planning or authorizing implementation work and need to determine what is in scope, out of scope, and required to stop/escalate.  
  **Relationship:** Downstream of design/gap analysis; upstream of implementation mapping and bounded implementation verification.

### Implementation mapping (review gate)

- [scalability_implementation_mapping.md](scalability_implementation_mapping.md)  
  **What it is:** Approved first-pass implementation mapping from the envelope to concrete modules, interfaces, output layout, `.gitignore` needs, and acceptance-test coverage.  
  **Status/authority:** Approved implementation mapping for first bounded scalability implementation.  
  **Open when:** You are implementing or reviewing the first bounded scalability pass and need the approved mapping from the envelope to concrete repository surfaces.  
  **Relationship:** Downstream of implementation plan; authority for the accepted first bounded implementation pass.

### Practical guidance

- [scalability_user_guide.md](scalability_user_guide.md)  
  **What it is:** Practical guide for operators and Agents for the accepted first bounded scalability implementation.  
  **Status/authority:** Implemented first-pass operator guide (non-normative; report details remain provisional).  
  **Open when:** You need the implemented run procedure and report-interpretation sequence for bounded scalability analysis.  
  **Relationship:** Downstream of program/design/implementation outputs; does not define principles.

## Implementation programs

These are the executable surfaces for the accepted first bounded scalability implementation. They do not replace the user guide.

### Operator entry

- [run_scalability.py](../../../run_scalability.py)  
  **What it is:** Operator entry for bounded Path A scalability analysis of a proposal YAML against the established environment. Prints a `=== SCALABILITY TRACE ===` block and writes JSON and Markdown reports under `local_scalability/sessions/<session_id>/runs/`. It does not write proposal content into established Path A resources.  
  **Open when:** You need to run a scalability analysis.  
  **How to run:** [scalability_user_guide.md](scalability_user_guide.md) sections 3–6. Implemented flags: `--proposal-file`, `--session-id`, `--run-index` (all required), optional `--report-version` (default `1.0`) and `--run-regression`.

### Package (`scalability/`)

Bounded first-pass library used by `run_scalability.py`. Orchestration is [scalability/run.py](../../../scalability/run.py) (`run_scalability_check`).

- [scalability/__init__.py](../../../scalability/__init__.py) — package docstring: Path A scalability bounded first-pass package.
- [scalability/proposal.py](../../../scalability/proposal.py) — load and validate proposal YAML (`dictionary_entry`, `association`, `major`, `seed`).
- [scalability/discovery.py](../../../scalability/discovery.py) — discover established environment surfaces (category cues, majors, default active space, associations, licensed-extension scaffold).
- [scalability/relationships.py](../../../scalability/relationships.py) — classify proposal items against the discovered environment.
- [scalability/dependencies.py](../../../scalability/dependencies.py) — evaluate dependency presence for each proposal item.
- [scalability/obligations.py](../../../scalability/obligations.py) — compute progression obligations, including derived candidate obligations from association changes.
- [scalability/qualification.py](../../../scalability/qualification.py) — emit qualification-state visibility for obligations (first pass currently records `unresolved` when explicit qualification evidence is not established).
- [scalability/regression.py](../../../scalability/regression.py) — optional reused regression checks: [pipeline_readiness_check.py](../../../support/tools/pipeline_readiness_check.py) and [s2m_category_selection_replay.py](../../../support/tools/s2m_category_selection_replay.py).
- [scalability/disposition.py](../../../scalability/disposition.py) — determine disposition (`PROCEED`, `HOLD`, `REVISE`, `RETURN_TO_CHARACTERIZATION`) from classification, dependency, qualification, and regression evidence.
- [scalability/report.py](../../../scalability/report.py) — build the JSON report and compact Markdown summary.
- [scalability/session_store.py](../../../scalability/session_store.py) — persist reports under `local_scalability/`; a report identity is not overwritten.

### First-pass replay checks

- [support/tools/scalability_proposal_replay.py](../../../support/tools/scalability_proposal_replay.py) — `already_defined` stays distinct from `extension_of` and does not create progression obligations.
- [support/tools/scalability_progression_replay.py](../../../support/tools/scalability_progression_replay.py) — new dictionary, association, and major proposals produce the expected obligations and unresolved qualification.
- [support/tools/scalability_seed_hold_replay.py](../../../support/tools/scalability_seed_hold_replay.py) — generalized seed proposal routes to `HOLD` with unresolved seed-generalization qualification.
- [support/tools/scalability_output_boundary_replay.py](../../../support/tools/scalability_output_boundary_replay.py) — a proposal run writes ignored reports under `local_scalability/` and does not modify established Path A resources.
- [support/tools/pipeline_readiness_check.py](../../../support/tools/pipeline_readiness_check.py) — deterministic pipeline-readiness check reused as a `--run-regression` script.

## Extensibility

This family is extensible. Register new scalability documents here with role, status, consult trigger, and dependency relationships.
