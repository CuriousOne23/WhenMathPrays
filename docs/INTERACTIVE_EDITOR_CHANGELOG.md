# Interactive Editor - Version History

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

### v2.1-diagnostic-markers (December 7, 2025) ← CURRENT STABLE
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
