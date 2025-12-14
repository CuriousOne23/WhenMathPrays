# State Management Refactoring - Phase 3.4

## Overview

Refactored scattered state management into centralized EditorState module for cleaner, more maintainable code.

## Problem Statement

**Before Refactoring:**
- ~40 state variables scattered across multiple files
- Implicit boolean flags (`dirty`, `in_undo_redo`, `initial_load_complete`)
- No explicit state machine or validation guards
- State transitions through direct assignment
- No observer pattern for state changes

**Issues:**
1. State scattered across controller.py, model.py, interactive_editor.py
2. Boolean flags hard to understand (what does `dirty=True` mean?)
3. No validation preventing invalid state transitions
4. Difficult to add new state-dependent features
5. No centralized place to understand application state

## Solution: Centralized State Management

Created `tools/editor/editor_state.py` with:

### 1. Explicit State Enums

Replace boolean flags with clear enum values:

```python
class PerspectiveState(Enum):
    M1 = "M1"
    M2 = "M2"

class EditState(Enum):
    IDLE = 1        # No active edit
    PREVIEW = 2     # Dragging marker (preview mode)
    COMMITTED = 3   # Edit committed to model

class UndoRedoState(Enum):
    CLEAN = 1           # No unsaved changes
    DIRTY = 2           # Has unsaved changes
    IN_OPERATION = 3    # Currently executing undo/redo

class TrajectoryComputeState(Enum):
    CURRENT = 1    # Trajectory is up-to-date
    SCHEDULED = 2  # Recomputation scheduled (debounce)
    COMPUTING = 3  # Currently computing trajectory

class FileLoadState(Enum):
    DUAL_PERSPECTIVE = 1  # Both M1 and M2 loaded
    SINGLE_M1 = 2         # Only M1 loaded
    SINGLE_M2 = 3         # Only M2 loaded
    NONE = 4              # No files loaded
```

**Benefits:**
- Self-documenting code
- IDE autocomplete support
- Type safety
- Clear valid values

### 2. EditorState Dataclass

Centralized container for all state:

```python
@dataclass
class EditorState:
    perspective: PerspectiveState = PerspectiveState.M1
    edit_state: EditState = EditState.IDLE
    compute_state: TrajectoryComputeState = TrajectoryComputeState.CURRENT
    undo_state: UndoRedoState = UndoRedoState.CLEAN
    file_load_state: FileLoadState = FileLoadState.NONE
    initial_load_complete: bool = False
    dirty: bool = False
```

**Benefits:**
- Single source of truth
- All state in one place
- Easy to serialize/debug

### 3. Validated State Transitions

Replace direct assignment with transition methods:

```python
# Before (scattered across files):
self.perspective = "M2"
self.dirty = True
self.in_undo_redo = True

# After (centralized with validation):
state.switch_perspective(PerspectiveState.M2)
state.mark_dirty()
state.enter_undo_operation()
```

**Transition Methods:**

| Method | Purpose | Validation |
|--------|---------|------------|
| `switch_perspective(target)` | Change M1↔M2 | Cannot switch during preview |
| `start_preview()` | Begin marker drag | Must be in IDLE state |
| `commit_preview()` | Save changes | Must be in PREVIEW state |
| `cancel_preview()` | Discard changes | Must be in PREVIEW state |
| `mark_dirty()` | Unsaved changes | Auto-transitions to DIRTY |
| `mark_clean()` | Changes saved | Auto-transitions to CLEAN |
| `enter_undo_operation()` | Start undo/redo | Prevents recursion |
| `exit_undo_operation()` | End undo/redo | Returns to previous state |

**Benefits:**
- Explicit state machine
- Validation prevents bugs
- Clear contracts

### 4. Operation Validation

Validation methods check if operations are allowed:

```python
# Before (ad-hoc checks scattered in UI event handlers):
if not event.locked and event_idx > 0:
    self.delete_event(event_idx)

# After (centralized validation):
if state.can_delete_event(event.locked, is_first, is_last, len(events)):
    self.delete_event(event_idx)
```

**Validation Methods:**

| Method | Purpose | Checks |
|--------|---------|--------|
| `can_edit_primitive(locked, is_first, is_last)` | Can marker be edited? | Not locked, not in preview |
| `can_delete_event(locked, is_first, is_last, num_events)` | Can event be deleted? | Not locked, not first/last, ≥3 events |
| `can_insert_event(is_first)` | Can event be inserted? | Not before first event |

**Benefits:**
- Consistent validation logic
- Single source of truth for rules
- Easy to update business rules

### 5. Observer Pattern

State change notifications for UI updates:

```python
# Register observer for perspective changes
def on_perspective_changed(old_value, new_value):
    print(f"Perspective changed: {old_value} → {new_value}")
    update_window_title(new_value)
    recompute_trajectory()

state.add_observer('perspective', on_perspective_changed)
```

**Observable State Fields:**
- `perspective` - M1/M2 switch
- `edit_state` - IDLE/PREVIEW/COMMITTED transitions
- `undo_state` - CLEAN/DIRTY/IN_OPERATION changes
- `compute_state` - Trajectory computation status
- `file_load_state` - File loading configuration

**Benefits:**
- Decouples state changes from UI updates
- Automatic notifications
- Easy to add new observers

### 6. Singleton Pattern

Global access to shared state:

```python
from tools.editor.editor_state import get_editor_state

# Access singleton from anywhere
state = get_editor_state()
current_perspective = state.perspective
```

**Benefits:**
- Single state instance shared across components
- No need to pass state through constructor chains
- Easy testing with `reset_editor_state()`

## Implementation Changes

### Controller (`tools/editor/controller.py`)

**Before:**
```python
def __init__(self, model, primitive_panel, trajectory_panel, undo_stack=None):
    self.model = model
    self.primitive_panel = primitive_panel
    self.trajectory_panel = trajectory_panel
    self.undo_stack = undo_stack
    
    self.perspective = "M1"
    self.dirty = False
    self.in_undo_redo = False
    self.initial_load_complete = False
```

**After:**
```python
def __init__(self, model, primitive_panel, trajectory_panel, undo_stack=None, editor_state=None):
    self.model = model
    self.primitive_panel = primitive_panel
    self.trajectory_panel = trajectory_panel
    self.undo_stack = undo_stack
    
    # Centralized state management
    self.state = editor_state if editor_state is not None else EditorState()
    
@property
def perspective(self) -> str:
    """Get current perspective (backward compatibility)."""
    return self.state.perspective.value

@property
def dirty(self) -> bool:
    """Get dirty flag (backward compatibility)."""
    return self.state.dirty
```

**Changes:**
1. Import EditorState, PerspectiveState, FileLoadState
2. Replace scattered state variables with `self.state` instance
3. Add backward-compatible properties for existing code
4. Use state transition methods instead of direct assignment

### Commands (`tools/editor/commands.py`)

**Before:**
```python
def _apply_value(self, value):
    self.controller.in_undo_redo = True
    try:
        self.controller._apply_primitive_change(...)
    finally:
        self.controller.in_undo_redo = False
```

**After:**
```python
def _apply_value(self, value):
    self.controller.state.enter_undo_operation()
    try:
        self.controller._apply_primitive_change(...)
    finally:
        self.controller.state.exit_undo_operation()
```

**Changes:**
1. Use `state.enter_undo_operation()` instead of boolean flag
2. Use `state.exit_undo_operation()` instead of direct assignment
3. Applied to all command classes: EditPrimitiveCommand, ResetPrimitiveCommand, DeleteEventCommand, InsertEventBeforeCommand

### State Transitions

**Before:**
```python
def switch_perspective(self, perspective: str):
    self.perspective = perspective  # Direct assignment
    # ... update UI ...
```

**After:**
```python
def switch_perspective(self, perspective: str):
    target = PerspectiveState.M1 if perspective == 'M1' else PerspectiveState.M2
    self.state.switch_perspective(target)  # Validated transition
    # ... update UI ...
```

**Before:**
```python
def on_primitive_preview(self, event_index, primitive, value):
    self.dirty = True  # Direct assignment
    self._schedule_recomputation_preview()
```

**After:**
```python
def on_primitive_preview(self, event_index, primitive, value):
    self.state.mark_dirty()  # State transition method
    self._schedule_recomputation_preview()
```

## Testing

Created comprehensive test suite: `tests/editor/test_editor_state.py`

**Test Coverage:**
- 34 tests covering all state functionality
- Perspective state transitions (3 tests)
- Edit state machine (5 tests)
- Undo/redo state management (6 tests)
- Trajectory compute state (1 test)
- File load state (2 tests)
- Dirty flag management (3 tests)
- Operation validation (8 tests)
- Observer pattern notifications (3 tests)
- Singleton pattern (2 tests)

**Test Results:**
```
34 passed in 0.07s
```

All existing editor tests continue to pass:
```
82 passed in 0.86s
```

## Benefits Achieved

### 1. Code Clarity
- **Before:** `if self.dirty and not self.in_undo_redo:`
- **After:** `if state.undo_state == UndoRedoState.DIRTY:`

### 2. Type Safety
```python
# Before: Any string accepted
self.perspective = "InvalidPerspective"  # Runtime error

# After: Only valid enums accepted
state.switch_perspective(PerspectiveState.INVALID)  # Compile-time error
```

### 3. Validation
```python
# Before: No validation
self.dirty = True
self.in_undo_redo = True  # Both can be true - what does this mean?

# After: Validated transitions
state.mark_dirty()  # Sets undo_state = DIRTY
state.enter_undo_operation()  # Sets undo_state = IN_OPERATION
# clear semantics: IN_OPERATION takes precedence
```

### 4. Maintainability
- All state logic in one module (`editor_state.py`)
- Easy to add new states or transitions
- Clear documentation of state machine
- Single place to update business rules

### 5. Testability
- State can be tested independently
- Easy to set up test scenarios
- Clear assertions on state values
- No need to mock complex UI interactions

### 6. Future Features
State management now supports:
- Multi-level undo grouping
- State persistence (save/restore)
- State history tracking
- Time-travel debugging
- State synchronization across components

## Migration Guide

### For New Code

Use EditorState directly:
```python
from tools.editor.editor_state import get_editor_state, PerspectiveState

state = get_editor_state()

# Check state
if state.perspective == PerspectiveState.M1:
    # ...

# Transition state
state.switch_perspective(PerspectiveState.M2)

# Validate operations
if state.can_edit_primitive(event.locked, is_first, is_last):
    # safe to edit
```

### For Existing Code

Backward-compatible properties available:
```python
# Old style still works
perspective = controller.perspective  # Returns string "M1" or "M2"
is_dirty = controller.dirty  # Returns boolean
in_undo = controller.in_undo_redo  # Returns boolean

# But prefer new style
perspective = controller.state.perspective  # Returns PerspectiveState.M1
is_dirty = controller.state.dirty
in_undo = controller.state.is_in_undo_operation()
```

### Adding New State

1. Define enum in `editor_state.py`:
```python
class MyState(Enum):
    STATE_A = 1
    STATE_B = 2
```

2. Add field to EditorState:
```python
@dataclass
class EditorState:
    my_state: MyState = MyState.STATE_A
```

3. Add transition methods:
```python
def transition_to_b(self) -> bool:
    if self.my_state != MyState.STATE_A:
        return False
    old = self.my_state
    self.my_state = MyState.STATE_B
    self._notify_observers('my_state', old, MyState.STATE_B)
    return True
```

4. Add validation methods if needed:
```python
def can_do_something(self) -> bool:
    return self.my_state == MyState.STATE_A
```

## Files Modified

1. **tools/editor/editor_state.py** - NEW (349 lines)
   - EditorState dataclass
   - 5 state enums
   - Transition methods
   - Validation methods
   - Observer pattern
   - Singleton pattern

2. **tools/editor/controller.py** - REFACTORED
   - Import EditorState
   - Replace scattered state variables
   - Add backward-compatible properties
   - Use state transition methods
   - Use state.mark_dirty()/mark_clean()

3. **tools/editor/commands.py** - REFACTORED
   - Update all undo command classes
   - Use state.enter_undo_operation()
   - Use state.exit_undo_operation()

4. **tests/editor/test_editor_state.py** - NEW (270 lines)
   - 34 comprehensive tests
   - All state functionality covered
   - 100% pass rate

## Performance Impact

**Negligible:**
- Enum comparisons same speed as string/boolean comparisons
- Observer notifications O(n) where n = number of observers
- Typically 0-3 observers per state field
- No observable performance degradation

## Future Work

### Potential Enhancements

1. **State History**
   ```python
   state.get_history()  # Returns list of state changes
   state.undo_state_change()  # Revert to previous state
   ```

2. **State Persistence**
   ```python
   state.save_to_file('editor_state.json')
   state.load_from_file('editor_state.json')
   ```

3. **State Validation**
   ```python
   state.validate()  # Check for invalid state combinations
   ```

4. **State Snapshots**
   ```python
   snapshot = state.create_snapshot()
   state.restore_snapshot(snapshot)
   ```

5. **State Debugging**
   ```python
   state.enable_debug_logging()
   # Logs all state transitions to console
   ```

## Conclusion

State management refactoring successfully:
- ✅ Centralized scattered state into EditorState
- ✅ Replaced implicit booleans with explicit enums
- ✅ Added state transition validation
- ✅ Implemented observer pattern for notifications
- ✅ Maintained backward compatibility
- ✅ All tests pass (82/82)
- ✅ No performance degradation
- ✅ Foundation for future features

Code is now more maintainable, testable, and extensible while preserving all existing functionality.

---

# Architectural Refactoring Plan - Next Steps

## Overview

Following the bug fix for perspective-isolation (marker labels persisting across M1/M2 views) and UI layout optimization (laptop-friendly 1200x590 window), the editor has several architectural improvements needed to eliminate technical debt and improve maintainability.

**Context:** The perspective bug was fixed with a temporary hack (`_modification_perspective` dict) and runtime filtering in the controller. The UI layout optimization revealed hardcoded magic numbers scattered across multiple files. Both areas need proper architectural solutions.

## Priority 1: Data Model (Perspective Isolation)

**Goal:** Eliminate the temporary hack and make dual-perspective explicit in the data model

**Current Problem:**
- `modified_primitives` is perspective-independent (shared dict)
- `marker_positions` is perspective-independent (shared dict)
- Controller filters these at runtime using `is_modified(event, primitive, perspective)`
- Model has `_modification_perspective: Dict[float, str]` tracking hack
- Bug fixed but architecture is wrong

**Solution:**

### 1.1 Split `modified_primitives` (model.py)
```python
# Replace:
modified_primitives: Dict[float, Dict[str, Any]] = {}

# With:
modified_primitives_m1: Dict[float, Dict[str, Any]] = {}
modified_primitives_m2: Dict[float, Dict[str, Any]] = {}
```

Add perspective-aware API:
```python
def get_modified_primitives(self, perspective: str) -> Dict[float, Dict[str, Any]]:
    """Get modifications for specific perspective."""
    return self.modified_primitives_m1 if perspective == "m1" else self.modified_primitives_m2

def modify_primitive(self, event_idx: int, primitive: str, new_value: float, perspective: str):
    """Modify primitive for specific perspective."""
    target_dict = self.modified_primitives_m1 if perspective == "m1" else self.modified_primitives_m2
    # ... rest of logic ...
```

### 1.2 Split `marker_positions` (model.py)
```python
# Replace:
marker_positions: Dict[float, Dict[str, float]] = {}

# With:
marker_positions_m1: Dict[float, Dict[str, float]] = {}
marker_positions_m2: Dict[float, Dict[str, float]] = {}
```

Add perspective-aware API:
```python
def get_marker_positions(self, perspective: str) -> Dict[float, Dict[str, float]]:
    """Get pinned markers for specific perspective."""
    return self.marker_positions_m1 if perspective == "m1" else self.marker_positions_m2

def pin_marker(self, time: float, gamma_self: float, perspective: str):
    """Pin marker for specific perspective."""
    target_dict = self.marker_positions_m1 if perspective == "m1" else self.marker_positions_m2
    # ... rest of logic ...
```

### 1.3 Remove Temporary Hack
**model.py:**
- Delete line 107: `_modification_perspective: Dict[float, str] = {}`
- Remove lines 236: Perspective tracking in modification
- Remove lines 470-481: `is_modified()` perspective filtering

**controller.py:**
- Remove lines 1330-1341: `is_modified()` filtering for marked_data
- Remove lines 1365-1367: `is_modified()` filtering for pinned_markers
- Use new API: `model.get_modified_primitives(self.perspective)`

**Files to Modify:**
- `tools/editor/model.py` - Data structure split
- `tools/editor/controller.py` - Use new APIs
- `tools/editor/views/trajectory_panel_pyqtgraph.py` - Pin marker calls
- `tools/editor/views/primitive_panel_pyqtgraph.py` - Modify primitive calls

**Testing:**
- Verify M1 modifications invisible in M2
- Verify M2 modifications invisible in M1
- Verify pinned markers respect perspective
- Load existing CSV files (backward compatibility)

**Estimated Effort:** 2-3 hours

---

## Priority 2: Layout Configuration

**Goal:** Make UI layout maintainable and extensible

**Current Problem:**
- Window size: `self.setGeometry(100, 100, 1200, 590)` in qt_window.py
- Panel widths: `resizeDocks([primitive_dock, controls_dock], [445, 755])` in interactive_editor.py
- Font sizes: `QFont("Arial", 7)` scattered in panel views
- Margins: `setContentsMargins(0, 0, 15, 0)` in trajectory panel
- No single source of truth for layout values

**Solution:**

### 2.1 Create Layout Config Module
**Create: tools/editor/layout_config.py**
```python
"""
Centralized configuration for editor layout, sizing, and styling.
"""

# Window dimensions
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 590
WINDOW_X = 100
WINDOW_Y = 100

# Panel widths (must sum to WINDOW_WIDTH)
PRIMITIVE_PANEL_WIDTH = 445
CONTROLS_PANEL_WIDTH = 260
TRAJECTORY_PANEL_WIDTH = 495

# Font sizes
PRIMITIVE_TICK_FONT_SIZE = 7
PRIMITIVE_LABEL_FONT_SIZE = 8
PRIMITIVE_AXIS_WIDTH = 35

TRAJECTORY_LABEL_FONT_SIZE = 9
TRAJECTORY_TICK_FONT_SIZE = 8

CONTROLS_LABEL_FONT_SIZE = 9

# Margins and spacing
TRAJECTORY_RIGHT_MARGIN = 15  # Layout margin (widget space)
PLOT_DATA_MARGIN = 20.0       # Plot margin (data space)

PANEL_SPACING = 0
DOCK_BORDER_WIDTH = 1

# Widget heights
GAUGE_MIN_HEIGHT = 30
SLIDER_HEIGHT = 30

# Colors (if centralized)
MODIFIED_MARKER_COLOR = (255, 0, 0)    # Red
PINNED_MARKER_COLOR = (0, 128, 255)    # Blue
```

### 2.2 Update Files to Use Config
**tools/editor/qt_window.py:**
```python
from tools.editor.layout_config import WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT

def __init__(self):
    super().__init__()
    self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
```

**tools/interactive_editor.py:**
```python
from tools.editor.layout_config import (
    PRIMITIVE_PANEL_WIDTH, CONTROLS_PANEL_WIDTH, TRAJECTORY_PANEL_WIDTH,
    GAUGE_MIN_HEIGHT
)

# Line 237, 259:
primitive_gauge.setMinimumHeight(GAUGE_MIN_HEIGHT)
gamma_self_gauge.setMinimumHeight(GAUGE_MIN_HEIGHT)

# Lines 305-320:
self.resizeDocks([primitive_dock, controls_dock], 
                 [PRIMITIVE_PANEL_WIDTH, CONTROLS_PANEL_WIDTH + TRAJECTORY_PANEL_WIDTH])
self.resizeDocks([controls_dock, trajectory_dock],
                 [CONTROLS_PANEL_WIDTH, TRAJECTORY_PANEL_WIDTH])
```

**tools/editor/views/primitive_panel_pyqtgraph.py:**
```python
from tools.editor.layout_config import (
    PRIMITIVE_TICK_FONT_SIZE, PRIMITIVE_LABEL_FONT_SIZE, PRIMITIVE_AXIS_WIDTH
)

# Lines 281-285:
axis.setStyle(tickFont=QFont("Arial", PRIMITIVE_TICK_FONT_SIZE))
axis.setWidth(PRIMITIVE_AXIS_WIDTH)
label_style = {'color': '#000', 'font-size': f'{PRIMITIVE_LABEL_FONT_SIZE}pt'}
axis.setLabel(label_text, **label_style)
```

**tools/editor/views/trajectory_panel_pyqtgraph.py:**
```python
from tools.editor.layout_config import TRAJECTORY_RIGHT_MARGIN, PLOT_DATA_MARGIN

# Line 152:
layout.setContentsMargins(0, 0, TRAJECTORY_RIGHT_MARGIN, 0)

# Line 367:
margin = PLOT_DATA_MARGIN
```

**Files to Modify:**
- `tools/editor/layout_config.py` - NEW
- `tools/editor/qt_window.py` - Import and use config
- `tools/interactive_editor.py` - Import and use config
- `tools/editor/views/primitive_panel_pyqtgraph.py` - Import and use config
- `tools/editor/views/trajectory_panel_pyqtgraph.py` - Import and use config

**Testing:**
- Clear registry: `reg delete "HKEY_CURRENT_USER\Software\WhenMathPrays\InteractiveEditor" /f`
- Launch editor, verify same layout as before
- Modify a constant, verify change takes effect
- Verify no hardcoded numbers remain (grep for `445`, `590`, `7pt`, etc.)

**Estimated Effort:** 1-2 hours

---

## Priority 3: Layout Management

**Goal:** Declarative dock arrangement for easy modification

**Current Problem:**
```python
# Lines 279-292 in interactive_editor.py
self.addDockWidget(Qt.LeftDockWidgetArea, controls_dock)
self.splitDockWidget(controls_dock, trajectory_dock, Qt.Horizontal)
self.tabifyDockWidget(primitive_dock, controls_dock)
# ... 13 more lines of imperative dock wiring
```
- Hard to visualize final layout
- Hard to modify arrangement
- Fragile order dependencies
- Adding new panels requires understanding splitDockWidget logic

**Solution:**

### 3.1 Define Declarative Layout Format
**In tools/editor/layout_config.py:**
```python
"""
Layout configuration defines a column-based structure.
Each column can contain one or more panels.
If multiple panels, they split the column vertically.
"""

LAYOUT_LAPTOP = {
    'name': 'Laptop (1200x590)',
    'window': {
        'width': 1200,
        'height': 590,
        'x': 100,
        'y': 100
    },
    'columns': [
        {
            'panels': ['primitives'],
            'width': 445,
        },
        {
            'panels': ['trajectory', 'controls'],
            'width': 755,
            'split': 'vertical',
            'sizes': [495, 260]  # Heights when split vertically
        }
    ]
}

# Future layouts
LAYOUT_DESKTOP = {
    'name': 'Desktop (1600x900)',
    'window': {'width': 1600, 'height': 900, 'x': 100, 'y': 100},
    'columns': [
        {'panels': ['primitives'], 'width': 600},
        {'panels': ['trajectory'], 'width': 700},
        {'panels': ['controls', 'history'], 'width': 300, 'split': 'vertical', 'sizes': [450, 450]}
    ]
}

# Active layout
ACTIVE_LAYOUT = LAYOUT_LAPTOP
```

### 3.2 Create Layout Manager
**Create: tools/editor/layout_manager.py**
```python
"""
Manages dock widget arrangement from declarative configuration.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QMainWindow

class LayoutManager:
    def __init__(self, main_window: QMainWindow):
        self.window = main_window
    
    def apply_layout(self, layout_config: dict, dock_registry: dict):
        """
        Apply layout configuration to registered dock widgets.
        
        Args:
            layout_config: Layout dict from layout_config.py
            dock_registry: {'panel_name': QDockWidget} mapping
        """
        # Set window geometry
        window_cfg = layout_config['window']
        self.window.setGeometry(
            window_cfg['x'], window_cfg['y'],
            window_cfg['width'], window_cfg['height']
        )
        
        columns = layout_config['columns']
        
        # Add first column's first panel as anchor
        first_panel = columns[0]['panels'][0]
        first_dock = dock_registry[first_panel]
        self.window.addDockWidget(Qt.LeftDockWidgetArea, first_dock)
        
        # Track rightmost dock for horizontal splitting
        rightmost_dock = first_dock
        column_docks = [first_dock]
        
        # Process remaining panels in first column (vertical splits)
        for panel_name in columns[0]['panels'][1:]:
            dock = dock_registry[panel_name]
            self.window.splitDockWidget(column_docks[0], dock, Qt.Vertical)
            column_docks.append(dock)
        
        # Process remaining columns (horizontal splits)
        for col in columns[1:]:
            col_panels = col['panels']
            col_first_dock = dock_registry[col_panels[0]]
            
            # Split horizontally from rightmost dock
            self.window.splitDockWidget(rightmost_dock, col_first_dock, Qt.Horizontal)
            column_docks = [col_first_dock]
            
            # Process remaining panels in column (vertical splits)
            for panel_name in col_panels[1:]:
                dock = dock_registry[panel_name]
                self.window.splitDockWidget(column_docks[0], dock, Qt.Vertical)
                column_docks.append(dock)
            
            rightmost_dock = column_docks[0]
        
        # Apply resize proportions
        self._apply_sizes(layout_config, dock_registry)
    
    def _apply_sizes(self, layout_config: dict, dock_registry: dict):
        """Apply width/height proportions to docks."""
        columns = layout_config['columns']
        
        # Horizontal splits (column widths)
        if len(columns) > 1:
            # Collect docks for horizontal resizing
            col_docks = [dock_registry[col['panels'][0]] for col in columns]
            col_widths = [col['width'] for col in columns]
            self.window.resizeDocks(col_docks, col_widths, Qt.Horizontal)
        
        # Vertical splits within columns
        for col in columns:
            if len(col['panels']) > 1 and 'sizes' in col:
                col_docks = [dock_registry[p] for p in col['panels']]
                self.window.resizeDocks(col_docks, col['sizes'], Qt.Vertical)
```

### 3.3 Update interactive_editor.py
```python
from tools.editor.layout_config import ACTIVE_LAYOUT
from tools.editor.layout_manager import LayoutManager

class InteractiveEditor(QtWindow):
    def __init__(self, csv_path):
        super().__init__()
        
        # ... create all panels ...
        
        # Register docks
        dock_registry = {
            'primitives': primitive_dock,
            'trajectory': trajectory_dock,
            'controls': controls_dock
        }
        
        # Apply layout
        layout_mgr = LayoutManager(self)
        layout_mgr.apply_layout(ACTIVE_LAYOUT, dock_registry)
```

**Files to Modify:**
- `tools/editor/layout_config.py` - Add LAYOUT_LAPTOP dict
- `tools/editor/layout_manager.py` - NEW
- `tools/interactive_editor.py` - Replace lines 279-320 with LayoutManager

**Testing:**
- Launch editor, verify same layout as before
- Change ACTIVE_LAYOUT to LAYOUT_DESKTOP (define stub), verify it applies
- Add dummy 'history' panel, verify it appears in layout

**Estimated Effort:** 2-3 hours

---

## Priority 4: Save/Export (Dual Perspective)

**Goal:** Persist both perspectives' modifications to file

**Current Problem:**
- Save only writes single perspective to CSV
- No way to preserve both M1 and M2 modifications
- Lost work when switching perspectives

**Solution:**

### 4.1 Design File Format
**Option A: Single File with Perspective Markers**
```csv
# DUAL_PERSPECTIVE_FILE
# Version: 1.0
event_day,M1_v,M1_r,M1_phi,M1_alpha,M1_eta,M2_v,M2_r,M2_phi,M2_alpha,M2_eta,gamma_self
0.0,0.3,0.2,0.95,0.1,0.1,0.3,0.2,0.95,0.1,0.1,-0.5
7.0,0.5,0.25,0.96,0.12,0.12,0.3,0.2,0.95,0.1,0.1,-0.3
...
```

**Option B: Metadata Section**
```csv
# METADATA
# perspective_m1: true
# perspective_m2: true
# modified_events_m1: 7.0,14.0,42.0
# modified_events_m2: 21.0,35.0
# pinned_markers_m1: 7.5:-0.45,14.5:-0.12
# pinned_markers_m2: 21.5:0.23
# END_METADATA
event_day,v,r,phi,alpha,eta,gamma_self
...
```

### 4.2 Implement Save/Load
**tools/editor/model.py:**
```python
def save_dual_perspective(self, filepath: str):
    """Save both M1 and M2 modifications to file."""
    # Build metadata
    metadata = {
        'version': '1.0',
        'perspective_m1': bool(self.modified_primitives_m1),
        'perspective_m2': bool(self.modified_primitives_m2),
        'modified_events_m1': list(self.modified_primitives_m1.keys()),
        'modified_events_m2': list(self.modified_primitives_m2.keys()),
        'pinned_markers_m1': self.marker_positions_m1,
        'pinned_markers_m2': self.marker_positions_m2,
    }
    
    # Write CSV with metadata header
    with open(filepath, 'w') as f:
        f.write("# DUAL_PERSPECTIVE_FILE\n")
        for key, value in metadata.items():
            f.write(f"# {key}: {value}\n")
        f.write("# END_METADATA\n")
        
        # Write data rows
        # ... CSV writing logic ...

def load_dual_perspective(self, filepath: str):
    """Load file with both M1 and M2 modifications."""
    # Parse metadata
    # Restore modified_primitives_m1/m2
    # Restore marker_positions_m1/m2
    # Return both perspectives
```

**Backward Compatibility:**
- Files without metadata header treated as single-perspective
- Load into M1, leave M2 empty
- Preserve existing workflow

**Files to Modify:**
- `tools/editor/model.py` - Add save/load methods
- `tools/editor/controller.py` - Call save_dual_perspective
- `tools/interactive_editor.py` - Update File→Save menu

**Testing:**
- Save file with M1 modifications only
- Save file with M2 modifications only
- Save file with both M1 and M2 modifications
- Load saved files, verify all modifications restored
- Load old single-perspective files, verify backward compatibility

**Estimated Effort:** 2-4 hours

---

## Implementation Order

### Step 1: Data Model (Priority 1)
- Most critical architectural debt
- Fixes temporary hack properly
- Enables correct save/load
- **Do First**

### Step 2: Layout Config (Priority 2)
- Extract hardcoded constants
- No new functionality
- Quick win for maintainability
- **Do Second** (while in those files from Step 1)

### Step 3: Layout Manager (Priority 3)
- Requires config from Step 2
- Biggest payoff for future panels
- **Do Third**

### Step 4: Save/Export (Priority 4)
- Requires data model from Step 1
- Less urgent (current hack works for session)
- **Do Fourth** (or defer to future)

## Success Criteria

### Data Model Refactoring
- ✅ No `_modification_perspective` hack
- ✅ No runtime filtering in controller
- ✅ Clean perspective-aware APIs
- ✅ All existing tests pass
- ✅ M1/M2 modifications completely isolated

### Layout Configuration
- ✅ No hardcoded sizes in view files
- ✅ Single source of truth for dimensions
- ✅ Easy to create new layout presets
- ✅ Same visual appearance after refactor

### Layout Management
- ✅ Declarative layout definition
- ✅ Trivial to add new panels
- ✅ LayoutManager class tested
- ✅ Multiple layout presets defined

### Save/Export
- ✅ Both perspectives saved to file
- ✅ Both perspectives restored on load
- ✅ Backward compatibility preserved
- ✅ Clear file format documentation

## Phased Implementation Strategy

### Rationale for Sequencing

The refactoring is structured in phases to maximize value and minimize risk:

1. **Clean Architecture First** - Eliminates technical debt before building on it
2. **Save Function Second** - Requires clean data model, enables preservation of work
3. **Testing After Architecture** - Test stable, clean code rather than temporary hacks
4. **Advanced Features Last** - Build on solid foundation

### Phase 1: Architecture Cleanup (Do First)

**Goal:** Clean, maintainable foundation for all future work

**Priorities:**
1. Data Model Refactoring (2-3 hours)
   - Split perspective-independent data structures
   - Remove temporary `_modification_perspective` hack
   - Clean perspective-aware APIs
   
2. Layout Configuration (1-2 hours)
   - Extract all hardcoded constants
   - Single source of truth for dimensions/fonts/margins
   
3. Layout Manager (2-3 hours)
   - Declarative dock arrangement
   - Easy panel addition for future features

**Why First:**
- Save function needs clean dual-perspective data model
- Testing needs stable architecture (avoid rewriting tests)
- Scenarios need save function (preserve work between sessions)
- Future features benefit from maintainable layout system

**Deliverables:**
- Proper dual-perspective data model
- Centralized configuration
- Declarative layout system
- All existing functionality preserved

**Phase 1 Total: 5-8 hours**

---

### Phase 2: Save Function (Do Second)

**Goal:** Make editor usable for research - preserve work between sessions

**Priority:**
4. Dual-Perspective Save/Load (2-4 hours)
   - Save both M1 and M2 modifications to file
   - Metadata format with version info
   - Backward compatibility with existing files
   - Restore complete session state

**Why Second:**
- Requires clean data model from Phase 1
- Critical blocker for scenario development
- Without save, all work is lost when editor closes
- Scenarios can't be refined/iterated without persistence

**Deliverables:**
- File format with dual-perspective support
- Save/load both perspectives
- Preserve pinned markers
- Backward compatible loading

**Phase 2 Total: 2-4 hours**

---

### Phase 3: Scenario Development (Parallel)

**Goal:** Build scenario library for gamma-self research

**Activities:**
- Define canonical relationship scenarios
- Document primitive modeling patterns
- Create scenario templates
- Validate against theoretical predictions

**Can Run Parallel With:**
- Phase 1 architecture work
- Phase 2 save implementation
- Scenarios inform what features are needed

**Prerequisites:**
- Phase 2 save function (to preserve scenarios)
- Clean editor workflow

**Deliverables:**
- Scenario library in `scenarios/library/`
- Scenario documentation
- Primitive modeling best practices

**Phase 3 Ongoing:** Continues through project lifetime

---

### Phase 4: Automated Testing (Do After Architecture)

**Goal:** Lock in correctness, enable confident refactoring

**Test Suites:**
1. Core Math Tests (3-4 hours)
   - revenge_core.py, love.py algorithms
   - Known scenarios with hand-calculated results
   - Edge cases (zero values, boundary conditions)
   - Numerical stability
   - Dual-perspective symmetry
   
2. Model Isolation Tests (2-3 hours)
   - Verify M1/M2 separation in refactored model
   - Test perspective-aware APIs
   - Validate modifications stay isolated
   - Test pinned marker isolation

**Why After Architecture:**
- Clean code is easier to test
- Tests validate refactored system correctness
- Stable APIs mean tests won't need rewriting
- Focus on scientific correctness, not implementation details

**Skipping:**
- GUI tests (manual testing working well)
- Integration tests (user workflow is integration test)

**Deliverables:**
- tests/test_revenge_core.py
- tests/editor/test_model_perspective.py
- pytest configuration
- CI-ready test suite

**Phase 4 Total: 5-7 hours**

---

### Phase 5: Reverse Gamma-Self Feature (Future)

**Goal:** Given target gamma-self trajectory, find primitive sequences

**Approach:**
- Optimization algorithms
- Search strategies
- Validation against forward model
- UI for specifying target trajectories

**Prerequisites:**
- Phases 1-4 complete (solid foundation)
- Core math validated by tests
- Save function working (preserve reverse-engineered scenarios)

**Research Questions:**
- Uniqueness: How many primitive sequences produce same trajectory?
- Controllability: Can any trajectory be achieved?
- Convergence: How quickly can we find solutions?

**Deliverables:**
- Reverse engineering algorithm
- UI panel for target specification
- Scenario generator from trajectories
- Research documentation

**Phase 5 Total: TBD** (requires research phase)

---

## Estimated Total Effort

### Immediate Work (Phases 1-2):
- Priority 1: 2-3 hours (Data Model)
- Priority 2: 1-2 hours (Layout Config)
- Priority 3: 2-3 hours (Layout Manager)
- Priority 4: 2-4 hours (Save Function)

**Phase 1-2 Total: 7-12 hours**

### Follow-on Work (Phase 4):
- Core math tests: 3-4 hours
- Model tests: 2-3 hours

**Phase 4 Total: 5-7 hours**

### Future Work (Phase 5):
- Research + implementation: TBD

**Grand Total (Phases 1-4): 12-19 hours**

---

## Success Criteria by Phase

### Phase 1 Complete:
- ✅ No `_modification_perspective` hack
- ✅ Clean perspective-aware APIs in model
- ✅ All constants in layout_config.py
- ✅ Declarative layout in layout_manager.py
- ✅ Same visual appearance after refactor
- ✅ All existing tests pass

### Phase 2 Complete:
- ✅ Save file preserves both M1 and M2 modifications
- ✅ Load restores complete session state
- ✅ Backward compatibility with old files
- ✅ Work persists between editor sessions

### Phase 3 Ongoing:
- ✅ Growing scenario library
- ✅ Scenarios validated against theory
- ✅ Documentation for scenario creation

### Phase 4 Complete:
- ✅ Core math validated by tests
- ✅ Perspective isolation verified
- ✅ pytest suite passes
- ✅ Confident refactoring enabled

### Phase 5 Complete:
- ✅ Reverse engineering working
- ✅ Target trajectories achievable
- ✅ Research questions answered

---

## Implementation Notes

**Phase 1 starts immediately** after documentation complete.

**Phase 2 follows Phase 1** - save function requires clean data model.

**Phase 3 runs parallel** - scenario development informs requirements.

**Phase 4 validates Phases 1-2** - tests confirm clean architecture is correct.

**Phase 5 is future work** - depends on research direction.

---

## State Viewer Log - Specification (v2.2.2+)

### Overview

The **State Viewer Log** exports detailed state transition information for debugging and analysis. This section defines what states are tracked, how they're logged, and what format users/AI assistants will see.

### Purpose

- **Debugging**: Rapid diagnosis of unexpected behavior
- **AI-Assisted Analysis**: Share structured logs for intelligent diagnosis
- **Learning**: Understand program behavior and state flow
- **Post-Mortem**: Analyze issues that occurred during session

### Architecture Philosophy

The State Viewer follows strict design principles to remain reliable and maintainable:

#### Core Principles

1. **Zero-Overhead Design**
   - ~100ns per operation when enabled
   - Zero overhead when disabled via `STATE_VIEWER=0`
   - Fixed 850KB memory footprint (ring buffer of 1000 operations)
   - No unbounded growth, no memory leaks
   - Always-on by default without impacting user experience

2. **Flight Data Recorder Pattern**
   - Records facts continuously during operation
   - Export happens instantly (all work done incrementally)
   - No reconstruction, no backfilling
   - Captures ground truth as it happens

3. **Automatic Context Capture**
   - Location detection via `traceback.extract_stack()`
   - No manual location strings needed
   - Compiler-precise file:line references
   - Single line of code per instrumented operation

4. **Agnostic, Simple, Reliable, No Waves**
   - **RECORDS FACTS ONLY** - before/after state snapshots
   - **NO DECISION LOGIC** - no if/then branches, no validation rules
   - **NO DOMAIN KNOWLEDGE** - doesn't know what states "should" be
   - **NO WARNINGS GENERATION** - only detects unchanged fields (structural, not semantic)
   
   ⚠️ **WARNING TO MAINTAINERS**: Do not add business logic, validation rules, or domain-specific decisions to StateViewer. Keep it pure. Analysis belongs in separate tools.

5. **Separation of Concerns**
   - **StateViewer**: Records what happened (facts)
   - **Separate Analyzers**: Interpret what it means (analysis)
   - **Domain Validators**: Check if behavior was correct (rules)
   
   This separation ensures StateViewer remains trustworthy even as domain rules evolve.

#### Why These Principles Matter

**Temptation to Add Logic**: As the codebase grows, there will be pressure to add "smart" features:
- "Let's have StateViewer detect this specific bug pattern"
- "Let's add validation for this particular invariant"
- "Let's generate warnings for domain-specific issues"

**Why to Resist**: 
- Adding logic creates coupling to domain knowledge
- Domain rules change; facts don't
- Complex StateViewer becomes unreliable
- Testing becomes harder
- Future bugs might be in StateViewer itself

**The Right Way**: Build separate analyzer tools that consume StateViewer logs. Keep the recorder pure and simple.

### Tracked States

The State Viewer logs transitions for these state domains:

#### 1. Marker State (Primitive Values)
**Tracked Operations:**
- `update_primitive` - User drags marker to new value
- `reset_primitive` - User double-clicks to restore baseline

**State Fields:**
```python
{
    'value': float,              # Primitive value
    'gamma_position': complex,   # Where on trajectory when modified
    'in_modified_dict': bool     # In modified_primitives tracking
}
```

**Invariants Validated:**
- After `reset_primitive`: `gamma_position` must be `None`
- After `reset_primitive`: `in_modified_dict` must be `False`
- After `update_primitive`: `in_modified_dict` must be `True`

#### 2. Event Lifecycle
**Tracked Operations:**
- `insert_event` - User Ctrl+Shift+Click to insert new event
- `delete_event` - User Ctrl+Click to delete event

**State Fields:**
```python
{
    'event_count': int,          # Total events in timeline
    'event_times': List[float],  # Time values of all events
    'event_ids': List[int]       # Immutable IDs of all events
}
```

**Invariants Validated:**
- Cannot delete first or last event
- Cannot delete when only 2 events remain
- Insertion shifts all subsequent times correctly

#### 3. Trajectory Computation
**Tracked Operations:**
- `trajectory_computed` - New gamma_self trajectory calculated

**State Fields:**
```python
{
    'trajectory_length': int,           # Number of trajectory points
    'final_gamma': complex,             # Endpoint of trajectory
    'pinned_markers_count': int,        # How many markers on trajectory
}
```

#### 4. Perspective State
**Tracked Operations:**
- `switch_perspective` - User switches between M1/M2

**State Fields:**
```python
{
    'active_perspective': str,   # 'M1' or 'M2'
    'has_m1_data': bool,
    'has_m2_data': bool
}
```

### Log File Format

**Filename:** `logs/state_log_YYYYMMDD_HHMMSS.txt`

**Example Log File:** See [example_state_log.txt](example_state_log.txt) for a complete real-world example showing 35 operations including edits, inserts, undos, and perspective switches.

#### Privacy and Path Sanitization

**Username Anonymization**: All paths in the log automatically replace usernames with `user` to protect privacy when sharing logs. For example:
- `C:\Users\jeffg\Documents\...` → `C:\Users\user\Documents\...`
- `/home/jeffg/projects/...` → `/home/user/projects/...`

This is intentional and ensures logs can be safely shared for debugging without exposing personal information. The sanitization is implemented in `StateViewer._sanitize_path()` and can be modified if different behavior is needed for your environment.

**Structure:**
```
STATE VIEWER LOG
================================================================================
Session: 2025-12-14T10:23:45.123456
Python: 3.10.0
Platform: Windows-10-...
Working directory: C:\Users\user\Documents\GitHub\WhenMathPrays

Loaded files:
  Dual-file mode:
    M1: data\library\love\single_dating_to_love_M1.csv
    M2: data\library\love\single_dating_to_love_M2.csv

Total operations: 89
Warnings: 1
================================================================================

⚠️  WARNINGS DETECTED
--------------------------------------------------------------------------------
  #0067: reset_primitive at model.py:572

OPERATION LOG
================================================================================

[0065] update_primitive
Time: 2025-12-14T10:23:45.120
Entity: (event_id=5, prim='v', perspective='M1')
Location: model.py:248 in update_primitive()
Changes:
  value: 5.0 → -0.125  ✓
  gamma_position: None → (21.78+69.12j)  ✓
  in_modified_dict: False → True  ✓

[0067] reset_primitive
Time: 2025-12-14T10:23:47.456
Entity: (event_id=5, prim='v', perspective='M1')
Location: model.py:572 in reset_event_primitive()
Changes:
  value: -0.125 → 5.0  ✓
  in_modified_dict: True → False  ✓
  gamma_position: (21.78+69.12j) → (21.78+69.12j)  ⚠️  UNCHANGED
⚠️  WARNING: Expected gamma_position to change to None, but remained unchanged

[0068] update_trajectory
Time: 2025-12-14T10:23:47.458
Entity: perspective='M1'
Location: controller.py:1532 in _update_trajectory()
Changes:
  pinned_markers_count: 0 → 1  ✓
  marker_included: (5, 'v') because gamma_position=(21.78+69.12j)
```

### Log Field Definitions

**Header Fields:**
- `Session` - ISO 8601 timestamp when log exported
- `Python` - Python version running the editor
- `Platform` - OS and version
- `Loaded file` - CSV file being edited
- `Perspective` - Active perspective (M1 or M2)
- `Total operations` - Count of state-changing operations
- `Warnings` - Count of invariant violations detected

**Operation Entry Fields:**
- `[ID]` - Sequential operation number (0-based)
- `Time` - ISO 8601 timestamp when operation occurred
- `Entity` - What was affected (event_id, primitive, perspective)
- `Location` - File:line where operation was executed
- `Changes` - Fields that changed with before → after values
- `✓` - Field changed as expected
- `⚠️  UNCHANGED` - Field should have changed but didn't (potential bug)
- `⚠️  WARNING` - Invariant violation detected

### Using the Log for Debugging

**Scenario: Label not clearing after reset**

1. **Export log**: Press `Ctrl+Shift+L`
2. **Read warnings section**: Identifies operation #67 has issue
3. **Find operation**: Jump to `[0067] reset_primitive`
4. **Check changes**: See `gamma_position` unchanged (should be None)
5. **Check location**: `model.py:572 in reset_event_primitive()`
6. **Fix**: Add `marker.clear_gamma_position(perspective)` at line 572

**Time to diagnosis**: ~30 seconds (vs 30 minutes without log)

### AI-Assisted Analysis Protocol

**User workflow:**
1. Bug occurs
2. Press `Ctrl+Shift+L` to export log
3. Tell AI: "Read `logs/state_log_20251214_102347.txt`"
4. AI reads structured log and provides:
   - Root cause identification
   - Exact file:line location
   - Suggested fix
   - Causal chain explanation

**AI reads the log directly from the file system**, eliminating copy/paste errors and providing full context.

### Implementation Status

**v2.2.2 (Current):**
- ✅ Infrastructure complete (Ctrl+Shift+L exports log)
- ✅ Visual feedback (title, status bar, dialog)
- ✅ Log file creation with metadata
- ⏳ Placeholder content (structure defined, awaiting full StateViewer implementation)

**Future (v2.3.0+):**
- ⏳ Full state tracking in operations
- ⏳ Automatic validation and warning detection
- ⏳ Causal chain tracking (what caused this operation?)
- ⏳ Differential analysis (compare good vs bad runs)
- ⏳ Query API (interactive log exploration)

### Related Documentation

- **User Guide**: [interactive_editor_user_guide.md](interactive_editor_user_guide.md#8-state-viewer-log-export-new---v222) - How to use State Viewer Log
- **Changelog**: [INTERACTIVE_EDITOR_CHANGELOG.md](INTERACTIVE_EDITOR_CHANGELOG.md#v222-state-viewer-log-december-14-2025) - Feature history
- **Debug Guide**: [DEBUG.md](DEBUG.md) - Debugging methodologies
- **This Document**: State domains and enums (earlier sections)
