# Interactive Scenario Editor - Complete Roadmap

**Purpose:** Master timeline showing past, present, and future development  
**Current Phase:** Phase 2 COMPLETE → Phase 3 Planning  
**Phase 2 Progress:** 9 hours completed (READY FOR RELEASE)  
**Total Vision:** ~30-40 hours across 4 phases  
**Last Updated:** December 10, 2025

---

## Quick Navigation

- **Phase 1 (✅ Complete):** Single-perspective editing, drag-and-drop, lock/unlock, real-time trajectory
- **Phase 2.0 (✅ Complete):** PySide6 migration, undo/redo system
- **Phase 2.1 (✅ Complete):** Diagnostic "what-if" markers, gamma_self0 editor, event insertion
- **Phase 2.2 (✅ Complete):** Delete events functionality
- **Phase 2.3 (⏸️ Deferred):** Inverse editing - deferred to Phase 4
- **Phase 3 (→ Next):** M2 integration with QDockWidget flexible workspace - [See architecture doc](architecture_recommendations.md)
- **Phase 4 (Future):** Advanced features - inverse editing, sensitivity analysis, analysis window

---

## Phase Timeline

### Phase 1: Foundation ✅ COMPLETE (December 5, 2025)
**Duration:** 4-6 hours  
**Status:** Released as v1.0-phase1

**What Was Built:**
- ✅ Single-perspective (M1) primitive editing with drag-and-drop
- ✅ Real-time gamma_self trajectory preview with debounced computation
- ✅ Lock/unlock event functionality (right-click toggle)
- ✅ Auto-marking of modified points (hollow vs filled visual system)
- ✅ Primitive readout gauge (marker ID + Y-value display)
- ✅ Gamma_self position readout (X,Y coordinates on click)
- ✅ Dual save functionality (Click=CSV, Shift=PNG, Ctrl=Both)
- ✅ CSV format with marker/locked columns for persistence
- ✅ Centralized LAYOUT system for maintainable UI
- ✅ Keyboard shortcuts (0=reset, +/-=zoom, F=fixed view, G=edit gamma_self_0)
- ✅ Primitives module (single source of truth for primitive metadata)
- ✅ Configuration system (user-customizable via JSON)

**Key Achievements:**
- Created diagnostic tool for event-level analysis
- Enabled real data anchoring (lock therapy sessions, perturb unknowns)
- Visual feedback loop for sensitivity exploration
- Foundation for all future phases

**Architecture Notes:**
- Matplotlib-based (sufficient for Phase 1, may migrate to Qt later)
- MVC pattern: EditorModel, EditorController, PrimitivePanel, TrajectoryPanel
- Backward-compatible CSV format (old format loads, always saves with full metadata)

### Phase 2.0: PySide6 Migration & Undo/Redo ✅ COMPLETE (December 6, 2025)
**Duration:** ~4 hours  
**Status:** Released as v2.0-undo-redo

**What Was Built:**
- ✅ Complete PySide6 migration (replaced Matplotlib/Tkinter with PyQtGraph)
- ✅ Full undo/redo system using QUndoStack
- ✅ Discrete undo steps (each marker edit is separate, undoable action)
- ✅ Keyboard shortcuts (Ctrl+Z undo, Ctrl+Y/Ctrl+Shift+Z redo)
- ✅ Command pattern for delegation (prevents recursive undo creation)
- ✅ Marker position synchronization on gamma_self graph
- ✅ Label management (appear when modified, disappear when back to baseline)
- ✅ Thread-safe incremental updates
- ✅ Significantly improved rendering performance

**Key Achievements:**
- Modern Qt-based architecture ready for advanced features
- Professional undo/redo workflow
- Much faster rendering and interaction

### Phase 2.1: Diagnostic "What-If" Markers ✅ COMPLETE (December 7, 2025)
**Duration:** ~3 hours  
**Status:** Released as v2.1-diagnostic-markers

**What Was Built:**
- ✅ **Shift+Click diagnostic marker placement** - Test hypothetical primitive values
- ✅ **Black X markers** - Visual distinction from actual data (primitive + trajectory)
- ✅ **Draggable hypothetical markers** - Real-time exploration of different values
- ✅ **Final outcome display** - Shows where trajectory ends with hypothetical change
- ✅ **Dual gauge updates** - Both primitive and gamma_self readouts show hypothetical values
- ✅ **Auto-clear previous** - New diagnostic marker clears old ones automatically
- ✅ **Non-destructive testing** - Explore scenarios without modifying actual data
- ✅ **gamma_self0 editor widget** - Edit initial state (real/imaginary spinboxes)
- ✅ **Apply/Reset buttons** - Apply new gamma_self0 or reset to CSV default
- ✅ **Orange start marker** - Visual indication when gamma_self0 is modified
- ✅ **Event insertion via time entry list** - Add events at any time (including fractional)
- ✅ **Fractional time support** - Full support for non-integer times (e.g., 2.5 days)
- ✅ **Vertical dashed lines** - Mark inserted events on primitive plots
- ✅ **Black diamond markers** - Show inserted events on gamma_self trajectory

**Technical Achievement:**
- Fixed PyQtGraph coordinate system using `QGraphicsScene.sigMouseClicked`
- Proper `event.scenePos()` + `mapSceneToView()` for accurate click positioning
- Computes full hypothetical trajectory showing final gamma_self position
- GammaSelf0Editor widget with real/imag QDoubleSpinBox controls
- InsertionOptionsWidget with dynamic time entry fields
- Automatic detection of inserted events (all primitives = 0)

**Key Value:**
- Quick "what-if" exploration before committing to edits
- Answers questions like: "What if resonance had been +7 at day 14?"
- Non-destructive sensitivity analysis
- Edit starting position to explore different initial conditions
- Add new time points for more detailed scenarios
- Full support for fractional timescales

### Phase 2.2: Delete Events ✅ COMPLETE (December 8, 2025)
**Duration:** ~2 hours  
**Status:** Released as v2.2-delete-events

**What Was Built:**
- ✅ **Ctrl+Click deletion** - Click any marker while holding Ctrl to delete that event
- ✅ **Full validation** - Prevents deleting first/last events, locked events, or when only 2 remain
- ✅ **DeleteEventCommand** - Proper QUndoCommand implementation for undo/redo
- ✅ **Ctrl+Z undo** - Restores deleted events with all primitives, notes, and lock status
- ✅ **Ctrl+Y redo** - Re-deletes events after undo
- ✅ **User-friendly dialogs** - Clear error messages for invalid deletion attempts
- ✅ **Baseline array management** - Properly updates internal arrays on delete/insert

**Technical Achievement:**
- Integrated with existing QUndoStack system
- Proper Event object reconstruction on undo
- View refresh after deletion/insertion
- Works seamlessly with other undo actions (edits, resets)

**Key Value:**
- Clean up scenarios by removing unwanted events
- Maintain data integrity (can't delete critical boundary events)
- Full undo/redo support for safe experimentation

### Phase 2.3: Inverse Editing ⏸️ DEFERRED (To Phase 4)
**Duration:** 15-20 hours (much more complex than initially estimated)  
**Status:** Deferred to Phase 4 - requires research and sophisticated algorithms

**Reason for Deferral:**
- Much more complex than originally anticipated
- Non-unique solutions (many primitive combinations can produce same gamma_self)
- Requires constraint satisfaction solver and heuristic optimization
- Better suited after M2 integration (Phase 3) when dual-perspective complexity is understood
- Would significantly delay Phase 2 release for marginal benefit

**Planned Features (Phase 4):**
- Inverse editing (drag gamma_self to suggest primitives)
- Constraint solver with multiple solution candidates
- Accept/reject dialog with preview of suggested primitive changes
- Heuristic scoring to rank solutions by "naturalness"

**Key Value:**
- Bidirectional editing workflow
- Goal-oriented scenario construction
- "Work backwards" from desired outcome

---

## Phase 2 Summary Status

**Completed Sub-Phases:**
- ✅ Phase 2.0: PySide6 Migration & Undo/Redo (~4 hours)
- ✅ Phase 2.1: Diagnostic Markers + gamma_self0 Editor + Event Insertion (~3 hours)
- ✅ Phase 2.2: Delete Events (~2 hours)

**Deferred Sub-Phases:**
- ⏸️ Phase 2.3: Inverse Editing → Moved to Phase 4 (complexity + M2 interactions)

**Overall Phase 2 Status:** ✅ **COMPLETE and READY FOR RELEASE** (9 hours total)

---

### Phase 3: M2 Integration & Flexible Workspace → NEXT
**Duration:** 10-12 hours  
**Status:** Planning - [See architecture doc](architecture_recommendations.md)

**Core Concept:**
- M1 and M2 (partner perspectives) share same graphs with overlay visualization
- QDockWidget architecture for flexible, resizable, movable panels
- Perspective switcher (radio buttons) to toggle between M1/M2 editing
- Active/inactive visual states (bold vs. faded)

**Phase 3.1: QDockWidget Foundation** (3-4 hours)
- Wrap panels in QDockWidget for resize/rearrange/hide/undock
- View menu for panel visibility controls
- Layout persistence (QSettings automatic save/restore)
- Multi-monitor support

**Phase 3.2: Perspective Switcher** (2 hours)
- Radio button widget (red glow = active, grey = inactive)
- Toolbar placement for visibility
- Keyboard shortcut (Tab or Space) to toggle M1/M2
- Connected to controller.switch_perspective()

**Phase 3.3: M2 Overlay Rendering** (3-4 hours)
- Both M1 and M2 datasets render on same graphs
- Active perspective: bold lines, solid markers, draggable (opacity=1.0)
- Inactive perspective: thin/dashed lines, hollow markers, read-only (opacity=0.4)
- Z-order management (active renders on top)
- Interaction filtering (drag/click only affects active perspective)

**Phase 3.4: M2 Data Model** (2 hours)
- EditorModel tracks both M1 and M2 events
- CSV format extension (M2 columns or separate files)
- Backward compatible (old M1-only CSVs load fine)
- Observer pattern handles dual-perspective updates

**Key Benefits:**
- Space-efficient overlay design (no duplicate panels needed)
- Flexible workspace adapts to laptop/wide monitor/dual monitor
- Clear visual feedback on which perspective is being edited
- Future-proof for statistics panels, help, debug instrumentation

**Key Value:**
- Edit both partner perspectives (M1 and M2) in single session
- Compare perspectives side-by-side with overlay visualization
- Professional, flexible workspace for serious research use
- Foundation for Phase 4 advanced features
  - PNG name indicates combined view (e.g., `scenario1_scenario2_combined.png`)
- `Close Second File`: Return to single-file mode

**State Management:**
- Separate undo stacks per file (preserved when switching)
- Separate modified_primitives tracking per file
- Separate marker_positions per file
- Active file state maintained during session

**Future Enhancements (Phase 4+):**
- Editable filename display in UI
- Editable gamma_self_0 (with constraint both must match)
- Load order doesn't matter (any file can be primary/secondary)

**Key Value:**
- Compare different scenarios side-by-side
- M1 vs M2 relationship dynamics visualization
- Before/after scenario comparison
- Sensitivity analysis: compare baseline vs modified scenarios
- Validate symmetry assumptions across perspectives

### Phase 4: Advanced Features (Future)
**Duration:** 3-4 hours  
**Status:** Future

**Planned Features:**
- Fill gaps: Linear/cubic/hold interpolation for unlocked points
- Automated sensitivity analysis: Rank events by trajectory impact
- Time unit conversion: Days ↔ Weeks ↔ Months ↔ Years
- Zoom/pan on plots, animation/playback mode
- Batch export (PNG plots)

**Key Value:**
- Production-ready polish
- Automated diagnostics
- Professional presentation

---

## Executive Summary

The interactive scenario editor provides a graphical diagnostic tool for event-level analysis of relationship dynamics. Users can load scenarios generated by `run_scenarios`, lock key events (real data anchor points), perturb specific primitives, and observe real-time gamma_self trajectory changes. This complements the scenario script workflow by enabling fine-grained sensitivity analysis and constraint validation.

**Key Decision (Updated):** Building progressive phases. Phase 1 ✅ COMPLETE - focuses on single-perspective (M1) editing with drag-and-drop primitives, lock/unlock functionality, real-time trajectory visualization, and diagnostic gauges. Future phases will add dual-perspective editing, add/delete points, inverse editing, and automated sensitivity analysis.

**Primary Use Case:** Diagnostic tool for understanding which events dominate outcomes, validating GRP fidelity with real data, and exploring "what-if" perturbations at specific time points.

---

## Core Concept

### The Problem
- **Arc-level design is solved** (scenario scripts work well)
- **Event-level analysis is needed** - Which specific events dominate outcomes?
- **Real data anchoring** - Need to lock known events and perturb others
- **Sensitivity exploration** - What happens if day 23 altruism changes from 3→5?
- **Constraint validation** - Can GRP reach this trajectory given realistic primitive bounds?

### The Solution - Diagnostic Workflow
A graphical editor integrated with scenario scripts:

```
Step 1: SCENARIO SCRIPT generates baseline CSV
        ↓
Step 2: INTERACTIVE EDITOR loads CSV for diagnostic analysis
        • Lock key events (real data anchor points)
        • Perturb unlocked events (drag primitives)
        • Observe real-time gamma_self trajectory changes
        • Auto-mark modified points
        ↓
Step 3: Save modified CSV → Re-run scenario script
```

**Key Features:**
1. **Visual primitive editing** - Drag control points for v, r, f, a, S
2. **Real-time trajectory preview** - See gamma_self update as you edit
3. **Lock/unlock events** - Anchor known data, vary unknowns
4. **Auto-marking** - Customized points automatically get markers
5. **Future: Bidirectional editing** - Drag gamma_self to suggest primitives
6. **Future: Dual perspective** - Edit M1 and M2 with comparison view

---

## Architecture Design

### Phase 1: Two-Panel Layout (Single Perspective)

```
┌────────────────────────────────────────────────────────────┐
│  Interactive Scenario Editor - M1: single_dating_M1.csv    │
├───────────────────────────────┬────────────────────────────┤
│                               │                            │
│   PRIMITIVES (M1)             │   GAMMA_SELF TRAJECTORY    │
│                               │                            │
│   v ─────────── (visibility)  │      ^  Love              │
│   r ─────────── (resonance)   │      │                    │
│   f ─────────── (freedom)     │      │    Q2    Q1       │
│   a ─────────── (altruism)    │   ───┼───                │
│   S ─────────── (soul)        │   Ego│We                 │
│                               │      │    Q3    Q4       │
│   [Time axis: 0 to 60 days]   │      v  Hate             │
│                               │                            │
│   • Drag control points       │   • M1 trajectory (blue)  │
│   • Right-click to lock       │   • Real-time update      │
│   • Locked = gray + hatching  │   • Start/end markers     │
│   • Modified = auto-marked    │   • Hover for values      │
│                               │                            │
└───────────────────────────────┴────────────────────────────┘
```

### Phase 3: Dual-File Comparison Layout (Future)

```
┌────────────────────────────────────────────────────────────┐
│  Interactive Editor - [Active: scenario1.csv] [Ref: scenario2.csv] │
│  [Toggle: ● File 1  ○ File 2]  [File] [Save] [Save All]   │
├───────────────────────────────┬────────────────────────────┤
│   PRIMITIVES (Overlay)        │   GAMMA_SELF (Dual)        │
│                               │                            │
│   File 1 (solid bold):        │   • File 1 (blue solid)    │
│   v ━━━━━━━ (active/editable) │   • File 2 (green dotted)  │
│   r ━━━━━━━                   │                            │
│   f ━━━━━━━                   │   Legend:                  │
│   a ━━━━━━━                   │   ━ scenario1.csv (active) │
│   S ━━━━━━━                   │   ┄ scenario2.csv (ref)    │
│                               │                            │
│   File 2 (dotted faded):      │   • Both visible           │
│   v ┄┄┄┄┄┄┄ (ref/view-only)   │   • Same timeline          │
│   r ┄┄┄┄┄┄┄  30% opacity      │   • Compare dynamics       │
│   f ┄┄┄┄┄┄┄                   │   • Modification markers   │
│   a ┄┄┄┄┄┄┄                   │     on active only         │
│   S ┄┄┄┄┄┄┄                   │                            │
│                               │                            │
│   [Shared time axis]          │   Click toggle to swap     │
│   • Click toggle to switch    │   active/reference         │
│   • Markers = union of both   │                            │
└───────────────────────────────┴────────────────────────────┘
```

### Technology Stack

**Chosen: Matplotlib with `matplotlib.widgets`**
- ✅ Already a dependency (no new installs)
- ✅ Good event handling for drag-and-drop
- ✅ Sufficient for scientific visualization
- ✅ Python-native (no web server complexity)
- ✅ Fast prototyping for Phase 1 validation
- ⚠️ Can migrate to PyQt5 later if performance/polish needed

**Implementation:**
- `matplotlib.widgets.RectangleSelector` for region selection
- Custom event handlers for drag-and-drop (`button_press_event`, `motion_notify_event`, `button_release_event`)
- Debounced trajectory computation (threading.Timer)
- Figure with GridSpec layout for multi-panel arrangement

---

## Feature Specifications

### Phase 1 Features (In Development)

### 1. Primitive Curve Editing

**Visual Representation:**
- Each primitive (v, r, f, a, S) as a line plot over time
- Control points at each event time (draggable circles)
- Lines connecting points for visual continuity
- Color coding:
  - M1 primitives: Distinct colors per primitive (blue tones)
  - Locked points: Gray with diagonal hatching
  - Modified points: Automatically marked (visible indicator)

**Phase 1 Interactions:**
- ✅ **Click-and-drag** control points vertically (change primitive value)
- ✅ **Right-click** to lock/unlock point
- ✅ **Hover** shows tooltip with exact values (time, primitive value)
- ❌ **Add/delete points** (deferred to Phase 2)

**Constraints:**
- Vertical drag clamped to [-10, +10] range
- Locked points non-draggable (grayed out with hatching)
- Horizontal dragging disabled (time stays fixed)
- Auto-marking: Any dragged point automatically gets a marker

### 2. Gamma_Self Trajectory Visualization

**Phase 1 Display:**
- Real-time trajectory computed from current primitives (uses `core/love.py`)
- M1 trajectory: Solid blue line with markers at events
- Quadrant lines and labels (Q1-Q4)
- Start/end markers clearly visible
- Axes: Ego↔We (horizontal), Hate↔Love (vertical)

**Phase 1 Updates:**
- ✅ Recompute trajectory on mouse release (debounced 300ms)
- ✅ Show "Computing..." overlay during calculation
- ✅ Auto-scale to fit trajectory range
- ❌ Interactive zoom/pan (deferred to Phase 4)

**Phase 1 Interactions:**
- ✅ **Hover** shows details (time, gamma_x, gamma_y, magnitude)
- ❌ **Drag trajectory points** for inverse editing (deferred to Phase 2)
- ❌ **Click to sync** time indicator across panels (deferred to Phase 3)

### 3. Bidirectional Editing (Phase 2+)

**Phase 1: Forward Mode Only (Primitives → Gamma_Self)**
- ✅ Standard mode: Drag primitives, see trajectory update
- ✅ Direct computation using `update_gamma_self()` from `core/love.py`
- ✅ Fast and deterministic

**Phase 2: Inverse Mode (Gamma_Self → Primitives)**
- ❌ Experimental: Drag gamma_self point, primitives adjust (deferred)
- ❌ **Challenge:** One trajectory point ≠ unique primitive values
- ❌ **Solution:** Heuristic inverse estimation (see below)

**Inverse Estimation Heuristic:**
```python
def suggest_primitives_for_target(current_gamma, target_gamma, time_step):
    """
    Suggest primitive changes to move from current_gamma to target_gamma.
    
    Strategy: Even distribution across primitives
    - Calculate required delta: Δγ = target - current
    - Distribute Δγ.real across v and S_R
    - Distribute Δγ.imag across r, f, a, and S_I
    - Apply weights and normalize to [-10, +10] range
    """
    delta = target_gamma - current_gamma
    
    # Real axis (Ego ↔ We)
    # v and S contribute: Δ_real = w_v*v + w_S_R*S
    v_suggestion = delta.real / (w_v + w_S_R/2)
    S_real = delta.real / (w_S_R + w_v/2)
    
    # Imaginary axis (Hate ↔ Love)
    # r, f, a, S contribute: Δ_imag = w_r*r + w_f*f + w_a*a + w_S_I*S
    total_weight = w_r + w_f + w_a + w_S_I
    r_suggestion = delta.imag * (w_r / total_weight)
    f_suggestion = delta.imag * (w_f / total_weight)
    a_suggestion = delta.imag * (w_a / total_weight)
    S_imag = delta.imag * (w_S_I / total_weight)
    
    # Combine S contributions
    S_suggestion = (S_real + S_imag) / 2
    
    # Clamp to [-10, +10]
    return {
        'v': clamp(v_suggestion, -10, 10),
        'r': clamp(r_suggestion, -10, 10),
        'f': clamp(f_suggestion, -10, 10),
        'a': clamp(a_suggestion, -10, 10),
        'S': clamp(S_suggestion, -10, 10)
    }
```

**User Experience:**
- Inverse mode toggle: "Drag primitives" ⇄ "Drag trajectory"
- Visual feedback: Dashed lines show suggested primitive changes
- "Accept suggestions" button to apply changes
- "Undo" always available

### 4. Radio Button Selection (M1/M2) - Phase 3+

**Phase 1:** Single perspective only (M1)
- ✅ Load one CSV file
- ✅ Edit M1 primitives
- ✅ Display M1 gamma_self trajectory

**Phase 3:** Dual perspective editing (deferred)
- ❌ Radio button toggle: ○ M1  ○ M2
- ❌ Selected perspective: Full opacity, active drag handlers
- ❌ Unselected perspective: 30% opacity, view-only
- ❌ Gamma_self panel shows both trajectories (M1 blue, M2 red)
- ❌ Keyboard shortcut: Tab to toggle between M1/M2

### 5. Timeline Management

**Phase 1 Time Axis Features:**
- ✅ Display time range from CSV (e.g., 0 to 60 days)
- ✅ Time unit from CSV metadata (default: days)
- ✅ Fixed time points (no add/delete in Phase 1)
- ❌ Zoom/pan (deferred to Phase 4)
- ❌ Add/delete time points (deferred to Phase 2)

**Phase 2 Features:**
- ❌ **Add time point:** Shift+Click on axis → Insert event
- ❌ **Delete time point:** Select point → Delete key (if unlocked)

**Phase 4 Features:**
- ❌ **Non-contiguous support:** Visual gap indicators, "Fill gaps" with interpolation
- ❌ **Time unit conversion:** Dropdown to switch days/weeks/months/years

### 6. Marker and Lock Management

**Phase 1 Implementation:**

**Auto-Marker Assignment:**
- ✅ Any point dragged by user automatically gets a marker
- ✅ Marker symbol: Small circle or dot indicator
- ✅ Purpose: Track which events were customized
- ✅ User can manually remove marker if desired (Phase 2)

**Lock Toggle:**
- ✅ Right-click point → "Lock" / "Unlock" (context menu)
- ✅ Visual: Locked points have gray fill + diagonal hatching
- ✅ Locked points cannot be dragged
- ✅ Lock status saved to CSV (`locked` column: `*` or empty)
- ❌ "Lock all" / "Unlock all" batch buttons (deferred to Phase 3)

### 7. File Operations

**Phase 1 Implementation:**

**Load:**
- ✅ Command-line argument: `python tools/interactive_editor.py <csv_file>`
- ✅ Reads CSV with or without `marker` and `locked` columns (backward compatible)
- ✅ Auto-detects time unit from CSV metadata (if present)
- ✅ Validates CSV format (checks for required columns: step,v,r,f,a,S)

**Save:**
- ✅ File → Save As (requires new filename, never overwrites input)
- ✅ Auto-suggests filename: `<original>_modified.csv`
- ✅ Always exports with full format: `step,v,r,f,a,S,notes,marker,locked`
- ✅ Preserves metadata (name, time_unit) in CSV header
- ❌ File → Save (overwrite current) - blocked to prevent data loss
- ❌ Dual export (M1+M2) (deferred to Phase 3)

### 8. Real-Time Computation

**Phase 1 Performance Strategy:**

**Debounced Computation:**
- ✅ Trajectory computation triggered on mouse release (not during drag)
- ✅ 300ms debounce timer (if user drags multiple points rapidly)
- ✅ "Computing..." status indicator during calculation
- ✅ Uses `core/love.py` `update_gamma_self()` directly

**Implementation:**
```python
class TrajectoryComputer:
    def __init__(self, debounce_ms=300):
        self.debounce_timer = None
        self.dirty = False
    
    def on_primitive_changed(self):
        """Called when user drags a primitive control point."""
        self.dirty = True
        
        # Cancel pending computation
        if self.debounce_timer:
            self.debounce_timer.cancel()
        
        # Schedule new computation after 300ms of inactivity
        self.debounce_timer = threading.Timer(
            self.debounce_ms / 1000,
            self.recompute_trajectory
        )
        self.debounce_timer.start()
    
    def on_mouse_release(self):
        """Immediate computation when user releases mouse."""
        if self.dirty:
            self.recompute_trajectory(immediate=True)
```

**Phase 1 Scope:**
- ✅ Adequate performance for typical scenarios (10-50 events)
- ❌ Progressive rendering (deferred if needed based on testing)

### 9. Keyboard Shortcuts

**Phase 1 Implementation:**
| Shortcut | Action | Status |
|----------|--------|--------|
| Ctrl+S | Save file (Save As dialog) | ✅ Phase 1 |
| Esc | Cancel current drag operation | ✅ Phase 1 |
| Right-click | Context menu (Lock/Unlock) | ✅ Phase 1 |

**Phase 2+ Shortcuts:**
| Shortcut | Action | Status |
|----------|--------|--------|
| Shift+Click | Add new control point | Phase 2 |
| Delete | Delete selected point (if unlocked) | Phase 2 |
| Ctrl+Z | Undo last change | Phase 2 |
| Ctrl+Y | Redo | Phase 2 |
| Tab | Toggle M1 ⇄ M2 selection | Phase 3 |
| Ctrl+L | Toggle lock on selected point | Phase 3 |
| Space | Play animation (time sweep) | Phase 4 |

### 10. Undo/Redo System (Phase 2+)

**Implementation (Deferred):**
- ❌ Command pattern for all edits
- ❌ Stack limit: 50 operations
- ❌ Memory efficient (store deltas, not full copies)

**Undoable Operations:**
- Primitive value changes
- Point additions/deletions
- Lock status changes

---

## Technical Implementation Details

### Data Model

```python
class ScenarioEditorModel:
    """Model for interactive scenario editing."""
    
    def __init__(self):
        self.name = ""
        self.time_unit = "days"
        self.events_m1 = []  # List of EventPoint objects
        self.events_m2 = []  # For dual scenarios
        self.selected_perspective = "M1"
        self.undo_stack = []
        self.redo_stack = []
        self.dirty = False  # Unsaved changes?
    
    def add_event(self, time, primitives, locked=False, marker=""):
        """Add new event at specified time."""
        # Implementation
    
    def update_primitive(self, time, primitive_name, value):
        """Update single primitive value at time point."""
        # Push to undo stack
        # Mark dirty
        # Notify observers
    
    def compute_trajectory(self, perspective="M1"):
        """Compute gamma_self trajectory from primitives."""
        # Uses ScenarioRunner internally
        return trajectory_dataframe
```

```python
class EventPoint:
    """Single event in scenario timeline."""
    
    def __init__(self, time, v, r, f, a, S, notes="", marker="", locked=False):
        self.time = time
        self.v = v
        self.r = r
        self.f = f
        self.a = a
        self.S = S
        self.notes = notes
        self.marker = marker
        self.locked = locked
    
    def to_dict(self):
        """Export to CSV row format."""
        return {
            'day': self.time,
            'v': self.v, 'r': self.r, 'f': self.f, 'a': self.a, 'S': self.S,
            'notes': self.notes,
            'marker': self.marker,
            'locked': '*' if self.locked else ''
        }
```

### View Components (Matplotlib)

```python
class PrimitivePanel:
    """Panel showing 5 primitive curves for one perspective."""
    
    def __init__(self, ax, perspective="M1"):
        self.ax = ax
        self.perspective = perspective
        self.control_points = {}  # {(time, primitive): DraggablePoint}
        self.lines = {}  # {primitive: Line2D}
    
    def update_from_model(self, events):
        """Refresh display from event data."""
        for prim in ['v', 'r', 'f', 'a', 'S']:
            times = [e.time for e in events]
            values = [getattr(e, prim) for e in events]
            self.lines[prim].set_data(times, values)
        self.ax.draw()
    
    def on_point_dragged(self, event, point):
        """Handle drag event for control point."""
        # Update model
        # Trigger trajectory recomputation


class TrajectoryPanel:
    """Panel showing gamma_self complex plane."""
    
    def __init__(self, ax):
        self.ax = ax
        self.trajectory_m1 = None
        self.trajectory_m2 = None
        self.draggable_points = []
    
    def update_trajectory(self, trajectory_data, perspective="M1"):
        """Update trajectory plot from computed data."""
        x = trajectory_data['gamma_x']
        y = trajectory_data['gamma_y']
        
        if perspective == "M1":
            self.trajectory_m1.set_data(x, y)
        else:
            self.trajectory_m2.set_data(x, y)
        
        self.ax.draw()


class DraggablePoint:
    """Draggable control point for interactive editing."""
    
    def __init__(self, ax, x, y, callback, locked=False):
        self.point, = ax.plot([x], [y], 'o', picker=5)
        self.ax = ax
        self.x = x
        self.y = y
        self.callback = callback
        self.locked = locked
        self.dragging = False
        
        # Event connections
        self.cidpress = ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
    
    def on_press(self, event):
        if self.locked or event.inaxes != self.ax:
            return
        contains, attrd = self.point.contains(event)
        if contains:
            self.dragging = True
    
    def on_motion(self, event):
        if not self.dragging or event.inaxes != self.ax:
            return
        
        # Update position (clamp to valid range)
        self.y = np.clip(event.ydata, -10, 10)
        self.point.set_ydata([self.y])
        self.ax.figure.canvas.draw_idle()
    
    def on_release(self, event):
        if self.dragging:
            self.dragging = False
            self.callback(self.x, self.y)  # Notify model of change
```

### Controller

```python
class ScenarioEditorController:
    """Main controller coordinating model and views."""
    
    def __init__(self):
        self.model = ScenarioEditorModel()
        self.views = {
            'primitives_m1': None,
            'primitives_m2': None,
            'trajectory': None
        }
        self.computation_thread = None
    
    def on_primitive_changed(self, time, primitive, value, perspective):
        """Handle primitive value change from UI."""
        # Update model
        self.model.update_primitive(time, primitive, value, perspective)
        
        # Schedule trajectory recomputation
        self.schedule_recomputation(perspective)
    
    def schedule_recomputation(self, perspective):
        """Debounced trajectory recomputation."""
        # Cancel existing computation if any
        if self.computation_thread and self.computation_thread.is_alive():
            self.computation_thread.cancel()
        
        # Start new computation thread
        self.computation_thread = threading.Timer(0.3, self.recompute_trajectory, [perspective])
        self.computation_thread.start()
    
    def recompute_trajectory(self, perspective):
        """Compute trajectory in background thread."""
        traj = self.model.compute_trajectory(perspective)
        
        # Update view on main thread
        wx.CallAfter(self.views['trajectory'].update_trajectory, traj, perspective)
```

---

## User Workflows

### Phase 1 Workflow: Diagnostic Analysis of Existing Scenario

**Use Case:** Anchor real therapy session data, perturb specific events, validate GRP fidelity

1. **Generate baseline scenario:**
   ```bash
   python scenarios/singles_dating_Fred.py
   # Outputs: data/single_dating_to_love_M1.csv
   ```

2. **Launch interactive editor:**
   ```bash
   python tools/interactive_editor.py data/single_dating_to_love_M1.csv
   ```

3. **Lock known events (real data):**
   - Right-click day 0 (initial condition) → Lock
   - Right-click day 30 (therapy breakthrough) → Lock
   - Right-click day 60 (outcome) → Lock

4. **Perturb unlocked events:**
   - Drag day 15 `altruism` from 3 → 5
   - Watch gamma_self trajectory shift in real-time
   - Auto-marked as customized event

5. **Sensitivity exploration:**
   - Vary day 7 `resonance` -2 → +2
   - Observe: Does outcome stay in Q1? Or flip to Q4?

6. **Save modified scenario:**
   - File → Save As
   - Suggested name: `single_dating_to_love_M1_modified.csv`
   - Includes locked points and markers

7. **Re-run with modified CSV:**
   - Update scenario script: `csv_file = 'data/single_dating_to_love_M1_modified.csv'`
   - Re-run to generate full simulation report

### Phase 2+ Workflow: Inverse Editing (Future)

**Use Case:** "I need Q1 by day 60, what primitives should days 31-60 look like?"

1. Load scenario, lock days 1-30 (historical data)
2. Click "Inverse mode" button
3. Drag gamma_self endpoint from Q2 to Q1
4. Editor suggests primitive changes (dashed preview)
5. Review suggestions, accept or manually adjust
6. Save and re-run

### Phase 3+ Workflow: Dual Asymmetric Analysis (Future)

**Use Case:** "Which person's actions dominated the breakup outcome?"

1. Load M1 + M2 CSV pair
2. Toggle between M1 and M2 (radio button)
3. Perturb M1 day 23 `altruism` -5 → -3
4. Observe both trajectories on gamma_self panel
5. Identify: Did M1's change rescue the relationship, or was M2's day 30 action more influential?

---

## Development Roadmap (Updated December 4, 2025)

### Phase 1: Core Diagnostic Tool (IN PROGRESS - 4-6 hours)
**Status:** Building now  
**Scope:** Single perspective (M1 only), forward editing, lock/unlock

**Deliverables:**
- ✅ Two-panel matplotlib layout (Primitives | Gamma_self)
- ✅ Load single CSV (backward compatible: with/without marker/locked columns)
- ✅ Drag primitive control points (vertical, clamped [-10, 10])
- ✅ Lock/unlock points (right-click context menu)
- ✅ Real-time gamma_self trajectory update (debounced 300ms)
- ✅ Auto-mark customized points
- ✅ Save As with new filename (always include marker/locked columns)
- ✅ Locked points: Gray with diagonal hatching, non-draggable
- ❌ No add/delete points (Phase 2)
- ❌ No undo/redo (Phase 2)

**Success Criteria:**
- Load `single_dating_to_love_M1.csv`
- Lock days 0 and 60
- Drag day 30 `altruism` from 3 → 5
- See gamma_self trajectory shift in real-time
- Save as `single_dating_to_love_M1_modified.csv` with locks preserved

---

### Phase 2: Add/Delete Points + Inverse Editing (3-4 hours)
**Scope:** Expand event manipulation, bidirectional editing

**Features:**
- Add points: Shift+Click on time axis → Insert new event
- Delete points: Select + Delete key (if unlocked)
- Undo/redo system (Command pattern, 50-item stack)
- Inverse mode: Drag gamma_self → Suggest primitive changes
- Keyboard shortcuts (Ctrl+Z, Ctrl+Y, Shift+Click)

---

### Phase 3: Dual Perspective (2-3 hours)
**Scope:** M1 + M2 simultaneous editing and comparison

**Features:**
- Load M1 + M2 CSV pair
- Radio button toggle: ○ M1  ○ M2
- Active perspective: Full opacity, inactive: 30%
- Gamma_self panel: Both trajectories (M1 blue, M2 red)
- Identify dominant events: Which person's actions mattered more?

---

### Phase 4: Advanced Features (3-4 hours)
**Scope:** Polish, automation, sensitivity analysis

**Features:**
- Fill gaps: Linear/cubic/hold interpolation for unlocked points
- Automated sensitivity analysis: Rank events by trajectory impact
- Time unit conversion: Days ↔ Weeks ↔ Months ↔ Years
- Zoom/pan on plots
- Animation/playback mode (time sweep)
- Batch export (PNG plots)

---

**Revised Total Estimate:** ~15-20 hours for full feature set (progressive phases)

---

## Risks and Mitigation

### Risk 1: Performance Issues
**Problem:** Real-time trajectory computation slow for long scenarios (>100 events)

**Mitigation:**
- Debouncing (only recompute after 300ms of inactivity)
- Progressive rendering (show partial results)
- Caching (only recompute affected time ranges)
- Background threading (don't block UI)

### Risk 2: Inverse Editing Ambiguity
**Problem:** Multiple primitive combinations can produce same gamma_self point

**Mitigation:**
- Clear documentation that inverse mode is "suggestive, not deterministic"
- Show confidence indicators (solid vs dashed for suggestions)
- Always allow manual override with forward editing
- Provide "Reset to original" button

### Risk 3: Learning Curve
**Problem:** Complex interface may overwhelm new users

**Mitigation:**
- Guided tutorial on first launch
- Tooltips on hover for all controls
- "Simple mode" with fewer options initially
- Video tutorials and documentation
- Keyboard shortcut cheat sheet (F1)

### Risk 4: GUI Framework Lock-in
**Problem:** Matplotlib may not scale to production quality

**Mitigation:**
- Design model/controller independent of view layer
- Abstract view interface that can be reimplemented
- Consider PyQt5 migration path if needed
- Prototype with matplotlib, evaluate before committing

---

## Decision: Why Build It Now? (Updated)

### Original Decision (December 3, 2025)
**Status:** Deferred - Command-line workflow sufficient for arc-level design

### New Decision (December 4, 2025)
**Status:** Building Phase 1 - Critical for event-level diagnostic analysis

### What Changed?

**Project Evolution:**
- ✅ Arc-level design **solved** (scenario scripts work well)
- ✅ Shifted focus to **event-level analysis**
- ✅ Need to validate GRP with **real data anchor points**
- ✅ Sensitivity analysis requires **rapid iteration** on specific events
- ✅ "Which event dominated the outcome?" questions require **visual exploration**

### Key Requirements Driving Implementation

**1. Real Data Integration:**
- Lock therapy session notes (days 1, 15, 30) as anchors
- Perturb unlocked days to match observed emotional states
- Validate GRP can reproduce real relationship trajectories

**2. Constraint Validation:**
- Can GRP reach this gamma_self position with realistic primitives ([-10, +10])?
- Visual feedback reveals when model asks for unrealistic values

**3. Diagnostic Tool:**
- Granularity shift: From "design 2-month arc" to "analyze day 23 crisis"
- Manual sensitivity: Drag day 15 altruism ±2, observe trajectory impact
- Identify dominant events: Which day's action mattered most?

**4. Complementary to Scenario Scripts:**
- Not a replacement - scenarios generate baseline
- Editor loads baseline, enables fine-tuning
- Modified CSV feeds back to scenarios

### Arguments For Building Now
✅ **Event-level analysis requires visual feedback**  
✅ **Lock/unlock workflow impossible without GUI**  
✅ **Diagnostic tool for validating GRP fidelity**  
✅ **Progressive phases reduce risk (4-6 hours Phase 1)**  
✅ **Matplotlib already a dependency (no new installs)**  
✅ **User demand: "I need control and visibility at event level"**

---

## Integration with Scenario Scripts

### Workflow Integration

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: SCENARIO SCRIPT (scenarios/*.py)                        │
│ • Define research question (BACKGROUND, HYPOTHESIS)             │
│ • Set gamma_self_0, weights, time_unit                          │
│ • Reference template CSV or manual CSV                          │
│ • Run: python scenarios/singles_dating_Fred.py                  │
│ • Output: data/single_dating_to_love_M1.csv + plots             │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Baseline CSV generated
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: INTERACTIVE EDITOR (tools/interactive_editor.py)        │
│ • Load: python tools/interactive_editor.py <csv_file>           │
│ • Lock key events (real data anchors)                           │
│ • Perturb unlocked events (drag primitives)                     │
│ • Real-time gamma_self trajectory preview                       │
│ • Auto-mark customized points                                   │
│ • Save As: <csv_file>_modified.csv                              │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Modified CSV with locks/markers
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: RE-RUN SCENARIO with Modified CSV                       │
│ • Update scenario script: csv_file = '..._modified.csv'         │
│ • Re-run: python scenarios/singles_dating_Fred.py               │
│ • Generate full simulation report with customized events        │
│ • Compare: Baseline vs Modified trajectory                      │
└─────────────────────────────────────────────────────────────────┘
```

### CSV Format Compatibility

**Input Formats Supported:**
```csv
# Format 1: Minimal (old format)
step,v,r,f,a,S,notes
0,5,0,2,2,0,Initial condition
7,5,2,2,3,1,First date
...

# Format 2: Full format (with marker/locked)
step,v,r,f,a,S,notes,marker,locked
0,5,0,2,2,0,Initial condition,,*
7,5,2,2,3,1,First date,star,
...
```

**Output Format (Always):**
```csv
step,v,r,f,a,S,notes,marker,locked
0,5,0,2,2,0,Initial condition,,*
7,5,2,2,3,1,First date,circle,
15,5,4,4,5,2,Modified by user,circle,
...
```
- `marker`: Empty or "circle" (auto-added when point dragged)
- `locked`: Empty or `*` (set by right-click Lock)

---

## Future Considerations (Phase 4+)

### Fill Gaps Feature
When CSV has locked points with gaps:
```
Locked:   Day 0, Day 30, Day 60
Unlocked: Days 7, 14, 21 (to be filled)

Options:
- Linear interpolation between locks
- Cubic spline (smooth)
- Hold previous value (step function)
- Inverse heuristic (suggest primitives for target trajectory)
```

**Implementation Options:**
- **Option A:** In `scenarios/runner.py` (auto-fill when loading CSV with locks)
- **Option B:** In `interactive_editor.py` (Tools → Fill Gaps menu, visual preview)
- **Decision:** Phase 4 - Implement in `core/fill_gaps.py` (shared by both)

### Web-Based Alternative (Phase 5+)
For broader accessibility:
- Plotly Dash or Streamlit interface
- No Python installation required
- Browser-based, accessible from any device
- Can integrate with GitHub for version control

### AI-Assisted Sensitivity Analysis (Phase 5+)
Natural language queries:
```
User: "Which event had the most impact on the Q4 outcome?"

AI: Runs automated sensitivity analysis, reports:
    "Day 23 (low altruism=-5) was 3x more influential than 
     Day 15 (high resonance=7). Changing day 23 to v=-2 would 
     have resulted in Q1 instead of Q4."
```

---

## References

**Similar Tools:**
- MATLAB Curve Fitting Toolbox - Interactive spline editing
- Adobe After Effects - Keyframe animation editor
- Audacity - Audio waveform editor
- Oscilloscope arbitrary waveform generators

**GRP Integration:**
- Uses `core/love.py` for trajectory computation
- Uses `scenarios/runner.py` ScenarioRunner for re-simulation
- Compatible with scenario script configuration system

---

*Phase 1 implementation in progress as of December 4, 2025. Progressive development approach based on user feedback and validation.*
