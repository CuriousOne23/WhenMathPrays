# Phase 1: Spinbox Access Audit

**Date:** December 15, 2025  
**Phase:** 1 of 5 (Audit Only - No Changes)  
**Goal:** Identify all code locations that access spinbox widget

---

## Summary

**Total Access Points Found:** 8 distinct code locations  
**Files Involved:** 3 files  
**Current Owners:** 2 (controller.py, interactive_editor.py)

**Key Finding:** Only **3 access points** from interactive_editor.py need migration. Controller already has proper access patterns.

---

## Access Points by File

### 1. tools/interactive_editor.py (NEEDS MIGRATION)

#### Access 1: Setup/Initialization (Line 257)
```python
# Connect signal for value changes
self.spinbox_editor.value_changed.connect(self._on_spinbox_value_changed)
```
**Type:** Signal connection (initialization)  
**Pattern:** Direct widget access for setup  
**Action Required:** Move to controller initialization  
**Risk:** Low (initialization only, happens once)

---

#### Access 2: Value Update (Line 574)
```python
# In _on_primitive_selected_m1() or _on_primitive_selected_m2()
if is_active:
    self.spinbox_editor.update_value(value)
```
**Type:** Write (update spinbox value programmatically)  
**Context:** When user clicks primitive marker in plot  
**Action Required:** Replace with controller method  
**Risk:** Medium (affects user interaction flow)

**Full Context:**
```python
def _on_primitive_selected_m1(self, event_idx, prim, time, val):
    """Handle primitive marker click in M1 perspective."""
    self.controller.on_primitive_selected(event_idx, prim)
    
    # Check if this is the active primitive in spinbox
    is_active = (
        self.controller.active_primitive_state['primitive'] == prim 
        and self.controller.active_primitive_state['event_id'] == self.model.get_events('M1')[event_idx].event_id
    )
    
    if is_active:
        self.spinbox_editor.update_value(val)  # ← THIS ACCESS
```

---

#### Access 3a: Set Active Primitive on Perspective Switch (Line 1025)
```python
# In _on_perspective_changed()
self.spinbox_editor.set_active_primitive(primitive_name, new_value, event_time)
```
**Type:** Write (update spinbox state)  
**Context:** User switches perspective (M1↔M2)  
**Status:** ⚠️ THIS WAS THE BUG - Fixed in v2.1.4 but still needs migration  
**Action Required:** Replace with controller method  
**Risk:** High (this is where race condition occurred)

**Full Context:**
```python
def _on_perspective_changed(self, perspective):
    """Handle perspective switch M1↔M2."""
    self.controller.switch_perspective(perspective)
    
    # Controller has already restored spinbox for this perspective
    # But this code ALSO tries to update it (causes race condition!)
    
    if self.controller.active_primitive_state['primitive']:
        primitive_name = self.controller.active_primitive_state['primitive']
        event_time = self.controller.active_primitive_state['event_time']
        
        # Find matching event in new perspective
        # ...
        
        if matching_event_found:
            self.spinbox_editor.set_active_primitive(primitive_name, new_value, event_time)  # ← THIS ACCESS
        else:
            self.spinbox_editor.clear_active()  # ← ACCESS 3b
```

---

#### Access 3b: Clear Active on Perspective Switch (Line 1035)
```python
# In _on_perspective_changed()
self.spinbox_editor.clear_active()
```
**Type:** Write (clear spinbox state)  
**Context:** No matching event in new perspective  
**Action Required:** Remove (controller already handles this)  
**Risk:** High (duplicate logic with controller)

---

### 2. tools/editor/controller.py (ALREADY CORRECT)

These are the **authoritative** access points. Keep these, make widget private.

#### Access 4: Restore State (Lines 180, 189, 204)
```python
def _restore_spinbox_state_for_perspective(self, perspective: str):
    """Restore spinbox when switching perspectives."""
    state = self.active_primitive_state_m1 if perspective == 'M1' else self.active_primitive_state_m2
    
    if state['primitive'] is None:
        self.spinbox_widget.clear_active()  # ← ACCESS (Line 180)
        return
    
    # Look up event by ID
    event_index = self._find_event_index_by_id(state['event_id'])
    if event_index < 0:
        self.spinbox_widget.clear_active()  # ← ACCESS (Line 189)
        state['primitive'] = None
        return
    
    # Restore spinbox with current values
    event = self.model.get_events(perspective)[event_index]
    primitive = state['primitive']
    current_value = event.markers[primitive].value
    event_time = event.time
    
    state['event_time'] = event_time  # Update stored time
    
    self.spinbox_widget.set_active_primitive(primitive, current_value, event_time)  # ← ACCESS (Line 204)
```
**Type:** Write (restore state)  
**Pattern:** Single owner pattern (GOOD!)  
**Action Required:** KEEP THIS - This is correct  
**Risk:** None (authoritative logic)

---

#### Access 5: Refresh After Time Shift (Lines 222, 235, 250)
```python
def _refresh_spinbox_after_time_shift(self):
    """Update spinbox time label after insertions shift event times."""
    if not self.spinbox_widget.is_editing():  # ← ACCESS (Line 222)
        return
    
    state = self.active_primitive_state
    event_id = state['event_id']
    
    event_index = self._find_event_index_by_id(event_id)
    if event_index < 0:
        self.spinbox_widget.clear_active()  # ← ACCESS (Line 235)
        state['primitive'] = None
        return
    
    # Get new time and update label
    events = self.model.get_events(self.perspective)
    event = events[event_index]
    new_time = event.time
    
    if abs(new_time - state['event_time']) > 0.01:
        state['event_time'] = new_time
        primitive = state['primitive']
        current_value = event.markers[primitive].value
        self.spinbox_widget.set_active_primitive(primitive, current_value, new_time)  # ← ACCESS (Line 250)
```
**Type:** Write (refresh time label)  
**Pattern:** Single owner pattern (GOOD!)  
**Action Required:** KEEP THIS - This is correct  
**Risk:** None (authoritative logic)

---

#### Access 6: Primitive Selection (Lines 719-720)
```python
def on_primitive_selected(self, event_index: int, primitive: str):
    """User clicked primitive marker in plot."""
    events = self.model.get_events(self.perspective)
    event = events[event_index]
    current_value = event.markers[primitive].value
    event_time = event.time
    
    # Update state
    state = self.active_primitive_state
    state['primitive'] = primitive
    state['event_id'] = event.event_id
    state['event_time'] = event_time
    
    # Update spinbox widget
    if EDITOR_DEBUG:
        _logger.debug(f"Calling spinbox_widget.set_active_primitive({primitive}, {current_value}, {event_time})")
    
    self.spinbox_widget.set_active_primitive(primitive, current_value, event_time)  # ← ACCESS (Line 720)
    
    if EDITOR_DEBUG:
        _logger.debug(f"Spinbox updated, label={self.spinbox_widget.get_active_label_text()}")
```
**Type:** Write (set active primitive)  
**Pattern:** Single owner pattern (GOOD!)  
**Action Required:** KEEP THIS - This is correct  
**Risk:** None (authoritative logic)

---

#### Access 7: Clear on Delete (Line 750)
```python
def _after_delete_event(self, event_id: str):
    """Called after event deletion to clean up spinbox."""
    state = self.active_primitive_state
    
    if state['event_id'] == event_id:
        # Active event was deleted
        self.spinbox_widget.clear_active()  # ← ACCESS (Line 750)
        state['primitive'] = None
        state['event_id'] = None
        state['event_time'] = None
```
**Type:** Write (clear on delete)  
**Pattern:** Single owner pattern (GOOD!)  
**Action Required:** KEEP THIS - This is correct  
**Risk:** None (authoritative logic)

---

#### Access 8: Debug Logging (Lines 206, 722)
```python
# In _restore_spinbox_state_for_perspective
print(f"[SPINBOX_RESTORE] After set_active_primitive, spinbox shows: label='{self.spinbox_widget.get_active_label_text()}', value={self.spinbox_widget.spinbox.value():.1f}")

# In on_primitive_selected
if EDITOR_DEBUG:
    _logger.debug(f"Spinbox updated, label={self.spinbox_widget.get_active_label_text()}")
```
**Type:** Read (query widget state for debugging)  
**Pattern:** Acceptable for debugging  
**Action Required:** KEEP for now, can remove debug logging later  
**Risk:** None (read-only)

---

### 3. tools/editor/widgets/primitive_spinbox_editor.py (WIDGET IMPLEMENTATION)

These are the **widget methods** themselves (not access points). Keep these.

- `set_active_primitive()` (Line 87) - Widget method implementation
- `clear_active()` (Line 112) - Widget method implementation
- `get_active_label_text()` (Line 121) - Widget method implementation
- `update_value()` (Line 125) - Widget method implementation
- `is_editing()` (Line 138) - Widget method implementation

**Action Required:** None - These are the public API of the widget

---

## Migration Strategy

### Phase 2: Add Controller API Methods

**New methods to add:**

```python
# controller.py

def initialize_spinbox_widget(self, widget):
    """Initialize spinbox reference (called once at startup).
    
    Args:
        widget: PrimitiveSpinboxEditor instance
    """
    self._spinbox_widget = widget  # Note: private!
    
    # Connect signal
    widget.value_changed.connect(self.on_spinbox_value_changed)

def update_spinbox_value(self, value: float):
    """Update spinbox value programmatically (called from interactive_editor).
    
    This is for when plot marker is clicked and spinbox should reflect new value.
    
    Args:
        value: New value to display
    """
    if self._spinbox_widget.is_editing():
        self._spinbox_widget.update_value(value)
```

**Rationale:**
- `initialize_spinbox_widget()` replaces signal connection in interactive_editor.py:257
- `update_spinbox_value()` replaces direct widget access in interactive_editor.py:574
- Accesses 3a/3b (perspective switch) will be completely removed (controller already handles via `_restore_spinbox_state_for_perspective`)

---

### Phase 3: Switch Callers

#### Change 1: Initialization
**File:** `tools/interactive_editor.py:257`

**OLD:**
```python
# In __init__
self.spinbox_editor = PrimitiveSpinboxEditor()
self.spinbox_editor.value_changed.connect(self._on_spinbox_value_changed)
```

**NEW:**
```python
# In __init__
self.spinbox_editor = PrimitiveSpinboxEditor()
self.controller.initialize_spinbox_widget(self.spinbox_editor)
```

**Test:** Launch editor, verify spinbox value changes update model.

---

#### Change 2: Value Update on Marker Click
**File:** `tools/interactive_editor.py:574`

**OLD:**
```python
# In _on_primitive_selected_m1/_m2
if is_active:
    self.spinbox_editor.update_value(value)
```

**NEW:**
```python
# In _on_primitive_selected_m1/_m2
if is_active:
    self.controller.update_spinbox_value(value)
```

**Test:** Click primitive marker, verify spinbox updates with correct value.

---

#### Change 3: Perspective Switch Handling
**File:** `tools/interactive_editor.py:1010-1040`

**OLD:**
```python
def _on_perspective_changed(self, perspective):
    self.controller.switch_perspective(perspective)
    
    # Duplicate logic - controller already handles this!
    if self.controller.active_primitive_state['primitive']:
        primitive_name = self.controller.active_primitive_state['primitive']
        event_time = self.controller.active_primitive_state['event_time']
        # ... find event ...
        if matching_event_found:
            self.spinbox_editor.set_active_primitive(primitive_name, new_value, event_time)
        else:
            self.spinbox_editor.clear_active()
```

**NEW:**
```python
def _on_perspective_changed(self, perspective):
    self.controller.switch_perspective(perspective)
    # That's it! Controller handles spinbox restore internally.
```

**Rationale:** Controller's `switch_perspective()` already calls `_restore_spinbox_state_for_perspective()`. The interactive_editor code was redundant and caused the race condition bug.

**Test:** Switch M1→M2→M1, verify spinbox state preserved.

---

### Phase 4: Validation

**Test Checklist:**
- [ ] Launch editor
- [ ] Click primitive marker (verify spinbox shows "Editing: r @ t=7.0")
- [ ] Change spinbox value (verify trajectory updates)
- [ ] Undo change (Ctrl+Z)
- [ ] Click different primitive (verify spinbox updates)
- [ ] Switch to M2 (verify spinbox clears or shows M2 selection)
- [ ] Select primitive in M2
- [ ] Switch back to M1 (verify spinbox restored to M1 selection)
- [ ] Insert event before active primitive (Ctrl+Shift+Click)
- [ ] Verify time label updates (e.g., t=7.0 → t=14.0)
- [ ] Delete active event (verify spinbox clears)
- [ ] Close editor (no crashes)

---

### Phase 5: Cleanup

#### Step 1: Make widget truly private
```python
# controller.py
self._spinbox_widget = None  # Already private!

# interactive_editor.py - REMOVE public access
# Delete or make property that raises:
@property
def spinbox_editor(self):
    raise AttributeError(
        "spinbox_editor is controller-owned. "
        "Use controller methods: update_spinbox_value(), etc."
    )
```

#### Step 2: Remove debug logging
```python
# primitive_spinbox_editor.py - Remove temporary debug prints
def set_active_primitive(self, primitive_name: str, current_value: float, event_time: float = None):
    # Remove: print(f"[SPINBOX_WIDGET] set_active_primitive called...")
    # Keep only: label setting logic
```

#### Step 3: Remove commented old code
Delete any `# OLD PATH:` comments from Phase 3.

#### Step 4: Update documentation
- Mark this file (spinbox_audit_phase1.md) as complete
- Update spinbox_refactor_2025_12.md with "Refactoring Complete" status
- Update ARCHITECTURE.md with new architecture diagram

---

## Risk Assessment

### Low Risk ✅
- **Change 1 (Initialization):** Just moving signal connection, same effect
- **Phase 4 (Validation):** Only testing, no code changes
- **Phase 5 (Cleanup):** Removing dead code and debug logging

### Medium Risk ⚠️
- **Change 2 (Value Update):** Affects user interaction, but straightforward proxy
- **Change 3 (Perspective Switch):** High impact area, but we're REMOVING problematic code

### High Risk ❌
None identified.

**Overall Risk:** **LOW** - Most changes are deletions or simple proxying. The biggest risk area (perspective switching) is being SIMPLIFIED by removing duplicate logic.

---

## Timeline Estimate

- **Phase 1 (Audit):** ✅ Complete (this document)
- **Phase 2 (Add API):** 15 minutes (2 simple methods)
- **Phase 3 (Switch Callers):** 20 minutes (3 changes)
- **Phase 4 (Validation):** 30 minutes (thorough manual testing)
- **Phase 5 (Cleanup):** 15 minutes (remove debug code, update docs)

**Total:** ~80 minutes end-to-end

---

## Success Criteria

**Refactoring succeeds if:**
1. ✅ All 12 test checklist items pass
2. ✅ Only controller.py accesses spinbox widget
3. ✅ interactive_editor.py has zero direct widget access
4. ✅ Code is simpler (fewer lines, clearer intent)
5. ✅ No regressions in existing functionality

**Bonus:**
- If something breaks, we'll discover hidden coupling → good for long-term health
- Tests reveal gaps → we'll add proper tests

---

## Next Steps

1. **Ready for Phase 2:** Add two controller methods
2. **Then Phase 3:** Update 3 call sites in interactive_editor.py
3. **Then Phase 4:** Run full test checklist
4. **Then Phase 5:** Clean up and document

**Current Status:** Phase 1 Complete ✅

---

**Audit Date:** December 15, 2025  
**Auditor:** GitHub Copilot  
**Reviewed By:** Development Team  
**Approved for Phase 2:** ✅ YES
