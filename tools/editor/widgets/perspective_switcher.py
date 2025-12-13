"""
Perspective Switcher Widget

Radio button group for switching between M1 and M2 perspectives.
Active perspective shown in red, inactive in grey.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QRadioButton, QLabel, QButtonGroup
from PySide6.QtCore import Signal, Qt


class PerspectiveSwitcher(QWidget):
    """Widget for switching between M1 and M2 perspectives."""
    
    # Signal emitted when perspective changes
    perspective_changed = Signal(str)  # 'M1' or 'M2'
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Current perspective
        self._current_perspective = 'M1'
        
        # Create UI
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI layout and widgets."""
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Label
        label = QLabel("Perspective:")
        label.setStyleSheet("font-weight: bold; font-size: 10pt;")
        layout.addWidget(label)
        
        # Create button group for exclusive selection
        self.button_group = QButtonGroup(self)
        
        # M1 radio button with line indicator
        m1_container = QVBoxLayout()
        m1_container.setSpacing(2)
        self.m1_button = QRadioButton("M1")
        self.m1_button.setChecked(True)
        self.m1_button.setStyleSheet(self._get_button_style(True))
        self.button_group.addButton(self.m1_button, 1)
        m1_container.addWidget(self.m1_button)
        
        # M1 line indicator (solid initially)
        self.m1_line = QLabel()
        self.m1_line.setFixedHeight(3)
        self.m1_line.setFixedWidth(40)
        self.m1_line.setStyleSheet("background-color: blue;")
        m1_container.addWidget(self.m1_line)
        
        layout.addLayout(m1_container)
        
        # M2 radio button with line indicator
        m2_container = QVBoxLayout()
        m2_container.setSpacing(2)
        self.m2_button = QRadioButton("M2")
        self.m2_button.setStyleSheet(self._get_button_style(False))
        self.button_group.addButton(self.m2_button, 2)
        m2_container.addWidget(self.m2_button)
        
        # M2 line indicator (dashed initially)
        self.m2_line = QLabel()
        self.m2_line.setFixedHeight(3)
        self.m2_line.setFixedWidth(40)
        self.m2_line.setStyleSheet("background-color: transparent; border-top: 3px dashed blue;")
        m2_container.addWidget(self.m2_line)
        
        layout.addLayout(m2_container)
        
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Connect signals
        self.m1_button.toggled.connect(self._on_m1_toggled)
        self.m2_button.toggled.connect(self._on_m2_toggled)
    
    def _get_button_style(self, is_active):
        """Get stylesheet for button based on active state."""
        if is_active:
            return """
                QRadioButton {
                    font-size: 11pt;
                    font-weight: bold;
                    color: #cc0000;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
                QRadioButton::indicator:checked {
                    background-color: #cc0000;
                    border: 2px solid #990000;
                    border-radius: 8px;
                }
            """
        else:
            return """
                QRadioButton {
                    font-size: 11pt;
                    color: #888888;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
                QRadioButton::indicator:unchecked {
                    background-color: #cccccc;
                    border: 2px solid #999999;
                    border-radius: 8px;
                }
            """
    
    def _on_m1_toggled(self, checked):
        """Handle M1 button toggle."""
        if checked:
            self._current_perspective = 'M1'
            self.m1_button.setStyleSheet(self._get_button_style(True))
            self.m2_button.setStyleSheet(self._get_button_style(False))
            # Update line indicators: M1 solid, M2 dashed
            self.m1_line.setStyleSheet("background-color: blue;")
            self.m2_line.setStyleSheet("background-color: transparent; border-top: 3px dashed blue;")
            self.perspective_changed.emit('M1')
    
    def _on_m2_toggled(self, checked):
        """Handle M2 button toggle."""
        if checked:
            self._current_perspective = 'M2'
            self.m1_button.setStyleSheet(self._get_button_style(False))
            self.m2_button.setStyleSheet(self._get_button_style(True))
            # Update line indicators: M2 solid, M1 dashed
            self.m1_line.setStyleSheet("background-color: transparent; border-top: 3px dashed blue;")
            self.m2_line.setStyleSheet("background-color: blue;")
            self.perspective_changed.emit('M2')
    
    def get_perspective(self):
        """Get current perspective."""
        return self._current_perspective
    
    def set_perspective(self, perspective):
        """Set perspective programmatically.
        
        Args:
            perspective: 'M1' or 'M2'
        """
        if perspective == 'M1':
            self.m1_button.setChecked(True)
        elif perspective == 'M2':
            self.m2_button.setChecked(True)
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts."""
        if event.key() == Qt.Key_Tab or event.key() == Qt.Key_Space:
            # Toggle perspective
            if self._current_perspective == 'M1':
                self.m2_button.setChecked(True)
            else:
                self.m1_button.setChecked(True)
            event.accept()
        else:
            super().keyPressEvent(event)
