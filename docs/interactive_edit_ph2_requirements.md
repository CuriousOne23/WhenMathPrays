# Interactive Editor - Phase 2 Requirements

**Status:** PLANNING  
**Target:** Post Phase 1 completion  
**Estimated Effort:** 6-8 hours  
**Last Updated:** December 6, 2025

---

## Phase 2 Overview

Phase 2 adds critical functionality for more complex editing scenarios:
- Add/delete time points (event insertion/removal)
- Inverse editing (drag gamma_self to suggest primitives)
- Manual marker management (add/remove markers without dragging)
- Improved undo/redo system

---

## 1. Add/Delete Time Points

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

### Phase 2.1: Add/Delete Events (2-3 hours)
- Event insertion with interpolation
- Event deletion with validation
- UI controls and keyboard shortcuts
- Update save/load to handle dynamic event lists

### Phase 2.2: Inverse Editing (3-4 hours)
- Mode toggle UI
- Inverse heuristic implementation
- Suggestion dialog with preview
- Visual feedback (dashed lines, preview trajectory)

### Phase 2.3: Marker Management (1 hour)
- Manual marker add/remove
- Marker style picker dialog
- Update marker persistence in CSV

### Phase 2.4: Undo/Redo (1-2 hours)
- Undo stack implementation
- Action classes for different edit types
- UI controls and status indicators
- Keyboard shortcuts

---

## Success Criteria

Phase 2 is complete when:
- ✅ User can insert new events via Shift+Click
- ✅ User can delete unlocked events via Delete key
- ✅ User can drag gamma_self points and accept primitive suggestions
- ✅ Inverse mode provides reasonable primitive estimates (within ±2 of manual tuning)
- ✅ User can manually add/remove markers without editing values
- ✅ Undo/Redo works for all action types
- ✅ All features have keyboard shortcuts
- ✅ No regressions in Phase 1 functionality
- ✅ Modified CSVs load correctly in Phase 1 editor (backward compatible)

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
