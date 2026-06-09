# Requirements Delta

## Purpose

This file records requirement-change proposals, implementer feedback, and migration notes for `40.270_scheduler_prototypes`.

## Flows Alignment Statement (per 40.160)

- **Forward Flow (10/20-series)**: Primary architecture from 10.10.40_scheduler_and_regulator_architecture.md (deterministic execution controller; roles for ordering, cycle boundaries, timing budgets, interrupt windows (pre-OB/post-TB/post-TR/pre-merge etc.), preemption, message handling, safety envelopes, logging/replayability, non-cognitive/non-mutating). Supporting HLRs/guidance:
  - 20.30_ts_functional_model.md (scheduling phase, pipeline ordering)
  - 20.40_ob_requirements.md (tick-level observability, replayability)
  - 20.90_ib_requirements.md + 20.90_ts_parameter_table.md (deterministic interfaces, scheduler.cycle_time.*, interrupt latencies)
  - 20.150_tcu_budgeting_requirements.md (per-tick budgeting, bounded cost)
  - 20.170_safety_requirements.md (fair progress, starvation prevention, deterministic failure)
  - 20.200_traceability_matrix.md (fairness/determinism test obligations)
  - 10.10.10/10.10.20/10.10.30/10.10.50/10.10.60 supporting contracts.

- **Backward Flow (40-series evidence)**: Phase B execution of this module (2026-06-06) produced 12/12 PASS scenarios + artifact exercising all 10 "What Phase B Must Explore" items from the approved software_description.md. Evidence (selection determinism + replay digests, tie-break provenance/rationale, interrupt window + preempt logging, timing/budget status modeling, cohort/merge metadata, rich last_* observability in snapshots, bounded history trim + asserts, fairness counters with starvation bounds, negative-path rejections) is now available for promotion through 30.40. This legitimately informs backward updates to 10.50.40 and 50-series without bypassing layers.

- **Iterative Design Flow (50-series influence)**: Downstream 10.50.40_scheduler_requirements.md (HLR-20.440-001 determinism/replay, -002 fairness/starvation, -003 input validation + TCU scheduler budget sections) shaped the exploration scope and HLR mapping. Phase B evidence (especially new obs fields, history bound, window/preempt, cohort) can drive iterative refinement of those HLRs or the scheduler design spec (50.40 or via 50.05).

**Agreement Statement**: The three flows are aligned on the scheduler prototype as a minimal, non-cognitive, deterministic control-plane explorer. All evidence is replayable (sorted-key JSON + verification_digest), bounded (history_max, positive contracts), and safety-first. No cognitive logic or core state mutation was introduced. Open items (canonical policy choice, exact tie-break precedence for 50) remain for higher layers; Phase B provides data not decisions. Full three-flow statements also appear in the updated verification_capsule.md and software_description.md.

## Evidence-Backed Requirement Deltas (Phase B Executed)

| HLR / Item | Status | Evidence Scenario(s) | Traceability / IO Fields | Notes |
|------------|--------|----------------------|--------------------------|-------|
| HLR-20.440-001 (determinism / replay) | Strongly demonstrated | positive_deterministic_replay, positive_rich_observability, positive_bounded_history | tick, policy, max_active, selected_tp_ids, history, verification_digest, last_*_rationale, digest match on replay | Identical event seq → identical snapshot + digest; all under deterministic_mode |
| HLR-20.440-002 (fairness / bounded progress / no starvation) | Strongly demonstrated | positive_round_robin_fairness, positive_fairness_starvation_prevent, positive_cohort_selection_merge | selected_tp_ids, wait_ticks, total_selected, last_scheduled_tick, max_wait_observed | RR cycles fairly; 20-tick run shows max_wait bounded (~2 for 3 TPs); cohort of 2 ok |
| HLR-20.440-003 (input validation / negative paths) | Strongly demonstrated | negative_empty_tp_id, negative_non_monotonic_tick, negative_invalid_policy | tp_id, tick, event_type, policy | Construction rejects empty set (empty active); apply rejects non-mono tick and unknown policy |
| HLR-20.440-006 (interrupt windows + preemption) | Strongly demonstrated | positive_interrupt_window_preemption | window, preempt, history, payload | Events carry "pre_ob", "post_tb", preempt=True; logged for replay/audit |
| HLR-20.440-005 (bounded internal state / timing budgets + cycle) | Strongly demonstrated | positive_timing_budget_and_cycle, positive_bounded_history | budget_tcu, budget_status, tick (monotonic), history_max | sim_tcu + within_budget modeled; strict increasing tick enforced; history bounded+trimmed |
| HLR-20.440-007 (cohort + merge semantics) | Strongly demonstrated | positive_cohort_selection_merge, positive_rich_observability | cohort_metadata (is_cohort, cohort_size, merge_semantics), max_active, selected | When max_active>1 emits deterministic merge meta; stable order |
| HLR-20.440-004 (rich replay-safe observability) | Strongly demonstrated | positive_rich_observability, positive_tie_break_provenance, all positives | last_selection_rationale, last_cohort_metadata, last_window, last_budget_status, history, thoughtpoints.* (wait/total) | Rationale includes cursor/score/tie logic; fairness counters on TP view; full event log |
| HLR-20.440-008 (tie-break provenance) | Strongly demonstrated | positive_tie_break_provenance | tie_break_rationale (incl. "stable tp_id asc"), selected | Explicit rationale + secondary key sort for equal scores |
| HLR-20.440-005 (bounded internal state) | Strongly demonstrated | positive_bounded_history | history_max, history (len <= max after trim), assert_invariants | history_max=4 exercised; trim on _record_event + init; invariants check bound |
| HLR-20.440-003 (negative empty active) | Strongly demonstrated | negative_empty_tp_id (and construction contract) | tp_id (empty) | Empty active set at init rejected deterministically (per "empty active set" example in software_description) |
| LLR-30.40-001 (artifact emission) | Strongly demonstrated | (all) + harness main | full report with summary 12/12, per-scenario io_fields + status, run_timestamp | artifacts/scheduler_verification_run_2026-06-06.json (sorted JSON) |

## Rationale

- Scheduler is the core deterministic control plane; Phase B focused on producing auditable, replayable evidence for its obligations per 10.10.40 without absorbing regulator/GB or cognitive concerns.
- The 10 "Must Explore" items (software_description) were each given explicit scenario coverage so that 30/50/10.50 can trace specific behaviors.
- Negative paths + bounded state + rich obs were prioritized because they directly mitigate replay divergence and silent fairness/starvation bugs.
- Exploratory weighted policy + weights are explicitly non-canonical (documented in rationale strings + Non-Goals); used only to generate tie-break + cohort evidence.

## Impacted Documents

- `software_description.md` (Phase B executed record + updated flows/agreement)
- `prototype.py` (bounded history, rich obs payload/snapshot, interrupt/window/budget/cohort support, select returns rationale+meta, invariants)
- `harness.py` (12 scenarios covering 10 items + repro; refreshed anchors + artifact 2026-06-06)
- `verification_capsule.md` (expanded ledger, invariants, flows/agreement)
- `artifacts/scheduler_verification_run_2026-06-06.json`
- Downstream (future): 30.40_* (promotion), 10.50.40 (updated with HLR-004..008), 50.40_scheduler_design_spec.md

## Open Validation Needed (unchanged from prior; now with data)

- Confirm canonical default policy decision: `round_robin` vs `weighted_round_robin` (or aging variant) — Phase B shows both are implementable deterministically with provenance.
- Confirm formal tie-break key order for weighted (and any production policy) once 50-series defines it.
- Additional runtime negative paths (e.g. empty active mid-cycle after hypothetical deactivate) can be added in future iterations or test benches.

## Migration Notes

- Scheduler prototype now emits rich, versioned, replay-safe observability (rationale, cohort, window, budget_status) in every schedule_tick event and top-level snapshot.
- Contract remains stable (contract_version 1.0); added history_max + last_* fields are additive and backward-compatible for consumers.
- All JSON is produced with sort_keys + digest for exact replay.
- 30.40/ will hold the promoted verification record; this 40.270 delta is the exploratory source-of-truth.
- Future deltas should append (or reference prior) rather than wholesale replace.

## Testbench-Driven Changes
(none this iteration; all evidence from 40 harness per 40.160. Future real testbenches under testbenches/ will feed only via 30.tb/ normalized records.)

