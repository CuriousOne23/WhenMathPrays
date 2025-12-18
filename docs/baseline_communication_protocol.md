# Baseline Communication Protocol - Architecture Documentation

## Table of Contents

- [Problem Statement](#problem-statement)
- [The Critical Issue](#the-critical-issue)
- [Solution: Baseline Communication Protocol](#solution-baseline-communication-protocol)
  - [Architecture Components](#architecture-components)
  - [Communication Flow](#communication-flow)
  - [Gamma_self Baseline Tracking](#gamma_self-baseline-tracking)
  - [Debug Logging Usage](#debug-logging-usage)
  - [Example Log Output](#example-log-output)
- [Key Design Principles](#key-design-principles)
- [Implementation Checklist](#implementation-checklist)
- [Future Enhancements](#future-enhancements)

## Problem Statement

The interactive editor has TWO fundamentally different coordinate spaces:

### 1. Primitive Space (Time-Indexed)
- **Indexing**: By TIME (float)
- **Keys**: `(time, primitive_name)` tuples
- **Property**: **Insertion-proof** - time values don't change when events are inserted
- **Example**: `(2.5, 'v')` always refers to the 'v' primitive at time=2.5

### 2. Gamma_self Space (Index-Based)
- **Indexing**: By TRAJECTORY INDEX (int)  
- **Keys**: Sequential integers `0, 1, 2, ...`
- **Property**: **NOT insertion-proof** - indices shift when events are inserted
- **Example**: Index 5 refers to the 6th point in the trajectory (gamma_self[5])

## The Critical Issue

When a primitive event is inserted:
1. Primitive space adds a new TIME point (e.g., t=2.5 between t=2 and t=3)
2. Gamma_self trajectory is **recomputed** with a new point inserted in the middle
3. All gamma_self indices AFTER the insertion point shift by +1
4. BUT gamma_self markers/labels were still using OLD indices!

**Example**:
```
Before insertion at t=2.5:
  Primitives: t=0, t=1, t=2, t=3, t=4
  Gamma_self: idx=0, idx=1, idx=2, idx=3, idx=4
  Marker at t=3 -> gamma_self[3]

After insertion at t=2.5:
  Primitives: t=0, t=1, t=2, t=2.5, t=3, t=4  
  Gamma_self: idx=0, idx=1, idx=2, idx=3, idx=4, idx=5
  Marker at t=3 -> gamma_self[4] (NOT 3!)
```

## Solution: Baseline Communication Protocol

### Architecture Components

#### 1. BaselineDebugLog (baseline_protocol.py)
- Centralized logging system for all baseline communications
- Can be enabled/disabled via `BaselineDebugLog.enable()/disable()`
- Logs timestamps, events, perspectives, and context
- Exportable to JSON for analysis

#### 2. BaselineTracker (baseline_protocol.py)
- Tracks baselines for a SINGLE space (primitive OR gamma_self)
- Stores: `key -> (value, baseline_type)` mappings
- Methods: `set_baseline()`, `get_baseline()`, `shift_key()`, `remove_baseline()`

#### 3. BaselineCommunicator (baseline_protocol.py)
- Central hub coordinating between primitive and gamma_self trackers
- One instance per perspective (M1 and M2)
- Handles communication events:
  - `notify_primitive_insert_shift()` - Ctrl+Shift+Click insertion
  - `notify_primitive_insert_fractional()` - Fractional time insertion
  - `notify_gamma_reindex()` - Gamma trajectory recomputed
  - `sync_primitive_baseline_to_view()` - Primitive baseline -> view
  - `sync_gamma_baseline_to_view()` - Gamma baseline -> view

#### 4. Baseline Types (BaselineType enum)
- **CSV_BASELINE**: Original values from loaded CSV (never changes)
- **INSERTION_BASELINE**: Created when Ctrl+Shift+Click inserts event (becomes new visual baseline)
- **FRACTIONAL_BASELINE**: Created when fractional time insertion occurs (neutral 0.0 values)

### Communication Flow

#### Ctrl+Shift+Click Insertion (with time shift):

```
1. User: Ctrl+Shift+Click at t=2.5
   └─> Controller._insert_event_before()
       
2. Controller: baseline_comm.notify_primitive_insert_shift(2.5, [(3→3.5), (4→4.5)])
   └─> BaselineDebugLog: [M1] primitive_insert_shift | insert_time=2.5 | shifts=[(3,3.5), (4,4.5)]
   
3. Controller: Shifts primitive baselines in reverse order
   └─> baseline_by_time: (3, 'v') → (3.5, 'v'), (4, 'v') → (4.5, 'v')
   
4. Controller: Adds INSERTION_BASELINE for new event at t=2.5
   └─> baseline_by_time: (2.5, 'v') = copied_from_previous_event
   
5. Controller: _sync_baseline_to_view()
   └─> baseline_comm.sync_primitive_baseline_to_view({0:0, 1:1, 2:2, 2.5:3, 3.5:4, 4.5:5})
   └─> PrimitivePanel.set_baseline_values({(0,'v'):..., (1,'v'):..., ...})
   
6. Controller: _recompute_trajectory_immediate()
   └─> Gamma_self trajectory recomputed with new point at index 3
   
7. TrajectoryPanel: Needs to reindex gamma baselines
   └─> gamma_baseline_m1: {3→4, 4→5, 5→6, ...}
```

#### Fractional Time Insertion (no time shift):

```
1. User: Inserts event at fractional time t=2.5
   └─> Controller.insert_event_at_time(2.5)
       
2. Controller: baseline_comm.notify_primitive_insert_fractional(2.5)
   └─> BaselineDebugLog: [M1] primitive_insert_fractional | insert_time=2.5 | baseline_type=fractional_baseline
   
3. Controller: Adds FRACTIONAL_BASELINE (zeros) at t=2.5
   └─> baseline_by_time: (2.5, 'v') = 0.0, (2.5, 'r') = 0.0, ...
   
4. Controller: _sync_baseline_to_view()
   └─> PrimitivePanel baseline updated
   
5. Controller: _recompute_trajectory_immediate()
   └─> Gamma_self trajectory gets new interpolated point
   └─> TrajectoryPanel reindex needed (indices shift after insertion point)
```

### Gamma_self Baseline Tracking

TrajectoryPanelPyQtGraph maintains SEPARATE baseline dictionaries:

```python
# CSV baselines (original from file)
self.gamma_baseline_m1 = {trajectory_idx: complex_value}
self.gamma_baseline_m2 = {trajectory_idx: complex_value}

# Insertion baselines (created by Ctrl+Shift+Click)
self.gamma_insertion_baseline_m1 = {trajectory_idx: complex_value}
self.gamma_insertion_baseline_m2 = {trajectory_idx: complex_value}
```

**Precedence**: Insertion baselines take precedence over CSV baselines (checked first).

**Methods**:
- `set_gamma_baseline(idx, value, "csv"|"insertion")` - Set baseline
- `get_gamma_baseline(idx)` -> `(value, type)` - Get baseline (insertion first, then CSV)
- `reindex_gamma_baselines(old→new mapping)` - Called after trajectory recomputation

### Debug Logging Usage

```python
# In editor code or console:
controller.enable_baseline_protocol_logging()

# Perform operations (insert, edit, undo, etc.)

# View log in console
controller.dump_baseline_protocol_log()

# Save to auto-generated timestamped JSON file (logs/baseline/baseline_protocol_YYYYMMDD_HHMMSS.json)
controller.dump_baseline_protocol_log("auto")

# Save to custom JSON file (machine-readable, for analysis)
controller.dump_baseline_protocol_log("logs/baseline/my_debug.json")

# Save to custom text file (human-readable, for quick scanning)
controller.dump_baseline_protocol_log("logs/baseline/my_debug.log")

# Disable when done
controller.disable_baseline_protocol_logging()
```

**Log File Location**: `logs/baseline/baseline_protocol_YYYYMMDD_HHMMSS.json` (default)

**Log Formats**: 
- **JSON** (default): Structured data for programmatic analysis
- **Text**: Human-readable with comprehensive header explaining:
- What the log tracks
- Why it exists
- Who calls it
- How to enable/disable
- Event types documentation
- How to read the entries

See [logs/baseline/README.md](../logs/baseline/README.md) for details.

### AI-Assisted Debugging Tools

The baseline protocol includes simple validation functions that AIs can use for rapid bug assessment:

```python
# Validate consistency between coordinate spaces
validation = controller.validate_baseline_consistency()
# Returns: {"is_consistent": True/False, "warnings": [...], "errors": [...]}

# Get current time->index mappings snapshot  
mappings = controller.snapshot_coordinate_mappings()
# Returns: {"time_to_index": {2.5: 3, 3.5: 4, ...}, "index_to_time": {3: 2.5, 4: 3.5, ...}}

# Check marker position validity
marker_check = controller.baseline_comm_m1.check_marker_positions(marker_positions, events)
# Returns: {"valid_markers": 5, "invalid_markers": 0, "issues": []}
```

These functions provide **immediate state validation** without requiring log analysis, making them perfect for AI debugging workflows.

## AI-Assisted Debugging Enhancements

### Overview

Three simple, low-overhead validation functions have been added to assist AI-assisted debugging of time/index synchronization issues. These functions provide immediate diagnostic capabilities without the complexity of a real-time visualizer.

### Why Implemented

The existing baseline protocol logging is excellent for detailed event tracing, but AIs sometimes need **immediate validation** of current state without analyzing logs. These functions provide:

- **Instant consistency checks** for common bugs
- **Current state snapshots** for relationship analysis  
- **Validation of marker references** after insertions/deletions
- **Structured output** perfect for programmatic analysis

### Implementation Location

**File**: `tools/editor/baseline_protocol.py`
- `BaselineDebugLog.validate_consistency()`
- `BaselineDebugLog.snapshot_mappings()`
- `BaselineDebugLog.check_marker_consistency()`

**File**: `tools/editor/controller.py`  
- `EditorController.validate_baseline_consistency()`
- `EditorController.snapshot_coordinate_mappings()`

### How to Use

#### 1. Consistency Validation

```python
# From controller (recommended)
validation = controller.validate_baseline_consistency()

# Direct call
from tools.editor.baseline_protocol import BaselineDebugLog
validation = BaselineDebugLog.validate_consistency('M1', events, gamma_length)

# Result format
{
    "perspective": "M1",
    "event_count": 5,
    "gamma_length": 5, 
    "warnings": [],
    "errors": [],
    "is_consistent": True,
    "marker_check": {  # If markers present
        "valid_markers": 3,
        "invalid_markers": 0,
        "issues": []
    }
}
```

**Validates**:
- Event count matches gamma trajectory length
- Event times are monotonically increasing
- Time values within reasonable bounds (0-1000)
- Marker positions reference valid time/primitive combinations

#### 2. Coordinate Mapping Snapshot

```python
# Get current time<->index relationships
mappings = controller.snapshot_coordinate_mappings()

# Direct call  
mappings = BaselineDebugLog.snapshot_mappings('M1', events)

# Result format
{
    "perspective": "M1",
    "timestamp": "2025-12-18T10:30:00",
    "time_to_index": {1.0: 0, 2.5: 1, 3.0: 2},
    "index_to_time": {0: 1.0, 1: 2.5, 2: 3.0},
    "event_count": 3
}
```

**Use Case**: AIs can instantly see current mappings without reconstructing from logs.

#### 3. Marker Position Validation

```python
# Check marker consistency
marker_check = controller.baseline_comm_m1.check_marker_positions(marker_positions, events)

# Result format
{
    "perspective": "M1", 
    "marker_count": 3,
    "valid_markers": 3,
    "invalid_markers": 0,
    "issues": []
}
```

**Validates**: All marker keys `(time, primitive)` exist in current events.

### Integration with Existing Logging

These functions integrate with the baseline protocol logging system:

- Results are logged when protocol logging is enabled
- Use existing event types (`BASELINE_SYNC_PRIMITIVE`, `BASELINE_SYNC_GAMMA`, etc.)
- Add context like `validation_result` or `marker_issues` to log entries
- No additional log files or formats needed

### Performance Characteristics

- **Overhead**: Minimal - single passes through data structures
- **Memory**: No additional state storage
- **Execution**: Only when called, zero impact on normal operation
- **Logging**: Optional integration with existing debug logging

### AI Debugging Workflow

```python
# 1. Enable logging if needed
controller.enable_baseline_protocol_logging()

# 2. Reproduce the issue
# ... perform operations that cause time/index bug ...

# 3. Quick validation check
validation = controller.validate_baseline_consistency()
if not validation["is_consistent"]:
    print("Found consistency issues:", validation["errors"])

# 4. Get current state snapshot
mappings = controller.snapshot_coordinate_mappings()
print("Current relationships:", mappings["time_to_index"])

# 5. Dump detailed logs if needed
controller.dump_baseline_protocol_log("auto")
```

### Error Detection Examples

**Count Mismatch**:
```json
{
  "warnings": [{
    "type": "count_mismatch",
    "message": "Event count (5) != gamma length (6)",
    "severity": "high"
  }]
}
```

**Invalid Marker Reference**:
```json
{
  "issues": [{
    "type": "invalid_marker_reference", 
    "marker": [2.5, "v"],
    "message": "Marker references non-existent time/primitive"
  }]
}
```

**Time Order Violation**:
```json
{
  "errors": [{
    "type": "time_order_violation",
    "message": "Event 3 time 2.0 <= previous 2.5",
    "severity": "critical"
  }]
}
```

These enhancements provide AIs with **immediate diagnostic capabilities** while maintaining the simplicity and robustness of the existing baseline communication protocol.

### Example Log Output

```
[10:23:45.123] [M1] primitive_insert_shift | insert_time=2.5 | shifts_count=3 | shifted_times=[(3.0,3.5), (4.0,4.5), (5.0,5.5)]
[10:23:45.145] [M1] baseline_sync_primitive | entries_count=6
[10:23:45.167] [M1] gamma_reindex | mappings_count=3 | mapping={3:4, 4:5, 5:6}
[10:23:45.189] [M1] baseline_sync_gamma | index_count=7
```

## Key Design Principles

1. **Single Source of Truth**: Controller owns `baseline_by_time_m1/m2`, views receive synchronized copies
2. **Time-based Primitive Tracking**: Insertion-proof, never needs reindexing
3. **Index-based Gamma Tracking**: Must be reindexed after trajectory changes
4. **Explicit Communication**: Every baseline change goes through protocol communicator
5. **Separate Baseline Types**: CSV vs Insertion vs Fractional tracked distinctly
6. **Debug Visibility**: All communications logged when enabled

## Implementation Checklist

- [x] Create baseline_protocol.py with logging and communicator classes
- [x] Add BaselineCommunicator instances to EditorController (M1 and M2)
- [x] Integrate protocol logging into _insert_event_before()
- [x] Integrate protocol logging into _update_baseline_after_insert()
- [x] Update _sync_baseline_to_view() to use protocol
- [x] Add gamma_self baseline tracking to TrajectoryPanelPyQtGraph
- [x] Add reindex_gamma_baselines() method to trajectory panel
- [ ] Call reindex_gamma_baselines() after trajectory recomputation
- [ ] Add gamma baseline indicators to trajectory display
- [ ] Test fractional insertion with gamma reindexing
- [ ] Test Ctrl+Shift+Click insertion with gamma reindexing
- [ ] Test undo operations with protocol logging
- [ ] Document edge cases and failure modes

## Future Enhancements

1. **Visual Gamma Baselines**: Show baseline markers on gamma_self trajectory (green triangles)
2. **Baseline Diff View**: Highlight differences between CSV and current state
3. **Automatic Reindexing**: Detect trajectory changes and auto-reindex
4. **Protocol Validation**: Assert baseline consistency at checkpoints
5. **Performance Metrics**: Log timing for sync operations
