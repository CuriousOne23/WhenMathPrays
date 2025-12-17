# Interactive Editor Testing Strategy

**Date:** December 14, 2025  
**Status:** Testing framework documentation  
**Related:** [INTERACTIVE_EDITOR_CHANGELOG.md](INTERACTIVE_EDITOR_CHANGELOG.md), [ARCHITECTURE.md](../ARCHITECTURE.md), [DEBUG.md](DEBUG.md)

---

## Overview

This document outlines the testing strategy for the Interactive Editor, from core logic validation to end-to-end workflow testing. The goal is to ensure software quality without over-engineering test infrastructure.

**Debugging and Logging:** For detailed logging configuration, debug flags, and troubleshooting techniques, see [DEBUG.md](DEBUG.md).

**All features follow the MVT quality standard** (see [ARCHITECTURE.md](../ARCHITECTURE.md#mvt-quality-standard)):
- **Modeled:** Clean architecture, follows patterns
- **Verifiable:** Observable behavior, clear success criteria
- **Testable:** Test cases ensure correctness and prevent regressions

**Testing Philosophy:**
- Start simple (core logic tests)
- Add complexity only when needed (command tests, GUI tests)
- Manual testing is acceptable for UI workflows
- Automated tests should be fast, reliable, and maintainable

---

## Testing Tiers

### Tier 1: Core Logic Tests (Highest Priority)

**What:** Test model and controller logic without GUI  
**Why:** Fast, reliable, high value - catches most bugs  
**When:** Before every major feature or release  
**Time to implement:** 3-4 hours

**Test Coverage:**
- Model primitive modifications
- Baseline tracking and reset
- Perspective isolation (M1/M2 separation)
- Modification tracking (is_modified)
- Event operations (delete, insert)

**Location:** `tests/editor/test_model.py`, `tests/editor/test_controller.py`, `tests/editor/test_perspective_isolation.py`

**Example Tests:**
```python
def test_modify_primitive_updates_events():
    """Verify primitive modification changes event values"""
    
def test_is_modified_tracks_changes():
    """Verify is_modified correctly detects changes"""
    
def test_reset_primitive_restores_baseline():
    """Verify reset restores original value"""
    
def test_m1_modifications_invisible_in_m2():
    """Verify perspective isolation works"""
```

**Run with:**
```bash
pytest tests/editor/ -v
```

---

### Tier 2: Command Pattern Tests (Medium Priority)

**What:** Test undo/redo without GUI  
**Why:** Critical for editor reliability  
**When:** After Tier 1 complete, or if undo bugs discovered  
**Time to implement:** 2-3 hours

**Test Coverage:**
- EditPrimitiveCommand undo/redo
- ResetPrimitiveCommand undo/redo
- DeleteEventCommand undo/redo
- InsertEventCommand undo/redo
- Undo stack switching between perspectives

**Location:** `tests/editor/test_commands.py`

**Example Tests:**
```python
def test_edit_primitive_undo_redo():
    """Verify undo/redo for primitive edits"""
    
def test_delete_event_undo_redo():
    """Verify event deletion can be undone"""
    
def test_undo_stack_switches_with_perspective():
    """Verify M1 and M2 have separate undo stacks"""
```

**Run with:**
```bash
pytest tests/editor/test_commands.py -v
```

---

### Tier 3: Manual Integration Tests (Critical Workflows)

**What:** Manual testing with documented checklist  
**Why:** GUI testing is complex/brittle, manual catches UI issues better  
**When:** Before demos, releases, or major changes  
**Time to complete:** 15-20 minutes per run

**Test Checklist:**

#### M1 Save/Load Workflow
- [ ] Load M1 CSV: `python tools/interactive_editor.py data/library/love/single_dating_to_love_M1.csv`
- [ ] Modify primitive (drag marker on Volatility at day 7)
- [ ] Save file (Ctrl+S or File → Save)
- [ ] Close editor
- [ ] Reopen same file
- [ ] **Verify:** Volatility marker at day 7 is at modified position

#### M2 Save/Load Workflow
- [ ] Load M2 CSV: `python tools/interactive_editor.py data/library/love/single_dating_to_love_M2.csv`
- [ ] Switch to M2 perspective (toolbar button)
- [ ] Modify primitive (drag marker on Resonance at day 14)
- [ ] Save file (Ctrl+S)
- [ ] Close editor
- [ ] Reopen same file
- [ ] Switch to M2 perspective
- [ ] **Verify:** Resonance marker at day 14 is at modified position

#### Dual-Perspective Isolation
- [ ] Load M1 CSV
- [ ] Modify Volatility at day 7 (drag marker up)
- [ ] Switch to M2 perspective
- [ ] **Verify:** Volatility at day 7 is at baseline (NOT modified position)
- [ ] Modify Resonance at day 14 in M2
- [ ] Switch to M1 perspective
- [ ] **Verify:** Resonance at day 14 is at baseline (NOT modified position)
- [ ] Switch back to M2
- [ ] **Verify:** Resonance modification still present in M2

#### Undo/Redo Workflow
- [ ] Load M1 CSV
- [ ] Modify Volatility at day 7 (drag up)
- [ ] **Verify:** Marker shows red (modified state)
- [ ] Ctrl+Z (undo)
- [ ] **Verify:** Marker returns to baseline, no longer red
- [ ] Ctrl+Y (redo)
- [ ] **Verify:** Marker returns to modified position, red again

#### Perspective Undo Stack Switching
- [ ] Load M1 CSV
- [ ] Modify primitive in M1
- [ ] Switch to M2 perspective
- [ ] **Verify:** Undo (Ctrl+Z) is disabled (empty M2 stack)
- [ ] Modify primitive in M2
- [ ] **Verify:** Undo (Ctrl+Z) now enabled
- [ ] Switch to M1
- [ ] **Verify:** Undo still enabled (M1 stack preserved)

#### Window Layout Persistence
- [ ] Launch editor
- [ ] Resize docks to custom layout
- [ ] Close editor
- [ ] Reopen editor
- [ ] **Verify:** Layout restored (or defaults applied - acceptable)

#### Reset to Baseline
- [ ] Load M1 CSV
- [ ] Modify Volatility at day 7
- [ ] Double-click marker
- [ ] **Verify:** Marker returns to baseline, no longer red
- [ ] Ctrl+Z (undo the reset)
- [ ] **Verify:** Marker returns to modified position, red again

#### Insert Event
- [ ] Load M1 CSV
- [ ] Right-click between two events on trajectory
- [ ] Select "Insert Event Before..."
- [ ] **Verify:** New event appears, primitives interpolated
- [ ] Ctrl+Z (undo insert)
- [ ] **Verify:** Event removed, trajectory restored

#### Delete Event
- [ ] Load M1 CSV with 5+ events
- [ ] Right-click event marker (not first or last)
- [ ] Select "Delete Event"
- [ ] **Verify:** Event removed from all plots
- [ ] Ctrl+Z (undo delete)
- [ ] **Verify:** Event restored to all plots

**Location:** Document checklist here or in `tests/editor/MANUAL_TEST_CHECKLIST.md`

**Completion Log:**
```
Date: YYYY-MM-DD
Tester: [Name]
Version: v2.2.1
All checks passed: Yes/No
Issues found: [List any failures]
```

---

### Tier 4: Automated GUI Tests (Low Priority - Optional)

**What:** Automated UI testing with pytest-qt  
**Why:** Catches regressions in GUI interactions  
**When:** Only if manual testing becomes too time-consuming  
**Time to implement:** 8-12 hours (complex, brittle)

**Not recommended initially** because:
- Manual testing is faster for current needs
- GUI tests are brittle (break with UI changes)
- High maintenance burden
- Better to focus on scenario development

**If needed later:**
- Use `pytest-qt` framework
- Test click/drag interactions
- Verify panel updates
- Mock file I/O operations

---

## Current Testing Status

### Existing Tests ✅
- **82 tests passing** (likely core math: `revenge_core.py`, `love.py`)
- Test infrastructure in place (`pytest.ini`, `tests/` directory)
- Conftest fixtures available

### Tests to Add 🔄

**Tier 1 (This Week - Before Scenario Work):**
- [ ] `tests/editor/test_model.py` - Model operations
- [ ] `tests/editor/test_perspective_isolation.py` - M1/M2 separation
- [ ] `tests/editor/MANUAL_TEST_CHECKLIST.md` - Document critical workflows
- [ ] Run manual checklist, log results

**Tier 2 (After Scenario Work - If Needed):**
- [ ] `tests/editor/test_commands.py` - Undo/redo validation

**Tier 4 (Much Later - If Ever):**
- [ ] `tests/editor/test_gui.py` - Automated UI tests (skip for now)

---

## Running Tests

### All Tests
```bash
pytest tests/ -v
```

### Specific Test File
```bash
pytest tests/editor/test_model.py -v
```

### Single Test Function
```bash
pytest tests/editor/test_model.py::test_modify_primitive_updates_events -v
```

### With Coverage Report
```bash
pytest tests/ --cov=tools/editor --cov-report=html
```

### Run Only Editor Tests
```bash
pytest tests/editor/ -v
```

---

## Test Data Files

**Location:** `tests/data/`

**Test Scenarios:**
- `test_simple_3_events.csv` - Minimal scenario for unit tests
- `test_m1_scenario.csv` - M1 perspective test data
- `test_m2_scenario.csv` - M2 perspective test data
- `test_dual_perspective.csv` - Both M1 and M2 columns

**Creating Test Data:**
```python
# Minimal CSV for testing
import pandas as pd

data = {
    'event_day': [0.0, 7.0, 14.0],
    'v': [0.5, 0.6, 0.7],
    'r': [0.5, 0.6, 0.7],
    'f': [0.8, 0.9, 0.9],
    'a': [0.4, 0.5, 0.6],
    'S': [0.5, 0.6, 0.7],
    'gamma_self': [-8+0j, 10+20j, 25+45j]
}
df = pd.DataFrame(data)
df.to_csv('tests/data/test_simple_3_events.csv', index=False)
```

---

## Test Implementation Guide

### Writing a New Test

**1. Create test file:**
```bash
# In tests/editor/
touch test_new_feature.py
```

**2. Import dependencies:**
```python
import pytest
from tools.editor.model import EditorModel
from tools.editor.controller import EditorController
```

**3. Write test function:**
```python
def test_feature_behavior():
    """Test description of what this validates"""
    # Arrange: Set up test conditions
    model = EditorModel()
    model.load_from_csv('tests/data/test_simple_3_events.csv')
    
    # Act: Perform the action being tested
    model.modify_primitive(event_idx=1, primitive='v', value=0.9)
    
    # Assert: Verify expected outcomes
    assert model.events[1]['v'] == 0.9
    assert model.is_modified(1, 'v')
```

**4. Run the test:**
```bash
pytest tests/editor/test_new_feature.py -v
```

### Using Fixtures

**Shared test setup:**
```python
# In tests/editor/conftest.py
import pytest
from tools.editor.model import EditorModel

@pytest.fixture
def simple_model():
    """Provide a model with 3 events for testing"""
    model = EditorModel()
    model.load_from_csv('tests/data/test_simple_3_events.csv')
    return model

# In test file:
def test_with_fixture(simple_model):
    """Use the fixture instead of creating model manually"""
    simple_model.modify_primitive(1, 'v', 0.9)
    assert simple_model.events[1]['v'] == 0.9
```

---

## Integration with CI/CD

**Future: Automated Testing on Commit**

Once tests are stable, add GitHub Actions workflow:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
```

**Benefits:**
- Catch regressions before merge
- Validate on multiple Python versions
- Ensure dependencies install correctly

**Recommendation:** Add CI after Tier 1 tests are stable.

---

## Testing Best Practices

### DO:
- ✅ Test behavior, not implementation
- ✅ Use descriptive test names
- ✅ Keep tests independent (no shared state)
- ✅ Test edge cases (empty, zero, boundary values)
- ✅ Document test purpose in docstring
- ✅ Run tests before committing changes

### DON'T:
- ❌ Test private methods directly
- ❌ Hard-code file paths (use fixtures)
- ❌ Write tests that depend on test order
- ❌ Skip failing tests without documenting why
- ❌ Over-mock (test real behavior when possible)

---

## Troubleshooting Test Failures

### Test can't find modules
```bash
# Add project root to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/Mac
$env:PYTHONPATH="$(pwd);$env:PYTHONPATH"  # Windows PowerShell
```

### Test data files not found
```bash
# Verify working directory
pytest tests/editor/ -v --tb=short
# Use absolute paths or path.join in test setup
```

### Qt/GUI tests hang
```bash
# Use QTest for GUI testing
from pytestqt.qtbot import QtBot

def test_gui(qtbot):
    widget = MyWidget()
    qtbot.addWidget(widget)
    qtbot.mouseClick(widget.button, Qt.LeftButton)
```

### Import errors
```bash
# Verify dependencies installed
pip install -r requirements.txt
# Check for circular imports in code
```

---

## Related Documentation

- **[INTERACTIVE_EDITOR_CHANGELOG.md](INTERACTIVE_EDITOR_CHANGELOG.md)** - Version history and feature additions
- **[ARCHITECTURE.md](../ARCHITECTURE.md)** - Overall system architecture
- **[DEBUG.md](DEBUG.md)** - Debugging methodology and troubleshooting
- **[04_API_CONTRACTS.md](architecture/04_API_CONTRACTS.md)** - API specifications with expected behavior
- **[STATE_MANAGEMENT_REFACTORING.md](STATE_MANAGEMENT_REFACTORING.md)** - State management testing examples

---

## Appendix: Test Examples

### Example: Test Model Perspective Isolation

```python
# tests/editor/test_perspective_isolation.py
import pytest
from tools.editor.model import EditorModel

@pytest.fixture
def dual_model():
    """Model with both M1 and M2 data"""
    model = EditorModel()
    model.load_from_csv('tests/data/test_dual_perspective.csv')
    return model

def test_m1_modifications_invisible_in_m2(dual_model):
    """M1 modifications should not affect M2 view"""
    # Modify in M1
    dual_model.modify_primitive_m1(event_idx=5, primitive='v', value=0.9)
    
    # Check M1 sees modification
    assert dual_model.is_modified_m1(5, 'v')
    assert dual_model.events_m1[5]['v'] == 0.9
    
    # Check M2 does NOT see modification
    assert not dual_model.is_modified_m2(5, 'v')
    assert dual_model.events_m2[5]['v'] != 0.9

def test_m2_modifications_invisible_in_m1(dual_model):
    """M2 modifications should not affect M1 view"""
    # Modify in M2
    dual_model.modify_primitive_m2(event_idx=5, primitive='r', value=0.8)
    
    # Check M2 sees modification
    assert dual_model.is_modified_m2(5, 'r')
    assert dual_model.events_m2[5]['r'] == 0.8
    
    # Check M1 does NOT see modification
    assert not dual_model.is_modified_m1(5, 'r')
    assert dual_model.events_m1[5]['r'] != 0.8
```

### Example: Test Command Undo/Redo

```python
# tests/editor/test_commands.py
import pytest
from PySide6.QtGui import QUndoStack
from tools.editor.model import EditorModel
from tools.editor.commands import EditPrimitiveCommand

@pytest.fixture
def model_with_undo():
    """Model with undo stack"""
    model = EditorModel()
    model.load_from_csv('tests/data/test_simple_3_events.csv')
    undo_stack = QUndoStack()
    return model, undo_stack

def test_edit_primitive_undo_redo(model_with_undo):
    """Verify undo/redo cycle restores state correctly"""
    model, undo_stack = model_with_undo
    
    original_value = model.events[1]['v']
    new_value = 0.9
    
    # Execute command
    cmd = EditPrimitiveCommand(model, 1, 'v', new_value)
    undo_stack.push(cmd)
    
    assert model.events[1]['v'] == new_value
    assert model.is_modified(1, 'v')
    
    # Undo
    undo_stack.undo()
    assert model.events[1]['v'] == original_value
    assert not model.is_modified(1, 'v')
    
    # Redo
    undo_stack.redo()
    assert model.events[1]['v'] == new_value
    assert model.is_modified(1, 'v')
```

---

**Last Updated:** December 14, 2025  
**Document Status:** Active - Testing framework definition  
**Next Review:** After Tier 1 tests implemented
