# Perspective Management Architecture Refactor

**Status**: Design Phase  
**Created**: December 12, 2024  
**Priority**: Critical - Resolves architectural debt causing state synchronization bugs

---

## Problem Statement

### Current Architecture Issues

1. **Manual State Synchronization**: Perspective switching requires manually coordinating 3+ components
   - Controller updates `self.perspective`
   - Controller directly sets `primitive_panel.current_perspective`
   - Controller directly sets `trajectory_panel.current_perspective`
   - Controller manually clears/recreates label dictionaries
   - Components can get out of sync

2. **No Single Source of Truth**: Perspective state scattered across components
   - Model has perspective-INDEPENDENT `modified_primitives` (shared between M1/M2)
   - Panels maintain separate `current_perspective` attributes
   - No atomic transaction for perspective changes

3. **Bug Manifestation**: Labels from M1 perspective appear in M2 perspective
   - Despite 15+ removal attempts (removeItem, deleteLater, nuclear cleanup)
   - Labels are responsive (move with M2 markers) indicating active creation
   - Hidden code paths recreate labels without debug tracing catching them

4. **Architectural Debt**: Similar bugs will emerge with future features
   - Any new perspective-aware component requires manual coordination
   - Easy to miss cleanup in one component
   - Difficult to debug event ordering issues

---

## Design Goals

### Primary Goals
1. **Centralized Coordination**: Single source managing perspective state
2. **Atomic Transactions**: Perspective switches happen completely or not at all
3. **Observable by Design**: Built-in logging and event tracing
4. **Extensible**: 3rd parties can add perspective-aware components

### Non-Goals
- Not changing the dual-perspective model (M1/M2 stays)
- Not affecting user-facing functionality
- Not requiring rewrites of working single-perspective logic

---

## Proposed Architecture

### Event-Driven Perspective Management

```
┌─────────────────────────────────────────────────────────────┐
│                    EditorController                          │
│  - Owns perspective state                                   │
│  - Emits Qt signal: perspective_changed(old, new)           │
│  - Logs all perspective operations                          │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ Signal: perspective_changed
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
┌─────────────────┐ ┌─────────────┐ ┌────────────────┐
│ PrimitivePanel  │ │   Model     │ │ TrajectoryPanel│
│ - Subscribes    │ │ - Subscribes│ │ - Subscribes   │
│ - Cleans labels │ │ - Returns   │ │ - Cleans markers│
│ - Logs actions  │ │   perspective│ │ - Logs actions │
│                 │ │   data      │ │                │
└─────────────────┘ └─────────────┘ └────────────────┘
```

### Components

#### 1. EditorController (Enhanced)

**Responsibilities**:
- Single source of truth for current perspective
- Emits `perspective_changed(old_perspective, new_perspective)` Qt signal
- Logs all perspective operations to observability system

**API**:
```python
class EditorController(QObject):
    # Qt Signal
    perspective_changed = pyqtSignal(str, str)  # (old, new)
    
    def switch_perspective(self, new_perspective: str):
        """
        Atomically switch perspective with full observability.
        Emits perspective_changed signal.
        """
        old = self.perspective
        ObservabilityLog.event("perspective_switch_start", old=old, new=new_perspective)
        
        self.perspective = new_perspective
        self.perspective_changed.emit(old, new_perspective)
        
        ObservabilityLog.event("perspective_switch_complete", old=old, new=new_perspective)
```

#### 2. PrimitivePanel (Refactored)

**Responsibilities**:
- Listens to `perspective_changed` signal
- Manages its own label cleanup/recreation
- Logs all label operations

**API**:
```python
class PrimitivePanelPyQtGraph(QWidget):
    def __init__(self, ...):
        # Subscribe to controller's signal
        controller.perspective_changed.connect(self._on_perspective_changed)
    
    def _on_perspective_changed(self, old_perspective: str, new_perspective: str):
        """
        Handle perspective switch.
        Called automatically via Qt signal.
        """
        ObservabilityLog.event("primitive_panel_perspective_change", 
                              component="PrimitivePanel",
                              old=old_perspective, 
                              new=new_perspective)
        
        # Hide old perspective labels
        old_labels = self._get_labels_for_perspective(old_perspective)
        for key, text_item in old_labels.items():
            self.plot_items[key[1]].removeItem(text_item)
            ObservabilityLog.event("label_hidden", key=key, perspective=old_perspective)
        
        # Show new perspective labels
        new_labels = self._get_labels_for_perspective(new_perspective)
        for key, text_item in new_labels.items():
            self.plot_items[key[1]].addItem(text_item)
            ObservabilityLog.event("label_shown", key=key, perspective=new_perspective)
        
        self.current_perspective = new_perspective
        ObservabilityLog.event("primitive_panel_perspective_complete", new=new_perspective)
```

#### 3. EditorModel (Enhanced)

**Responsibilities**:
- Track perspective-specific modifications
- Return perspective-filtered data

**API**:
```python
class EditorModel:
    def __init__(self):
        # Perspective-aware modification tracking
        self.modified_primitives_m1: Dict[float, Set[str]] = {}  # {time: {prims}}
        self.modified_primitives_m2: Dict[float, Set[str]] = {}
    
    def get_modified_primitives(self, perspective: str) -> Dict[float, Set[str]]:
        """Return modifications for specified perspective only."""
        return self.modified_primitives_m1 if perspective == "M1" else self.modified_primitives_m2
    
    def mark_primitive_modified(self, time: float, primitive: str, perspective: str):
        """Mark a primitive as modified in the specified perspective."""
        modified = self.get_modified_primitives(perspective)
        if time not in modified:
            modified[time] = set()
        modified[time].add(primitive)
        
        ObservabilityLog.event("primitive_modified", 
                              time=time, 
                              primitive=primitive, 
                              perspective=perspective)
```

#### 4. TrajectoryPanel (Refactored)

**Responsibilities**:
- Listens to `perspective_changed` signal
- Manages its own marker cleanup
- Logs trajectory operations

**API**: (Similar pattern to PrimitivePanel)

---

## Observability System

### Built-In Logging Infrastructure

```python
# tools/editor/observability.py

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
import json

class ObservabilityLog:
    """
    Centralized observability system for editor debugging.
    
    Design Principles:
    - Separate from business logic
    - Toggle-able via environment variable or config
    - Structured output for analysis
    - Minimal performance impact
    """
    
    _enabled = False
    _logger = None
    _log_file = None
    
    @classmethod
    def initialize(cls, enabled: bool = None):
        """
        Initialize observability system.
        
        Args:
            enabled: True/False to override, None to read from environment
        """
        if enabled is None:
            import os
            enabled = os.environ.get("EDITOR_DEBUG", "false").lower() == "true"
        
        cls._enabled = enabled
        
        if cls._enabled:
            # Create logs directory
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            # Setup file logger
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cls._log_file = log_dir / f"editor_debug_{timestamp}.log"
            
            cls._logger = logging.getLogger("EditorObservability")
            cls._logger.setLevel(logging.DEBUG)
            
            handler = logging.FileHandler(cls._log_file)
            handler.setFormatter(logging.Formatter(
                '%(asctime)s.%(msecs)03d | %(message)s',
                datefmt='%H:%M:%S'
            ))
            cls._logger.addHandler(handler)
            
            cls._logger.info(f"=== Editor Observability Initialized ===")
            cls._logger.info(f"Log file: {cls._log_file}")
    
    @classmethod
    def event(cls, event_type: str, **kwargs):
        """
        Log a structured event.
        
        Args:
            event_type: Event identifier (e.g., "perspective_switch_start")
            **kwargs: Event-specific data
        """
        if not cls._enabled or cls._logger is None:
            return
        
        event_data = {
            "event": event_type,
            **kwargs
        }
        
        cls._logger.info(json.dumps(event_data))
    
    @classmethod
    def is_enabled(cls) -> bool:
        """Check if observability is enabled."""
        return cls._enabled
    
    @classmethod
    def get_log_file(cls) -> Path:
        """Get path to current log file."""
        return cls._log_file


# Usage in application.py or interactive_editor.py:
from tools.editor.observability import ObservabilityLog

# Initialize at startup
ObservabilityLog.initialize()  # Reads EDITOR_DEBUG env var

# Or force enable for debugging:
# ObservabilityLog.initialize(enabled=True)
```

### Log Format

Each log entry is a JSON object for easy parsing:

```json
{"event": "perspective_switch_start", "old": "M1", "new": "M2"}
{"event": "primitive_panel_perspective_change", "component": "PrimitivePanel", "old": "M1", "new": "M2"}
{"event": "label_hidden", "key": [42.0, "v"], "perspective": "M1"}
{"event": "label_hidden", "key": [42.0, "v"], "perspective": "M1"}
{"event": "label_shown", "key": [35.0, "r"], "perspective": "M2"}
{"event": "primitive_panel_perspective_complete", "new": "M2"}
{"event": "trajectory_panel_perspective_change", "component": "TrajectoryPanel", "old": "M1", "new": "M2"}
{"event": "perspective_switch_complete", "old": "M1", "new": "M2"}
```

### Enabling Debug Mode

**Via Environment Variable** (recommended):
```bash
# Windows PowerShell
$env:EDITOR_DEBUG="true"
python tools\interactive_editor_new.py data\library\love\single_dating_to_love_M1.csv

# Linux/Mac
EDITOR_DEBUG=true python tools/interactive_editor_new.py data/library/love/single_dating_to_love_M1.csv
```

**Via Config File**:
```json
// config/editor_config.json
{
  "debug": {
    "observability_enabled": true
  }
}
```

**Programmatically**:
```python
# Force enable for debugging session
ObservabilityLog.initialize(enabled=True)
```

---

## Third-Party Extensibility

### Adding Perspective-Aware Components

Third-party developers can add perspective-aware components by:

1. **Subscribe to Signal**:
```python
class CustomPanel(QWidget):
    def __init__(self, controller):
        super().__init__()
        # Subscribe to perspective changes
        controller.perspective_changed.connect(self._on_perspective_changed)
    
    def _on_perspective_changed(self, old: str, new: str):
        # Component-specific cleanup/update logic
        self.update_for_perspective(new)
```

2. **Use Observability**:
```python
from tools.editor.observability import ObservabilityLog

def _on_perspective_changed(self, old: str, new: str):
    ObservabilityLog.event("custom_panel_perspective_change",
                          component="CustomPanel",
                          old=old, 
                          new=new)
    # ... component logic ...
    ObservabilityLog.event("custom_panel_perspective_complete", new=new)
```

3. **Query Model by Perspective**:
```python
# Instead of accessing shared modified_primitives:
# BAD: modifications = model.modified_primitives

# GOOD: Get perspective-specific data:
modifications = model.get_modified_primitives(controller.perspective)
```

### Extension Points

Documented extension points for 3rd parties:

1. **Perspective Change Listeners**: Subscribe to `perspective_changed` signal
2. **Observability Events**: Log custom events via `ObservabilityLog.event()`
3. **Model Queries**: Use perspective-aware API methods
4. **Custom Panels**: Follow PrimitivePanel/TrajectoryPanel patterns

---

## Migration Strategy

### Phase 1: Observability Infrastructure (Week 1)
- Create `observability.py` module
- Add `ObservabilityLog` initialization to application startup
- Document usage and configuration

### Phase 2: Model Refactor (Week 1)
- Split `modified_primitives` into `modified_primitives_m1` and `modified_primitives_m2`
- Add perspective-aware query methods
- Update all model access to use new API
- Comprehensive testing

### Phase 3: Signal-Based Coordination (Week 2)
- Add `perspective_changed` signal to EditorController
- Refactor PrimitivePanel to subscribe and self-manage
- Refactor TrajectoryPanel to subscribe and self-manage
- Add observability logging to all operations

### Phase 4: Cleanup (Week 2)
- Remove manual coordination code from controller
- Remove scattered perspective state
- Comprehensive integration testing
- Update architecture documentation

### Phase 5: Validation (Week 3)
- Verify label bug is resolved
- Performance testing (observability overhead)
- Third-party extension validation
- Documentation review

---

## Success Criteria

1. **Bug Resolution**: Labels no longer persist across perspective switches
2. **Atomic Operations**: Perspective switches complete fully or not at all
3. **Observability**: Full event trace available for debugging
4. **Extensibility**: Third party can add perspective-aware panel in <50 lines
5. **Performance**: <5ms overhead for perspective switch with logging enabled
6. **Maintainability**: Adding new perspective-aware component requires <3 touch points

---

## Risks and Mitigations

### Risk: Qt Signal/Slot Overhead
**Mitigation**: Performance testing, fallback to direct calls if needed

### Risk: Breaking Existing Functionality
**Mitigation**: Comprehensive test suite, gradual migration, feature flags

### Risk: Observability Performance Impact
**Mitigation**: Disabled by default, async logging if needed, sampling for high-frequency events

### Risk: Model API Changes Break Tests
**Mitigation**: Backward compatibility layer during migration, comprehensive test updates

---

## References

- [Qt Signals and Slots Documentation](https://doc.qt.io/qt-6/signalsandslots.html)
- [Observer Pattern](https://refactoring.guru/design-patterns/observer)
- [DEBUG.md](../DEBUG.md) - Debugging methodology
- [ARCHITECTURE.md](../../ARCHITECTURE.md) - Overall system architecture
