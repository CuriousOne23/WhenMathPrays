# ObservabilityLog Usage Guide

## Overview
The ObservabilityLog system provides toggle-able structured logging for debugging complex event-driven interactions in the editor. When enabled, it outputs timestamped JSON events to help trace perspective switches, label operations, and model updates.

## Quick Start

### Enable Logging via Environment Variable
```bash
# Windows PowerShell
$env:EDITOR_DEBUG="true"
python main.py scenarios/library/single_dating_to_love_M1.csv

# Windows CMD
set EDITOR_DEBUG=true
python main.py scenarios/library/single_dating_to_love_M1.csv

# Linux/macOS
export EDITOR_DEBUG=true
python main.py scenarios/library/single_dating_to_love_M1.csv
```

### Enable Programmatically
```python
from tools.editor.observability import ObservabilityLog

# Enable at application startup
ObservabilityLog.initialize(enabled=True)

# Check if enabled
if ObservabilityLog.is_enabled():
    print(f"Logging to: {ObservabilityLog.get_log_file()}")
```

## Log Output Location
- **Path**: `tools/editor/logs/editor_debug_YYYYMMDD_HHMMSS.log`
- **Format**: Timestamped JSON events with human-readable sections
- **Rotation**: New file per editor session

## Core API

### Log an Event
```python
ObservabilityLog.event("event_type", **kwargs)
```
Outputs: `{"event": "event_type", "key1": value1, "key2": value2}`

### Log a Section Separator
```python
ObservabilityLog.section("=== PERSPECTIVE SWITCH ===")
```
Outputs a visual separator for readability in log files.

### Check Status
```python
ObservabilityLog.is_enabled()  # Returns True/False
ObservabilityLog.get_log_file()  # Returns path or None
```

## Instrumented Operations

### Perspective Switching
```json
{"event": "perspective_switch_start", "old_perspective": "M1", "new_perspective": "M2", "m1_labels": 3, "m2_labels": 1}
{"event": "recreating_labels", "perspective": "M2", "count": 1, "labels": [[42.0, "Volatility", 0.8]]}
{"event": "perspective_switch_complete", "old_perspective": "M1", "new_perspective": "M2", "m1_labels_final": 3, "m2_labels_final": 1}
```

### Label Operations
```json
{"event": "add_marker_label", "event_time": 42.0, "primitive": "Volatility", "value": 0.8, "perspective": "M2", "m1_label_count": 3, "m2_label_count": 0}
{"event": "removed_old_label", "key": [42.0, "Volatility"], "perspective": "M2"}
```

### Model Updates
```json
{"event": "primitive_panel_update_start", "perspective": "M1", "event_count": 50, "m1_label_count": 3, "m2_label_count": 0}
```

## Performance
- **Zero overhead when disabled**: No file I/O, minimal CPU usage
- **Minimal overhead when enabled**: Buffered writes, async-friendly
- **Production safe**: Can be left in code, toggle via environment variable

## Debugging Workflow

### 1. Enable Logging
```bash
$env:EDITOR_DEBUG="true"
```

### 2. Reproduce the Issue
1. Launch editor
2. Perform the operation that exhibits the bug (e.g., drag marker, switch perspective)
3. Close editor

### 3. Analyze the Log
```bash
# View the log file
cat tools/editor/logs/editor_debug_*.log | Select-String "perspective_switch"

# Search for specific events
cat tools/editor/logs/editor_debug_*.log | Select-String "add_marker_label" | Select-String "42.0"
```

### 4. Key Questions to Answer
- **When are labels created?** Look for `add_marker_label` events
- **What triggers label creation?** Check the sequence of events before `add_marker_label`
- **Which perspective is active?** Every event includes `perspective` field
- **Are labels being destroyed?** Look for `removed_old_label` events
- **What's the state before/after perspective switch?** Compare `m1_label_count` and `m2_label_count`

## Example: Debugging Label Persistence Bug

### Symptom
Label "42.0" appears in M2's Volatility plot even though M2 never modified day 42.

### Investigation Steps
1. Enable logging: `$env:EDITOR_DEBUG="true"`
2. Run editor, drag M1 marker at day 42
3. Switch to M2 perspective
4. Search log for: `"event_time": 42.0`

### Expected Log Pattern
```json
# Step 1: User drags marker in M1
{"event": "add_marker_label", "event_time": 42.0, "primitive": "Volatility", "value": 0.8, "perspective": "M1"}

# Step 2: User switches to M2
{"event": "perspective_switch_start", "old_perspective": "M1", "new_perspective": "M2", "m1_labels": 1, "m2_labels": 0}
{"event": "recreating_labels", "perspective": "M2", "count": 0, "labels": []}
{"event": "perspective_switch_complete", "m1_labels_final": 1, "m2_labels_final": 0}

# BUG: If we see this, something called add_marker_label in M2 context
{"event": "add_marker_label", "event_time": 42.0, "primitive": "Volatility", "value": 0.8, "perspective": "M2"}
```

The extra `add_marker_label` event reveals the hidden code path creating the label.

## Third-Party Extensibility

Custom panels can use ObservabilityLog for debugging:

```python
from tools.editor.observability import ObservabilityLog

class CustomPanel:
    def custom_operation(self, data):
        ObservabilityLog.event("custom_panel_operation",
                               panel_id=self.id,
                               data_size=len(data),
                               custom_field=self.state)
        # ... perform operation ...
```

## Disabling Logging
```bash
# Windows PowerShell
$env:EDITOR_DEBUG="false"

# Or unset the variable
Remove-Item Env:EDITOR_DEBUG
```

## Best Practices
1. **Use descriptive event names**: `perspective_switch_start` not `switch1`
2. **Include context**: Always log perspective, counts, relevant IDs
3. **Log state transitions**: Before/after snapshots for comparisons
4. **Use sections for readability**: Group related operations
5. **Don't log in hot loops**: Only log significant events (marker drags, not mouse moves)

## Troubleshooting

### "Log file not created"
- Check `EDITOR_DEBUG` environment variable is set to `"true"` or `"1"`
- Verify `tools/editor/logs/` directory permissions
- Call `ObservabilityLog.initialize(enabled=True)` explicitly

### "Too much output"
- Log only significant events (perspective switches, label operations)
- Avoid logging in `mouseMoveEvent` or similar high-frequency callbacks
- Use `ObservabilityLog.is_enabled()` guard for expensive computations

### "Can't find the event I'm looking for"
- Instrument more code paths with `ObservabilityLog.event()`
- Use `ObservabilityLog.section()` to mark logical boundaries
- Search for related events (e.g., if missing `add_label`, search for `update_from_model`)
