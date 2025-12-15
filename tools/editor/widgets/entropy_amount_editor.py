"""
Entropy amount (ΔS) editor widget.

Allows editing the entropy drift rates per time unit (separate for real and imaginary axes).
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QDoubleSpinBox, QPushButton, QGroupBox
)
from PySide6.QtCore import Signal


class EntropyAmountEditor(QWidget):
    """
    Widget for editing entropy drift rates per time unit (ΔS_real, ΔS_imag).
    
    This controls the rate at which gamma_self drifts toward the
    entropy attractor, with independent rates for real and imaginary axes.
    
    Signals:
        value_changed: Emitted when user clicks Apply with (delS_real, delS_imag) tuple
        reset_requested: Emitted when user clicks Reset to Default
    """
    
    value_changed = Signal(tuple)  # (delS_real, delS_imag)
    reset_requested = Signal()
    
    DEFAULT_VALUE_REAL = 0.02
    DEFAULT_VALUE_REAL = 0.02
    DEFAULT_VALUE_IMAG = 0.02
    
    def __init__(self, initial_real: float = DEFAULT_VALUE_REAL, initial_imag: float = DEFAULT_VALUE_IMAG):
        """
        Initialize entropy amount editor.
        
        Args:
            initial_real: Initial ΔS_real value
            initial_imag: Initial ΔS_imag value
        """
        super().__init__()
        self.default_real = self.DEFAULT_VALUE_REAL
        self.default_imag = self.DEFAULT_VALUE_IMAG
        self._setup_ui()
        self.set_value(initial_real, initial_imag)
    
    def _setup_ui(self):
        """Setup widget UI."""
        # Main group box
        group = QGroupBox("Entropy Decay Rates")
        layout = QVBoxLayout()
        
        # Description (split into two lines for narrow layouts)
        desc = QLabel("Separate decay rates for Real (Ego)\nand Imag (Affect) axes")
        desc.setStyleSheet("font-style: italic; color: #666;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Real axis spinbox
        real_layout = QHBoxLayout()
        real_layout.addWidget(QLabel('ΔS Real (→Ego):'))
        self.spinbox_real = QDoubleSpinBox()
        self.spinbox_real.setRange(0.0, 50.0)
        self.spinbox_real.setSingleStep(0.1)
        self.spinbox_real.setDecimals(2)
        self.spinbox_real.setMinimumWidth(60)
        real_layout.addWidget(self.spinbox_real)
        real_layout.addStretch()
        layout.addLayout(real_layout)
        
        # Imaginary axis spinbox
        imag_layout = QHBoxLayout()
        imag_layout.addWidget(QLabel('ΔS Imag (→Neutral):'))
        self.spinbox_imag = QDoubleSpinBox()
        self.spinbox_imag.setRange(0.0, 50.0)
        self.spinbox_imag.setSingleStep(0.1)
        self.spinbox_imag.setDecimals(2)
        self.spinbox_imag.setMinimumWidth(60)
        imag_layout.addWidget(self.spinbox_imag)
        imag_layout.addStretch()
        layout.addLayout(imag_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        apply_btn = QPushButton('Apply')
        apply_btn.setToolTip('Apply new decay rates and recompute trajectory')
        apply_btn.clicked.connect(self._on_apply)
        button_layout.addWidget(apply_btn)
        
        reset_btn = QPushButton('Reset to Default')
        reset_btn.setToolTip('Reset to default rates (0.02, 0.02)')
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
        real_value = self.spinbox_real.value()
        imag_value = self.spinbox_imag.value()
        self.value_changed.emit((real_value, imag_value))
    
    def _on_reset(self):
        """Handle Reset button click."""
        self.set_value(self.default_real, self.default_imag)
        self.reset_requested.emit()
    
    def set_value(self, real: float, imag: float):
        """
        Set the decay rate values.
        
        Args:
            real: Decay rate for real axis (toward ego)
            imag: Decay rate for imaginary axis (toward neutral)
        """
        self.spinbox_real.setValue(real)
        self.spinbox_imag.setValue(imag)
    
    def get_value(self) -> tuple:
        """
        Get current decay rates.
        
        Returns:
            Tuple of (delS_real, delS_imag)
        """
        return (self.spinbox_real.value(), self.spinbox_imag.value())
