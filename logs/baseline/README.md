# Baseline Protocol Log Files

This directory contains debug logs from the Baseline Communication Protocol.

## What are these logs?

These logs track communication between two coordinate spaces in the interactive editor:
- **Primitive Space**: Time-indexed (insertion-proof)
- **Gamma_self Space**: Index-based (requires reindexing after insertions)

## When to use?

Enable protocol logging when debugging:
- Markers/labels not disappearing when returning to baseline
- Baseline indicators showing incorrect values after insertions
- Undo/redo operations affecting wrong events
- Synchronization issues between primitive and gamma_self plots

## How to enable/disable?

```python
# Enable logging
controller.enable_baseline_protocol_logging()

# Perform operations (insert, edit, undo, etc.)

# Dump to console
controller.dump_baseline_protocol_log()

# Dump to auto-generated timestamped JSON (default, for analysis)
controller.dump_baseline_protocol_log("auto")

# Dump to custom JSON file
controller.dump_baseline_protocol_log("logs/baseline/my_debug.json")

# Dump to custom text file (human-readable)
controller.dump_baseline_protocol_log("logs/baseline/my_debug.log")

# Disable logging
controller.disable_baseline_protocol_logging()
```

## Log file formats

### JSON Format (default)

Structured data file with:
```json
{
  "metadata": {
    "generated": "2025-12-13T14:23:45.123456",
    "total_entries": 42,
    "format_version": "1.0"
  },
  "entries": [
    {
      "timestamp": "14:23:45.123",
      "event": "primitive_insert_shift",
      "perspective": "M1",
      "insert_time": 2.5,
      "shifts_count": 3
    },
    ...
  ]
}
```

### Text Format (optional)

Human-readable text file with:

### Header Section
- What the log tracks
- Why it exists
- Who calls it
- How to enable/disable
- Event types documentation
- How to read the log

### Log Entries Section
```
[HH:MM:SS.mmm] [M1|M2] event_type | key=value | key=value | ...
```

Example:
```
[14:23:45.123] [M1] primitive_insert_shift | insert_time=2.5 | shifts_count=3
[14:23:45.145] [M1] baseline_sync_primitive | entries_count=6
[14:23:45.167] [M1] gamma_reindex | mappings_count=3 | mapping={3:4, 4:5, 5:6}
```

## Event types

| Event Type | Description |
|------------|-------------|
| `primitive_insert_shift` | Ctrl+Shift+Click insertion (shifts subsequent times) |
| `primitive_insert_fractional` | Fractional time insertion (no shift) |
| `gamma_reindex` | Gamma_self trajectory reindexed after insertion |
| `baseline_sync_primitive` | Primitive baseline synchronized to view |
| `baseline_sync_gamma` | Gamma_self baseline synchronized to view |
| `primitive_undo_insert` | Undo insertion operation |
| `primitive_edit` | User edited primitive value |
| `primitive_reset` | User reset to baseline |

## File naming

Auto-generated files use the format:
```
baseline_protocol_YYYYMMDD_HHMMSS.json  (default)
baseline_protocol_YYYYMMDD_HHMMSS.log   (if you specify .log/.txt extension)
```

Examples: 
- `baseline_protocol_20251213_142345.json`
- `baseline_protocol_20251213_142345.log`

## Retention

Log files are not automatically cleaned up. Delete old logs manually when no longer needed.

## See also

- [docs/baseline_communication_protocol.md](../../docs/baseline_communication_protocol.md) - Full architecture documentation
- [tools/editor/baseline_protocol.py](../../tools/editor/baseline_protocol.py) - Implementation
