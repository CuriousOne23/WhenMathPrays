# 40.40_scheduler_prototypes / software_description.md

## Approval State

Approved by human on 2026-05-28 (Phase A complete; eligible for Phase B execution).

## Two-Phase Execution Model (Global 40.* Rule)

- Phase A: generate and review `software_description.md` only.
- Mandatory stop after Phase A until explicit human approval.
- Phase B (only after approval): `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

## 1. Purpose

This module defines exploratory scheduler behavior for the Thought Simulator tick cycle, with emphasis on deterministic ordering, fairness, and parallel-safe cohort execution semantics.

## 2. Scope

- model scheduler selection behavior per tick
- define deterministic ordering and tie-break rules
- define fairness expectations and starvation prevention constraints
- define deterministic merge expectations for parallel-safe cohorts
- define scheduler observability fields required for replay and diagnosis

This Phase A document does not define implementation code or verification artifacts.

## 3. Source Index (Conceptual Inputs)

Primary conceptual sources in `20_requirements/`:

- `20.140_program_flow.md` (scheduling phase and phase ordering)
- `20.40_performance_requirements.md` (deterministic parallel semantics and scheduler efficiency)
- `20.20_error_and_stability_requirements.md` (fair progress and deterministic failure behavior)
- `20.60_testing_and_validation.md` (scheduler fairness and determinism test obligations)
- `20.50_observability_requirements.md` (tick-level observability and replayability)
- `20.90_interfaces_and_io.md` (deterministic interface and runtime control constraints)

## 4. Core Responsibilities

- Select active ThoughtPoints in deterministic order each tick.
- Preserve strict tick-phase boundaries (scheduler is phase-local, no cross-phase mutation).
- Support fair progress across active ThoughtPoints.
- Support deterministic parallel-safe cohort selection/merge semantics where enabled.
- Emit scheduler decision evidence needed for replay and audit.

## 5. Key Invariants

- Identical deterministic inputs produce identical scheduling sequences.
- Tie-breaking is explicit and deterministic (no wall-clock or nondeterministic ordering sources).
- No ThoughtPoint experiences unbounded starvation under configured fairness policy.
- Scheduler behavior does not mutate non-scheduler phase state.
- Deterministic mode disables or constrains any optimization that could alter order semantics.

## 6. Tentative Scheduler Contract (Phase A)

Inbound context (conceptual):

- current tick index
- active ThoughtPoint set (identity, priority signals, state counters)
- scheduler policy configuration (round-robin baseline, optional weighting)
- deterministic mode flag

Outbound scheduler decision payload (conceptual):

- selected ThoughtPoint order for current tick
- deterministic tie-break provenance
- fairness counters/metadata for diagnostics
- cohort grouping metadata when parallel-safe execution is used

## 7. Observability Expectations

- Each tick should expose scheduler decision order and selection rationale fields.
- Scheduler diagnostics should be replay-safe and comparable across reruns.
- Fairness-related counters should be available for long-run monitoring.

## 8. Open Questions for Human Review

- Which fairness policy is canonical for default mode: pure round-robin, weighted round-robin, or priority-plus-aging?
- What minimum fairness metric should be enforced (for example, max wait ticks bound)?
- Which tie-break key order should be canonical when multiple priority signals are equal?
- What cohort-merge constraints are mandatory for deterministic parallel scheduler behavior?

## 9. Phase A Exit Condition

Phase B may begin only after explicit human approval of this document.
