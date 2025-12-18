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
from ..debug_config import get_logger

_logger = get_logger('trajectory_panel')


class TrajectoryPanelPyQtGraph(QWidget):

	panel_ready = Signal()
	gamma_clicked = Signal(object)  # Add this signal for compatibility

	def place_diagnostic_marker(self, x, y, label_text="Diag", color="magenta"):
		"""
		Place a diagnostic marker at the specified (x, y) position.
		Clears previous diagnostic markers and adds a new one (cross symbol and label).
		"""
		# Remove previous diagnostic marker if it exists
		if hasattr(self, '_diagnostic_marker') and self._diagnostic_marker is not None:
			self.plot_widget.removeItem(self._diagnostic_marker)
			self._diagnostic_marker = None
		# Add new marker (cross symbol)
		marker = pg.ScatterPlotItem([x], [y], symbol='x', size=16, pen=pg.mkPen(color, width=2), brush=pg.mkBrush(color))
		self.plot_widget.addItem(marker)
		self._diagnostic_marker = marker
		# Add label as before
		self.clear_marker_labels()
		self.add_marker_label(x, y, label_text, color)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.layout = QVBoxLayout(self)
		self.plot_widget = pg.PlotWidget()
		self.plot_widget.showGrid(x=True, y=True)  # Enable grid
		# Disable auto-range from the start
		self.plot_widget.getViewBox().disableAutoRange()
		self.layout.addWidget(self.plot_widget)
		self.trajectory_line = None
		self.overlay_line = None
		self.marker_labels = []
		self.trajectory_label_manager = TrajectoryLabelManager(self.plot_widget)
		self.active_perspective = "M1"  # Default to M1
		self.trajectory_initialized = False  # Track whether trajectory has been initialized
		self.panel_ready.emit()


	def set_initial_view_range(self, gamma_x, gamma_y, padding=0.1):
		"""Set initial view range to properly show the gamma trajectory."""
		if not gamma_x or not gamma_y:
			return
		
		x_min, x_max = min(gamma_x), max(gamma_x)
		y_min, y_max = min(gamma_y), max(gamma_y)
		
		# Add padding
		x_padding = (x_max - x_min) * padding if x_max != x_min else 1.0
		y_padding = (y_max - y_min) * padding if y_max != y_min else 1.0
		
		x_range = [x_min - x_padding, x_max + x_padding]
		y_range = [y_min - y_padding, y_max + y_padding]
		
		self.plot_widget.setRange(xRange=x_range, yRange=y_range, disableAutoRange=True)
		_logger.debug(f"Set initial range: x={x_range}, y={y_range}")

	def set_scenario_name(self, name):
		self.plot_widget.setTitle(f"{name}, γ_self Trajectory" if name else "γ_self Trajectory")

	def set_active_perspective(self, perspective):
		"""Set the active perspective for color coding."""
		self.active_perspective = perspective

	def update_trajectory(self, gamma_x, gamma_y, *args, **kwargs):
		"""
		Update trajectory display with proper initialization handling.
		
		On first call: sets up view range and plots trajectory
		On subsequent calls: updates trajectory data while preserving view
		"""
		# Always plot/update the trajectory data
		self.plot_trajectory(gamma_x, gamma_y, self.active_perspective)
		
		# Handle view setup only on first initialization
		if not self.trajectory_initialized:
			self.set_initial_view_range(gamma_x, gamma_y)
			self.trajectory_initialized = True
		
		# Handle markers (always done)
		pinned_markers = kwargs.get('pinned_markers')
		if pinned_markers is not None:
			self.set_pinned_markers(pinned_markers)

	def plot_trajectory(self, x_data, y_data, active_perspective="M1"):
		# Disable auto-range before any item manipulation
		self.plot_widget.getViewBox().disableAutoRange()
		
		if self.trajectory_line:
			# Update existing line data instead of removing/re-adding to prevent view changes
			self.trajectory_line.setData(x_data, y_data)
			# Update color if perspective changed
			color = 'b' if active_perspective == "M1" else '#006400'  # Dark green for M2
			self.trajectory_line.setPen(pg.mkPen(color, width=2))
		else:
			# Create new line if it doesn't exist
			color = 'b' if active_perspective == "M1" else '#006400'  # Dark green for M2
			self.trajectory_line = self.plot_widget.plot(x_data, y_data, pen=pg.mkPen(color, width=2), symbol=None)

	def set_overlay_trajectory(self, gamma_x, gamma_y, active_perspective="M1"):
		# Disable auto-range before any item manipulation
		self.plot_widget.getViewBox().disableAutoRange()
		
		if self.overlay_line:
			if gamma_x is None or gamma_y is None:
				# Remove overlay if no data
				self.plot_widget.removeItem(self.overlay_line)
				self.overlay_line = None
				return
			# Update existing overlay data instead of removing/re-adding
			self.overlay_line.setData(gamma_x, gamma_y)
			# Update color if perspective changed
			color = '#006400' if active_perspective == "M1" else 'b'  # Dark green for M2 overlay, blue for M1 overlay
			self.overlay_line.setPen(pg.mkPen(color, style=Qt.DashLine, width=2))
		else:
			if gamma_x is None or gamma_y is None:
				return
			# Create new overlay if it doesn't exist
			color = '#006400' if active_perspective == "M1" else 'b'  # Dark green for M2 overlay, blue for M1 overlay
			self.overlay_line = self.plot_widget.plot(gamma_x, gamma_y, pen=pg.mkPen(color, style=Qt.DashLine, width=2))

	def show_computing(self, flag):
		pass

	def clear_marker_labels(self):
		# Disable auto-range before removing items to prevent view changes
		self.plot_widget.getViewBox().disableAutoRange()
		for label in self.marker_labels:
			self.plot_widget.removeItem(label)
		self.marker_labels.clear()

	def add_marker_label(self, x, y, label_text, color='red'):
		# Disable auto-range before adding items to prevent view changes
		self.plot_widget.getViewBox().disableAutoRange()
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

