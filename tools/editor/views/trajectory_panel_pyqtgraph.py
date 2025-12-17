"""
PyQtGraph-based trajectory panel for gamma_self complex plane visualization.
Restored full version for debugging label/marker issues.
"""

import pyqtgraph as pg
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QColor
import numpy as np
from .trajectory_label_manager import TrajectoryLabelManager


class TrajectoryPanelPyQtGraph(QWidget):
	panel_ready = Signal()
	gamma_clicked = Signal(object)  # Add this signal for compatibility

	def __init__(self, parent=None):
		super().__init__(parent)
		self.layout = QVBoxLayout(self)
		self.plot_widget = pg.PlotWidget()
		self.layout.addWidget(self.plot_widget)
		self.trajectory_line = None
		self.overlay_line = None
		self.marker_labels = []
		self.trajectory_label_manager = TrajectoryLabelManager(self.plot_widget)
		self.panel_ready.emit()

	def set_scenario_name(self, name):
		self.plot_widget.setTitle(f"{name}, γ_self Trajectory" if name else "γ_self Trajectory")

	def update_trajectory(self, gamma_x, gamma_y, *args, **kwargs):
		self.plot_trajectory(gamma_x, gamma_y)
		pinned_markers = kwargs.get('pinned_markers')
		if pinned_markers is not None:
			self.set_pinned_markers(pinned_markers)

	def plot_trajectory(self, x_data, y_data):
		if self.trajectory_line:
			self.plot_widget.removeItem(self.trajectory_line)
		self.trajectory_line = self.plot_widget.plot(x_data, y_data, pen='b', symbol=None)

	def set_overlay_trajectory(self, gamma_x, gamma_y):
		if self.overlay_line:
			self.plot_widget.removeItem(self.overlay_line)
		self.overlay_line = self.plot_widget.plot(gamma_x, gamma_y, pen=pg.mkPen('g', style=Qt.DashLine))

	def show_computing(self, flag):
		pass

	def clear_marker_labels(self):
		for label in self.marker_labels:
			self.plot_widget.removeItem(label)
		self.marker_labels.clear()

	def add_marker_label(self, x, y, label_text, color='red'):
		text_item = pg.TextItem(text=label_text, color=color, anchor=(0, 1))
		text_item.setPos(x, y)
		self.plot_widget.addItem(text_item)
		self.marker_labels.append(text_item)

	def set_pinned_markers(self, markers):
		self.clear_marker_labels()
		# Only add marker labels for markers that should be visible
		for marker in markers:
			if marker.get('visible', True):
				self.add_marker_label(
					x=marker['x'],
					y=marker['y'],
					label_text=marker['label'],
					color=marker.get('color', 'red')
				)

