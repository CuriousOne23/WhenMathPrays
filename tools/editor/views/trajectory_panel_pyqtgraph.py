"""
PyQtGraph-based trajectory panel for gamma_self complex plane visualization.

Clean, fast implementation using Qt Signals for event communication.
"""

import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor
from tools.editor.editor_constants import (
    MARKER_SIZE_TRAJECTORY_START, MARKER_SIZE_TRAJECTORY_END, MARKER_SIZE_MODIFIED,
    MARKER_SIZE_ATTRACTOR, MARKER_SIZE_PINNED, MARKER_SIZE_DIAGNOSTIC, MARKER_SIZE_BASELINE,
    LINE_WIDTH_TRAJECTORY, LINE_WIDTH_MODIFIED_MARKER, LINE_WIDTH_NORMAL_MARKER,
    LINE_WIDTH_LABEL_BORDER, PLOT_PADDING_NONE
)


class TrajectoryPanelPyQtGraph(QWidget):
    """
    High-performance trajectory panel using PyQtGraph.
    
    Displays gamma_self trajectory in complex plane with:
    - Trajectory line
    - Start/end markers
    - Pinned event markers with labels
    - Preview marker during drag operations
    - Click detection for gamma_self readout
    
    Signals:
        gamma_clicked(float, float): Emitted when user clicks on plot, provides (x, y) coordinates
    """
    
    # Qt Signals - Clean event communication
    gamma_clicked = Signal(float, float)  # x, y coordinates when clicked
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')  # White background
        
        # Configure axes
        self.plot_widget.setLabel('left', 'Imaginary (Hate ↔ Love)', units='')
        self.plot_widget.setLabel('bottom', 'Real (Ego ↔ We)', units='')
        self.plot_widget.setTitle('γ_self Trajectory')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        
        # Store name for title updates (will be set when loading data)
        self.scenario_name = ''
        
        # Enable mouse interaction - right-click drag to pan, scroll to zoom
        self.plot_widget.setMouseEnabled(x=True, y=True)
        # Set pan mode: left-click disabled (for gamma readout), right-click for pan
        view_box = self.plot_widget.getViewBox()
        view_box.setMouseMode(pg.ViewBox.PanMode)  # Enable pan/zoom mode
        
        # Create trajectory line
        self.trajectory_line = pg.PlotCurveItem(
            pen=pg.mkPen(color='b', width=LINE_WIDTH_TRAJECTORY),
            name='Trajectory'
        )
        self.plot_widget.addItem(self.trajectory_line)
        
        # Create start marker (green triangle pointing right)
        self.start_marker = pg.ScatterPlotItem(
            size=MARKER_SIZE_TRAJECTORY_START,
            pen=pg.mkPen('g', width=LINE_WIDTH_MODIFIED_MARKER),
            brush=pg.mkBrush('g'),
            symbol='t1',  # Triangle pointing right
            name='Start'
        )
        self.plot_widget.addItem(self.start_marker)
        
        # Create end marker (red square)
        self.end_marker = pg.ScatterPlotItem(
            size=MARKER_SIZE_TRAJECTORY_END,
            pen=pg.mkPen('r', width=LINE_WIDTH_MODIFIED_MARKER),
            brush=pg.mkBrush('r'),
            symbol='s',  # Square
            name='End'
        )
        self.plot_widget.addItem(self.end_marker)
        
        # Create pinned event markers (small dots)
        self.event_markers = pg.ScatterPlotItem(
            size=MARKER_SIZE_MODIFIED,
            pen=pg.mkPen('k', width=LINE_WIDTH_NORMAL_MARKER),
            brush=pg.mkBrush(100, 100, 255, 200),  # Light blue
            symbol='o',
            name='Events'
        )
        self.plot_widget.addItem(self.event_markers)
        
        # Create inserted event markers (black diamonds)
        self.inserted_markers = pg.ScatterPlotItem(
            size=MARKER_SIZE_BASELINE,
            pen=pg.mkPen('k', width=LINE_WIDTH_MODIFIED_MARKER),
            brush=pg.mkBrush('k'),
            symbol='d',  # Diamond
            name='Inserted'
        )
        self.plot_widget.addItem(self.inserted_markers)
        
        # Create preview marker (hollow orange circle)
        self.preview_marker = pg.ScatterPlotItem(
            size=MARKER_SIZE_PINNED,
            pen=pg.mkPen('orange', width=3),
            brush=None,  # Hollow
            symbol='o',
            name='Preview'
        )
        self.plot_widget.addItem(self.preview_marker)
        self.preview_marker.setVisible(False)
        
        # Create diagnostic marker (black X)
        self.diagnostic_marker = pg.ScatterPlotItem(
            size=MARKER_SIZE_DIAGNOSTIC,
            pen=pg.mkPen('k', width=3),
            brush=None,
            symbol='x',
            name='Diagnostic'
        )
        self.plot_widget.addItem(self.diagnostic_marker)
        self.diagnostic_marker.setVisible(False)
        
        # Text items for labels
        self.marker_labels = []  # List of TextItem objects
        self.preview_label = None  # TextItem for preview
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
        
        # Connect click events
        self.plot_widget.scene().sigMouseClicked.connect(self._on_mouse_clicked)
        
        # Store view limits for reset
        self.original_xlim = None
        self.original_ylim = None
        self.manual_xlim = None
        self.manual_ylim = None
    
    def set_scenario_name(self, name: str):
        """Update the title with scenario name."""
        self.scenario_name = name
        if name:
            # TODO: Add bold/fade styling when active/inactive
            title = f"{name}, γ_self Trajectory"
        else:
            title = "γ_self Trajectory"
        self.plot_widget.setTitle(title)
    
    def place_diagnostic_marker(self, gamma_x: float, gamma_y: float):
        """Place diagnostic marker at specified gamma_self coordinates and adjust view if needed."""
        self.diagnostic_marker.setData([gamma_x], [gamma_y])
        self.diagnostic_marker.setVisible(True)
        print(f"[DIAGNOSTIC] Placed trajectory marker at ({gamma_x:.2f}, {gamma_y:.2f})")
        
        # Check if marker is outside current view and adjust if needed
        view_range = self.plot_widget.viewRange()
        x_min, x_max = view_range[0]
        y_min, y_max = view_range[1]
        
        # If marker is outside view, expand view to include it with margin
        needs_adjustment = False
        new_x_min, new_x_max = x_min, x_max
        new_y_min, new_y_max = y_min, y_max
        
        margin_x = (x_max - x_min) * 0.1  # 10% margin
        margin_y = (y_max - y_min) * 0.1
        
        if gamma_x < x_min:
            new_x_min = gamma_x - margin_x
            needs_adjustment = True
        elif gamma_x > x_max:
            new_x_max = gamma_x + margin_x
            needs_adjustment = True
            
        if gamma_y < y_min:
            new_y_min = gamma_y - margin_y
            needs_adjustment = True
        elif gamma_y > y_max:
            new_y_max = gamma_y + margin_y
            needs_adjustment = True
        
        if needs_adjustment:
            print(f"[DIAGNOSTIC] Adjusting view to include marker: x:[{new_x_min:.1f}, {new_x_max:.1f}], y:[{new_y_min:.1f}, {new_y_max:.1f}]")
            self.plot_widget.setXRange(new_x_min, new_x_max, padding=0)
            self.plot_widget.setYRange(new_y_min, new_y_max, padding=0)
    
    def clear_diagnostic_marker(self):
        """Remove diagnostic marker from trajectory."""
        self.diagnostic_marker.setVisible(False)
        print(f"[DIAGNOSTIC] Cleared trajectory marker")
        
    def update_trajectory(self, gamma_x, gamma_y, marked_data=None, pinned_markers=None, 
                         preview_gamma=None, preserve_view=False, inserted_events=None):
        """
        Update trajectory display.
        
        Args:
            gamma_x: Array of real components
            gamma_y: Array of imaginary components  
            marked_data: Dict[event_idx, set of primitives] (not used in this view)
            pinned_markers: List of marker dicts with 'event_idx', 'primitive', 'x', 'y', 'color', 'label'
            preview_gamma: (x, y) tuple for preview marker during drag
            preserve_view: If True, maintain current zoom/pan
            inserted_events: List of inserted event dicts (not used yet)
        """
        if len(gamma_x) == 0:
            return
        
        # Store current view if preserving
        stored_xlim = None
        stored_ylim = None
        if preserve_view:
            view_range = self.plot_widget.viewRange()
            stored_xlim = view_range[0]
            stored_ylim = view_range[1]
        
        # Update trajectory line
        self.trajectory_line.setData(gamma_x, gamma_y)
        
        # Update start/end markers
        self.start_marker.setData([gamma_x[0]], [gamma_y[0]])
        self.end_marker.setData([gamma_x[-1]], [gamma_y[-1]])
        
        # Clear old labels
        for label in self.marker_labels:
            self.plot_widget.removeItem(label)
        self.marker_labels.clear()
        
        # Update pinned markers
        if pinned_markers:
            marker_xs = [m['x'] for m in pinned_markers]
            marker_ys = [m['y'] for m in pinned_markers]
            self.event_markers.setData(marker_xs, marker_ys)
            
            # Add labels for pinned markers
            for marker in pinned_markers:
                label_text = marker.get('label', '')
                if label_text:
                    color = QColor(marker.get('color', 'blue'))
                    text_item = pg.TextItem(
                        text=label_text,
                        color=color,
                        anchor=(0, 1),  # Bottom-left anchor
                        border=pg.mkPen(color, width=1.5),
                        fill=pg.mkBrush(255, 255, 255, 230)
                    )
                    text_item.setPos(marker['x'], marker['y'])
                    self.plot_widget.addItem(text_item)
                    self.marker_labels.append(text_item)
        else:
            self.event_markers.setData([], [])
        
        # Update inserted event markers (black diamonds)
        if inserted_events:
            inserted_xs = [evt['x'] for evt in inserted_events]
            inserted_ys = [evt['y'] for evt in inserted_events]
            self.inserted_markers.setData(inserted_xs, inserted_ys)
        else:
            self.inserted_markers.setData([], [])
        
        # Update preview marker
        if preview_gamma:
            self.preview_marker.setData([preview_gamma[0]], [preview_gamma[1]])
            self.preview_marker.setVisible(True)
            
            # Add preview label
            if self.preview_label:
                self.plot_widget.removeItem(self.preview_label)
            
            label_text = f"γ: {preview_gamma[0]:.1f} + {preview_gamma[1]:.1f}i"
            self.preview_label = pg.TextItem(
                text=label_text,
                color='orange',
                anchor=(0, 1),
                border=pg.mkPen('orange', width=2),
                fill=pg.mkBrush(255, 255, 255, 240)
            )
            self.preview_label.setPos(preview_gamma[0], preview_gamma[1])
            self.plot_widget.addItem(self.preview_label)
            self.marker_labels.append(self.preview_label)
        else:
            self.preview_marker.setVisible(False)
            if self.preview_label:
                self.plot_widget.removeItem(self.preview_label)
                self.preview_label = None
        
        # Handle view limits
        if preserve_view and stored_xlim is not None and stored_ylim is not None:
            # Restore preserved view (maintain user's zoom/pan)
            self.plot_widget.setXRange(stored_xlim[0], stored_xlim[1], padding=0)
            self.plot_widget.setYRange(stored_ylim[0], stored_ylim[1], padding=0)
        elif not preserve_view and not self.manual_xlim and not self.manual_ylim:
            # Auto-scale with padding ONLY when not preserving view
            margin = 2.0
            x_min, x_max = min(gamma_x) - margin, max(gamma_x) + margin
            y_min, y_max = min(gamma_y) - margin, max(gamma_y) + margin
            
            # Ensure axes include origin
            x_min = min(x_min, -1)
            x_max = max(x_max, 1)
            y_min = min(y_min, -1)
            y_max = max(y_max, 1)
            
            self.plot_widget.setXRange(x_min, x_max, padding=0)
            self.plot_widget.setYRange(y_min, y_max, padding=0)
            
            # Store as original view
            if self.original_xlim is None:
                self.original_xlim = (x_min, x_max)
                self.original_ylim = (y_min, y_max)
    
    def _on_mouse_clicked(self, event):
        """Handle mouse click and double-click events."""
        if event.button() == Qt.LeftButton:
            # Get position in data coordinates
            pos = self.plot_widget.plotItem.vb.mapSceneToView(event.scenePos())
            x, y = pos.x(), pos.y()
            
            # Check if this is a double-click
            if event.double():
                print(f"[TRAJECTORY DOUBLE-CLICK] at ({x:.2f}, {y:.2f})")
                # Double-click emits the same signal - controller can distinguish if needed
                self.gamma_clicked.emit(x, y)
            else:
                # Single click - emit signal with coordinates
                print(f"[TRAJECTORY CLICK] Emitting gamma_clicked signal: ({x:.2f}, {y:.2f})")
                self.gamma_clicked.emit(x, y)
    
    def reset_view(self):
        """Reset view to original auto-scaled limits."""
        if self.original_xlim and self.original_ylim:
            self.plot_widget.setXRange(self.original_xlim[0], self.original_xlim[1], padding=0)
            self.plot_widget.setYRange(self.original_ylim[0], self.original_ylim[1], padding=0)
            self.manual_xlim = None
            self.manual_ylim = None
    
    def zoom_in(self):
        """Zoom in by 20% around current center."""
        view_range = self.plot_widget.viewRange()
        x_min, x_max = view_range[0]
        y_min, y_max = view_range[1]
        
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        x_range = (x_max - x_min) * 0.8 / 2  # 20% zoom in
        y_range = (y_max - y_min) * 0.8 / 2
        
        self.plot_widget.setXRange(x_center - x_range, x_center + x_range, padding=0)
        self.plot_widget.setYRange(y_center - y_range, y_center + y_range, padding=0)
    
    def zoom_out(self):
        """Zoom out by 20% around current center."""
        view_range = self.plot_widget.viewRange()
        x_min, x_max = view_range[0]
        y_min, y_max = view_range[1]
        
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        x_range = (x_max - x_min) * 1.25 / 2  # 20% zoom out
        y_range = (y_max - y_min) * 1.25 / 2
        
        self.plot_widget.setXRange(x_center - x_range, x_center + x_range, padding=0)
        self.plot_widget.setYRange(y_center - y_range, y_center + y_range, padding=0)
    
    def show_computing(self, computing: bool):
        """Show/hide computing indicator (compatibility method)."""
        # Could add a text overlay or spinner if needed
        pass
    
    def update_start_marker_style(self, is_modified: bool):
        """Update start marker appearance based on gamma_self_0 modification status."""
        if is_modified:
            # Modified: Orange square
            self.start_marker.setSymbol('s')
            self.start_marker.setPen(pg.mkPen('orange', width=2))
            self.start_marker.setBrush(pg.mkBrush('orange'))
        else:
            # Baseline: Green triangle
            self.start_marker.setSymbol('t1')
            self.start_marker.setPen(pg.mkPen('g', width=2))
            self.start_marker.setBrush(pg.mkBrush('g'))


# ==========================================
# STANDALONE TEST
# ==========================================
if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication, QLabel, QHBoxLayout
    import sys
    import time
    
    app = QApplication(sys.argv)
    
    # Create test window with panel and gauge
    test_widget = QWidget()
    test_widget.setWindowTitle("PyQtGraph Trajectory Panel Test")
    test_widget.resize(900, 600)
    
    layout = QHBoxLayout()
    
    # Create trajectory panel
    panel = TrajectoryPanelPyQtGraph()
    layout.addWidget(panel, stretch=3)
    
    # Create gauge display
    gauge = QLabel("Click on plot")
    gauge.setAlignment(Qt.AlignCenter)
    gauge.setStyleSheet(
        'background-color: lightblue; '
        'border: 2px solid blue; '
        'border-radius: 8px; '
        'padding: 20px; '
        'font-size: 14pt; '
        'font-weight: bold;'
    )
    gauge.setFixedWidth(200)
    layout.addWidget(gauge, stretch=1)
    
    test_widget.setLayout(layout)
    
    # Connect click signal to gauge
    def update_gauge(x, y):
        gauge.setText(f"{x:.2f} + {y:.2f}i")
        print(f"[TEST] Gauge updated: {x:.2f} + {y:.2f}i")
    
    panel.gamma_clicked.connect(update_gauge)
    
    # Generate test trajectory (spiral)
    print("[TEST] Generating spiral trajectory with 500 points...")
    t0 = time.time()
    
    n_points = 500
    t = np.linspace(0, 4*np.pi, n_points)
    gamma_x = t * np.cos(t) * 10
    gamma_y = t * np.sin(t) * 20 + 50
    
    # Create some pinned markers
    pinned_markers = [
        {'x': gamma_x[100], 'y': gamma_y[100], 'color': '#1f77b4', 'label': '100/v'},
        {'x': gamma_x[200], 'y': gamma_y[200], 'color': '#ff7f0e', 'label': '200/r'},
        {'x': gamma_x[300], 'y': gamma_y[300], 'color': '#2ca02c', 'label': '300/f'},
    ]
    
    # Simulate preview marker
    preview_gamma = (gamma_x[400], gamma_y[400])
    
    # Update display
    panel.update_trajectory(gamma_x, gamma_y, pinned_markers=pinned_markers, preview_gamma=preview_gamma)
    
    elapsed = (time.time() - t0) * 1000
    print(f"[TEST] Rendered {n_points} points in {elapsed:.1f}ms")
    
    # Test start marker modification
    panel.update_start_marker_style(is_modified=True)
    
    test_widget.show()
    
    print("\n" + "="*60)
    print("TEST INSTRUCTIONS:")
    print("="*60)
    print("1. You should see a spiral trajectory with 500 points")
    print("2. Three pinned markers with labels (100/v, 200/r, 300/f)")
    print("3. One preview marker (hollow orange) with label")
    print("4. Click anywhere on the plot")
    print("5. The gauge on the right should update with coordinates")
    print("6. Zoom with mouse wheel, pan by dragging")
    print("="*60 + "\n")
    
    sys.exit(app.exec())
