# Architectural Principles

**Purpose**: These principles are invariants that survive across rearchitecture cycles. When a principle is violated, it indicates architectural debt that must be addressed.

## Core Principles

### P1: Single Source of Truth
**Principle**: Every piece of data has exactly one authoritative source.

**Rationale**: Multiple sources create synchronization bugs that are difficult to debug and don't scale.

**Application**:
- EditorModel is authoritative for all event/primitive data
- Controller is authoritative for UI state (selection, editing mode)
- Panels are purely presentational - they display data, never own it

**Validation Test**:
```python
# If you can answer these questions definitively, principle holds:
# - What is the current value of event 5, primitive 'r'?
#   Answer: model.events[5]['r']
# - Is event 5 primitive 'r' modified from baseline?
#   Answer: model.is_modified(5, 'r')
# - Which event is currently selected?
#   Answer: controller.selected_event_idx
```

**Violations**:
- ❌ Panel caches data that could diverge from Model
- ❌ Controller duplicates data that exists in Model
- ❌ Global variables used to share state between components

---

### P2: Controller as Mediator
**Principle**: All component-to-component communication flows through the Controller. No direct component communication.

**Rationale**: Direct communication creates O(n²) interaction complexity. Mediator pattern creates O(n) complexity and provides single observation point.

**Application**:
- Panel → Controller: Events sent via callbacks (e.g., `on_primitive_value_changed`)
- Controller → Panel: Commands sent via method calls (e.g., `update_marker`)
- Panel → Panel: **Forbidden** - must route through Controller

**Validation Test**:
```python
# Draw the component graph:
# - Every edge must pass through Controller
# - No Panel-to-Panel edges
# - No Panel-to-Model edges (Controller mediates)
```

**Violations**:
- ❌ Global `_double_click_armed` variable (Panel-to-Panel side channel)
- ❌ Panel directly queries Model
- ❌ Panel directly modifies another Panel

---

### P3: Incremental Updates Over Full Rebuilds
**Principle**: When one thing changes, update one thing. Never rebuild everything.

**Rationale**: Full rebuilds don't scale. At 50 events it's slow (200-500ms). At 1000 events it's unusable.

**Application**:
- User edits event 5, primitive 'r' → Update only that marker
- User resets event 5, primitive 'r' → Update only that marker
- User selects different event → Update selection state, no rebuild
- User zooms → Update axis limits, no rebuild

**Validation Test**:
```python
# Measure operations:
# - Edit single primitive: <50ms (target), currently 200-500ms ❌
# - Reset single primitive: <50ms (target)
# - Select event: <10ms (target)
# - Zoom: <10ms (target)
```

**Violations**:
- ❌ `display_primitives()` destroys and recreates all 50 markers
- ❌ Any method that loops through all events to update one thing

---

### P4: Persistent Objects for Interactive Elements
**Principle**: Objects that users interact with (markers, lines) must persist across updates.

**Rationale**: Creating/destroying interactive objects is expensive and loses state (hover, selection, double-click arming).

**Application**:
- DraggablePoint objects created once, updated many times
- Stored in `_markers` dict: `{(event_idx, prim): DraggablePoint}`
- Updates modify marker properties, not marker identity
- Only destroy markers when event is deleted

**Validation Test**:
```python
# After 100 edit operations:
# - Same DraggablePoint object instances exist (check `id()`)
# - Memory usage is stable (no leak from repeated create/destroy)
```

**Violations**:
- ❌ Current `display_primitives()` creates new DraggablePoint on every edit
- ❌ Losing double-click arming state on rebuild

---

### P5: No Timing Dependencies
**Principle**: Correctness cannot depend on timing thresholds or sleep/wait calls.

**Rationale**: Timing varies across hardware, under load, and with language/OS. Timing-based logic is fundamentally unreliable.

**Application**:
- Use state machines instead of time windows
- Use message acknowledgment instead of delays
- Use explicit sequencing instead of "wait and hope"

**Validation Test**:
```python
# Remove all time.sleep(), threshold checks
# Replace with explicit state: armed/disarmed, ready/busy
# Double-click: State-based (armed → triggered) ✅
# Not timing-based (< 0.15s threshold) ❌
```

**Violations**:
- ❌ Original double-click detection: `time.time() - last_click < 0.15`

---

### P6: Explicit Contracts Over Implicit Coupling
**Principle**: Every interface has documented preconditions, postconditions, and error behavior.

**Rationale**: Implicit assumptions become bugs when components evolve independently. Explicit contracts enable parallel development and confident refactoring.

**Application**:
- Every Controller method has contract in `04_API_CONTRACTS.md`
- Every callback signature documented with data flow direction
- Every error condition has defined handling (raise, log, ignore)

**Validation Test**:
```python
# For every method:
# - Preconditions: What must be true before calling?
# - Postconditions: What is guaranteed after return?
# - Errors: What exceptions can be raised and why?
```

**Violations**:
- ❌ Undocumented assumptions about call order
- ❌ Silent failures or ignored errors
- ❌ Methods that sometimes succeed, sometimes fail with no indication

---

### P7: Observable Information Flow
**Principle**: All information flow must be visible for debugging. No hidden side channels.

**Rationale**: Debugging requires understanding what changed and why. Hidden communication makes this impossible.

**Application**:
- Every Controller method can log: "received X from Y, sending Z to W"
- No shared mutable state between components
- No action-at-a-distance through global variables

**Validation Test**:
```python
# Can you draw a sequence diagram of any operation?
# Can you add logging to trace every message?
# Can you replay a sequence of operations deterministically?
```

**Violations**:
- ❌ Global `_double_click_armed` (invisible state change)
- ❌ Panel methods with side effects on other panels
- ❌ "Magically" synchronized state with no clear update path

---

### P8: Coordinate Systems Abstracted
**Principle**: Layout and positioning logic is centralized, not scattered.

**Rationale**: Matplotlib's multiple coordinate systems (data, axes, figure) are confusing. Scattering transform logic makes simple positioning (gauge at X=0.55) take 4 iterations to get right.

**Application**:
- LayoutManager owns all coordinate transforms
- Panels request positions: `layout.get_gauge_position()` → returns figure coords
- Layout decisions in one place, easy to understand and modify

**Validation Test**:
```python
# To reposition gauge:
# - Change one value in LayoutManager
# - Not hunt through multiple files for transform calls
```

**Violations**:
- ❌ Gauge positioning code scattered in `trajectory_panel.py`
- ❌ Each panel manually computing figure coordinates
- ❌ Transform logic copy-pasted with slight variations

---

### P9: Type-Consistent Keying for State Dictionaries
**Principle**: All state dictionaries must use consistent, immutable key types. Never mix types (e.g., int vs float) for the same logical entity.

**Rationale**: Type mismatches in dictionary lookups cause silent failures that are hard to debug and don't scale. Immutable keys (e.g., IDs) prevent cascading updates on structural changes.

**Application**:
- Use `event_id` (int) for modification tracking, not `event_time` (float)
- Document key types in data structure definitions
- Prefer immutable keys over mutable ones (IDs over times/dates)

**Validation Test**:
```python
# For every state dict:
# - Keys are of consistent type (all int, all str, etc.)
# - Keys are immutable (don't change on insert/delete)
# - Lookup failures are logged/asserted in debug mode
```

**Violations**:
- ❌ Using `event_time` (float) to check `modified_primitives` (keyed by `event_id` int)
- ❌ Undocumented key type assumptions

---

## Known Architectural Debt (December 7, 2025)

### Technical Debt from Phase 2.1 (Diagnostic Markers)

**Status**: Non-critical, works well, but violates principles documented above.

#### TD1: Mixed Event System Violates P2 (Controller as Mediator)
**Issue**: Primitive panel uses both Qt Signals and callback attributes for communication.
- Qt Signals: `primitive_changed`, `diagnostic_marker_placed` (modern, proper)
- Callbacks: `on_primitive_preview`, `on_primitive_reset` (legacy, direct)

**Violation**: Callbacks create direct Panel→Main communication bypassing controller pattern.

**Impact**: Low - both patterns work, but inconsistency confuses maintenance.

**Recommended Fix**:
```python
# Convert all callbacks to signals
class PrimitivePanelPyQtGraph(QWidget):
    primitive_changed = Signal(int, str, float)
    primitive_preview = Signal(int, str, float)  # NEW
    primitive_reset = Signal(int, str)           # NEW
    diagnostic_marker_placed = Signal(int, str, float)
```

#### TD2: Coordinate System Knowledge Implicit
**Issue**: PyQtGraph coordinate mapping differs between event types:
- `QMouseEvent.position()` - Widget-relative coordinates (wrong for scene)
- `QGraphicsSceneMouseEvent.scenePos()` - Scene coordinates (correct)

**Violation**: Violates documentation principle - critical knowledge only in git history.

**Impact**: Medium - future developers will rediscover this bug through trial and error.

**Recommended Fix**: Add docstring to both panel files:
```python
"""
PyQtGraph Coordinate System Notes:
- Use scene().sigMouseClicked.connect() for click handling
- Event will be QGraphicsSceneMouseEvent with scenePos() method
- Then mapSceneToView() converts to data coordinates
- DO NOT use mousePressEvent() - gives QMouseEvent with wrong coordinates
"""
```

#### TD3: Diagnostic Handler Violates P1 (Single Source of Truth)
**Issue**: `_on_diagnostic_marker()` in `interactive_editor.py` directly accesses model and duplicates controller logic.

**Current**:
```python
# In interactive_editor.py (UI layer)
events = self.model.get_events(...)  # UI accessing model directly
for i in range(len(events) - 1):
    gamma_self = update_gamma_self(...)  # UI duplicating controller math
```

**Violation**: UI layer doing business logic. Model access should be mediated by controller.

**Impact**: Medium - logic duplication risks divergence if controller trajectory computation changes.

**Recommended Fix**:
```python
# In controller.py
def compute_hypothetical_trajectory(self, event_index, primitive, value):
    """Compute full trajectory with one primitive modified."""
    # Use existing trajectory computation logic with modified primitives
    return final_gamma_self

# In interactive_editor.py
gamma_val = self.controller.compute_hypothetical_trajectory(...)
```

#### TD4: Incomplete Signal Chain for Drag Events
**Issue**: Diagnostic marker drag handlers don't emit signals.

**Current**:
```python
def _on_diagnostic_dragged(self, idx, prim, y_value):
    # Does nothing - drag doesn't trigger trajectory update
    pass
```

**Violation**: Breaks expected event flow - dragging should update trajectory in real-time.

**Impact**: High - feature incomplete. Dragging diagnostic marker doesn't show real-time trajectory updates.

**Recommended Fix**:
```python
def _on_diagnostic_dragged(self, idx, prim, y_value):
    self.diagnostic_marker_placed.emit(self.diagnostic_event_idx, prim, y_value)

def _on_diagnostic_released(self, idx, prim, y_value):
    self.diagnostic_marker_placed.emit(self.diagnostic_event_idx, prim, y_value)
```

#### TD5: GUI Importing Core Math Violates Separation of Concerns
**Issue**: `interactive_editor.py` imports `from core.love import update_gamma_self`

**Violation**: GUI knows about mathematical implementation. Should only know about controller API.

**Impact**: Low - works fine, but couples UI to core math details.

**Recommended Fix**: Move all `core.love` interaction to controller, GUI only calls controller methods.

**Status**: ⏳ Deferred to Phase 3 cleanup (after QDockWidget migration)

---

## Phase 3 Technical Debt Resolution

When implementing Phase 3 (QDockWidget + M2 integration), address:
1. **TD5** - Move `core.love` imports from GUI to controller
2. **GUI/Controller separation** - Ensure panels only call controller methods
3. **State management** - Verify single source of truth for M1/M2 data
4. **Observer pattern** - Ensure dual-perspective updates work correctly

See [../architecture_recommendations.md](../architecture_recommendations.md) for Phase 3 architecture details.

---

## Principle Evolution

Principles are not immutable - they evolve as we learn. When violated principles repeatedly cause bugs, they're correct. When enforced principles repeatedly block progress, they need revision.

### How to Update Principles

1. **Document the violation**: What principle was broken and why?
2. **Analyze the outcome**: Did it cause bugs? Performance issues? Confusion?
3. **Propose revision**: Should principle be strengthened, weakened, or removed?
4. **Create ADR**: Document the decision in `decisions/`
5. **Update this file**: Keep principles in sync with reality

### Principle Health

A principle is **healthy** if:
- Enforcing it prevents bugs
- Violating it causes problems
- Team agrees it's worth the cost

A principle is **sick** if:
- Enforcing it blocks reasonable solutions
- Violating it causes no problems
- Team works around it regularly

---

**Last Updated**: 2025-12-07  
**Status**: Phase 2.1 complete with documented technical debt
