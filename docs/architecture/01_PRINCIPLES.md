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

**Last Updated**: 2025-12-06  
**Status**: Initial principles defined during PySide6 migration refactor
