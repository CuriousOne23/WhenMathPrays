# 09 Data Structures

## 1. Purpose

This document provides the detailed, implementation-ready data structures for the **Thought Simulator (TS)**.

It builds upon the high-level data model defined in Document 08, specifying concrete structures, relationships, and usage patterns needed for a robust, deterministic, and observable implementation.

## 2. Design Goals

- High performance for multi-TP scenarios.
- Full determinism and reproducibility.
- Excellent observability and debuggability.
- Clear separation between core TS data and optional visualization data.
- Easy serialization (JSON, binary snapshots, etc.).

## 3. Core Data Structures

### 3.1 ThoughtPoint

The fundamental unit of thought-in-process.

```python
class ThoughtPoint:
    tp_id: str                          # Unique UUID
    ts_step_index: int                  # Global simulation timestep
    tagged_state_counter: int           # Increments on every change
    current_basin_id: str | None
    embedding: np.ndarray               # Current embedding vector
    entropy: float                      # H_total
    normalized_entropy: float           # H_% (0.0 - 100.0)
    energy: float
    tags: dict[str, Any]                # All metadata/tags
    provenance: list[ProvenanceEntry]   # History chain
    creation_step: int
    last_updated_step: int
    status: str                         # "ACTIVE", "COMPLETED", "STALLED", etc.
```

### 3.2 ProvenanceEntry

```python
class ProvenanceEntry:
    step_index: int
    state_counter: int
    basin_id: str
    action: str                         # "entered", "tagged", "ejected", "split", "merged", etc.
    timestamp: datetime
    details: dict[str, Any]
```

### 3.3 Basin

```python
class Basin:
    basin_id: str
    basin_type: str                     # "OB", "RB", "Inquiry", "Feeling", "Done"
    lifecycle_state: str                # "NEW", "RUNNING", "DONE"
    max_capacity: int
    current_tps: list[str]              # List of TP IDs currently inside
    parameters: dict[str, Any]          # Type-specific config
    entry_conditions: list[dict]
    exit_conditions: list[dict]
    tags_applied: dict[str, int]        # Tag statistics
    metadata: dict[str, Any]
```

### 3.4 TS State Snapshot

```python
class TSSnapshot:
    step_index: int
    timestamp: datetime
    thought_points: dict[str, ThoughtPoint]   # tp_id → TP
    basins: dict[str, Basin]                  # basin_id → Basin
    global_metrics: dict[str, float]          # entropy, active_tps, etc.
    event_log: list[dict]                     # Recent events
```

## 4. Supporting Data Structures

- **TagRegistry** — Centralized catalog of valid tags and their schemas.
- **RoutingTable** — Deterministic rules for moving TPs between basins.
- **EventLog** — Chronological list of all system events with full context.
- **SimulationConfig** — All runtime parameters (concurrency limits, scheduling policy, etc.).
- **Condition** — Reusable rule definition for entry/exit conditions.

## 5. Multi-TP Design Considerations

- All structures must efficiently handle hundreds or thousands of concurrent ThoughtPoints.
- Lookups by `tp_id`, `basin_id`, and `ts_step_index` must be fast (use dictionaries and indexes).
- Memory management for long provenance chains must be considered.
- Snapshots must be efficient enough for frequent saving during long runs.

## 6. Observability & Debugging Features

- Every major structure must support `to_dict()` and `from_dict()` for serialization.
- Full snapshot comparison utilities should be available.
- Debug-friendly string representations (`__repr__`) for TPs and Basins.
- Support for filtering and querying the event log by step index or state counter.

## 7. Invariants

- No geometric data exists in any TS data structure.
- All identifiers (`tp_id`, `basin_id`) are globally unique.
- State changes are only allowed through defined TS state machine transitions.
- Every modification to a ThoughtPoint increments its `tagged_state_counter`.

## 8. Success Criteria

- The data structures support efficient multi-TP simulation.
- Full system state can be saved, loaded, and compared reproducibly.
- Debugging and analysis tools can easily trace any TP’s complete lifecycle.
- The model is clean enough for multiple developers or AI agents to implement consistently.

---

**Last Updated**: May 25, 2026  
**Version**: 0.2 (Cleaned & Aligned with 08)

---