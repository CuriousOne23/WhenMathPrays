# 10 Interaction Model

## 1. Purpose

This document defines how the major components of the **Thought Simulator (TS)** interact with each other. It specifies the interfaces, data flow, communication patterns, and responsibilities between layers to ensure a clean, deterministic, observable, and maintainable architecture.

## 2. Core Interaction Principles

- The **Thought Simulator (TS) Core** is the single source of truth for all simulation state and behavior.
- All interactions are deterministic and reproducible.
- The optional Relational Manifold is strictly read-only and has no influence on TS behavior.
- The Observer is external and non-mechanical — its signals are advisory only.
- Communication between components is explicit, observable, and logged.
- Multi-TP concurrency is supported natively with clear synchronization rules.
- Within each tick, ThoughtPoints are processed in a deterministic order (e.g., sorted by `tp_id`).

## 3. Major Components and Their Roles

- **TS Core** — Owns the simulation loop, scheduling, state machine, and determinism.
- **Basins** — Process ThoughtPoints, apply tags, reduce entropy, and manage local state.
- **Regulators** — Monitor system state and intervene when needed.
- **Observer** — External entity that evaluates coherence and may provide advisory signals.
- **Relational Manifold** — Optional visualization and interpretive layer.
- **IO Layer** — Handles input and output.
- **Experiment Layer** — Orchestrates experiments and analysis.

## 4. Primary Interaction Patterns

### 4.1 TS Core ↔ Basins
- TS Core routes ThoughtPoints to appropriate basins based on deterministic routing rules.
- Basins notify the TS Core synchronously (within the same tick) when a TP meets exit conditions.
- TS Core handles ejection and routing to the next basin.

### 4.2 TS Core ↔ Regulators
- After main basin processing, the TS Core calls active regulators in a deterministic priority order.
- Regulators may tag TPs, modify entropy, force routing, or recommend splitting/merging.
- All regulator actions are logged and increment the affected TP’s `tagged_state_counter`.

### 4.3 TS Core ↔ Observer
- At defined points (typically after OB processing), the TS Core may request Observer evaluation.
- The Observer returns advisory coherence signals (meaning, beauty, harmony, value, etc.).
- These signals are treated as external inputs. The TS Core interprets them through deterministic rules — they do not modify TS state directly.

### 4.4 TS Core ↔ Relational Manifold
- The Manifold receives complete TS state snapshots **after** each tick completes (read-only).
- It projects the state (including multiple TPs) into geometric visualizations.
- No feedback from the Manifold is allowed back into the TS.

### 4.5 Tick Boundaries
All major interactions (basin processing, regulator evaluation, Observer signals, splitting/merging, and snapshots) occur within well-defined tick boundaries. Splitting and merging operations are atomic with respect to each tick.

## 5. Key Interfaces

- **Basin Interface**: `enter(tp)`, `process(tp)`, `can_exit(tp)`, `get_tags(tp)`
- **Regulator Interface**: `evaluate(system_state)` → list of deterministic actions
- **Observer Interface**: `evaluate(tp, context)` → advisory coherence signal
- **Manifold Interface**: `update_snapshot(ts_snapshot)`
- **Snapshot Interface**: `save()`, `load()`, `compare()`

## 6. Data Flow Summary (Per Tick)

1. Configuration + Initial TPs → TS Core
2. TS Core schedules TPs (deterministic order) → Basins
3. Basins process & tag → TS Core
4. Regulators evaluate → TS Core
5. Observer may evaluate (optional) → TS Core
6. TS Core performs splitting/merging and final updates
7. TS Core creates snapshot and logs
8. Optional: Snapshot sent to Manifold for visualization
9. Tick completes

## 7. Observability Requirements

- All component interactions must be logged with timestamps, TP IDs, step index, and state counter.
- Major events (entry, exit, tagging, splitting, merging, regulator action, observer signal) must be traceable.
- The system must support step-by-step replay using saved snapshots.

## 8. Invariants

- The TS Core is the sole owner of simulation state.
- No component outside the TS Core can modify TP or basin state directly.
- The Manifold is strictly read-only.
- Observer signals are advisory only.
- All interactions must preserve determinism.

## 9. Success Criteria

- Clear, well-defined interfaces between all major components.
- Multi-TP interactions are deterministic, observable, and debuggable.
- The system supports clean extension of new components.
- Data flow is understandable by new developers and implementers.

---

**Last Updated**: May 25, 2026  
**Version**: 0.3 (Incorporated CoPilot’s refinements)

---