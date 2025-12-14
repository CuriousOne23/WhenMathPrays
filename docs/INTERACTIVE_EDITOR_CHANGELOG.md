# Interactive Editor - Version History

## Related Documentation

- **[Interactive Editor Testing](INTERACTIVE_EDITOR_TESTING.md)** - Testing strategy and quality assurance
- **[Architecture](../ARCHITECTURE.md)** - Overall system architecture
- **[State Management Refactoring](STATE_MANAGEMENT_REFACTORING.md)** - Phase 3.4 centralized state
- **[Debugging Methodology](DEBUG.md)** - Systematic debugging approaches

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

### v2.2.1-insertion-undo-fix (December 13, 2025) ← CURRENT
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

### v2.4-marker-management (Planned)
**Phase 2.4 Features:**
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
