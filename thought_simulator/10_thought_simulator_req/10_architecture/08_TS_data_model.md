# 08 TS Data Model

## 1. Purpose

This document defines the core data structures and object models used within the **Thought Simulator (TS)**.

It specifies the internal representation of ThoughtPoints, Basins, tags, state, and supporting structures in a way that supports determinism, observability, multi-TP concurrency, and full lifecycle traceability.

## 2. Core Design Principles

- All data structures must be fully serializable for snapshots and reproducibility.
- Every ThoughtPoint must carry complete lifecycle metadata.
- Structures must support efficient lookup, membership testing, and logging.
- No geometric data is stored in the TS data model — geometry belongs exclusively to the optional Manifold layer.

## 3. Primary Data Structures

### 3.1 ThoughtPoint (TP)

The fundamental unit of thought-in-process.

```python
class ThoughtPoint:
    tp_id: str                          # Unique UUID
    ts_step_index: int                  # Global simulation timestep when created/updated
    tagged_state_counter: int           # Increments on every modification/tagging
    current_basin_id: str | None
    embedding: Vector                   # Current embedding vector
    entropy: float                      # Unified entropy value (H_total)
    normalized_entropy: float           # H_% (0–100)
    energy: float
    tags: dict[str, Any]                # All attached metadata/tags
    provenance: list[ProvenanceEntry]   # History of modifications
    creation_step: int
    last_updated_step: int
```

### 3.2 Basin

Base class for all basin types.

```python
class Basin:
    basin_id: str
    basin_type: str                     # "OB", "RB", "Inquiry", "Feeling", etc.
    lifecycle_state: str                # NEW, RUNNING, DONE
    max_capacity: int
    current_tps: list[str]              # List of TP IDs currently inside
    parameters: dict                    # Type-specific configuration
    entry_conditions: list[Condition]
    exit_conditions: list[Condition]
    tags_applied: dict[str, int]        # Statistics of tags applied
```

### 3.3 ProvenanceEntry

```python
class ProvenanceEntry:
    step_index: int
    state_counter: int
    basin_id: str
    action: str                         # "tagged", "split", "merged", "ejected", etc.
    timestamp: datetime
    details: dict
```

## 4. Supporting Structures

- **TS State Snapshot**: Full system state at a given timestep (all TPs, all basins, global counters).
- **Tag Registry**: Centralized definition of allowed tags and their semantics.
- **Routing Table**: Deterministic mapping rules for TP transitions between basins.
- **Event Log**: Chronological record of all significant events (entry, exit, tagging, splitting, merging, etc.).

## 5. Multi-TP Considerations

- Multiple ThoughtPoints may reside in the same basin simultaneously.
- Each TP maintains independent state (Step Index + Tagged State Counter).
- Basins must handle concurrent access safely with deterministic ordering where required.
- Data structures must support efficient lookup by TP ID, basin ID, and step index.

## 6. Observability Requirements

- Every data structure must support full serialization to JSON.
- Snapshots must be versioned and comparable.
- All changes to ThoughtPoints and Basins must be logged with both:
  - `ts_step_index`
  - `tagged_state_counter`

This ensures full lifecycle traceability.

## 7. Invariants

- The TS data model contains no geometric information.
- All state is fully deterministic and reproducible.
- Every ThoughtPoint’s lifecycle is completely traceable.
- Data structures are designed for efficient debugging and analysis.

## 8. Success Criteria

- The data model supports arbitrary numbers of concurrent ThoughtPoints without ambiguity.
- Full lifecycle reconstruction is possible from logs and snapshots.
- The model is clean, extensible, and implementable in multiple languages.
- It enables efficient debugging, replay, and analysis.

---

**Last Updated**: May 25, 2026  
**Version**: 0.2 (Cleaned & Aligned with 04–07)

---

