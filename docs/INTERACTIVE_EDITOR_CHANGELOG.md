# Interactive Editor - Version History

## Related Documentation

- **[Interactive Editor Testing](INTERACTIVE_EDITOR_TESTING.md)** - Testing strategy and quality assurance
- **[Architecture](../ARCHITECTURE.md)** - Overall system architecture (see [MVT Quality Standard](../ARCHITECTURE.md#mvt-quality-standard))
- **[State Management Refactoring](STATE_MANAGEMENT_REFACTORING.md)** - Phase 3.4 centralized state
- **[Debugging Methodology](DEBUG.md)** - Systematic debugging approaches

---

## Quality Standard

All versions follow the **MVT standard** (Modeled, Verifiable, Testable):
- Clean architecture patterns
- Observable behavior with clear validation
- Test coverage for regression prevention

See [ARCHITECTURE.md](../ARCHITECTURE.md#mvt-quality-standard) for complete definition.

---

## Version Tracking Strategy

**Branching:**
- `main` - Stable releases only
- `phase2` - Active Phase 2 development
- `phase3` - Future Phase 3 development (when started)

**Tags:**
- Mark stable checkpoints during development
- Tag format: `v{phase}.{feature}-{description}`
- Example: `v2.0-undo-redo`, `v2.1-event-management`

**Rollback:**
```bash
# View all tags
git tag -l

# Go to specific version
git checkout v2.0-undo-redo

# Return to development
git checkout phase2
```

---

## Version History

### v2.2.3-double-click-reset (December 17, 2025)
**Status:** ✅ Complete - Bug fix and feature implementation

**Bug Fixed:** Double-click reset functionality for primitive markers
- ✅ **Root Cause Identified:** ResetPrimitiveCommand was created but never pushed to undo stack
- ✅ **Signal Chain Completed:** Added missing `self.undo_stack.push(command)` in controller._do_primitive_reset_logic
- ✅ **Mouse Event Handling:** Added `sigPointDoubleClicked` signal to DraggableScatterItem class
- ✅ **Signal Processing:** Added `_on_point_double_clicked` method to PrimitivePanelPyQtGraph for event handling

**Technical Implementation:**
- **Signal Emission:** DraggableScatterItem emits sigPointDoubleClicked on mouse double-click events
- **Event Processing:** PrimitivePanelPyQtGraph receives signal and emits primitive_reset_requested
- **Controller Logic:** EditorController processes reset request and creates ResetPrimitiveCommand
- **Undo Integration:** Fixed critical bug where command was created but not pushed to undo stack
- **Model Update:** ResetPrimitiveCommand.redo() resets primitive values to baseline CSV values

**User Experience:**
- Double-clicking any primitive marker now resets its value to the original baseline
- Undo (Ctrl+Z) and redo (Ctrl+Y) work correctly for reset operations
- Visual feedback shows immediate value change and label updates
- Consistent with user expectations from interactive editor design

**Debugging Integration:**
- Full event correlation tracking with unique IDs
- Comprehensive logging for mouse events, hit detection, signal emission, and command execution
- Integrated with debug_gui.py infrastructure for troubleshooting

**Testing:**
- Manual verification: Double-click markers successfully reset to baseline values
- Undo/redo verification: Reset operations can be undone and redone
- Signal chain verification: Debug logs confirm complete event flow
- Regression testing: Existing functionality remains unaffected

**MVT Compliance:**
- ✅ Modeled: Clean signal/slot architecture with proper separation of concerns
- ✅ Verifiable: Immediate visual feedback and debug logging confirm functionality
- ✅ Testable: Manual test procedures and automated verification possible

---

### v2.2.2-state-viewer-log (December 14, 2025)
**Status:** ✅ Complete - Infrastructure ready for full state tracking

**Feature: State Viewer Log Export**
- ➕ **Keyboard shortcut** - Ctrl+Shift+L exports state log to `logs/state_log_YYYYMMDD_HHMMSS.txt`
- ➕ **Visual feedback** - Window title shows [STATE LOG EXPORTED] for 5 seconds
- ➕ **Status bar notification** - Shows file path where log was saved
- ➕ **Message box confirmation** - Informs user about export location
- ➕ **Auto-directory creation** - Creates `logs/` directory if it doesn't exist
- ➕ **Timestamped filenames** - Never overwrites previous logs

**Purpose:**
- Enable rapid debugging through state transition logs
- Facilitate AI-assisted bug diagnosis (share log file with assistant)
- Provide visibility into complex state machines
- Support post-mortem analysis of unexpected behavior

**Implementation:**
- Added `_on_export_state_log()` method in `main_window.py`
- Placeholder log created with session metadata
- Infrastructure ready for full StateViewer integration (future)

**Use Cases:**
- Debug marker label not clearing after reset
- Understand sequence of operations leading to unexpected state
- Share structured log with AI for rapid diagnosis
- Learn program behavior while onboarding

**Documentation:**
- Updated user guide with State Viewer Log section
- Added to keyboard shortcuts reference
- Added troubleshooting entry for debugging state issues

**MVT Compliance:**
- ✅ Modeled: Clear state export architecture
- ✅ Verifiable: Visual feedback (title, status, dialog)
- ✅ Testable: Press Ctrl+Shift+L, verify file created

---

### v2.3.0-entry-consolidation (Planned - December 2025)
**Status:** Architecture refactoring planned

**Planned Changes:**
- 🔄 **Entry point consolidation** - Migrate all logic from `interactive_editor.py` to `application.py`
- 🔄 **Observability framework** - Add lightweight observer pattern for full operation visibility
- 🔄 **Single code path** - Eliminate dual implementations of insertion/deletion/modification
- 🔄 **Enhanced debugging** - Complete visibility: widget → application → controller → model

**Goals:**
- Reduce maintenance burden (one implementation instead of two)
- Improve debugging time (30 minutes → 5 minutes with observability)
- Prevent class of bugs seen in v2.2.1 (undo bypassed in legacy path)
- Enable future enhancements without code duplication

**See:** [Entry Point Consolidation Plan](architecture/entry_point_consolidation_plan.md)

**Timeline:** 4 weeks (1 week observer, 2 weeks migration, 1 week enhanced features)

### v2.2.2-save-both-perspectives (December 14, 2025) ← CURRENT
**Status:** Feature addition - Save Both Perspectives

**New Feature:**
- ✅ **Save Both M1 & M2** - Single toolbar action saves both perspectives to separate files
- ✅ **Keyboard shortcut** - Ctrl+Shift+S saves both M1_modified.csv and M2_modified.csv
- ✅ **Workflow optimization** - Eliminates need to switch perspectives just to save
- ✅ **Session preservation** - Captures all dual-perspective edits from one session

**Implementation:**
- Added `save_both_action` to main_window.py toolbar with Ctrl+Shift+S shortcut
- Added `_handle_save_both_request()` to interactive_editor.py
- Added `save_both_perspectives()` method to controller.py
- Uses existing `model.save_csv()` called twice (once for M1, once for M2)

**User Experience:**
- Toolbar button: "Save Both M1 & M2"
- Status bar confirms: "Saved M1: {file}_M1_modified.csv, M2: {file}_M2_modified.csv"
- Error handling: Shows error dialog if either save fails

**Use Cases:**
- Scenario development: Building canonical scenarios with coordinated M1/M2 edits
- Iteration workflow: Testing different relational patterns across both perspectives
- Session snapshots: Capturing complete state before experimental changes
- Pre-testing baseline: Saving both perspectives before manual testing week

**Quality Standard:**
- **Modeled:** Extends existing save architecture, clean separation of concerns
- **Verifiable:** Clear terminal output, status bar feedback, file creation observable
- **Testable:** Manual test checklist in INTERACTIVE_EDITOR_TESTING.md Tier 3

**Documentation:**
- User guide: [interactive_editor_user_guide.md](interactive_editor_user_guide.md#save-both-perspectives-planned)
- Testing: [INTERACTIVE_EDITOR_TESTING.md](INTERACTIVE_EDITOR_TESTING.md) Tier 3

### v2.2.1-insertion-undo-fix (December 13, 2025)
**Status:** Bug fix - Event Insertion Point undo tracking

**Bug Fixed:**
- ✅ **Insertion undo tracking** - Event Insertion Point widget insertions now create proper undo commands
- ✅ **Command pattern consistency** - Fixed `interactive_editor.py` to use `InsertEventCommand` instead of direct controller calls

**Root Cause:**
- `interactive_editor._on_insertions_changed()` was calling `controller.insert_event_at_time_no_update()` directly
- Bypassed undo command system entirely
- Meanwhile, `application.py` correctly used `InsertEventCommand`
- Result: insertions from Event Insertion Point widget couldn't be undone with Ctrl+Z

**Fix:**
- Updated `interactive_editor.py` lines 733-758 to use `InsertEventCommand` and push to undo stack
- Updated deletion logic lines 714-732 to use `DeleteEventCommand`
- Removed redundant view updates (commands already update views)

**Impact:**
- All event insertions now properly tracked in undo stack
- Ctrl+Z correctly removes inserted events
- Revealed architectural issue: dual entry points with different implementations
- Led to v2.3.0 consolidation plan

### v2.2.0-marker-centric (December 13, 2025)
**Status:** Marker-centric state architecture

**See:** v2.2.0 entry in ARCHITECTURE.md for complete details

### v2.1.2-baseline-refactor (December 11, 2025)
**Status:** Baseline storage architecture refactored

**Architecture Improvements:**
- ✅ **Migrated to time-keyed baseline storage** - Replaced fragile index-based arrays with stable time-keyed dictionary
- ✅ **Removed index synchronization** - No longer need to update baseline arrays after insert/delete operations
- ✅ **Eliminated corruption risk** - Baseline storage completely independent of model, cannot accidentally fetch modified values
- ✅ **Simplified code** - Removed complex array manipulation logic (5 dict operations vs 12 array operations per insert/delete)

**Technical Details:**
- Changed from: `baseline_primitives['r'][6]` (index-based, shifts on insert)
- Changed to: `baseline_by_time[(42.0, 'r')]` (time-keyed, insertion-proof)
- Removed `original_baseline_primitives` shadow copy (no longer needed)
- Updated all baseline lookups in: `_apply_primitive_change`, `_reset_primitive`, insert/delete handlers
- Handles time-shifting operations (Ctrl+Shift+Click) by deleting old keys and adding new keys

**Benefits:**
- Cannot become invalid when events inserted/deleted
- Clearer semantics: "Baseline at time 42" vs "Baseline at index 6"
- Prevents entire class of index-related bugs
- Foundation for future event management features (Phase 2.2+)

**Testing:**
- All existing undo/redo tests pass
- Label appearance/removal works correctly
- Insert/delete operations maintain baseline correctly
- Time-shifting insertions (Ctrl+Shift+Click) preserve baseline values

---

### v2.1.1-undo-fixes (December 11, 2025)
**Status:** Critical bug fixes for undo system

**Bug Fixes:**
- ✅ **Fixed undo system bypass** - Insertion options widget (text field) now creates proper `InsertEventCommand` instead of bypassing undo stack
- ✅ **Fixed command index instability** - EditPrimitiveCommand and ResetPrimitiveCommand now store event **time** instead of **index**, preventing corruption when insertions/deletions shift indices
- ✅ **Fixed baseline corruption** - `_update_baseline_after_insert/delete` now insert/delete from existing baseline arrays instead of re-fetching from modified model
- ✅ **Fixed label cleanup** - Modified marker labels now properly removed when values return to baseline during undo

**Root Cause Analysis:**
Three interconnected issues:
1. **Insertion bypass**: Text field insertions didn't create undo commands, breaking undo chain
2. **Index fragility**: Commands storing array indices became invalid after insertions shifted all subsequent indices
3. **Baseline pollution**: Re-fetching baseline from model after insertion captured modified values as "baseline"

**Technical Details:**
- Created `InsertEventCommand` for simple insertion (no time shifting)
- Commands now store `event_time` and dynamically look up current index during undo/redo
- Baseline arrays maintained as immutable snapshots, updated via np.insert/np.delete operations
- Label removal integrated into `_apply_primitive_change()` for consistent cleanup

**Architectural Issue Identified:**
Index-based baseline storage (`baseline_primitives['r'][6]`) is fragile and error-prone. See "Planned Refactoring" section below.

---

### v2.1-diagnostic-markers (December 7, 2025)
**Status:** Checkpoint during Phase 2 development

**New Features:**
- ✅ **Diagnostic "What-If" Markers** - Shift+click to place hypothetical test markers
  - Black X marker on primitive plots shows test value
  - Black X marker on gamma_self trajectory shows final outcome with hypothetical value
  - Draggable X markers for real-time exploration of different hypothetical values
  - Both readout gauges update to show hypothetical primitive and gamma_self values
  - Markers clear automatically when placing new diagnostic marker
  - **Non-destructive** - diagnostic markers don't modify actual data
- ✅ Coordinate system fix - PyQtGraph scene signal handling for accurate click positioning

**Technical Details:**
- Uses `QGraphicsScene.sigMouseClicked` for proper coordinate mapping
- `event.scenePos()` + `mapSceneToView()` for accurate data coordinate conversion
- Computes full hypothetical trajectory with modified primitive value
- Shows **final** gamma_self position (end of trajectory), not intermediate state

**Use Cases:**
- "What if resonance had been +7 instead of +2 at day 14?"
- "How much would increasing altruism at day 21 improve the outcome?"
- Quick exploration before committing to actual edits

**Known Issues:**
- None currently

**Next Steps:**
- Phase 2.2: Add/delete events, edit gamma_self_0, fractional time support

---

### v2.0-undo-redo (December 6, 2025)
**Status:** Checkpoint during Phase 2 development

**Completed Features:**
- ✅ PySide6 migration complete (replaced Matplotlib/Tkinter)
- ✅ Full undo/redo system with QUndoStack
- ✅ Discrete undo steps (each edit is separate)
- ✅ Marker position synchronization on gamma_self graph
- ✅ Label management (appear when modified, disappear when back to baseline)
- ✅ Thread-safe incremental updates
- ✅ Keyboard shortcuts (Ctrl+Z, Ctrl+Y)
- ✅ Command pattern delegation (prevents recursive undo creation)

**Known Issues:**
- None currently

**Next Steps:**
- Phase 2.2: Add/delete events, edit gamma_self_0, fractional time support

---

### v1.0-phase1 (December 5, 2025)
**Status:** Phase 1 Complete

**Features:**
- ✅ Single-perspective (M1) primitive editing with drag-and-drop
- ✅ Real-time gamma_self trajectory preview with debounced computation
- ✅ Lock/unlock event functionality (right-click toggle)
- ✅ Auto-marking of modified points (hollow vs filled markers)
- ✅ Primitive readout gauge (marker ID + Y-value display)
- ✅ Gamma_self position readout (X,Y coordinates on hover)
- ✅ Dual save functionality (Click=CSV, Shift=PNG, Ctrl=Both)
- ✅ CSV format with marker/locked columns for persistence
- ✅ Centralized LAYOUT system for maintainable UI
- ✅ Keyboard shortcuts (0=reset, +/-=zoom, F=fixed view, G=edit gamma_self_0)
- ✅ Primitives module (single source of truth for metadata)
- ✅ Configuration system (user-customizable via JSON)

**Architecture:**
- Matplotlib-based visualization
- MVC pattern: EditorModel, EditorController, PrimitivePanel, TrajectoryPanel
- Backward-compatible CSV format

---

## Completed Refactoring

### Baseline Storage Architecture ✅ COMPLETE

**Status:** Migrated from index-based arrays to time-keyed dictionary (v2.1.2)

See [architecture/baseline_storage_refactoring.md](architecture/baseline_storage_refactoring.md) for detailed documentation.

---

## Planned Future Versions

### v2.2-event-management (Planned)
**Phase 2.2 Features:**
- Add/delete time points (Shift+Click to insert, Delete key to remove)
- Edit gamma_self_0 initial state
- Fractional time support (e.g., 2.5 days)
- Event insertion/deletion undo support

### v2.3-inverse-editing (Planned)
**Phase 2.3 Features:**
- Drag gamma_self trajectory to suggest primitive changes
- Heuristic inverse estimation
- Accept/reject dialog for suggestions

### v2.4-spinbox-primitive-editor (Planned)
**Status:** Specification complete - Ready for implementation

**Feature: Spinbox Primitive Editor**
- ➕ **Single shared spinbox** - Replaces gauge-based primitive editing with precise numeric input
- ➕ **Active primitive tracking** - Spinbox shows currently selected primitive (v, r, f, a, S)
- ➕ **Persistent labeling** - "Editing: {primitive}" label follows same architecture as gamma_self plot labels
- ➕ **Workflow**: Click event → click primitive → type exact value → Enter to commit
- ➕ **Full integration** - Works with Event Insertion Points, Ctrl+Shift+Click markers, M1/M2 switching
- ➕ **State Viewer logging** - All primitive value changes logged with event ID, primitive name, old/new values
- ➕ **Gauge removal** - Eliminates imprecise drag-based editing, cleaner UI

**Purpose:**
- Enable precise primitive value entry (-10.0 to +10.0)
- Reduce editing friction (type "7.2" instead of dragging to approximate value)
- Cleaner UI (one spinbox instead of 5 gauges or complex drag interfaces)
- Better accessibility (keyboard-driven workflow)

**Design Decisions:**
- Single spinbox (not 5 separate) - shows active primitive value
- Label architecture matches gamma_self plot pattern for consistency
- Primitive selection by clicking primitive label/marker
- Event selection by clicking event marker (existing mechanism)
- Spinbox disabled until event + primitive selected

**Implementation Phases:**
1. Create spinbox widget with label management
2. Wire primitive selection tracking (active primitive state)
3. Connect value commit to model updates
4. Integrate with Event Insertion Points
5. Handle M1/M2 perspective switching
6. Add State Viewer logging
7. Remove gauge code
8. Testing across all event types

**Open Design Questions:**
1. Keep read-only primitive value labels or remove entirely?
2. How to replace gauge double-click reset functionality? (Reset button? Ctrl+double-click? Right-click menu?)
3. Visual feedback for active primitive (bold label? color highlight? background?)
4. Spinbox placement (above primitives? below? inline?)

**Success Criteria:**
- ✅ User can type exact primitive values
- ✅ Clear indication of which primitive is active
- ✅ Works with all event types (normal, insertion, modified)
- ✅ Works across M1/M2 perspective switches
- ✅ State Viewer logs all changes
- ✅ Label architecture matches existing pattern
- ✅ No regression in functionality
- ✅ UI cleaner and more intuitive

**See:** [interactive_editor_user_guide.md - Spinbox Primitive Editing](interactive_editor_user_guide.md#spinbox-primitive-editing-planned)

---

### v2.5-marker-management (Planned)
**Phase 2.5 Features:**
- Manual marker add/remove (without editing values)
- Marker palette/picker
- Enhanced marker styling options

### v3.0-dual-file (Planned)
**Phase 3 Features:**
- Dual-file comparison mode
- Load second file for side-by-side comparison
- Toggle active/reference files
- Combined trajectory visualization
- Compatibility validation (same timeline, same gamma_self_0)
- Save/Save All operations

---

## Release Notes Template

When creating a new tag:

```bash
# Tag current state
git tag -a v2.X-feature-name -m "Brief description of milestone"

# Push tag to remote
git push origin v2.X-feature-name

# Update this file with:
# - Version number and date
# - Completed features (✅)
# - Known issues
# - Next steps
```
