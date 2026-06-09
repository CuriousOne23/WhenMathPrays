# 40.320_regulator_prototypes / software_description.md

## Approval State
- Phase A (software_description): approved (per CP review confirming the 20-series anchors)
- Phase B (prototype + harness + evidence): executed 2026-06-06

## Phase B Deliverables (Executed)
- Harness scenarios executed: 15/15 PASS
- Artifact: `artifacts/regulator_verification_run_2026-06-06.json` (generated 2026-06-06, contains full scenario ledger, deterministic digests, input/output for replay)
- Coverage of all 12 "What Phase B Must Explore" items (via dedicated scenarios + supporting):
  - Deterministic ΔH% enforcement + L-interrupts — delta_h_enforcement, interrupt_generation
  - Deterministic routing fan-out enforcement — fan_out_enforcement
  - Deterministic operator cost enforcement — operator_cost_enforcement
  - Overflow detection + deterministic degradation — overflow_enforcement
  - Memory/resource bounds enforcement — memory_bound_enforcement
  - Cycle time bounds monitoring + L2 — cycle_time_enforcement
  - Generation of regulatory interrupts (L0/L1/L2) — interrupt_generation, various high-pressure scenarios
  - Explicit auditable decision outputs with separation — explicit_auditable_decision, rich_observability
  - Input validation + deterministic rejection — negative_invalid_policy, negative_negative_pressure
  - Rich replay-safe observability and logs — rich_observability, all scenarios (enforcements, interrupt_level, obs fields)
  - Bounded internal state for regulator — bounded_internal_state
  - Full support for deterministic mode — full_deterministic_mode, positive_deterministic_replay
- Additional invariants demonstrated: non-cognitive (no core state mutation), read-only decisions, replay via digest + sorted JSON, safety envelopes (interrupt levels, degradation), bounded history in stateful Regulator, contract validation, exploratory policies (non-final per Non-Goals).
- Note: policies (clamp/attenuate/stabilize) and thresholds in prototype are exploratory only for evidence generation; no final numeric or algorithm claims (governed by 20.95/50-series and 10.50.50).

## Scaffold Metadata
- scaffold_status: planned
- intended_10_10_anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.40_scheduler_and_regulator_architecture.md
- intended_20_anchors:
  - thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md
  - thought_simulator/20_requirements/20.170_safety_requirements.md
  - thought_simulator/20_requirements/20.200_traceability_matrix.md
  - thought_simulator/20_requirements/20.30_ts_functional_model.md
  - thought_simulator/20_requirements/20.40_ob_requirements.md
  - thought_simulator/20_requirements/20.90_ib_requirements.md
  - thought_simulator/20_requirements/20.90_ts_parameter_table.md
- applicability: planned exploratory module for regulator safety envelope and resource constraint enforcement behavior (ΔH% limits, routing fan-out, operator costs, overflow detection, memory bounds, cycle time bounds, regulatory interrupt generation)
- disposition_target: promote

## Purpose
This scaffold reserves the module slot for future exploratory implementation of regulator prototypes in the 40-layer.

It corresponds directly to the regulator architecture defined in 10.10.40_scheduler_and_regulator_architecture.md (the safety and resource enforcer) and supporting HLRs and principles in the 20-series.

The regulator is the **safety and resource enforcer** of the TS. It is responsible for:
- ΔH% enforcement (hard/soft limits, monotonicity rules, normalization)
- routing fan-out limits (max branches, inquiry depth, parallel operators, TP proliferation)
- operator cost limits (per-operator profiles, cumulative cycle cost)
- overflow detection and deterministic degradation
- memory and resource bounds (buffers, queues, snapshots)
- cycle time bounds (module, interrupt, merge, commit)
- safety envelope enforcement
- generating regulatory interrupts (L0, L1, L2)

The regulator **does not**:
- perform cognitive inference
- modify semantic content
- alter TP or MTP state
- override scheduler ordering

## Scope
- placeholder module for requirements-driven exploration of regulator enforcement behavior
- no executable behavior is asserted yet
- will explore: deterministic ΔH% enforcement and interrupt generation, fan-out limit enforcement, operator cost limit enforcement, overflow detection and degradation, memory/cycle time bound enforcement, explicit auditable decision outputs with rationale codes, input validation for policy modes and pressure values, emission of replay-safe observability and audit logs, preservation of separation (no core cognitive state mutation, no scheduler override), bounded internal state and resources, full deterministic mode.

All exploration **SHALL** remain strictly deterministic, non-cognitive, and non-mutating to core cognitive state, and must not override scheduler ordering, per 10.10.40 and 20-series principles.

## Flows Alignment Statement

- **Forward Flow (10/20-series)**: Driven by the detailed architecture in 10.10.40_scheduler_and_regulator_architecture.md (regulator role and responsibilities, ΔH% enforcement details, routing fan-out limits, operator cost limits, overflow detection, memory and cycle time bounds, safety envelope enforcement, generating regulatory interrupts, scheduler–regulator event flow and handoff, separation of concerns, forbidden interactions, hard/soft safety envelopes, logging and replayability, conformance obligations) and supporting 20-series guidance:
  - 20.150_tcu_budgeting_requirements.md (TCU budgeting, min/typ/max ranges, overrun handling, per-tick accounting, calibration, which the regulator enforces)
  - 20.170_safety_requirements.md (deterministic fail-safe termination, bounded resource utilization, emergency control, prohibited unsafe pathways, explicit audit, which the regulator enforces via limits and interrupts)
  - 20.200_traceability_matrix.md (test obligations for safety and TCU enforcement)
  - 20.30_ts_functional_model.md (functional pipeline ordering, fan-out limits, overflow handling and degradation, TCU allocation and per-subsystem budgets)
  - 20.40_ob_requirements.md (OB TCU budgets, boundedness constraints, overflow/degradation tags and telemetry)
  - 20.90_ib_requirements.md and 20.90_ts_parameter_table.md (IB/parameter enforcement points, TCU profiles, bounds, lifecycle logging relevant to regulator monitoring)

- **Backward Flow (40-series evidence)**: No evidence collected yet; this is the initial scaffold. (Note: prior exploration produced HLR-20.450-* in 10.50.50, but this scaffold supports additional or refreshed exploration.)

- **Iterative Design Flow (50-series influence)**: The downstream 10.50.50_regulator_requirements.md exists with HLR-20.450-001 to 003 (determinism/replay for decisions, explicit auditable action outputs, input validation for policy/pressure) + TCU regulator budget sections. The 50.50_regulator_design_support.md provides initial contracts and obligations. This scaffold can explore and provide evidence to refine or validate those.

**Agreement Statement**: Scaffold stage only. The three flows are provisionally aligned on the regulator as the non-cognitive, deterministic safety and resource enforcement layer responsible for ΔH%, fan-out, costs, overflow, memory, cycle time, and regulatory interrupt generation, with strict separation from the scheduler (when) and GB (why). Full alignment (including explicit three-flow statements in all core docs) will be recorded after Phase A approval of this software_description and after Phase B execution produces traceable evidence against the 10.10.40 and 20-series sources.

## Phase A Deliverables (this document)
- High-level description of regulator behavior for exploratory prototyping
- Mapping of 10.10/20-series intent to prototype responsibilities
- Identification of unknowns, ambiguities, and missing definitions
- Clear definition of what Phase B must explore
- No algorithms, data structures, numeric thresholds, or implementation details

## What Phase B Must Explore
Phase B **SHALL** explore and produce concrete (deterministic, replayable) evidence for at least:

- Deterministic enforcement of ΔH% hard and soft limits, monotonicity rules, and normalization (may be offloaded), generating appropriate L0/L1/L2 regulatory interrupts on violation.
- Deterministic enforcement of routing fan-out limits (maximum branches, inquiry depth, parallel operators, TP proliferation), with degradation or interrupt on breach.
- Deterministic enforcement of operator cost limits (per cognitive operator cost profiles, maximum allowed, cumulative cycle cost), issuing L2 slowdowns or scheduler frequency reduction on overrun.
- Overflow detection and deterministic degradation behavior (lane/evidence truncation, ΔH% normalization, fan-out reduction, provenance compression) with full telemetry, reason codes, and audit records.
- Enforcement of memory and resource bounds (buffer size, queue depth, snapshot size limits), triggering deterministic L1 safe-mode or L0 emergency stop on violation.
- Monitoring of cycle time bounds (cycle duration, module execution, interrupt handling, merge, commit) and generation of L2 slowdowns or scheduler timing window adjustments when exceeded.
- Generation of regulatory interrupts (L0 emergency stop for hard violations, L1 safe-mode for soft, L2 dampen/slowdown for minor), with correct severity classification, scheduler handoff, and full logging.
- Production of explicit, auditable regulator decision outputs (action type, rationale code, applied limits/deltas, affected subsystems/entities, boundary markers, policy signatures) while strictly preserving separation (no mutation of TP/MTP or other core cognitive state, no reordering or override of scheduler).
- Input validation and deterministic rejection or safe degradation for malformed inputs (unsupported policy modes, negative or out-of-range pressure values, contradictory contexts or missing required fields).
- Emission of rich, replay-safe observability and logs for all regulator decisions and events (including full lineage, reason codes, policy signatures, applied effects, boundary context, affected state) for audit, diagnosis, and 30-series verification.
- Bounded internal state and resource usage for the regulator subsystem itself (e.g. policy state, decision history, logs), consistent with 10.10.40 safety envelopes and 20.150 TCU constraints.
- Full support for deterministic mode (no nondeterministic optimizations that could alter observable decisions, interrupt behavior, logs, or replay).

## Non-Goals (Scaffold and Initial Phase B)
This module **SHALL NOT**:
- Perform any cognitive, semantic, or interpretation logic (strictly non-cognitive per 10.10.40)
- Mutate TP, MTP, or other cognitive state (or bypass safe boundaries to do so)
- Define or hard-code final numeric thresholds, limits, cost profiles, or policy values/algorithms (these are governed by 20.95/50-series and 10.50.50)
- Override scheduler ordering, timing, or preemption decisions (focus on "whether" enforcement, not "when")
- Implement the full control plane (GB supervisory, etc.); focus on enforcement decisions, interrupt generation, and observability logic
- Assume specific hardware or runtime details beyond the portable contracts in 10.10.60

## Risks & Unknowns to Investigate (aligned with 10.10.40 and 20.10)
- Selection of canonical regulator action taxonomy (e.g. clamp, attenuate, stabilize, crop, prune, kill, etc.) and their precise semantics/effects on pressure/ΔH%/trajectory/fan-out.
- Precise canonical decision precedence, tie-break, or aggregation logic when multiple violations (ΔH%, fan-out, cost, overflow, time, memory) occur simultaneously or cascade.
- Exact integration and handoff points with scheduler for regulatory interrupt generation, queuing at safe windows, and enforcement actions.
- Performance and determinism under high load (frequent/cascading violations, high fan-out scenarios, many concurrent operators, large memory pressure).
- Edge cases: empty or minimal state on violation, mid-cycle reconfiguration, interaction with coprocessor offload for normalization/TCU, simultaneous hard + soft conditions, fail-open vs fail-closed behavior.
- Ensuring strict separation and no leakage of cognitive state, nondeterminism, or scheduler override into regulator decisions or logs.
- Calibration, versioned policy binding, and profile-specific enforcement for TCU/safety without introducing replay divergence or silent truncation.

## Required Next Step
Phase B complete (see Phase B Deliverables above and updates to requirements_delta.md + verification_capsule.md with full evidence + three-flow statements).

Next (per 40.05 + 30.00): human may request 30.00 promotion step on this module (copy artifact + refresh 30.50 delta/capsule as canonical verification record). Evidence is now available to inform 10.50.50 refinements or 50.50_regulator_design_support.md (and any 50.50 main spec) via 50.05 patterns, always through 30.

All Phase B work preserved the non-cognitive, deterministic, bounded, replayable, and safety-first nature of the regulator (see invariants in capsule).

## Traceability
- 10.10.40_scheduler_and_regulator_architecture.md (primary detailed architecture source for regulator roles, ΔH% / fan-out / cost / overflow / memory / cycle time enforcement, interrupt generation L0/L1/L2, scheduler–regulator interaction, separation of concerns, safety envelopes, logging/replayability, conformance)
- 20.150_tcu_budgeting_requirements.md (TCU budgeting and enforcement obligations that regulator must uphold)
- 20.170_safety_requirements.md (safety constraints, fail-safe, bounded resources, emergency control, prohibited unsafe pathways that regulator enforces)
- 20.200_traceability_matrix.md (test obligations)
- 20.30_ts_functional_model.md (functional pipeline, fan-out limits, overflow handling and degradation, TCU allocation)
- 20.40_ob_requirements.md (OB TCU, boundedness, overflow tags/telemetry)
- 20.90_ib_requirements.md and 20.90_ts_parameter_table.md (IB/parameter enforcement points, TCU, bounds, logging)
- 10.10.10_system_architecture.md, 10.10.20_interprocess_communication_and_channels.md, 10.10.30_interrupts_and_preemption_model.md, 10.10.36_gb_requirements.md, 10.10.50_module_contracts_and_visibility_rules.md, 10.10.60_coprocessor_offload_and_portability_rules.md (supporting architecture and conformance)
- 10.50.50_regulator_requirements.md (downstream canonical anchor with HLR-20.450-001..003 + TCU regulator budgets)
- 50.50_regulator_design_support.md (downstream design support)
- 30.50_regulator_prototypes/ (current verification records; to be refreshed post Phase B)
- 40.05_master_program_guide.md and 30.00_verification_user_guide.md (process)

All Phase B evidence **SHALL** be traceable to the relevant sources above.
