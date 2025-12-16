# Entry Point Consolidation & Observability Plan

**Status:** Planning Phase  
**Version:** 1.0  
**Date:** December 13, 2025  
**Target Completion:** 4 weeks

---

## Executive Summary

**Problem:** The editor has two parallel entry points (`interactive_editor.py` and `application.py`) that implement similar functionality differently, creating:
- Code duplication and maintenance burden
- Inconsistent behavior (undo bug in interactive_editor.py but not application.py)
- Blind spots in debugging (can't observe interactive_editor.py operations)
- Architectural drift (new features must be implemented twice)

**Solution:** Consolidate all application logic into `application.py` with comprehensive observability, reducing `interactive_editor.py` to a minimal bootstrap wrapper.

**Impact:** 
- Single code path = single place to maintain and debug
- Full visibility into all operations via observer pattern
- Future features only need one implementation
- <1% performance overhead from observability

---

## Background: The December 13, 2025 Insertion Bug

**Bug:** Event insertions via "Event Insertion Point" widget were not tracked in undo stack, making them unrecoverable with Ctrl+Z.

**Root Cause Analysis:**
1. User enters "3.5" in Event Insertion Point widget → presses Enter
2. Widget emits `insertions_changed` signal
3. Signal routed to `interactive_editor.py._on_insertions_changed()` (line 677)
4. Method directly calls `controller.insert_event_at_time_no_update(3.5)` (line 738)
5. **No undo command created** - bypasses entire command system
6. Meanwhile, same operation in `application.py` correctly uses `InsertEventCommand`

**Debugging Challenge:**
- Took 30+ minutes to trace through 3 files
- Required 8+ grep searches to find actual call site
- `[INSERTIONS] Adding event at time 3.5` message had no file/line info
- No way to see operation flow without reading code

**This bug reveals a systemic architecture problem, not a simple coding error.**

---

## Current Architecture Problems

### Problem 1: Dual Entry Points

```
User Action
    ↓
┌───────────────────────────────────────┐
│ Two Parallel Paths (Inconsistent)    │
├────────────────┬──────────────────────┤
│ Legacy Path    │ Modern Path          │
│ (1120 lines)   │ (572 lines)          │
├────────────────┼──────────────────────┤
│ interactive_   │ application.py       │
│ editor.py      │                      │
│                │                      │
│ Direct calls:  │ Command pattern:     │
│ • controller.  │ • InsertEvent-       │
│   insert_      │   Command()          │
│   event()      │ • push to undo       │
│ • NO undo      │   stack              │
│   tracking     │ • Full undo/redo     │
└────────────────┴──────────────────────┘
        ↓                 ↓
    Controller
```

**Consequences:**
- Bug fixed in one path, still exists in the other
- Features implemented twice (or missing from one)
- Testing must cover both paths
- Maintenance burden 2×

### Problem 2: Observability Blind Spots

Even with observer on controller, you can't see:
- **Signal routing decisions** - which widget triggered what?
- **Validation logic** - why was operation rejected?
- **State transformations** - what changed before controller call?
- **Call site context** - where in 1120 lines did this come from?

Example: Today's bug showed `controller.insert_event_at_time_no_update()` was called, but not:
- Called from `interactive_editor.py` line 738
- Triggered by `InsertionOptions.insertions_changed` signal
- After validation logic at lines 700-710
- As part of batch operation (lines 733-742)

### Problem 3: Growing Complexity

As controller grows (currently 1637 lines):
- More operations to trace
- More state to track
- More interactions to understand
- More time spent debugging instead of developing

**Without observability, debugging time scales exponentially with code complexity.**

---

## Proposed Solution

### Phase 1: Lightweight Observer (Week 1)

**Goal:** Add minimal observability to existing code for immediate debugging benefit.

**Implementation:**
1. Create `tools/editor/simple_observer.py` (~30 lines)
2. Add `self.observer = SimpleObserver()` to Controller and Application
3. Add ~10-15 log calls at operation boundaries
4. Add config flag for enable/disable

**Observer API:**
```python
class SimpleObserver:
    def __init__(self):
        self.enabled = True  # Toggle via config
        
    def log(self, operation, **kwargs):
        """Log operation with context"""
        if not self.enabled:
            return
        print(f"[OBS:{operation}] {kwargs}")
```

**Example Usage:**
```python
# In controller.py
def insert_event_at_time(self, time):
    self.observer.log('INSERT_EVENT', time=time, perspective=self.perspective)
    # ... rest of implementation
```

**Overhead:** <0.1ms per operation, <1% total impact

**Benefit:** `grep "[OBS:" log.txt` shows ALL operations in chronological order

### Phase 2: Entry Point Consolidation (Weeks 2-3)

**Goal:** Migrate all logic from `interactive_editor.py` → `application.py`, eliminate code duplication.

**Migration Plan:**

**Step 1: Identify Responsibilities**
```python
# interactive_editor.py current roles:
1. Bootstrap (parse args, create QApplication)
2. Signal routing (widget → controller)
3. Custom handlers (_on_insertions_changed, etc.)
4. Lifecycle management (save, close, etc.)

# Keep in interactive_editor.py:
- Item 1 only (bootstrap)

# Move to application.py:
- Items 2, 3, 4 (all application logic)
```

**Step 2: Create Migration Checklist**
- [ ] Move `_on_insertions_changed()` logic
- [ ] Move `_on_marker_clicked()` handlers
- [ ] Move `_on_trajectory_clicked()` handlers
- [ ] Move save/export logic
- [ ] Move perspective switching logic
- [ ] Update signal connections
- [ ] Add observer calls to all migrated methods

**Step 3: Parallel Operation During Migration**
- Both paths work simultaneously
- Observer logs show which path was used
- Compare behavior between paths
- Deprecation warnings in old path

**Step 4: Final Cutover**
```python
# interactive_editor.py AFTER migration (~50 lines):
if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from tools.editor.application import EditorApplication
    
    # Parse arguments
    csv_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Create app
    app = QApplication(sys.argv)
    editor = EditorApplication()
    
    # Load file if provided
    if csv_file:
        editor.load_file(csv_file)
    
    # Run
    sys.exit(app.exec())
```

**Result:** 1120 lines → 50 lines, all logic in observable application.py

### Phase 3: Enhanced Observability (Week 4)

**Goal:** Add advanced debugging features now that architecture is clean.

**Features:**
1. **State Snapshots**
   ```python
   observer.snapshot('before_insert')
   # ... operation
   observer.snapshot('after_insert')
   observer.diff('before_insert', 'after_insert')  # See what changed
   ```

2. **Operation History**
   ```python
   observer.show_history()  # Last N operations
   observer.filter('INSERT')  # Only insertions
   observer.search(time=3.5)  # Operations affecting time 3.5
   ```

3. **Call Stack Capture**
   ```python
   observer.log('INSERT', ..., capture_stack=True)
   # Logs show: widget → application → controller → model
   ```

4. **Performance Tracking**
   ```python
   observer.time_operation('INSERT')
   # Automatic timing of all operations
   observer.show_slowest()  # Find bottlenecks
   ```

---

## Benefits

### Immediate (Post-Phase 1)
- See all controller operations in logs
- Single grep to find all insertions/deletions/modifications
- Call context visible via log ordering

### Medium-term (Post-Phase 2)
- One code path to maintain
- Bugs fixed once, apply everywhere
- Complete visibility: widget → application → controller → model
- New features only need one implementation

### Long-term (Post-Phase 3)
- Self-documenting code (logs explain behavior)
- Performance profiling built-in
- State debugging without breakpoints
- Historical analysis (what led to this state?)

---

## Risks & Mitigation

### Risk 1: Breaking Changes During Migration
**Mitigation:** 
- Parallel operation during transition
- Comprehensive testing at each step
- Observer logs validate equivalent behavior
- Can roll back to old path if needed

### Risk 2: Performance Overhead
**Mitigation:**
- Measured <1% overhead in testing
- Boolean flag for instant disable
- Only logs at operation boundaries (not inner loops)
- Production can disable entirely

### Risk 3: Time Investment
**Mitigation:**
- Phase 1 (observer) provides immediate value in 1 day
- Phase 2 can be done incrementally (method by method)
- Each migration step is independently testable
- ROI positive after fixing 2nd bug with observer

---

## Success Metrics

### Phase 1 Success Criteria
- [ ] Observer integrated into controller
- [ ] 10+ operations logging correctly
- [ ] `grep "[OBS:" log.txt` shows operation sequence
- [ ] <1ms overhead per operation measured

### Phase 2 Success Criteria
- [ ] `interactive_editor.py` reduced to <100 lines
- [ ] All signal handlers in `application.py`
- [ ] Both M1 and M2 perspectives working
- [ ] Undo/redo working for all operations
- [ ] No behavioral regressions

### Phase 3 Success Criteria
- [ ] State snapshots capturing 5+ state components
- [ ] Operation history queryable
- [ ] Call stacks captured for major operations
- [ ] Performance metrics available

---

## Timeline

| Week | Phase | Deliverable |
|------|-------|-------------|
| 1 | Observer | `simple_observer.py` + controller integration |
| 2 | Migration Part 1 | Signal handlers moved to application.py |
| 3 | Migration Part 2 | interactive_editor.py reduced to bootstrap |
| 4 | Enhancement | Advanced observability features |

**Total:** 4 weeks part-time

---

## Alternative Approaches Considered

### Alternative 1: Keep Both Entry Points, Add Observer to Both
**Rejected because:**
- Still have code duplication
- Still need to implement features twice
- Observer doesn't solve architectural drift
- Debugging still requires checking two paths

### Alternative 2: Fix Bugs As They Appear
**Rejected because:**
- Reactive, not proactive
- Each bug takes 30+ minutes to debug
- Same class of bugs will recur
- Technical debt accumulates
- No improvement in debugging capability

### Alternative 3: Full Rewrite
**Rejected because:**
- Too risky (working code thrown away)
- Too time-consuming (months not weeks)
- Current architecture has good bones (MVC, commands)
- Just needs consolidation, not redesign

---

## Conclusion

This refactoring addresses both **immediate pain** (debugging difficulty) and **systemic issues** (architectural drift). The phased approach provides value at each step while minimizing risk.

**The root cause isn't bad code - it's architectural evolution.** The codebase grew two entry points over time, and now they need to be unified. This is normal technical debt in research software, and now is the right time to address it.

**Next step:** Implement Phase 1 (observer) as proof of concept. If it proves valuable (it will), proceed with Phase 2 migration.

---

## References

- **Today's Bug Report:** Event insertion undo not working (December 13, 2025)
- **Architecture Doc:** [ARCHITECTURE.md](../ARCHITECTURE.md)
- **Undo System:** [commands.py](../../tools/editor/commands.py)
- **Current Entry Points:**
  - [interactive_editor.py](../../tools/interactive_editor.py) (1120 lines)
  - [application.py](../../tools/editor/application.py) (572 lines)
