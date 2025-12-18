#!/usr/bin/env python3
"""
GUI Debugging Test Script for Interactive Editor.

This script provides comprehensive testing and debugging tools for the
double-click reset functionality and other GUI interactions.

Usage:
    python tools/editor/test_gui_debugging.py

Features:
- Test signal connections
- Simulate mouse events
- Inspect widget state
- Verify event correlation
- Run automated GUI tests
"""

import sys
import os
import time
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QMouseEvent

from tools.editor.debug_gui import (
    get_gui_debugger, enable_all_gui_debugging,
    inspect_widget, inspect_gui_state, event_correlation_context
)
from tools.editor.debug_config import get_logger

logger = get_logger('test_gui_debugging')

class TestWidget(QWidget):
    """Test widget with signals for debugging testing."""

    test_signal = Signal(int, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI Debugging Test")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.label = QLabel("Click anywhere to test mouse events")
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Connect signal for testing
        self.test_signal.connect(self.on_test_signal)

    def on_test_signal(self, value: int, text: str):
        """Handle test signal."""
        logger.info(f"[TEST] Received signal: {value}, {text}")
        self.label.setText(f"Signal received: {value}, {text}")

    def mousePressEvent(self, event):
        """Handle mouse press for testing."""
        logger.info(f"[TEST] Mouse press at {event.pos()}")
        super().mousePressEvent(event)

class GUIDebuggingTester:
    """Comprehensive GUI debugging tester."""

    def __init__(self):
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)

        # Enable all debugging
        enable_all_gui_debugging()
        self.debugger = get_gui_debugger()

    def test_basic_debugging(self):
        """Test basic debugging infrastructure."""
        logger.info("[TEST] Testing basic debugging infrastructure")

        # Test GUI state inspection
        state = inspect_gui_state("test_start")
        logger.info(f"[TEST] Initial GUI state: {state}")

        # Create test widget
        widget = TestWidget()
        widget.show()

        # Inspect widget
        widget_info = inspect_widget(widget, "test_widget")
        logger.info(f"[TEST] Widget info: {widget_info}")

        # Test signal tracking
        self.debugger.event_tracker.track_signal(widget.test_signal, "test_signal")

        # Emit test signal
        logger.info("[TEST] Emitting test signal")
        widget.test_signal.emit(42, "hello world")

        # Simulate mouse event
        logger.info("[TEST] Simulating mouse event")
        pos = widget.rect().center()
        mouse_event = QMouseEvent(
            QMouseEvent.MouseButtonPress,
            pos,
            Qt.LeftButton,
            Qt.LeftButton,
            Qt.NoModifier
        )
        QApplication.sendEvent(widget, mouse_event)

        # Check event history
        history = self.debugger.event_tracker.get_event_history()
        logger.info(f"[TEST] Event history: {len(history)} events")

        for event in history[-3:]:  # Last 3 events
            logger.info(f"[TEST] Recent event: {event['event_type']} from {event['source']}")

        return True

    def test_event_correlation(self):
        """Test event correlation tracking."""
        logger.info("[TEST] Testing event correlation")

        with event_correlation_context('test_correlation', 'GUIDebuggingTester', test_data="correlation_test") as correlation_id:
            logger.info(f"[TEST] Inside correlation context: {correlation_id}")

            # Simulate some work
            time.sleep(0.1)

            # Add some steps
            self.debugger.event_tracker.add_event_step(
                correlation_id, 'step1', 'GUIDebuggingTester', data="step1_data"
            )
            time.sleep(0.05)

            self.debugger.event_tracker.add_event_step(
                correlation_id, 'step2', 'GUIDebuggingTester', data="step2_data"
            )

        # Check that correlation was tracked
        history = self.debugger.event_tracker.get_event_history()
        correlation_events = [e for e in history if e.get('correlation_id') == correlation_id]

        if correlation_events:
            event = correlation_events[0]
            logger.info(f"[TEST] Correlation event completed: {event['result']} in {event['duration']:.3f}s")
            logger.info(f"[TEST] Steps recorded: {len(event['steps'])}")
            return True
        else:
            logger.error("[TEST] Correlation event not found")
            return False

    def test_widget_inspection(self):
        """Test widget inspection capabilities."""
        logger.info("[TEST] Testing widget inspection")

        # Create a complex widget hierarchy
        parent = QWidget()
        parent.setWindowTitle("Parent Widget")

        child1 = QLabel("Child 1")
        child1.setObjectName("child1")
        child2 = QLabel("Child 2")
        child2.setObjectName("child2")

        layout = QVBoxLayout()
        layout.addWidget(child1)
        layout.addWidget(child2)
        parent.setLayout(layout)

        # Inspect the hierarchy
        parent_info = inspect_widget(parent, "parent_widget")
        logger.info(f"[TEST] Parent has {len(parent_info['children'])} direct children")

        for child_info in parent_info['children']:
            logger.info(f"[TEST] Child: {child_info['class']} '{child_info['object_name']}' visible={child_info['visible']}")

        return len(parent_info['children']) == 2

    def run_all_tests(self):
        """Run all debugging tests."""
        logger.info("[TEST] Starting comprehensive GUI debugging tests")

        tests = [
            ("Basic Debugging", self.test_basic_debugging),
            ("Event Correlation", self.test_event_correlation),
            ("Widget Inspection", self.test_widget_inspection),
        ]

        results = []
        for test_name, test_func in tests:
            try:
                logger.info(f"[TEST] Running {test_name}")
                result = test_func()
                results.append((test_name, result))
                logger.info(f"[TEST] {test_name}: {'PASS' if result else 'FAIL'}")
            except Exception as e:
                logger.error(f"[TEST] {test_name} failed with exception: {e}")
                results.append((test_name, False))

        # Summary
        passed = sum(1 for _, result in results if result)
        total = len(results)

        logger.info(f"[TEST] Results: {passed}/{total} tests passed")

        for test_name, result in results:
            status = "PASS" if result else "FAIL"
            logger.info(f"[TEST] {test_name}: {status}")

        return passed == total

def main():
    """Main test function."""
    logger.info("[TEST] GUI Debugging Test Script Starting")

    # Check if we're in GUI environment
    if not os.environ.get('DISPLAY') and os.name != 'nt':
        logger.warning("[TEST] No display detected, some tests may not work")

    try:
        tester = GUIDebuggingTester()
        success = tester.run_all_tests()

        if success:
            logger.info("[TEST] All tests passed!")
            return 0
        else:
            logger.error("[TEST] Some tests failed")
            return 1

    except Exception as e:
        logger.error(f"[TEST] Test script failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())