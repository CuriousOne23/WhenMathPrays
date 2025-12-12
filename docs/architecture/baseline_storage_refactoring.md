# Baseline Storage Refactoring

**Date:** December 11, 2025  
**Status:** ✅ COMPLETE (v2.1.2)  
**Implementation Time:** ~2.5 hours  
**Risk:** Low - All tests passing  

---

## Executive Summary

**COMPLETED:** Migrated baseline storage from index-based arrays to time-keyed dictionary.

**Recommendation:** Migrate to **time-keyed dictionary** storage for baseline values.

---

## Current Architecture

### Data Structure
```python
# Controller initialization
self.baseline_primitives = {
    'time': np.array([0.0, 7.0, 14.0, 21.0, 28.0, 35.0, 42.0, 49.0, 56.0, 60.0]),
    'v': np.array([5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 6.0, 7.0, 8.0, 8.0]),
    'r': np.array([0.0, 2.0, -2.0, 2.0, 5.0, 7.0, 8.0, 9.0, 9.0, 9.0]),
    'f': np.array([2.0, 2.0, 2.0, 5.0, 5.0, 7.0, 8.0, 9.0, 9.0, 9.0]),
    'a': np.array([2.0, 3.0, 3.0, 5.0, 5.0, 7.0, 8.0, 9.0, 9.0, 9.0]),
    'S': np.array([0.0, 1.0, -1.0, 3.0, 5.0, 7.0, 8.0, 9.0, 10.0, 10.0])
}

# Also maintains shadow copy
self.original_baseline_primitives = {...}  # Deep copy of above
```

### Lookup Pattern
```python
def _apply_primitive_change(self, event_index: int, primitive: str, value: float):
    # Get baseline for comparison
    baseline_value = self.baseline_primitives[primitive][event_index]
    
    # Check if back to baseline
    if abs(value - baseline_value) < FLOAT_TOLERANCE:
        # Remove from modified set...
```

### Problems Exposed

**1. Index Instability After Insertion**
```python
# Initial state: Event at time 42 is at index 6
baseline_primitives['r'][6] = 8.0  # Correct

# User inserts event at time 3.5 (becomes index 1)
# All subsequent events shift: time 42 now at index 7

# But baseline_primitives['r'][6] still = 8.0
# baseline_primitives['r'][7] = 9.0 (what was at time 49)

# Undo tries to restore index 6 to baseline
# Gets wrong baseline value!
```

**2. Corruption Via Model Re-fetch**
```python
# Original (BUGGY) code in _update_baseline_after_insert:
def _update_baseline_after_insert(self, insert_idx: int):
    # Re-fetch from model after insertion
    self.baseline_primitives = self.model.get_primitives_array(...)
    # ❌ Problem: Model contains MODIFIED values (user has edited)
    # ❌ Now baseline contains user edits, not original CSV values!
```

**3. Complex Synchronization Requirements**
```python
def _update_baseline_after_insert(self, insert_idx: int):
    # Must carefully insert into baseline arrays
    self.baseline_primitives['time'] = np.insert(...)
    self.original_baseline_primitives['time'] = np.insert(...)
    
    for prim in ['v', 'r', 'f', 'a', 'S']:
        self.baseline_primitives[prim] = np.insert(...)
        self.original_baseline_primitives[prim] = np.insert(...)
    # 12 array operations for every insertion!

def _update_baseline_after_delete(self, deleted_idx: int):
    # Must carefully delete from baseline arrays
    # Another 12 array operations...
```

**4. Need for Shadow Copy**
The existence of `original_baseline_primitives` as a backup is a code smell - it indicates the architecture doesn't cleanly separate mutable state from immutable baseline.

---

## Proposed Architecture

### Data Structure
```python
# Time-keyed dictionary (no arrays)
self.baseline_by_time = {
    # Key: (time, primitive) → Value: baseline_value
    (0.0, 'v'): 5.0,
    (0.0, 'r'): 0.0,
    (0.0, 'f'): 2.0,
    (7.0, 'v'): 5.0,
    (7.0, 'r'): 2.0,
    (42.0, 'r'): 8.0,  # This key NEVER changes
    # ... etc
}
```

### Lookup Pattern
```python
def _apply_primitive_change(self, event_index: int, primitive: str, value: float):
    # Get event time (stable identifier)
    events = self.model.get_events(self.perspective)
    event_time = events[event_index].time
    
    # Get baseline for comparison (insertion-proof!)
    baseline_value = self.baseline_by_time[(event_time, primitive)]
    
    # Check if back to baseline
    if abs(value - baseline_value) < FLOAT_TOLERANCE:
        # Remove from modified set...
```

### Initialization
```python
def _load_scenario(self, csv_file):
    # Load from CSV
    primitives = self.model.get_primitives_array(self.perspective)
    
    # Build time-keyed baseline dictionary
    self.baseline_by_time = {}
    for i, time in enumerate(primitives['time']):
        for prim in ['v', 'r', 'f', 'a', 'S']:
            key = (float(time), prim)
            self.baseline_by_time[key] = float(primitives[prim][i])
    
    # No need for separate original_baseline - this dict never changes!
```

### Insertion/Deletion Handling
```python
def _update_baseline_after_insert(self, insert_idx: int):
    # Get new event
    events = self.model.get_events(self.perspective)
    new_event = events[insert_idx]
    
    # Add baseline entries for new time point
    for prim in ['v', 'r', 'f', 'a', 'S']:
        key = (new_event.time, prim)
        self.baseline_by_time[key] = 0.0  # Inserted events start at neutral
    
    # Done! No array manipulation needed.

def _update_baseline_after_delete(self, deleted_idx: int):
    # Get deleted event time BEFORE deletion
    events = self.model.get_events(self.perspective)
    deleted_time = events[deleted_idx].time
    
    # Remove baseline entries for deleted time point
    for prim in ['v', 'r', 'f', 'a', 'S']:
        key = (deleted_time, prim)
        if key in self.baseline_by_time:
            del self.baseline_by_time[key]
    
    # Done! No array manipulation needed.
```

---

## Benefits

### 1. Insertion-Proof
```python
# Initial state
baseline_by_time[(42.0, 'r')] = 8.0

# User inserts event at time 3.5
# Event list indices shift, but keys don't change!

# Lookup still works perfectly
baseline_by_time[(42.0, 'r')]  # Still 8.0
```

### 2. No Synchronization Needed
- Baseline dictionary is completely independent of event list
- Insertions/deletions only need to add/remove keys, no reindexing
- 5 dict operations instead of 12 array operations

### 3. Impossible to Corrupt
- Cannot accidentally fetch from model (different data structure)
- Single source of truth for baseline values
- No shadow copy needed

### 4. Clear Semantics
```python
# Before (confusing)
baseline_primitives['r'][6]  # What event is this? Depends on insertion history!

# After (explicit)
baseline_by_time[(42.0, 'r')]  # Unambiguous: original value at time 42
```

### 5. Simpler Code
- Remove `original_baseline_primitives` entirely
- Remove complex array manipulation in insert/delete handlers
- Clearer variable names and intent

---

## Migration Plan

### Phase 1: Add New System Alongside Old (1 hour)

**Step 1.1: Initialize new structure**
```python
def _load_scenario(self, csv_file):
    # ... existing code ...
    
    # NEW: Build time-keyed baseline
    self.baseline_by_time = {}
    temp_primitives = self.model.get_primitives_array(self.perspective)
    for i, time in enumerate(temp_primitives['time']):
        for prim in ['v', 'r', 'f', 'a', 'S']:
            key = (float(time), prim)
            self.baseline_by_time[key] = float(temp_primitives[prim][i])
    
    # OLD: Keep existing array-based system for now
    self.baseline_primitives = {...}  # Existing code
```

**Step 1.2: Add assertion checks**
```python
def _apply_primitive_change(self, event_index: int, primitive: str, value: float):
    # Get baseline both ways
    old_baseline = self.baseline_primitives[primitive][event_index]
    
    event_time = events[event_index].time
    new_baseline = self.baseline_by_time[(event_time, primitive)]
    
    # Verify they match (catch any discrepancies)
    assert abs(old_baseline - new_baseline) < 0.001, \
        f"Baseline mismatch at idx={event_index}, time={event_time}: old={old_baseline}, new={new_baseline}"
    
    # Use new baseline
    baseline_value = new_baseline
```

### Phase 2: Switch Primary System (30 minutes)

**Step 2.1: Update all baseline lookups**
- Search for: `self.baseline_primitives[`
- Replace with: `self.baseline_by_time[(event_time, `
- Verify each call site has `event_time` available

**Step 2.2: Update insert/delete handlers**
```python
def _update_baseline_after_insert(self, insert_idx: int):
    events = self.model.get_events(self.perspective)
    new_event = events[insert_idx]
    
    for prim in ['v', 'r', 'f', 'a', 'S']:
        key = (new_event.time, prim)
        self.baseline_by_time[key] = 0.0

def _update_baseline_after_delete(self, deleted_idx: int):
    # Must get time BEFORE deleting from model
    events = self.model.get_events(self.perspective)
    deleted_time = events[deleted_idx].time
    
    for prim in ['v', 'r', 'f', 'a', 'S']:
        key = (deleted_time, prim)
        if key in self.baseline_by_time:
            del self.baseline_by_time[key]
```

### Phase 3: Remove Old System (30 minutes)

**Step 3.1: Delete old arrays**
```python
# Remove these entirely
# self.baseline_primitives = {...}
# self.original_baseline_primitives = {...}
```

**Step 3.2: Remove assertion checks**
```python
# Remove temporary validation code from Phase 1
```

**Step 3.3: Test thoroughly**
- Load CSV
- Drag primitives
- Insert events (text field and Ctrl+Shift+Click)
- Delete events
- Undo/redo all operations
- Verify labels appear/disappear correctly

### Phase 4: Update Documentation (30 minutes)

- Update architecture diagrams
- Update inline code comments
- Add migration notes to changelog

---

## Testing Strategy

### Unit Tests (Create New)
```python
def test_baseline_survives_insertion():
    """Verify baseline values unchanged after event insertion."""
    # Load scenario with event at time 42, r=8
    controller.load_csv('test_scenario.csv')
    
    # Modify r at time 42 to 5
    controller.on_primitive_changed(6, 'r', 5.0)
    
    # Insert event at time 3.5 (shifts indices)
    controller.insert_event_at_time(3.5)
    
    # Verify baseline still shows original value
    baseline = controller.baseline_by_time[(42.0, 'r')]
    assert baseline == 8.0, f"Expected baseline 8.0, got {baseline}"

def test_baseline_survives_deletion():
    """Verify baseline values unchanged after event deletion."""
    # Load scenario, modify value, insert event, delete it
    # Verify baselines remain correct
```

### Integration Tests (Existing)
- All existing undo/redo tests should pass without modification
- Label appearance/removal tests should pass
- Scenario save/load tests should pass

---

## Risk Assessment

### Low Risk Areas
- **No UI changes** - User-facing behavior identical
- **No file format changes** - CSV loading/saving unchanged
- **Undo commands already time-based** - No changes needed to command classes

### Medium Risk Areas
- **Initialization logic** - Must correctly populate dictionary from CSV
- **Edge cases** - Fractional times, duplicate times (should be prevented elsewhere)

### Mitigation
1. Implement in phases with assertions to catch issues early
2. Keep old system running in parallel during Phase 1
3. Extensive testing before removing old system
4. Git checkpoint before each phase

---

## Decision Checkpoint

**Go/No-Go Criteria:**

✅ **GO** if:
- Continuing development on event management features (Phase 2.2+)
- Team has 3+ hours available for focused refactoring
- Can afford testing time after migration

⏸️ **DEFER** if:
- No immediate plans for event management features
- Current bug fixes are sufficient for near-term needs
- Development resources extremely limited

**Recommendation:** Proceed with refactoring **before** Phase 2.2 (event management). Current architecture is fragile and will cause more bugs as features expand.

---

## Implementation Checklist

- [ ] Phase 1: Add `baseline_by_time` alongside existing arrays
- [ ] Phase 1: Add assertion checks comparing old vs new baseline lookups
- [ ] Phase 1: Run all existing tests, verify assertions don't fire
- [ ] Phase 2: Switch `_apply_primitive_change` to use new system
- [ ] Phase 2: Switch insert/delete handlers to use new system
- [ ] Phase 2: Run all tests again
- [ ] Phase 3: Remove `baseline_primitives` and `original_baseline_primitives`
- [ ] Phase 3: Remove assertion checks
- [ ] Phase 3: Full regression testing
- [ ] Phase 4: Update documentation
- [ ] Phase 4: Update changelog
- [ ] Git tag: `v2.1.2-baseline-refactor`

---

## References

- Original bug report: v2.1.1 undo fixes (December 11, 2025)
- Related issue: Index instability in undo commands (fixed in v2.1.1)
- Design principle: Use stable identifiers (time) over mutable indices
