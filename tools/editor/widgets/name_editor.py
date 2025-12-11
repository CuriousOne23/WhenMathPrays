"""
Name Editor Widget

Simple widget for editing the scenario name (M1 or M2 perspective).
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Signal


class NameEditor(QWidget):
    """
    Widget for editing scenario name.
    
    Signals:
        name_changed(str): Emitted when name is changed
    """
    
    name_changed = Signal(str)
    
    def __init__(self, initial_name: str = ""):
        super().__init__()
        
        self._setup_ui(initial_name)
    
    def _setup_ui(self, initial_name: str):
        """Create UI layout."""
        layout = QVBoxLayout()
        
        # Title label
        title = QLabel("Scenario Name")
        title.setStyleSheet("font-weight: bold; font-size: 10pt;")
        layout.addWidget(title)
        
        # Name input field
        input_layout = QHBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setText(initial_name)
        self.name_input.setPlaceholderText("Enter name...")
        self.name_input.returnPressed.connect(self._on_name_changed)
        
        # Apply button (optional - also triggers on Enter)
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self._on_name_changed)
        apply_btn.setMaximumWidth(60)
        
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(apply_btn)
        
        layout.addLayout(input_layout)
        
        self.setLayout(layout)
    
    def _on_name_changed(self):
        """Handle name change."""
        new_name = self.name_input.text().strip()
        self.name_changed.emit(new_name)
    
    def set_name(self, name: str):
        """
        Update displayed name.
        
        Args:
            name: New name to display
        """
        self.name_input.setText(name)
    
    def get_name(self) -> str:
        """
        Get current name.
        
        Returns:
            Current name text
        """
        return self.name_input.text().strip()
