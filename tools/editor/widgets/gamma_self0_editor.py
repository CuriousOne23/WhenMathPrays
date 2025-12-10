"""
Gamma_self_0 editor widget.

Allows editing initial state position in gamma-space.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QDoubleSpinBox, QPushButton, QGroupBox
)
from PySide6.QtCore import Signal


class GammaSelf0Editor(QWidget):
    """
    Widget for editing initial gamma_self state (γ_self₀).
    
    Signals:
        value_changed: Emitted when user clicks Apply with new complex value
        reset_requested: Emitted when user clicks Reset to CSV Default
    """
    
    value_changed = Signal(complex)  # New gamma_self_0 value
    reset_requested = Signal()
    
    def __init__(self, initial_value: complex = 0+0j):
        """
        Initialize gamma_self_0 editor.
        
        Args:
            initial_value: Initial gamma_self_0 value from CSV
        """
        super().__init__()
        self.original_value = initial_value
        self._setup_ui()
        self.set_value(initial_value)
    
    def _setup_ui(self):
        """Setup widget UI."""
        # Main group box
        group = QGroupBox("Initial State (γ_self₀)")
        layout = QVBoxLayout()
        
        # Real component (Ego ↔ We)
        real_layout = QHBoxLayout()
        real_layout.addWidget(QLabel('Real (Ego ↔ We):'))
        self.real_spinbox = QDoubleSpinBox()
        self.real_spinbox.setRange(-10.0, 10.0)
        self.real_spinbox.setSingleStep(0.1)
        self.real_spinbox.setDecimals(2)
        self.real_spinbox.setMinimumWidth(80)
        real_layout.addWidget(self.real_spinbox)
        real_layout.addStretch()
        layout.addLayout(real_layout)
        
        # Imaginary component (Hate ↔ Love)
        imag_layout = QHBoxLayout()
        imag_layout.addWidget(QLabel('Imag (Hate ↔ Love):'))
        self.imag_spinbox = QDoubleSpinBox()
        self.imag_spinbox.setRange(-10.0, 10.0)
        self.imag_spinbox.setSingleStep(0.1)
        self.imag_spinbox.setDecimals(2)
        self.imag_spinbox.setMinimumWidth(80)
        imag_layout.addWidget(self.imag_spinbox)
        imag_layout.addWidget(QLabel('i'))
        imag_layout.addStretch()
        layout.addLayout(imag_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        apply_btn = QPushButton('Apply')
        apply_btn.setToolTip('Apply new gamma_self_0 and recompute trajectory')
        apply_btn.clicked.connect(self._on_apply)
        button_layout.addWidget(apply_btn)
        
        reset_btn = QPushButton('Reset to CSV Default')
        reset_btn.setToolTip('Restore original gamma_self_0 from CSV file')
        reset_btn.clicked.connect(self._on_reset)
        button_layout.addWidget(reset_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        group.setLayout(layout)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(group)
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def _on_apply(self):
        """Handle Apply button click."""
        new_value = complex(
            self.real_spinbox.value(),
            self.imag_spinbox.value()
        )
        self.value_changed.emit(new_value)
    
    def _on_reset(self):
        """Handle Reset button click."""
        self.set_value(self.original_value)
        self.reset_requested.emit()
    
    def set_value(self, value: complex):
        """
        Set current value in spinboxes.
        
        Args:
            value: Complex gamma_self_0 value
        """
        self.real_spinbox.setValue(value.real)
        self.imag_spinbox.setValue(value.imag)
    
    def get_value(self) -> complex:
        """Get current value from spinboxes."""
        return complex(
            self.real_spinbox.value(),
            self.imag_spinbox.value()
        )
    
    def set_original_value(self, value: complex):
        """
        Update the original CSV value (for reset functionality).
        
        Args:
            value: New original value
        """
        self.original_value = value
