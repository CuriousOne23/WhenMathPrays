# API Contracts

**Purpose**: Explicit specifications for every interface. When a method is called, what must be true before (preconditions), what is guaranteed after (postconditions), and what can go wrong (errors).

## Table of Contents

- [Contract Notation](#contract-notation)
- [EditorModel API](#editormodel-api)
- [EditorController API](#editorcontroller-api)
- [PrimitivePanel API](#primitivepanel-api)
- [DraggablePoint API](#draggablepoint-api)
- [TrajectoryPanel API](#trajectorypanel-api)
- [Contract Validation](#contract-validation)
- [Contract Violations to Watch For](#contract-violations-to-watch-for)

---

## Contract Notation

Each contract specifies:
- **Purpose**: What this method does
- **Preconditions**: What must be true when called
- **Postconditions**: What is guaranteed upon return
- **Parameters**: Types and constraints
- **Returns**: Type and meaning
- **Errors**: Exceptions that can be raised
- **Performance**: Expected timing

---

## EditorModel API

### `get_event(event_idx: int) -> dict`

**Purpose**: Retrieve current state of a single event.

**Preconditions**:
- `0 <= event_idx < len(events)`

**Postconditions**:
- Returns current event dict (may differ from baseline if modified)
- Does not modify any state

**Parameters**:
- `event_idx`: Zero-based event index

**Returns**:
- `dict` with keys: `{t, v, r, f, a, S, gamma_self}`

**Errors**:
- `IndexError` if `event_idx` out of range

**Performance**: O(1), <1ms

---

### `get_all_events() -> list[dict]`

**Purpose**: Retrieve all current events.

**Preconditions**: None

**Postconditions**:
- Returns copy of events list (modifications won't affect Model)
- Does not modify any state

**Returns**:
- `list[dict]` with all events

**Errors**: None

**Performance**: O(n), <10ms for n=1000

---

### `is_modified(event_idx: int, prim: str) -> bool`

**Purpose**: Check if primitive has been modified from baseline.

**Preconditions**:
- `0 <= event_idx < len(events)`
- `prim in ['v', 'r', 'f', 'a', 'S']`

**Postconditions**:
- Returns True if current value differs from baseline
- Does not modify any state

**Parameters**:
- `event_idx`: Zero-based event index
- `prim`: Primitive name

**Returns**:
- `bool`: True if modified, False if at baseline

**Errors**:
- `IndexError` if `event_idx` out of range
- `KeyError` if `prim` invalid

**Performance**: O(1), <1ms

---

### `get_baseline_value(event_idx: int, prim: str) -> float`

**Purpose**: Get the original (pre-edit) value of a primitive.

**Preconditions**:
- `0 <= event_idx < len(events)`
- `prim in ['v', 'r', 'f', 'a', 'S']`

**Postconditions**:
- Returns baseline value
- Does not modify any state

**Parameters**:
- `event_idx`: Zero-based event index
- `prim`: Primitive name

**Returns**:
- `float`: Original value from file load or last save

**Errors**:
- `IndexError` if `event_idx` out of range
- `KeyError` if `prim` invalid

**Performance**: O(1), <1ms

---

### `update_event(event_idx: int, changes: dict) -> None`

**Purpose**: Update one or more primitives for an event.

**Preconditions**:
- `0 <= event_idx < len(events)`
- `changes` keys are subset of `['v', 'r', 'f', 'a', 'S']`
- `changes` values are valid floats for those primitives

**Postconditions**:
- `events[event_idx]` updated with changes
- Modified primitives added to `modified_events[event_idx]`
- If value equals baseline, removed from modified set

**Parameters**:
- `event_idx`: Zero-based event index
- `changes`: `dict` mapping primitive names to new values

**Returns**: None

**Errors**:
- `IndexError` if `event_idx` out of range
- `KeyError` if `changes` contains invalid primitive name
- `ValueError` if values are invalid (e.g., negative for magnitude primitives)

**Performance**: O(k) where k = len(changes), <1ms typical

**Example**:
```python
model.update_event(5, {'r': 0.85, 'f': 0.3})
# Updates event 5's r and f primitives
```

---

### `reset_event_primitive(event_idx: int, prim: str) -> float`

**Purpose**: Reset single primitive to baseline value.

**Preconditions**:
- `0 <= event_idx < len(events)`
- `prim in ['v', 'r', 'f', 'a', 'S']`

**Postconditions**:
- `events[event_idx][prim]` set to `baseline_events[event_idx][prim]`
- `prim` removed from `modified_events[event_idx]`
- Returns the baseline value

**Parameters**:
- `event_idx`: Zero-based event index
- `prim`: Primitive name

**Returns**:
- `float`: The baseline value that was restored

**Errors**:
- `IndexError` if `event_idx` out of range
- `KeyError` if `prim` invalid

**Performance**: O(1), <1ms

---

### `get_modified_events() -> set[int]`

**Purpose**: Get indices of all events with modifications.

**Preconditions**: None

**Postconditions**:
- Returns set of event indices with at least one modified primitive
- Does not modify any state

**Returns**:
- `set[int]`: Event indices with modifications

**Errors**: None

**Performance**: O(n) where n = number of events, <10ms for n=1000

---

### `set_baseline(events: list[dict]) -> None`

**Purpose**: Update baseline after save (makes current state the new ground truth).

**Preconditions**:
- `events` has same structure as current events

**Postconditions**:
- `baseline_events` updated to match `events`
- `modified_events` cleared (all events now at baseline)

**Parameters**:
- `events`: New baseline state

**Returns**: None

**Errors**:
- `ValueError` if `events` structure invalid

**Performance**: O(n), <10ms for n=1000

---

## EditorController API

### `on_primitive_value_changed(event_idx: int, prim: str, value: float) -> None`

**Purpose**: Handle user editing a primitive value.

**Preconditions**:
- Valid event_idx, prim, value (validated by caller)

**Postconditions**:
- Model updated with new value
- Primitive panel marker updated visually
- Trajectory panel updated if gamma_self affected

**Parameters**:
- `event_idx`: Event being edited
- `prim`: Primitive name
- `value`: New value

**Returns**: None

**Errors**: None (errors logged, not raised)

**Performance**: <50ms (target), currently 200-500ms ❌

**Information Flow**:
```
Controller → Model.update_event()
Controller → Model.is_modified()
Controller → PrimitivePanel.update_marker()
Controller → TrajectoryPanel.update_trajectory()
```

---

### `on_primitive_reset(event_idx: int, prim: str) -> None`

**Purpose**: Handle user resetting primitive to baseline.

**Preconditions**:
- Valid event_idx, prim

**Postconditions**:
- Model primitive reset to baseline
- Primitive panel marker updated to show baseline value
- Marker visual shows not-modified state
- Trajectory panel updated if gamma_self affected

**Parameters**:
- `event_idx`: Event being reset
- `prim`: Primitive name

**Returns**: None

**Errors**: None (errors logged, not raised)

**Performance**: <50ms (target)

**Information Flow**:
```
Controller → Model.get_baseline_value()
Controller → Model.update_event()
Controller → PrimitivePanel.update_marker()
Controller → TrajectoryPanel.update_trajectory()
```

---

### `save() -> bool`

**Purpose**: Save current state to file.

**Preconditions**: None

**Postconditions**:
- If no modifications: returns False, no action
- If modifications: writes to file, updates baseline, clears modified markers
- All panels show unmodified state

**Returns**:
- `bool`: True if saved, False if no changes

**Errors**:
- `IOError` if file write fails (caught and logged)

**Performance**: O(n), <100ms for n=1000

**Information Flow**:
```
Controller → Model.get_modified_events()
Controller → Model.get_all_events()
Controller → save_to_csv()
Controller → Model.set_baseline()
Controller → PrimitivePanel.clear_all_modified()
```

---

### `on_event_selected(event_idx: int) -> None`

**Purpose**: Handle user selecting an event.

**Preconditions**:
- Valid event_idx

**Postconditions**:
- Selection state updated in Controller
- All panels visually show selected event

**Parameters**:
- `event_idx`: Event being selected

**Returns**: None

**Errors**: None

**Performance**: <10ms (target)

**Information Flow**:
```
Controller → self.selected_event = event_idx
Controller → PrimitivePanel.set_selection()
Controller → TrajectoryPanel.set_selection()
```

---

## PrimitivePanel API

### `display_primitives() -> None`

**Purpose**: Full rebuild of all markers (rare, only on initialization).

**Preconditions**:
- Model has valid events

**Postconditions**:
- All subplots cleared and redrawn
- All DraggablePoint objects recreated
- `_markers` dict populated

**Returns**: None

**Errors**: None (errors logged)

**Performance**: O(n * m) where n=events, m=primitives, ~10ms per marker
- Current: 200-500ms for 50 markers ❌
- Target: <500ms for 50 markers (acceptable for rare operation)

**Usage**: Only call on initialization or major structural change (e.g., file reload)

---

### `update_marker(event_idx: int, prim: str, value: float, is_modified: bool) -> None`

**Purpose**: Update single marker incrementally.

**Preconditions**:
- Marker exists in `_markers[(event_idx, prim)]`
- Valid value for primitive

**Postconditions**:
- Marker position updated to reflect value
- Marker visual updated to show modified/unmodified state
- Canvas redrawn (only affected region)

**Parameters**:
- `event_idx`: Event index
- `prim`: Primitive name
- `value`: New value to display
- `is_modified`: Whether to show as modified from baseline

**Returns**: None

**Errors**: None (errors logged)

**Performance**: <50ms (target)

**Implementation**:
```python
def update_marker(self, event_idx, prim, value, is_modified):
    marker = self._markers[(event_idx, prim)]
    marker.update_position(value)
    marker.set_modified(is_modified)
    self.canvas.draw_idle()  # Efficient redraw
```

---

### `clear_all_modified() -> None`

**Purpose**: Clear modified visual state from all markers (after save).

**Preconditions**: None

**Postconditions**:
- All markers show unmodified visual state
- Positions unchanged

**Returns**: None

**Errors**: None

**Performance**: O(n * m), <100ms for 1000 events

---

### `set_selection(event_idx: int) -> None`

**Purpose**: Visually highlight selected event.

**Preconditions**:
- Valid event_idx

**Postconditions**:
- Previous selection unhighlighted
- New selection highlighted

**Returns**: None

**Errors**: None

**Performance**: <10ms (target)

---

## DraggablePoint API

### `update_position(value: float) -> None`

**Purpose**: Move marker to new position on plot.

**Preconditions**:
- Valid value for this primitive's subplot

**Postconditions**:
- Marker moved to (event_idx, value) in data coordinates
- Artist updated

**Parameters**:
- `value`: New y-coordinate value

**Returns**: None

**Errors**: None

**Performance**: <1ms

---

### `set_modified(is_modified: bool) -> None`

**Purpose**: Update visual to show modified/unmodified state.

**Preconditions**: None

**Postconditions**:
- Marker color/style reflects modification state
- Artist updated

**Parameters**:
- `is_modified`: True for modified style, False for baseline style

**Returns**: None

**Errors**: None

**Performance**: <1ms

---

### `reset_double_click_state() -> None`

**Purpose**: Reset internal double-click detection state machine.

**Preconditions**: None

**Postconditions**:
- `_click_count` reset to 0
- State machine back to idle

**Returns**: None

**Errors**: None

**Performance**: <1ms

**Usage**: Called after successful reset to prevent triple-click triggering another reset

---

## TrajectoryPanel API

### `update_trajectory() -> None`

**Purpose**: Replot gamma_self trajectory with current Model data.

**Preconditions**:
- Model has valid events with gamma_self values

**Postconditions**:
- Trajectory line updated
- Gauge updated to show current position
- Canvas redrawn

**Returns**: None

**Errors**: None (errors logged)

**Performance**: O(n), <50ms for n=1000 (target)

---

### `set_selection(event_idx: int) -> None`

**Purpose**: Highlight selected event on trajectory.

**Preconditions**:
- Valid event_idx

**Postconditions**:
- Selection marker updated to event's gamma_self position

**Returns**: None

**Errors**: None

**Performance**: <10ms (target)

---

## Contract Validation

### How to Verify Contracts

1. **Preconditions**: Add assertions at method entry
```python
def update_marker(self, event_idx, prim, value, is_modified):
    assert 0 <= event_idx < len(self.model.events)
    assert prim in ['v', 'r', 'f', 'a', 'S']
    assert isinstance(value, (int, float))
    assert isinstance(is_modified, bool)
    # ... implementation ...
```

2. **Postconditions**: Add assertions before return
```python
def update_event(self, event_idx, changes):
    # ... implementation ...
    assert self.events[event_idx][prim] == changes[prim]
    if changes[prim] != self.baseline_events[event_idx][prim]:
        assert prim in self.modified_events[event_idx]
```

3. **Performance**: Add timing instrumentation
```python
import time
def update_marker(self, ...):
    start = time.perf_counter()
    # ... implementation ...
    elapsed = time.perf_counter() - start
    if elapsed > 0.050:  # 50ms target
        logger.warning(f"update_marker took {elapsed*1000:.1f}ms (target <50ms)")
```

---

## Contract Violations to Watch For

### Silent Failures
```python
# WRONG: Silently ignoring errors
def update_marker(self, ...):
    try:
        marker = self._markers[(event_idx, prim)]
    except KeyError:
        return  # ❌ Violates contract - should error
```

```python
# RIGHT: Fail loudly
def update_marker(self, ...):
    marker = self._markers[(event_idx, prim)]  # ✅ Raises KeyError
```

---

### Side Effects in Queries
```python
# WRONG: Query modifies state
def get_event(self, idx):
    self._last_accessed = idx  # ❌ Side effect
    return self.events[idx]
```

```python
# RIGHT: Query is pure
def get_event(self, idx):
    return self.events[idx]  # ✅ No side effects
```

---

### Performance Regressions
```python
# WRONG: O(n) when contract specifies O(1)
def is_modified(self, idx, prim):
    # ❌ Linear search violates O(1) contract
    for i, modified_set in enumerate(self.modified_events):
        if i == idx:
            return prim in modified_set
```

```python
# RIGHT: O(1) as contracted
def is_modified(self, idx, prim):
    return prim in self.modified_events[idx]  # ✅ O(1)
```

---

**Last Updated**: 2025-12-06  
**Status**: Contracts defined for target architecture (not yet implemented)
