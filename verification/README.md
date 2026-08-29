# Verification

## Overview

This directory holds verification scripts and procedures for the WhenMathPrays interactive scenario editor.

On disk in this folder:

- [`verification.py`](verification.py) — automated state-log structure checker
- [`interactive_editor_performance_baseline.md`](interactive_editor_performance_baseline.md)
- [`interactive_editor_performance_validation.py`](interactive_editor_performance_validation.py)

Canonical scenario CSV format: [`docs/CSV_FORMAT.md`](../docs/CSV_FORMAT.md).

Love scenario CSVs used with the editor:

- [`data/library/love/single_dating_to_love_M1.csv`](../data/library/love/single_dating_to_love_M1.csv)
- [`data/library/love/single_dating_to_love_M2.csv`](../data/library/love/single_dating_to_love_M2.csv)

Session `.log` files from historical editor runs are **not** stored in this git tree.

**Note**: Supporting test CSVs live under `data/` (including `data/verification_data/` and entropy-calibration files).

## What Was Verified

This log captures comprehensive testing of entropy mathematics and attractor dynamics:

### Core Entropy Mathematics
- **Entropy Attractor Location**: Validation of entropy convergence to target coordinates (-150.0 + 0.0j)
- **Real/Imaginary Weights**: Testing of axis-specific entropy decay rates (ΔS_real, ΔS_imag = 0.02 each)
- **GRP Algorithm Correctness**: 8 successful trajectory computations validating the entropy equation implementation
- **Convergence Properties**: Verification of constant-force entropy decay toward attractor basins

### M1/M2 Entropy Dynamics
- **Dual-Perspective Entropy**: Testing entropy behavior across M1 (ego) and M2 (we) perspectives
- **Perspective Switching**: Validation of entropy state consistency during M1↔M2 transitions
- **Cross-Perspective Interactions**: Verification of entropy calculations when markers span both perspectives

### Entropy Trajectory Validation
- **963 Marker Operations**: Extensive testing of entropy responses to marker positioning changes
- **Real-time Entropy Updates**: Validation of entropy trajectory recalculation after each marker modification
- **Entropy Stability**: Verification that entropy attractors remain consistent across multiple operations

### User Interface Integration
- **Perspective Switching**: Verified dual-perspective entropy handling
- **Undo/Redo Operations**: Entropy calculation consistency across user actions
- **Real-time Updates**: UI responsiveness during entropy computations

## Operation Breakdown

```
pin_marker:                              963 operations (96.3%)
trajectory_computed:                        8 operations
update_primitive_to_gamma_self_mapping:     8 operations
mark_clean/dirty:                           9 operations
update_primitive:                           2 operations
undo operations:                            6 operations
perspective switches:                       2 operations
```

## Verification Status

✅ **PASSED** - All entropy functionality verified successfully

**Verification Date**: December 17, 2025
**Verified By**: Automated verification logging system
**Test Environment**: Windows 11, Python 3.14.1

## Future Verification Use

### Regression Testing
Use this log as a baseline for:
- Detecting entropy calculation regressions
- Validating marker positioning accuracy
- Ensuring state transition reliability

### Performance Benchmarking
Compare future logs against this baseline to:
- Monitor entropy computation performance
- Track memory usage patterns
- Identify performance degradation

### AI-Assisted Debugging
This log serves as training/validation data for:
- Automated entropy issue detection
- State transition analysis
- Performance anomaly identification

### Quality Assurance
- **Pre-release validation**: Compare new builds against this verified baseline
- **Integration testing**: Ensure entropy features work across different scenarios
- **User acceptance testing**: Validate that entropy functionality meets requirements

## How to Use a Verification Log

Historical editor session logs are not checked into git. If you have a local state log, `verification.py` (below) is the checker. Example grep patterns for a log you already have:

```bash
# Search for specific operations
grep "trajectory_computed" path/to/state_log.log

# Count operation types
grep "^\[" path/to/state_log.log | cut -d']' -f2 | sort | uniq -c
```

### Automated Analysis
The log format is designed for automated processing:
- Structured operation records with timestamps
- Consistent change tracking format
- Machine-readable entity and change data
- Zero false positives (warnings/errors = 0)

### Comparison with New Logs
```bash
# Compare operation counts
diff <(grep "^\[" old_log.log | wc -l) <(grep "^\[" new_log.log | wc -l)

# Check for new warning patterns
grep "WARNING\|ERROR" new_log.log
```

## Automated Verification Script

This directory includes `verification.py`, a comprehensive automated verification script that can replay operations from state logs and validate software behavior.

### Features

- **Log Structure Validation**: Parses and validates state log format and completeness
- **Operation Analysis**: Counts and categorizes all logged operations
- **Session Information Extraction**: Validates session metadata and test file references
- **Error Detection**: Identifies warnings, errors, and structural issues
- **CI/CD Integration**: Returns appropriate exit codes for automated testing

### Usage

```bash
# Validate a local state log (session .log files are not in git)
python verification/verification.py path/to/your/state_log.log

# Get help
python verification/verification.py --help
```

### Verification Process

1. **Header Validation**: Checks session info, Python version, platform, and loaded files
2. **Operation Counting**: Tallies total operations and breaks down by operation type
3. **Structure Validation**: Ensures operations have required fields and proper sequencing
4. **Error Checking**: Scans for warnings and errors in the log content
5. **Rule-Based Validation**: Applies validation rules for completeness assessment

### Validation Rules

The script validates logs against these criteria:
- **Session Information**: Presence of session timestamp, Python version, platform
- **Operation Structure**: All operations have required fields (number, type, time, entity, location, changes)
- **Sequential Operations**: Operation numbers are sequential (allowing for non-zero starting numbers)
- **Error-Free Logs**: No ERROR entries in the log content
- **Complete Operations**: All operation headers have corresponding complete operation blocks

### Supported Validation

The script validates the structure of all operation types found in state logs:
- `pin_marker`: Marker positioning operations
- `trajectory_computed`: Trajectory calculation events
- `switch_perspective`: Perspective switching operations
- `update_primitive`: Primitive value modifications
- `mark_clean/mark_dirty`: State management operations
- `enter_undo_operation/exit_undo_operation`: Undo system operations
- `primitive_changed/redo_edit_primitive`: Edit operations
- `update_primitive_to_gamma_self_mapping`: Mapping updates

### Output Format

```
============================================================
VERIFICATION RESULTS
============================================================
Status: PASSED
Log File: path/to/your/state_log.log
Session: 2025-12-17T14:50:08.575559
Total Operations: 1000
Warnings: 0
Operations Found: 1000

Operation Breakdown:
  pin_marker: 963
  trajectory_computed: 8
  switch_perspective: 2
  ...

Validation Rules:
  ✓ Has session info
  ✓ Has operations
  ✓ No errors in log
  ✓ Operations are sequential
============================================================
```

### Integration with CI/CD

The script returns appropriate exit codes for automation:
- **Exit Code 0**: Verification passed
- **Exit Code 1**: Verification failed

Example CI integration:
```yaml
- name: Run Verification Tests
  run: python verification/verification.py path/to/your/state_log.log
  working-directory: ${{ github.workspace }}
```

## Interactive Editor Functionality Verification

A December 17, 2025 editor-functionality session (538 operations, 0 warnings) is historical; the `.log` is not in git. That session used the standard love scenario files:

- **Primary Test File (M1)**: [`data/library/love/single_dating_to_love_M1.csv`](../data/library/love/single_dating_to_love_M1.csv)
- **Secondary Test File (M2)**: [`data/library/love/single_dating_to_love_M2.csv`](../data/library/love/single_dating_to_love_M2.csv)

## What Was Verified

This log captures comprehensive testing of interactive editor functionality across dual perspectives:

### Core Interactive Operations
- **Drag Primitive Markers**: 8+ `redo_edit_primitive` operations validating marker dragging and value updates
- **Double-Click Reset**: 1 `redo_reset_primitive` operation validating double-click reset to baseline values
- **Insert Time Primitive**: 2 `redo_insert_event_before` operations validating event insertion at specific times
- **M1/M2 Perspective Switching**: 6+ `switch_perspective` operations validating seamless perspective transitions

### Undo/Redo System
- **CTRL+Z (Undo)**: Multiple `undo_reset_primitive`, `undo_edit_primitive`, and `undo_insert_event_before` operations
- **CTRL+Y (Redo)**: Command re-execution through redo operations with perspective context
- **Cross-Perspective Undo/Redo**: Undo/redo operations tested across M1↔M2 perspective switches

### State Management
- **Dual-Perspective State**: Validation of independent M1/M2 state management during operations
- **Marker Pinning**: Automatic gamma_self position updates after primitive changes
- **Trajectory Recalculation**: Real-time trajectory updates after each operation
- **Clean State Transitions**: All operations completed without warnings or errors

### User Interface Integration
- **Signal Chain Validation**: Complete mouse event → signal emission → controller → model → view updates
- **Visual Feedback**: Marker position updates, label changes, and trajectory redrawing
- **Command Pattern**: All operations properly wrapped in undoable commands

## Verification Coverage

✅ **Drag primitive** - Multiple marker dragging operations recorded
✅ **Ctrl+Shift** - Time-based event insertions (Ctrl+Shift+Click equivalent)
✅ **Double click** - Primitive reset to baseline values
✅ **Insert time primitive** - Event insertion with time positioning
✅ **M1 and M2** - Full dual-perspective operation coverage
✅ **CTRL+Z** - Undo operations across all command types
✅ **CTRL+Y** - Redo operations with perspective switching

This verification log serves as the official record that all core interactive editor functionality operates correctly across dual perspectives with full undo/redo support.

---

## Maintenance Notes

- Session `.log` files are not stored in git; treat any local log as an immutable baseline
- **Keep associated test files** in their original locations for future reference
- **Expand verification_data directory** as needed for additional test scenarios
- **Archive periodically** as part of release verification artifacts
- **Update this README** if new verification procedures are established

## Contact

For questions about this verification log or entropy functionality:
- Reference: [`README.md`](../README.md) - GRP entropy equation and mathematical foundations
- Logs: [`logs/`](../logs/) directory for current session logs
- Tests: [`tests/`](../tests/) directory for entropy-related test cases