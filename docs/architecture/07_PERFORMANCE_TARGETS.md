# Performance Targets

**Purpose**: Measurable performance requirements that validate architecture health. When targets are consistently missed, architecture needs attention.

## Table of Contents

- [Critical Performance Requirements](#critical-performance-requirements)
- [Performance Validation Scripts](#performance-validation-scripts)
- [Performance Debugging Workflow](#performance-debugging-workflow)
- [Scaling Projections](#scaling-projections)
- [Performance vs Correctness](#performance-vs-correctness)
- [Performance Health Check](#performance-health-check)

---

## Critical Performance Requirements

### Single Marker Operations

| Operation | Target | Current | Status | Validation |
|-----------|--------|---------|--------|------------|
| Edit primitive (drag) | <50ms | 200-500ms | ❌ FAIL | User perception: <50ms feels instant, >100ms feels laggy |
| Reset primitive (dbl-click) | <50ms | 200-500ms | ❌ FAIL | Same operation as edit, should be same speed |
| Select event (click) | <10ms | Not measured | ⚠️ UNKNOWN | Selection is visual-only, should be near-instant |
| Update marker position | <1ms | Not measured | ⚠️ UNKNOWN | Single artist update, O(1) operation |
| Update marker style | <1ms | Not measured | ⚠️ UNKNOWN | Single artist property change |

**Why 50ms?**
- Human perception threshold: <50ms = instant, 50-100ms = perceptible, >100ms = slow
- Jakob Nielsen's usability research: 0.1s is limit for feeling like system is reacting instantaneously
- Current 200-500ms is 4-10x too slow

**Root Cause of Current Failure**:
- Full panel rebuild (destroy + recreate 50 markers) on every operation
- O(n*m) operation when should be O(1)

---

### Batch Operations

| Operation | Target | Current | Status | Validation |
|-----------|--------|---------|--------|------------|
| Initialize panel (50 events) | <500ms | ~300ms | ✅ PASS | Rare operation, user expects slight delay |
| Save file (50 events) | <100ms | Not measured | ⚠️ UNKNOWN | IO-bound, should be fast for small files |
| Load file (50 events) | <200ms | Not measured | ⚠️ UNKNOWN | IO + panel rebuild, one-time cost |
| Clear all modified markers | <100ms | Not measured | ⚠️ UNKNOWN | Updates all marker styles |

**Why These Are Acceptable Being Slower**:
- Initialization: One-time cost at startup
- Save/Load: Explicit user action, expects brief pause
- Clear modified: After save, part of save operation

---

### Scaling Targets (Phase 2.1)

| Operation | 50 Events | 1000 Events | Status | Validation |
|-----------|-----------|-------------|--------|------------|
| Edit single primitive | <50ms | <50ms | ❌ FAIL | O(1) should scale |
| Reset single primitive | <50ms | <50ms | ❌ FAIL | O(1) should scale |
| Initialize panel | <500ms | <10s | ⚠️ UNKNOWN | O(n*m) but rare |
| Save file | <100ms | <1s | ⚠️ UNKNOWN | O(n) IO-bound |
| Update trajectory | <50ms | <100ms | ⚠️ UNKNOWN | O(n) plot update |

**Critical Insight**: Incremental operations (edit, reset, select) must be O(1) to scale. If they're O(n), system is unusable at 1000 events.

**Current Architecture**: All operations are O(n) due to full rebuilds. This is the core problem.

---

### Memory Performance

| Metric | Target | Current | Status | Validation |
|--------|--------|---------|--------|------------|
| Baseline memory (50 events) | <100MB | Not measured | ⚠️ UNKNOWN | Qt + matplotlib + numpy overhead |
| Memory after 100 edits | Stable | Not measured | ⚠️ UNKNOWN | No leaks from create/destroy cycle |
| Memory at 1000 events | <500MB | Not measured | ⚠️ UNKNOWN | Linear scaling acceptable |
| Memory growth rate | 0 (after init) | Not measured | ⚠️ UNKNOWN | No leaks |

**How to Measure**:
```python
import psutil
import os

process = psutil.Process(os.getpid())
baseline = process.memory_info().rss / 1024 / 1024  # MB

# Perform 100 edit operations
for i in range(100):
    # ... edit ...
    pass

after = process.memory_info().rss / 1024 / 1024
growth = after - baseline

assert growth < 10, f"Memory leak: {growth}MB growth after 100 ops"
```

---

### UI Responsiveness

| Metric | Target | Current | Status | Validation |
|--------|--------|---------|--------|------------|
| Frame rate during drag | >30 FPS | Not measured | ⚠️ UNKNOWN | Smooth visual feedback |
| Input lag | <16ms | Not measured | ⚠️ UNKNOWN | One frame at 60 FPS |
| Canvas redraw time | <16ms | Not measured | ⚠️ UNKNOWN | 60 FPS = 16ms per frame |
| Zoom response time | <10ms | Not measured | ⚠️ UNKNOWN | Should feel instant |

**Why 30 FPS**:
- Below 24 FPS: Motion appears jerky
- 30 FPS: Acceptable for UI interaction
- 60 FPS: Ideal but not required for drag operations

---

## Performance Validation Scripts

### Script 1: Single Operation Timing

```python
# tools/editor/tests/test_performance.py

import time
from editor.models.editor_model import EditorModel
from editor.controllers.editor_controller import EditorController
from editor.views.primitive_panel import PrimitivePanel

def test_edit_primitive_performance():
    """Edit single primitive should complete in <50ms."""
    
    # Setup
    model = EditorModel()
    model.load_from_csv('data/single_dating_to_love_M1.csv')
    controller = EditorController(model)
    panel = PrimitivePanel(controller)
    
    # Warmup (first operation may be slower)
    controller.on_primitive_value_changed(0, 'r', 0.5)
    
    # Measure
    times = []
    for i in range(10):
        start = time.perf_counter()
        controller.on_primitive_value_changed(5, 'r', 0.5 + i*0.01)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    
    avg_time = sum(times) / len(times)
    max_time = max(times)
    
    print(f"Edit primitive: avg={avg_time*1000:.1f}ms, max={max_time*1000:.1f}ms")
    
    assert avg_time < 0.050, f"Average time {avg_time*1000:.1f}ms exceeds 50ms target"
    assert max_time < 0.100, f"Max time {max_time*1000:.1f}ms exceeds 100ms threshold"
```

---

### Script 2: Scaling Test

```python
def test_scaling_1000_events():
    """Verify O(1) operations don't degrade with scale."""
    
    # Test at different scales
    for n_events in [50, 100, 500, 1000]:
        model = create_synthetic_events(n_events)
        controller = EditorController(model)
        panel = PrimitivePanel(controller)
        
        # Measure edit time
        start = time.perf_counter()
        controller.on_primitive_value_changed(n_events // 2, 'r', 0.5)
        elapsed = time.perf_counter() - start
        
        print(f"n={n_events}: edit_time={elapsed*1000:.1f}ms")
        
        # Should be constant regardless of n
        assert elapsed < 0.050, f"Edit time increased with scale: {elapsed*1000:.1f}ms at n={n_events}"
```

---

### Script 3: Memory Leak Detection

```python
def test_no_memory_leaks():
    """Verify repeated operations don't leak memory."""
    
    import psutil
    import os
    
    model = EditorModel()
    model.load_from_csv('data/single_dating_to_love_M1.csv')
    controller = EditorController(model)
    panel = PrimitivePanel(controller)
    
    process = psutil.Process(os.getpid())
    baseline = process.memory_info().rss / 1024 / 1024
    
    # Perform 100 edit/reset cycles
    for i in range(100):
        controller.on_primitive_value_changed(5, 'r', 0.5 + (i % 10) * 0.01)
        controller.on_primitive_reset(5, 'r')
    
    after = process.memory_info().rss / 1024 / 1024
    growth = after - baseline
    
    print(f"Memory: baseline={baseline:.1f}MB, after={after:.1f}MB, growth={growth:.1f}MB")
    
    assert growth < 10, f"Memory leak detected: {growth:.1f}MB growth after 100 ops"
```

---

### Script 4: Continuous Monitoring

```python
class PerformanceMonitor:
    """Add to Controller to continuously monitor performance."""
    
    def __init__(self):
        self.times = {}
    
    def time_operation(self, operation_name):
        """Context manager for timing operations."""
        class Timer:
            def __init__(self, monitor, name):
                self.monitor = monitor
                self.name = name
            
            def __enter__(self):
                self.start = time.perf_counter()
                return self
            
            def __exit__(self, *args):
                elapsed = time.perf_counter() - self.start
                
                if self.name not in self.monitor.times:
                    self.monitor.times[self.name] = []
                self.monitor.times[self.name].append(elapsed)
                
                # Log slow operations
                if elapsed > 0.050:  # 50ms threshold
                    logger.warning(f"{self.name} took {elapsed*1000:.1f}ms (target <50ms)")
        
        return Timer(self, operation_name)

# Usage in Controller:
class EditorController:
    def __init__(self, model):
        self.model = model
        self.perf = PerformanceMonitor()
    
    def on_primitive_value_changed(self, idx, prim, value):
        with self.perf.time_operation('edit_primitive'):
            # ... implementation ...
            pass
```

---

## Performance Debugging Workflow

### When Performance Target Is Missed

1. **Identify the operation**:
   - Check `07_PERFORMANCE_TARGETS.md` for target
   - Measure actual time with `perf_counter()`
   - Document gap: "Edit primitive taking 250ms vs 50ms target"

2. **Profile the operation**:
   ```python
   import cProfile
   import pstats
   
   profiler = cProfile.Profile()
   profiler.enable()
   
   controller.on_primitive_value_changed(5, 'r', 0.5)
   
   profiler.disable()
   stats = pstats.Stats(profiler)
   stats.sort_stats('cumtime')
   stats.print_stats(20)  # Top 20 slowest functions
   ```

3. **Check information flow**:
   - Consult `02_INFORMATION_FLOW.md`
   - Is it following target flow or current (broken) flow?
   - Are there unexpected O(n) operations?

4. **Check API contracts**:
   - Consult `04_API_CONTRACTS.md`
   - Are performance contracts being violated?
   - Are there hidden full rebuilds?

5. **Check principles**:
   - Consult `01_PRINCIPLES.md`
   - Is P3 (Incremental Updates) being violated?
   - Is P4 (Persistent Objects) being violated?

---

## Scaling Projections

### Phase 2.0: 50 Events (Current)
- **Target**: All operations <50ms
- **Status**: ❌ Edit/Reset taking 200-500ms
- **Blocker**: Full rebuilds on every operation

### Phase 2.1: 1000 Events (Planned)
- **Target**: O(1) operations remain <50ms, O(n) operations <1s
- **Projection with current architecture**: 
  - Edit: 4000-10000ms (4-10 seconds) ❌ UNUSABLE
  - Save: ~1s ✅ Acceptable
- **Projection with incremental updates**:
  - Edit: <50ms ✅ Target met
  - Save: ~1s ✅ Target met

### Phase 2.2: 10,000+ Events (Future)
- **Target**: O(1) operations <100ms (slight degradation acceptable), O(n) operations <10s
- **Requirements**:
  - Virtualized rendering (only render visible markers)
  - Chunked file IO (stream large files)
  - Background trajectory computation

---

## Performance vs Correctness

**Principle**: Never sacrifice correctness for performance.

**Bad Tradeoff**:
```python
# ❌ Skipping validation for speed
def update_event(self, idx, changes):
    # Skip bounds checking to save 1μs
    self.events[idx].update(changes)
```

**Good Tradeoff**:
```python
# ✅ Algorithmic improvement preserves correctness
def update_marker(self, idx, prim, value):
    # O(1) lookup instead of O(n) rebuild
    marker = self._markers[(idx, prim)]
    marker.update_position(value)
```

**When Performance Can't Meet Target**:
1. Document in refactor history why target can't be met
2. Update target if it's unrealistic
3. Consider if operation should be async
4. Consider if UI feedback can make it feel faster (progress indicator)

---

## Performance Health Check

### ✅ Green: Performance is healthy if...
- All critical operations meet targets
- No performance regressions in recent commits
- Profiling shows expected O() complexity
- Memory usage is stable

### ⚠️ Yellow: Performance needs attention if...
- Operations miss target by <2x
- Performance has regressed recently
- Unexpected O(n) operations appearing
- Memory slowly growing

### 🔴 Red: Performance requires architecture fix if...
- Operations miss target by >2x
- Fundamental O(n) when should be O(1)
- Memory leaks detected
- Performance degrades with scale

**Current Status**: 🔴 Red - Edit/Reset operations 4-10x too slow due to architectural issue

---

**Last Updated**: 2025-12-06  
**Status**: Targets defined, current performance measured as failing, validation scripts designed
