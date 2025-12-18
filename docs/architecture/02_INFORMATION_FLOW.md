# Information Flow

**Purpose**: Document all message paths through the system. Every component interaction must be traceable through these sequences.

## Architecture Overview

```
┌─────────────────┐
│  User Actions   │
└────────┬────────┘
         │
         v
┌─────────────────────────────────────────────────┐
│              Interactive UI                     │
│  ┌──────────────┐         ┌─────────────────┐  │
│  │ Primitive    │         │  Trajectory     │  │
│  │ Panel        │         │  Panel          │  │
│  │ (5 subplots) │         │  (gamma_self)   │  │
│  └──────┬───────┘         └─────────────────┘  │
│         │                                        │
│         │ callbacks                              │
│         v                                        │
│  ┌─────────────────────────────────┐            │
│  │     EditorController             │            │
│  │  (Single Mediator)               │            │
│  └──────┬──────────────────┬───────┘            │
│         │                  │                     │
│         │                  │ commands            │
│         v                  v                     │
│  ┌──────────────┐   ┌─────────────────┐         │
│  │ EditorModel  │   │  Panels          │         │
│  │ (Ground      │   │  (View Update)   │         │
│  │  Truth)      │   │                  │         │
│  └──────────────┘   └─────────────────┘         │
└─────────────────────────────────────────────────┘
```

## Message Sequences

### Sequence 1: Edit Primitive Value (Current - BROKEN)

**User Action**: Drags marker for event 5, primitive 'r' to new value 0.85

```
User
  │
  │ drag
  v
DraggablePoint (event 5, 'r')
  │
  │ on_primitive_value_changed(5, 'r', 0.85)
  v
EditorController
  │
  │ update_event(5, {'r': 0.85})
  v
EditorModel
  │
  │ events[5]['r'] = 0.85
  │ modified_events[5].add('r')
  │
  │ (returns)
  v
EditorController
  │
  │ ❌ PROBLEM: Loses context - knows "something changed"
  │             but rebuilds everything
  │
  │ primitive_panel.display_primitives()
  v
PrimitivePanel
  │
  │ ❌ Destroys all 50 DraggablePoint objects
  │ ❌ Recreates all 50 DraggablePoint objects
  │ ❌ 200-500ms rebuild time
  │
  v
User sees update (slowly)
```

**Problem**: Information flow loses context. Controller knows specific change but Panel gets "rebuild all" command.

---

### Sequence 2: Edit Primitive Value (Target - FIXED)

**User Action**: Drags marker for event 5, primitive 'r' to new value 0.85

```
User
  │
  │ drag
  v
DraggablePoint (event 5, 'r')
  │
  │ on_primitive_value_changed(5, 'r', 0.85)
  v
EditorController
  │
  │ model.update_event(5, {'r': 0.85})
  v
EditorModel
  │
  │ events[5]['r'] = 0.85
  │ modified_events[5].add('r')
  │ (returns updated value, modified status)
  │
  v
EditorController
  │
  │ ✅ Preserves context - knows exactly what changed
  │
  │ primitive_panel.update_marker(5, 'r', 0.85, is_modified=True)
  v
PrimitivePanel
  │
  │ marker = _markers[(5, 'r')]
  │ marker.update_position(0.85)
  │ marker.set_modified(True)
  │ ✅ Updates only one marker
  │ ✅ <50ms update time
  │
  v
User sees update (instantly)
```

**Solution**: Information flow preserves context. Controller sends specific update command, Panel applies incremental change.

---

### Sequence 3: Reset Primitive to Baseline (Current - BROKEN)

**User Action**: Double-clicks marker for event 5, primitive 'r'

```
User
  │
  │ double-click
  v
DraggablePoint (event 5, 'r')
  │
  │ on_double_click()
  │ global _double_click_armed ❌ (hidden side channel)
  │
  │ on_primitive_reset(5, 'r')
  v
EditorController
  │
  │ model.reset_event_primitive(5, 'r')
  v
EditorModel
  │
  │ events[5]['r'] = baseline_events[5]['r']
  │ modified_events[5].discard('r')
  │
  v
EditorController
  │
  │ primitive_panel.display_primitives()
  v
PrimitivePanel
  │
  │ ❌ Full rebuild (200-500ms)
  │
  v
User sees reset (slowly)
```

**Problems**:
1. Global `_double_click_armed` bypasses Controller (violates P2: Mediator)
2. Full rebuild after reset (violates P3: Incremental Updates)

---

### Sequence 4: Reset Primitive to Baseline (Target - FIXED)

**User Action**: Double-clicks marker for event 5, primitive 'r'

```
User
  │
  │ double-click
  v
DraggablePoint (event 5, 'r')
  │
  │ (internal state machine)
  │ click_count: 0 → 1 → 2
  │ state: idle → armed → trigger
  │
  │ on_primitive_reset(5, 'r')
  v
EditorController
  │
  │ baseline = model.get_baseline_value(5, 'r')
  │ model.update_event(5, {'r': baseline})
  v
EditorModel
  │
  │ events[5]['r'] = baseline_events[5]['r']
  │ modified_events[5].discard('r')
  │ (returns baseline value, modified=False)
  │
  v
EditorController
  │
  │ primitive_panel.update_marker(5, 'r', baseline, is_modified=False)
  v
PrimitivePanel
  │
  │ marker = _markers[(5, 'r')]
  │ marker.update_position(baseline)
  │ marker.set_modified(False)
  │ marker.reset_double_click_state()
  │ ✅ <50ms update
  │
  v
User sees reset (instantly)
```

**Solutions**:
1. Double-click state managed within DraggablePoint (no global variable)
2. Incremental marker update (no rebuild)
3. All communication through Controller

---

### Sequence 5: Context-Aware Zoom

**User Action**: Scroll wheel while mouse over 'r' subplot

```
User
  │
  │ scroll wheel (over 'r' axes)
  v
PrimitivePanel
  │
  │ on_scroll(event)
  │ identifies: axes = 'r' subplot
  │ stores: last_mouse_axes = axes
  │
  │ (toolbar button clicked by user)
  v
InteractiveEditor (MainWindow)
  │
  │ _handle_zoom_in()
  │ target = primitive_panel.last_mouse_axes
  │ primitive_panel.zoom_in(target_axes=target)
  v
PrimitivePanel
  │
  │ if target_axes == specific subplot:
  │     zoom that subplot's y-axis
  │ else:
  │     zoom all subplots
  │
  v
User sees zoom (only 'r' subplot)
```

**Note**: This sequence correctly preserves context through the call chain.

---

### Sequence 6: Save File (Multi-Step)

**User Action**: Clicks Save button

```
User
  │
  │ save button
  v
InteractiveEditor (MainWindow)
  │
  │ controller.save()
  v
EditorController
  │
  │ (1) Query Model for modified events
  │ modified = model.get_modified_events()
  │
  │ (2) If no changes, done
  │ if not modified: return
  │
  │ (3) Get complete state
  │ all_events = model.get_all_events()
  │
  │ (4) Write to file
  │ save_to_csv(filepath, all_events)
  │
  │ (5) Update Model baseline
  │ model.set_baseline(all_events)
  │
  │ (6) Update UI
  │ primitive_panel.clear_all_modified_markers()
  │
  v
PrimitivePanel
  │
  │ for (event_idx, prim) in _markers:
  │     marker.set_modified(False)
  │
  v
User sees "Saved" notification
```

**Note**: Multi-step sequence with clear query/command separation.

---

## Communication Pipelines

### Panel → Controller (Events)

All callbacks flow from Panel to Controller:

| Callback | Sender | Purpose | Parameters |
|----------|--------|---------|------------|
| `on_primitive_value_changed` | PrimitivePanel | User dragged marker | `(event_idx, prim, value)` |
| `on_primitive_reset` | PrimitivePanel | User double-clicked | `(event_idx, prim)` |
| `on_event_selected` | PrimitivePanel | User clicked marker | `(event_idx)` |

**Contract**: Callbacks are notifications only. Panel must not wait for response or assume outcome.

---

### Controller → Panel (Commands)

All updates flow from Controller to Panel:

| Command | Receiver | Purpose | Parameters |
|---------|----------|---------|------------|
| `update_marker` | PrimitivePanel | Update single marker | `(event_idx, prim, value, is_modified)` |
| `display_primitives` | PrimitivePanel | Full rebuild (rare) | `()` |
| `set_selection` | PrimitivePanel | Highlight marker | `(event_idx)` |
| `update_trajectory` | TrajectoryPanel | Replot trajectory | `()` |

**Contract**: Commands are imperative. Panel must execute and complete before returning.

---

### Controller → Model (Queries)

Controller queries Model for ground truth:

| Query | Purpose | Returns |
|-------|---------|---------|
| `get_event(idx)` | Get single event | `dict` |
| `get_all_events()` | Get all events | `list[dict]` |
| `is_modified(idx, prim)` | Check modified status | `bool` |
| `get_baseline_value(idx, prim)` | Get original value | `float` |
| `get_modified_events()` | Get dirty set | `set[int]` |

**Contract**: Queries are read-only. Must not modify Model state.

---

### Controller → Model (Commands)

Controller updates Model state:

| Command | Purpose | Effect |
|---------|---------|--------|
| `update_event(idx, changes)` | Modify event | Updates `events[idx]`, marks modified |
| `set_baseline(events)` | Reset baseline after save | Updates `baseline_events` |
| `reset_event(idx)` | Reset all primitives | Copies baseline to current |

**Contract**: Commands modify state atomically. Must not fail partially.

---

## Anti-Patterns to Avoid

### ❌ Direct Panel-to-Panel Communication
```python
# WRONG: PrimitivePanel directly updates TrajectoryPanel
class PrimitivePanel:
    def on_change(self):
        self.trajectory_panel.update()  # ❌ Violates P2
```

```python
# RIGHT: Route through Controller
class PrimitivePanel:
    def on_change(self):
        self.controller.on_primitive_changed(...)

class EditorController:
    def on_primitive_changed(self, ...):
        self.trajectory_panel.update()  # ✅
```

---

### ❌ Global Shared State
```python
# WRONG: Global variable for communication
_double_click_armed = False  # ❌ Violates P2, P7

class DraggablePoint:
    def on_click(self):
        global _double_click_armed
        _double_click_armed = True
```

```python
# RIGHT: State managed locally
class DraggablePoint:
    def __init__(self):
        self._click_count = 0  # ✅ Local state
    
    def on_click(self):
        self._click_count += 1
        if self._click_count == 2:
            self.on_reset()
```

---

### ❌ Lossy Information Flow
```python
# WRONG: Losing context in Controller
class EditorController:
    def on_primitive_changed(self, idx, prim, value):
        self.model.update(idx, prim, value)
        self.panel.display_primitives()  # ❌ Lost context
```

```python
# RIGHT: Preserving context
class EditorController:
    def on_primitive_changed(self, idx, prim, value):
        self.model.update(idx, prim, value)
        is_modified = self.model.is_modified(idx, prim)
        self.panel.update_marker(idx, prim, value, is_modified)  # ✅
```

---

## Debugging Information Flow

### How to Trace a Message

1. **Add logging at Controller boundaries**:
```python
class EditorController:
    def on_primitive_value_changed(self, idx, prim, value):
        logger.debug(f"RX: on_primitive_value_changed({idx}, {prim}, {value})")
        # ... process ...
        logger.debug(f"TX: update_marker({idx}, {prim}, {value}, {is_modified})")
```

2. **Verify sequence matches documentation**:
   - Does actual flow match diagram above?
   - Are there unexpected calls?
   - Is order correct?

3. **Check for shortcuts**:
   - Any direct Panel-to-Panel calls?
   - Any global variables changing?
   - Any "magical" synchronization?

---

**Last Updated**: 2025-12-06  
**Status**: Current flow documented (broken), target flow designed (not yet implemented)
