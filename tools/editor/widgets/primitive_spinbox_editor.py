"""
Primitive Spinbox Editor Widget.

Single shared spinbox for precise numeric input of primitive values.
Follows "Active Primitive State Tracking" pattern from ARCHITECTURE.md.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QDoubleSpinBox, QGroupBox
)
from PySide6.QtCore import Signal


class PrimitiveSpinboxEditor(QWidget):
    """
    Widget for editing primitive values with precise numeric input.
    
    Architecture (from ARCHITECTURE.md - Spinbox Primitive Editor):
    - Controller owns active_primitive_state (which primitive + which event)
    - Widget displays controller state (label + value)
    - Unidirectional signal flow: widget emits value_changed, controller updates model
    - Label persists until next primitive selected (user requirement)
    
    Signals:
        value_changed: Emitted when user commits new value (float)
    """
    
    value_changed = Signal(float)  # New primitive value
    
    def __init__(self):
        """Initialize primitive spinbox editor."""
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup widget UI."""
        # Main group box
        group = QGroupBox("Primitive Value Editor")
        layout = QVBoxLayout()
        
        # Label showing which primitive is active
        # Follows same pattern as gamma_self plot labels (ARCHITECTURE.md requirement)
        self.active_label = QLabel('Editing: (none)')
        self.active_label.setStyleSheet("font-weight: bold; color: #333;")
        layout.addWidget(self.active_label)
        
        # Spinbox for value input
        spinbox_layout = QHBoxLayout()
        spinbox_layout.addWidget(QLabel("Value:"))
        
        self.spinbox = QDoubleSpinBox()
        self.spinbox.setRange(-10.0, 10.0)  # Human-scale authoring values (CONSTANTS.md)
        self.spinbox.setDecimals(1)
        self.spinbox.setSingleStep(0.1)
        self.spinbox.setEnabled(False)  # Disabled until primitive selected
        self.spinbox.setKeyboardTracking(False)  # Only emit on Enter/focus loss
        spinbox_layout.addWidget(self.spinbox)
        
        layout.addLayout(spinbox_layout)
        
        # Info text
        info_label = QLabel("Click event, then click primitive to edit")
        info_label.setStyleSheet("font-size: 9pt; color: #666;")
        layout.addWidget(info_label)
        
        group.setLayout(layout)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(group)
        main_layout.addStretch()
        self.setLayout(main_layout)
        
        # Connect signals
        self.spinbox.valueChanged.connect(self._on_value_changed)
    
    def _on_value_changed(self, value: float):
        """
        Internal handler for spinbox value change.
        
        Only emits if spinbox is enabled (primitive is active).
        """
        if self.spinbox.isEnabled():
            self.value_changed.emit(value)
    
    def set_active_primitive(self, primitive_name: str, current_value: float, event_time: float = None):
        """
        Set the active primitive and its current value.
        
        Called by controller when user selects a primitive.
        
        Args:
            primitive_name: Name of primitive ('v', 'r', 'f', 'a', 'S')
            current_value: Current value of that primitive
            event_time: Time of the event (day number)
        """
        if event_time is not None:
            self.active_label.setText(f"Editing: {primitive_name} @ t={event_time:.1f}")
        else:
            self.active_label.setText(f"Editing: {primitive_name}")
        self.spinbox.blockSignals(True)  # Prevent emit during programmatic set
        self.spinbox.setValue(current_value)
        self.spinbox.blockSignals(False)
        self.spinbox.setEnabled(True)
    
    def clear_active(self):
        """
        Clear active primitive selection.
        
        Called when no event/primitive selected.
        """
        self.active_label.setText("Editing: (none)")
        self.spinbox.setEnabled(False)
    
    def get_active_label_text(self) -> str:
        """Get current label text (for debugging/testing)."""
        return self.active_label.text()
    
    def update_value(self, new_value: float):
        """
        Update spinbox value without emitting signal.
        
        Used during drag operations to keep spinbox in sync.
        
        Args:
            new_value: New value to display
        """
        self.spinbox.blockSignals(True)
        self.spinbox.setValue(new_value)
        self.spinbox.blockSignals(False)
    
    def is_editing(self) -> bool:
        """Check if currently editing a primitive."""
        return self.spinbox.isEnabled()
