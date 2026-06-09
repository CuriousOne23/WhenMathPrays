# 40.270_scheduler_prototypes / software_description.md

## Approval State
- Phase A (software_description): approved (per user "CP approved" on the Phase A content in this file)
- Phase B (prototype + harness + evidence): executed 2026-06-06

## Phase B Deliverables (Executed)
- Harness scenarios executed: 12/12 PASS
- Artifact: `scheduler_verification_run_2026-06-06.json` (generated 2026-06-06, contains full scenario ledger, deterministic digests, input/output for replay)
- Coverage of all 10 "What Phase B Must Explore" items (via dedicated positive/negative scenarios + supporting):
  - Deterministic per-tick selection (RR baseline + WRR exploratory) — positive_deterministic_replay, positive_round_robin_fairness, etc.
  - Explicit deterministic tie-breaking + provenance — positive_tie_break_provenance (rationale + stable tp_id tie-break)
  - Fairness + bounded progress / starvation prevention — positive_fairness_starvation_prevent, positive_round_robin_fairness (wait_ticks / total_selected bounded)
  - Interrupt windows (pre_ob, post_tb, ...) + preemption — positive_interrupt_window_preemption (window + preempt flags in events/payloads)
  - Per-module/per-cycle timing budgets + cycle boundaries — positive_timing_budget_and_cycle (budget_tcu, budget_status, monotonic tick enforcement)
  - Deterministic parallel-safe cohort selection + merge semantics — positive_cohort_selection_merge (cohort_metadata with is_cohort, merge_semantics)
  - Rich replay-safe observability (selection order, tie-break rationale, fairness counters, cohort metadata, event logs) — positive_rich_observability (last_* fields in snapshot, history, TP wait/total)
  - Negative-path / deterministic rejection for malformed (empty active set at construction, non-monotonic tick, unsupported policy) — the three negative_* scenarios
  - Bounded internal state / resource usage (history_max enforced) — positive_bounded_history (trim on record, assert_invariants, snapshot)
  - Full deterministic mode (no nondet opts) — positive_deterministic_replay (identical replay + digest match), all scenarios under deterministic_mode=True
- Additional invariants demonstrated: non-cognitive (no TP/MTP semantic mutation or interpretation), read-only on caller contracts, replay via digest + sorted JSON, safety envelopes (history bound, positive int checks), contract_version 1.0 + deterministic payloads.
- Note: policies/weights/budgets in prototype are exploratory only for evidence generation; no final numeric or algorithm claims (per Non-Goals).

## Scaffold Metadata
- scaffold_status: planned
- intended_10_10_anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.40_scheduler_and_regulator_architecture.md
- intended_20_anchors:
  - thought_simulator/20_requirements/20.30_ts_functional_model.md
  - thought_simulator/20_requirements/20.40_ob_requirements.md
  - thought_simulator/20_requirements/20.90_ib_requirements.md
  - thought_simulator/20_requirements/20.90_ts_parameter_table.md
  - thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md
  - thought_simulator/20_requirements/20.170_safety_requirements.md
  - thought_simulator/20_requirements/20.200_traceability_matrix.md
- applicability: planned exploratory module for scheduler control-plane behavior (deterministic ordering, fairness, interrupt handling, replayable observability)
- disposition_target: promote

## Purpose
This scaffold reserves the module slot for future exploratory implementation of scheduler prototypes in the 40-layer.

It corresponds directly to the scheduler architecture defined in 10.10.40_scheduler_and_regulator_architecture.md (the deterministic execution controller) and supporting HLRs and principles in the 20-series.

The scheduler is the **deterministic execution controller** of the TS. It is responsible for ordering module execution, enforcing cycle boundaries, enforcing timing budgets, managing interrupt windows, coordinating preemption, ensuring deterministic sequencing, validating module readiness, and routing supervisory and regulatory events.

The scheduler **does not** perform cognitive inference, modify semantic content, alter TP or MTP state, or interpret cognitive payloads.

## Scope
- placeholder module for requirements-driven exploration of scheduler behavior
- no executable behavior is asserted yet
- will explore: deterministic per-tick selection of active ThoughtPoints, explicit deterministic tie-breaking, fairness policies with starvation prevention, handling of interrupt windows and preemption, timing and cycle boundary enforcement, support for deterministic parallel-safe cohort selection and merge, and emission of replay-safe observability and diagnostics.

All exploration **SHALL** remain strictly deterministic, non-cognitive, and non-mutating to core cognitive state, per 10.10.40 and 20-series principles.

## Flows Alignment Statement

- **Forward Flow (10/20-series)**: Driven by the detailed architecture in 10.10.40_scheduler_and_regulator_architecture.md (roles, execution ordering, cycle model, timing model, interrupt windows, message handling, safety envelopes, logging/replayability) and supporting 20-series guidance:
  - 20.30_ts_functional_model.md (scheduling phase and pipeline ordering)
  - 20.40_ob_requirements.md (tick-level observability and replayability under scheduler control)
  - 20.90_ib_requirements.md and 20.90_ts_parameter_table.md (deterministic interfaces, runtime control, and scheduler parameters such as cycle_time and interrupt latencies)
  - 20.150_tcu_budgeting_requirements.md (budgeting, efficiency, and per-tick cost constraints for the scheduler)
  - 20.170_safety_requirements.md (fair progress, starvation prevention, and deterministic failure behavior)
  - 20.200_traceability_matrix.md (test obligations for fairness and determinism)

- **Backward Flow (40-series evidence)**: Phase B execution (this module) produced concrete deterministic evidence against the 10.10.40 architecture and 20-series HLRs/guidance. Evidence is captured in the 12-scenario artifact + verification_capsule.md + requirements_delta.md. This provides backward input for refinement of 10.50.210 and 50-series scheduler specs (e.g., confirming bounded history, rich obs emission, interrupt window logging, cohort metadata as useful for audit).

- **Iterative Design Flow (50-series influence)**: The downstream 10.50.210_scheduler_requirements.md (updated with HLR-20.440-001 to 008 + contract elements) exists as the canonical anchor. Phase B evidence can explore and provide evidence to refine or validate those.

**Agreement Statement**: With Phase A approved and Phase B executed (12/12 PASS artifact covering all 10 required exploration items + core invariants from 10.10.40), the three flows are aligned:

- Forward: implementation and evidence directly traceable to 10.10.40 (roles, ordering, interrupts, timing, safety, replay) + listed 20 anchors (determinism, fairness, TCU, safety, OB replay, params).
- Backward: the generated artifact, capsule, and delta now supply concrete evidence (selection determinism, tie-break provenance, window/preempt handling, budget modeling, cohort/merge meta, bounded history, rich logs, negative-path rejection, starvation prevention) that can legitimately drive targeted updates to 10.50.210 HLRs or 50-series specs via the 30 promotion path (no bypass).
- Iterative: downstream 10.50.210 (HLR-20.440-001..008 + contract elements + TCU scheduler budgets) influenced the scope; Phase B evidence can now feed iterative refinement (e.g. explicit rationale logging, history bound as measurable).

All work preserved non-cognitive / deterministic / bounded / replayable / safety-first nature (no cognitive interpretation, no core state mutation, sorted JSON + digest for replay, history_max enforced, contract validation, monotonic ticks).

## Phase A Deliverables (this document)
- High-level description of scheduler behavior for exploratory prototyping
- Mapping of 10.10/20-series intent to prototype responsibilities
- Identification of unknowns, ambiguities, and missing definitions
- Clear definition of what Phase B must explore
- No algorithms, data structures, numeric thresholds, or implementation details

## What Phase B Must Explore
Phase B **SHALL** explore and produce concrete (deterministic, replayable) evidence for at least:

- Deterministic per-tick selection of active ThoughtPoints according to policy (round-robin baseline, with support for weighting or other configured policies)
- Explicit, deterministic tie-breaking rules and provenance when multiple ThoughtPoints have equal priority signals
- Fairness mechanisms that guarantee bounded progress for all active ThoughtPoints and prevent unbounded starvation under the configured policy
- Proper handling of interrupt windows (pre-OB, post-TB, post-TR, etc.) and preemption within scheduler control
- Enforcement of per-module and per-cycle timing budgets and cycle boundaries
- Support for deterministic parallel-safe cohort selection and merge semantics (where enabled by higher layers)
- Emission of rich, replay-safe observability (selection order, tie-break rationale, fairness counters/wait ticks, cohort metadata, event logs) for audit, diagnosis, and 30-series verification
- Negative-path and error handling: deterministic rejection or safe degradation for malformed inputs (e.g., empty active set, non-monotonic tick indices, unsupported policy values)
- Bounded internal state and resource usage consistent with 10.10.40 safety envelopes and 20.150 TCU constraints
- Full support for deterministic mode (no nondeterministic optimizations that could alter observable order or fairness)

## Non-Goals (Scaffold and Initial Phase B)
This module **SHALL NOT**:
- Perform any cognitive, semantic, or interpretation logic (strictly non-cognitive per 10.10.40)
- Mutate TP, MTP, or other cognitive state
- Define or hard-code final policy algorithms, tie-break orders, or numeric thresholds (these are governed by 20.95/50-series and 10.50.210)
- Implement the full control plane (regulator, GB supervisory, etc.); focus on core scheduler selection and observability logic
- Assume specific hardware or runtime details beyond the portable contracts in 10.10.60

## Risks & Unknowns to Investigate (aligned with 10.10.40 and 20.10)
- Selection of canonical default fairness policy (pure round-robin, weighted, with aging?) and validation of starvation bounds
- Precise, canonical tie-break key ordering and provenance logging when signals are equal
- Exact integration and handoff points with the regulator for ΔH% enforcement, fan-out limits, and overflow handling
- Performance and determinism under high load (many active TPs, high fan-out, frequent interrupts)
- Edge cases: empty active ThoughtPoint set, mid-cycle reconfiguration, interaction with coprocessor offload
- Ensuring strict separation and no leakage of cognitive state or nondeterminism into scheduler decisions

## Required Next Step
Phase B complete (see Phase B Deliverables above and updates to requirements_delta.md + verification_capsule.md with full evidence + three-flow statements).

Next (per 40.05 + 30.00): human may request 30.00 promotion step on this module (copy artifact + refresh 30.210 delta/capsule as canonical verification record). Evidence is now available to inform 10.50.210 refinements or 50.210_scheduler_design_spec.md construction (via 50.05 patterns), always through 30.

All Phase B work preserved the non-cognitive, deterministic, bounded, replayable, and safety-first nature of the scheduler (see invariants in capsule).

## Traceability
- 10.10.40_scheduler_and_regulator_architecture.md (primary detailed architecture source for roles, ordering, cycle/timing model, interrupts, safety, logging)
- 20.30_ts_functional_model.md (scheduling phase and functional pipeline ordering)
- 20.40_ob_requirements.md (tick-level observability and replayability)
- 20.90_ib_requirements.md and 20.90_ts_parameter_table.md (deterministic interfaces and scheduler parameters)
- 20.150_tcu_budgeting_requirements.md (budgeting and efficiency constraints)
- 20.170_safety_requirements.md (fairness and failure behavior)
- 20.200_traceability_matrix.md (test obligations)
- 10.10.10_system_architecture.md, 10.10.20_interprocess_communication_and_channels.md, 10.10.30_interrupts_and_preemption_model.md, 10.10.50_module_contracts_and_visibility_rules.md, 10.10.60_coprocessor_offload_and_portability_rules.md (supporting architecture)
- 10.50.210_scheduler_requirements.md (downstream canonical anchor with HLR-20.440-001..008 + contract elements + TCU)
- 50.210_scheduler_design_spec.md (constructed per 50.05)

All Phase B evidence **SHALL** be traceable to the relevant sources above.