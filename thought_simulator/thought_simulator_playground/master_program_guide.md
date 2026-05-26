# Master Program Guide

## 1. Purpose

The Thought Simulator Playground is the controlled exploration layer for developing, testing, and refining ideas before they are promoted into the formal architecture, requirements, and implementation tracks.

This guide defines the common operating model for all playground modules.

## 2. Playground Philosophy

- Explore quickly, but document rigorously.
- Keep modules small, focused, and testable.
- Treat failures as high-value evidence.
- Maintain deterministic thinking even during early experimentation.
- Promote only verified designs.

## 3. Verification Capsule Concept

Each module accumulates a Verification Capsule: a compact, auditable record of what was tested, what evidence exists, and whether the module is ready for promotion.

A module's Verification Capsule is distributed across:

- software_description.md
- harness.py
- verification_summary.md
- insights.md
- failures.md
- requirements_traceability.md

The capsule must answer:

- What was attempted?
- What passed, failed, or remains unknown?
- Which invariants were validated?
- Which requirements and design docs are affected?

## 4. State Control Rules

All module exploration should follow these rules:

1. Deterministic by default
   - Prefer fixed seeds and repeatable execution paths.
2. Explicit state transitions
   - Record major state changes in logs or summaries.
3. No hidden mutation assumptions
   - Document where state changes occur and why.
4. Evidence before conclusions
   - Conclusions must reference run output or artifacts.
5. Versioned iteration
   - Update verification_summary.md and insights.md for each meaningful run.

## 5. Exploration Workflow

1. Define scope in software_description.md.
2. Implement or refine prototype.py.
3. Execute harness.py for repeatable verification.
4. Record run evidence in insights.md.
5. Record failures in failures.md.
6. Update verification_summary.md with status and evidence links.
7. Update requirements_traceability.md with impacted requirement/design docs.
8. Decide: iterate, pause, or promote.

## 6. Promotion Criteria: Playground to Final Design

A module is eligible for promotion when:

- core invariants are explicit and stable,
- verification steps are repeatable,
- results are supported by concrete evidence,
- requirement and design impacts are clearly mapped,
- unresolved risks are documented and bounded.

Promotion path:

1. Consolidate verified findings.
2. Propose requirement/design updates.
3. Add implementation-grade tests.
4. Integrate into final design and core project structure.

## 7. Standard Module File Roles

- software_description.md: current design intent and boundaries
- prototype.py: exploratory implementation
- harness.py: repeatable verification runner
- verification_summary.md: authoritative verification capsule summary
- insights.md: run-by-run observations and outcomes
- failures.md: failed attempts and invalidated assumptions
- updated_requirements.md: candidate requirement changes
- requirements_traceability.md: links to requirement/design sources and impacts
