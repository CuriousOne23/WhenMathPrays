# Category Selection Characterization Reference

**Document:** notes/program/category_selection_characterization_reference.md  
**Status:** Draft bounded software-reference contract for characterization infrastructure.

## 1) Purpose

Define the bounded software contract for category-selection characterization infrastructure: how characterization runs are invoked, dispatched, measured, identified, and stored as independent artifacts without changing category-selection meaning logic.

This reference is a coordinated sibling of [category_selection_program_reference.md](category_selection_program_reference.md):

- [category_selection_program_reference.md](category_selection_program_reference.md): bounded category-selection realization contract.
- This document: bounded characterization instrumentation and experimentation support contract.

Milestone-1 characterization infrastructure implementation/verification closeout evidence is recorded in [category_selection_characterization_milestone1_closeout.md](category_selection_characterization_milestone1_closeout.md). This document remains the method/contract reference.

## 2) Authority and boundaries

This reference is implementation-facing for characterization infrastructure only.  
It does **not** authorize changes to normative TS requirements or category-selection meaning policy.

Characterization in this document:

- observes and exercises the existing category-selection realization,
- provides measurement and artifact discipline,
- supports controlled multi-run characterization studies.

Characterization in this document does **not**:

- create a competing category-selection path,
- create a competing meaning path,
- define the final no-category decision rule,
- define threshold/region/hysteresis policy,
- prewrite scientific conclusions.

Entropy-related characterization in this document is governed by the Path-A process-level entropy principle in [20.705_patha_pathb_flow.md](../../../20.705_patha_pathb_flow.md) and by normative ISc entropy/ΔH requirements in [20.45_ts_isc_scoring.md](../../../20.45_ts_isc_scoring.md). Characterization instrumentation does not define entropy ownership, entropy normalization, first-cycle ownership, or entropy carrier design.

## 3) Category-selection document family

For the complete category-selection document map, document roles, authority relationships, software references, characterization documents, and observation records, see:

[category_selection_index.md](category_selection_index.md)

## 4) Related documents

- [category_selection_proposal.md](category_selection_proposal.md)
- [category_selection_research_plan.md](category_selection_research_plan.md)
- [category_selection_stage1_modification_map.md](category_selection_stage1_modification_map.md)
- [category_selection_program_reference.md](category_selection_program_reference.md)
- [category_selection_observation.md](category_selection_observation.md)
- [user_guide.md](../../user_guide.md)

## 5) Relationship to existing run workflow

Existing workflow remains valid:

`[run_examples.py](../../run_examples.py) -> run.log -> [pathA_dbug.py](../../pathA_dbug.py)`

Characterization adds independent outputs and does not replace this workflow.

- `run.log` remains the human-readable execution log/debug stream.
- Characterization artifacts are separate machine-readable records for experiment evidence.
- [pathA_dbug.py](../../pathA_dbug.py) continues to operate on `run.log`; it is not the characterization artifact reader.

## 6) run_examples.py characterization interface

[run_examples.py](../../run_examples.py) is the primary characterization entrypoint.

### 6.1 Baseline compatibility

Current flags (for example `--no-s2m-seed`, `--no-category-observations`) remain supported.  
Characterization parameters are additive and must not break baseline usage.

### 6.2 Required characterization parameters

The characterization interface shall include parameterized controls covering:

- `characterization_type` (required when characterization mode is requested),
- session identity selection,
- output destination,
- run cardinality/repetition controls,
- optional parameter payload for type-specific sweeps.

Exact flag spelling may be finalized in implementation, but semantics are fixed by this reference.

Milestone 1 currently establishes the bounded single-run `infra_smoke` subset of this interface; broader multi-run/session orchestration capabilities remain future work.

## 6.3 Milestone-1 shared-execution and non-interference contract

For milestone-1 characterization:

1. Characterization observes the same caller-selected TS execution available to ordinary execution.
2. TS case/input selection is an execution responsibility, not a characterization parameter.
3. Characterization types (including `infra_smoke`) do not own sentence selection, prior context, category-selection enablement, S2M enablement, or other TS-affecting controls.
4. Characterization observes the completed runtime result and must not mutate that result.
5. One characterization invocation performs one TS execution.
6. Characterized-versus-uncharacterized non-interference comparisons must hold TS-affecting controls constant.
7. Verification has two levels:
   - **Level A (primary):** TS behavioral verification using runtime/replay/testbench surfaces.
   - **Level B (supplemental):** characterization-evidence verification for faithful recording of selected runtime observations.
8. Characterization artifact equality is not sole authority for TS deterministic replay or non-interference.
9. Full runtime-result equality may differ only for explicitly approved non-behavioral metadata.
10. The only approved non-behavioral exclusion at this stage is `created_at_utc` timestamp metadata.
11. Behavioral comparison may exclude only this approved timestamp metadata.
12. Exclusions must not be expanded merely to make tests pass.
13. Any future difference outside approved non-behavioral metadata requires investigation before exclusion.

## 7) Characterization-type variable and dispatcher

Characterization execution is selected by `characterization_type`.

### 7.1 Dispatcher contract

A dispatcher maps `characterization_type` to an independently implemented characterization routine.

Required behavior:

1. Validate requested type.
2. Resolve routine.
3. Execute routine under one characterization session.
4. Emit one artifact per run (and optional aggregate summaries).
5. Fail explicitly for unknown types (no silent fallback).

### 7.2 Independent routine contract

Each routine is implemented independently and receives:

- immutable run/session identity context,
- simulation invocation controls,
- type-specific parameters.

Each routine emits standardized measurement fields plus type-specific fields.

## 8) Characterization session model

A characterization session is a bounded execution context grouping one or more runs under shared intent.

Required session properties:

- unique `session_id` within the characterization artifact/session namespace,
- monotonic `run_index` within session,
- immutable creation metadata,
- stable provenance fields copied into every artifact,
- hard non-overwrite artifact allocation.

### 8.1 Unique/session-number allocation

Session/run identity allocation must prevent filename collision:

- unique `session_id` within the characterization artifact/session namespace,
- deterministic zero-padded `run_index`,
- allocation logic that refuses to reuse an existing artifact path.

If a collision is detected, the program must fail the write and must not overwrite an existing artifact.
Artifact metadata is authoritative for session/run identity; filenames are informative and are not the sole identity authority.
UUID-style global uniqueness is not required by this reference unless a separate normative authority later requires it.

### 8.2 Hard non-overwrite requirement

Characterization artifact writes must be create-only semantics (fail if target exists).  
Overwriting existing characterization artifacts is prohibited.

## 9) Artifact model

### 9.1 Independent artifacts

Characterization artifacts are independent from `run.log` and independent from debug markdown outputs.  
They are the machine-readable evidence input for future analysis and [category_selection_observation.md](category_selection_observation.md) entries.

### 9.2 Common TS-wide characterization extension

Use one TS-wide characterization artifact extension:

- `.tschar.json`

All characterization types use this extension for per-run records to keep downstream tooling stable.
Within this extension:

- `.tschar` identifies the artifact class as TS characterization evidence.
- `.json` identifies the internal serialization format.

Generated characterization artifacts are intended to be excluded from Git using the dedicated pattern `*.tschar.json` (implementation to add this rule later; no `.gitignore` edit is performed in this document).

### 9.3 Informative filenames

Filenames must be informative and include at minimum:

- characterization type,
- session id,
- run index,
- UTC timestamp or equivalent stable temporal marker.

Temporal markers are useful for readability/order but are not the authoritative uniqueness mechanism.

### 9.4 Internal provenance/identity payload

Every artifact must include internal provenance/identity fields:

- `session_id`
- `run_index`
- `characterization_type`
- invocation/config metadata
- source sentence/prior-context inputs used for the run
- software identity (version/commit hash when available)
- creation timestamp

## 10) Required measurements

At minimum, each characterization run must preserve category-selection measurement outputs needed by current research scope, including:

- normalized category distribution,
- top category,
- top-vs-second margin,
- entropy,
- confidence,
- rationale,
- provenance,
- downstream candidate relevance/selection states,
- legitimation/refusal state,
- final participation/composite summary.

If a required measurement is unavailable from current runtime output, the run must explicitly mark it unavailable rather than fabricating a value.

## 11) Multi-run category-support / unsupported-space characterization

A dedicated support-boundary characterization capability is required to support repeated controlled runs where category support behavior can be observed under varied evidence/category-space conditions.

Research sequence remains:

observe -> characterize -> design

This characterization exists to gather evidence for possible later design of a robust no-category function; it does not presuppose that such a function is already defined.

This characterization must:

- support multiple runs in one session,
- preserve per-run identity and measurement outputs,
- emit artifacts for each run without overwrite,
- avoid introducing a no-category decision rule.

It does not assume beforehand:

- that a single no-category region exists,
- that the boundary is sharp,
- that the boundary is a threshold,
- that weak support within available inventory and poor representation by the inventory are already separable,
- that hysteresis is required.

Characterization may reveal a threshold-like transition, gradient behavior, ambiguity region, overlapping conditions, inventory-sensitive behavior, sequential instability, or another pattern.

## 12) Campaign orchestration (optional higher-level layer)

A higher-level campaign orchestrator may be added later to schedule multiple characterization sessions/types.  
If present, it coordinates sessions; it does not replace type routines or alter routine-level contracts.

## 13) Observation-driven extensibility

Unforeseen characterization types may be added when observation reveals new questions.

Required addition path:

1. define the new type and intent,
2. add independent routine,
3. register with dispatcher,
4. preserve standardized artifact identity/measurement contract,
5. record addition in [category_selection_index.md](category_selection_index.md) family map if documentation scope expands.

## 14) .gitignore and repository hygiene

Characterization output directories/files must be excluded from source control by default via `.gitignore` rules, except where a specific reviewed artifact set is intentionally committed.

The default posture is: generated characterization artifacts are runtime outputs, not source files.

## 15) user_guide relationship

[user_guide.md](../../user_guide.md) remains the reader-facing operator manual for normal simulator output and debug workflow.

When characterization controls are implemented, [user_guide.md](../../user_guide.md) should document:

- how to invoke characterization types,
- where artifacts are written,
- how characterization outputs differ from `run.log`,
- how characterization evidence feeds observation reporting.

## 16) Explicit no-rule constraint (critical)

This reference does **not** define the no-category decision rule.

Specifically not defined here:

- no-category threshold policy,
- boundary-region policy,
- entropy/margin cutoffs,
- persistence/hysteresis policy,
- final unsupported-inventory decision policy.

Characterization records evidence; it does not settle the final decision function in this stage.
