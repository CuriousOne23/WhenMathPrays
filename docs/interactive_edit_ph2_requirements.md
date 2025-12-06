# Interactive Editor - Phase 2 Requirements

**Status:** PLANNING  
**Target:** Post Phase 1 completion  
**Estimated Effort:** 12-15.5 hours  
**Last Updated:** December 6, 2025

---

## Phase 2 Overview

Phase 2 migrates to a modern UI framework and adds critical functionality for more complex editing scenarios:
- **PySide6 migration** (professional UI foundation)
- **Edit initial state (gamma_self0)** and fractional time support
- Add/delete time points (event insertion/removal)
- Inverse editing (drag gamma_self to suggest primitives)
- Manual marker management (add/remove markers without dragging)
- Enhanced undo/redo system with QUndoStack

---

## Phase 2.0: PySide6 Migration (Foundation)

### Why Migrate from Matplotlib/Tkinter?

**Current Phase 1 Architecture:**
- Matplotlib for all visualization
- Tkinter only for file dialogs
- Matplotlib event handlers (`mpl_connect`) for mouse/keyboard

**Limitations for Phase 2:**
- No native dialog system (inverse mode acceptance dialog would be clunky)
- No built-in undo/redo stack
- Tkinter dialogs look dated (1990s aesthetics)
- Hard to add professional UI chrome (toolbars, status bars, menus)

**PySide6 Advantages:**
- ✅ **LGPL license** (permissive, commercial-friendly)
- ✅ **Official Qt for Python** (maintained by Qt Company)
- ✅ **Built-in QUndoStack** (undo/redo for free)
- ✅ **Native widgets** (QSpinBox, QDialog, QFileDialog, QStatusBar)
- ✅ **Matplotlib integration** via `FigureCanvasQTAgg` (seamless)
- ✅ **Professional appearance** (native OS look and feel)
- ✅ **Future-proof** for Phase 3+ (dual perspective, side-by-side panels)

### Migration Strategy

**Good news:** Phase 1 architecture already has clean MVC separation!
- Model (`tools/editor/model.py`) - unchanged
- Controller (`tools/editor/controller.py`) - minimal changes
- Views (`tools/editor/views/*.py`) - wrap in Qt, matplotlib stays

**What changes:**
1. Matplotlib figures embedded in QMainWindow via FigureCanvasQTAgg
2. Replace tkinter file dialog → QFileDialog
3. Add Qt window chrome (toolbar, status bar)
4. Matplotlib events auto-handled by Qt canvas
5. Add QUndoStack for Phase 2.4

**What stays the same:**
- All GRP computation logic (model, controller)
- Matplotlib plotting code (primitives, trajectory)
- Draggable point mechanics
- CSV loading/saving

### Implementation Steps

#### Step 1: Add PySide6 Dependency

**Update `requirements.txt`:**
```pip-requirements
numpy
matplotlib
pandas
pytest
PySide6
```

**Install:**
```bash
pip install PySide6
```

#### Step 2: Create Qt Main Window

**New file: `tools/editor/qt_window.py`**
```python
"""
Qt main window wrapper for interactive editor.
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QToolBar, 
    QStatusBar, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence, QUndoStack
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.pyplot as plt


class EditorMainWindow(QMainWindow):
    """
    Main window for interactive scenario editor.
    
    Embeds matplotlib figures in Qt framework with native
    toolbars, menus, and status bar.
    """
    
    def __init__(self, csv_file):
        super().__init__()
        self.csv_file = csv_file
        self.setWindowTitle(f'Interactive Scenario Editor - {csv_file.name}')
        self.setGeometry(100, 100, 1400, 800)
        
        # Create matplotlib figure (same as Phase 1)
        self.fig = plt.figure(figsize=(14, 8))
        
        # Embed in Qt canvas
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.setCentralWidget(self.canvas)
        
        # Add toolbar
        self._setup_toolbar()
        
        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')
        
        # Undo stack (for Phase 2.4)
        self.undo_stack = QUndoStack(self)
    
    def _setup_toolbar(self):
        """Create toolbar with common actions."""
        toolbar = QToolBar('Main Toolbar')
        self.addToolBar(toolbar)
        
        # Save action
        save_action = QAction('Save', self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self._on_save)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Undo/Redo (Phase 2.4)
        undo_action = self.undo_stack.createUndoAction(self, 'Undo')
        undo_action.setShortcut(QKeySequence.Undo)
        toolbar.addAction(undo_action)
        
        redo_action = self.undo_stack.createRedoAction(self, 'Redo')
        redo_action.setShortcut(QKeySequence.Redo)
        toolbar.addAction(redo_action)
    
    def _on_save(self):
        """Save current scenario (Qt file dialog)."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            'Save Scenario',
            str(self.csv_file),
            'CSV Files (*.csv);;All Files (*)'
        )
        if file_path:
            self.save_callback(file_path)
            self.status_bar.showMessage(f'Saved: {file_path}', 3000)
    
    def show_message(self, message, level='info'):
        """Show message in status bar or dialog."""
        if level == 'info':
            self.status_bar.showMessage(message, 5000)
        elif level == 'warning':
            QMessageBox.warning(self, 'Warning', message)
        elif level == 'error':
            QMessageBox.critical(self, 'Error', message)
```

#### Step 3: Update `interactive_editor.py`

**Replace matplotlib figure creation:**
```python
# OLD (Phase 1):
self.fig = plt.figure(figsize=(14, 8))

# NEW (Phase 2):
from PySide6.QtWidgets import QApplication
from tools.editor.qt_window import EditorMainWindow

app = QApplication(sys.argv)
window = EditorMainWindow(self.csv_file)
self.fig = window.fig  # Use figure from Qt window
```

**Replace file dialog:**
```python
# OLD (Phase 1):
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
file_path = filedialog.asksaveasfilename(...)

# NEW (Phase 2):
# Already handled by EditorMainWindow._on_save()
```

**Update event loop:**
```python
# OLD (Phase 1):
plt.show()

# NEW (Phase 2):
window.show()
sys.exit(app.exec())
```

#### Step 4: Test Migration

**Smoke Tests:**
1. ✅ Editor launches with Qt window chrome
2. ✅ Matplotlib plots render correctly in Qt canvas
3. ✅ Mouse drag on primitives still works
4. ✅ Keyboard shortcuts still work (or re-map to Qt shortcuts)
5. ✅ Save dialog is native Qt dialog
6. ✅ Status bar shows messages
7. ✅ Window resizes correctly

**Cross-platform:**
- Windows: Native Windows 11 theme
- macOS: Native macOS theme
- Linux: Native theme (KDE/GNOME)

### Effort Estimate: 4-6 hours

**Breakdown:**
- Dependency setup: 15 min
- Qt window wrapper: 2 hours
- Update interactive_editor.py: 1 hour
- Test and debug: 1-2 hours
- Documentation: 30 min

---

## Phase 2.1: Add/Delete Events + Edit gamma_self0 + Fractional Time

### Feature: Edit Initial State (gamma_self0)

**Purpose:**
- Allow users to change starting position in gamma-space without editing CSV
- Enables sensitivity analysis: "What if this person started more negative?"
- Useful for comparing same event sequence from different initial conditions

**What is gamma_self0:**
- Complex number representing initial relational state: `gamma_self0 = real + imag*j`
- Real axis: Ego (negative) ↔ We (positive)
- Imaginary axis: Hate (negative) ↔ Love (positive)
- Examples:
  - Narcissist: `(-3, -2)` in Quadrant 3
  - Saint: `(2, 3)` in Quadrant 1
  - Buddha: `(0, 0)` at origin
  - Wounded: `(-2, 1)` in Quadrant 2

**UI Design:**

**Location:** Control panel area (add to Qt window as dockable widget)

```
┌──────────────────────────────────────┐
│ Initial State (γ_self0)              │
├──────────────────────────────────────┤
│ Real (Ego↔We):  [  0.00  ] ←→       │
│ Imag (Hate↔Love): [  0.00  ] i ↑↓   │
│                                      │
│ [Apply]  [Reset to CSV Default]     │
└──────────────────────────────────────┘
```

**Implementation:**
```python
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QDoubleSpinBox, QPushButton
)

class GammaSelf0Editor(QWidget):
    """Widget for editing initial gamma_self state."""
    
    def __init__(self, model, controller):
        super().__init__()
        self.model = model
        self.controller = controller
        
        layout = QVBoxLayout()
        
        # Real component
        real_layout = QHBoxLayout()
        real_layout.addWidget(QLabel('Real (Ego↔We):'))
        self.real_spinbox = QDoubleSpinBox()
        self.real_spinbox.setRange(-10.0, 10.0)
        self.real_spinbox.setSingleStep(0.1)
        self.real_spinbox.setValue(self.model.gamma_self0.real)
        real_layout.addWidget(self.real_spinbox)
        layout.addLayout(real_layout)
        
        # Imaginary component
        imag_layout = QHBoxLayout()
        imag_layout.addWidget(QLabel('Imag (Hate↔Love):'))
        self.imag_spinbox = QDoubleSpinBox()
        self.imag_spinbox.setRange(-10.0, 10.0)
        self.imag_spinbox.setSingleStep(0.1)
        self.imag_spinbox.setValue(self.model.gamma_self0.imag)
        imag_layout.addWidget(self.imag_spinbox)
        layout.addLayout(imag_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        apply_btn = QPushButton('Apply')
        apply_btn.clicked.connect(self._on_apply)
        reset_btn = QPushButton('Reset to CSV Default')
        reset_btn.clicked.connect(self._on_reset)
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(reset_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _on_apply(self):
        """Apply new gamma_self0 and recompute trajectory."""
        new_gamma_self0 = complex(
            self.real_spinbox.value(),
            self.imag_spinbox.value()
        )
        self.model.gamma_self0 = new_gamma_self0
        self.model.gamma_self0_modified = True
        self.controller.recompute_trajectory()
        self.controller.trajectory_panel.update_start_marker(new_gamma_self0)
    
    def _on_reset(self):
        """Reset to original CSV value."""
        self.model.gamma_self0 = self.model.gamma_self0_original
        self.model.gamma_self0_modified = False
        self.real_spinbox.setValue(self.model.gamma_self0.real)
        self.imag_spinbox.setValue(self.model.gamma_self0.imag)
        self.controller.recompute_trajectory()
        self.controller.trajectory_panel.update_start_marker(self.model.gamma_self0)
```

**Visual Feedback:**
- Original gamma_self0 from CSV: **Blue square** marker
- Modified gamma_self0: **Orange square** marker
- Tooltip shows: "γ_self0: (2.5, -1.0) [Modified]"

**Save Behavior:**
- Prompt user: "Save modified initial state?" with checkbox
- If yes, write `gamma_self_0,2.5-1.0j` to CSV metadata

---

### Feature: Fractional Time Support

**Current Limitation:**
- CSV `day` column expects integers: `0, 1, 2, 3, ...`
- But `time_unit` can be `days`, `weeks`, `months`, `years`
- Can't represent "2.5 days" or "1.75 weeks"

**Good News: Already Mostly Works!**
- Pandas `read_csv` handles floats automatically
- Matplotlib plots fractional x-coordinates
- GRP computation uses float arithmetic

**What Needs to Change:**

#### 1. Event Insertion (Shift+Click)
```python
def on_shift_click_timeline(self, time_value):
    """
    Insert new event at specified time.
    
    Phase 1: Snaps to integer
    Phase 2: Allows fractional time
    """
    # OLD:
    # time_value = int(round(time_value))
    
    # NEW:
    time_value = round(time_value, 2)  # 2 decimal places
    
    # Validate minimum spacing
    MIN_SPACING = 0.1
    for existing_time in self.events_time:
        if abs(existing_time - time_value) < MIN_SPACING:
            self.show_error(
                f"Too close to event at t={existing_time}. "
                f"Min spacing: {MIN_SPACING} {self.time_unit}"
            )
            return
    
    # Rest of insertion logic...
```

#### 2. Display Formatting
```python
def format_time_label(self, time_value):
    """
    Format time value for display.
    
    - Integers: "Day 5"
    - Fractional: "Day 5.5" or "Day 5.25"
    """
    unit_singular = self.time_unit.rstrip('s')  # 'days' -> 'day'
    
    if time_value == int(time_value):
        return f"{unit_singular.capitalize()} {int(time_value)}"
    else:
        return f"{unit_singular.capitalize()} {time_value:.2f}"
```

#### 3. Time Axis Formatting
```python
# In trajectory/primitive panel setup:
import matplotlib.ticker as ticker

ax.xaxis.set_major_formatter(
    ticker.FormatStrFormatter('%.1f')  # Show 1 decimal place
)
```

**Examples:**
```csv
day,v,r,f,a,S,notes
0.0,5,5,0,0,5,First meeting
2.5,8,7,3,2,6,Great afternoon date
2.8,-3,-4,0,0,-5,Argument same evening
5.25,6,5,4,3,4,Reconciliation lunch
```

**Edge Cases:**
- Very small fractions (< 0.01): Round to 2 decimals
- Integer-only CSVs: Still work (2.0 displays as "Day 2")
- Mixed precision: Some integer, some fractional - no problem

**Backward Compatibility:**
- Phase 1 editor already handles floats (just reads as numbers)
- No breaking changes

### Effort Estimate: 3-4 hours

**Breakdown:**
- gamma_self0 editor widget: 1.5 hours
- Fractional time validation/formatting: 1 hour
- Integration testing: 1 hour
- Documentation: 30 min

---

## 2. Add/Delete Time Points (continued)

### Feature: Insert New Events

**User Interaction:**
- **Shift+Click** on time axis → Insert new event at that time
- Dialog prompts for initial primitive values (or interpolate from neighbors)
- New event automatically unlocked (can be edited)
- New event gets auto-marker if values modified from interpolated defaults

**Implementation:**
```python
def on_shift_click_timeline(self, time_value):
    """Insert new event at specified time."""
    # Find insertion index
    idx = bisect.bisect_left(self.events_time, time_value)
    
    # Interpolate primitive values from neighbors
    if 0 < idx < len(self.events_time):
        prev_event = self.events[idx-1]
        next_event = self.events[idx]
        t_frac = (time_value - self.events_time[idx-1]) / \
                 (self.events_time[idx] - self.events_time[idx-1])
        new_primitives = interpolate(prev_event, next_event, t_frac)
    else:
        # Edge case: default to zeros or copy nearest
        new_primitives = {'v': 0, 'r': 0, 'f': 0, 'a': 0, 'S': 0}
    
    # Create new event
    new_event = Event(
        step=time_value,
        primitives=new_primitives,
        notes=f"Inserted at t={time_value}",
        marker="",
        locked=False
    )
    
    # Insert into model
    self.model.insert_event(idx, new_event)
    
    # Refresh UI
    self.refresh_all_panels()
```

**Constraints:**
- Cannot insert at existing event time (show error message)
- Minimum spacing: 1 time unit between events (configurable)
- Maximum events: 200 (performance limit)

### Feature: Delete Events

**User Interaction:**
- **Select event** (click on marker) + **Delete key** → Remove event
- Only unlocked events can be deleted
- Confirmation dialog if event has notes or is marked
- Cannot delete if <2 events remain (minimum scenario length)

**Implementation:**
```python
def on_delete_key(self):
    """Delete selected event if unlocked."""
    if self.selected_event is None:
        return
    
    event = self.model.get_event(self.selected_event_idx)
    
    if event.locked:
        show_error("Cannot delete locked event. Unlock first.")
        return
    
    if len(self.model.events) <= 2:
        show_error("Cannot delete. Minimum 2 events required.")
        return
    
    # Confirm if event has data
    if event.marker or event.notes:
        if not confirm_dialog(f"Delete event at t={event.step}?"):
            return
    
    # Remove from model
    self.model.delete_event(self.selected_event_idx)
    
    # Clear selection
    self.selected_event_idx = None
    
    # Refresh UI
    self.refresh_all_panels()
```

---

## 2. Inverse Editing (Gamma_Self → Primitives)

### Feature: Drag Trajectory to Suggest Primitives

**Concept:**
- User drags a gamma_self point to new location
- System suggests primitive changes that would move trajectory closer to target
- User reviews suggestions and accepts/rejects

**Challenge:**
- **One trajectory point ≠ unique primitive values**
- Multiple primitive combinations can produce same gamma_self
- Solution: Heuristic estimation with visual feedback

**User Interaction:**
1. Toggle mode: **[Forward Mode]** ⇄ **[Inverse Mode]** (button or 'I' key)
2. In inverse mode, click and drag gamma_self marker
3. Dashed lines show suggested primitive changes (preview)
4. Release mouse → "Accept Suggestions?" dialog
5. Accept → Apply primitive changes, recompute trajectory
6. Reject → Revert to original position

### Inverse Estimation Heuristic

**Strategy: Even distribution across primitives**

```python
def suggest_primitives_for_target(current_gamma, target_gamma, event_idx):
    """
    Suggest primitive changes to move from current_gamma to target_gamma.
    
    Uses weighted distribution based on GRP weights.
    """
    delta = target_gamma - current_gamma
    
    # Get current weights from model
    weights = self.model.weights
    
    # Real axis (Ego ↔ We): v and S contribute
    # Δγ_real = w_v*v + w_S*S*cos(θ_S)
    total_real_weight = weights['visibility'] + weights['soul'] * 0.7071  # Assume 45° angle
    v_delta = delta.real * (weights['visibility'] / total_real_weight)
    S_real_delta = delta.real * (weights['soul'] * 0.7071 / total_real_weight)
    
    # Imaginary axis (Hate ↔ Love): r, f, a, S contribute  
    # Δγ_imag = w_r*r + w_f*f + w_a*a + w_S*S*sin(θ_S)
    total_imag_weight = (weights['resonance'] + weights['fidelity'] + 
                         weights['altruism'] + weights['soul'] * 0.7071)
    r_delta = delta.imag * (weights['resonance'] / total_imag_weight)
    f_delta = delta.imag * (weights['fidelity'] / total_imag_weight)
    a_delta = delta.imag * (weights['altruism'] / total_imag_weight)
    S_imag_delta = delta.imag * (weights['soul'] * 0.7071 / total_imag_weight)
    
    # Combine S contributions
    S_delta = (S_real_delta + S_imag_delta) / 2
    
    # Get current primitive values
    event = self.model.events[event_idx]
    
    # Calculate suggestions (clamped to [-10, +10])
    suggestions = {
        'v': clamp(event.primitives['v'] + v_delta, -10, 10),
        'r': clamp(event.primitives['r'] + r_delta, -10, 10),
        'f': clamp(event.primitives['f'] + f_delta, -10, 10),
        'a': clamp(event.primitives['a'] + a_delta, -10, 10),
        'S': clamp(event.primitives['S'] + S_delta, -10, 10)
    }
    
    return suggestions
```

**Visual Feedback:**
- Original primitives: Solid circles
- Suggested primitives: Hollow circles with dashed connector lines
- Trajectory preview: Dashed line showing where it would go if accepted
- Color coding: Green if improvement, yellow if ambiguous, red if worsens

**Acceptance Dialog:**
```
┌──────────────────────────────────────────────┐
│ Suggested Primitive Changes (Event 15)      │
├──────────────────────────────────────────────┤
│ Visibility (v):  5.0 → 6.2  (+1.2)          │
│ Resonance (r):   3.0 → 4.5  (+1.5)          │
│ Fidelity (f):    4.0 → 4.0  (no change)     │
│ Altruism (a):    3.0 → 4.1  (+1.1)          │
│ Soul (S):        2.0 → 2.8  (+0.8)          │
├──────────────────────────────────────────────┤
│ Trajectory Impact:                           │
│ • Distance to target: 2.3 → 0.4 (improved)  │
│                                              │
│ [Accept]  [Modify]  [Cancel]                │
└──────────────────────────────────────────────┘
```

**Modify Option:**
- Opens mini-editor to manually adjust suggested values
- Real-time preview of trajectory with adjustments
- Apply when satisfied

---

## 3. Manual Marker Management

### Feature: Add/Remove Markers Without Editing

**Current Behavior (Phase 1):**
- Markers auto-added when primitive is dragged
- No way to manually add marker without editing value
- No way to remove marker from edited point

**Phase 2 Enhancements:**

**Add Marker:**
- **Ctrl+M** on selected event → Add marker (even if not edited)
- Use case: Mark important events for reference (e.g., "therapy session")
- Marker style: User selectable (circle, star, square, triangle)

**Remove Marker:**
- **Ctrl+Shift+M** on selected event → Remove marker
- Use case: Clean up after testing, remove accidental marks
- Confirmation if event was actually edited

**Marker Styles:**
- Circle (default for auto-markers)
- Star (high importance)
- Square (anchor point)
- Triangle (experimental)
- Diamond (validated)

**Implementation:**
```python
def on_ctrl_m(self):
    """Add marker to selected event."""
    if self.selected_event_idx is None:
        return
    
    event = self.model.events[self.selected_event_idx]
    
    # Show marker style picker
    style = show_marker_picker_dialog()  # circle, star, square, etc.
    
    event.marker = style
    self.model.mark_modified()
    self.refresh_primitives_panel()

def on_ctrl_shift_m(self):
    """Remove marker from selected event."""
    if self.selected_event_idx is None:
        return
    
    event = self.model.events[self.selected_event_idx]
    
    if not event.marker:
        show_info("No marker to remove.")
        return
    
    # Warn if event was actually edited
    if self.model.is_event_modified(self.selected_event_idx):
        if not confirm_dialog("Event was edited. Remove marker anyway?"):
            return
    
    event.marker = ""
    self.model.mark_modified()
    self.refresh_primitives_panel()
```

---

## 4. Enhanced Undo/Redo System

### Current Limitation (Phase 1):
- Only "Reset" button (reverts all changes)
- No granular undo for individual edits
- No redo functionality

### Phase 2 Improvements:

**Multi-Level Undo Stack:**
- **Ctrl+Z** → Undo last action
- **Ctrl+Y** or **Ctrl+Shift+Z** → Redo
- Stack depth: 50 actions (configurable)
- Actions tracked:
  - Primitive value changes
  - Lock/unlock toggles
  - Add/delete events
  - Marker add/remove

**Implementation:**
```python
class UndoStack:
    def __init__(self, max_depth=50):
        self.stack = []
        self.current_idx = -1
        self.max_depth = max_depth
    
    def push(self, action):
        """Add action to undo stack."""
        # Truncate future actions if in middle of stack
        self.stack = self.stack[:self.current_idx + 1]
        
        # Add new action
        self.stack.append(action)
        self.current_idx += 1
        
        # Limit stack depth
        if len(self.stack) > self.max_depth:
            self.stack.pop(0)
            self.current_idx -= 1
    
    def undo(self):
        """Undo last action and return it."""
        if self.current_idx < 0:
            return None
        
        action = self.stack[self.current_idx]
        self.current_idx -= 1
        return action
    
    def redo(self):
        """Redo next action and return it."""
        if self.current_idx >= len(self.stack) - 1:
            return None
        
        self.current_idx += 1
        return self.stack[self.current_idx]
    
    def can_undo(self):
        return self.current_idx >= 0
    
    def can_redo(self):
        return self.current_idx < len(self.stack) - 1

class Action:
    """Base class for undoable actions."""
    def undo(self, model):
        raise NotImplementedError
    
    def redo(self, model):
        raise NotImplementedError

class EditPrimitiveAction(Action):
    def __init__(self, event_idx, primitive, old_value, new_value):
        self.event_idx = event_idx
        self.primitive = primitive
        self.old_value = old_value
        self.new_value = new_value
    
    def undo(self, model):
        model.set_primitive(self.event_idx, self.primitive, self.old_value)
    
    def redo(self, model):
        model.set_primitive(self.event_idx, self.primitive, self.new_value)
```

**UI Indicators:**
- Undo/Redo buttons enabled/disabled based on stack state
- Status bar shows last action: "Edited event 15 visibility"
- Tooltip on Undo button: "Undo: Edit v at event 15"

---

## 5. Keyboard Shortcuts (Phase 2 Additions)

| Key | Action |
|-----|--------|
| **I** | Toggle Inverse Mode (gamma_self drag) |
| **Shift+Click** | Insert new event at time |
| **Delete** | Delete selected event (if unlocked) |
| **Ctrl+M** | Add marker to selected event |
| **Ctrl+Shift+M** | Remove marker from selected event |
| **Ctrl+Z** | Undo last action |
| **Ctrl+Y** | Redo last undone action |
| **Ctrl+Shift+Z** | Redo (alternate binding) |

---

## Testing Plan

### Unit Tests
- `test_insert_event()` - Verify event insertion at various positions
- `test_delete_event()` - Verify locked events cannot be deleted
- `test_inverse_heuristic()` - Validate primitive suggestions are within bounds
- `test_undo_redo()` - Verify stack operations and state consistency
- `test_marker_management()` - Verify add/remove marker operations

### Integration Tests
- Load CSV → Add event → Save → Reload → Verify persistence
- Edit primitive → Undo → Redo → Verify trajectory matches
- Drag gamma_self → Accept suggestions → Verify primitives updated
- Add marker manually → Lock event → Verify marker+lock persisted

### User Acceptance Tests
1. **Insert Event Workflow:**
   - Load scenario with 10 events
   - Shift+Click to insert event at t=15
   - Verify interpolated values reasonable
   - Edit new event, verify trajectory updates
   - Save and reload, verify event persists

2. **Inverse Editing Workflow:**
   - Toggle to inverse mode
   - Drag gamma_self point to new location
   - Review suggested primitive changes
   - Accept suggestions
   - Verify trajectory moves closer to target
   - Undo and verify revert

3. **Marker Management:**
   - Select event without marker
   - Ctrl+M to add star marker
   - Verify marker appears in CSV
   - Ctrl+Shift+M to remove marker
   - Verify marker removed from CSV

---

## Implementation Phases

### Phase 2.0: PySide6 Migration (4-6 hours) ← START HERE
- Add PySide6 dependency to requirements.txt
- Create Qt main window wrapper (EditorMainWindow)
- Embed matplotlib figures in Qt canvas
- Replace tkinter file dialog with QFileDialog
- Add toolbar with Save/Undo/Redo actions
- Add status bar for user feedback
- Test cross-platform (Windows/Mac/Linux)
- Update documentation

### Phase 2.1: Add/Delete Events + gamma_self0 + Fractional Time (3-4 hours)
- Edit gamma_self0 widget (QDoubleSpinBox for real/imag)
- Fractional time support (validation, formatting)
- Event insertion with interpolation (fractional positions)
- Event deletion with validation
- UI controls and keyboard shortcuts
- Update save/load to handle dynamic event lists

### Phase 2.2: Inverse Editing (3-4 hours)
- Mode toggle UI (Qt button or menu action)
- Inverse heuristic implementation
- Suggestion dialog with preview (QDialog with matplotlib preview)
- Visual feedback (dashed lines, preview trajectory)

### Phase 2.3: Marker Management (1 hour)
- Manual marker add/remove
- Marker style picker dialog (QDialog with radio buttons)
- Update marker persistence in CSV

### Phase 2.4: Enhanced Undo/Redo (30 min) ← EASY with Qt!
- Integrate QUndoStack (already created in Phase 2.0)
- Create QUndoCommand subclasses for edit types
- Connect to toolbar actions (already wired in Phase 2.0)
- Test undo/redo across all action types

---

## Success Criteria

Phase 2 is complete when:
- ✅ **Phase 2.0:** Editor runs in PySide6 with native Qt chrome
- ✅ **Phase 2.0:** Matplotlib plots render correctly in Qt canvas
- ✅ **Phase 2.0:** All Phase 1 features work unchanged (no regressions)
- ✅ **Phase 2.1:** User can edit gamma_self0 (real, imaginary components)
- ✅ **Phase 2.1:** Modified gamma_self0 shown with orange marker (vs blue)
- ✅ **Phase 2.1:** User can insert events at fractional times (e.g., 2.5 days)
- ✅ **Phase 2.1:** Time axis displays fractional labels correctly
- ✅ **Phase 2.1:** User can insert new events via Shift+Click (fractional times)
- ✅ **Phase 2.1:** User can delete unlocked events via Delete key
- ✅ **Phase 2.2:** User can drag gamma_self points and accept primitive suggestions
- ✅ **Phase 2.2:** Inverse mode provides reasonable primitive estimates (within ±2 of manual tuning)
- ✅ **Phase 2.3:** User can manually add/remove markers without editing values
- ✅ **Phase 2.4:** Undo/Redo works for all action types via QUndoStack
- ✅ **Phase 2.4:** Toolbar shows Undo/Redo button states (enabled/disabled)
- ✅ **All:** All features have keyboard shortcuts
- ✅ **All:** Modified CSVs (including fractional times, gamma_self0) load correctly in Phase 1 editor (backward compatible)

---

## Future Considerations (Phase 3+)

**Phase 3: Dual-Perspective Editing**
- Radio toggle: M1 ⇄ M2
- Side-by-side primitive panels
- Combined gamma_self display

**Phase 4: Advanced Features**
- Fill gaps (interpolation for unlocked points)
- Automated sensitivity analysis
- Zoom/pan on plots
- Animation/playback mode

**Phase 5: AI-Assisted Analysis**
- Natural language queries about trajectory impact
- Automated event ranking by influence
- Suggested primitive adjustments to reach target trajectory

---

*Document created December 6, 2025 - Ready for Phase 2 implementation*
