# Refactor: Incremental Updates Architecture

**Date**: 2025-12-06  
**Status**: ✅ COMPLETED  
**Trigger**: PySide6 migration exposed performance issues

---

## Implementation Summary

**Completion Date**: 2025-12-06  
**Result**: All performance targets met, architecture principles restored

### What Was Delivered
- ✅ Phase 1: Model query interface (`get_event`, `is_modified`, `get_baseline_value`, etc.)
- ✅ Phase 2: Persistent marker infrastructure with `update_marker()` method
- ✅ Phase 3: Controller incremental update path for all operations
- ✅ Thread-safe GUI updates using Qt's event loop
- ✅ Scroll wheel zoom and right-click pan navigation
- ✅ Instant label removal on double-click reset
- ✅ Preserved zoom state across trajectory updates

### Performance Results
- Edit operation: <50ms ✅ (was 200-500ms)
- Reset operation: <50ms ✅ (was 200-500ms)
- Label removal: Instant ✅ (was delayed until recomputation)
- Zoom preservation: Working ✅ (was resetting on every update)

---

## Problem Statement

### Symptoms
- Editing a single primitive takes 200-500ms (target: <50ms)
- Resetting a single primitive takes 200-500ms (target: <50ms)
- User perceives UI as "slow" and "laggy"
- Double-click state being lost intermittently

### Root Cause
**Full panel rebuilds on every operation**

Current flow when user edits event 5, primitive 'r':
1. User drags marker → `on_primitive_value_changed(5, 'r', 0.85)`
2. Controller updates Model: `model.update_event(5, {'r': 0.85})`
3. Controller **loses context**: knows "something changed" but not what
4. Controller rebuilds entire panel: `primitive_panel.display_primitives()`
5. Panel destroys all 50 DraggablePoint objects
6. Panel recreates all 50 DraggablePoint objects
7. 200-500ms later, user sees update

**Information flow is lossy**: Controller knows `(event_idx=5, prim='r', value=0.85)` but sends "rebuild everything" to Panel.

### Why This Matters
- **Performance**: O(n*m) operation when should be O(1)
- **Scaling**: At 1000 events, would take 4-10 seconds per edit (unusable)
- **State loss**: Destroying/recreating markers loses double-click arming state
- **Architecture smell**: Violates P3 (Incremental Updates), P4 (Persistent Objects), P7 (Observable Flow)

---

## Architectural Analysis

### Principle Violations

| Principle | Violated? | Evidence |
|-----------|-----------|----------|
| P1: Single Source of Truth | ⚠️ Partial | Model is authoritative, but Controller duplicates some logic |
| P2: Controller as Mediator | ❌ YES | Global `_double_click_armed` bypasses Controller |
| P3: Incremental Updates | ❌ YES | Full rebuilds on every edit |
| P4: Persistent Objects | ❌ YES | DraggablePoint objects recreated on every edit |
| P5: No Timing Dependencies | ⚠️ Partial | Fixed double-click, but was timing-based |
| P6: Explicit Contracts | ⚠️ Partial | Contracts not documented |
| P7: Observable Information Flow | ❌ YES | Global state, lossy communication |
| P8: Coordinate Systems | ⚠️ Partial | Transform logic scattered |

**Critical violations**: P2, P3, P4, P7

### Performance Impact

Current (50 events, 5 primitives = 250 markers):
- Edit: 200-500ms ❌ (target: <50ms)
- Marker creation: ~10ms each × 50 = 500ms
- Reset: 200-500ms ❌ (target: <50ms)

Projected (1000 events):
- Edit: 4000-10000ms ❌ (4-10 seconds, unusable)
- Marker creation: ~10ms each × 1000 = 10000ms

With incremental updates (1000 events):
- Edit: <50ms ✅ (O(1) marker update)
- Reset: <50ms ✅ (O(1) marker update)

---

## Solution Design

### Target Architecture

**Information flow preserves context**:

1. User drags marker → `on_primitive_value_changed(5, 'r', 0.85)`
2. Controller updates Model: `model.update_event(5, {'r': 0.85})`
3. Controller queries modified status: `is_modified = model.is_modified(5, 'r')`
4. Controller sends **specific update**: `primitive_panel.update_marker(5, 'r', 0.85, is_modified)`
5. Panel updates **only that marker**: `_markers[(5, 'r')].update_position(0.85)`
6. <50ms later, user sees update ✅

**Key changes**:
- Panel maintains `_markers` dict: `{(event_idx, prim): DraggablePoint}`
- DraggablePoint objects created once, updated many times
- Controller sends specific commands, not generic "rebuild"
- Model provides rich query interface

---

## Implementation Phases

### Phase 1: Model Query Interface

**Goal**: Model becomes complete source of truth with rich query API

**Changes**:
- ✅ Already has: `get_event()`, `get_all_events()`, `update_event()`
- Add: `is_modified(event_idx, prim) -> bool`
- Add: `get_baseline_value(event_idx, prim) -> float`
- Add: `get_modified_events() -> set[int]`
- Add: `reset_event_primitive(event_idx, prim) -> float`

**Contract** (see `04_API_CONTRACTS.md`):
- All queries are O(1)
- All queries are side-effect free
- Commands update atomically

**Validation**:
```python
def test_model_query_interface():
    model = EditorModel()
    model.load_from_csv('data/single_dating_to_love_M1.csv')
    
    # Query baseline
    baseline = model.get_baseline_value(5, 'r')
    assert baseline == model.baseline_events[5]['r']
    
    # Update
    model.update_event(5, {'r': 0.85})
    
    # Query modified status
    assert model.is_modified(5, 'r') == True
    
    # Reset
    reset_value = model.reset_event_primitive(5, 'r')
    assert reset_value == baseline
    assert model.is_modified(5, 'r') == False
```

---

### Phase 2: Persistent Markers in Panel

**Goal**: Panel maintains marker objects, updates them incrementally

**Changes**:
- Add `_markers: dict[(int, str), DraggablePoint]` to PrimitivePanel
- `display_primitives()`: Create markers once, store in `_markers`
- Add `update_marker(event_idx, prim, value, is_modified)`: Update single marker
- `clear_all_modified()`: Loop through `_markers`, update styles

**Before**:
```python
def display_primitives(self):
    for ax in self.axes:
        ax.clear()
    
    # Recreate all markers
    for event_idx, event in enumerate(self.model.events):
        for prim in ['v', 'r', 'f', 'a', 'S']:
            # Creates new DraggablePoint every time ❌
            DraggablePoint(ax, event_idx, event[prim], ...)
```

**After**:
```python
def display_primitives(self):
    """Full rebuild - only on initialization."""
    # Clear old markers
    self._markers.clear()
    
    # Create persistent markers
    for event_idx, event in enumerate(self.model.events):
        for prim in ['v', 'r', 'f', 'a', 'S']:
            marker = DraggablePoint(ax, event_idx, event[prim], ...)
            self._markers[(event_idx, prim)] = marker  # ✅ Store for reuse

def update_marker(self, event_idx, prim, value, is_modified):
    """Incremental update - on every edit."""
    marker = self._markers[(event_idx, prim)]
    marker.update_position(value)  # ✅ Update existing object
    marker.set_modified(is_modified)
    self.canvas.draw_idle()  # Efficient partial redraw
```

**Validation**:
```python
def test_persistent_markers():
    panel = PrimitivePanel(controller)
    
    # Get marker identity
    marker = panel._markers[(5, 'r')]
    id_before = id(marker)
    
    # Update
    panel.update_marker(5, 'r', 0.85, True)
    
    # Verify same object
    id_after = id(panel._markers[(5, 'r')])
    assert id_before == id_after
```

---

### Phase 3: Controller Context Preservation

**Goal**: Controller routes specific updates, not generic rebuilds

**Before**:
```python
def on_primitive_value_changed(self, event_idx, prim, value):
    self.model.update_event(event_idx, {prim: value})
    # ❌ Loses context, rebuilds everything
    self.primitive_panel.display_primitives()
```

**After**:
```python
def on_primitive_value_changed(self, event_idx, prim, value):
    # Update model
    self.model.update_event(event_idx, {prim: value})
    
    # Query modified status
    is_modified = self.model.is_modified(event_idx, prim)
    
    # ✅ Incremental update with context preserved
    self.primitive_panel.update_marker(event_idx, prim, value, is_modified)
    
    # Update trajectory (only if gamma_self affected)
    if self._affects_gamma_self(prim):
        self.trajectory_panel.update_trajectory()
```

**Validation**:
```python
def test_incremental_update_flow():
    # Mock panel
    update_marker_called = False
    display_primitives_called = False
    
    def mock_update(*args):
        nonlocal update_marker_called
        update_marker_called = True
    
    def mock_display():
        nonlocal display_primitives_called
        display_primitives_called = True
    
    controller.primitive_panel.update_marker = mock_update
    controller.primitive_panel.display_primitives = mock_display
    
    # Trigger edit
    controller.on_primitive_value_changed(5, 'r', 0.85)
    
    # Verify incremental path taken
    assert update_marker_called
    assert not display_primitives_called
```

---

### Phase 4: LayoutManager (Optional Enhancement)

**Goal**: Centralize coordinate transform logic

**Changes**:
- Create `layout_manager.py` with coordinate abstractions
- Extract gauge positioning to `LayoutManager.get_gauge_position()`
- Extract subplot positioning to `LayoutManager.get_subplot_bounds()`

**Before** (scattered):
```python
# In trajectory_panel.py
gauge_text.set_transform(self.fig.transFigure)
gauge_text.set_position((0.55, 0.95))  # ❌ Magic numbers

# In primitive_panel.py
ax.set_position([0.1, 0.2, 0.4, 0.7])  # ❌ Manual positioning
```

**After** (centralized):
```python
# In layout_manager.py
class LayoutManager:
    GAUGE_X = 0.55  # Between panels
    GAUGE_Y = 0.95
    
    def get_gauge_position(self):
        return (self.GAUGE_X, self.GAUGE_Y)
    
    def get_subplot_bounds(self, panel='primitive'):
        if panel == 'primitive':
            return [0.1, 0.2, 0.4, 0.7]
        elif panel == 'trajectory':
            return [0.55, 0.2, 0.4, 0.7]

# In trajectory_panel.py
layout = LayoutManager()
gauge_text.set_position(layout.get_gauge_position())  # ✅ Clear intent
```

**Validation**: Reposition gauge by changing one value, works on first try

---

## Migration Plan

### Rollout Strategy

**Stage 1: Model Enhancement** (Low Risk)
- Implement Phase 1 (Model query interface)
- Add tests for new methods
- Existing code continues to work

**Stage 2: Panel Refactor** (Medium Risk)
- Implement Phase 2 (Persistent markers)
- Keep `display_primitives()` working for initialization
- Add new `update_marker()` method
- No Controller changes yet, still calls `display_primitives()`

**Stage 3: Controller Integration** (High Risk)
- Implement Phase 3 (Context preservation)
- Switch Controller to call `update_marker()`
- Remove global `_double_click_armed` variable
- **This is the critical cutover point**

**Stage 4: Cleanup** (Low Risk)
- Implement Phase 4 (LayoutManager) if desired
- Refactor coordinate logic
- Performance optimization

### Rollback Plan

If Stage 3 fails:
1. Revert Controller changes
2. Continue calling `display_primitives()`
3. Persistent markers (Stage 2) still work with full rebuilds
4. Investigate failure, retry

### Testing Strategy

**Unit Tests**:
- Model query interface (Phase 1)
- Marker persistence (Phase 2)
- Contract validation (Phase 3)

**Integration Tests**:
- Edit→Save→Reset workflow
- Rapid edits stress test
- Memory leak detection

**Performance Tests**:
- Edit operation: <50ms
- Reset operation: <50ms
- 100 rapid edits: <5s total

**Manual Tests**:
- Drag marker smoothly
- Double-click reset feels instant
- Gauge updates correctly
- No visual artifacts

---

## Success Criteria

### Must Have (Required for Success)
- ✅ Edit single primitive: <50ms
- ✅ Reset single primitive: <50ms
- ✅ Persistent markers (same object ID after update)
- ✅ No memory leaks after 100 operations
- ✅ All validation tests pass

### Should Have (Quality Improvements)
- ✅ Controller context preserved (no lossy communication)
- ✅ No global state variables
- ✅ Contracts documented in `04_API_CONTRACTS.md`

### Nice to Have (Future Enhancements)
- Coordinate system abstraction (Phase 4)
- Undo/redo support
- Multi-select editing

---

## Risk Assessment

### High Risk
- **Controller cutover (Phase 3)**: Changes communication pattern fundamentally
- **Mitigation**: Extensive testing, gradual rollout, rollback plan

### Medium Risk
- **Marker lifecycle management**: Must ensure markers cleaned up when events deleted
- **Mitigation**: Implement `remove_marker()` method, test with dynamic event lists

### Low Risk
- **Model query interface (Phase 1)**: Pure additions, no breaking changes
- **Performance**: Incremental updates are fundamentally faster than rebuilds

---

## Learnings to Preserve

### What We Discovered
1. **PySide6 revealed, didn't cause**: The architectural issue existed with matplotlib, just masked by blocking event loop
2. **Performance is architectural**: Can't optimize a fundamentally O(n) algorithm to O(1) - need structural change
3. **Information flow matters**: Losing context in Controller→Panel communication was root cause
4. **State-based > Timing-based**: Double-click state machine more robust than timing threshold

### What to Watch For
1. **Persistent object lifecycle**: Must clean up when events deleted
2. **Synchronization**: Model update must trigger Panel update atomically
3. **Error propagation**: Failures must not leave Panel in inconsistent state

### What to Avoid
1. **Shortcuts**: "Just this once" global variable becomes permanent
2. **Lossy communication**: Preserving context costs nothing, losing it costs everything
3. **Premature optimization**: Get correctness first, then optimize

---

## Lessons Learned (Post-Implementation)

### Critical Discoveries

**1. Thread Safety is Non-Negotiable in Qt**
- **Problem**: Application hung after minimize/restore when dragging primitives
- **Root Cause**: Background timer thread calling GUI updates directly violated Qt's thread model
- **Solution**: Used `QTimer.singleShot(0, lambda: ...)` to marshal all GUI updates to main thread
- **Lesson**: Qt/matplotlib widgets must ONLY be updated from the main Qt event loop, even if changes originated from background threads
- **Code Pattern**:
  ```python
  # WRONG - in timer thread
  self.trajectory_panel.update_trajectory(...)
  
  # RIGHT - marshal to main thread
  from PySide6.QtCore import QTimer
  QTimer.singleShot(0, lambda: self.trajectory_panel.update_trajectory(...))
  ```

**2. View State Must Be Explicitly Preserved**
- **Problem**: User's scroll zoom was lost when editing primitives
- **Root Cause**: `update_trajectory(preserve_view=False)` cleared `manual_xlim/ylim` even when user had zoomed
- **Solution**: Only clear manual zoom on explicit reset, not on every update
- **Lesson**: User-initiated state (zoom, pan) is sacred - preserve it unless user explicitly resets
- **Code Pattern**:
  ```python
  # Check if manual zoom exists, preserve it
  if not self.manual_xlim and not self.manual_ylim:
      # No manual zoom, allow auto-scaling
      pass
  # else: keep existing manual zoom
  ```

**3. Label Annotations Need Separate Lifecycle**
- **Problem**: Double-click removed marker instantly, but label lingered until recomputation
- **Root Cause**: Labels only updated in `update_markers()` which was called after async recomputation
- **Solution**: Added `remove_marker_label(event_idx, prim)` for immediate synchronous removal
- **Lesson**: Visual feedback should be instant - don't wait for background computation
- **Code Pattern**:
  ```python
  # Update marker position immediately (synchronous)
  self.primitive_panel.update_marker(event_idx, prim, baseline_value, is_modified=False)
  # Remove label immediately (synchronous)  
  self.primitive_panel.remove_marker_label(event_idx, prim)
  # Background recomputation happens later
  ```

**4. Daemon Threads Prevent Clean Shutdown**
- **Problem**: Need to mark timer threads as daemon to allow application exit
- **Solution**: Set `timer.daemon = True` before starting
- **Lesson**: Background threads should be daemon unless they must complete critical work
- **Code Pattern**:
  ```python
  self.debounce_timer = threading.Timer(0.3, callback)
  self.debounce_timer.daemon = True  # Allow clean exit
  self.debounce_timer.start()
  ```

**5. Window State Changes Require Canvas Refresh**
- **Problem**: Application hung after minimize/restore
- **Contributing Factor**: Matplotlib canvas state may be stale after window state changes
- **Solution**: Added `showEvent` and `changeEvent` handlers to refresh canvas
- **Lesson**: Window lifecycle events (minimize, restore) may require refreshing embedded widgets
- **Code Pattern**:
  ```python
  def showEvent(self, event):
      super().showEvent(event)
      if hasattr(self, 'canvas'):
          self.canvas.draw_idle()
  ```

### Architecture Validation

**What Worked Well**:
1. **Incremental updates**: O(1) marker updates dramatically improved perceived performance
2. **Persistent markers**: Creating markers once and updating them proved robust
3. **Model query interface**: Rich query API made controller logic clean and simple
4. **Architecture documentation**: Having principles and contracts written down caught violations early

**What Was Harder Than Expected**:
1. **Thread safety**: Qt's threading model is strict - required careful marshaling of GUI updates
2. **View state preservation**: Needed careful logic to distinguish user zoom vs auto-scaling
3. **Multiple visual updates**: Single logical operation (reset) required coordinating marker + label + line updates

**What Would We Do Differently**:
1. **Start with thread safety**: Should have used QTimer from the beginning, not as a fix
2. **Document state ownership**: Be explicit about who owns zoom state (user vs system)
3. **Test window lifecycle**: Should have tested minimize/restore earlier in development

### Impact on Future Work

**For Phase 2.1 (Scaling to 1000 events)**:
- Thread-safe update pattern is established and working
- Incremental update infrastructure supports virtualized rendering
- Performance measurement tools are in place

**For Phase 2.x (New features)**:
- Undo/Redo: Will need to capture marker state changes, not full rebuilds
- Multi-file: Each file will have its own controller/panel set
- Export: Can export from Model directly, no need for Panel state

### Validation After Implementation

After completing this refactor, verify:

- [✅] All tests in `08_VALIDATION_CHECKLIST.md` pass
- [✅] Performance targets in `07_PERFORMANCE_TARGETS.md` met (<50ms operations)
- [✅] Information flow matches `02_INFORMATION_FLOW.md` target sequences
- [✅] API contracts in `04_API_CONTRACTS.md` implemented correctly
- [✅] Principles in `01_PRINCIPLES.md` no longer violated
- [✅] Navigation features: scroll zoom, right-click pan, reset view all working
- [✅] Thread safety: No hangs after minimize/restore
- [✅] State preservation: User zoom persists across edits

---

## Next Refactor Prediction

**When**: Phase 2.1 (scaling to 1000 events)

**Why**: Rendering 1000 markers may still be slow, even with incremental updates

**Likely Solution**: Virtualized rendering
- Only render visible markers (in current viewport)
- Create/destroy markers as user scrolls
- Maintain logical model of all 1000 events
- Physical view only shows ~100 visible events

**Principle Evolution**:
- P4 (Persistent Objects) may become "Persistent for visible objects"
- New principle: "Render only what user can see"

---

## Validation After Implementation

After completing this refactor, verify:

- [ ] All tests in `08_VALIDATION_CHECKLIST.md` pass
- [ ] Performance targets in `07_PERFORMANCE_TARGETS.md` met
- [ ] Information flow matches `02_INFORMATION_FLOW.md` target sequences
- [ ] API contracts in `04_API_CONTRACTS.md` implemented correctly
- [ ] Principles in `01_PRINCIPLES.md` no longer violated
- [ ] `00_INDEX.md` updated with new architecture status

---

**Author**: Architecture team  
**Reviewers**: Validated through user testing  
**Implementation Status**: ✅ COMPLETED  
**Completion Date**: 2025-12-06  
**Lines Changed**: ~500 (model, controller, panels, main app)  
**Performance Gain**: 4-10x faster operations (<50ms vs 200-500ms)

