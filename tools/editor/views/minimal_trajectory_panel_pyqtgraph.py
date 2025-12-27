
"""
Minimal, explicit trajectory panel for gamma_self complex plane visualization.
This version is for debugging label/marker issues. All variables and methods are documented.
"""


import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore

class MinimalTrajectoryPanel(QtWidgets.QWidget):
        def set_overlay_trajectory(self, gamma_x, gamma_y):
            """Stub for compatibility: does nothing."""
            pass
    """
    Minimal trajectory panel for plotting gamma_self trajectory and pinned marker labels.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def show_computing(self, flag):
        """Stub for compatibility: does nothing."""
        pass

    def update_trajectory(self, gamma_x, gamma_y, *args, **kwargs):
        """Stub for compatibility: updates the trajectory plot."""
        self.plot_trajectory(gamma_x, gamma_y)

    def set_scenario_name(self, name):
        """Stub for compatibility: sets the scenario name and updates the plot title."""
        self.scenario_name = name
        if hasattr(self, 'plot_widget'):
            self.plot_widget.setTitle(f"{name}, γ_self Trajectory" if name else "γ_self Trajectory")
        self.plot_widget = pg.PlotWidget()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.plot_widget)
        self.trajectory_line = None  # pg.PlotDataItem for the main trajectory
        self.marker_labels = []      # List of pg.TextItem for pinned markers

    def plot_trajectory(self, x_data, y_data):
        """
        Plot the main gamma_self trajectory.
        Args:
            x_data (list or np.ndarray): X coordinates (real part)
            y_data (list or np.ndarray): Y coordinates (imag part)
        """
        if self.trajectory_line:
            self.plot_widget.removeItem(self.trajectory_line)
        self.trajectory_line = self.plot_widget.plot(x_data, y_data, pen='b', symbol=None)

    def clear_marker_labels(self):
        """
        Remove all marker labels from the plot.
        """
        for label in self.marker_labels:
            self.plot_widget.removeItem(label)
        self.marker_labels.clear()

    def add_marker_label(self, x, y, label_text, color='red'):
        """
        Add a text label at (x, y) to the plot.
        Args:
            x (float): X coordinate
            y (float): Y coordinate
            label_text (str): Text to display
            color (str or QColor): Text color
        """
        text_item = pg.TextItem(text=label_text, color=color, anchor=(0, 1))
        text_item.setPos(x, y)
        self.plot_widget.addItem(text_item)
        self.marker_labels.append(text_item)

    def set_pinned_markers(self, markers):
        """
        Add all pinned marker labels from a list of marker dicts.
        Args:
            markers (list of dict): Each dict must have 'x', 'y', 'label', and optionally 'color'.
        """
        self.clear_marker_labels()
        for marker in markers:
            self.add_marker_label(
                x=marker['x'],
                y=marker['y'],
                label_text=marker['label'],
                color=marker.get('color', 'red')
            )
