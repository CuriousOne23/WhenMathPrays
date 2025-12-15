# Spinbox Architecture Refactoring - December 2025

**Status:** Pre-Refactoring Documentation  
**Version:** v2.1.4  
**Date:** December 15, 2025

## Executive Summary

This document captures the state of the Primitive Value Editor (spinbox) architecture before a planned refactoring to single controller ownership. It documents three critical bugs that were fixed, the root cause analysis, and the architectural improvements planned to prevent recurrence.

**Key Achievements:**
- ✅ Fixed time label refresh on event insertions (Ctrl+Shift+Click)
- ✅ Implemented per-perspective state tracking (M1 and M2 independent)
- ✅ Fixed time label preservation on perspective switching

**Key Finding:**
Multiple code paths accessing the same widget led to race conditions and silent state corruption. The fix revealed architectural weakness: lack of single ownership.

---

## Bug Fixes Completed

### Bug 1: Time Label Not Updating on Event Insertions

**Symptom:**
When inserting an event via Ctrl+Shift+Click, event times shift (e.g., t=49 → t=56), but the spinbox label still showed old time:
```
Before insert: "Editing: S @ t=49.0"
After insert:  "Editing: S @ t=49.0"  ← WRONG! Event is now at t=56
```

**Root Cause:**
No mechanism to refresh spinbox label after `_insert_event_before()` shifted event times.

**Fix:**
Added `_refresh_spinbox_after_time_shift()` called after insertions:
```python
# controller.py:1254
self.primitive_panel.update_from_model(events)
self._recompute_trajectory_immediate()
self._refresh_spinbox_after_time_shift()  # NEW
```

The helper checks if active event's time changed and updates label accordingly.

**Files Changed:**
- `tools/editor/controller.py`: Added `_refresh_spinbox_after_time_shift()` method

---

### Bug 2: Perspective Switching Loses Spinbox State

**Symptom:**
Edit primitive in M1 → Switch to M2 → Switch back to M1 → Spinbox shows "(none)" instead of what you were editing.

**Root Cause:**
Single `active_primitive_state` dict shared between perspectives. Switching overwrote M1 state with M2 state.

**Fix:**
Separate state dictionaries for each perspective:
```python
# controller.py:108-118
self.active_primitive_state_m1 = {
    'primitive': None,
    'event_id': None,
    'event_time': None
}
self.active_primitive_state_m2 = {
    'primitive': None,
    'event_id': None,
    'event_time': None
}

@property
def active_primitive_state(self):
    """Get state for current perspective."""
    return self.active_primitive_state_m1 if self.perspective == 'M1' else self.active_primitive_state_m2
```

Added `_restore_spinbox_state_for_perspective()` called during perspective switch.

**Files Changed:**
- `tools/editor/controller.py`: Separate M1/M2 state dicts, restore function

---

### Bug 3: Time Label Lost After Perspective Switch

**Symptom:**
The most subtle bug. Spinbox restored correctly in controller, but UI showed "Editing: f" without time.

**Logs showed:**
```
[SPINBOX_RESTORE] Restored M1 state: f @ t=42.0, value=-3.0  ✅
[SPINBOX_RESTORE] After set_active_primitive, spinbox shows: label='Editing: f @ t=42.0'  ✅
[SPINBOX_WIDGET] set_active_primitive called: prim=f, value=-3.0, time=None  ❌
[SPINBOX_WIDGET] Set label WITHOUT time: 'Editing: f'  ❌
```

Restore worked, then something immediately overwrote it!

**Root Cause:**
`interactive_editor.py` had its own perspective change handler that directly called spinbox widget **after** controller restored it, but without passing `event_time`:

```python
# interactive_editor.py:1025 (BUGGY)
self.spinbox_editor.set_active_primitive(primitive_name, new_value)  # Missing event_time!
```

**Fix:**
Pass the time parameter:
```python
# interactive_editor.py:1025 (FIXED)
self.spinbox_editor.set_active_primitive(primitive_name, new_value, event_time)
```

**Files Changed:**
- `tools/interactive_editor.py`: Added `event_time` parameter to call

**Key Insight:**
This was a **silent failure** because `event_time` had a default value (`= None`). The call was syntactically valid but semantically wrong.

---

## Why These Bugs Were Hard to Trace

### 1. Race Condition Disguise

The restore worked perfectly, logs confirmed it. But then something else overwrote it milliseconds later. The user only saw the final (wrong) state.

**Logs said:** "label='Editing: f @ t=42.0'" (correct!)  
**UI showed:** "Editing: f" (wrong!)

This creates cognitive dissonance - is the log lying? Is Qt not rendering?

### 2. Split Responsibilities

Two files both manipulating the same widget:
- `controller.py`: Has `_restore_spinbox_state_for_perspective()` 
- `interactive_editor.py`: ALSO updates spinbox in `_on_perspective_changed()`

Which one is authoritative? Both? Neither? Unclear ownership.

### 3. Silent Failure via Optional Parameters

```python
def set_active_primitive(self, primitive_name: str, current_value: float, event_time: float = None):
```

The `= None` default made forgetting the parameter **syntactically valid**. No error, no warning, just wrong behavior.

### 4. Call Stack Depth

Bug triggered by:
```
User clicks M1 → _on_perspective_changed() → controller.switch_perspective() 
→ _restore_spinbox_state_for_perspective() → set_active_primitive() [CORRECT]
→ [returns to _on_perspective_changed()] → set_active_primitive() [WRONG]
```

Two calls to the same method in the same operation, one correct and one wrong.

### 5. The Winning Move: Instrument the Widget

The breakthrough came from adding logging **inside the widget itself**:

```python
# primitive_spinbox_editor.py
def set_active_primitive(self, primitive_name: str, current_value: float, event_time: float = None):
    print(f"[SPINBOX_WIDGET] set_active_primitive called: prim={primitive_name}, value={current_value:.1f}, time={event_time}")
```

This revealed:
1. First call: `time=42.0` ✅ (from controller restore)
2. Second call: `time=None` ❌ (from interactive_editor)

Widget-level logging showed **all mutations**, not just high-level intent.

---

## Current Architecture (Pre-Refactor)

### Ownership Diagram

```
┌─────────────────────────┐
│  interactive_editor.py  │
│  _on_perspective_       │──┐
│     changed()           │  │ Both directly
└─────────────────────────┘  │ access widget!
                             ↓
                      ┌──────────────┐
                      │   Spinbox    │
                      │    Widget    │
                      └──────────────┘
                             ↑
┌─────────────────────────┐  │
│   controller.py         │  │
│  on_primitive_          │──┘
│    selected()           │
│  _restore_spinbox...()  │
└─────────────────────────┘
```

**Problem:** Two owners = race conditions, unclear responsibility, hard to debug.

### Code Paths to Spinbox

**Path 1: User clicks primitive marker**
```
interactive_editor._on_marker_clicked() 
→ controller.on_primitive_selected()
→ spinbox_widget.set_active_primitive()
```

**Path 2: User switches perspective**
```
interactive_editor._on_perspective_changed()
→ controller.switch_perspective()
→ controller._restore_spinbox_state_for_perspective()
→ spinbox_widget.set_active_primitive()  ✅

→ [BACK TO interactive_editor._on_perspective_changed()]
→ spinbox_editor.set_active_primitive()  ❌ (This was the bug!)
```

**Path 3: User changes value via spinbox**
```
spinbox_widget.value_changed (signal)
→ controller.on_spinbox_value_changed()
→ controller.on_primitive_changed()
→ model.update_primitive()
```

### Current State Storage

```python
# controller.py
self.active_primitive_state_m1 = {
    'primitive': 'f',     # Which primitive
    'event_id': 6,        # Permanent event ID (not index!)
    'event_time': 42.0    # Time for label display
}

self.active_primitive_state_m2 = {
    'primitive': 'a',
    'event_id': 16,
    'event_time': 35.0
}

@property
def active_primitive_state(self):
    """Returns M1 or M2 state based on current perspective."""
    return self.active_primitive_state_m1 if self.perspective == 'M1' else self.active_primitive_state_m2
```

### Files Involved

**Core Files:**
- `tools/editor/controller.py`: Main business logic, state management
- `tools/interactive_editor.py`: Main window, UI orchestration
- `tools/editor/widgets/primitive_spinbox_editor.py`: Spinbox widget

**Related Files:**
- `tools/editor/model.py`: Data model (events, primitives)
- `tools/editor/commands.py`: Undo/redo commands
- `tools/editor/views/primitive_panel_pyqtgraph.py`: Primitive plots

---

## Lessons Learned

### 1. Optional Parameters Hide Bugs

**Bad:**
```python
def set_active_primitive(self, prim: str, value: float, time: float = None):
```

Calling without `time` is valid but wrong. Silent failure.

**Better:**
```python
def set_active_primitive(self, prim: str, value: float, time: float):
```

Calling without `time` = compilation error. Fail fast.

**Best:**
```python
def set_active_primitive_with_time(self, prim: str, value: float, time: float):
def set_active_primitive_no_time(self, prim: str, value: float):  # Rare cases only
```

Intent is explicit. No ambiguity.

### 2. Multiple Owners = Hidden Coupling

If two files can modify the same widget:
- Which one is authoritative?
- What's the update order?
- Who's responsible for validation?
- How do you debug race conditions?

**Solution:** Single owner pattern. Controller owns all widget access.

### 3. Instrument the Victim, Not the Perpetrator

When logs and UI disagree, add logging at the **lowest level** (the widget), not the high level (controller).

The widget sees **all mutations**, regardless of who triggered them.

### 4. Test What You Can Break

We had no test for:
```python
def test_spinbox_time_preserved_on_perspective_switch():
    controller.on_primitive_selected(6, 'f')
    assert spinbox.label == "Editing: f @ t=42.0"
    
    controller.switch_perspective('M2')
    controller.switch_perspective('M1')
    
    assert spinbox.label == "Editing: f @ t=42.0"  # Would fail before fix
```

If it can break, test it. If you don't test it, it will break.

### 5. Technical Debt Compounds

**Timeline of this bug:**

1. **Initial implementation:** Controller-owned spinbox (clean)
2. **Feature added:** Perspective switching needs to update spinbox
3. **Quick fix:** Add code to `interactive_editor.py` (shortcut taken)
4. **Time passes:** Pattern becomes "normal"
5. **Bug manifests:** Time label lost (mysterious)
6. **Debug cost:** Hours to trace, multiple developers confused

**Lesson:** The cost of fixing the architecture at step 3 was 10 minutes. The cost at step 6 was hours. Debt accrues interest.

---

## Planned Refactoring

### Goal: Single Controller Ownership

**Objective:** Controller is the ONLY code that accesses spinbox widget.

**Benefits:**
- ✅ Clear ownership (controller)
- ✅ Single code path to debug
- ✅ Easier to test (mock widget, test controller)
- ✅ Prevents this entire class of bugs
- ✅ Consistent state management

### Target Architecture

```
┌─────────────────────────┐
│  interactive_editor.py  │
│  (UI orchestration)     │
└─────────────────────────┘
           │
           │ Calls controller API only
           ↓
┌─────────────────────────┐
│   controller.py         │ ← SINGLE OWNER
│  (all spinbox logic)    │
└─────────────────────────┘
           │
           │ Private reference
           ↓
     ┌──────────────┐
     │   Spinbox    │
     │    Widget    │
     └──────────────┘
```

### Five-Phase Implementation

#### Phase 1: Audit (No Changes)

**Goal:** Find all spinbox access points.

**Tasks:**
```bash
grep -r "spinbox_editor\." tools/
grep -r "spinbox_widget\." tools/
grep -r "set_active_primitive" tools/
```

**Deliverable:** Complete list of files and line numbers that access spinbox.

**Expected locations:**
- `interactive_editor.py`: Main window setup, perspective changes
- `controller.py`: Primitive selection, state restore
- Others?

#### Phase 2: Add Controller API (Additive Only)

**Goal:** Create new methods on controller, don't remove anything yet.

**New methods:**
```python
# controller.py
def set_spinbox_widget(self, widget):
    """Initialize spinbox reference (called once during startup)."""
    self._spinbox_widget = widget  # Note: private reference

def update_spinbox_for_perspective_change(self, new_perspective):
    """Handle spinbox update when perspective changes.
    
    Called by interactive_editor after switch_perspective().
    Replaces direct widget access from interactive_editor.
    """
    state = self.active_primitive_state_m1 if new_perspective == 'M1' else self.active_primitive_state_m2
    
    if state['primitive'] is None:
        self._spinbox_widget.clear_active()
        return
    
    event_id = state['event_id']
    event_index = self._find_event_index_by_id(event_id)
    
    if event_index < 0:
        # Event was deleted
        self._spinbox_widget.clear_active()
        state['primitive'] = None
        return
    
    events = self.model.get_events(new_perspective)
    event = events[event_index]
    primitive = state['primitive']
    value = event.markers[primitive].value
    time = event.time
    
    # Update stored time (may have changed)
    state['event_time'] = time
    
    # Update widget
    self._spinbox_widget.set_active_primitive(primitive, value, time)
```

**Testing:** New methods exist but aren't called yet. Old code still works.

#### Phase 3: Switch Callers (One at a Time)

**Goal:** Replace direct widget access with controller API calls.

**Change in interactive_editor.py:**
```python
def _on_perspective_changed(self, perspective):
    self.controller.switch_perspective(perspective)
    
    # OLD PATH (comment out, don't delete yet):
    # if self.controller.active_primitive_state['primitive']:
    #     primitive_name = self.controller.active_primitive_state['primitive']
    #     event_time = self.controller.active_primitive_state['event_time']
    #     new_events = self.model.get_events(perspective)
    #     # ... find event and call spinbox ...
    #     self.spinbox_editor.set_active_primitive(primitive_name, new_value, event_time)
    
    # NEW PATH:
    self.controller.update_spinbox_for_perspective_change(perspective)
```

**Testing after this change:**
- Switch perspectives M1 → M2 → M1
- Verify spinbox preserves state
- Check logs for any errors

#### Phase 4: Validate (Thorough Testing)

**Test scenarios:**
1. **Primitive editing:**
   - Click primitive marker
   - Change value via spinbox
   - Verify trajectory updates

2. **Perspective switching:**
   - Edit in M1
   - Switch to M2
   - Switch back to M1
   - Verify spinbox restored

3. **Event insertions:**
   - Click primitive
   - Insert event before it (Ctrl+Shift+Click)
   - Verify time label updates

4. **Undo/redo:**
   - Edit primitive
   - Undo (Ctrl+Z)
   - Redo (Ctrl+Y)
   - Verify spinbox state

5. **Event deletion:**
   - Select event with active spinbox
   - Delete event
   - Verify spinbox clears

**Success criteria:**
- All test scenarios pass
- No errors in console
- Behavior matches pre-refactor

#### Phase 5: Cleanup

**Tasks:**
1. **Remove direct spinbox access from interactive_editor:**
   ```python
   # Remove or make private
   # self.spinbox_editor = PrimitiveSpinboxEditor()
   
   @property
   def spinbox_editor(self):
       raise AttributeError("spinbox_editor is controller-owned. Use controller API.")
   ```

2. **Make controller reference truly private:**
   ```python
   # controller.py
   self._spinbox_widget = None  # Leading underscore = private
   ```

3. **Remove old commented code**

4. **Update documentation:**
   - Update ARCHITECTURE.md
   - Add docstrings to new methods
   - Update this file with "Refactoring Complete" status

5. **Add regression tests:**
   ```python
   def test_spinbox_single_ownership():
       """Ensure only controller accesses spinbox."""
       # This test verifies the architectural constraint
       # by checking that spinbox_widget is private
       assert hasattr(controller, '_spinbox_widget')
       assert not hasattr(interactive_editor, 'spinbox_editor')
   ```

---

## Testing Strategy

### Manual Testing Checklist

Before tagging and after each phase:

- [ ] Launch editor with romeo_juliet_M1.csv
- [ ] Click primitive marker (r at t=7)
- [ ] Verify spinbox shows "Editing: r @ t=7.0"
- [ ] Change value to -5.0
- [ ] Verify trajectory updates
- [ ] Switch to M2
- [ ] Verify spinbox clears (no M2 selection yet)
- [ ] Click primitive in M2 (a at t=14)
- [ ] Switch back to M1
- [ ] Verify spinbox shows "Editing: r @ t=7.0" (restored)
- [ ] Click event at t=0
- [ ] Ctrl+Shift+Click to insert before t=7
- [ ] Verify spinbox time updates to t=14.0 (shifted)
- [ ] Undo (Ctrl+Z)
- [ ] Verify spinbox time returns to t=7.0
- [ ] Close editor (no crashes)

### Automated Testing (Future)

**Unit tests needed:**
```python
# tests/test_spinbox_controller.py

def test_spinbox_state_per_perspective():
    """Each perspective maintains independent spinbox state."""
    controller = EditorController(model)
    mock_spinbox = MockSpinbox()
    controller.set_spinbox_widget(mock_spinbox)
    
    # Select in M1
    controller.perspective = 'M1'
    controller.on_primitive_selected(6, 'f')
    assert controller.active_primitive_state_m1['primitive'] == 'f'
    
    # Switch to M2
    controller.switch_perspective('M2')
    assert controller.active_primitive_state_m2['primitive'] is None
    
    # Select in M2
    controller.on_primitive_selected(5, 'a')
    assert controller.active_primitive_state_m2['primitive'] == 'a'
    
    # Switch back to M1
    controller.switch_perspective('M1')
    assert controller.active_primitive_state_m1['primitive'] == 'f'  # Preserved!

def test_spinbox_time_updates_on_insertion():
    """Spinbox time label updates when events shift."""
    controller = EditorController(model)
    mock_spinbox = MockSpinbox()
    controller.set_spinbox_widget(mock_spinbox)
    
    # Select event at t=49
    controller.on_primitive_selected(7, 'S')
    assert mock_spinbox.label == "Editing: S @ t=49.0"
    
    # Insert event before it (causes shift to t=56)
    controller._insert_event_before(7, 42.0, 7.0)
    
    # Time label should update
    assert mock_spinbox.label == "Editing: S @ t=56.0"

def test_spinbox_single_owner():
    """Only controller can access spinbox (architectural constraint)."""
    controller = EditorController(model)
    interactive_editor = InteractiveEditor(controller, model)
    
    # Controller has private reference
    assert hasattr(controller, '_spinbox_widget')
    
    # Interactive editor does NOT have direct access
    with pytest.raises(AttributeError):
        _ = interactive_editor.spinbox_editor
```

---

## Risk Assessment

### Low Risk ✅
- Adding new controller methods (Phase 2)
- Commenting out old code (Phase 3)
- Adding logging/debugging

### Medium Risk ⚠️
- Changing call sites (Phase 3)
- Removing old code (Phase 5)

**Mitigation:** Test thoroughly after each change. Keep git commits small.

### High Risk ❌
None identified. Refactoring is localized to spinbox only.

### What Could Go Wrong?

**Scenario 1: Forget to call controller method**
```python
# interactive_editor.py - WRONG
def _on_perspective_changed(self, perspective):
    self.controller.switch_perspective(perspective)
    # Forgot: self.controller.update_spinbox_for_perspective_change(perspective)
```

**Result:** Spinbox doesn't update on perspective switch.

**Detection:** Manual testing catches immediately (spinbox doesn't change).

**Fix:** Add the missing call.

---

**Scenario 2: Breaking existing functionality**

**Example:** Undo/redo stops working for spinbox edits.

**Detection:** Manual testing or automated tests.

**Analysis:** If this breaks, it reveals we didn't understand the undo system properly. Good to find out now!

**Fix:** Debug properly, add test to prevent regression.

---

**Scenario 3: Qt signal timing issues**

**Example:** Widget updates before model updates.

**Detection:** Logs show wrong order of operations.

**Fix:** Ensure controller methods are called in correct order. Qt signals are synchronous by default, so timing should be predictable.

---

## Success Metrics

**Refactoring is successful if:**

1. ✅ All manual tests pass
2. ✅ No regressions in existing functionality
3. ✅ Code is simpler (fewer lines, clearer intent)
4. ✅ Only one file accesses spinbox widget
5. ✅ Future bugs are easier to debug
6. ✅ Team confidence increases

**Refactoring revealed problems if:**

1. Something breaks that we didn't know could break → Good! Hidden coupling revealed.
2. Tests fail → Good! Tests doing their job.
3. Architecture is messier than expected → Good! Now we know the real scope.

**Either outcome improves the codebase.**

---

## References

### Code Locations

**Bug fixes (v2.1.4):**
- `tools/editor/controller.py:108-133` - Per-perspective state dicts
- `tools/editor/controller.py:159-210` - Restore and refresh functions  
- `tools/interactive_editor.py:1025` - Added event_time parameter

**Current spinbox access points:**
- `tools/interactive_editor.py:1025` - Direct widget access (to be removed)
- `tools/editor/controller.py:720` - Proper controller access (keep)

**Widget implementation:**
- `tools/editor/widgets/primitive_spinbox_editor.py`

### Related Documentation

- `ARCHITECTURE.md` - Overall system architecture
- `docs/architecture/refactors/2025-12-07_ui_architecture_cleanup.md` - Previous refactoring
- `docs/interactive_editor_user_guide.md` - User-facing documentation

---

## Timeline

**December 14-15, 2025:**
- Bug reported: Time label missing on perspective switch
- Root cause identified: Multiple code paths to widget
- Three bugs fixed: Time refresh, per-perspective state, time preservation
- Documentation created (this file)

**Next Steps:**
- Tag: `v2.1.4-spinbox-fixes`
- Phase 1: Audit (find all access points)
- Phase 2-5: Refactor to single ownership
- Final tag: `v2.2.0-spinbox-refactor` (when complete)

---

## Conclusion

The spinbox bugs revealed a fundamental architectural issue: **multiple owners**. While the immediate bugs are fixed, the architecture remains fragile. The planned refactoring to single controller ownership will:

1. **Prevent recurrence** - Can't have race conditions with only one owner
2. **Improve debuggability** - One code path to trace
3. **Enable testing** - Clear interface to mock and test
4. **Build confidence** - Team knows the system is sound

**The bugs were a gift.** They showed us the weakness before it became a crisis. Now we can fix it properly.

---

**Document Status:** ✅ Complete  
**Next Action:** Git tag `v2.1.4-spinbox-fixes`  
**Owner:** Development Team  
**Review Date:** After Phase 5 completion
