# Project Architecture: WhenMathPrays Scenario Editor

## Purpose
This document describes the overall architecture, object model, and design principles for the WhenMathPrays interactive scenario editor. It is intended to guide development, debugging, and future enhancements.

## Recent Updates

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

### Marker
Represents a visual and logical marker for an event/primitive.
- Properties: `time`, `value`, `state` (original/modified/preview), `style`, `gamma_self_value` (optional)
- Used in both primitive and gamma_self panels

### Event
Represents a single scenario event.
- Properties: `time`, all primitive values, references to marker objects
- Methods: update, reset, audit

### Primitive
Encapsulates logic/state for a single primitive (v, r, f, a, S).
- Properties: `name`, `value`, constraints, metadata

### GammaSelfPoint
Represents a computed gamma_self value at a specific time.
- Properties: `time`, `value`, `pinned` (bool), debug info

### EditorController
MVC controller managing business logic and trajectory computation.
- Uses `EditorState` for centralized state management
- Coordinates between model, views, and core mathematics
- Handles primitive edits, perspective switching, undo/redo

## Design Principles
- **Structured Programming:** Code is organized into clear classes and functions with well-defined responsibilities
- **Separation of Concerns:** Model, view, and controller logic are separated for maintainability
  - Phase 3.5: FileManager (paths), UIBuilder (widgets), Controller (logic)
- **Single Source of Truth:** 
  - Primitive metadata centralized in `primitives.py`
  - Application state centralized in `EditorState` (Phase 3.4)
  - File path logic centralized in `FileManager` (Phase 3.5)
  - Configuration values loaded from JSON with sensible defaults
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

- **User Guide:** [docs/interactive_editor_user_guide.md](docs/interactive_editor_user_guide.md)
- **Installation:** [docs/installation_4_interactive_editor.md](docs/installation_4_interactive_editor.md)
- **State Management:** [docs/STATE_MANAGEMENT_REFACTORING.md](docs/STATE_MANAGEMENT_REFACTORING.md)
- **Phase Roadmap:** [docs/interactive_edit_roadmap.md](docs/interactive_edit_roadmap.md)
- **Main README:** [README.md](README.md)

---

For more details on usage and features, see the documentation links above.
