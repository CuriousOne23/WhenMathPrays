# Path A Scalability Implementation Plan

**Document:** notes/program/scalability/scalability_implementation_plan.md  
**Status:** Accepted implementation envelope for first bounded scalability pass.  
**Date:** 2026-11-23  
**Purpose:** Freeze the physical and software contract for the first bounded implementation of Path A scalability. This document does not re-open architectural questions settled in `scalability_design.md`. It defines what an Agent may implement now and what it must not invent.

## Relationship to existing documents

- Governing principles, three-space separation, resource roles, relationship classifications, progression obligations, finding visibility, and dispositions are defined in [scalability_design.md](scalability_design.md).
- Reuse-versus-adapt decisions and deferred concerns are recorded in [scalability_gap_analysis.md](scalability_gap_analysis.md).
- The program document remains the authority for expansion definition and the regression/progression distinction.
- This plan is the implementation envelope. It does not freeze final report field names beyond the minimum evidence required below, nor does it complete the user guide.

## Directory contract

The following external locations are fixed for the first implementation:

```
pathA_short_sim/
├── scalability/                  # runtime code for analysis
├── support/
│   └── scalability/              # tracked reference material, schemas, or example proposals if needed
├── local_scalability/            # generated sessions and reports (ignored)
└── notes/program/scalability/    # program, design, gap analysis, this plan, index, user guide
```

These four top-level locations are frozen. The Agent may inspect existing short-sim conventions and choose the internal module and package layout beneath `scalability/`. Exact Python filenames are not prescribed here.

## Local / generated-output rule

Generated scalability sessions and reports belong under `local_scalability/` and are not committed.

Reuse the existing ignored/local-output discipline already present for characterization outputs (see gap analysis). The implementation must add or extend `.gitignore` so that `local_scalability/` (and any equivalent session directory) is ignored. Tracked artifacts remain limited to source, reference material, program documents, and deliberately promoted formal conclusions.

## Input contract

Proposal YAML is analysis input only. It is never written into established Path A resources by a scalability run.

Proposals are supplied by explicit filesystem path at invocation time (command-line argument or equivalent). They are not assumed to reside in any tracked directory. Optional tracked example proposals, if desired for documentation or tests, may be placed under `support/scalability/examples/`; these remain reference material and are not treated as established Path A resources. Runtime proposals stay outside the established environment for the entire run.

Minimum required content for a proposal:
- proposal identity (stable id for the analysis run);
- for each proposed item:
  - resource class (from the supported set below);
  - resource identity (exact key or structural signature used by the established system);
  - proposed delta (the concrete addition, extension, or change);
  - provenance (source of the proposal item);
- optional advisory intent or expected surfaces (ignored as evidence; may be echoed in the report).

Fail closed if identity or structural content required for the analysis is missing.

## Output contract

A scalability run produces a report (machine-readable and human/Agent-readable views of the same evidence). Exact field names remain provisional; the following evidence must be present:

- proposal and item/delta identity;
- relationship classification(s) with comparison basis and evidence;
- affected dependencies and missing support;
- progression-obligation inventory (newly reachable-and-valid combinations);
- qualification state for each obligation (`qualified`, `unqualified`, `deferred_bounded`, `unresolved`);
- regression result (pass / fail / not-run), kept visibly separate from progression results;
- findings that follow ORIGIN → WHERE → WHAT → WHY → EVIDENCE → CONSEQUENCE → ROUTE;
- final disposition (`PROCEED`, `HOLD`, `REVISE`, `RETURN_TO_CHARACTERIZATION`) that references both regression and progression/qualification evidence.

Reports are written under `local_scalability/` and are not committed.

## Initial implementation scope

Implement only the resource models earned by the pressure tests. Do not invent solutions for unresolved classes.

**Implement first**
- Dictionary entry (proposal-capable).
- Association (proposal-capable).
- Category / major (proposal-capable + reference dimension).
- Candidate as a derived expansion surface (traced to its generating association or major; no independent proposal class).

**Represent but do not generalize**
- Seed: treat as historical/unresolved. A proposal that targets generalized seed expansion produces an explicit unresolved finding and routes `HOLD`. Do not invent a generalized seed identity or combination model.
- Licensed region: treat the present hardcoded scaffolding as a constraint/licensing surface. Do not invent a declarative licensed-region inventory or generalized licensing engine. Report the current filter behavior and any boundary crossings against the existing table.

**Leave open**
- Reference objects/tables. Do not implement expansion analysis for them until their matrix row is completed.

## Reuse requirements

From the gap analysis, the following must be reused rather than recreated:
- existing regression / replay / check infrastructure for the regression leg;
- characterization execution and artifact persistence discipline (canonical identity, hard non-overwrite) where evidence artifacts are required;
- generated/local-output handling and ignore rules.

New code is limited to proposal intake, discovery against established surfaces, relationship classification, dependency alignment, progression-obligation computation for the supported classes, qualification-boundary checking against existing characterization records, disposition logic, and report emission.

## Execution flow (bounded)

The first implementation must realize this sequence for the supported classes:
1. Read and validate proposal YAML.
2. Identify deltas (identity versus proposed change).
3. Discover existing related definitions (distinguish absent from discovery failed).
4. Classify relationships using the evidence-bearing set.
5. Evaluate dependencies.
6. Compute newly reachable-and-valid combinations, `$O_{\Delta}$`.
7. Determine qualification state against existing characterization boundaries.
8. Invoke existing regression infrastructure (results kept separate).
9. Evaluate characterization boundary and produce disposition.
10. Emit findings and reports under `local_scalability/`.

Derived surfaces (Candidate) must be traced to their generating proposal-capable origin.

## Acceptance tests (first pass)

A bounded implementation is acceptable when it can:
- accept a proposal whose resource identity and proposed relation are already established, classify it `already_defined`, produce no false progression obligations, and report the existing evidence;
- accept a proposal YAML that adds a new dictionary key→cue mapping and produce a finding that names the new relation, the resulting obligations, and a disposition that does not treat green regression as qualification;
- accept a proposal that extends an existing dictionary word with a new category and classify it as `extension_of` with an explicit notification;
- accept a proposal that adds an association entry and enumerate the newly reachable candidate proposals that result;
- accept a proposal that adds a major and show the downstream eligibility consequences;
- accept a proposal that targets generalized seed expansion and terminate with an unresolved finding and `HOLD`;
- write all generated output under `local_scalability/` and leave that directory untracked;
- never write proposal content into established Path A YAML or reference files.

## Non-goals for the first implementation

- Full population of the resource-class matrix.
- Generalized seed model.
- Declarative licensed-region inventory.
- Reference-object expansion analysis.
- Final user-guide commands or frozen report schemas.
- Root-cause diagnostics beyond the structured finding contract.
- Any change that grants a proposal standing in the established environment.

## Historical authorization sequence (completed)

The following sequence was executed as the first bounded-pass authorization lifecycle for this plan:

1. **Implementation mapping only (no code changes).**
2. **Mapping review and approval.**
3. **Bounded implementation execution under approved mapping/envelope.**
4. **Acceptance-test and reused-regression verification.**
5. **Stop for review before further work.**

Historical first-task authorization record:

The first Agent instruction was required to:

1. read [scalability_program.md](scalability_program.md),
2. read [scalability_design.md](scalability_design.md),
3. read [scalability_gap_analysis.md](scalability_gap_analysis.md),
4. read this implementation plan,
5. inspect existing runtime, regression/replay, characterization, dictionary, association, category, Candidate, Licensed Region, and `.gitignore` conventions.

That first task output was required to report:
- existing facilities to reuse;
- proposed files/modules under `scalability/`;
- proposal-entry/run interface;
- support files believed necessary;
- existing functions/modules each scalability stage will call;
- report/session output structure;
- `.gitignore` changes;
- test files and mapping from each acceptance test to its proposed test;
- anything in this implementation plan that cannot be mapped onto existing code;
- anything that would require inventing an unresolved contract.

## Current implementation state

- The first bounded scalability implementation has been accepted.
- Bounded scalability acceptance tests pass.
- Reused regression checks pass.
- Regression remains distinct from progression/qualification.
- An analyzed proposal may correctly result in `HOLD` when qualification evidence remains `unresolved`.
- Further scalability work requires a new bounded authorization.
- This document remains the accepted implementation envelope and historical authorization record for the first bounded pass.
