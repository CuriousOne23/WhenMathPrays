# Thought Simulator Playground

## Purpose

The playground is a structured prototyping zone for fast, disciplined exploration of ideas before they are promoted into the formal Thought Simulator architecture and requirements.

It is intentionally separated from production-facing design and implementation paths so we can test hypotheses, discard weak approaches quickly, and preserve learning artifacts.

## Playground Philosophy

- Prototype first, formalize second.
- Preserve failures as first-class knowledge.
- Keep each module narrowly scoped and testable.
- Promote only validated patterns to final architecture.
- Maintain deterministic and traceable thinking even in early experiments.

## Workflow

1. Define a focused prototype objective in a module's `software_description.md`.
2. Draft minimal exploratory code in `prototype.py` (once implementation begins).
3. Record observations in `insights.md`.
4. Record dead ends and broken assumptions in `failures.md`.
5. Capture requirement impacts in `updated_requirements.md`.
6. Review whether the module is ready for promotion.

## Promotion Path: Playground -> Final Design

A module can move from playground to final design when:

- core invariants are clear and stable,
- behavior is reproducible and explainable,
- interfaces are coherent with system architecture,
- unresolved risks are documented and bounded,
- requirement deltas are explicit and reviewable.

Promotion sequence:

1. Consolidate findings into architecture/design documents.
2. Update requirement docs and traceability matrix.
3. Add deterministic tests and observability hooks.
4. Integrate into main code paths only after review.

## Directory Map

- `01_math_prototypes/` - entropy, stability, and math experiments
- `02_tp_lifecycle/` - ThoughtPoint lifecycle exploration
- `03_basin_prototypes/` - basin behavior prototypes
- `04_scheduler_prototypes/` - scheduling and ordering experiments
- `05_regulator_prototypes/` - regulator mechanisms and policies
- `06_tick_cycle_skeleton/` - simulation tick-cycle skeletons
- `07_snapshot_prototypes/` - snapshot and restoration patterns
- `08_event_log_prototypes/` - event stream and replay experiments
- `09_experiment_runner/` - experiment orchestration prototypes
- `shared/` - shared helpers for prototype work
