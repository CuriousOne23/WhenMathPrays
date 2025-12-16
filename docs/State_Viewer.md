# State Viewer: Detailed Specification and Usage

## Purpose & Intent
The State Viewer is designed to provide a complete, impartial, and easily exportable record of all significant state transitions in the scenario editor. Its primary intent is to enable robust debugging, traceability, and AI-assisted analysis by capturing exactly what happened, when, and in what context—without interpretation or judgment.

## Architecture Overview
- **Location:** Implemented in `tools/editor/state_viewer.py`.
- **Integration:** Invoked from the main window (Ctrl+Shift+L) and by internal state change hooks.
- **Design:** Follows the observer pattern—records state changes as they occur, without interfering with application logic.
- **Extensibility:** New event types and state domains can be added with minimal changes.

## Log Format
Each log entry includes:
- Timestamp (ISO 8601)
- Event type (e.g., PRIMITIVE_EDIT, PERSPECTIVE_SWITCH)
- Context (perspective, event_id, primitive, old/new values, etc.)
- Optional: Stack trace or user action source (for advanced debugging)

Example:
```
[2025-12-15T14:23:01Z] PRIMITIVE_EDIT perspective=M1 event_id=2 primitive=v old=5.5 new=7.2
[2025-12-15T14:23:05Z] PERSPECTIVE_SWITCH from=M1 to=M2
```

## How to Invoke
- **Export Log:** Press Ctrl+Shift+L at any time in the editor. The log is saved to the logs/ directory with a timestamped filename.
- **Visual Feedback:** The window title and status bar confirm export and show the log file location.

## Performance Impact
- **Zero Overhead When Disabled:** Logging can be toggled off for production use, incurring no runtime cost.
- **Minimal Overhead When Enabled:** Log writes are buffered and efficient; the impact is negligible for typical editing sessions.

## When to Use
- When diagnosing UI, synchronization, or logic bugs
- For AI-assisted analysis or sharing with collaborators
- To trace the sequence of user actions and state changes
- During regression testing or after major refactors

## What Not to Put in State Viewer
- **No Business Logic:** Do not add if/then, validation, or domain-specific rules.
- **No Controllers:** State Viewer must not alter application state or make decisions.
- **No Filtering:** Log all relevant state transitions; analysis and filtering should be done by external tools.
- **No User Data:** Avoid logging sensitive or personal information; file paths are sanitized.

## Design Constraints: Impartiality & Simplicity
- **Impartial:** State Viewer records only facts—what happened, not why or whether it was correct.
- **Simple:** The codebase should remain as simple and maintainable as possible. Complexity belongs in analysis tools, not in the viewer itself.

## References
- [ARCHITECTURE.md](../ARCHITECTURE.md)
- [STATE_MANAGEMENT_REFACTORING.md](STATE_MANAGEMENT_REFACTORING.md#state-viewer-log---specification-v222)
- [interactive_editor_user_guide.md](interactive_editor_user_guide.md#8-state-viewer-log-export-new---v222)
- [tools/editor/state_viewer.py](../tools/editor/state_viewer.py)

---

*This document is the authoritative reference for the State Viewer. For user-facing instructions, see the user guide. For implementation details, see the architecture and refactoring documents.*

## Purpose
The State Viewer is a core debugging and analysis tool for the WhenMathPrays interactive scenario editor. It provides a complete, timestamped log of all state transitions, enabling rapid diagnosis of UI, synchronization, and logic bugs. The State Viewer log is designed for both human and AI-assisted analysis.

## Key Features
- **Comprehensive State Logging:** Captures all relevant state changes, including primitive edits, event insertions/deletions, perspective switches, undo/redo, and more.
- **Exportable Log:** Users can export the current state log at any time (Ctrl+Shift+L), generating a timestamped file in the logs/ directory.
- **Structured Format:** Log entries are structured for easy parsing and analysis, with clear event types, context, and before/after values.
- **Privacy/Security:** File paths and sensitive data are sanitized before export.
- **Zero Overhead When Disabled:** Logging can be toggled off for production use.

## Design Principles
- **Purity:** The State Viewer records only what happens (facts), not why or whether it is correct. No business logic or validation is embedded.
- **Separation of Concerns:** Analysis and bug detection are performed by separate tools/scripts that consume the log.
- **Extensibility:** The log format and system are designed to support future state domains and new event types.

## Log Format
Each log entry includes:
- Timestamp (ISO 8601)
- Event type (e.g., PRIMITIVE_EDIT, PERSPECTIVE_SWITCH)
- Context (perspective, event_id, primitive, old/new values, etc.)
- Optional: Stack trace or user action source (for advanced debugging)

Example:
```
[2025-12-15T14:23:01Z] PRIMITIVE_EDIT perspective=M1 event_id=2 primitive=v old=5.5 new=7.2
[2025-12-15T14:23:05Z] PERSPECTIVE_SWITCH from=M1 to=M2
```

## Usage Workflow
1. **Trigger Export:** Press Ctrl+Shift+L at any time to export the current state log.
2. **Visual Feedback:** The window title and status bar confirm export and show the log file location.
3. **Analyze Log:** Open the log file in any text editor or share with an AI assistant for diagnosis.
4. **Debugging:** Use the log to trace the sequence of state changes, identify mismatches, and isolate bugs.

## What is Logged?
- Primitive value changes (with before/after values)
- Event insertions and deletions
- Perspective switches
- Undo/redo operations
- Label/marker visibility changes
- State mapping between primitive and gamma_self domains
- Any other significant state transition relevant to scenario editing

## Implementation Notes
- The State Viewer is implemented in `tools/editor/state_viewer.py`.
- Log export is triggered via the main window (Ctrl+Shift+L shortcut).
- The log format is defined in `docs/STATE_MANAGEMENT_REFACTORING.md` (see: State Viewer Log - Specification).
- For integration and extension, see the architecture and coding guidelines.

## References
- [ARCHITECTURE.md](../ARCHITECTURE.md)
- [STATE_MANAGEMENT_REFACTORING.md](STATE_MANAGEMENT_REFACTORING.md#state-viewer-log---specification-v222)
- [interactive_editor_user_guide.md](interactive_editor_user_guide.md#8-state-viewer-log-export-new---v222)
- [tools/editor/state_viewer.py](../tools/editor/state_viewer.py)

---

*This document is the authoritative reference for the State Viewer. For user-facing instructions, see the user guide. For implementation details, see the architecture and refactoring documents.*
