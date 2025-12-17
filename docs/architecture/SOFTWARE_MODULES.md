# Software Modules Reference

This document provides a comprehensive reference for all software modules in the WhenMathPrays interactive scenario editor. Each module is documented with its location, purpose, key input/output variables, and relationships to other components.

## Table of Contents

- [Core Architecture](#core-architecture)
- [MVC Components](#mvc-components)
- [View Components](#view-components)
- [Widget Components](#widget-components)
- [Utility Modules](#utility-modules)
- [Testing Framework](#testing-framework)
- [Related Documentation](#related-documentation)

## Core Architecture

### interactive_editor.py
**Location:** `tools/interactive_editor.py`  
**Purpose:** Main application entry point and orchestration layer for the interactive scenario editor.  
**Lines:** ~100 (Phase 3.5 target)  
**Key IO Variables:**
- Input: `sys.argv` (command line arguments, primarily CSV file path)
- Output: QApplication execution, GUI display
- Internal: EditorModel, EditorController, main window instances

**Responsibilities:**
- Parse command line arguments
- Initialize PySide6 application
- Load scenario data from CSV
- Create and wire MVC components
- Launch main window
- Handle application lifecycle

### editor_state.py
**Location:** `tools/editor/editor_state.py`  
**Purpose:** Centralized state management system using enums and observer pattern for the entire editor application.  
**Lines:** ~400  
**Key IO Variables:**
- Input: State transition requests (perspective switches, edit operations, file operations)
- Output: State change notifications to observers
- Internal: PerspectiveState, EditState, TrajectoryComputeState, UndoRedoState, FileLoadState enums

**Responsibilities:**
- Manage application-wide state transitions
- Validate state-dependent operations
- Notify observers of state changes
- Provide state query methods
- Coordinate undo/redo operations

## MVC Components

### model.py
**Location:** `tools/editor/model.py`  
**Purpose:** Data model for scenario events, modifications tracking, and CSV I/O operations.  
**Lines:** ~800  
**Key IO Variables:**
- Input: CSV file paths, primitive modification requests, event operations
- Output: Event lists, gamma trajectory data, modification tracking
- Internal: events_m1/events_m2 (EventPoint lists), modified_primitives (dict), gamma_self_0 values

**Responsibilities:**
- Load/save scenario data from/to CSV files
- Track primitive modifications by event ID
- Compute gamma_self trajectories
- Manage event insertion/deletion
- Handle perspective-specific data (M1/M2)

### controller.py
**Location:** `tools/editor/controller.py`  
**Purpose:** MVC controller coordinating user interactions, business logic, and view updates.  
**Lines:** ~600  
**Key IO Variables:**
- Input: User actions (primitive edits, event operations), model data
- Output: View update commands, undo/redo operations
- Internal: EditorState instance, undo stack, trajectory data

**Responsibilities:**
- Handle user interaction events
- Coordinate model updates
- Manage undo/redo operations
- Update all views after model changes
- Validate user operations against current state

### commands.py
**Location:** `tools/editor/commands.py`  
**Purpose:** Implementation of command pattern for undo/redo operations.  
**Lines:** ~300  
**Key IO Variables:**
- Input: Operation parameters (event indices, primitive values, time points)
- Output: State change notifications, undo/redo actions
- Internal: Command instances (InsertEventCommand, DeleteEventCommand, etc.)

**Responsibilities:**
- Execute reversible operations
- Maintain operation history
- Support undo/redo functionality
- Validate command preconditions
- Update model state atomically

## View Components

### primitive_panel_pyqtgraph.py
**Location:** `tools/editor/views/primitive_panel_pyqtgraph.py`  
**Purpose:** High-performance PyQtGraph-based visualization of GRP primitives with interactive editing.  
**Lines:** ~1400  
**Key IO Variables:**
- Input: Event data, primitive values, user interaction events
- Output: Visual plots, user action signals, diagnostic markers
- Internal: Plot items, scatter plots, diagnostic overlays

**Responsibilities:**
- Render 5 primitive plots (v, r, f, a, S)
- Handle mouse interactions (drag, click, Ctrl+click)
- Display diagnostic markers and labels
- Manage plot synchronization
- Support perspective switching

### trajectory_panel_pyqtgraph.py
**Location:** `tools/editor/views/trajectory_panel_pyqtgraph.py`  
**Purpose:** Visualization of gamma_self trajectory with position readouts and interactive markers.  
**Lines:** ~300  
**Key IO Variables:**
- Input: Gamma trajectory data, user click events
- Output: Trajectory plot, position readouts, click signals
- Internal: Trajectory curve, position markers

**Responsibilities:**
- Plot gamma_self trajectory
- Display current position readouts
- Handle trajectory clicks for position updates
- Support diagnostic marker placement

## Widget Components

### ui_builder.py
**Location:** `tools/editor/ui_builder.py`  
**Purpose:** Centralized widget creation and layout configuration for the editor interface.  
**Lines:** ~220  
**Key IO Variables:**
- Input: Layout specifications, widget configurations
- Output: Configured widget hierarchies, dock layouts
- Internal: Panel instances, widget collections

**Responsibilities:**
- Create all UI panels and widgets
- Configure dock widget layouts
- Setup widget interconnections
- Support dual-perspective (M1/M2) layouts

### insertion_options.py
**Location:** `tools/editor/widgets/insertion_options.py`  
**Purpose:** Widget for managing explicit time points for event insertion.  
**Lines:** ~200  
**Key IO Variables:**
- Input: User time inputs, insertion requests
- Output: insertions_changed signal with time list
- Internal: Time input widgets, validation logic

**Responsibilities:**
- Collect user-specified insertion times
- Validate time inputs
- Prevent duplicate times
- Emit insertion requests

### gamma_self0_editor.py
**Location:** `tools/editor/widgets/gamma_self0_editor.py`  
**Purpose:** Widget for editing initial gamma_self state position.  
**Lines:** ~150  
**Key IO Variables:**
- Input: Initial complex value, user edits
- Output: value_changed signal, reset_requested signal
- Internal: Real/imaginary spinboxes

**Responsibilities:**
- Display complex number input controls
- Validate numeric inputs
- Support reset to original values
- Emit value change notifications

## Utility Modules

### debug_config.py
**Location:** `tools/editor/debug_config.py`  
**Purpose:** Centralized logging configuration and debug flag management.  
**Lines:** ~140  
**Key IO Variables:**
- Input: Environment variables (LOG_LEVEL, LOG_TO_TERMINAL)
- Output: Logger instances, debug flags
- Internal: Logging handlers, formatters

**Responsibilities:**
- Setup Python logging system
- Provide module-specific loggers
- Manage debug flag states
- Configure log file output

### config.py
**Location:** `tools/editor/config.py`  
**Purpose:** User preferences and configuration management system.  
**Lines:** ~100  
**Key IO Variables:**
- Input: Configuration file path, user preferences
- Output: Configuration values, validation results
- Internal: JSON configuration data

**Responsibilities:**
- Load/save user preferences
- Provide configuration defaults
- Validate configuration values
- Support runtime configuration changes

### primitives.py
**Location:** `tools/editor/primitives.py`  
**Purpose:** Single source of truth for GRP primitive metadata and constants.  
**Lines:** ~80  
**Key IO Variables:**
- Output: Primitive names, labels, colors, ranges
- Internal: PRIMITIVE_NAMES, PRIMITIVE_LABELS, etc. constants

**Responsibilities:**
- Define primitive properties
- Provide display metadata
- Centralize primitive constants
- Support primitive enumeration

### file_manager.py
**Location:** `tools/editor/file_manager.py`  
**Purpose:** Centralized file path management and M1/M2 file resolution.  
**Lines:** ~240  
**Key IO Variables:**
- Input: File paths, perspective requests
- Output: FileLoadResult with resolved paths
- Internal: Path resolution logic, validation results

**Responsibilities:**
- Resolve M1/M2 file pairs
- Validate file existence
- Generate save paths
- Handle file discovery logic

### load_events.py
**Location:** `tools/editor/load_events.py`  
**Purpose:** CSV parsing and event data loading utilities.  
**Lines:** ~150  
**Key IO Variables:**
- Input: CSV file paths, start event IDs
- Output: Event lists, metadata dictionaries
- Internal: CSV parsing logic, validation

**Responsibilities:**
- Parse CSV scenario files
- Extract metadata (gamma_self_0, time_unit, names)
- Create EventPoint instances
- Handle CSV format validation

### event.py
**Location:** `tools/editor/event.py`  
**Purpose:** Data structure definitions for scenario events.  
**Lines:** ~50  
**Key IO Variables:**
- Output: EventPoint dataclass instances
- Internal: Event attributes (time, primitives, metadata)

**Responsibilities:**
- Define EventPoint structure
- Provide event serialization
- Support event comparison operations

### marker.py
**Location:** `tools/editor/marker.py`  
**Purpose:** Data structure for primitive markers with perspective-aware state.  
**Lines:** ~100  
**Key IO Variables:**
- Input: Primitive values, perspective context
- Output: Marker state, gamma positions
- Internal: Perspective-specific marker data

**Responsibilities:**
- Manage marker visibility
- Track gamma_self positions
- Support perspective switching
- Handle marker serialization

## Testing Framework

### test_editor_state.py
**Location:** `tests/editor/test_editor_state.py`  
**Purpose:** Comprehensive test suite for the EditorState system.  
**Lines:** ~400  
**Test Coverage:** 34 tests, all passing  
**Key IO Variables:**
- Input: State transition scenarios
- Output: State validation results
- Internal: Mock observers, state assertions

**Responsibilities:**
- Test state transitions
- Validate observer notifications
- Verify state-dependent operations
- Ensure thread safety

## Related Documentation

- **[ARCHITECTURE.md](../ARCHITECTURE.md)** - Overall system architecture and design principles
- **[DEBUG.md](../DEBUG.md)** - Debugging guide and logging configuration
- **[interactive_editor_user_guide.md](../interactive_editor_user_guide.md)** - User guide for the interactive editor
- **[INTERACTIVE_EDITOR_TESTING.md](../INTERACTIVE_EDITOR_TESTING.md)** - Testing methodology and procedures
- **[STATE_MANAGEMENT_REFACTORING.md](../STATE_MANAGEMENT_REFACTORING.md)** - Phase 3.4 state management documentation
- **[interactive_edit_roadmap.md](../interactive_edit_roadmap.md)** - Development roadmap and requirements</content>
<parameter name="filePath">c:\Users\jeffg\Documents\GitHub\WhenMathPrays\docs\architecture\SOFTWARE_MODULES.md