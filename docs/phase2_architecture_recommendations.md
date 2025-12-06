# Phase 2 Architecture Recommendations

**Date:** December 5, 2025  
**Context:** Phase 1 interactive editor completed successfully. This document outlines architectural considerations for Phase 2+ development.

---

## Current Architecture Assessment

### Phase 1 - What Works Well ✅

**Strengths:**
- **Centralized LAYOUT system** - All positioning constants in one dictionary, easy to adjust
- **Clean MVC separation** - Model (`EditorModel`), View (`PrimitivePanel`, `TrajectoryPanel`), Controller (`EditorController`) are properly separated
- **Well-documented** - Comprehensive user guide and inline comments
- **Reliable** - No major bugs, stable for Phase 1 scope
- **Maintainable** - Future developers can understand and modify the code

**Current Stack:**
- Python 3.8+ with matplotlib for visualization
- CSV-based data persistence
- Custom matplotlib widgets for UI controls

### Phase 1 - Known Limitations ⚠️

**1. Matplotlib UI Constraints**
- **Issue:** Matplotlib is designed for plotting, not complex user interfaces
- **Impact:** 
  - Adding dropdown menus, checkboxes, text inputs is awkward
  - Layout system (LAYOUT dictionary) is functional but has limitations
  - Custom widgets (Save button) require hacky workarounds using `matplotlib.widgets`
  - No native support for dialogs, forms, or multi-window interfaces

**2. Event Management**
- **Issue:** Events stored in simple list with manual tracking
- **Impact:**
  - No undo/redo functionality
  - No change history or audit trail
  - Batch operations (e.g., delete multiple events) require custom code
  - Event validation is ad-hoc

**3. Configuration System**
- **Issue:** Settings hardcoded in LAYOUT dictionary
- **Impact:**
  - Users cannot customize without editing code
  - No persistent user preferences
  - Cannot save/load editor state
  - Weights, colors, defaults not easily configurable

---

## Phase 2+ Requirements & Challenges

### Planned Phase 2 Features (from future_interactive_edit_requirements.md)

1. **Dual-perspective editing (M1 & M2)**
   - Toggle between perspectives
   - Side-by-side comparison view
   - Synchronized scrolling/zooming

2. **Add/delete time points**
   - UI forms for adding new events
   - Confirmation dialogs for deletion
   - Timeline manipulation

3. **Inverse editing**
   - Drag gamma_self trajectory to suggest primitives
   - Constraint solver UI
   - Real-time feasibility feedback

4. **Automated sensitivity analysis**
   - Progress bars for batch processing
   - Results table/grid display
   - Export controls

### Why Current Architecture Will Struggle

**Matplotlib Limitations:**
- **Dropdown menus** (perspective toggle) - No native support, would need custom implementation
- **Forms/dialogs** (add event, delete confirmation) - Requires separate Tkinter windows or custom matplotlib hacks
- **Table displays** (sensitivity results) - Matplotlib tables are static and limited
- **Progress bars** - Not designed for this, would be very hacky
- **Multi-window** (comparison views) - Matplotlib figures are independent, hard to coordinate

**Event Management Needs:**
- Undo/redo stack for complex editing operations
- Transaction-based changes (add/delete/modify as atomic operations)
- Change history for debugging and audit
- Validation rules engine

**Configuration Needs:**
- User preference persistence (JSON/YAML)
- Profile-based settings (different users, different scenarios)
- Runtime customization without code changes

---

## Recommendations

### Option 1: Migrate to Qt Framework (Recommended for Phase 2) ✅

**Why Qt (PyQt5 or PySide6):**
- **Mature GUI framework** - Designed for complex applications
- **Rich widget library** - Native dropdowns, forms, dialogs, tables, progress bars
- **Flexible layout system** - QHBoxLayout, QVBoxLayout, QGridLayout, QSplitter
- **Matplotlib integration** - Can embed matplotlib plots as widgets using `FigureCanvasQTAgg`
- **Multi-window support** - Easy to create comparison views, dialogs
- **Professional appearance** - Native look and feel on all platforms
- **Active community** - Extensive documentation and examples

**Migration Effort:** ~15-20 hours
- 5-7 hours: Port main window and layout
- 3-5 hours: Integrate matplotlib plots as Qt widgets
- 3-5 hours: Implement new widgets (menus, forms)
- 2-3 hours: Testing and polish

**Benefits:**
- All Phase 2 features become straightforward to implement
- Much easier to add new UI elements
- Better user experience
- More maintainable long-term

**Drawbacks:**
- New dependency (PyQt5/PySide6)
- Learning curve if unfamiliar with Qt
- More complex build/packaging

**Implementation Strategy:**
1. Create new Qt main window
2. Embed matplotlib plots as `FigureCanvasQTAgg` widgets
3. Port LAYOUT system to Qt layouts (QHBoxLayout, etc.)
4. Reuse model and controller classes (minimal changes)
5. Add new UI elements as needed

### Option 2: Hybrid Matplotlib + Tkinter (Intermediate Solution)

**Why Hybrid:**
- Keep matplotlib for plotting (what it's good at)
- Add Tkinter for forms, dialogs, controls
- Lighter weight than Qt

**Migration Effort:** ~8-12 hours
- 3-5 hours: Create Tkinter control panel
- 2-4 hours: Coordinate matplotlib and Tkinter windows
- 3-3 hours: Implement forms and dialogs

**Benefits:**
- Smaller dependency (Tkinter included with Python)
- Leverage existing matplotlib code
- Moderate complexity increase

**Drawbacks:**
- Two separate window systems to coordinate
- Less polished than Qt
- More complex than pure Qt solution
- Tkinter has some UI limitations

### Option 3: Enhance Current System (Only if Phase 2 scope reduces)

**When to consider:**
- Phase 2 features are significantly reduced
- Only adding minor functionality
- Timeline or resources are very constrained

**Effort:** ~4-6 hours for incremental improvements
- Add event manager class
- Implement configuration file system
- Custom matplotlib dialogs (limited functionality)

**Benefits:**
- No framework migration
- Minimal code changes
- Fast implementation

**Drawbacks:**
- Still limited by matplotlib constraints
- Will need migration eventually for richer features
- Kicking the can down the road

---

## Specific Recommendations by Component

### 0. Primitive Metadata Module ✅ IMPLEMENTED (December 6, 2025)

**Status:** Complete - `tools/editor/primitives.py` created

**Implementation:** Single source of truth for primitive definitions

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class PrimitiveInfo:
    key: str           # Short key (v, r, f, a, S)
    name: str          # Full name (Visibility, Resonance, etc.)
    color: str         # Hex color code
    description: str   # Human-readable description

PRIMITIVES = {
    'v': PrimitiveInfo('v', 'Visibility', '#1f77b4', 'How visible/present...'),
    'r': PrimitiveInfo('r', 'Resonance', '#ff7f0e', 'Emotional alignment...'),
    # ...
}
```

**Benefits:**
- One place to update primitive names (no multi-file hunts)
- Includes descriptions ready for tooltips/help text
- Self-documenting with metadata
- Easy to extend (validation rules, ranges, etc.)

**Completed:** December 6, 2025 (~30 minutes)

### 1. Event Management System (Improve Now or Phase 2)

**Recommendation:** Implement `EventManager` class

```python
class EventManager:
    """Manages event lifecycle with undo/redo support."""
    
    def __init__(self):
        self.events = []
        self.undo_stack = []
        self.redo_stack = []
    
    def add_event(self, event):
        """Add event with undo support."""
        
    def delete_event(self, index):
        """Delete event with undo support."""
        
    def modify_event(self, index, changes):
        """Modify event with transaction support."""
        
    def undo(self):
        """Undo last change."""
        
    def redo(self):
        """Redo last undone change."""
```

**When:** 
- Phase 2 start if migrating to Qt (part of larger refactor)
- Could implement now (~4-6 hours) if useful for diagnostics

### 2. Configuration System ✅ IMPLEMENTED (December 6, 2025)

**Status:** Complete - `tools/editor/config.py` created

**Implementation:** User preferences file with JSON format

**File:** `~/.whenmathprays/editor_config.json`

```json
{
  "layout": {
    "margin_left": 0.14,
    "margin_right": 0.02,
    "panel_gap": 0.35,
    "primitive_gauge_x": -0.18
  },
  "weights": {
    "w_v": 1.0,
    "w_r": 1.0,
    "w_f": 1.0,
    "w_a": 1.0,
    "w_S_real": 0.5,
    "w_S_imag": 0.5
  },
  "appearance": {
    "marker_size": 8,
    "line_width": 1.5
  }
}
```

**Features:**
- Falls back to sensible defaults if file doesn't exist (zero breakage)
- Loads on editor startup, merges with defaults
- Example config file: `docs/editor_config_example.json`
- All LAYOUT values now user-customizable

**Completed:** December 6, 2025 (~2 hours)

### 3. GUI Framework (Decide at Phase 2 Start)

**Decision Point:** When starting Phase 2 development

**Recommendation:** Go with **Qt (PyQt5 or PySide6)**
- Most future-proof
- Best support for complex features
- Industry standard for scientific applications
- Worth the migration effort

**Migration Strategy:**
1. **Week 1:** Qt main window skeleton, embed matplotlib
2. **Week 2:** Port existing functionality
3. **Week 3:** Add Phase 2 features incrementally
4. **Week 4:** Testing and polish

---

## Migration Path to Qt (Detailed)

### Step 1: Setup (1 hour)
```bash
pip install PyQt5
# or
pip install PySide6
```

### Step 2: Create Qt Main Window (3-4 hours)

```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class InteractiveEditorQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Scenario Editor")
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout: horizontal split
        layout = QHBoxLayout(central)
        
        # Left: Primitive plots
        self.primitive_canvas = FigureCanvasQTAgg(Figure(figsize=(6, 8)))
        layout.addWidget(self.primitive_canvas, stretch=1)
        
        # Right: Trajectory plot
        self.trajectory_canvas = FigureCanvasQTAgg(Figure(figsize=(6, 8)))
        layout.addWidget(self.trajectory_canvas, stretch=1)
        
        # Create axes on figures
        self.setup_plots()
```

### Step 3: Port Existing Components (5-7 hours)

**Reuse:**
- ✅ `EditorModel` - No changes needed
- ✅ `EditorController` - Minor changes to interface with Qt
- ✅ `PrimitivePanel` / `TrajectoryPanel` - Adapt to Qt canvas

**Replace:**
- ❌ matplotlib Button widgets → QPushButton
- ❌ matplotlib text displays → QLabel
- ❌ LAYOUT dictionary → Qt layouts (QHBoxLayout, QVBoxLayout)

### Step 4: Add Phase 2 Features (varies by feature)

**Example: Perspective Toggle (2 hours)**
```python
# Add to main window
self.perspective_combo = QComboBox()
self.perspective_combo.addItems(["M1", "M2"])
self.perspective_combo.currentTextChanged.connect(self.on_perspective_changed)
```

**Example: Add Event Dialog (3 hours)**
```python
class AddEventDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Event")
        
        layout = QFormLayout(self)
        self.time_input = QDoubleSpinBox()
        self.v_input = QDoubleSpinBox()
        # ... other primitives
        
        layout.addRow("Time:", self.time_input)
        layout.addRow("Ego (v):", self.v_input)
        # ...
```

---

## Decision Matrix

| Feature | Matplotlib (Current) | Matplotlib + Tkinter | Qt Framework |
|---------|---------------------|----------------------|--------------|
| **Phase 1 Features** | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| **Dual Perspective** | ⚠️ Difficult | ✅ Moderate | ✅ Easy |
| **Add/Delete Events** | ❌ Very Difficult | ⚠️ Moderate | ✅ Easy |
| **Sensitivity Analysis** | ❌ Very Difficult | ⚠️ Difficult | ✅ Easy |
| **Professional Look** | ⚠️ Basic | ⚠️ Basic | ✅ Excellent |
| **Maintainability** | ✅ Good | ⚠️ Moderate | ✅ Excellent |
| **Learning Curve** | ✅ Low | ⚠️ Moderate | ⚠️ Moderate-High |
| **Dependencies** | ✅ Minimal | ✅ Minimal | ⚠️ PyQt5/PySide6 |
| **Migration Effort** | ✅ None | ~10 hours | ~15-20 hours |

**Legend:**
- ✅ Good/Easy
- ⚠️ Moderate/Some Issues
- ❌ Poor/Very Difficult

---

## Timeline Recommendations

### If Starting Phase 2 Within 1-2 Months:
**Recommended:** Migrate to Qt immediately at Phase 2 start
- **Week 1:** Qt migration
- **Week 2-4:** Phase 2 features with Qt
- **Total:** 4 weeks for Phase 2 complete

### If Phase 2 Timeline Uncertain (3+ months):
**Recommended:** Implement EventManager and Configuration now
- Keep current matplotlib implementation
- Add incremental improvements (~6-8 hours total)
- Defer Qt migration until Phase 2 commitment

### If Phase 2 Scope Reduces Significantly:
**Recommended:** Stay with current implementation
- Only add specific needed features
- Defer major refactoring

---

## Implementation Status (December 6, 2025)

### ✅ Completed Improvements
1. **Primitives Module** (`tools/editor/primitives.py`) - 30 minutes
   - Single source of truth for primitive metadata
   - Includes names, colors, descriptions
   - Updated across all files (primitive_panel.py, documentation)

2. **Configuration System** (`tools/editor/config.py`) - 2 hours
   - User preferences from `~/.whenmathprays/editor_config.json`
   - Fallback to sensible defaults (zero breakage)
   - All LAYOUT values now customizable
   - Example config in `docs/editor_config_example.json`

**Total Time:** ~2.5 hours  
**Risk:** Very low (backward compatible)  
**Benefits:** Immediate maintainability improvements, Phase 2 ready

### 🔜 Recommended Next (When Phase 2 Starts)
3. **Event Manager with Undo/Redo** - 6-8 hours
4. **GUI Framework Decision** - Qt for rich features vs. stay with matplotlib

---

## Action Items

### Immediate (Optional, ~6-8 hours total):
1. ✅ ~~Implement primitives module~~ (DONE December 6)
2. ✅ ~~Implement configuration system~~ (DONE December 6)
3. ☐ Implement `EventManager` class with undo/redo (~6-8 hours)
2. ☐ Add configuration file system (~2-3 hours)
3. ☐ Document both in code and user guide

### Phase 2 Start (Required, ~15-20 hours):
1. ☐ Decision: Commit to Qt migration (recommended)
2. ☐ Setup PyQt5/PySide6 environment
3. ☐ Port existing functionality to Qt
4. ☐ Implement Phase 2 features using Qt widgets

### Future Considerations:
- Database backend for large-scale scenario management
- Web interface (Flask + JavaScript) for remote access
- Export to video/animation for presentations

---

## Conclusion

**For Phase 1:** Current architecture is **adequate and maintainable** ✅

**For Phase 2:** Migration to **Qt framework is strongly recommended** 🎯
- Enables all planned features
- More maintainable long-term
- Better user experience
- Worth the migration investment (~15-20 hours)

**Alternative:** Hybrid matplotlib + Tkinter is acceptable if Qt is not feasible, but still requires ~10 hours of work with more limitations.

**Not Recommended:** Staying with pure matplotlib for Phase 2 unless scope significantly reduces.

---

**Related Documents:**
- [future_interactive_edit_requirements.md](future_interactive_edit_requirements.md) - Phase 2 feature requirements
- [ARCHITECTURE.md](../ARCHITECTURE.md) - Current system architecture
- [interactive_editor_user_guide.md](interactive_editor_user_guide.md) - Phase 1 user guide

**Questions?** Contact the development team or see issue tracker for Qt migration planning.
