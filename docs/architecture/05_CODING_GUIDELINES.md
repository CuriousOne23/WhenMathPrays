# Coding Guidelines

**Purpose**: Concrete do's and don'ts for writing maintainable code in this codebase. These guidelines emerged from real bugs and refactorings.

**Status**: Living document - updated when new lessons are learned.

**Last Updated**: December 2025 (post = None elimination)

---

## Table of Contents

1. [Parameter Design](#parameter-design)
2. [State Management](#state-management)
3. [Debugging & Observability](#debugging--observability)
4. [Type Annotations](#type-annotations)
5. [Error Handling](#error-handling)

---

## Parameter Design

### ❌ DON'T: Use `= None` for Required Parameters

**Problem**: Lets you write wrong code that compiles. Silent failures that appear as runtime bugs.

```python
# BAD - event_time is required but caller can forget it
def set_active_primitive(self, prim: str, value: float, time: float = None):
    if time is not None:
        label = f"Editing: {prim} @ t={time}"
    else:
        label = f"Editing: {prim}"  # ❌ Time missing! User won't know which event
```

**Consequence**: The time label bug (v2.1.4) - users couldn't see which event they were editing.

### ✅ DO: Make Required Parameters Explicit

```python
# GOOD - compiler enforces correctness
def set_active_primitive(self, prim: str, value: float, time: float):
    label = f"Editing: {prim} @ t={time}"  # ✅ Always correct
```

**Result**: Wrong calls fail at call time: `TypeError: missing required argument 'time'`

### ✅ DO: Use Explicit Alternatives for Optional Behavior

**Option A: Split methods**
```python
def set_active_primitive_with_time(self, prim: str, value: float, time: float):
    """Standard case - show time."""
    label = f"Editing: {prim} @ t={time}"

def set_active_primitive_no_time(self, prim: str, value: float):
    """Rare edge case - initialization before events exist."""
    label = f"Editing: {prim}"
```

**Option B: Class method for defaults**
```python
@classmethod
def default_config_path(cls) -> Path:
    return Path.home() / '.whenmathprays' / 'editor_config.json'

# Usage - explicit at call site
config = EditorConfig(EditorConfig.default_config_path())
```

**Option C: Sentinel value (when semantics matter)**
```python
def calculate_num_events(duration: float, time_unit: str, num_events: int = -1) -> int:
    """
    Args:
        num_events: Number of events, or -1 to auto-calculate
    """
    if num_events > 0:
        return num_events
    # Auto-calculate based on time_unit
```

**Guideline**: If `None` means "I don't know" or "figure it out", that's **hidden logic**. Make it explicit.

---

## State Management

### ❌ DON'T: Multiple Owners

**Problem**: Creates race conditions and ambiguous authority.

```python
# BAD - who's authoritative?
class InteractiveEditor:
    def on_perspective_switch(self):
        self.spinbox.set_active_primitive(prim, value, time)  # ❌ Editor controls widget
        
class Controller:
    def restore_active_primitive(self):
        self._spinbox_widget.set_active_primitive(prim, value, time)  # ❌ Controller also controls widget
```

**Consequence**: The spinbox time label race condition - editor overwrites controller's correct state.

### ✅ DO: Single Owner Pattern

```python
# GOOD - one owner only
class Controller:
    def initialize_spinbox_widget(self, widget):
        """Controller owns the spinbox."""
        self._spinbox_widget = widget  # Private!
        widget.value_changed.connect(self.on_spinbox_value_changed)
    
    def update_spinbox_value(self, value: float):
        """Only entry point for spinbox updates."""
        if self._spinbox_widget.is_editing():
            self._spinbox_widget.update_value(value)

# Other components go through controller
class InteractiveEditor:
    def on_perspective_switch(self):
        # ✅ No direct spinbox access - controller handles it
        self.controller.restore_state_for_perspective(perspective)
```

**Guideline**: Widget with private reference (`_spinbox_widget`) = owned. Public methods = API.

### ✅ DO: Explicit State Tracking

```python
# GOOD - explicit per-perspective state
class Controller:
    def __init__(self):
        # Explicit state dictionaries
        self.active_primitive_state_m1 = {
            'primitive': None,
            'event_id': None,
            'event_time': None
        }
        self.active_primitive_state_m2 = {
            'primitive': None,
            'event_id': None,
            'event_time': None
        }
    
    def _restore_spinbox_state_for_perspective(self, perspective: str):
        """Single source of truth for state restoration."""
        state = self.active_primitive_state_m1 if perspective == "M1" else self.active_primitive_state_m2
        if state['primitive'] is not None:
            self._spinbox_widget.set_active_primitive(
                state['primitive'],
                self._get_current_value(state),
                state['event_time']  # ✅ Always preserved
            )
```

**Guideline**: If you need to restore state later, **store it explicitly**. Don't try to reconstruct from widget state.

---

## Debugging & Observability

### ❌ DON'T: Log at High Level When Low Level is Wrong

**Problem**: Logs show expected behavior, but widget shows wrong state.

```python
# BAD - logging at controller level
def restore_state(self):
    _logger.debug(f"Restoring state: {state}")
    self._update_widget(state)  # ❌ Widget gets wrong value, but logs look correct
```

### ✅ DO: Instrument the Victim

**Principle**: When logs disagree with reality, log at the **lowest level** (the widget itself).

```python
# GOOD - logging at widget level
class PrimitiveSpinboxEditor:
    def set_active_primitive(self, prim: str, value: float, time: float):
        _logger.debug(f"[SPINBOX] set_active_primitive({prim}, {value}, {time})")
        label = f"Editing: {prim} @ t={time}"
        self.active_label.setText(label)
        _logger.debug(f"[SPINBOX] Label text set to: {label}")
        _logger.debug(f"[SPINBOX] Label text now shows: {self.active_label.text()}")
```

**Result**: Discovered that controller's call was correct, but interactive_editor overwrote it 50ms later.

**Guideline**: When UI shows X but logs show Y, add logging at the **widget level**. The race condition is between log and UI update.

### ✅ DO: Use StateViewer for Operation Tracking

```python
# GOOD - automatic operation recording
from tools.editor.state_viewer import StateViewer

def insert_event(self, event_idx: int, time: float):
    StateViewer.record(
        operation='insert_event',
        entity=(event_idx, self.perspective, time),
        changes={'action': 'insert', 'count': 1}
    )
    # ... perform operation
```

**Benefit**: Export complete operation history with Ctrl+Shift+L. See exactly what happened and when.

---

## Type Annotations

### ✅ DO: Annotate Function Signatures

```python
# GOOD - clear contract
def set_gamma_baseline(
    self,
    trajectory_idx: int,
    gamma_value: complex,
    baseline_type: str,
    perspective: str
) -> None:
    """
    Set gamma_self baseline for a trajectory index.
    
    Args:
        trajectory_idx: Index in gamma_self trajectory
        gamma_value: Complex gamma_self value at baseline
        baseline_type: "csv" or "insertion"
        perspective: "M1" or "M2" - REQUIRED for clarity
    """
```

**Benefits**:
1. IDE autocomplete works correctly
2. Type checkers catch errors
3. Documentation is self-evident
4. AI assistants understand intent

### ✅ DO: Use Enums for Closed Sets

```python
# GOOD - type-safe perspective
from enum import Enum

class Perspective(Enum):
    M1 = "M1"
    M2 = "M2"

def set_gamma_baseline(self, perspective: Perspective):
    # ✅ Can't pass "m1" or "M3" by accident
```

**Guideline**: If parameter has 2-5 fixed values, use Enum. If it's a string token, consider StrEnum or Literal.

---

## Error Handling

### ✅ DO: Fail Fast with Clear Messages

```python
# GOOD - validation at entry point
def __init__(self, controller, event_idx: int, insert_time: float):
    if event_idx == 0:
        raise ValueError("Cannot insert before first event")
    
    if insert_time < 0:
        raise ValueError(f"insert_time must be >= 0, got {insert_time}")
    
    # Now we know parameters are valid
    self.event_idx = event_idx
    self.insert_time = insert_time
```

**Benefits**:
1. Bugs caught at call site, not deep in logic
2. Stack trace points to caller (who passed wrong value)
3. Clear error message guides fix

### ❌ DON'T: Silent Failures or Defensive Fixes

```python
# BAD - hides the problem
def update_trajectory(self, gamma_x, gamma_y):
    if gamma_x is None:
        gamma_x = []  # ❌ Why is it None? This hides a bug upstream
    # ... proceed with potentially wrong data
```

**Guideline**: If a parameter is wrong, **fail loudly**. Don't try to recover - force the caller to fix it.

---

## Summary: Key Takeaways

1. **`= None` parameters hide bugs** → Make required parameters explicit
2. **Multiple owners create race conditions** → Single owner pattern with private references
3. **Log at the victim level** → When UI disagrees with logs, instrument the widget
4. **Explicit state tracking** → Don't reconstruct state, store it
5. **Type annotations everywhere** → Self-documenting, IDE-friendly, type-safe
6. **Fail fast** → Validate at entry, raise clear errors, don't recover from wrong data

---

## References

- **Spinbox Refactoring**: [spinbox_refactor_2025_12.md](spinbox_refactor_2025_12.md) - Original lessons learned
- **= None Elimination**: Git commit `0cc6e7a` - Removed optional parameters throughout codebase
- **Architecture Principles**: [01_PRINCIPLES.md](01_PRINCIPLES.md) - High-level design principles
- **API Contracts**: [04_API_CONTRACTS.md](04_API_CONTRACTS.md) - Component interfaces

---

**Contributing**: When you fix a bug or learn a lesson, add it here. Coding guidelines evolve with the codebase.
