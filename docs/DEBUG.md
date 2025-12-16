# Debugging Methodology for Interactive Editor

This document outlines systematic debugging approaches for the interactive editor, particularly for complex UI/state synchronization issues.

## Complete Debugging Methodology Inventory

### 1. Direct Bug Squashing
**What**: Try solutions directly, iterate until something works.

**When to use**: 
- Simple, well-understood problems
- Time-constrained situations
- When you have a strong hypothesis

**Limitations**: Can miss root causes, create technical debt

---

### 2. Control Testing
**What**: Verify what we can and cannot control in the framework/libraries.

**When to use**:
- Working with external libraries (PyQtGraph, Qt)
- Unexpected behavior from framework components
- Need to understand API limitations

**Example**: Testing if PyQtGraph's `removeItem()` actually removes items from rendering cache vs just from data structures.

---

### 3. Information Flow Tracking
**What**: Trace how data moves through the system using logging, breakpoints, or stack traces.

**When to use**:
- Multi-component interactions
- Understanding execution order
- Finding where state changes occur

**Tools**: 
- Debug print statements with timestamps
- Python debugger breakpoints
- Stack trace logging (`traceback.format_stack()`)

---

### 4. State Inspection
**What**: Snapshot complete system state at key moments and compare.

**When to use**:
- State corruption issues
- Data getting lost or appearing unexpectedly
- Understanding what's different between working/broken states

**How**:
```python
def dump_state(label):
    print(f"=== STATE DUMP: {label} ===")
    print(f"M1 labels: {len(panel.modified_labels_m1)}")
    print(f"M2 labels: {len(panel.modified_labels_m2)}")
    print(f"Plot items: {[(k, len(v.items)) for k, v in panel.plot_items.items()]}")
    print(f"Model modified_primitives: {model.modified_primitives}")
    print("===========================")
```

---

### 5. Bisection/Isolation
**What**: Systematically disable code sections to narrow down the problem location.

**When to use**:
- Unknown root cause
- Complex code paths
- Multiple suspects

**Process**:
1. Comment out half the suspected code
2. Test if bug persists
3. If yes, bug is in other half; if no, bug is in commented half
4. Repeat until you isolate the exact line

---

### 6. Assumption Validation
**What**: Explicitly test assumptions we're making about the system.

**When to use**: 
- Stuck on a problem for >30 minutes
- Behavior doesn't match expectations
- Before major refactoring

**Critical Questions**:
- Is the data structure actually empty when we think it is?
- Is this the same object or a different instance?
- Is the code path we think is executing actually being executed?
- Are we checking the right variable/attribute?

**Example**:
```python
# Don't assume, verify:
assert len(modified_labels_m2) == 0, f"Expected 0 labels, found {len(modified_labels_m2)}"
assert text_item.scene() is None, f"TextItem still has scene: {text_item.scene()}"
assert id(label1) != id(label2), "These are the same object!"
```

---

### 7. Minimal Reproduction
**What**: Create smallest possible standalone script that reproduces the bug.

**When to use**:
- Suspecting framework bug
- Need to report issue to library maintainers
- Want to understand framework behavior in isolation

**Benefits**:
- Eliminates application-specific complexity
- Can test framework behavior independently
- Often reveals misunderstandings of API

---

### 8. Framework Exploration
**What**: Read library source code, documentation, or known issues.

**When to use**:
- Unexpected framework behavior
- Undocumented edge cases
- Before filing bug report

**Resources**:
- PyQtGraph GitHub: https://github.com/pyqtgraph/pyqtgraph
- Qt documentation
- Stack Overflow for known issues

---

## Debugging Workflow Recommendation

When facing a complex bug:

1. **Start with Assumption Validation** (#6) - Question what you think you know
2. **Add Information Flow Tracking** (#3) - Understand execution order
3. **Do State Inspection** (#4) - Compare expected vs actual state
4. **Try Bisection** (#5) - Narrow down the problem location
5. **Consider Control Testing** (#2) - Verify framework behavior
6. **Create Minimal Reproduction** (#7) - If still stuck, isolate the issue
7. **Only then**: Direct Bug Squashing (#1) - Apply targeted fix

---

## Case Study: Marker Label Persistence Bug (Dec 2024)

**Problem**: Labels from M1 perspective appearing in M2 perspective despite removal attempts.

**What we tried** (Direct Bug Squashing):
- `removeItem()` - didn't work
- `setVisible(False)` - didn't work  
- `deleteLater()` - didn't work
- "Nuclear cleanup" removing all TextItems - didn't work

**What we should have done**:
1. **Assumption Validation**: Verify the label IS actually a leftover M1 label (user tested: it moves with M2 marker → NOT a leftover!)
2. **Information Flow**: Trace where labels are created (found: only in `_add_marker_label()`)
3. **State Inspection**: Check if TextItems persist in plot after removal (added debug for this)

**Key insight**: After 15+ removal attempts, user revealed the label moves with M2's marker, proving it's NOT a ghost - it's being actively created/attached, but our debug tracing doesn't catch it. This means there's a hidden code path.

**Next steps**: Instrument all `addItem()` calls to find the hidden creation path.

---

## Best Practices

1. **Log state changes** with timestamps and context
2. **Use assertions** to validate assumptions during development
3. **Add debug modes** that can be toggled without code changes
4. **Document what you tried** to avoid repeating failed approaches
5. **Question your assumptions** before adding more code
6. **Simplify before expanding** - remove debug code once understood

---

## Debug Infrastructure

### Centralized Debug Logging System (December 2024)

**Location**: `tools/editor/debug_config.py`

The editor now uses a centralized logging system based on Python's `logging` module, replacing scattered print statements with professional, configurable logging.

#### Architecture

**Master Controls**:
- `DEBUG_ENABLED` - Global on/off switch for all debug logging
- `DEBUG_TO_FILE` - Routes logs to timestamped files in `logs/debug_<timestamp>.log`
- `DEBUG_TO_TERMINAL` - Routes logs to terminal/console output


**Category Flags**: Enable/disable logging for specific subsystems:
- `DEBUG_SPINBOX` - Primitive spinbox editor (click, drag, value changes)
- `DEBUG_TRAJECTORY` - Trajectory computation and gamma_self calculations
- `DEBUG_LABELS` - Label synchronization and perspective switching (all label-related debug output except assignment block)
- `DEBUG_LABELS_ASSIGNMENT` - **Label assignment block only** (fine-grained):
    - Controls deep debug output for the label assignment logic in `trajectory_panel_pyqtgraph.py`.
    - When enabled, logs all mapping keys, label text, and assignment steps for pinned markers.
    - Use this to trace and debug the exact process of label placement and mapping, without enabling all label debug output.
    - See [ARCHITECTURE.md](../ARCHITECTURE.md#debug-flag-granularity-label-assignment) for architectural context and usage guidance.
- `DEBUG_GAMMA` - Gamma_self parameter calculations
- `DEBUG_STATE` - State save/restore operations
- `DEBUG_UNDO` - Undo/redo command execution
- `DEBUG_DRAG` - Drag operation tracking
- `DEBUG_BASELINE` - Baseline synchronization events
- `DEBUG_SYNC` - Cross-component synchronization

#### Usage Pattern

```python
# In each module that needs logging:
from tools.editor.debug_config import get_debug_logger, DEBUG_SPINBOX
_logger = get_debug_logger('SPINBOX')

# In code:
if DEBUG_SPINBOX:
    _logger.debug("marker clicked: index={index}, primitive={primitive}")
```

#### Benefits

1. **Centralized control**: Single file controls all debug logging flags
2. **File output**: Logs persist to timestamped files for post-mortem analysis
3. **Granular control**: Enable only specific categories without noise
4. **Professional formatting**: Timestamps, log levels, module names
5. **No console spam**: Logs route to files, keeping terminal clean
6. **Easy toggling**: Change one flag to enable/disable entire category

#### Migration Status (December 2024)

**Completed**:
- ✅ Spinbox-related logging fully migrated (interactive_editor.py, controller.py, primitive_panel_pyqtgraph.py)
- ✅ All primitive spinbox editor debug statements use logger

**Future Migrations**:
- Trajectory computation logging → DEBUG_TRAJECTORY
- Label sync logging → DEBUG_LABELS
- Gamma_self calculation logging → DEBUG_GAMMA
- State save/restore logging → DEBUG_STATE
- Undo/redo logging → DEBUG_UNDO
- Drag operations → DEBUG_DRAG
- Baseline tracking → DEBUG_BASELINE

### Legacy Console Output Tags

**Note**: These are being migrated to the centralized logging system above.

Debug messages use prefixed tags for filtering/searching:
- `[DEBUG]` - General debug information
- `[BASELINE]` - Baseline synchronization events
- `[BASELINE_CHECK]` - Baseline comparison logic
- `[APPLY_CHANGE]` - Primitive value changes
- `[UNDO]` - Undo/redo operations
- `[CONTROLLER]` - Controller state changes
- `[PYQTGRAPH]` - View update timing
- `[TRAJECTORY]` - Gamma_self trajectory computation
- `[PANEL_REMOVE]` - Label removal operations
- `[LABEL_ADD]` - Label addition with call stacks

### Section Markers

Major operations use delimited sections:
```
=== INSERT EVENT ===
... operation details ...
=== END INSERT ===
```

### Baseline Protocol Logging

The baseline communication protocol has dedicated logging (see [baseline_communication_protocol.md](baseline_communication_protocol.md)):
- Enable: `controller.enable_baseline_protocol_logging()`
- Disable: `controller.disable_baseline_protocol_logging()`
- Dump: `controller.dump_baseline_protocol_log("path/to/file.json")`

### Debug Principles

1. **Minimal noise**: Production code has minimal debug output (critical operations only)
2. **Targeted logging**: Add detailed logging temporarily when debugging specific issues
3. **Centralized control**: Use debug_config.py flags instead of scattered conditionals
4. **File-based logs**: Route to files for analysis without terminal clutter
5. **Tagged output**: All debug messages include category and context information

---

## Architecture Insights from Debugging

Complex bugs often reveal architectural issues:

- **The label persistence bug** revealed fragmented perspective switching across multiple components without centralized coordination
- **Proper fix**: Refactor to event-driven architecture with Qt signals/slots for perspective changes
- **The baseline cascade deletion bug** revealed time-based keys creating shift complexity
- **Proper fix**: Migrate to ID-based event identity for immutable tracking
- **Lesson**: Manual state synchronization across components is error-prone; use observer pattern and immutable identities

**See**: 
- [architecture/perspective_management_refactor.md](architecture/perspective_management_refactor.md) for perspective switching refactor
- [ARCHITECTURE.md](../ARCHITECTURE.md) Event Identity section for ID-based tracking design
---

## Future Considerations & Proposals

### Testing & Validation

While the primitive spinbox editor has been validated for:
- ✅ Click activation and auto-activation during drag
- ✅ Undo/redo (Ctrl+Z/Ctrl+Y) across M1/M2 perspectives
- ✅ Event insertion (Ctrl+Shift+Click) with spinbox active
- ✅ Event deletion with spinbox active (no crashes)

**Proposals for systematic testing**:
1. Create automated UI test suite for editor operations
2. Add regression tests for known bugs (label persistence, baseline cascade deletion)
3. Consider property-based testing for trajectory computation
4. Add performance benchmarks for large timelines (>100 events)

### Debug Logging Enhancements

**Immediate opportunities**:
1. **Verify file logging**: Test that logs actually appear in `logs/debug_<timestamp>.log` when `DEBUG_TO_FILE = True`
2. **Complete migration**: Migrate remaining print statements to centralized logger:
   - Trajectory computation → DEBUG_TRAJECTORY
   - Label synchronization → DEBUG_LABELS
   - Gamma_self calculations → DEBUG_GAMMA
   - State save/restore → DEBUG_STATE
   - Undo/redo operations → DEBUG_UNDO
   - Drag operations → DEBUG_DRAG
   - Baseline tracking → DEBUG_BASELINE

**Future architecture improvements**:
1. **Log rotation**: Implement max file size/age limits to prevent disk bloat
2. **Log levels**: Use INFO/WARNING/ERROR more strategically instead of only DEBUG
3. **Context managers**: Add context managers for operation logging:
   ```python
   with log_operation('PRIMITIVE_EDIT', event_id=5):
       # operation code
       # automatic logging of start/end/duration
   ```
4. **Structured logging**: Consider JSON-formatted logs for machine parsing
5. **Performance profiling**: Add timing decorators to identify slow operations
6. **Remote logging**: Optional log aggregation for distributed testing

### Documentation

**Proposals**:
1. Add debug_config.py usage examples to ARCHITECTURE.md
2. Create visual debugging guide with screenshots of:
   - Spinbox editor in action
   - Log file output examples
   - Common debug workflows
3. Document known gotchas and their solutions
4. Maintain changelog of debug infrastructure changes

### Tooling

---

## Debugging Primitive ↔ Gamma_Self Mapping (v2.2.3 Proposal)

### Motivation
Complex UI bugs often arise from hidden or implicit mapping between the primitive (time-based) domain and the gamma_self (event-based) domain. To ensure robust debugging and synchronization, the mapping must be explicit, visible, and debuggable.

### Debugging Principles
- **Explicit Mapping:** All correspondences between primitive events and gamma_self events must be recorded in a first-class mapping structure (e.g., a dictionary).
- **Bidirectional Traceability:** Debugging tools must allow tracing from primitive to gamma_self and vice versa.
- **State Viewer Integration:** The State Viewer log should export the mapping for inspection and AI-assisted analysis.
- **Logging:** All mapping changes (creation, update, removal) should be logged with context (who, what, why, when).

### Debugging Workflow
1. **Observe UI Issue:** Label or marker appears in the wrong position or perspective.
2. **Export State Viewer Log:** Use Ctrl+Shift+L to export the current mapping and state.
3. **Inspect Mapping:** Check the mapping structure in the log to verify correct correspondence between primitive and gamma_self domains.
4. **Trace Source:** Use mapping logs to identify where synchronization failed (e.g., missing, stale, or incorrect mapping entries).
5. **Round-Trip Check:** Given a primitive event, confirm its gamma_self representation (and vice versa) using the mapping.

### Example Mapping Log Entry
```python
primitive_to_gamma_self = {
    (event_id, 'v'): {'gamma_self_pos': 3+2j, 'label': 'Visibility', 'perspective': 'M1'},
    (event_id, 'r'): {'gamma_self_pos': 1+4j, 'label': 'Resonance', 'perspective': 'M2'},
    # ...
}
```

### Benefits
- Eliminates hidden/implicit mapping bugs
- Enables rapid diagnosis and AI-assisted debugging
- Supports future extensibility (new perspectives, primitives)

### See Also
- [ARCHITECTURE.md](../ARCHITECTURE.md#explicit-mapping-between-primitive-and-gamma_self-domains-v223-proposal)
- [STATE_MANAGEMENT_REFACTORING.md](STATE_MANAGEMENT_REFACTORING.md)

> **Note:** The user-facing manual now provides a brief summary and refers here for full details on the explicit primitive-to-gamma_self mapping, debugging workflows, and log inspection. This section is the canonical technical reference for developers and advanced users.

**Future development tools**:
1. **Log viewer**: GUI for browsing/filtering debug logs
2. **State diff tool**: Visual comparison of state dumps
3. **Replay mode**: Record user interactions, replay with different parameters
4. **Performance monitor**: Real-time visualization of operation timing
5. **Test scenario generator**: Record user interactions as automated tests