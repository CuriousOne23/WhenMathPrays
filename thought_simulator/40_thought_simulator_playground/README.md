# Thought Simulator Playground

## Purpose

The playground is a structured exploration space for rapidly testing ideas before promoting them into formal requirements, architecture, and implementation.

It is intentionally separate from production-facing paths so we can iterate quickly, preserve evidence, and make promotion decisions with confidence.

## Verification Capsule (Core Process)

Each module maintains a Verification Capsule: a compact, auditable package of design intent, test evidence, failures, and requirement traceability.

Required capsule files per module:

- software_description.md
- prototype.py
- harness.py
- verification_capsule.md
- requirements_delta.md
- artifacts/

Shared playground vocabulary:

- 40_thought_simulator_playground/40.30_verification_glossary.md

## Workflow

1. Define scope in software_description.md.
2. Draft and evolve prototype.py.
3. Run harness.py for repeatable verification.
4. Record run evidence in verification_capsule.md (command, result, exit code, artifacts, notes).
5. Record failures and invalidated assumptions in verification_capsule.md and requirements_delta.md.
6. Update verification_capsule.md with current status, evidence, and IO fields exercised.
7. Update requirements_delta.md with requirement/design links and change log entries.
8. Decide whether the module is ready to move from exploration to final design.

## Promotion Path: Exploration -> Final Design

A module is promoted when invariants are stable, verification is repeatable, evidence is sufficient, and requirement impacts are explicit.

Promotion sequence:

1. Consolidate validated findings.
2. Update requirement and design documents.
3. Add implementation-grade tests.
4. Integrate into final architecture and codebase.

## Revision Control and Design Release Coupling

Playground artifacts are revision-controlled project assets.

When a design specification in `50_thought_simulator_design/` cites playground files (for example, `software_description.md`, `verification_capsule.md`, `requirements_delta.md`, or artifact outputs), those cited files become part of the released design evidence for that design version.

Coupling rules:

- requirement documents in `20_requirements/` remain normative source of truth
- design documents in `50_thought_simulator_design/` remain subsystem architectural contracts
- cited playground evidence in `40_thought_simulator_playground/` remains the auditable verification trail tied to the released design version

If cited playground evidence changes materially after promotion:

- update the affected design document version
- update traceability/evidence references
- record the change in the appropriate delta/capsule files

## Module Format Coherence and Exception Policy

To keep the playground coherent and scalable, all numbered module folders under `40_thought_simulator_playground/` should follow a common verification-capsule structure and naming pattern.

Coherence baseline for module folders:

- `software_description.md`
- `prototype.py`
- `harness.py`
- `verification_capsule.md`
- `requirements_delta.md`
- `artifacts/`

Why this coherence is required:

- consistent onboarding for contributors and external adopters
- consistent verification evidence and traceability across modules
- predictable promotion path from exploration to design release artifacts
- reduced process drift between subsystem teams and module owners

Exception policy for `40.10_math_prototypes/`:

- math prototypes may use a lighter documentation burden while still keeping the same file/folder names where practical
- early mathematical exploration may not immediately impact canonical requirements or design contracts
- when there is no requirement/design impact yet, `requirements_delta.md` may remain concise but should still record that status explicitly

Why the exception exists:

- math research often starts as hypothesis exploration before subsystem contract implications are known
- forcing full design-level delta detail too early increases noise and slows research iteration
- preserving naming compatibility still allows smooth promotion when math findings mature into design-relevant evidence

## Directory Map

- 40.10_math_prototypes/ - entropy, stability, and math experiments
- 40.20_tp_lifecycle/ - ThoughtPoint lifecycle exploration
- 40.30_basin_prototypes/ - basin behavior prototypes
- 40.40_scheduler_prototypes/ - scheduling and ordering experiments
- 40.50_regulator_prototypes/ - regulator mechanisms and policies
- 40.60_tick_cycle_skeleton/ - simulation tick-cycle skeletons
- 40.70_snapshot_prototypes/ - snapshot and restoration patterns
- 40.80_event_log_prototypes/ - event stream and replay experiments
- 40.90_experiment_runner/ - experiment orchestration prototypes
- shared/ - shared helpers for prototype work
- 40.20_master_program_guide.md - unified process guide and state-control policy
- 40.30_verification_glossary.md - shared verification vocabulary




