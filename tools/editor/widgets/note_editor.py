"""
Note Editor Widget

Widget for editing event notes tied to specific time markers.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Signal


class NoteEditor(QWidget):
    """
    Widget for editing notes for events.
    
    Notes are tied to event time, not individual primitives.
    
    Signals:
        note_changed(float, str): Emitted when note is changed (event_time, note_text)
    """
    
    note_changed = Signal(float, str)
    
    def __init__(self):
        super().__init__()
        
        self.current_event_time = None  # Track which event we're editing
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Create UI layout."""
        layout = QVBoxLayout()
        
        # Title label
        title_layout = QHBoxLayout()
        title = QLabel("Event Notes")
        title.setStyleSheet("font-weight: bold; font-size: 10pt;")
        
        self.time_label = QLabel("")
        self.time_label.setStyleSheet("color: #666; font-size: 9pt;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(self.time_label)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # Text editor
        self.note_edit = QTextEdit()
        self.note_edit.setPlaceholderText("Click on a marker to view/edit notes...")
        self.note_edit.setMaximumHeight(120)
        self.note_edit.setEnabled(False)
        
        layout.addWidget(self.note_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self._on_apply)
        self.apply_btn.setEnabled(False)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self._on_clear)
        self.clear_btn.setEnabled(False)
        
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def set_event(self, event_time: float, note_text: str = ""):
        """
        Set the event to edit.
        
        Args:
            event_time: Time of the event
            note_text: Current note text for this event
        """
        self.current_event_time = event_time
        self.time_label.setText(f"(Time: {event_time})")
        self.note_edit.setPlainText(note_text)
        self.note_edit.setEnabled(True)
        self.apply_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
    
    def clear_event(self):
        """Clear the current event selection."""
        self.current_event_time = None
        self.time_label.setText("")
        self.note_edit.setPlainText("")
        self.note_edit.setEnabled(False)
        self.apply_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
    
    def _on_apply(self):
        """Handle apply button click."""
        if self.current_event_time is not None:
            note_text = self.note_edit.toPlainText().strip()
            self.note_changed.emit(self.current_event_time, note_text)
    
    def _on_clear(self):
        """Handle clear button click."""
        self.note_edit.clear()
        if self.current_event_time is not None:
            self.note_changed.emit(self.current_event_time, "")
    
    def get_current_note(self) -> str:
        """
        Get the current note text.
        
        Returns:
            Current note text
        """
        return self.note_edit.toPlainText().strip()
