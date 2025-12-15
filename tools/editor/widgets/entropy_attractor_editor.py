"""
Entropy attractor editor widget.

Allows editing the entropy attractor position in gamma-space.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QDoubleSpinBox, QPushButton, QGroupBox
)
from PySide6.QtCore import Signal


class EntropyAttractorEditor(QWidget):
    """
    Widget for editing entropy attractor position (γ_attractor).
    
    The entropy attractor is where gamma_self drifts when relationship
    experiences entropy/decay. Default is -150+0j (deep ego zone).
    
    Signals:
        value_changed: Emitted when user clicks Apply with new complex value
        reset_requested: Emitted when user clicks Reset to Default
    """
    
    value_changed = Signal(complex)  # New entropy target (real=Ego target, imag=Affect target)
    reset_requested = Signal()
    
    DEFAULT_VALUE = -150.0 + 0.0j  # Real: deep Ego, Imag: neutral affect
    
    def __init__(self, initial_value: complex = DEFAULT_VALUE):
        """
        Initialize entropy attractor editor.
        
        Args:
            initial_value: Initial entropy attractor value
        """
        super().__init__()
        self.default_value = self.DEFAULT_VALUE
        self._setup_ui()
        self.set_value(initial_value)
    
    def _setup_ui(self):
        """Setup widget UI."""
        # Main group box
        group = QGroupBox("Entropy Attractor (γ_attractor)")
        layout = QVBoxLayout()
        
        # Description
        desc = QLabel("Target position for entropy drift")
        desc.setStyleSheet("font-style: italic; color: #666;")
        layout.addWidget(desc)
        
        # Real component (Ego ↔ We)
        real_layout = QHBoxLayout()
        real_layout.addWidget(QLabel('Real (Ego ↔ We):'))
        self.real_spinbox = QDoubleSpinBox()
        self.real_spinbox.setRange(-200.0, 200.0)
        self.real_spinbox.setSingleStep(1.0)
        self.real_spinbox.setDecimals(1)
        self.real_spinbox.setMinimumWidth(60)
        real_layout.addWidget(self.real_spinbox)
        real_layout.addStretch()
        layout.addLayout(real_layout)
        
        # Imaginary component (Hate ↔ Love)
        imag_layout = QHBoxLayout()
        imag_layout.addWidget(QLabel('Imag (Hate ↔ Love):'))
        self.imag_spinbox = QDoubleSpinBox()
        self.imag_spinbox.setRange(-100.0, 100.0)
        self.imag_spinbox.setSingleStep(1.0)
        self.imag_spinbox.setDecimals(1)
        self.imag_spinbox.setMinimumWidth(60)
        imag_layout.addWidget(self.imag_spinbox)
        imag_layout.addWidget(QLabel('i'))
        imag_layout.addStretch()
        layout.addLayout(imag_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        apply_btn = QPushButton('Apply')
        apply_btn.setToolTip('Apply new entropy attractor and recompute trajectory')
        apply_btn.clicked.connect(self._on_apply)
        button_layout.addWidget(apply_btn)
        
        reset_btn = QPushButton('Reset to Default')
        reset_btn.setToolTip('Reset to default entropy attractor (-150+0j)')
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
        real = self.real_spinbox.value()
        imag = self.imag_spinbox.value()
        value = complex(real, imag)
        self.value_changed.emit(value)
    
    def _on_reset(self):
        """Handle Reset button click."""
        self.set_value(self.default_value)
        self.reset_requested.emit()
    
    def set_value(self, value: complex):
        """
        Set the entropy attractor value.
        
        Args:
            value: Complex entropy attractor position
        """
        self.real_spinbox.setValue(value.real)
        self.imag_spinbox.setValue(value.imag)
    
    def get_value(self) -> complex:
        """
        Get current entropy attractor value.
        
        Returns:
            Complex entropy attractor position
        """
        return complex(self.real_spinbox.value(), self.imag_spinbox.value())
