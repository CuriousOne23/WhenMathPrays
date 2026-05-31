# Thought Simulator User Guide

## Purpose

This guide explains how to run the Thought Simulator documentation workflow using forward flow and backward flow.

It defines:

- where users should edit
- what prompt to give the AI agent
- what the AI agent will execute
- what CI checks should enforce

## Directory Roles

Use these roles consistently:

- `thought_simulator/20_requirements/`:
  exploratory and architectural rationale
- `thought_simulator/10_thought_simulator_req/`:
  canonical requirement authority and flow trigger source
- `thought_simulator/30_verification/`:
  canonical verification capsules and requirement deltas
- `thought_simulator/40_thought_simulator_playground/`:
  exploratory module workspace and master execution guide
- `thought_simulator/50_thought_simulator_design/`:
  canonical design specifications and traceability index
- `thought_simulator/10_program_governance/`:
  architecture/program governance references (not the canonical requirement trigger source)

## 10-Layer Disambiguation Rule

When you request "update 10" in flow execution, this means:

- `10_thought_simulator_req/` by default

Only reference `10_program_governance/` when you explicitly name it.

## Where The User Should Edit

### Forward Flow

User edits usually begin in one of:

- `20_requirements/` for architecture/rationale changes
- `40_thought_simulator_playground/` for exploratory module behavior and evidence

The AI agent then promotes and synchronizes into canonical layers.

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
- 30_verification
- 50_thought_simulator_design
Requirements:
- preserve IDs unless explicitly approved for change
- update traceability references
- produce execution log and integrity check summary
```

### AI Agent Expected Execution

The AI agent should:

1. Confirm direction as `forward` (or request clarification if ambiguous).
2. Build/update canonical anchors in `10_thought_simulator_req/` when required.
3. Update `30_verification/` capsules and deltas for trace/evidence consistency.
4. Update impacted `50_thought_simulator_design/` files.
5. Synchronize `50.00_design_traceability_index.md` if any design mapping changed.
6. Create/update execution log under `10_thought_simulator_req/docs/`.
7. Run integrity check and report pass/fail summary.

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
   - `thought_simulator/40_thought_simulator_playground/40.20_master_program_guide.md`
   - `thought_simulator/50_thought_simulator_design/50.05_software_spec_construction_guide.md`
   - `thought_simulator/50_thought_simulator_design/50.00_design_traceability_index.md`
4. If a PR includes backward-flow changes to 30/40/50, CI must fail unless:
   - at least one matching backward-flow execution log exists in `10_thought_simulator_req/docs/`
   - the log contains `Forward-Equivalence State: YES`
   - integrity check summary is present
5. If a PR changes any file under `50_thought_simulator_design/`, CI must run the existing traceability-index consistency rule from `50.00_design_traceability_index.md`.

## Done Criteria

A flow run is done only when:

- direction is explicit and recorded
- target layers are synchronized
- required execution log exists
- integrity checks pass
- if backward flow with design synchronization gate: log includes `Forward-Equivalence State: YES`
