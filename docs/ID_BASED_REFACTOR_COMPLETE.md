# ID-Based Event Tracking Refactor - Complete

## Summary
Successfully migrated the interactive editor from **time-based** to **ID-based** event tracking. This eliminates the fragile baseline shifting logic that caused the baseline cascade deletion bug.

## Problem Statement
The original time-based tracking system used `(event_time, primitive)` as keys for:
- `baseline_by_time_m1/m2`: Original CSV values
- `modified_primitives_m1/m2`: Tracking which events have modifications
- `marker_positions_m1/m2`: Pinned marker positions

When inserting events using Ctrl+Shift+Click, all subsequent event times shifted forward. This required shifting all dictionary keys, which led to a cascade deletion bug:
1. Shift (56.0, 'v') → (49.0, 'v') creates new key
2. Shift (49.0, 'v') → (42.0, 'v') **immediately deletes** the just-created key
3. Result: Lost baseline data, hollow markers persist after undo

## Solution Architecture
**Event Identity**: Every event now has an immutable `id` attribute:
- IDs assigned monotonically at creation (CSV load or insertion)
- IDs never reused, even after deletion
- Time is mutable (changes during insertion), ID is immutable

**Key Benefits**:
- No baseline shifting needed - IDs don't change when events are inserted
- Simpler undo logic - just add/remove baseline entries by ID
- Easier debugging - event identity stable across operations
- No cascade deletion bugs - dictionary keys are stable

## Files Modified

### 1. tools/editor/event.py
- Added `event_id` parameter to `__init__` (default None)
- Added `self.id = event_id` attribute
- Updated docstring explaining immutable identity

### 2. tools/editor/load_events.py
- Changed signature: `def load_events_from_csv(filepath, start_id=0)`
- Assigns sequential IDs during load: `Event(..., event_id=event_id)`
- Returns tuple: `(events, metadata, next_event_id)`

### 3. tools/editor/model.py
Key changes:
- Line 102: Added `self.next_event_id: int = 0` counter
- Lines 109-110, 116-117: Updated comments for ID-based dictionaries
- Lines 127-149: `load_csv()` handles new return signature, updates `next_event_id`
- Lines 465-486: `is_modified()` uses `event_id` instead of `event_time`
- Lines 609-620: `pin_marker(event_id, ...)` signature changed
- Lines 622-633: `unpin_marker(event_id, ...)` signature changed
- Lines 635-648: `clear_primitive_modification(event_id, ...)` signature changed

### 4. tools/editor/controller.py
**Major structural changes**:
- Lines 92-93: Renamed `baseline_by_time_m1/m2` → `baseline_by_id_m1/m2`
- Lines 176-189: Initialize baselines using `event.id` from events list
- Lines 218-243: `_sync_baseline_to_view()` converts ID space → index space

**Baseline operations now use IDs**:
- Lines 515-522: `_apply_primitive_change()` uses `event.id` for baseline lookup
- Lines 526-541: Modified primitives tracking uses `event.id` keys
- Lines 570-585: Marker pinning uses `event.id` for all operations
- Lines 654-659: Reset to baseline uses ID-based lookup
- Lines 770-775: Delete event removes baseline by ID
- Lines 816-821: Insert event (undo) adds baseline by ID
- Lines 1272-1280: `_update_baseline_after_insert()` uses ID keys
- Lines 1287-1304: `_update_baseline_after_delete()` uses ID keys

**Insertion logic simplified**:
- Lines 887-896: New event creation assigns `event_id=self.model.next_event_id`, increments counter
- Lines 980-991: Baseline addition uses `new_event.id` - **NO SHIFTING LOGIC**
- Lines 1110-1115: Undo insertion removes baseline by `removed_event.id` - **NO SHIFTING LOGIC**

**Debug logging cleaned up**:
- Removed verbose per-key shift logging (~8 print statements)
- Kept high-level operation markers for debugging

## What Was Removed
**Eliminated entirely** from insertion operations:
```python
# OLD CODE (REMOVED):
for shift_old, shift_new in reversed(time_shifts):
    for prim in ['v', 'r', 'f', 'a', 'S']:
        old_key = (shift_old, prim)
        new_key = (shift_new, prim)
        if old_key in baseline_dict:
            baseline_val = baseline_dict[old_key]
            del baseline_dict[old_key]  # Dangerous!
            baseline_dict[new_key] = baseline_val
```

**NEW CODE (SIMPLE)**:
```python
# Add baseline for newly inserted event using its ID
for prim in ['v', 'r', 'f', 'a', 'S']:
    key = (new_event.id, prim)
    baseline_dict[key] = new_event.markers[prim].value
```

**Eliminated from undo insertion**:
```python
# OLD CODE (REMOVED):
# Collect all shifts FIRST to avoid cascade deletion
shifts_to_apply = []
for orig_idx, old_time, new_time in reversed(shifted_events):
    # ... collect shifts ...

# Apply shifts in two phases
for new_key, old_key, baseline_val in shifts_to_apply:
    del baseline_dict[new_key]
for new_key, old_key, baseline_val in shifts_to_apply:
    baseline_dict[old_key] = baseline_val
```

**NEW CODE (SIMPLE)**:
```python
# Remove baseline for inserted event by ID
for prim in ['v', 'r', 'f', 'a', 'S']:
    key = (removed_event.id, prim)
    if key in baseline_dict:
        del baseline_dict[key]
```

## Testing Checklist
To verify the refactor works correctly:

1. **Original Bug Test**: M1 move→insert→M2→move→insert→M1→undo×2
   - ✅ Markers should fill correctly after undo
   - ✅ Labels should be removed after undo
   
2. **ID Persistence**: Insert event, verify it gets unique ID
   - Check console output: `[INSERT] New event ID=N`
   
3. **Multiple Insertions**: Insert 3 events in sequence
   - IDs should increment: ID=50, 51, 52
   
4. **Baseline Lookup**: Reset primitive to baseline
   - Should find baseline by event ID, not time
   
5. **Marker Pinning**: Pin marker on inserted event
   - Should store by `(event_id, primitive)` key

## Documentation Updates
- **ARCHITECTURE.md**: Added v2.1.3 changelog, Event class documentation, ID-based design principles
- **docs/DEBUG.md**: Added debug infrastructure section, updated architecture insights

## Architecture Benefits
1. **Robustness**: No cascade deletion possible - keys are stable
2. **Simplicity**: ~50 lines of complex shift logic eliminated
3. **Debuggability**: Event identity stable across all operations
4. **Maintainability**: Adding new ID-based dictionaries requires no shift logic
5. **Performance**: Fewer dictionary operations during insertion

## Migration Notes
- **Backward Compatibility**: Existing CSV files load correctly (IDs assigned on load)
- **No Data Loss**: All original CSV data preserved with stable ID references
- **Undo Stack**: Existing undo commands work (they reference events by index/data)

## Verification
Run: `python tools\editor\main.py data\library\single_dating_to_love.csv`

Test sequence:
1. M1 perspective: Move v marker at t=28
2. Ctrl+Shift+Click to insert event at t=35
3. Switch to M2 perspective
4. Move v marker at t=42
5. Ctrl+Shift+Click to insert event at t=49
6. Switch back to M1 perspective
7. Press Ctrl+Z twice
8. **Expected**: Markers should fill, labels should disappear, baseline intact
