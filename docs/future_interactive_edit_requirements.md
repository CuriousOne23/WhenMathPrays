# Future Interactive Editor - Requirements and Design

**Status:** Not yet implemented  
**Priority:** Optional enhancement  
**Complexity:** High (~40-60 hours)  
**Date:** December 3, 2025

---

## Executive Summary

The interactive waveform editor would provide a graphical interface for creating and editing scenarios, similar to arbitrary waveform generators used in oscilloscopes and signal processing. Users could drag primitive curves and gamma_self trajectory points to shape relationship dynamics visually, with real-time updates and bidirectional editing.

**Key Decision:** Deferred in favor of simpler command-line tools + manual CSV editing. The current workflow (generator + converter + CSV editing) is sufficient for most use cases and avoids GUI complexity.

---

## Core Concept

### The Problem
- CSV editing requires understanding primitive values and their effects
- No visual feedback until running the scenario
- Difficult to design complex asymmetric dual scenarios
- Trial-and-error workflow to achieve desired trajectory shape

### The Solution
A graphical editor with:
1. **Visual primitive editing** - Drag curves to shape v, r, f, a, S over time
2. **Trajectory preview** - See gamma_self path update in real-time
3. **Bidirectional editing** - Drag gamma_self points to suggest primitive changes
4. **Dual perspective** - Edit M1 and M2 simultaneously with synchronized timeline

---

## Architecture Design

### Three-Panel Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  [Radio] ○ M1  ○ M2         Interactive Scenario Editor         │
├──────────────────────┬──────────────────────┬───────────────────┤
│                      │                      │                   │
│   M1 PRIMITIVES      │   M2 PRIMITIVES      │  GAMMA_SELF PLANE │
│   (Blue tones)       │   (Red tones)        │  (Combined view)  │
│                      │                      │                   │
│  v ────────────      │  v ────────────      │     ^  Love       │
│  r ────────────      │  r ────────────      │     │             │
│  f ────────────      │  f ────────────      │     │   Q2  Q1    │
│  a ────────────      │  a ────────────      │  ───┼───          │
│  S ────────────      │  S ────────────      │  Ego│We           │
│                      │                      │     │   Q3  Q4    │
│  [Time axis]         │  [Time axis]         │     v  Hate       │
│                      │                      │                   │
│  • Drag control pts  │  • Drag control pts  │  • M1 trajectory  │
│  • Add/delete pts    │  • Add/delete pts    │  • M2 trajectory  │
│  • Locked grayed     │  • Locked grayed     │  • Drag endpoints │
│                      │                      │  • See real-time  │
└──────────────────────┴──────────────────────┴───────────────────┘
```

### Technology Stack

**Option A: Matplotlib (Recommended)**
- Pros: Already a dependency, good event handling, familiar to Python users
- Cons: Not as polished as dedicated GUI frameworks
- Implementation: `matplotlib.widgets` for interactive elements

**Option B: PyQt5/PySide6**
- Pros: Professional GUI, better performance, more control
- Cons: New dependency, steeper learning curve, licensing considerations
- Implementation: Custom widget classes with signal/slot architecture

**Option C: Web-based (Plotly Dash / Streamlit)**
- Pros: Modern interface, easy deployment, cross-platform
- Cons: Requires web server, more complex architecture
- Implementation: Flask backend + JavaScript frontend

**Recommendation:** Start with Matplotlib for proof-of-concept, migrate to PyQt5 if needed.

---

## Feature Specifications

### 1. Primitive Curve Editing

**Visual Representation:**
- Each primitive (v, r, f, a, S) as a line plot over time
- Control points at each event time (draggable circles)
- Spline interpolation between points for smooth preview
- Color coding:
  - M1 primitives: Shades of blue (#0066CC to #99CCFF)
  - M2 primitives: Shades of red (#CC0000 to #FF9999)
  - Locked points: Gray with diagonal hatching

**Interactions:**
- **Click-and-drag** control points vertically (change primitive value)
- **Shift-click** to add new control point at cursor time
- **Delete key** to remove selected control point (if unlocked)
- **Hover** shows tooltip with exact values (time, primitive value)
- **Snap to grid** option for integer time/value alignment

**Constraints:**
- Vertical drag clamped to [-10, +10] range
- Locked points non-draggable (grayed out)
- First and last points always locked by default
- Horizontal dragging disabled (time stays fixed)

### 2. Gamma_Self Trajectory Visualization

**Display:**
- Real-time trajectory computed from current primitives
- M1 trajectory: Solid blue line with blue markers
- M2 trajectory: Solid red line with red markers
- Quadrant lines and labels
- Start/end markers clearly visible
- Current time indicator (vertical line synced across panels)

**Updates:**
- Recompute trajectory on mouse release (not during drag for performance)
- Show "Computing..." overlay during calculation
- Highlight affected region when editing specific time range

**Interactions:**
- **Drag trajectory points** to suggest primitive changes (see Bidirectional Editing)
- **Click point** to select and show details (time, gamma_x, gamma_y, magnitude)
- **Zoom/pan** with mouse wheel and middle-click drag
- **Reset view** button to auto-scale to data

### 3. Bidirectional Editing

**Forward Mode (Primitives → Gamma_Self):**
- Standard mode: Drag primitives, see trajectory update
- Direct computation using `update_gamma_self()`
- Fast and deterministic

**Inverse Mode (Gamma_Self → Primitives):**
- Experimental: Drag gamma_self point, primitives adjust
- **Challenge:** One trajectory point ≠ unique primitive values
- **Solution:** Heuristic inverse estimation

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

### 4. Radio Button Selection (M1/M2)

**Purpose:**
- Focus editing on one perspective at a time
- Reduces visual clutter
- Prevents accidental modification of wrong perspective

**Behavior:**
- Selected perspective: Full opacity, active drag handlers
- Unselected perspective: 30% opacity, view-only
- Gamma_self panel always shows both (for context)
- Keyboard shortcut: Tab to toggle between M1/M2

### 5. Timeline Management

**Time Axis Features:**
- **Zoom:** Mouse wheel or pinch gesture
- **Pan:** Click-drag on axis
- **Add time point:** Right-click on axis → "Insert event here"
- **Delete time point:** Select point → Delete key (if unlocked)
- **Negative time:** Extend axis left of zero for prehistory

**Non-Contiguous Support:**
- Visual gap indicators (hatched regions)
- "Fill gaps" button with interpolation options (hold/linear)
- Warning icon if large gaps exist

**Time Unit Selection:**
- Dropdown: Days / Weeks / Months / Years
- Auto-rescales axis and values
- Uses `convert_time_units()` internally

### 6. Marker and Lock Management

**Marker Assignment:**
- Right-click point → "Add marker" → Choose type (star/circle/square/etc.)
- Markers shown as colored symbols on gamma_self plot
- Legend shows marker meanings

**Lock Toggle:**
- Right-click point → "Lock" / "Unlock"
- Visual: Locked points have gray fill + diagonal lines
- Locked points cannot be dragged or deleted
- "Lock all" / "Unlock all" buttons for batch operations

### 7. File Operations

**Load:**
- File → Open CSV (single or M1/M2 pair)
- Auto-detects metadata (name, time_unit)
- Validates CSV format
- Displays warnings for missing/invalid data

**Save:**
- File → Save (overwrites current)
- File → Save As (new filename)
- Exports with all metadata preserved
- Option: "Export both M1 and M2" for dual scenarios

**Import/Export:**
- Import from generator output (validates format)
- Export to different time units
- Batch export (generate PNG plots automatically)

### 8. Real-Time Computation

**Performance Considerations:**
- Trajectory computation can be expensive (100+ events)
- **Solution:** Debouncing and progressive rendering

**Optimization Strategy:**
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

**Progressive Rendering:**
- Show first 10 events immediately (< 10ms)
- Render remaining events in background
- Update display as more points complete
- "Still computing..." indicator for long scenarios

### 9. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Tab | Toggle M1 ⇄ M2 selection |
| Ctrl+Z | Undo last change |
| Ctrl+Y | Redo |
| Ctrl+S | Save file |
| Ctrl+O | Open file |
| Delete | Delete selected point (if unlocked) |
| Shift+Click | Add new control point |
| Ctrl+L | Toggle lock on selected point |
| Ctrl+M | Add marker to selected point |
| Space | Play animation (time sweep) |
| Esc | Cancel current drag operation |
| Ctrl+D | Duplicate selected point |
| Ctrl+G | Toggle grid snap |

### 10. Undo/Redo System

**Implementation:**
- Command pattern for all edits
- Stack limit: 50 operations
- Memory efficient (store deltas, not full copies)

**Undoable Operations:**
- Primitive value changes
- Point additions/deletions
- Lock status changes
- Marker changes
- Time unit conversions

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

### Workflow 1: Create New Scenario from Scratch

1. Launch editor: `python tools/scenario_editor.py`
2. File → New → Single/Dual
3. Set name and time unit
4. Click "Generate base" → Choose arc type
5. Adjust primitives by dragging control points
6. Add markers at key events (right-click → Add marker)
7. Watch gamma_self trajectory update in real-time
8. File → Save → Export to `data/my_scenario.csv`

### Workflow 2: Edit Existing Scenario

1. File → Open → Select `my_scenario.csv`
2. Switch to M1 or M2 (if dual)
3. Identify unlocked control points (not grayed)
4. Drag primitives up/down to adjust
5. Add new events with Shift+Click
6. Delete events with Delete key
7. Toggle locks with Ctrl+L
8. Save changes

### Workflow 3: Design Dual Asymmetric Scenario

1. File → New → Dual perspective
2. Generate base arc for both M1 and M2
3. Select M1 (radio button or Tab)
4. Edit M1 primitives (M2 fades to 30% opacity)
5. Tab to switch to M2
6. Edit M2 primitives to create asymmetry
7. Both trajectories visible on gamma_self panel
8. Compare magnitudes and quadrant positions
9. Export both files

### Workflow 4: Inverse Editing (Advanced)

1. Load scenario
2. Click "Inverse mode" button
3. Gamma_self trajectory points become draggable
4. Drag endpoint to desired position
5. Editor suggests primitive changes (shown as dashed lines)
6. Review suggestions
7. Click "Accept" or "Reject"
8. Fine-tune with forward editing if needed

---

## Development Roadmap

### Phase 1: Proof of Concept (1 week)
- Basic matplotlib window with 3 panels
- Load CSV and display primitives + trajectory
- Draggable control points (forward editing only)
- No undo/redo, minimal features

### Phase 2: Core Features (2 weeks)
- Add/delete control points
- Lock/unlock functionality
- Marker assignment
- Save/load files
- Undo/redo system
- Keyboard shortcuts

### Phase 3: Polish (1 week)
- Dual perspective support with M1/M2 toggle
- Time unit conversion
- Interpolation for gaps
- Real-time computation optimization
- Error handling and validation

### Phase 4: Advanced Features (2 weeks)
- Inverse editing (gamma_self → primitives)
- Animation/playback mode
- Batch operations
- Templates and presets
- Export to multiple formats

### Phase 5: Production Ready (1 week)
- Comprehensive testing
- Documentation and tutorials
- Performance profiling and optimization
- Packaging and distribution

**Total Estimate:** 7 weeks (40-60 hours) for full implementation

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

## Decision: Why Not Built Yet?

### Arguments For Building It
✅ Professional interface for non-technical users  
✅ Visual feedback accelerates scenario design  
✅ Bidirectional editing is intellectually interesting  
✅ Dual perspective editing difficult without visualization  
✅ Reduces trial-and-error cycles  

### Arguments Against (Why We Chose Not To)
❌ Complexity: 40-60 hours vs current 15-20 hours  
❌ Maintenance burden: GUIs need ongoing support  
❌ Dependencies: Additional packages to manage  
❌ Learning curve: New tool to learn vs familiar CSV editing  
❌ **Most users comfortable with spreadsheets/text editors**  
❌ **Command-line workflow already sufficient for core use cases**  

### Current Recommendation
**Wait for user demand.** If multiple people request visual editing or if scenario complexity increases significantly, revisit this. The design is complete and ready to implement.

---

## Future Considerations

### Web-Based Alternative
A simpler alternative might be a web-based editor:
- No Python installation required
- Accessible from any device
- Easier to share and collaborate
- Can integrate with GitHub for version control

**Technology:** Plotly Dash or Streamlit + GitHub Pages

### AI-Assisted Scenario Generation
Future enhancement: Natural language scenario generation
```
User: "Create a scenario where two people meet casually, have a crisis at 3 weeks,
       but recover and fall in love by 2 months"

AI: Generates CSV with appropriate arc shape, primitives, and markers
```

Uses GPT-4 with UREP domain knowledge to suggest realistic primitive sequences.

---

## References

**Similar Tools:**
- MATLAB Curve Fitting Toolbox - Interactive spline editing
- Adobe After Effects - Keyframe animation editor
- Audacity - Audio waveform editor
- Microsoft Power BI - Interactive data visualization

**Design Inspiration:**
- Arbitrary waveform generators (oscilloscopes)
- Video editing timeline interfaces
- Audio synthesizer envelope editors

---

*This document captures the complete design for a future interactive editor. Implementation deferred pending user demand and project priorities.*
