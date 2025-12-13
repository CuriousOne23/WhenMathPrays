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

The editor has built-in debug logging facilities:

### Console Output Tags

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
3. **Remove after fix**: Clean up verbose logging once bugs are resolved
4. **Tagged output**: All debug messages prefixed with tags for easy filtering

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
