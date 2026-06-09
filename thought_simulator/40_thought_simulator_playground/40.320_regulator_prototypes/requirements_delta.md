# Requirements Delta

## Flows Alignment Statement (per 40.05)

- **Forward Flow (10/20-series)**: Driven by the detailed architecture in 10.10.40_scheduler_and_regulator_architecture.md (regulator role, ΔH% / fan-out / cost / overflow / memory / cycle time enforcement, interrupt generation, separation) and the listed 20-series sources in the 40.320_regulator_prototypes/software_description.md (TCU budgeting, safety constraints, functional model fan-out/overflow, OB/IB bounds and TCU, parameter table enforcement, traceability).
- **Backward Flow (40-series evidence)**: No evidence collected yet; this is the initial scaffold. Preliminary prototype/harness exist but full Phase B evidence collection awaits Phase A approval.
- **Iterative Design Flow (50-series influence)**: Downstream 10.50.220_regulator_requirements.md (HLR-20.450-001..003 + TCU) and 50.50_regulator_design_support.md exist as anchors. This scaffold (and future Phase B) can explore and provide evidence to refine or validate those.

**Agreement Statement**: Scaffold stage only. The three flows are provisionally aligned on the regulator as the non-cognitive, deterministic safety/resource enforcement layer. Full alignment will be recorded after Phase A approval and Phase B execution.

## Evidence-Backed Requirement Deltas (Phase B Executed)

| Explore Item / HLR | Status | Evidence Scenario(s) | Traceability / IO Fields | Notes |
|--------------------|--------|----------------------|--------------------------|-------|
| ΔH% enforcement + L-interrupts (10.10.40 + 20.170/20.30) | Strongly demonstrated | delta_h_enforcement, interrupt_generation | enforcement_area, interrupt_level, enforcements.delta_h, rationale, obs | L1 on exceed; explicit per-area |
| Routing fan-out limits (20.30/20.90) | Strongly demonstrated | fan_out_enforcement | enforcement_area, interrupt_level=L2, enforcements.fan_out | Count-based, L2 on breach |
| Operator cost limits (20.150/20.30) | Strongly demonstrated | operator_cost_enforcement | enforcement_area, interrupt_level=L2, applied_delta | Cumulative cost model |
| Overflow detection + degradation (20.30/20.40) | Strongly demonstrated | overflow_enforcement | enforcement_area, interrupt_level=L1, obs.degradation | Truncation/normalization signals |
| Memory/resource bounds (20.170/20.150) | Strongly demonstrated | memory_bound_enforcement | enforcement_area, interrupt_level=L1 | Buffer/queue/snapshot model |
| Cycle time bounds (20.150/10.10.40) | Strongly demonstrated | cycle_time_enforcement | enforcement_area, interrupt_level=L2 | Per-cycle timing model |
| Regulatory interrupt generation (L0/L1/L2) (10.10.40) | Strongly demonstrated | interrupt_generation + high-pressure scenarios | interrupt_level, obs, rationale with area | Severity mapping L1/L2 |
| Explicit auditable decisions + separation (10.10.40 + 10.50.220 HLR-002) | Strongly demonstrated | explicit_auditable_decision, rich_observability | action, rationale, applied_delta, enforcement_area, obs (enforcements, boundary_marker, policy_signature) | No core mutation; rich fields |
| Input validation + rejection (10.50.220 HLR-003) | Strongly demonstrated | negative_invalid_policy, negative_negative_pressure | error on bad policy/negative pressure | Deterministic ValueError |
| Rich replay-safe observability (10.10.40 + 20.40/20.90) | Strongly demonstrated | rich_observability + all | obs (enforcements, interrupt_level, areas_covered, policy_signature, total_applied_impact), rationale | Per-area + overall |
| Bounded internal state (10.10.40 + 20.150/20.170) | Strongly demonstrated | bounded_internal_state | history_len (trimmed to max_history=4), state_counter | Class Regulator with decision_history |
| Full deterministic mode (10.50.220 HLR-001) | Strongly demonstrated | full_deterministic_mode, positive_deterministic_replay | identical outputs + digest on replay; no nondet paths | Always det; stateful replay |
| HLR-20.450-001 (determinism/replay) | Strongly demonstrated | positive_deterministic_replay + full_deterministic_mode | verification_digest, identical decisions | Core 10.50.220 HLR |
| HLR-20.450-002 (explicit auditable actions) | Strongly demonstrated | explicit_auditable_decision, positive_policy_comparison | action, rationale, applied_delta, obs | Policy differentiation stable |
| HLR-20.450-003 (input validation) | Strongly demonstrated | negative_* scenarios | ValueError on bad policy/pressure | Per 10.50.220 |
| LLR-30.220-001 (artifact emission) | Strongly demonstrated | all + harness main | full report, 15/15, per-scenario io_fields + status + digests | artifacts/regulator_verification_run_2026-06-06.json |

## Rationale

- Regulator is the core deterministic safety/resource enforcer; Phase B focused on producing auditable, replayable evidence for its obligations per 10.10.40 + the 20-series (TCU, safety, functional model, OB/IB bounds, parameters) without absorbing cognitive or scheduling logic.
- The 12 "What Phase B Must Explore" items were each given explicit scenario coverage (plus supporting) so that 30/10.50.220/50.50 can trace specific behaviors (ΔH%, fan-out, costs, overflow, bounds, interrupts, decisions, validation, obs, bounded state, determinism).
- Negative paths + bounded state + rich obs prioritized to mitigate replay divergence and silent violation handling bugs.
- Exploratory policies (clamp/attenuate/stabilize) and simple thresholds in prototype are explicitly non-canonical (documented in rationale/obs + Non-Goals); used only to generate evidence for the enforcement model.

## Impacted Documents

- `software_description.md` (Phase B executed record + updated flows/agreement)
- `prototype.py` (rich multi-area enforcement, interrupt levels, rich obs, stateful Regulator with bounded history)
- `harness.py` (15 scenarios covering 12 items + repro + negatives; refreshed anchors + artifact 2026-06-06)
- `verification_capsule.md` (expanded ledger, invariants, flows/agreement)
- `artifacts/regulator_verification_run_2026-06-06.json`
- Downstream (future): 30.220_* (promotion), 10.50.220, 50.50_regulator_design_support.md (and any main 50.50 spec)

## Open Validation Needed (post Phase B data)

- Confirm canonical regulator action taxonomy and exact semantics for each enforcement area (beyond exploratory clamp/attenuate/stabilize).
- Define normative tie-break / aggregation when multiple areas violate simultaneously.
- Minimum regulator decision schema fields for canonical 10.50.220 audit/replay (current rich obs is strong evidence).
- Calibration/versioning of per-area limits and policy signatures (governed by 20.95/50 + 10.50.220).

## Migration Notes

- Regulator prototype now emits rich, versioned, replay-safe observability (per-area enforcements, interrupt_level, obs with boundary/policy_signature, history_len) in every decision.
- Contract remains stable; added multi-area support, interrupt_level, obs, history are additive and backward-compatible.
- All JSON produced with sort_keys + digest for exact replay.
- 30.220/ will hold the promoted verification record; this 40.320 delta is the exploratory source-of-truth.
- Future deltas should append (or reference prior) rather than wholesale replace.

## Testbench-Driven Changes
(none this iteration; all evidence from 40 harness per 40.05. Future real testbenches under testbenches/ will feed only via 30.tb/ normalized records.)
	- `negative_negative_pressure` PASS

