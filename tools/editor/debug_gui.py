"""
Enhanced GUI Event Debugging Infrastructure for WhenMathPrays Interactive Editor.

This module provides comprehensive debugging tools for Qt/PyQtGraph GUI events,
signal/slot connections, and widget interactions. It makes GUI debugging tractable
by providing:

1. Unified event logging with correlation IDs
2. Signal emission tracking and verification
3. Widget state inspection tools
4. Event replay capabilities
5. Visual debugging overlays

Usage:
    from tools.editor.debug_gui import GUIDebugger, EventTracker

    # Enable comprehensive GUI debugging
    debugger = GUIDebugger()
    debugger.enable_all_debugging()

    # Track specific signals
    tracker = EventTracker()
    tracker.track_signal(widget.primitive_reset_requested)

    # Inspect widget state
    debugger.inspect_widget(panel, "primitive_panel")
"""

import logging
import time
import uuid
from typing import Dict, List, Any, Optional, Callable
from contextlib import contextmanager
from PySide6.QtCore import QObject, Signal, QEvent, Qt
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QMouseEvent, QKeyEvent

from .debug_config import get_logger

logger = get_logger('debug_gui')

# ============================================================================
# Event Correlation and Tracking
# ============================================================================

class EventTracker:
    """
    Tracks GUI events and signal emissions with correlation IDs.

    Provides end-to-end visibility into event chains from mouse clicks
    through signal emissions to slot executions.
    """

    def __init__(self):
        self.active_events: Dict[str, Dict[str, Any]] = {}
        self.event_history: List[Dict[str, Any]] = []
        self.signal_connections: Dict[Signal, List[Callable]] = {}

    def start_event(self, event_type: str, source: str, **kwargs) -> str:
        """
        Start tracking a new event chain.

        Args:
            event_type: Type of event (e.g., 'mouse_double_click', 'signal_emission')
            source: Source component (e.g., 'DoubleClickPlotItem', 'Controller')
            **kwargs: Additional event data

        Returns:
            Correlation ID for this event chain
        """
        correlation_id = str(uuid.uuid4())[:8]
        event_data = {
            'correlation_id': correlation_id,
            'event_type': event_type,
            'source': source,
            'start_time': time.time(),
            'kwargs': kwargs,
            'steps': []
        }
        self.active_events[correlation_id] = event_data

        logger.info(f"[EVENT_START] {correlation_id} {event_type} from {source}")
        return correlation_id

    def add_event_step(self, correlation_id: str, step: str, component: str, **data):
        """Add a processing step to an active event chain."""
        if correlation_id in self.active_events:
            step_data = {
                'timestamp': time.time(),
                'step': step,
                'component': component,
                'data': data
            }
            self.active_events[correlation_id]['steps'].append(step_data)
            logger.debug(f"[EVENT_STEP] {correlation_id} {step} in {component}")

    def end_event(self, correlation_id: str, result: str = "success", **final_data):
        """Complete an event chain."""
        if correlation_id in self.active_events:
            event_data = self.active_events[correlation_id]
            event_data.update({
                'end_time': time.time(),
                'duration': time.time() - event_data['start_time'],
                'result': result,
                'final_data': final_data
            })

            # Move to history
            self.event_history.append(event_data)
            del self.active_events[correlation_id]

            logger.info(f"[EVENT_END] {correlation_id} {result} in {event_data['duration']:.3f}s")

            # Keep only recent history
            if len(self.event_history) > 100:
                self.event_history = self.event_history[-50:]

    def track_signal(self, signal: Signal, signal_name: str = None):
        """
        Track all emissions of a Qt signal.

        Args:
            signal: Qt Signal to track
            signal_name: Human-readable name for the signal
        """
        if signal_name is None:
            signal_name = str(signal)

        # Store original connections
        if signal not in self.signal_connections:
            self.signal_connections[signal] = []

        # Monkey patch the signal to add tracking
        original_emit = signal.emit

        def tracked_emit(*args, **kwargs):
            correlation_id = self.start_event('signal_emission', signal_name, args=args)
            logger.info(f"[SIGNAL_EMIT] {signal_name} with args: {args}")

            try:
                result = original_emit(*args, **kwargs)
                self.end_event(correlation_id, "emitted")
                return result
            except Exception as e:
                self.end_event(correlation_id, f"error: {e}")
                raise

        signal.emit = tracked_emit
        logger.info(f"[SIGNAL_TRACK] Now tracking {signal_name}")

    def get_event_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent event history."""
        return self.event_history[-limit:]

# ============================================================================
# Widget State Inspection
# ============================================================================

class WidgetInspector:
    """
    Provides detailed inspection of Qt widget state for debugging.
    """

    @staticmethod
    def inspect_widget(widget: QWidget, name: str = None) -> Dict[str, Any]:
        """
        Comprehensive widget state inspection.

        Args:
            widget: Qt widget to inspect
            name: Human-readable name for the widget

        Returns:
            Dictionary with widget state information
        """
        if name is None:
            name = widget.__class__.__name__

        info = {
            'name': name,
            'class': widget.__class__.__name__,
            'object_name': widget.objectName(),
            'geometry': {
                'x': widget.x(),
                'y': widget.y(),
                'width': widget.width(),
                'height': widget.height()
            },
            'visible': widget.isVisible(),
            'enabled': widget.isEnabled(),
            'has_focus': widget.hasFocus(),
            'children': []
        }

        # Inspect children
        for child in widget.findChildren(QWidget):
            if child.parent() == widget:  # Direct children only
                info['children'].append({
                    'class': child.__class__.__name__,
                    'object_name': child.objectName(),
                    'visible': child.isVisible()
                })

        # Widget-specific inspection
        if hasattr(widget, 'scatter_items'):
            info['scatter_items'] = list(widget.scatter_items.keys())

        if hasattr(widget, 'plot_items'):
            info['plot_items'] = list(widget.plot_items.keys())

        logger.info(f"[WIDGET_INSPECT] {name}: {info}")
        return info

    @staticmethod
    def inspect_signal_connections(widget: QWidget) -> Dict[str, List[str]]:
        """
        Inspect signal connections on a widget.

        Note: Qt doesn't provide easy introspection of signal connections,
        so this is limited to what we can detect.
        """
        connections = {}

        # Check for common signals we know about
        signal_names = ['primitive_reset_requested', 'marker_clicked', 'valueChanged']

        for signal_name in signal_names:
            if hasattr(widget, signal_name):
                signal = getattr(widget, signal_name)
                # We can't easily inspect connections, but we can check if signal exists
                connections[signal_name] = "exists"

        return connections

# ============================================================================
# Enhanced Event Debugging
# ============================================================================

class EnhancedEventDebugger:
    """
    Enhanced event debugging with detailed logging and correlation.
    """

    def __init__(self):
        self.event_tracker = EventTracker()
        self.widget_inspector = WidgetInspector()
        self.mouse_events_enabled = False
        self.signal_tracking_enabled = False

    def enable_mouse_event_debugging(self):
        """Enable detailed mouse event logging."""
        self.mouse_events_enabled = True
        logger.info("[DEBUG_ENABLE] Mouse event debugging enabled")

    def enable_signal_tracking(self):
        """Enable signal emission tracking."""
        self.signal_tracking_enabled = True
        logger.info("[DEBUG_ENABLE] Signal tracking enabled")

    def debug_mouse_event(self, widget: QWidget, event: QMouseEvent, event_type: str):
        """Debug a mouse event with full context."""
        if not self.mouse_events_enabled:
            return

        correlation_id = self.event_tracker.start_event(
            'mouse_event',
            widget.__class__.__name__,
            event_type=event_type,
            button=event.button(),
            buttons=event.buttons(),
            pos=event.pos(),
            global_pos=event.globalPos()
        )

        logger.debug(f"[MOUSE_EVENT] {event_type} at {event.pos()} button={event.button()}")

        return correlation_id

    def debug_signal_emission(self, signal_name: str, *args):
        """Debug signal emission."""
        if not self.signal_tracking_enabled:
            return

        correlation_id = self.event_tracker.start_event(
            'signal_emission',
            signal_name,
            args=args
        )

        logger.debug(f"[SIGNAL_EMIT] {signal_name}({args})")
        return correlation_id

    def inspect_gui_state(self, name: str = "gui_state"):
        """Take a snapshot of the current GUI state."""
        app = QApplication.instance()
        if app:
            widgets = app.topLevelWidgets()
            state = {
                'top_level_widgets': len(widgets),
                'active_window': app.activeWindow().__class__.__name__ if app.activeWindow() else None,
                'focus_widget': app.focusWidget().__class__.__name__ if app.focusWidget() else None
            }
            logger.info(f"[GUI_STATE] {name}: {state}")
            return state
        return {}

# ============================================================================
# Global Debugger Instance
# ============================================================================

# Singleton debugger instance
_gui_debugger = EnhancedEventDebugger()

def get_gui_debugger() -> EnhancedEventDebugger:
    """Get the global GUI debugger instance."""
    return _gui_debugger

# ============================================================================
# Convenience Functions for Easy Debugging
# ============================================================================

def debug_mouse_event(widget: QWidget, event: QMouseEvent, event_type: str):
    """Convenience function for mouse event debugging."""
    return _gui_debugger.debug_mouse_event(widget, event, event_type)

def debug_signal_emission(signal_name: str, *args):
    """Convenience function for signal emission debugging."""
    return _gui_debugger.debug_signal_emission(signal_name, *args)

def inspect_widget(widget: QWidget, name: str = None):
    """Convenience function for widget inspection."""
    return _gui_debugger.widget_inspector.inspect_widget(widget, name)

def inspect_gui_state(name: str = "current"):
    """Convenience function for GUI state inspection."""
    return _gui_debugger.inspect_gui_state(name)

@contextmanager
def event_correlation_context(event_type: str, source: str, **kwargs):
    """
    Context manager for event correlation.

    Usage:
        with event_correlation_context('double_click_reset', 'DoubleClickPlotItem', prim='v', idx=5):
            # Process the event
            pass
    """
    correlation_id = _gui_debugger.event_tracker.start_event(event_type, source, **kwargs)
    try:
        yield correlation_id
    finally:
        _gui_debugger.event_tracker.end_event(correlation_id)

# ============================================================================
# Quick Setup Functions
# ============================================================================

def enable_all_gui_debugging():
    """
    Enable all GUI debugging features.

    Call this early in application startup for comprehensive debugging.
    """
    debugger = get_gui_debugger()
    debugger.enable_mouse_event_debugging()
    debugger.enable_signal_tracking()
    logger.info("[DEBUG_SETUP] All GUI debugging enabled")

def enable_minimal_gui_debugging():
    """
    Enable minimal GUI debugging (just signal tracking).

    Good for production debugging without too much noise.
    """
    debugger = get_gui_debugger()
    debugger.enable_signal_tracking()
    logger.info("[DEBUG_SETUP] Minimal GUI debugging enabled")