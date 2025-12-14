# Project Architecture: WhenMathPrays Scenario Editor

## Purpose
This document describes the overall architecture, object model, and design principles for the WhenMathPrays interactive scenario editor. It is intended to guide development, debugging, and future enhancements.

## Recent Updates

**December 13, 2025:** Entry Point Consolidation & Observability Refactor (PLANNED):
- **🔄 Phase 1-3 Planned:** Consolidate dual entry points and add comprehensive observability
  - **Problem**: `interactive_editor.py` (1120 lines) and `application.py` (572 lines) implement duplicate logic
  - **Bug Example**: Event insertion undo failed because interactive_editor.py bypassed command system
  - **Root Cause**: Two parallel code paths with different implementations (legacy vs modern)
  - **Solution**: Migrate all logic to `application.py` + add observer pattern for full visibility
  - **Timeline**: 4 weeks (1 week per phase + cleanup)
  - **See**: [docs/architecture/entry_point_consolidation_plan.md](docs/architecture/entry_point_consolidation_plan.md)
  - **Benefits**:
    - Single code path eliminates duplicate implementations
    - Observer provides complete visibility: widget → application → controller → model
    - Debugging time reduced from 30+ minutes to <5 minutes
    - Future features only need one implementation
    - <1% performance overhead from observability

**December 13, 2025:** v2.2.0 Marker-Centric State Architecture (Debugging-First Design):
- **✅ Marker as Single Entry Point (v2.2.0):** Marker objects now own all perspective-aware state
  - **Why This Change**: Debugging complexity with scattered state across Model/Controller/View
    - Bug example: "Label persists after undo" - where's the bug?
    - Had to check: Controller label commands, Model tracking dicts, View rendering, all in different files
    - No single observation point to understand marker lifecycle
    - User mental model: "marker didn't do what I expected" → needs single place to inspect marker state
  - **Problem Pattern**: Scattered state = scattered debugging
    - `modified_primitives` dict in Model → is marker modified?
    - `marker_positions` dict in Model → where's gamma_self marker?
    - `modified_labels` dict in View → is label shown?
    - Controller coordinates all three → debugging requires tracing through 4+ files
  - **Solution**: Marker objects own their state, expose via accessor methods
    - `marker.is_modified[perspective]` - modification status
    - `marker.gamma_self_position[perspective]` - position on gamma_self plot
    - `marker.label_visible[perspective]` - label should be shown
    - Single entry point methods: `set_is_modified()`, `set_gamma_position()`, `set_label_visible()`
  - **Debugging Architecture**: "Event tree terminus pattern"
    - All state changes flow through Marker accessor methods
    - One breakpoint in accessor = catch ALL changes from any code path
    - Call stack reveals: who (controller method), what (action), why (user intent), when (sequence)
    - Compare marker state vs view rendering to isolate bugs immediately
  - **View Pattern**: Declarative/reactive (pull from marker state)
    - Controller sets marker state: `marker.set_label_visible(perspective, True)`
    - View reads marker state: `if marker.get_label_visible(perspective): show_label()`
    - View can't drift out of sync - always reads fresh marker state
    - Self-correcting on every `update_from_model()` call
  - **Benefits**:
    - Single breakpoint catches all marker state changes
    - Call stack shows complete context (who, what, why, how)
    - Marker inspection shows complete state (not scattered across 3+ dicts)
    - View synchronization bugs immediately visible (compare marker state vs rendering)
    - Extensible to arbitrary perspectives (dict keyed by perspective name)
  - **Event Source Tracking**: Events now track origin via `event.source = 'csv' | 'inserted'`
  - See detailed rationale in Marker State Architecture section below

**December 13, 2025:** v2.1.3 Event ID-based tracking system:
- **✅ Event Identity Architecture (v2.1.3):** Migrated from time-based to ID-based event tracking
  - **Why This Change**: Discovered cascade deletion bug during undo operations
    - When undoing insertions, baseline shift logic deleted keys it just created
    - Example: Shift (56.0, 'v')→(49.0, 'v') creates (49.0, 'v')=8.0
    - Then shift (49.0, 'v')→(42.0, 'v') immediately deletes (49.0, 'v') that was just created!
    - Root cause: Time-based keys change during insertions, requiring fragile shift operations
    - Fix required collect-then-apply pattern to prevent self-destruction
  - **Problem Pattern**: Time-based keys = mutable identity
    - Insert event → all subsequent times shift → all tracking dictionaries must shift
    - Baseline, modified_primitives, marker_positions, labels all shift in parallel
    - Each shift operation had cascade deletion risk
    - Undo/redo complexity exponential with each new tracking dictionary added
  - **Solution**: Immutable event IDs assigned at creation, independent of timeline position
    - Event identity never changes regardless of insertions/deletions before it
    - No shifting logic required anywhere in codebase
  - **Benefits**: 
    - Zero baseline shifting during insert/undo operations
    - Simplified state management (no cascade deletion bugs possible)
    - Enhanced debuggability (stable event identity through history)
    - Object-oriented design (event carries its own identity as attribute)
    - Extensibility: New tracking dictionaries don't need shift logic
  - **Implementation**: Events assigned monotonically increasing IDs at creation, never reused
  - **Impact**: All tracking uses `(event_id, primitive)` keys instead of `(time, primitive)`
  - See detailed rationale and implementation in event identity section below

**December 12, 2024:** Phase 3.6 Perspective Management Architecture Refactor (Design Phase):
- **🔄 Phase 3.6 Planned:** Event-driven perspective management to resolve state synchronization bugs
  - **Problem**: Manual coordination of perspective switches across 3+ components causes bugs
  - **Example Bug**: Labels from M1 perspective persist in M2 despite cleanup attempts
  - **Root Cause**: No centralized coordination, scattered state, no atomic transactions
  - **Solution**: Qt signal-based architecture + built-in observability + perspective-aware model
  - **See**: [docs/architecture/perspective_management_refactor.md](docs/architecture/perspective_management_refactor.md)
  - **Goals**: 
    - Centralized perspective state management
    - Components self-manage via Qt signals (observer pattern)
    - Built-in observability for debugging (toggle-able via EDITOR_DEBUG env var)
    - 3rd-party extensibility (documented extension points)
  - **Status**: Design complete, awaiting implementation

**December 11, 2025:** v2.1.2 baseline storage refactoring complete:
- **✅ Baseline Storage Refactoring (v2.1.2):** Migrated from index-based arrays to time-keyed dictionary
  - Replaced fragile `baseline_primitives['r'][6]` with stable `baseline_by_time[(42.0, 'r')]`
  - Removed complex array synchronization (12 operations → 5 dict operations per insert/delete)
  - Eliminated corruption risk (baseline completely independent of model)
  - All tests passing, undo/redo working correctly
  - See [docs/architecture/baseline_storage_refactoring.md](docs/architecture/baseline_storage_refactoring.md)

**December 11, 2025:** v2.1.1 undo system bug fixes and baseline storage architecture identified:
- **✅ Undo System Fixes (v2.1.1):** Critical bugs in undo/redo system resolved
  - Fixed insertion bypass: Text field insertions now create proper undo commands
  - Fixed command index instability: Commands store event **time** (stable) instead of **index** (shifts on insert/delete)
  - Fixed baseline corruption: Insert/delete operations now maintain baseline arrays correctly
  - Fixed label cleanup: Modified labels properly removed when values return to baseline
- **⚠️ Baseline Storage Architecture Issue:** Identified and documented fragility in index-based storage
  - Status: ✅ RESOLVED in v2.1.2 - migrated to time-keyed dictionary
  - See refactoring details above

**December 11, 2025:** Phase 3.4 state management refactoring completed, Phase 3.5 architecture refactoring in progress:
- **✅ Phase 3.4 Complete:** Centralized state management with `editor_state.py` module (see [STATE_MANAGEMENT_REFACTORING.md](docs/STATE_MANAGEMENT_REFACTORING.md))
  - Eliminated ~40 scattered state variables with explicit state enums
  - Observer pattern for state change notifications
  - Validated state transitions with operation guards
  - 34 comprehensive tests, all passing
  - Backward compatible integration into controller and commands
- **🔄 Phase 3.5 In Progress:** Architecture refactoring to eliminate "god class" pattern
  - ✅ Created `file_manager.py` (240 lines) - Centralized M1/M2 path resolution and file management
  - ✅ Created `ui_builder.py` (220 lines) - Extracted widget creation logic from interactive_editor.py
  - ⏳ Remaining: Application module, qt_window→main_window refactor, interactive_editor.py slimming
  - Target: Reduce interactive_editor.py from 1094 lines to ~100 line entry point
  - Benefit: Clean separation of concerns, Phase 4 readiness (multi-window architecture)

**December 7, 2025:** Phase 2.1 diagnostic markers completed - Known architectural debt documented:
- **Mixed Event System:** ✅ Being addressed in Phase 3.5 - signal-based architecture
- **Coordinate System Documentation:** PyQtGraph coordinate mapping differences documented in working code
- **Diagnostic Handler Placement:** ✅ Being addressed in Phase 3.5 - proper controller separation
- **GUI Importing Core Math:** ✅ Being addressed in Phase 3.5 - clean controller boundary
- *Status: Phase 3.5 refactoring resolves most architectural debt identified in Phase 2.1*

**December 6, 2025:** Architecture improvements for Phase 2 readiness:
- **Primitives Module (`tools/editor/primitives.py`)** - Single source of truth for primitive metadata
- **Configuration System (`tools/editor/config.py`)** - User preferences with JSON config
- **Primitive Name Updates** - Corrected UI labels: Ego→Visibility, Vulnerability→Altruism

## Related Documentation

- **[Interactive Editor Changelog](docs/INTERACTIVE_EDITOR_CHANGELOG.md)** - Version history and feature additions
- **[Interactive Editor Testing](docs/INTERACTIVE_EDITOR_TESTING.md)** - Testing strategy and quality assurance
- **[State Management Refactoring](docs/STATE_MANAGEMENT_REFACTORING.md)** - Phase 3.4 centralized state
- **[Debugging Methodology](docs/DEBUG.md)** - Systematic debugging approaches
- **[Observability Guide](tools/editor/OBSERVABILITY_GUIDE.md)** - Toggle-able logging for debugging
- **[Architecture Principles](docs/architecture/01_PRINCIPLES.md)** - Core design principles
- **[Information Flow](docs/architecture/02_INFORMATION_FLOW.md)** - Component interaction patterns
- **[API Contracts](docs/architecture/04_API_CONTRACTS.md)** - Method specifications with pre/postconditions

---

## Axis Interpretation: Identity Boundary vs Affective Quality

The GRP framework distinguishes two orthogonal dimensions:

**Real Axis (Ego ↔ We): Identity Boundary**
- **Ego-space (negative)**: Separate, distinct identities—M1 experiences self as "I" (distinct from M2)
- **We-space (positive)**: Merged, shared identity—M1 experiences self as "We", self-concept includes M2
- **Primitive**: Visibility (v) affects identity boundary through presence/absence

**Imaginary Axis (Hate ↔ Love): Affective Quality**
- **Hate (negative)**: Negative emotional states—resentment, bitterness, discord
- **Love (positive)**: Positive emotional states—warmth, care, resonance
- **Primitives**: Resonance (r), Fidelity (f), Altruism (a) affect emotional experience

**Identity Statement Test** for primitive classification:
- **Imaginary axis primitives** (r, f, a): Use action/feeling language
  - "I helped them" (action, identity remains distinct)
  - "I care about them" (feeling, identity remains distinct)
  - "I resonate with them" (emotional experience)
- **Real axis primitives** (v): Support identity language
  - "I am married to them" (defines WHO M1 is)
  - "We are partners" (shared identity statement)
  - "We are buying a house" (joint identity action)

**Key distinction**: Imaginary effects describe what M1 DOES or FEELS—identity remains distinct. Real effects define WHO M1 IS—self-concept incorporates M2.

**Examples validating orthogonality**:
- **Fan relationship**: High r/a (Love) + Ego-space (separate identity)
- **Toxic enmeshment**: Low r/a (Hate) + We-space (merged identity)
- **Marriage**: Variable affect (Love or Hate) + We-space ("I am married to them")

For detailed empirical foundation, see [gamma_self_defense.md](docs/gamma_self_defense.md).

## Marker State Architecture (v2.2.0)

### Design Principle: Event Tree Terminus Pattern

**Problem**: Complex controller orchestrates Model ↔ View synchronization across multiple state dimensions:
- Modification tracking (hollow vs filled markers)
- Gamma_self marker positions (trajectory plot)
- Label visibility (primitive panel)
- Perspective switching (M1 vs M2)

Traditional MVC scatter this state across Model dictionaries, Controller logic, and View rendering, making debugging difficult.

**Solution**: Marker as **event tree terminus** - single observable point where all state changes converge.

### Architecture Flow

```
User Action (drag, undo, insert, etc.)
    ↓
Controller logic (complex, multiple paths)
    ↓
Marker.set_is_modified(perspective, True)  ← SINGLE BREAKPOINT
Marker.set_gamma_position(perspective, pos) ← SINGLE BREAKPOINT  
Marker.set_label_visible(perspective, True) ← SINGLE BREAKPOINT
    ↓
View.update_from_model()
    ↓
View reads marker state (pull pattern)
    if marker.get_label_visible(perspective):
        show_label()
    ↓
Rendering synchronized to marker state
```

### Debugging Strategy

**Three-Layer Checkpoint System:**
```python
# Layer 1: Model/Marker state (should it be modified?)
marker.is_modified['M1']  # True

# Layer 2: Controller intention (did controller set visibility?)
marker.label_visible['M1']  # True

# Layer 3: View rendering (did view actually render it?)
(event.time, 'v') in view.modified_labels_m1  # Check actual TextItem
```

**Bug Isolation:**
- If layers 1-2 match but layer 3 differs → View refresh bug
- If layer 1 differs from layer 2 → Controller logic bug
- If all layers match but still wrong → Baseline/computation bug

**Call Stack Analysis:**
Breakpoint in `Marker.set_label_visible()` reveals:
- **Who**: Which controller method (`_apply_primitive_change`, `_insert_event`, etc.)
- **What**: User action (drag release, undo, perspective switch)
- **Why**: Intent (modification, baseline reset, cleanup)
- **When**: Sequence in operation timeline

### Perspective Extensibility

State stored in dicts keyed by perspective name:
```python
marker.is_modified = {'M1': True, 'M2': False}
marker.gamma_self_position = {'M1': 3+2j, 'M2': None}
marker.label_visible = {'M1': True, 'M2': False}
```

Adding M3 perspective requires no Marker changes - automatically supported.

### View Pull Pattern (Declarative/Reactive)

**Old (imperative - bug-prone):**
```python
# Controller directly manipulates view (4+ call sites)
self.view._add_marker_label(time, prim, value)
# Can forget to call, call twice, call at wrong time
```

**New (declarative - self-correcting):**
```python
# Controller sets marker state
marker.set_label_visible(perspective, True)

# View reads marker state on every refresh
def _sync_labels_from_markers(self, events):
    for event in events:
        for prim in ['v', 'r', 'f', 'a', 'S']:
            if event.markers[prim].get_label_visible(perspective):
                self._ensure_label_shown(event.time, prim)
```

View can't drift out of sync - always reads fresh marker state.

### Benefits Summary

1. **Single breakpoint debugging**: Catch ALL state changes from any code path
2. **Complete context**: Call stack shows who/what/why/when
3. **Isolated bug detection**: Three-layer checkpoint system pinpoints exact failure layer
4. **Self-correcting view**: Pull pattern prevents synchronization drift
5. **Perspective scalability**: Dict-based storage extends to arbitrary perspectives
6. **Maintainability**: Adding new tracking doesn't scatter code across multiple files

This pattern trades slight redundancy (state stored on marker + briefly in view dict) for dramatic debugging improvements.

## Directory Structure
```
/WhenMathPrays/
  README.md
  ARCHITECTURE.md
  requirements.txt
  tools/
    interactive_editor.py          # Main editor entry point (Phase 3.5: slimming to ~100 lines)
    editor/
      # Phase 3.4: State Management (COMPLETE)
      editor_state.py              # Centralized state management with enums and observers
      
      # Phase 3.5: Architecture Modules (IN PROGRESS)
      file_manager.py              # ✅ M1/M2 path resolution and file management (240 lines)
      ui_builder.py                # ✅ Widget creation and layout (220 lines)
      
      # Core MVC Components
      model.py                     # Data model (Events, Markers)
      controller.py                # MVC controller with trajectory computation (uses EditorState)
      commands.py                  # Undo/redo command pattern (uses EditorState)
      
      # Supporting Modules
      config.py                    # Configuration system (user preferences)
      primitives.py                # Primitive metadata constants
      qt_window.py                 # Main window (Phase 3.5: refactor to main_window.py)
      event.py                     # Event data structure
      marker.py                    # Marker data structure
      load_events.py               # CSV loading utilities
      
      views/
        primitive_panel.py         # Primitive plots with readout gauge
        trajectory_panel.py        # Gamma_self trajectory with position readout
        draggable_point.py         # Draggable marker implementation
      
      widgets/
        # UI widget components
  
  core/
    love.py                        # GRP core mathematics
  
  data/
    # Scenario CSV files
  
  docs/
    interactive_editor_user_guide.md           # User guide for interactive editor
    installation_4_interactive_editor.md       # Installation guide
    interactive_edit_roadmap.md                # Phase roadmap and requirements
    STATE_MANAGEMENT_REFACTORING.md            # Phase 3.4 state management documentation
  
  tests/
    editor/
      test_editor_state.py         # State management tests (34 tests, all passing)
  ...
```

## Key Objects & Classes

### EditorState (Phase 3.4)
Centralized state management for the entire editor application.
- **State Enums:** `PerspectiveState`, `EditState`, `TrajectoryComputeState`, `UndoRedoState`, `FileLoadState`
- **Transition Methods:** `switch_perspective()`, `start_edit()`, `mark_dirty()`, `enter_undo_operation()`, etc.
- **Validation Methods:** `can_edit_primitive()`, `can_delete_event()`, `can_insert_event()`
- **Observer Pattern:** `add_observer()`, `_notify_observers()` for UI updates
- **Singleton Access:** `get_editor_state()`, `reset_editor_state()`
- See [STATE_MANAGEMENT_REFACTORING.md](docs/STATE_MANAGEMENT_REFACTORING.md) for detailed documentation

### FileManager (Phase 3.5)
Centralized file path management and M1/M2 resolution.
- **Methods:** `validate_and_resolve()`, `get_save_path()`, `get_png_path()`, `has_dual_perspective()`
- **FileLoadResult:** Dataclass containing validation results, resolved paths, and perspective info
- Handles automatic M1↔M2 file discovery and perspective-based naming

### UIBuilder (Phase 3.5)
Widget creation and layout configuration.
- **Methods:** `build_panels()`, `build_dock_widgets()`, `build_editor_widgets()`, `build_gauges()`, `configure_layout()`
- Pure UI construction, no business logic
- Supports dual-perspective M1/M2 layouts

### Marker (v2.2.0: Perspective-Aware State Owner)
Represents a visual and logical marker for an event/primitive, now owning all perspective-specific state.

**Core Properties:**
- `time`: Event time (synchronized with parent Event)
- `value`: Primitive value at this event
- `state`: Display state ('original', 'modified', 'preview')
- `style`: Visual styling information

**Perspective-Aware State (v2.2.0):**
- `gamma_self_position`: Dict `{perspective: complex}` - where gamma_self was when this primitive was modified
- `is_modified`: Dict `{perspective: bool}` - whether modified from baseline in each perspective
- `label_visible`: Dict `{perspective: bool}` - whether label should be shown in each perspective

**Accessor Methods (Single Entry Points for Debugging):**
- `get_gamma_position(perspective)`, `set_gamma_position(perspective, pos)`, `clear_gamma_position(perspective)`
- `get_is_modified(perspective)`, `set_is_modified(perspective, modified)`, `clear_is_modified(perspective)`
- `get_label_visible(perspective)`, `set_label_visible(perspective, visible)`

**Debugging Pattern:**
Breakpoint in any `set_*()` method catches ALL changes to that state from any code path. Call stack reveals complete context (controller method → user action → event sequence).

**Design Rationale:**
- **Single observation point**: One breakpoint per state type vs. scattered across Model/Controller/View
- **Event tree terminus**: All state changes flow through Marker, making it the debugging choke point
- **Self-documenting**: Inspecting marker shows complete state, not scattered across 3+ dictionaries
- **Perspective extensibility**: Dict-based storage scales naturally to arbitrary perspectives (M1, M2, M3...)

### Event (v2.1.3: ID-Based Identity, v2.2.0: Source Tracking)
Represents a single scenario event with immutable identity and origin tracking.

**Properties:**
- `id`: Permanent, immutable identifier (integer) - assigned at creation, never changes
- `time`: Current position in timeline (mutable - changes on insertion/deletion)
- `source`: Event origin ('csv' = from file, 'inserted' = user-created via Ctrl+Shift+Click)
- `markers`: Dict of Marker objects for primitives `{v, r, f, a, S}`
- `notes`, `marker`, `locked`: Metadata fields
- References to marker objects

**Event Identity System:**
- **ID Assignment:** Events receive monotonically increasing IDs at creation (0, 1, 2, 3, ...)
- **ID Permanence:** IDs are NEVER reused, even after deletion
  - Similar to database primary keys or Social Security Numbers
  - Once ID=5 is assigned, that ID is "retired forever" if deleted
- **Counter Management:** `next_event_id` only increments, never decrements
  - After deleting event id=5, next new event gets id=6, NOT id=5
  - Prevents collision bugs when undoing deletions

**Deletion Strategy:**
- **Hard Delete:** Deleted events removed from `events` list
- **Undo Storage:** DeleteEventCommand stores complete Event object
- **Redo Cycle:** Events toggle between:
  - **Active:** Present in `events` list
  - **Dormant:** Stored in undo command, can be resurrected
- **No Soft Delete:** No `deleted` flag - events either exist in list or don't
  - Simpler code (no filtering required)
  - Better performance (no flag checks)
  - Undo stack is the "graveyard" for deleted events

**Why ID-Based Over Time-Based:**
- Time changes during insertions (event at time=49.0 shifts to time=56.0)
- IDs remain constant regardless of timeline position
- Eliminates complex baseline/label shifting logic
- Simplifies undo/redo (just reference stable ID)
- Enhanced debuggability ("trace event id=7" vs "trace whatever is at time=49.0")

**Methods:** update, reset, audit

### Primitive
Encapsulates logic/state for a single primitive (v, r, f, a, S).
- Properties: `name`, `value`, constraints, metadata

### GammaSelfPoint
Represents a computed gamma_self value at a specific time.
- Properties: `time`, `value`, `pinned` (bool), debug info

### EditorController
MVC controller managing business logic and trajectory computation.

**State Management:**
- Uses `EditorState` for centralized state management
- Coordinates between model, views, and core mathematics
- Handles primitive edits, perspective switching, undo/redo

**Event Tracking (v2.1.3):**
- `baseline_by_id[(event_id, primitive)]` - Baseline values indexed by immutable event ID
- `modified_primitives[(event_id, primitive)]` - Modified state tracking
- `next_event_id` - Monotonically increasing counter for new events
- **ID Assignment Rules:**
  - New events: `event.id = next_event_id++`
  - Deleted events: ID permanently retired, never reused
  - CSV load: IDs assigned sequentially (0, 1, 2, ...) based on file order
- **No Shifting Required:** When inserting events, baseline/modified dictionaries unchanged (IDs don't shift)

**Migration from v2.1.2:**
- v2.1.2 used `baseline_by_time[(time, primitive)]` requiring complex shift logic
- v2.1.3 uses `baseline_by_id[(event_id, primitive)]` with no shifts needed

## Design Principles
- **Structured Programming:** Code is organized into clear classes and functions with well-defined responsibilities
- **Separation of Concerns:** Model, view, and controller logic are separated for maintainability
  - Phase 3.5: FileManager (paths), UIBuilder (widgets), Controller (logic)
- **Single Source of Truth:** 
  - Primitive metadata centralized in `primitives.py`
  - Application state centralized in `EditorState` (Phase 3.4)
  - File path logic centralized in `FileManager` (Phase 3.5)
  - Configuration values loaded from JSON with sensible defaults
  - Baseline values use time-keyed dictionary (v2.1.2)
- **Immutable Event Identity:** Use event IDs as stable identifiers (v2.1.3)
  - ✅ Events have permanent IDs assigned at creation, independent of timeline position
  - ✅ Baseline storage: `baseline_by_id[(event_id, primitive)]` (v2.1.3)
  - ✅ Modified primitives tracked by ID: `modified_primitives[(event_id, primitive)]` (v2.1.3)
  - ✅ Marker positions keyed by ID: `marker_positions[(event_id, primitive)]` (v2.1.3)
  - ✅ Undo commands reference events by ID (v2.1.3)
  - **Rationale**: Time changes during insertions; IDs remain constant throughout event lifetime
- **Explicit State Management:** Phase 3.4 replaced ~40 scattered boolean flags with explicit state enums
- **Observer Pattern:** State changes trigger UI updates through registered observers (Phase 3.4)
- **Configuration Over Code:** User preferences externalized to JSON config file
- **Validated Transitions:** State changes go through validation methods preventing invalid operations
- **Extensibility:** Architecture designed for Phase 4 features (multi-window, analysis tools, inverse editing)
- **Testability:** 34 state management tests, 82 total editor tests (all passing)
- **Debuggability:** State is explicit and easy to inspect; marker objects centralize event state

## Data Flow Overview

### File Loading (uses FileManager + EditorState)
1. User provides CSV path → FileManager validates and resolves M1/M2 pair
2. EditorState transitions: `FILE_NOT_LOADED` → `FILE_LOADING` → `FILE_LOADED`
3. Events and markers created from CSV data
4. Perspective set based on file availability (M1 or M2)

### Editing Flow (uses EditorState + Controller)
1. User edits marker → EditorState validates operation with `can_edit_primitive()`
2. EditorState transitions: `NO_EDIT` → `EDITING` (marks dirty)
3. Marker state updates, curve redraws
4. Controller triggers trajectory recomputation
5. EditorState transitions: `TRAJECTORY_COMPUTING` → `TRAJECTORY_READY` (marks clean)
6. Observer notifications update UI gauges and readouts

### Perspective Switching (uses EditorState)
1. User clicks M1/M2 button → EditorState validates with `can_switch_perspective()`
2. EditorState transitions perspective: `M1` ↔ `M2`
3. Controller reloads events from alternate perspective file
4. UI rebuilds panels with new data
5. Observers notified to update button states

### Undo/Redo (uses EditorState + Command Pattern)
1. EditorState tracks: `CAN_UNDO`, `CAN_REDO`, `IN_UNDO_REDO`
2. Commands use `enter_undo_operation()` / `exit_undo_operation()`
3. Prevents recursive undo during undo execution
4. Trajectory recomputation triggered after command execution

### Save Flow (uses FileManager)
1. User clicks Save → FileManager determines correct save path based on active perspective
2. Modified events written to CSV
3. EditorState marks file as clean

## Phase 4 Roadmap (Future Directions)

See [interactive_edit_roadmap.md](docs/interactive_edit_roadmap.md) for complete Phase 4 requirements:

- **Analysis Window:** Separate synchronized window for advanced analysis
- **Inverse Editing:** Drag gamma_self to suggest primitive changes
- **Sensitivity Analysis:** Automated ranking of primitive influence
- **Batch Export:** Multiple PNG exports with templating
- **Interpolation Tools:** Fill gaps in trajectory data
- **Animation/Playback:** Time-based trajectory visualization
- **Constraint Validation:** Multi-primitive constraint checking
- **Database Integration:** Large-scale scenario management

**Architecture Readiness:**
Phase 3.5 refactoring prepares for Phase 4 by:
- Enabling multi-window architecture (shared model/controller)
- Supporting tool plugins (sensitivity, inverse solver)
- Establishing event-driven communication patterns
- Centralizing export pipeline for batch operations

---

## Related Documentation

### Current Architecture
- **User Guide:** [docs/interactive_editor_user_guide.md](docs/interactive_editor_user_guide.md)
- **Installation:** [docs/installation_4_interactive_editor.md](docs/installation_4_interactive_editor.md)
- **Debugging Guide:** [docs/DEBUG.md](docs/DEBUG.md) - Debug infrastructure and methodology
- **State Management:** [docs/STATE_MANAGEMENT_REFACTORING.md](docs/STATE_MANAGEMENT_REFACTORING.md)
- **Architecture Recommendations:** [docs/architecture_recommendations.md](docs/architecture_recommendations.md)
- **Baseline Storage Refactoring:** [docs/architecture/baseline_storage_refactoring.md](docs/architecture/baseline_storage_refactoring.md)
- **Baseline Communication Protocol:** [docs/baseline_communication_protocol.md](docs/baseline_communication_protocol.md)
- **Version History:** [docs/INTERACTIVE_EDITOR_CHANGELOG.md](docs/INTERACTIVE_EDITOR_CHANGELOG.md)

### Planned Refactoring
- **Entry Point Consolidation:** [docs/architecture/entry_point_consolidation_plan.md](docs/architecture/entry_point_consolidation_plan.md) - Dual entry point consolidation + observability
- **Phase Roadmap:** [docs/interactive_edit_roadmap.md](docs/interactive_edit_roadmap.md)

### General
- **Main README:** [README.md](README.md)

---

For more details on usage and features, see the documentation links above.
