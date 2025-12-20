"""
Perspective Switcher Widget

Radio button group for switching between M1 and M2 perspectives.
Active perspective shown in red, inactive in grey.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QRadioButton, QLabel, QButtonGroup
from PySide6.QtCore import Signal, Qt

# Import debug configuration
from tools.editor.debug_config import get_logger

# Get logger for this module
_logger = get_logger('perspective_switcher')


class PerspectiveSwitcher(QWidget):
    """Widget for switching between M1 and M2 perspectives."""
    # Signal emitted when perspective changes
    perspective_changed = Signal(str)  # 'M1' or 'M2'
    # Signal emitted when entropy mode changes
    entropy_mode_changed = Signal(bool)  # True = by event, False = by time
    
    def __init__(self, parent=None, m1_available=True, m2_available=True):
        super().__init__(parent)
        
        # Available perspectives
        self.m1_available = m1_available
        self.m2_available = m2_available
        
        # Current perspective
        self._current_perspective = 'M1' if m1_available else 'M2'
        _logger.debug(f"PerspectiveSwitcher init: m1_available={m1_available}, m2_available={m2_available}, _current_perspective={self._current_perspective}")
        
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
        self.m1_button.setChecked(self._current_perspective == 'M1' and self.m1_available)
        self.m1_button.setEnabled(self.m1_available)
        self.m1_button.setStyleSheet(self._get_button_style(self._current_perspective == 'M1' and self.m1_available))
        if self.m1_available:
            self.button_group.addButton(self.m1_button, 1)
        m1_container.addWidget(self.m1_button)

        # M1 line indicator
        self.m1_line = QLabel()
        self.m1_line.setFixedHeight(3)
        self.m1_line.setFixedWidth(40)
        if self.m1_available and self._current_perspective == 'M1':
            self.m1_line.setStyleSheet("background-color: blue;")
        else:
            self.m1_line.setStyleSheet("background-color: transparent;")
        m1_container.addWidget(self.m1_line)

        layout.addLayout(m1_container)

        # M2 radio button with line indicator
        m2_container = QVBoxLayout()
        m2_container.setSpacing(2)
        self.m2_button = QRadioButton("M2")
        self.m2_button.setChecked(self._current_perspective == 'M2' and self.m2_available)
        self.m2_button.setEnabled(self.m2_available)
        self.m2_button.setStyleSheet(self._get_button_style(self._current_perspective == 'M2' and self.m2_available))
        if self.m2_available:
            self.button_group.addButton(self.m2_button, 2)
        m2_container.addWidget(self.m2_button)

        # M2 line indicator
        self.m2_line = QLabel()
        self.m2_line.setFixedHeight(3)
        self.m2_line.setFixedWidth(40)
        if self.m2_available and self._current_perspective == 'M2':
            self.m2_line.setStyleSheet("background-color: blue;")
        else:
            self.m2_line.setStyleSheet("background-color: transparent; border-top: 3px dashed blue;")
        m2_container.addWidget(self.m2_line)

        layout.addLayout(m2_container)

        # Entropy mode radio buttons
        entropy_label = QLabel("Entropy:")
        entropy_label.setStyleSheet("font-weight: bold; font-size: 10pt;")
        layout.addWidget(entropy_label)

        self.entropy_time_radio = QRadioButton("By Time")
        self.entropy_event_radio = QRadioButton("By Event")
        # Default: By Time unless set externally
        self.entropy_time_radio.setChecked(not getattr(self, '_entropy_per_event', False))
        self.entropy_event_radio.setChecked(getattr(self, '_entropy_per_event', False))
        layout.addWidget(self.entropy_time_radio)
        layout.addWidget(self.entropy_event_radio)

        layout.addStretch()
        self.setLayout(layout)

        # Connect signals
        self.m1_button.toggled.connect(self._on_m1_toggled)
        self.m2_button.toggled.connect(self._on_m2_toggled)
        self.entropy_time_radio.toggled.connect(self._on_entropy_mode_toggled)
        self.entropy_event_radio.toggled.connect(self._on_entropy_mode_toggled)

    def set_entropy_mode(self, by_event: bool):
        """Set the entropy mode radio buttons from external state."""
        self._entropy_per_event = by_event
        self.entropy_event_radio.setChecked(by_event)
        self.entropy_time_radio.setChecked(not by_event)

    def _on_entropy_mode_toggled(self):
        # Emit True if By Event is checked, else False
        self.entropy_mode_changed.emit(self.entropy_event_radio.isChecked())
    
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
        if checked and self.m1_available:
            self._current_perspective = 'M1'
            self.m1_button.setStyleSheet(self._get_button_style(True))
            self.m2_button.setStyleSheet(self._get_button_style(False))
            # Update line indicators: M1 solid, M2 dashed
            self.m1_line.setStyleSheet("background-color: blue;")
            self.m2_line.setStyleSheet("background-color: transparent; border-top: 3px dashed blue;")
            self.perspective_changed.emit('M1')
    
    def _on_m2_toggled(self, checked):
        """Handle M2 button toggle."""
        if checked and self.m2_available:
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
        print(f"DEBUG: PerspectiveSwitcher.set_perspective called with: {perspective}")
        print(f"DEBUG: Current _current_perspective before: {self._current_perspective}")
        _logger.debug(f"PerspectiveSwitcher.set_perspective called with: {perspective}")
        _logger.debug(f"Current _current_perspective: {self._current_perspective}")
        if perspective == 'M1' and self.m1_available:
            self._current_perspective = 'M1'
            self.m1_button.setChecked(True)
            # Update visual styling
            self.m1_button.setStyleSheet(self._get_button_style(True))
            self.m2_button.setStyleSheet(self._get_button_style(False))
            # Update line indicators: M1 solid, M2 dashed
            self.m1_line.setStyleSheet("background-color: blue;")
            self.m2_line.setStyleSheet("background-color: transparent; border-top: 3px dashed blue;")
            print(f"DEBUG: Set M1 - m1_button.checked: {self.m1_button.isChecked()}, m2_button.checked: {self.m2_button.isChecked()}")
            # Emit signal to trigger perspective change
            _logger.debug(f"Emitting perspective_changed('M1') from set_perspective")
            self.perspective_changed.emit('M1')
        elif perspective == 'M2' and self.m2_available:
            self._current_perspective = 'M2'
            self.m2_button.setChecked(True)
            # Update visual styling
            self.m1_button.setStyleSheet(self._get_button_style(False))
            self.m2_button.setStyleSheet(self._get_button_style(True))
            # Update line indicators: M2 solid, M1 dashed
            self.m1_line.setStyleSheet("background-color: transparent; border-top: 3px dashed blue;")
            self.m2_line.setStyleSheet("background-color: blue;")
            print(f"DEBUG: Set M2 - m1_button.checked: {self.m1_button.isChecked()}, m2_button.checked: {self.m2_button.isChecked()}")
            # Emit signal to trigger perspective change
            _logger.debug(f"Emitting perspective_changed('M2') from set_perspective")
            self.perspective_changed.emit('M2')
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts."""
        if event.key() == Qt.Key_Tab or event.key() == Qt.Key_Space:
            # Toggle perspective
            if self._current_perspective == 'M1' and self.m2_available:
                self.m2_button.setChecked(True)
            elif self._current_perspective == 'M2' and self.m1_available:
                self.m1_button.setChecked(True)
            event.accept()
        else:
            super().keyPressEvent(event)
