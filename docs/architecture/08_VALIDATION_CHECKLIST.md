# Architecture Validation Checklist

**Purpose**: Systematic tests to verify architecture principles are being followed. Run these checks when:
- Completing a refactor
- Reviewing code changes
- Investigating bugs
- Onboarding new developers

## Quick Health Check

Run this 5-minute check daily during active development:

```bash
# 1. No global state for communication
grep -r "global " tools/editor/ --include="*.py" | grep -v "# global"

# 2. All Panel updates go through Controller
grep -r "\.update\|\.display\|\.set_" tools/editor/views/ --include="*.py" | grep -v "self\."

# 3. Performance targets met
python tools/editor/tests/test_performance.py

# 4. No memory leaks
python tools/editor/tests/test_memory.py

# 5. Information flow follows contracts
python tools/editor/tests/test_contracts.py
```

Expected: All checks pass ✅

---

## P1: Single Source of Truth

### Manual Check
**Question**: For each piece of data, can you identify exactly one authoritative source?

**Test**:
1. Open `tools/editor/models/editor_model.py`
2. For each data type (events, modified status, baseline):
   - Is it stored in Model? ✅
   - Is it duplicated in Controller? ❌
   - Is it duplicated in any Panel? ❌

**Validation Questions**:
- What is the current value of event 5, primitive 'r'?
  - **Answer**: `model.events[5]['r']` (one place to check)
- Is event 5, primitive 'r' modified?
  - **Answer**: `model.is_modified(5, 'r')` (one method to call)
- What is the baseline value?
  - **Answer**: `model.get_baseline_value(5, 'r')` (one source)

**Failure Signs**:
- Multiple components claiming to know "current value"
- Synchronization code between components
- Caching with potential staleness

---

## P2: Controller as Mediator

### Automated Check
```python
# tools/editor/tests/test_architecture.py

def test_no_direct_panel_communication():
    """Verify no Panel directly calls another Panel."""
    
    import ast
    import os
    
    violations = []
    
    for root, dirs, files in os.walk('tools/editor/views'):
        for file in files:
            if not file.endswith('.py'):
                continue
            
            path = os.path.join(root, file)
            with open(path) as f:
                tree = ast.parse(f.read())
            
            # Look for method calls on other panel instances
            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute):
                    # self.other_panel.update() is violation
                    if 'panel' in node.attr.lower():
                        violations.append(f"{path}:{node.lineno}")
    
    assert len(violations) == 0, f"Direct Panel communication found: {violations}"
```

### Manual Check
**Test**: Draw the communication graph

```
Panel A → Controller → Panel B   ✅ Correct
Panel A → Panel B                 ❌ Violation
Panel A → Model                   ❌ Violation (should go through Controller)
```

**Validation Questions**:
- When PrimitivePanel changes, how does TrajectoryPanel know?
  - **Answer**: PrimitivePanel → Controller → TrajectoryPanel ✅
- Can PrimitivePanel query Model directly?
  - **Answer**: No, must ask Controller ✅

**Failure Signs**:
- Panels holding references to other Panels
- Panels holding references to Model
- Callbacks with >1 recipient

---

## P3: Incremental Updates Over Full Rebuilds

### Automated Check
```python
def test_edit_is_incremental():
    """Verify editing doesn't trigger full rebuild."""
    
    model = EditorModel()
    model.load_from_csv('data/single_dating_to_love_M1.csv')
    controller = EditorController(model)
    panel = PrimitivePanel(controller)
    
    # Track method calls
    rebuild_called = False
    update_called = False
    
    original_display = panel.display_primitives
    original_update = panel.update_marker
    
    def mock_display():
        nonlocal rebuild_called
        rebuild_called = True
        original_display()
    
    def mock_update(*args):
        nonlocal update_called
        update_called = True
        original_update(*args)
    
    panel.display_primitives = mock_display
    panel.update_marker = mock_update
    
    # Edit single primitive
    controller.on_primitive_value_changed(5, 'r', 0.85)
    
    assert update_called, "update_marker should be called"
    assert not rebuild_called, "display_primitives should NOT be called"
```

### Performance Check
```python
def test_incremental_performance():
    """Verify incremental update meets performance target."""
    
    # From 07_PERFORMANCE_TARGETS.md
    TARGET_MS = 50
    
    times = []
    for i in range(10):
        start = time.perf_counter()
        controller.on_primitive_value_changed(5, 'r', 0.5 + i*0.01)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    
    avg = sum(times) / len(times)
    assert avg < TARGET_MS / 1000, f"Average {avg*1000:.1f}ms exceeds {TARGET_MS}ms target"
```

**Failure Signs**:
- Edit operation taking >50ms
- Profiler showing marker creation/destruction
- Frame rate drops during drag operations

---

## P4: Persistent Objects for Interactive Elements

### Automated Check
```python
def test_markers_persist():
    """Verify DraggablePoint objects are reused, not recreated."""
    
    model = EditorModel()
    model.load_from_csv('data/single_dating_to_love_M1.csv')
    controller = EditorController(model)
    panel = PrimitivePanel(controller)
    
    # Get marker object identity
    marker_before = panel._markers[(5, 'r')]
    id_before = id(marker_before)
    
    # Edit primitive
    controller.on_primitive_value_changed(5, 'r', 0.85)
    
    # Check same object
    marker_after = panel._markers[(5, 'r')]
    id_after = id(marker_after)
    
    assert id_before == id_after, "Marker object was recreated (should be persistent)"
```

### Memory Check
```python
def test_no_marker_leaks():
    """Verify no memory leaks from repeated operations."""
    
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    baseline = process.memory_info().rss / 1024 / 1024
    
    # Perform 100 operations
    for i in range(100):
        controller.on_primitive_value_changed(5, 'r', 0.5 + (i % 10) * 0.01)
    
    after = process.memory_info().rss / 1024 / 1024
    growth = after - baseline
    
    assert growth < 10, f"Memory leak: {growth:.1f}MB growth after 100 ops"
```

**Failure Signs**:
- Memory growing with repeated operations
- Object `id()` changing for same marker
- Double-click state being lost

---

## P5: No Timing Dependencies

### Code Review Check
```bash
# Search for timing-based logic
grep -r "time\\.sleep\|time\\.time.*<\|threading\\.Timer" tools/editor/ --include="*.py"
```

Expected: No results (or only in test fixtures)

### Automated Check
```python
def test_double_click_is_state_based():
    """Verify double-click uses state machine, not timing."""
    
    marker = DraggablePoint(ax, 0, 0.5, callback=None)
    
    # Simulate two clicks
    marker.on_press(None)
    marker.on_release(None)
    
    # Check state changed (not time-based)
    assert marker._click_count == 1, "First click should arm"
    
    marker.on_press(None)
    marker.on_release(None)
    
    assert marker._click_count == 2, "Second click should trigger"
    
    # Verify no time.time() calls in implementation
    import inspect
    source = inspect.getsource(marker.on_press)
    assert 'time.time' not in source, "Should not use timing"
    assert 'time.perf_counter' not in source, "Should not use timing"
```

**Failure Signs**:
- Code comparing timestamps with thresholds
- Behavior changing on different hardware
- `sleep()` calls to "wait for state to stabilize"

---

## P6: Explicit Contracts Over Implicit Coupling

### Documentation Check
For each public method in Controller and Model:

```python
def test_contracts_documented():
    """Verify all public methods have contracts in 04_API_CONTRACTS.md."""
    
    import ast
    
    # Parse API_CONTRACTS.md
    with open('docs/architecture/04_API_CONTRACTS.md') as f:
        contracts_doc = f.read()
    
    # Get all public methods
    with open('tools/editor/controllers/editor_controller.py') as f:
        tree = ast.parse(f.read())
    
    methods = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not node.name.startswith('_'):  # Public method
                methods.append(node.name)
    
    # Check each is documented
    for method in methods:
        assert f"### `{method}" in contracts_doc, \
            f"Method {method} not documented in API contracts"
```

### Runtime Check
```python
def test_preconditions_validated():
    """Verify preconditions are checked at method entry."""
    
    model = EditorModel()
    
    # Invalid event index should raise
    with pytest.raises(IndexError):
        model.get_event(999)
    
    # Invalid primitive should raise
    with pytest.raises(KeyError):
        model.get_event(0)['invalid_prim']
```

**Failure Signs**:
- Methods silently failing
- Unclear error messages
- Assumptions not documented

---

## P7: Observable Information Flow

### Logging Check
```python
def test_communication_is_logged():
    """Verify all Controller communication can be traced."""
    
    import logging
    from io import StringIO
    
    # Capture logs
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger('editor.controller')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    # Perform operation
    controller.on_primitive_value_changed(5, 'r', 0.85)
    
    # Check logs show communication
    logs = log_stream.getvalue()
    assert 'on_primitive_value_changed' in logs
    assert 'update_marker' in logs or 'update_event' in logs
```

### No Hidden State Check
```bash
# Find global variables
grep -n "^[A-Za-z_][A-Za-z0-9_]* = " tools/editor/**/*.py | grep -v "class \|def \|import "
```

Expected: Only constants (UPPERCASE) or module-level configuration

**Failure Signs**:
- Can't trace why state changed
- Debugging requires print statements in many places
- Action-at-a-distance effects

---

## P8: Coordinate Systems Abstracted

### Centralization Check
```bash
# Find coordinate transform code
grep -r "transFigure\|transData\|transAxes" tools/editor/views/ --include="*.py"
```

Expected: Only in `layout_manager.py` (once implemented)

### Manual Check
**Test**: Try to reposition gauge

1. Open `docs/architecture/06_COORDINATE_SYSTEMS.md` (once created)
2. Find gauge position specification
3. Should be single value to change: `GAUGE_X = 0.55`
4. Change should work on first try ✅

**Failure Signs**:
- Coordinate calculations scattered across files
- Trial-and-error to position elements
- Multiple files need changes for one positioning change

---

## Integration Validation

### End-to-End Test
```python
def test_edit_reset_cycle():
    """Verify complete edit→save→reset workflow."""
    
    model = EditorModel()
    model.load_from_csv('data/single_dating_to_love_M1.csv')
    controller = EditorController(model)
    panel = PrimitivePanel(controller)
    
    # Get baseline
    baseline = model.get_baseline_value(5, 'r')
    
    # Edit
    controller.on_primitive_value_changed(5, 'r', 0.85)
    assert model.is_modified(5, 'r')
    assert model.events[5]['r'] == 0.85
    
    # Save
    controller.save()
    assert not model.is_modified(5, 'r')  # No longer modified
    assert model.get_baseline_value(5, 'r') == 0.85  # New baseline
    
    # Reset (should be no-op since not modified)
    controller.on_primitive_reset(5, 'r')
    assert model.events[5]['r'] == 0.85  # Unchanged
```

### Stress Test
```python
def test_rapid_edits():
    """Verify system handles rapid user input."""
    
    # Simulate user rapidly dragging marker
    for i in range(100):
        value = 0.5 + (i % 10) * 0.01
        controller.on_primitive_value_changed(5, 'r', value)
    
    # Should complete without errors
    final_value = model.events[5]['r']
    assert 0.5 <= final_value <= 0.6  # In expected range
```

---

## Validation Workflow

### Before Merging Code
```bash
# Run full validation suite
python -m pytest tools/editor/tests/test_architecture.py -v
python -m pytest tools/editor/tests/test_performance.py -v
python -m pytest tools/editor/tests/test_contracts.py -v

# Manual checks
./docs/architecture/run_health_check.sh
```

### After Refactor
1. Run all automated tests ✅
2. Complete this checklist manually ✅
3. Update `00_INDEX.md` with current status ✅
4. Document learnings in refactor `.md` file ✅

### Daily During Development
1. Quick health check (5 min)
2. Performance spot check (if editing critical path)
3. Review recent commits against principles

---

## Checklist Summary

| Principle | Automated Test | Manual Check | Performance Test |
|-----------|----------------|--------------|------------------|
| P1: Single Source | ✅ AST analysis | ✅ Code review | - |
| P2: Mediator | ✅ Call graph | ✅ Draw diagram | - |
| P3: Incremental | ✅ Mock tracking | ✅ Profiling | ✅ <50ms |
| P4: Persistent | ✅ Object identity | ✅ Memory check | ✅ No leaks |
| P5: No Timing | ✅ Source scan | ✅ State machine | - |
| P6: Contracts | ✅ Doc coverage | ✅ Preconditions | - |
| P7: Observable | ✅ Log tracing | ✅ Grep globals | - |
| P8: Coord Systems | ✅ Grep transforms | ✅ Positioning test | - |

### Passing Criteria
- **Green**: All automated tests pass, manual checks confirm principles
- **Yellow**: <3 violations, documented and tracked for fix
- **Red**: ≥3 violations, or critical principle violated (P1, P2, P3)

**Current Status**: 🔴 Red - P3 violated (full rebuilds), P4 violated (no persistence), P7 violated (global state)

---

**Last Updated**: 2025-12-06  
**Status**: Validation checklist defined, tests designed (not yet implemented)
