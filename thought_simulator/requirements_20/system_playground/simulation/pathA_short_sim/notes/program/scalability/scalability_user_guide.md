# Scalability User Guide

**Document:** notes/program/scalability/scalability_user_guide.md  
**Status:** Partial scaffold (non-normative).  
**Date:** 2026-11-23  
**Purpose:** Provide the practical sequence an operator or Agent follows after expanding Path A. This document is not yet the final operational guide; it now records implementation-backed command/report facts needed for later completion and still does not freeze report schema or storage format.

## Intended use

After an expansion (new or modified seed, association, category, candidate, licensed-region YAML, or other expansion-sensitive resource):

1. Identify what changed.  
2. Determine the affected dependency surfaces.  
3. Invoke the scalability check (tooling to be defined).  
4. Locate the resulting report.  
5. Interpret its status (regression, new coverage obligations, missing support, boundary crossing).  
6. Determine whether ordinary regression is sufficient or progression qualification is required.  
7. Stop and return to research review when the decision is HOLD, REVISE, or RETURN_TO_CHARACTERIZATION.

## Current status

This document remains non-normative and incomplete. The final step-by-step operational procedure is still pending.

Implementation-backed facts now available for later completion:
- runner: `python run_scalability.py --proposal-file <path> --session-id <id> --run-index <n> [--report-version <v>] [--run-regression]`
- output locality: `local_scalability/sessions/<session_id>/runs/`
- paired report outputs per run: `<run_index>__scalability_check__<version>.json` and `.md`
- current machine-readable report sections: identity, proposal, relationships, dependencies, progression obligations, qualification, regression, findings, disposition
- `--run-regression` records reused regression checks in the report and remains distinct from progression/qualification disposition handling

Pending for guide completion:
- concise operator/Agent sequence for selecting proposal fixtures versus external proposal files;
- interpretation guidance for each disposition route (`PROCEED`, `HOLD`, `REVISE`, `RETURN_TO_CHARACTERIZATION`);
- explicit handoff boundaries to future controlled integration/promotion work (outside current scalability implementation scope).

See [scalability_program.md](scalability_program.md) for the governing principles.
