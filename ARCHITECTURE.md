# Project Architecture: WhenMathPrays Scenario Editor

## Purpose
This document describes the overall architecture, object model, and design principles for the WhenMathPrays interactive scenario editor. It is intended to guide development, debugging, and future enhancements.

## Recent Updates
**December 5, 2025:** Phase 1 of interactive editor completed with maintainable UI architecture. The `interactive_editor.py` UI system has been designed with a centralized LAYOUT dictionary that consolidates all positioning constants, making future modifications and enhancements significantly easier. This architecture allows for independent positioning of UI elements (gauges, buttons, panels) without hunting through code for magic numbers.

## Directory Structure
```
/WhenMathPrays/
  README.md
  ARCHITECTURE.md
  requirements.txt
  tools/
    interactive_editor.py          # Main editor application with LAYOUT system
    editor/
      model.py                     # Data model (Events, Markers)
      controller.py                # MVC controller with trajectory computation
      views/
        primitive_panel.py         # Primitive plots with readout gauge
        trajectory_panel.py        # Gamma_self trajectory with position readout
        draggable_point.py         # Draggable marker implementation
  core/
  data/
  docs/
    interactive_editor_user_guide.md   # User guide for interactive editor
    future_interactive_edit_requirements.md  # Phase roadmap and requirements
  ...
```

## Key Objects & Classes

### Marker
Represents a visual and logical marker for an event/primitive.
- Properties: `time`, `value`, `state` (original/modified/preview), `style`, `gamma_self_value` (optional)
- Used in both primitive and gamma_self panels.

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

### Scenario
Represents the entire scenario.
- Properties: list of events, metadata, file info
- Methods: load, save, export, undo

## Design Principles
- **Structured Programming:** Code is organized into clear classes and functions with well-defined responsibilities.
- **Separation of Concerns:** Model, view, and controller logic are separated for maintainability.
- **Extensibility:** Objects are designed to be extended or modified as new features are added.
- **Debuggability:** State is explicit and easy to inspect; marker objects centralize event state.

## Data Flow Overview
- Scenario loads from CSV → Events and markers are created
- User edits marker → Marker state updates, curve redraws
- Gamma_self recalculates and pins at modified events
- Save commits all changes to CSV

## Future Directions
- Support for undo/redo via UserAction objects
- Database integration for large-scale scenario management
- Advanced analytics and visualization features

---
For more details on usage and features, see [README.md](README.md).
