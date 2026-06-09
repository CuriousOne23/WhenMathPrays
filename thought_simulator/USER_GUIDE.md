# Thought Simulator User Guide

## Purpose

This guide explains how to run the Thought Simulator documentation workflow using forward flow and backward flow.

It defines:

- where users should edit
- what prompt to give the AI agent
- what the AI agent will execute
- what CI checks should enforce

## Repository Authorship and Workflow

This repository is currently run as a human-owned, AI-drafted, human-reviewed workflow.

Use these rules consistently:

- humans, led by the repository owner, control 20-series intent, scope, and final approval
- AI agents draft most 20-series content, expansion, normalization, and scaffolding
- a small set of core 20-series documents remain human-written because they define the canonical methodology
- AI-drafted content becomes authoritative only after human review and approval

In practice, this is both the current repository method and the recommended workflow going forward.

## Directory Roles

Use these roles consistently:

- `thought_simulator/00_program_governance/`:
  governance, repo-wide control, direction, and policy
- `thought_simulator/10_thought_simulator_req/`:
  architecture, top-level system shape, invariants, and decomposition
- `thought_simulator/20_requirements/`:
  requirements, normative "what TS must be", and traceable HLRs
- `thought_simulator/30_verification/`:
  verification of the design, review, and evidence that the design is sound (see `30.00_verification_user_guide.md` for the standard process, artifact templates, and three-flow requirements)
- `thought_simulator/40_thought_simulator_playground/`:
  playground, experiments, exploratory work, and interactive prototyping
- `thought_simulator/50_thought_simulator_design/`:
  design, implementation design, realization details, and concrete spec-to-code mapping
- `thought_simulator/60_review/`:
  review, critique, architectural draft review, and decision analysis
- `thought_simulator/70_measurement/`:
  measurement, metrics, instrumentation, and evaluation methodology
- `thought_simulator/80_safety/`:
  safety, constraints, failure containment, and protective controls
- `thought_simulator/90_validation_certification/`:
  validation and certification, conformance, acceptance, and formal sign-off

## Test Benches (High-Level Overview)

Test benches are high-fidelity, external verification infrastructure (not exploratory prototypes). They live in the top-level `testbenches/` directory.

**Only the test bench programs, scripts, and documentation** are stored in the repository under `testbenches/`. All generated outputs, logs, artifacts, plots, traces, CSV results, and raw data are excluded via .gitignore (they may live locally in ignored subdirectories inside the bench folder or externally).

They generate evidence that can validate, challenge, or extend requirements and design contracts. All test bench evidence is normalized and promoted through the 30-series via the `30_verification/30.tb/` structure (see `30.tb/README.md`), which stores **only normalized text records** (capsules and deltas containing textual summaries, three-flow statements, HLR mappings, and "Testbench-Driven Changes" notes). Raw data payloads are never committed to the repo.

Test bench results can drive backward flow updates into 10.50-series design requirements and 50-series design specs (and, when sufficiently strong, even into 20-series requirements). The path is always: test bench → 30-series delta/capsule → higher layers.

The authoritative contract for test benches (required outputs, HLR referencing, reproducibility, artifact formats, repo policy, etc.) is in `testbenches/00_testbench_requirements.md`.

Future high-fidelity test benches will also feed 30-series verification evidence via the 30.tb/ structure.

## 10-Layer Disambiguation Rule

When you request "update 10" in flow execution, this means:

- `10_thought_simulator_req/` by default

Only reference `00_program_governance/` when you explicitly name it.

## Where The User Should Edit

## No Automatic Propagation From 20 (Mandatory)

Edits in `20_requirements/` must not automatically trigger updates in `10_thought_simulator_req/`, `30_verification/`, `40_thought_simulator_playground/`, or `50_thought_simulator_design/`.

Allowed AI-agent behavior after a 20-layer edit:

- report impacted downstream directories/files
- ask whether the user wants to run forward flow or backward flow
- provide a ready-to-run prompt template

Disallowed behavior:

- automatic cross-layer edits initiated only because `20_requirements/` changed

Allowed automatic maintenance inside `30_verification/`, `40_thought_simulator_playground/`, and `50_thought_simulator_design/` after explicit forward/backward flow start:

- glossary and terminology synchronization updates
- README path and reference repairs
- intra-layer markdown link/path repairs after file rename or section-name changes
- `50.00_design_traceability_index.md` synchronization when any 50-series file is added, renamed, deleted, or remapped

### Forward Flow

User edits usually begin in one of:

- `20_requirements/` for architecture/rationale changes
- `40_thought_simulator_playground/` for exploratory module behavior and evidence

The AI agent then promotes and synchronizes into canonical layers.

For `40.05`-governed exploratory module work, the forward-flow sequence after the module is executed and human-approved is explicit:

1. create or update the corresponding `10.50.*` canonical anchor in `10_thought_simulator_req/50_design/`
2. create the matching `30.*` verification subdirectory and canonical verification artifacts in `30_verification/`
3. execute `50.05` to create or update the corresponding `50.*` design artifact and synchronize `50.00_design_traceability_index.md`

This means an approved `40.*` module does not promote directly to `50.*`; it first establishes its `10.50.*` anchor and `30.*` verification package.

### Backward Flow

User edits usually begin with canonical anchor updates in:

- `10_thought_simulator_req/`

If those 10-anchor changes were derived from `20_requirements/`, backward flow still treats 10 as the normative trigger source.

## Forward Flow Runbook

### User Prompt Template

Use this prompt when you want promotion/synchronization from exploratory work:

```text
Run FORWARD FLOW from updated exploratory sources.
Source edits:
- <list files under 20_requirements and/or 40_thought_simulator_playground>
Targets:
- 10_thought_simulator_req
- 30_verification (see `30.00_verification_user_guide.md` for the full verification process, artifact requirements, and three-flow rules)
- 50_thought_simulator_design
Requirements:
- preserve IDs unless explicitly approved for change
- update traceability references
- produce execution log and integrity check summary
```

### AI Agent Expected Execution

The AI agent should:

1. Confirm direction as `forward` (or request clarification if ambiguous).
2. If the initiating source is approved `40.05` exploratory module work, create or update the corresponding `10.50.*` canonical anchor first.
3. Create the matching `30.*` verification package for that approved `40.*` module.
4. Update impacted `50_thought_simulator_design/` files only after the `10.50.*` and `30.*` artifacts exist.
5. Synchronize `50.00_design_traceability_index.md` if any design mapping changed.
6. Create/update execution log under `10_thought_simulator_req/docs/`.
7. Run integrity check and report pass/fail summary.

Forward flow must start only after explicit user request; a 20-layer edit alone is not sufficient to execute propagation.

`40.05` itself is not limited to forward flow. It can also be an impacted layer during backward flow when updated `10_thought_simulator_req/` anchors need to propagate into `40_thought_simulator_playground/`.

## Backward Flow Runbook

### User Prompt Template

Use this prompt when canonical anchors are already updated and must be propagated:

```text
Run BACKWARD FLOW from updated 10_thought_simulator_req anchors.
Initiating lineage:
- 20_requirements -> 10_thought_simulator_req (if applicable)
Targets:
- 30_verification
- 40_thought_simulator_playground
- 50_thought_simulator_design
Requirements:
- automatic execution log
- automatic integrity check
- full 50-series design synchronization review
- final assertion: Forward-Equivalence State: YES
```

### AI Agent Expected Execution

The AI agent should:

1. Confirm direction as `backward` (or stop for clarification if ambiguous).
2. Treat `10_thought_simulator_req/` as normative trigger source.
3. Propagate updates in order:
   - `30_verification`
   - `40_thought_simulator_playground`
   - `50_thought_simulator_design`
4. Update all impacted design files and synchronize `50.00_design_traceability_index.md` if mappings changed.
5. Create/update backward-flow execution log in `10_thought_simulator_req/docs/`.
6. Run integrity checks and record results.
7. Record final completion assertion:
   - `Forward-Equivalence State: YES`

Backward flow must start only after explicit user request; a 20-layer edit alone is not sufficient to execute propagation.

## 20-Series Refactor Prompt Template

Use this prompt when you want the AI Agent to refactor the entire `20_requirements/` directory into a new 20-series structure while keeping all downstream layers unchanged unless explicitly approved.

```text
You are refactoring the entire `20_requirements/` directory of the Thought Simulator (TS) repository.

This refactor must be deterministic, safe, complete, and fully aligned with the TS architecture.

You must follow every instruction below exactly.

1. Create the new 20-series directory structure

Create the following files, in this exact order:

20.10   ts_architectural_principles.md
20.20   ts_primitives.md
20.30   ts_functional_model.md

20.40   ob_requirements.md
20.50   rb_requirements.md
20.60   tb_requirements.md

20.70   mb_requirements.md
20.80   gb_requirements.md
20.90   ib_requirements.md
20.100  inb_requirements.md
20.110  oub_requirements.md

20.120  mtp_schema_requirements.md
20.130  splitting_and_merging_requirements.md
20.140  truth_evaluation_requirements.md
20.150  tcu_budgeting_requirements.md
20.160  randomness_requirements.md
20.170  safety_requirements.md

20.180  conversational_relevance_requirements.md
20.190  glossary.md
20.200  traceability_matrix.md

These are the only authoritative requirement documents for the 20-series.

2. All rewritten documents must be fully consistent with the current 20.03 document

This is mandatory.

- 20.03 is the authoritative pre-refactor specification.
- All rewritten documents must reflect the architecture, semantics, definitions, invariants, and functional model described in 20.03.
- No rewritten document may contradict or reinterpret 20.03.
- All new requirement documents must extend, formalize, or modularize the content of 20.03 - never replace or alter its meaning.

This includes:

- OB/RB/TB semantics
- ΔH%
- H%
- MTP structure
- deterministic meaning construction
- seed isolation
- splitting and merging
- truth evaluation
- TCU budgeting
- randomness boundary
- safety invariants

20.03 is the source of truth for the refactor.

3. Migrate content from old 20-series files

Only three existing files contain content that must be preserved:

Preserve (rewrite plus migrate):

- `20.150_glossary.md` -> merge into `20.190_glossary.md`
- `20.160_traceability_matrix.md` -> rewrite into `20.200_traceability_matrix.md`
- `20.140_program_flow.md` -> integrate content into:
  - `20.10 ts_architectural_principles.md`
  - `20.30 ts_functional_model.md`

All other existing 20-series files must be archived.

Archive them into:

20_archive/

Do not delete their content - move them intact.

4. Rewrite all content to match the TS architecture (as defined in 20.03)

All new 20-series documents must be rewritten using the current TS architecture, including:

- OB / RB / TB
- MB / GB / IB / InB / OuB
- TP / MTP
- ΔH%
- H%
- deterministic meaning construction
- seed isolation
- splitting and merging
- truth evaluation
- TCU budgeting
- randomness boundary
- safety invariants
- conversational relevance subsystem

No legacy terminology may remain.

No references to the old architecture may remain.

5. Requirements must be explicit, testable, and traceable

Each requirement must:

- have a unique requirement ID
- be written in normative language (must, shall, may not)
- be testable
- be traceable to 40-series design documents
- be traceable to 30-series verification documents

Update the `20.200 traceability matrix` accordingly.

6. Respect the 20 -> 40 -> 10/30 -> 50 CI-checked flow

- Do not update 40-series, 30-series, or 10-series automatically.
- Provide impact analysis only.
- Wait for explicit user approval before generating any downstream changes.

7. Safety and determinism rules

All rewritten documents must enforce:

- deterministic execution
- no nondeterministic code paths
- no floating-point chaos
- no GPU nondeterminism
- seed isolation
- reproducibility
- auditability
- no emergent memory
- no probabilistic embeddings
- no hallucinated continuity

8. Conversational relevance subsystem

Implement `20.180 conversational_relevance_requirements.md` with:

- cross-turn MTP persistence rules
- conversation anchors
- relevance scoring
- thread continuity
- drift detection
- IB triggers
- deterministic update rules
- safety constraints

This subsystem is essential for TS multi-turn coherence.

9. Deliverables

When complete, you must produce:

A. The full rewritten 20-series directory

with all new files populated and all content rewritten.

B. The 20_archive directory

containing all old files except the three preserved ones.

C. A summary of changes

including:

- migrated content
- rewritten sections
- new requirement IDs
- traceability updates
- any detected inconsistencies
- any recommended follow-up actions

10. Do not proceed beyond the 20-series

Do not modify:

- 40_design
- 30_verification
- 10_program
- 50_playground

until explicitly instructed.

Provide impact analysis only.
```

## Ambiguity Rule

If user intent could mean either forward or backward flow, the AI agent must stop and request explicit direction before making edits.

Minimum confirmation record:

- selected direction (`forward` or `backward`)
- initiating source documents
- impacted target set

## Required Execution Logs

Execution logs must be stored under:

- `thought_simulator/10_thought_simulator_req/docs/`

Recommended naming pattern:

- `BACKFLOW_EXECUTION_LOG_YYYY-MM-DD_<scope>.md`
- `FORWARDFLOW_EXECUTION_LOG_YYYY-MM-DD_<scope>.md`

## Integrity Check Requirements

At minimum, integrity checks must validate:

- stale or unresolved requirement references
- glossary/terminology mismatches
- unmapped HLR/LLR references introduced by updates
- required backward-flow governance sections in impacted 30 module docs (when in scope)
- 50-series traceability index synchronization when design mappings changed
- 30-series inventory index synchronization when verification module structure changed

## CI Checks Associated With This Guide

CI should enforce the following:

1. `thought_simulator/USER_GUIDE.md` exists.
2. `thought_simulator/USER_GUIDE.md` contains these section headers:
   - `Forward Flow Runbook`
   - `Backward Flow Runbook`
   - `Where The User Should Edit`
   - `Integrity Check Requirements`
   - `CI Checks Associated With This Guide`
3. All required governance files referenced by this guide exist:
   - `thought_simulator/10_thought_simulator_req/docs/promotion_protocol.md`
   - `thought_simulator/30_verification/README.md`
   - `thought_simulator/30_verification/30.00_verification_user_guide.md`
   - `thought_simulator/40_thought_simulator_playground/40.05_master_program_guide.md`
   - `thought_simulator/50_thought_simulator_design/50.05_software_spec_construction_guide.md`
   - `thought_simulator/50_thought_simulator_design/50.00_design_traceability_index.md`
   - `thought_simulator/30_verification/30.01_verification_inventory_index.md`
4. If a PR includes backward-flow changes to 30/40/50, CI must fail unless:
   - at least one matching backward-flow execution log exists in `10_thought_simulator_req/docs/`
   - the log contains `Forward-Equivalence State: YES`
   - integrity check summary is present
5. If a PR changes any file under `50_thought_simulator_design/`, CI must run the traceability-index consistency rule from `50.00_design_traceability_index.md` (blocking workflow).
6. Structural drift between `30.01_verification_inventory_index.md` and on-disk `30.*` module directories is reported by `validate_30_inventory_index.py` (non-blocking warning).
7. Incomplete forward-flow promotion (`30.01` rows with status `promoted` or `approved` but no matching `10.50.{band}_*.md` in `10_thought_simulator_req/50_design/`) is reported by `validate_30_10_50_pairing.py` (non-blocking warning; one-way 30 → 10.50 only).
8. Local pre-PR runs may use `validate_50_traceability_index.py` (non-blocking warning) as a mirror of the blocking 50.00 workflow check.
9. If a PR renames any markdown file under `30_verification/`, `40_thought_simulator_playground/`, or `50_thought_simulator_design/`, CI must fail unless the same change set includes:
  - `30_verification/30.160_verification_glossary.md`
  - `30_verification/glossary_term_registry.json`
  - `50_thought_simulator_design/50.00_design_traceability_index.md` (required when the rename touches `50_thought_simulator_design/`)
  Note: The 50-series glossary (`50.01_50_series_glossary.md` + registry) is under CI warning checks (non-blocking) so the team is notified of potential freshness issues, but updates are decided by humans rather than enforced.
10. If a PR introduces broken markdown file references or broken markdown heading anchors in governed docs, CI must fail.
  - Governance policy note: this failing check is a red warning signal by default and is merge-blocking only when configured as a required status check in repository branch-protection/ruleset settings.

## Done Criteria

A flow run is done only when:

- direction is explicit and recorded
- target layers are synchronized
- required execution log exists
- integrity checks pass
- if backward flow with design synchronization gate: log includes `Forward-Equivalence State: YES`
