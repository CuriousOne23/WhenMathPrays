# 22 Program Flow

## 1. Purpose

This document defines the **precise, deterministic program flow** of the Thought Simulator (TS) — the ordered sequence of operations executed on every tick.

It ensures the simulation is fully traceable, reproducible, and maintainable by making the per-tick pipeline explicit and unambiguous.

## 2. Core Program Flow Principles

* The TS uses a **fixed-time-step** execution model.
* Every tick follows a **strict, deterministic ordering** of phases.
* All phases are designed to be **parallel-friendly** (see [12_performance_requirements.md](12_performance_requirements.md)).
* The flow must preserve the external Observer boundary — no observer logic runs inside the core tick.
* Every state-changing action increments the **State Counter** and is logged (see 13_observability_requirements.md).
* Within each phase, operations must be ordered deterministically (e.g., sorted by TP ID or basin ID).

## 3. Full Lifecycle Flow

### 0. Initialization Phase (Pre-Tick)
- Load configuration and schema validation
- Initialize RNG with seed
- Allocate basins and regulators
- Load starting snapshot (if any)
- Set TS Step Index = 0
- Perform architectural conformance checks

### Per-Tick Cycle (Main Loop)

1. **Scheduling Phase**  
   Deterministic scheduler selects active ThoughtPoints (round-robin with optional energy/coherence weighting). Support for parallel execution of independent cohorts with deterministic merge.

2. **Creation / Injection Phase**  
   New ThoughtPoints may be injected (from experiment setup or regulators). Provenance and initial embedding assigned.

3. **Entry Conditions Phase**  
   Check eligibility for each TP to enter current or target basins.

4. **Processing Phase**  
   Apply basin-specific deterministic rules.  
   Compute entropy updates and update embeddings.  
   *Must be pure with respect to routing.*

5. **Routing & Transitions Phase**  
   Evaluate Exit Conditions.  
   Execute deterministic movement between basins (including Highways).  
   Perform Split / Merge operations with lineage preservation.  
   *Must be pure with respect to regulation.*

6. **Regulation Phase**  
   Run all active regulators in priority order.  
   Apply Flow Modulators if thresholds are breached.  
   *Must be pure with respect to completion detection.*

7. **Completion Detection Phase**  
   Check for Clean Completion, Stressed Completion, or terminal conditions.  
   Move completed TPs to Done / Terminal Basin if criteria met.

8. **Logging & Observability Phase**  
   Record all state-changing events with tick, TP ID(s), state counter, and event type.  
   Prepare incremental snapshot data if due.

9. **Snapshot & Checkpoint Phase** (optional)  
   Write full or differential snapshot using atomic write strategy.

10. **Housekeeping Phase**  
    Memory management, culling of stabilized TPs (if enabled), watchdog checks, global metrics update.

**Diagram Placeholder**  
*(A Mermaid or ASCII diagram of the tick cycle will be added in a future revision for visual onboarding.)*

## 4. Phase Ordering Guarantees

* Phases execute **sequentially** in the order above when `deterministic_mode` is enabled.
* **No cross-phase mutation**: No phase may modify state belonging to a phase that has already executed in the same tick.
* Parallel execution (when allowed) is restricted to safe sub-phases with deterministic merge semantics.
* Regulators and the Watchdog can interrupt normal flow but must do so deterministically.

## 5. Error and Safety Flow

* Any phase detecting a critical violation immediately triggers **Fail-safe Termination** (freeze state → flush logs → atomic snapshot → close).

## 6. Integration Points

* **Experiment Layer** (19): Controls starting conditions, max ticks, and parameter sweeps.
* **Observability** (13): Full event stream and snapshots.
* **Visualization** (18): Consumes exported data only — never runs inside the tick cycle.
* **Interfaces** (17): CLI and Python API trigger the flow via `run()` / `resume()`.

## 7. Invariants (Non-Negotiable)

* The tick cycle ordering is **immutable** and must be identical across all runs in deterministic mode.
* Every state change increments the State Counter.
* Observer tools have zero influence on the internal tick flow.
* All phases must be parallel-friendly and pure where possible (see 12).
* No cross-phase mutation is permitted.

## 8. Success Criteria

* A researcher can trace any ThoughtPoint’s behavior by examining logs and snapshots and reconstruct the exact sequence of phases it experienced.
* The program flow is fully deterministic and reproducible.
* Long-running simulations (100,000+ ticks) execute without phase-order violations or hidden state.
* New developers can understand the entire mechanical heart of the TS by reading this document + the tick cycle implementation.

---

**Last Updated**: May 26, 2026  
**Version**: 0.2  
**Changes from 0.1**:
- Added **0. Initialization Phase** (Pre-Tick).
- Added deterministic intra-phase ordering rule.
- Added explicit “No cross-phase mutation” rule.
- Added Phase Purity clarification.
- Included diagram placeholder note as requested.
- Strengthened invariants and flow guarantees.

---