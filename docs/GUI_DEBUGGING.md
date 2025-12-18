# GUI Event Debugging Infrastructure

This document describes the enhanced GUI event debugging infrastructure for the WhenMathPrays Interactive Editor. This infrastructure makes GUI event debugging tractable by providing comprehensive event tracking, signal monitoring, and widget inspection capabilities.

## Overview

The GUI debugging infrastructure addresses the core challenges of Qt/PyQtGraph event debugging:

- **Event Correlation**: Track events from mouse clicks through signal emissions to slot executions
- **Signal Monitoring**: Monitor Qt signal emissions with automatic logging
- **Widget Inspection**: Comprehensive widget state inspection for debugging
- **Unified Logging**: All debug output goes through the same logging system

## Quick Start

### Enable Debugging

```bash
# Enable comprehensive GUI debugging
python tools/interactive_editor.py data/library/love/single_dating_to_love_M1.csv --debug-gui

# Enable specific debugging features
python tools/interactive_editor.py data/library/love/single_dating_to_love_M1.csv --debug-signals --debug-mouse

# Enable terminal logging
python tools/interactive_editor.py data/library/love/single_dating_to_love_M1.csv --log-terminal
```

### Environment Variables

```bash
# Set debug level
export LOG_LEVEL=DEBUG

# Enable terminal logging
export LOG_TO_TERMINAL=true
```

## Features

### 1. Event Correlation Tracking

Track complete event chains with unique correlation IDs:

```python
from tools.editor.debug_gui import event_correlation_context

with event_correlation_context('double_click_reset', 'DoubleClickPlotItem', prim='v', idx=5):
    # Process the event
    process_reset(5, 'v')
```

This creates a complete audit trail:
```
[EVENT_START] a1b2c3 double_click_reset from DoubleClickPlotItem
[EVENT_STEP] a1b2c3 signal_emit in DoubleClickPlotItem
[EVENT_STEP] a1b2c3 controller_call in Controller
[EVENT_END] a1b2c3 success in 0.045s
```

### 2. Signal Emission Tracking

Automatically track Qt signal emissions:

```python
from tools.editor.debug_gui import get_gui_debugger

debugger = get_gui_debugger()
debugger.event_tracker.track_signal(widget.primitive_reset_requested, "reset_signal")
```

Now all emissions are logged:
```
[SIGNAL_EMIT] reset_signal (5, 'v')
```

### 3. Widget State Inspection

Comprehensive widget inspection:

```python
from tools.editor.debug_gui import inspect_widget

info = inspect_widget(my_widget, "primitive_panel")
print(f"Widget has {len(info['children'])} children")
print(f"Geometry: {info['geometry']}")
```

### 4. GUI State Snapshots

Take snapshots of the entire GUI state:

```python
from tools.editor.debug_gui import inspect_gui_state

state = inspect_gui_state("after_double_click")
print(f"Active window: {state.get('active_window')}")
```

## Testing the Infrastructure

Run the comprehensive debugging test suite:

```bash
python tools/editor/test_gui_debugging.py
```

This tests:
- Event correlation tracking
- Signal emission monitoring
- Widget state inspection
- GUI state snapshots

## Debugging Double-Click Reset

### Enable Full Debugging

```bash
python tools/interactive_editor.py data/library/love/single_dating_to_love_M1.csv \
    --debug-gui --log-terminal
```

### What You'll See

1. **Mouse Events**:
   ```
   [DOUBLE_CLICK] mouseDoubleClickEvent called, button=1, correlation_id=a1b2c3
   [DOUBLE_CLICK] Scene pos: PySide6.QtCore.QPointF(150, 200) -> Data pos: PySide6.QtCore.QPointF(15.0, 2.5)
   ```

2. **Hit Detection**:
   ```
   [DOUBLE_CLICK] v: 1 points at PySide6.QtCore.QPointF(15.0, 2.5)
   [DOUBLE_CLICK] Hit detected: v point 7 at PySide6.QtCore.QPointF(15.0, 2.5)
   ```

3. **Signal Emission**:
   ```
   [SIGNAL_EMIT] primitive_reset_requested (7, 'v')
   ```

4. **Controller Processing**:
   ```
   [CONTROLLER] on_primitive_reset called: event_index=7, primitive=v, correlation_id=a1b2c3
   [CONTROLLER] old_value=2.969, baseline_value=7.0, diff=4.031
   ```

5. **Command Execution**:
   ```
   [UNDO] Pushing ResetPrimitiveCommand to stack (event=7, prim=v, 2.97->7.00)
   ```

### Troubleshooting Common Issues

#### No Signal Emissions
```bash
# Check signal connections
python -c "
from tools.editor.debug_gui import inspect_widget
# Inspect the primitive panel
info = inspect_widget(panel, 'primitive_panel')
print('Signal connections:', info.get('signal_connections', {}))
"
```

#### Coordinate Transformation Issues
```bash
# Enable mouse debugging to see coordinate transformations
python tools/interactive_editor.py --debug-mouse --log-terminal
```

#### Widget Initialization Problems
```bash
# Inspect widget hierarchy
python -c "
from tools.editor.debug_gui import inspect_gui_state
state = inspect_gui_state('startup')
print('Top level widgets:', [w['class'] for w in state.get('top_level_widgets', [])])
"
```

## Architecture

### Core Components

1. **EventTracker**: Tracks event chains with correlation IDs
2. **WidgetInspector**: Provides detailed widget state inspection
3. **EnhancedEventDebugger**: Coordinates all debugging features
4. **GUIDebugger**: Singleton instance for global access

### Integration Points

- **DoubleClickPlotItem**: Enhanced with correlation tracking
- **Controller**: Event correlation in reset handling
- **InteractiveEditor**: Command-line debugging options
- **Logging System**: Unified output through debug_config.py

## Best Practices

### For Developers

1. **Use Event Correlation**: Wrap complex operations in `event_correlation_context`
2. **Track Signals**: Monitor important signal emissions during development
3. **Inspect State**: Use widget inspection when debugging layout issues
4. **Enable Selectively**: Use specific debug flags rather than `--debug-gui` for performance

### For Debugging

1. **Start with Signals**: Enable `--debug-signals` first to verify connections
2. **Check Coordinates**: Use `--debug-mouse` for positioning issues
3. **Inspect Widgets**: Use `inspect_widget()` in debug sessions
4. **Follow Correlation IDs**: Use correlation IDs to trace complete event chains

## Performance Considerations

- GUI debugging adds overhead - disable in production
- Event history is limited to 100 entries
- Signal tracking uses function wrapping (minimal performance impact)
- Widget inspection is synchronous and fast

## Future Enhancements

- Visual debugging overlays
- Event replay capabilities
- Performance profiling integration
- Automated GUI testing framework