# Scalability User Guide

**Document:** notes/program/scalability/scalability_user_guide.md  
**Status:** Implemented first-pass operator guide (non-normative; report details remain provisional).  
**Date:** 2026-11-23  
**Purpose:** Document how to run and interpret the accepted first bounded Path A scalability implementation as it exists now.

## 1) Purpose and boundary

Scalability analyzes a **proposal** against the established Path A environment.  
It evaluates identity/delta effects, dependencies, progression obligations, qualification visibility, optional regression checks, and final disposition.

Proposal input is hypothetical analysis input only.  
A scalability run does **not** write proposal content into established Path A YAML/reference resources.

## 2) Current supported resource roles

First bounded implementation roles:

- **Proposal-capable (implemented):**
  - `dictionary_entry`
  - `association`
  - `major`
  - `seed` (accepted as proposal class, but treated as unresolved/historical in first pass)

- **Derived surface (not independently proposal-capable):**
  - `candidate` (derived from association/major consequences; not a standalone proposal class)

- **Constraint/licensing surface (bounded observation only):**
  - Licensed Region scaffold is observed via existing bounded `LICENSED_EXTENSIONS`; no generalized licensing model is implemented.

- **Historical/unresolved in first pass:**
  - generalized Seed expansion routes unresolved behavior (`HOLD` path).

- **Deferred/not implemented for expansion analysis in first pass:**
  - Reference object/table expansion analysis.

## 3) Proposal preparation

Runner input is a YAML file with:

- top-level `proposal_id` (required),
- top-level `items` (required, non-empty array),
- per item:
  - `item_id` (optional; default generated if missing),
  - `resource_class` (required),
  - `identity` (required object),
  - `delta` (required object),
  - `provenance` (required object),
  - optional `advisory_intent`, `expected_surfaces`.

Supported `resource_class` values in current implementation:
- `dictionary_entry`, `association`, `major`, `seed`.

Identity is validated separately from delta:
- identity = what existing structure the item addresses;
- delta = what change is proposed.

Example fixtures are in [support/scalability/examples/](../../../support/scalability/examples):
- [proposal_already_defined.yaml](../../../support/scalability/examples/proposal_already_defined.yaml)
- [proposal_dict_extension.yaml](../../../support/scalability/examples/proposal_dict_extension.yaml)
- [proposal_dict_new_mapping.yaml](../../../support/scalability/examples/proposal_dict_new_mapping.yaml)
- [proposal_association_add.yaml](../../../support/scalability/examples/proposal_association_add.yaml)
- [proposal_major_add.yaml](../../../support/scalability/examples/proposal_major_add.yaml)
- [proposal_seed_generalized.yaml](../../../support/scalability/examples/proposal_seed_generalized.yaml)

Operator meaning of key relationship outcomes:
- `already_defined`: identity+relation already exists in established environment; no new progression obligation for that item.
- `extension_of`: item targets an existing structure but adds a new relation/member; progression obligations are expected.

## 4) Running scalability

From [pathA_short_sim/](../../../), run:

```bash
python run_scalability.py --proposal-file <path> --session-id <id> --run-index <n> [--report-version <v>] [--run-regression]
```

Implemented arguments:
- `--proposal-file` (required): proposal YAML path.
- `--session-id` (required): session label (validated by runtime).
- `--run-index` (required): integer, must be `>= 1`.
- `--report-version` (optional): default `1.0`.
- `--run-regression` (optional flag): when present, runs reused regression checks and records them in the report.

## 5) Run flow (implemented)

Current flow:
1. Load/validate proposal YAML.
2. Discover established environment surfaces (dictionary cues, majors, default active space, endpoint associations, licensed scaffold table).
3. Classify item relationships (`already_defined`, `extension_of`, `additional_to`, `missing`, `unresolved` as applicable).
4. Evaluate dependency presence for each proposal item.
5. Compute progression obligations for supported classes (including derived candidate obligations from association changes).
6. Determine qualification state visibility for obligations.
7. Optionally run reused regression checks (`--run-regression`).
8. Determine disposition from classification/dependency/qualification/regression evidence.
9. Emit JSON and Markdown reports under local ignored output.

Regression is kept separate from progression/qualification in both logic and report structure.

## 6) Reports and output

Output root:
- [local_scalability/](../../../local_scalability)

Per run:
- `local_scalability/sessions/<session_id>/runs/<run_index>__scalability_check__<version>.json`
- `local_scalability/sessions/<session_id>/runs/<run_index>__scalability_check__<version>.md`

Observed JSON report sections (current implementation):
- `identity`
- `proposal`
- `relationships`
- `dependencies`
- `progression_obligations`
- `qualification`
- `regression`
- `findings`
- `disposition`

Observed Markdown report behavior (current implementation):
- compact summary with identity, disposition, and counts.

Report content/field details remain provisional per program/plan authority; required evidence separation is the stable contract.

## 7) Qualification states

Authority-level qualification state vocabulary:
- `qualified`
- `unqualified`
- `deferred_bounded`
- `unresolved`

Current first-pass implementation behavior:
- qualification entries are currently emitted as `unresolved` when explicit existing qualification evidence is not established.
- seed generalization also routes unresolved behavior in first pass.

Do not infer missing qualification evidence as `qualified`.
Do not invent a qualification registry.

## 8) Dispositions

Disposition labels in current system:
- `PROCEED`
- `HOLD`
- `REVISE`
- `RETURN_TO_CHARACTERIZATION`

Concise operator meanings:
- `PROCEED`: no blocking incompatibility/dependency/qualification condition was found for this bounded analysis run.
- `HOLD`: proposal is recognized, but unresolved qualification or another bounded blocking condition prevents acceptance.
- `REVISE`: proposal conflicts with explicit structure/contract constraints and must be adjusted before re-analysis.
- `RETURN_TO_CHARACTERIZATION`: at least one obligation is explicitly unqualified and must be routed to characterization work.

Operator guidance:
- Regression `pass` does **not** by itself establish progression qualification.
- A run may complete successfully and still correctly return `HOLD` when qualification evidence remains `unresolved`.
- `--run-regression` augments evidence; it does not replace progression/qualification assessment.

## 9) Finding visibility (operator view)

Findings are structured for traceability using:

`ORIGIN → WHERE → WHAT → WHY → EVIDENCE → CONSEQUENCE → ROUTE`

Operator interpretation:
- ORIGIN: which proposal item triggered the finding.
- WHERE: affected surface/identity.
- WHAT: observed classification/dependency/obligation condition.
- WHY: rule basis used.
- EVIDENCE: obligation/dependency/qualification details.
- CONSEQUENCE: impact on progression follow-up.
- ROUTE: disposition routing context.

This is scalability evidence visibility, not root-cause diagnostics.

## 10) What scalability does not do

The first bounded scalability implementation does not:
- modify established Path A resources;
- auto-install or auto-promote proposal content;
- perform root-cause diagnostics;
- invent qualification evidence;
- generalize excluded classes (generalized Seed model, generalized Licensed Region machinery, reference object/table expansion analysis).

## 11) Post-analysis boundary

Controlled integration/promotion of a user-accepted proposal into established/versioned Path A resources is outside the current scalability implementation.

That separate program is not yet defined.

## Related programs

The runner, `scalability/` package modules, and first-pass replay checks are registered in [scalability_index.md](scalability_index.md) under Implementation programs. This guide remains the operator how-to for [run_scalability.py](../../../run_scalability.py).

## Related references

- [scalability_program.md](scalability_program.md)
- [scalability_design.md](scalability_design.md)
- [scalability_gap_analysis.md](scalability_gap_analysis.md)
- [scalability_implementation_plan.md](scalability_implementation_plan.md)
- [scalability_implementation_mapping.md](scalability_implementation_mapping.md)
- [scalability_index.md](scalability_index.md)
