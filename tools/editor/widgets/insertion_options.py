"""
Event insertion options widget.

Allows user to specify explicit time points for event insertion.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QGroupBox, QLabel, QScrollArea
)
from PySide6.QtCore import Signal, Qt


class InsertionOptionsWidget(QWidget):
    """
    Widget for managing event insertion time points.
    
    Signals:
        insertions_changed: Emitted when insertion list changes (list of float times)
    """
    
    insertions_changed = Signal(list)
    
    def __init__(self):
        """Initialize insertion options widget."""
        super().__init__()
        self.time_inputs = []  # List of QLineEdit widgets
        self._updating_from_model = False  # Flag to prevent signal loops
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup widget UI."""
        # Main group box
        group = QGroupBox("Event Insertion Points")
        layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel("Enter time values to insert events.\nPress Enter to add, clear and Enter to remove.")
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: gray; font-size: 9pt;")
        layout.addWidget(instructions)
        
        # Scroll area for time inputs
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(200)
        
        self.inputs_container = QWidget()
        self.inputs_layout = QVBoxLayout()
        self.inputs_layout.setSpacing(5)
        self.inputs_container.setLayout(self.inputs_layout)
        scroll.setWidget(self.inputs_container)
        
        layout.addWidget(scroll)
        
        # Add first input field
        self._add_input_field()
        
        group.setLayout(layout)
        
        # Main widget layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(group)
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def _add_input_field(self, value: str = ""):
        """Add a new time input field."""
        container = QWidget()
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        
        # Time input
        input_field = QLineEdit()
        input_field.setPlaceholderText("Enter time (e.g., 25.5)")
        input_field.setText(value)
        input_field.setMaximumWidth(150)
        input_field.returnPressed.connect(lambda: self._on_input_changed(input_field))
        
        hlayout.addWidget(input_field)
        hlayout.addStretch()
        
        container.setLayout(hlayout)
        self.inputs_layout.addWidget(container)
        self.time_inputs.append((container, input_field))
    
    def _on_input_changed(self, changed_input: QLineEdit):
        """Handle input field change (Enter pressed)."""
        text = changed_input.text().strip()
        
        if text == "":
            # Empty field - remove it if not the last one
            self._remove_input(changed_input)
        else:
            # Validate input
            try:
                float(text)
                # Valid input - check if we need to add a new field
                if changed_input == self.time_inputs[-1][1]:
                    # Last field filled - add a new empty one
                    self._add_input_field()
            except ValueError:
                # Invalid input - clear it
                changed_input.setText("")
                changed_input.setPlaceholderText("Invalid - enter a number")
        
        # Notify about changes
        self._emit_changes()
    
    def _remove_input(self, input_field: QLineEdit):
        """Remove an input field from the list."""
        # Find and remove
        for i, (container, field) in enumerate(self.time_inputs):
            if field == input_field:
                # Don't remove if it's the only field
                if len(self.time_inputs) == 1:
                    field.clear()
                    return
                
                # Remove from layout and list
                self.inputs_layout.removeWidget(container)
                container.deleteLater()
                self.time_inputs.pop(i)
                break
    
    def _emit_changes(self):
        """Emit current list of valid insertion times."""
        # Don't emit if we're updating from model to avoid signal loops
        if self._updating_from_model:
            return
            
        times = []
        for _, field in self.time_inputs:
            text = field.text().strip()
            if text:
                try:
                    times.append(float(text))
                except ValueError:
                    pass
        
        # Sort times
        times.sort()
        self.insertions_changed.emit(times)
    
    def get_insertion_times(self) -> list:
        """
        Get current list of insertion times.
        
        Returns:
            List of float time values, sorted
        """
        times = []
        for _, field in self.time_inputs:
            text = field.text().strip()
            if text:
                try:
                    times.append(float(text))
                except ValueError:
                    pass
        times.sort()
        return times
    
    def clear_all(self):
        """Clear all input fields."""
        # Remove all but first
        while len(self.time_inputs) > 1:
            container, _ = self.time_inputs.pop()
            self.inputs_layout.removeWidget(container)
            container.deleteLater()
        
        # Clear the remaining one
        if self.time_inputs:
            self.time_inputs[0][1].clear()
        
        self._emit_changes()
    
    def update_from_times(self, times: list):
        """
        Update widget to display the given list of insertion times.
        This is used to sync the widget with the actual model state.
        
        Args:
            times: List of float time values (will be sorted)
        """
        # Block signals during update to prevent loops
        self._updating_from_model = True
        
        try:
            # Sort times
            sorted_times = sorted(times)
            
            # Clear existing fields
            while len(self.time_inputs) > 0:
                container, _ = self.time_inputs.pop()
                self.inputs_layout.removeWidget(container)
                container.deleteLater()
            
            # Add fields for each time
            for time_val in sorted_times:
                self._add_input_field(str(time_val))
            
            # Add one empty field at the end
            self._add_input_field()
        finally:
            # Always restore signal emission
            self._updating_from_model = False
        
        # Don't emit changes - this is just syncing the UI
