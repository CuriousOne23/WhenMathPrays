# 40.280_tick_cycle_skeleton / software_description.md

## Approval State
- Phase A (software_description): approved (per human review 2026-05-28 confirming the cycle skeleton intent)
- Phase B (prototype + harness + evidence): executed 2026-05-28

## Phase B Deliverables (Executed)
- Harness scenarios executed: 3/3 PASS
- Artifact: `artifacts/tick_cycle_verification_run_2026-05-28.json` (generated 2026-05-28, contains full scenario ledger, deterministic outputs, digests, and error messages for replay)
- Coverage of core "What Phase B Must Explore" items (via dedicated scenarios + supporting logic):
  - Deterministic enforcement of monotonic tick advancement — negative_non_monotonic_tick
  - Enforcement of fixed canonical phase sequence with no re-entry or deviation — negative_invalid_phase_order, positive_deterministic_replay using exact CANONICAL_PHASES match
  - Generation of replay-safe evidence fields (tick, executed_phases list, state_digest) — all scenarios, especially positive_deterministic_replay (identical outputs across independent TickCycle instances)
  - Input validation and deterministic rejection for malformed inputs (non-monotonic/negative ticks, non-matching phase lists) — the two negative scenarios with precise error messages
  - Full support for deterministic mode (identical contract produces identical output sequences and digests) — positive_deterministic_replay
- Additional invariants demonstrated: strict phase ordering, no cross-tick state leakage in the skeleton, JSON-serializable outputs, cryptographic digest for replay verification, clean separation (the skeleton performs no semantic/cognitive work).
- Note: The four phases ("schedule", "process", "transition", "log") and the enforcement logic are exploratory only for evidence generation; final phase responsibilities and integration with the full TS cycle model are governed by 10.10.40 and 20-series.

## Scaffold Metadata
- scaffold_status: executed
- intended_10_10_anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.40_scheduler_and_regulator_architecture.md (cycle model, pre-cycle checks, module execution sequence, cycle boundary enforcement, monotonic timestamps, strict ordering, deterministic cycle start/end)
- intended_20_anchors:
  - thought_simulator/20_requirements/20.30_ts_functional_model.md (determinism, per-tick behavior, pipeline determinism, interpretability)
  - thought_simulator/20_requirements/20.40_ob_requirements.md (observability of execution and lifecycle)
  - thought_simulator/20_requirements/20.170_safety_requirements.md (deterministic fail-safe termination, bounded behavior, explicit audit)
  - thought_simulator/20_requirements/20.200_traceability_matrix.md
  - thought_simulator/20_requirements/20.90_ib_requirements.md
- applicability: exploratory low-level skeleton for deterministic tick execution mechanics inside TS cycles (monotonic advancement, fixed phase ordering, replay-safe boundaries and evidence emission)
- disposition_target: promote

## Purpose
This scaffold reserves the module slot for exploratory implementation of a minimal deterministic tick-cycle skeleton.

It corresponds directly to the cycle execution model defined in 10.10.40_scheduler_and_regulator_architecture.md (the deterministic execution controller responsible for ordering, cycle boundaries, monotonic timestamps, strict event ordering, and no cross-cycle leakage) and supporting principles in the 20-series.

The tick cycle skeleton is the **inner deterministic execution mechanism** for TS cycles. It is responsible for:
- Maintaining strictly monotonic, non-negative tick indexing
- Enforcing a fixed, canonical sequence of phases within each tick with no re-entry or out-of-order execution
- Producing explicit, replay-safe evidence of phase execution and state transitions (via digests and phase lists)
- Deterministically rejecting violations of monotonicity or phase ordering

The skeleton **does not**:
- Perform cognitive inference or semantic processing
- Define the final responsibilities or contracts for individual phases
- Implement full scheduler logic, TCU budgeting, ΔH% accounting, or interrupt windows (those belong to the broader scheduler/regulator)
- Mutate external module state

## Scope
- skeleton module for requirements-driven exploration of core tick execution invariants
- executable enforcement of monotonicity and phase ordering
- will explore: deterministic phase sequencing, tick advancement rules, input validation and rejection, replay via digest, clean error signaling for violations

All exploration **SHALL** remain strictly deterministic, non-cognitive, and replayable.

## Enforcement Scope

| Aspect                  | Skeleton Enforces                                      | Does Not Define or Enforce                          | Delegated To (10-series / Upstream) |
|-------------------------|--------------------------------------------------------|-----------------------------------------------------|-------------------------------------|
| Tick indexing           | Strictly monotonic, non-negative integer, advances by exactly +1 | Semantic meaning or origin of tick numbers          | Full cycle model in 10.10.40       |
| Phase sequencing        | Exact match to fixed canonical list; no re-entry, omission, or reordering within a tick | Responsibilities, side-effects, or contracts of individual phases ("schedule", "process", etc.) | 10.10.40 module execution sequence and pipeline stages |
| Evidence emission       | tick + executed_phases list + state_digest (sha256 of sorted JSON) for replay verification | Rich per-phase telemetry, MB/GB integration, or higher-level logging | 20.40 observability and 10.10.40 transparency requirements |
| Violation handling      | Deterministic rejection with specific, auditable error messages | Error classification (terminal vs. recoverable), escalation, or recovery semantics | 20.170 safety and regulator        |

## Evidence Schema

The skeleton produces the following normative evidence for every executed tick (JSON-compatible, replay-verifiable):

- `tick`: integer (monotonic, non-negative)
- `executed_phases`: ordered list of strings, exactly matching the canonical sequence used for that tick
- `state_digest`: string — SHA-256 hex digest of the canonical JSON serialization (`json.dumps({"tick": tick, "phases": phases}, sort_keys=True, separators=(",", ":"))`)

This schema is sufficient for cross-run deterministic replay verification and for detecting any deviation in ordering or tick advancement. Richer per-phase diagnostics, MB telemetry, or provenance are explicitly out of scope for this skeleton (delegated to 20.40 and 10.10.40 observability layers).

## Flows Alignment Statement

- **Forward Flow (10/20-series)**: Driven by the detailed cycle model in 10.10.40_scheduler_and_regulator_architecture.md (A TS cycle consists of pre-cycle checks, module execution sequence, TR dirty-flag gate, interrupt window, supervisory review, regulation, commit, cycle boundary enforcement; guarantees no cross-cycle state leakage, deterministic cycle start and end, monotonic timestamps, strict ordering of events) and 10.10.10_system_architecture.md (deterministic cycles, architectural principles of determinism, replayability, boundedness, transparency), plus supporting 20-series guidance:
  - 20.30_ts_functional_model.md (core determinism HLR-20.030-001 and -008, per-tick cost reporting and bounded behavior HLR-20.030-011, architectural behavior interpretability HLR-20.030-014, pipeline stage determinism)
  - 20.40_ob_requirements.md (observability of execution behavior and lifecycle transitions)
  - 20.170_safety_requirements.md (deterministic fail-safe termination sequencing HLR-20.170-001, safety-relevant state transitions fully logged HLR-20.170-003, unsafe nondeterministic pathways prohibited HLR-20.170-004)
  - 20.90_ib_requirements.md and 20.200_traceability_matrix.md (interface and traceability obligations)

- **Backward Flow (40-series evidence)**: No prior dedicated evidence for this low-level skeleton existed; this is the initial execution. Harness scenarios executed 2026-05-28 provide the first concrete demonstration. Positive deterministic replay shows bit-identical outputs and digests across independent runs. Negative scenarios provide deterministic rejection evidence with exact error messages for the two primary violation classes (non-monotonic tick and phase order mismatch). All outputs are JSON-compatible and digest-verifiable.

- **Iterative Design Flow (50-series influence)**: The skeleton provides executable evidence of minimal phase-ordered tick mechanics (monotonic advancement + strict ordering + replay evidence) that can be used to validate assumptions or refine contracts for the canonical tick cycle execution in the 10-series. It can surface practical questions (phase semantics, extensibility, evidence richness) for upstream resolution.

**Agreement Statement**: Scaffold + initial Phase B complete. The three flows are provisionally aligned on the tick cycle skeleton as the non-cognitive, deterministic enforcement layer for monotonic tick indexing and fixed phase sequencing within TS cycles, with strong replayability via digests and clear violation detection. Full alignment (including explicit three-flow statements in all core docs) will be recorded after Phase A approval of this software_description and after Phase B execution produces traceable evidence against the 10.10.40, 10.10.10, and 20-series sources.

## Phase A Deliverables (this document)
- High-level description of the tick cycle skeleton for exploratory prototyping
- Mapping of 10/20-series intent (cycle model, determinism, per-tick) to skeleton responsibilities
- Identification of unknowns, ambiguities, and missing definitions
- Clear definition of what Phase B must explore
- Tentative data structures/interfaces
- No final claims on phase semantics or full cycle integration (governed by 10.10.40 and 20-series)

## What Phase B Must Explore
Phase B **SHALL** explore and produce concrete (deterministic, replayable) evidence for at least:

- Deterministic enforcement of monotonic tick advancement (tick must be non-negative integer and exactly last_tick + 1; rejection of skips, repeats, or backward movement).
- Enforcement of a fixed canonical phase sequence within each tick (exact match to the defined order; no re-entry, no permutation, no omission within the tick).
- Generation of rich, replay-safe observability and evidence for every tick (tick index, exact list of executed phases, state_digest computed over the execution for verification and replay).
- Input validation and deterministic rejection or safe degradation for malformed inputs (non-integer or negative tick values, non-list phases, phases that do not exactly match the canonical ordered list).
- Full support for deterministic mode (no nondeterministic behavior; identical input contract on a fresh or reset skeleton must produce identical output sequence and identical digests; cross-run replay must succeed).
- Explicit, auditable decision outputs on violation (clear error messages distinguishing the violation type while preserving separation from any cognitive state).

## Non-Goals (Scaffold and Initial Phase B)
This module **SHALL NOT**:
- Define or hard-code final semantic responsibilities, contracts, or side-effects for the individual phases ("schedule", "process", "transition", "log" are skeletal labels only).
- Implement the full TS cycle (pre-cycle checks, interrupt windows, supervisory review, regulation, commit, end-of-cycle enforcement — those are in the broader scheduler per 10.10.40).
- Perform TCU budgeting, ΔH% accounting, or any resource/cost tracking inside the skeleton.
- Mutate TP, MTP, or other cognitive state.
- Override or implement scheduler ordering, preemption, or global cycle control.
- Assume or implement specific behavior inside the phases (the skeleton only sequences and enforces the handoff points).
- Provide production-grade observability or logging (only the minimal replay-safe evidence fields for the skeleton itself).

## Risks & Unknowns to Investigate (aligned with 10.10.40 and 20.30)
- Precise mapping of the four skeletal phases to the actual module execution sequence and pipeline stages defined in 10.10.40 and 20.30 (pre-cycle, OB/TB/IB steps, TR gate, merge, etc.).
- Whether the phase set should be strictly fixed or allow controlled extensibility/pluggability for different module types.
- Exact format and richness of phase-boundary evidence required for higher-level observability (MB pathways, event logs, GB diagnostics) while staying minimal and replay-safe.
- Error taxonomy and handling: which violations are terminal vs. recoverable, how errors should be classified and propagated (L-level interrupts vs. local ValueError), and what the skeleton should log vs. raise.
- Integration and handoff points with the scheduler (how/when the scheduler invokes the tick skeleton, how enabled phases are determined per tick, interaction with dirty flags and conditional execution).
- Performance, determinism, and state management under sustained high tick counts or when the skeleton is embedded inside a larger per-module or per-lane execution context.
- Edge cases: tick 0 start, very large tick values, empty phase list (if ever allowed), concurrent or re-entrant calls, state reset between independent runs for replay testing.
- Ensuring the skeleton remains strictly non-cognitive and does not leak or depend on semantic content.

## Required Next Step
Phase B complete (see Phase B Deliverables above and updates to requirements_delta.md with the proposed new requirement IDs for phase-order determinism and tick monotonicity).

Next (per 40.05): human may request further iteration on the skeleton, addition of more scenarios (e.g. phase-level evidence richness, integration stubs), or promotion consideration once evidence is mapped to canonical 10-series anchors. The concrete demonstration of monotonic + ordered phase enforcement with replay digests is now available to inform the 10.10.40 cycle model and any 10.50.60 tick cycle requirements.

All Phase B work preserved the non-cognitive, deterministic, bounded, replayable, and safety-first nature of the tick cycle enforcement.

## Traceability

| Upstream Source | Key Principle / Obligation | Implementation in 40.60 | Phase B Evidence |
|-----------------|----------------------------|-------------------------|------------------|
| 10.10.10_system_architecture.md | Deterministic cycles, replayability, boundedness, transparency | TickCycle class + digest emission | positive_deterministic_replay (identical outputs + digests) |
| 10.10.40_scheduler_and_regulator_architecture.md | Cycle model, monotonic timestamps, strict ordering, cycle boundary enforcement, no cross-cycle leakage | `execute_tick` monotonic + exact phase list checks | All 3 scenarios + error messages for violations |
| 20.30_ts_functional_model.md | Core determinism, per-tick behavior, pipeline determinism, interpretability | Fixed CANONICAL_PHASES ordering + state_digest | positive_deterministic_replay + harness replay comparison |
| 20.40_ob_requirements.md | Observability of execution behavior and lifecycle | `executed_phases` list + state_digest per tick | Artifact JSON with full outputs for every scenario |
| 20.170_safety_requirements.md | Deterministic fail-safe termination, logged safety transitions | Explicit ValueError on violation with precise messages | negative_non_monotonic_tick and negative_invalid_phase_order (PASS with error capture) |
| 20.90_ib_requirements.md + 20.200_traceability_matrix.md | Interface contracts and traceability | Contract dict (`tick` + `phases`) → output dict | requirements_delta.md + this document's mapping |
| ../40.05_master_program_guide.md | Playground process, self-documenting modules, three-flow alignment in software_description | This document (Flows Alignment Statement + Agreement Statement) | N/A (process compliance) |
| 40.280_tick_cycle_skeleton/prototype.py | Executable skeleton (CANONICAL_PHASES, monotonic enforcement, digest) | Core logic | All scenarios execute against this module |
| 40.280_tick_cycle_skeleton/harness.py | Test scenarios for invariants | positive_deterministic_replay + two negative cases | 3/3 PASS in artifact |
| 40.280_tick_cycle_skeleton/artifacts/tick_cycle_verification_run_2026-05-28.json | Raw deterministic evidence | Full ledger with outputs and digests | Direct artifact used for replay verification |
| 40.280_tick_cycle_skeleton/requirements_delta.md | Proposed deltas for phase-order and monotonicity requirements | Explicit calls for new HLRs | Rationale section + evidence snapshot |

All Phase B evidence **SHALL** be traceable to the relevant sources above.