# 40.40_scheduler_prototypes / software_description.md

## Approval State
Scaffold only (not implementation-complete).

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

- **Backward Flow (40-series evidence)**: No evidence collected yet; this is the initial scaffold. (Note: prior exploration produced HLR-20.440-* in 10.50.40, but this scaffold supports additional or refreshed exploration.)

- **Iterative Design Flow (50-series influence)**: The downstream 10.50.40_scheduler_requirements.md exists with HLR-20.440-001 to 003 (determinism/replayability, fairness/starvation prevention, input validation). This scaffold can explore and provide evidence to refine or validate those.

**Agreement Statement**: Scaffold stage only. The three flows are provisionally aligned on the scheduler as the non-cognitive, deterministic control-plane layer for execution ordering, resource enforcement, and replayable observability. Full alignment (including explicit three-flow statements in all core docs) will be recorded after Phase A approval of this software_description and after Phase B execution produces traceable evidence against the 10.10.40 and 20-series sources.

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
- Define or hard-code final policy algorithms, tie-break orders, or numeric thresholds (these are governed by 20.95/50-series and 10.50.40)
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
After explicit human approval of this Phase A `software_description.md`, implement `prototype.py` + `harness.py` (a minimal deterministic scheduler that accepts tick context and policy configuration and emits selection decisions + observability while preserving all invariants from 10.10.40 and 20-series), then populate `verification_capsule.md` and `requirements_delta.md` with executed evidence.

Both of those documents **SHALL** also contain Flows Alignment Statements + Agreement Statements per 40.20_master_program_guide.md.

All work must preserve the non-cognitive, deterministic, bounded, replayable, and safety-first nature of the scheduler.

## Traceability
- 10.10.40_scheduler_and_regulator_architecture.md (primary detailed architecture source for roles, ordering, cycle/timing model, interrupts, safety, logging)
- 20.30_ts_functional_model.md (scheduling phase and functional pipeline ordering)
- 20.40_ob_requirements.md (tick-level observability and replayability)
- 20.90_ib_requirements.md and 20.90_ts_parameter_table.md (deterministic interfaces and scheduler parameters)
- 20.150_tcu_budgeting_requirements.md (budgeting and efficiency constraints)
- 20.170_safety_requirements.md (fairness and failure behavior)
- 20.200_traceability_matrix.md (test obligations)
- 10.10.10_system_architecture.md, 10.10.20_interprocess_communication_and_channels.md, 10.10.30_interrupts_and_preemption_model.md, 10.10.50_module_contracts_and_visibility_rules.md, 10.10.60_coprocessor_offload_and_portability_rules.md (supporting architecture)
- 10.50.40_scheduler_requirements.md (downstream canonical anchor with HLR-20.440-001..003)

All Phase B evidence **SHALL** be traceable to the relevant sources above.