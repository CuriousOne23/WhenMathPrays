"""
PyQtGraph-based primitive panel - HIGH PERFORMANCE version.

This is a prototype demonstrating 20-80x faster rendering compared to matplotlib.
Uses Qt's native graphics scene for real-time interactive updates.
"""

import pyqtgraph as pg
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QColor
import numpy as np

# Import from central constants
from tools.editor.constants import (
    PRIMITIVE_NAMES, PRIMITIVE_LABELS, PRIMITIVE_COLORS,
    is_inserted_event
)
from tools.editor.editor_constants import (
    FLOAT_TOLERANCE, MARKER_SIZE_NORMAL, MARKER_SIZE_BASELINE, MARKER_SIZE_DIAGNOSTIC,
    LINE_WIDTH_MODIFIED_MARKER, LINE_WIDTH_NORMAL_MARKER, LINE_WIDTH_TRAJECTORY,
    LINE_WIDTH_LABEL_BORDER, PLOT_PADDING_NONE, PLOT_X_MARGIN, PRIMITIVE_MIN_VALUE, PRIMITIVE_MAX_VALUE
)


class DraggableScatterItem(pg.ScatterPlotItem):
    """
    Custom scatter plot with draggable points.
    Emits signals when points are dragged, released, or double-clicked.
    """
    
    sigPointDragged = Signal(int, float, float)  # index, x, y (during drag)
    sigPointReleased = Signal(int, float, float)  # index, x, y (on release)
    sigPointClicked = Signal(int, float, float)  # index, x, y (on click without drag)
    sigPointDoubleClicked = Signal(int)  # index
    sigPointCtrlClicked = Signal(int)  # index (Ctrl+Click for deletion)
    
    def __init__(self, *args, is_diagnostic=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.dragging_idx = None
        self.click_idx = None
        self.did_drag = False
        self.x_data = None
        self.y_data = None
        self.is_diagnostic = is_diagnostic  # Flag to identify diagnostic markers
        self.setAcceptHoverEvents(True)
        
    def setData(self, *args, **kwargs):
        """Override to cache x,y arrays for dragging."""
        # Store x,y data for dragging
        if 'x' in kwargs:
            self.x_data = np.array(kwargs['x'])
        if 'y' in kwargs:
            self.y_data = np.array(kwargs['y'])
        super().setData(*args, **kwargs)
    
    def mouseDoubleClickEvent(self, ev):
        """Handle double-click for reset."""
        if ev.button() == Qt.LeftButton:
            pos = ev.pos()
            pts = self.pointsAt(pos)
            if len(pts) > 0:
                idx = pts[0].index()
                self.sigPointDoubleClicked.emit(idx)
                ev.accept()
                return
        super().mouseDoubleClickEvent(ev)
    
    def mouseClickEvent(self, ev):
        """Handle single click for readout or Ctrl+Click for deletion."""
        if ev.button() == Qt.LeftButton:
            pos = ev.pos()
            pts = self.pointsAt(pos)
            if len(pts) > 0:
                idx = pts[0].index()
                
                # Check for Ctrl+Shift+Click (insert event) - don't consume, let scene handle it
                if (ev.modifiers() & Qt.ControlModifier) and (ev.modifiers() & Qt.ShiftModifier):
                    # Don't accept - let it propagate to scene signal for insertion handling
                    super().mouseClickEvent(ev)
                    return
                
                # Check for Ctrl+Click (deletion request) - but NOT Ctrl+Shift+Click
                if (ev.modifiers() & Qt.ControlModifier) and not (ev.modifiers() & Qt.ShiftModifier):
                    print(f"[CTRL+CLICK] Request to delete event index={idx}")
                    self.sigPointCtrlClicked.emit(idx)
                    ev.accept()
                    return
                
                # Normal click - readout
                if self.x_data is not None and self.y_data is not None:
                    print(f"[CLICK EVENT] index={idx}, x={self.x_data[idx]}, y={self.y_data[idx]}")
                    self.sigPointClicked.emit(idx, self.x_data[idx], self.y_data[idx])
                ev.accept()
                return
        super().mouseClickEvent(ev)
        
    def mouseDragEvent(self, ev):
        import time
        t0 = time.time()
        
        if ev.button() != Qt.LeftButton:
            return
            
        if ev.isStart():
            pos = ev.buttonDownPos()
            pts = self.pointsAt(pos)
            if len(pts) > 0:
                self.dragging_idx = pts[0].index()
                self.click_idx = self.dragging_idx
                self.did_drag = False
                ev.accept()
                print(f"[DRAG START] index={self.dragging_idx}, time={time.time()-t0:.3f}s")
        elif ev.isFinish():
            if self.dragging_idx is not None:
                if self.did_drag:
                    # Emit release signal with final position after drag
                    print(f"[DRAG FINISH] Dragged - emitting sigPointReleased")
                    if self.y_data is not None:
                        self.sigPointReleased.emit(
                            self.dragging_idx,
                            self.x_data[self.dragging_idx],
                            self.y_data[self.dragging_idx]
                        )
                else:
                    # Just a click without drag
                    print(f"[DRAG FINISH] No drag - emitting sigPointClicked")
                    if self.y_data is not None:
                        self.sigPointClicked.emit(
                            self.dragging_idx,
                            self.x_data[self.dragging_idx],
                            self.y_data[self.dragging_idx]
                        )
                ev.accept()
                self.dragging_idx = None
                self.click_idx = None
                self.did_drag = False
        else:
            if self.dragging_idx is not None and self.y_data is not None:
                # Get current position in data coordinates
                pos = ev.pos()
                view_pos = self.mapToView(pos)
                
                # Only allow vertical dragging (keep x fixed)
                new_y = view_pos.y()
                
                # Clamp to [-10, 10]
                new_y = max(-10, min(10, new_y))
                
                # Update y position in cached array
                self.y_data[self.dragging_idx] = new_y
                
                # Mark that we actually dragged
                self.did_drag = True
                
                # Redraw with updated data
                super().setData(x=self.x_data, y=self.y_data)
                
                # Emit signal
                self.sigPointDragged.emit(self.dragging_idx, self.x_data[self.dragging_idx], new_y)
                ev.accept()
                print(f"[DRAG MOVE] index={self.dragging_idx}, y={new_y:.1f}, time={time.time()-t0:.3f}s")


class PrimitivePanelPyQtGraph(QWidget):
    """
    PyQtGraph-based primitive panel with 5 plots stacked vertically.
    
    Architecture (Phase 3 refactoring):
    - Pure view component (no model/controller references)
    - Emits signals for user actions
    - Receives data updates via method calls
    - All communication via Qt signals/slots pattern
    
    Signals (OUT - user actions):
        primitive_changed: Emitted when marker is released after drag (commit)
        diagnostic_marker_placed: Emitted when shift+click places diagnostic marker
        primitive_preview_requested: Emitted during marker drag (preview)
        primitive_reset_requested: Emitted when marker is double-clicked (reset to baseline)
    
    Public Methods (IN - display updates):
        update_from_model(events): Refresh all plots from event data
        set_modified_state(state, perspective): Update cached modification state
        set_scenario_name(name): Update scenario display name
        clear_diagnostic_marker(): Remove diagnostic marker
    """
    
    # Signals
    primitive_changed = Signal(int, str, float)  # event_idx, primitive, value
    diagnostic_marker_placed = Signal(int, str, float)  # event_idx, primitive, hypothetical_value
    event_delete_requested = Signal(int)  # event_idx (Ctrl+Click on marker)
    event_insert_requested = Signal(int)  # event_idx (Ctrl+Shift+Click near marker - insert before)
    marker_clicked = Signal(int, str)  # event_idx, primitive (single click to view/edit notes)
    
    # New signals (Phase 1 refactoring - replacing callbacks)
    primitive_preview_requested = Signal(int, str, float)  # event_idx, primitive, value (during drag)
    primitive_reset_requested = Signal(int, str)  # event_idx, primitive (double-click reset)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set white background globally
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        
        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        
        # Create GraphicsLayoutWidget (container for plots)
        self.graphics_widget = pg.GraphicsLayoutWidget()
        self.graphics_widget.setBackground('w')
        self.layout.addWidget(self.graphics_widget)
        
        # Class constants for compatibility with save methods
        self.PRIMITIVE_NAMES = PRIMITIVE_NAMES
        self.PRIMITIVE_LABELS = PRIMITIVE_LABELS
        self.PRIMITIVE_COLORS = PRIMITIVE_COLORS
        
        # Phase 4 cleanup: Callback functions removed (now using signals only)
        # Kept as None for backward compatibility during transition
        self.on_primitive_preview = None
        self.on_primitive_reset = None
        
        # Storage
        self.plot_items = {}  # {prim: PlotItem}
        self.scatter_items = {}  # {prim: DraggableScatterItem}
        self.baseline_scatter_items = {}  # {prim: ScatterPlotItem}
        self.line_items = {}  # {prim: PlotDataItem}
        self.overlay_line_items = {}  # {prim: PlotDataItem} - for inactive perspective (Phase 3.3)
        self.overlay_scatter_items = {}  # {prim: ScatterPlotItem} - for inactive perspective (Phase 3.3)
        self.text_items = {}  # {(event_idx, prim): TextItem} - for trajectory markers
        self.modified_labels = {}  # {(event_time, prim): TextItem} - for modified primitives (time-based keys survive insertion/deletion)
        self.inserted_lines = []  # List of InfiniteLine objects for inserted events
        self.events_data = None
        self.overlay_events_data = None  # Events for inactive perspective (Phase 3.3)
        self.baseline_values = {}  # {(event_idx, prim): float}
        self.modified_markers = {}  # {event_idx: set of prims}
        
        # Readout displays
        self.primitive_readout = None
        self.gamma_self_readout = None
        
        # Store scenario name for display
        self.scenario_name = ''
        self.name_label = None  # Will be created after plots
        
        # Diagnostic marker (shift+click anywhere on primitive plots)
        self.diagnostic_markers = {}  # {primitive: DraggableScatterItem}
        self.diagnostic_event_idx = None  # Current diagnostic event index
        self.diagnostic_primitive = None  # Which primitive has the diagnostic marker
        
        # Phase 3 refactoring: Cache modified state locally (no controller access)
        self._modified_state = {}  # {(event_idx, primitive): bool}
        self._perspective = 'baseline'  # Current perspective ('baseline' or 'original')
        
        # Create 5 plots
        self._create_plots()
        
        # Create readout gauges
        self._create_readouts()
        
        # Set white background
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        
    def _create_plots(self):
        """Create 5 stacked primitive plots."""
        for i, prim in enumerate(PRIMITIVE_NAMES):
            # Create plot
            plot = self.graphics_widget.addPlot(row=i, col=0)
            plot.setLabel('left', PRIMITIVE_LABELS[prim])
            plot.setYRange(-10, 10)
            plot.showGrid(y=True, alpha=0.3)
            
            # Enable mouse interaction (left-click drag to pan, wheel to zoom)
            plot.setMouseEnabled(x=True, y=True)  # Allow 2D pan/zoom like trajectory panel
            plot.enableAutoRange(axis='y', enable=False)  # Disable auto-range but allow manual zoom
            
            # Add zero line
            plot.addLine(y=0, pen=pg.mkPen('k', width=1, style=Qt.SolidLine))
            
            if i == len(PRIMITIVE_NAMES) - 1:
                plot.setLabel('bottom', 'Time')
            else:
                plot.getAxis('bottom').setStyle(showValues=False)
            
            # Create line plot (trajectory between points)
            color = QColor(PRIMITIVE_COLORS[prim])
            line = plot.plot(pen=pg.mkPen(color, width=LINE_WIDTH_TRAJECTORY))
            
            # Create overlay line (inactive perspective - dotted, faded)
            overlay_line = plot.plot(pen=pg.mkPen(color, width=LINE_WIDTH_TRAJECTORY, style=Qt.DotLine), alpha=0.4)
            overlay_line.setZValue(-5)  # Below active data
            
            # Create overlay scatter (inactive perspective - faded, non-interactive)
            overlay_scatter = pg.ScatterPlotItem(
                size=MARKER_SIZE_BASELINE,
                pen=pg.mkPen(color, width=LINE_WIDTH_NORMAL_MARKER, alpha=128),
                brush=pg.mkBrush(color.red(), color.green(), color.blue(), 100)
            )
            overlay_scatter.setZValue(-5)  # Below active data
            plot.addItem(overlay_scatter)
            
            # Create baseline scatter (filled, semi-transparent)
            baseline_scatter = pg.ScatterPlotItem(
                size=MARKER_SIZE_BASELINE,
                pen=pg.mkPen(color, width=LINE_WIDTH_NORMAL_MARKER),
                brush=pg.mkBrush(color.red(), color.green(), color.blue(), 128)
            )
            plot.addItem(baseline_scatter)
            
            # Create scatter plot (draggable points)
            scatter = DraggableScatterItem(
                size=MARKER_SIZE_BASELINE,
                pen=pg.mkPen('k', width=1.5),
                brush=pg.mkBrush(color)
            )
            scatter.setZValue(10)  # Place above diagnostic markers for click priority
            plot.addItem(scatter)
            
            # Connect signals
            scatter.sigPointDragged.connect(
                lambda idx, x, y, p=prim: self._on_point_dragged(idx, p, y)
            )
            scatter.sigPointReleased.connect(
                lambda idx, x, y, p=prim: self._on_point_released(idx, p, y)
            )
            scatter.sigPointClicked.connect(
                lambda idx, x, y, p=prim: self._on_point_clicked(idx, p, y)
            )
            scatter.sigPointDoubleClicked.connect(
                lambda idx, p=prim: self._on_point_double_clicked(idx, p)
            )
            scatter.sigPointCtrlClicked.connect(
                lambda idx, p=prim: self._on_point_ctrl_clicked(idx, p)
            )
            
            # Store references
            self.plot_items[prim] = plot
            self.line_items[prim] = line
            self.overlay_line_items[prim] = overlay_line
            self.overlay_scatter_items[prim] = overlay_scatter
            self.scatter_items[prim] = scatter
            self.baseline_scatter_items[prim] = baseline_scatter
            
            # Create diagnostic marker (black X, draggable, initially hidden)
            diagnostic_marker = DraggableScatterItem(
                size=MARKER_SIZE_DIAGNOSTIC,
                pen=pg.mkPen('k', width=3),
                brush=None,
                symbol='x',
                is_diagnostic=True  # Mark as diagnostic so it can be ignored for normal clicks
            )
            diagnostic_marker.setZValue(-1)  # Place below committed markers so they get priority
            plot.addItem(diagnostic_marker)
            
            # Connect diagnostic marker signals for drag tracking
            diagnostic_marker.sigPointDragged.connect(
                lambda idx, x, y, p=prim: self._on_diagnostic_dragged(idx, p, y)
            )
            diagnostic_marker.sigPointReleased.connect(
                lambda idx, x, y, p=prim: self._on_diagnostic_released(idx, p, y)
            )
            
            self.diagnostic_markers[prim] = diagnostic_marker
        
        # Create readout displays
        self._create_readouts()
        
        # Create name label (at top of panel)
        self._create_name_label()
    
    def _create_name_label(self):
        """Create label to display scenario name."""
        from PySide6.QtWidgets import QLabel
        from PySide6.QtCore import Qt
        
        self.name_label = QLabel('')
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet(
            'font-size: 11pt; '
            'font-weight: normal; '  # TODO: Change to bold when editing
            'color: black; '  # TODO: Change to gray when not editing
            'padding: 3px;'
        )
        self.name_label.setVisible(False)
        # Insert at top of layout (position 0)
        self.layout.insertWidget(0, self.name_label)
        
        # Connect click events using scene signal (like trajectory panel)
        self.graphics_widget.scene().sigMouseClicked.connect(self._on_mouse_clicked)
    
    def set_scenario_name(self, name: str):
        """Update the name label with scenario name."""
        self.scenario_name = name
        if self.name_label:
            if name:
                self.name_label.setText(name)
                self.name_label.setVisible(True)
            else:
                self.name_label.setVisible(False)
    
    def set_modified_state(self, modified_state: dict, perspective: str = 'baseline'):
        """
        Update the cached modified state.
        Phase 3 refactoring: Replaces direct controller.model access.
        
        Args:
            modified_state: Dict of {(event_idx, primitive): bool}
            perspective: Current perspective ('baseline' or 'original')
        """
        self._modified_state = modified_state.copy()
        self._perspective = perspective
    
    def clear_diagnostic_marker(self):
        """Remove diagnostic marker from all plots."""
        for prim in PRIMITIVE_NAMES:
            self.diagnostic_markers[prim].setVisible(False)
            self.diagnostic_markers[prim].setData([], [])
        self.diagnostic_event_idx = None
        self.diagnostic_primitive = None
        print(f"[DIAGNOSTIC] Cleared all markers")
    
    def update_from_model(self, events):
        """
        Update display from model data.
        
        Args:
            events: List of Event objects
        """
        import time
        t0 = time.time()
        
        self.events_data = events
        
        # Clear old text labels (trajectory markers)
        for text_item in self.text_items.values():
            for plot in self.plot_items.values():
                plot.removeItem(text_item)
        self.text_items.clear()
        
        # NOTE: modified_labels uses time-based keys and survives insertion/deletion
        # No need to clear - labels stay valid across structural changes
        
        # Clear old inserted event lines
        for line in self.inserted_lines:
            for plot in self.plot_items.values():
                plot.removeItem(line)
        self.inserted_lines.clear()
        
        # Find inserted events (all primitives = 0)
        inserted_times = []
        for event_idx, event in enumerate(events):
            if is_inserted_event(event, exclude_first_last=True, event_idx=event_idx, total_events=len(events)):
                inserted_times.append(event.time)
        
        # Add vertical dashed lines for inserted events
        for insert_time in inserted_times:
            for plot in self.plot_items.values():
                line = pg.InfiniteLine(
                    pos=insert_time,
                    angle=90,
                    pen=pg.mkPen('k', width=1, style=Qt.DashLine),
                    movable=False
                )
                plot.addItem(line)
                self.inserted_lines.append(line)
        
        for prim in PRIMITIVE_NAMES:
            times = np.array([event.time for event in events])
            values = np.array([event.markers[prim].value for event in events])
            
            # Update line
            self.line_items[prim].setData(times, values)
            
            # Prepare styling based on modifications
            brushes = []
            pens = []
            baseline_times = []
            baseline_values_list = []
            
            color = QColor(PRIMITIVE_COLORS[prim])
            for event_idx, event in enumerate(events):
                # Phase 3 refactoring: Use cached modified state (no controller access)
                is_modified = self._modified_state.get((event_idx, prim), False)
                
                # Check if this is an inserted event (all primitives = 0, not first/last)
                is_inserted = is_inserted_event(event, exclude_first_last=True, event_idx=event_idx, total_events=len(events))
                
                if is_inserted:
                    # Inserted events: Cyan/turquoise fill to indicate "needs editing"
                    brushes.append(pg.mkBrush(0, 200, 200, 180))  # Bright cyan, semi-transparent
                    pens.append(pg.mkPen('k', width=2))
                elif is_modified:
                    # Hollow marker (no fill, thick border)
                    brushes.append(pg.mkBrush(None))
                    pens.append(pg.mkPen(color, width=2))
                    
                    # Show baseline position
                    baseline_val = self.baseline_values.get((event_idx, prim))
                    if baseline_val is not None and abs(baseline_val - event.markers[prim].value) > FLOAT_TOLERANCE:
                        baseline_times.append(event.time)
                        baseline_values_list.append(baseline_val)
                else:
                    # Filled marker
                    brushes.append(pg.mkBrush(color))
                    pens.append(pg.mkPen('k', width=1))
            
            # Update scatter points
            self.scatter_items[prim].setData(
                x=times,
                y=values,
                brush=brushes,
                pen=pens
            )
            
            # Update baseline scatter
            if baseline_times:
                self.baseline_scatter_items[prim].setData(
                    x=np.array(baseline_times),
                    y=np.array(baseline_values_list)
                )
            else:
                self.baseline_scatter_items[prim].setData(x=[], y=[])
            
            # Auto-range on first update
            if len(times) > 0:
                self.plot_items[prim].setXRange(times.min() - PLOT_X_MARGIN, times.max() + PLOT_X_MARGIN, padding=PLOT_PADDING_NONE)
        
        t1 = time.time()
        print(f"[PYQTGRAPH] update_from_model: {(t1-t0)*1000:.1f}ms for {len(events)} events")
    
    def set_baseline_values(self, baseline_values):
        """Store baseline values for showing original positions."""
        self.baseline_values = baseline_values.copy()
    
    def update_marker(self, event_index, primitive, value, is_modified):
        """
        Update a single marker (for compatibility with matplotlib panel interface).
        
        Args:
            event_index: Index of event
            primitive: Primitive name ('v', 'r', 'f', 'a', 'S')
            value: New value
            is_modified: Whether marker has been edited (ignored - queried from model)
        """
        if not self.events_data or event_index >= len(self.events_data):
            return
        
        # Update the data
        self.events_data[event_index].markers[primitive].value = value
        
        # NOTE: We no longer maintain local modified_markers dict.
        # Modification status is queried from controller.model (time-based tracking)
        
        # Rebuild all data for this primitive (fast with PyQtGraph)
        times = np.array([e.time for e in self.events_data])
        values_arr = np.array([e.markers[primitive].value for e in self.events_data])
        
        # Update line
        self.line_items[primitive].setData(times, values_arr)
        
        # Update scatter with proper styling
        brushes = []
        pens = []
        color = QColor(PRIMITIVE_COLORS[primitive])
        for idx in range(len(self.events_data)):
            # Phase 3 refactoring: Use cached modified state (no controller access)
            is_mod = self._modified_state.get((idx, primitive), False)
            if is_mod:
                brushes.append(pg.mkBrush(None))  # Hollow
                pens.append(pg.mkPen(color, width=LINE_WIDTH_MODIFIED_MARKER))
            else:
                brushes.append(pg.mkBrush(color))  # Filled
                pens.append(pg.mkPen('k', width=LINE_WIDTH_NORMAL_MARKER))
        
        self.scatter_items[primitive].setData(x=times, y=values_arr, brush=brushes, pen=pens)
        
        # Update baseline markers
        baseline_times = []
        baseline_values_list = []
        for idx in range(len(self.events_data)):
            # Phase 3 refactoring: Use cached modified state (no controller access)
            is_mod = self._modified_state.get((idx, primitive), False)
            if is_mod:
                baseline_val = self.baseline_values.get((idx, primitive))
                if baseline_val is not None:
                    baseline_times.append(self.events_data[idx].time)
                    baseline_values_list.append(baseline_val)
        
        if baseline_times:
            self.baseline_scatter_items[primitive].setData(
                x=np.array(baseline_times),
                y=np.array(baseline_values_list)
            )
        else:
            self.baseline_scatter_items[primitive].setData(x=[], y=[])
    
    def update_markers(self, marked_data=None):
        """
        Update trajectory marker labels on specified events/primitives.
        These are the labels that show which events were clicked on the trajectory plot.
        
        Args:
            marked_data: Dict {event_idx: set of primitives} or list of event indices
        """
        if not self.events_data:
            return
        
        # Clear old trajectory marker labels
        for text_item in self.text_items.values():
            for plot in self.plot_items.values():
                plot.removeItem(text_item)
        self.text_items.clear()
        
        if not marked_data:
            return
        
        # Add new trajectory marker labels
        if isinstance(marked_data, dict):
            for event_idx, prims in marked_data.items():
                if event_idx >= len(self.events_data):
                    continue
                event = self.events_data[event_idx]
                for prim in prims:
                    self._add_trajectory_marker_label(event_idx, prim, event.time, event.markers[prim].value)
        elif isinstance(marked_data, list):
            for event_idx in marked_data:
                if event_idx >= len(self.events_data):
                    continue
                event = self.events_data[event_idx]
                for prim in PRIMITIVE_NAMES:
                    self._add_trajectory_marker_label(event_idx, prim, event.time, event.markers[prim].value)
    
    def set_overlay_data(self, overlay_events):
        """
        Set overlay data for inactive perspective (Phase 3.3).
        
        Args:
            overlay_events: List of Event objects for inactive perspective (or None to hide)
        """
        self.overlay_events_data = overlay_events
        
        if overlay_events is None or len(overlay_events) == 0:
            # Hide overlay
            for prim in PRIMITIVE_NAMES:
                self.overlay_line_items[prim].setData([], [])
                self.overlay_scatter_items[prim].setData([], [])
            return
        
        # Update overlay with faded/dotted style
        for prim in PRIMITIVE_NAMES:
            times = np.array([event.time for event in overlay_events])
            values = np.array([event.markers[prim].value for event in overlay_events])
            
            # Update overlay line (dotted, faded)
            self.overlay_line_items[prim].setData(times, values)
            
            # Update overlay scatter (faded, non-interactive)
            color = QColor(PRIMITIVE_COLORS[prim])
            self.overlay_scatter_items[prim].setData(
                x=times,
                y=values,
                pen=pg.mkPen(color, width=1, alpha=128),
                brush=pg.mkBrush(color.red(), color.green(), color.blue(), 100)
            )
    
    def remove_marker_label(self, event_time, primitive):
        """Remove modified primitive label for a specific event/primitive.
        
        Args:
            event_time: Event time (not index - uses time-based keys)
            primitive: Primitive name ('v', 'r', 'f', 'a', 'S')
        """
        key = (event_time, primitive)
        if key in self.modified_labels:
            text_item = self.modified_labels[key]
            self.plot_items[primitive].removeItem(text_item)
            del self.modified_labels[key]
    
    @property
    def draggable_points(self):
        """Compatibility property for matplotlib panel interface."""
        # Return empty dict since PyQtGraph doesn't use DraggablePoint objects
        return {}
    
    @property
    def axes(self):
        """Compatibility property for matplotlib panel interface."""
        # Return empty dict since PyQtGraph doesn't use matplotlib axes
        return {}
    
    def _add_marker_label(self, event_time, primitive, value):
        """Add or update a timestamp label to a modified primitive marker.
        
        Args:
            event_time: Event time (not index - uses time-based keys that survive insertion/deletion)
            primitive: Primitive name ('v', 'r', 'f', 'a', 'S')
            value: Primitive value (Y position)
        """
        key = (event_time, primitive)
        
        # Remove old label if it exists
        if key in self.modified_labels:
            old_text = self.modified_labels[key]
            self.plot_items[primitive].removeItem(old_text)
        
        # Create new label with timestamp
        text = pg.TextItem(
            text=str(event_time),
            color=PRIMITIVE_COLORS[primitive],
            anchor=(0, 1),
            border=pg.mkPen(PRIMITIVE_COLORS[primitive], width=LINE_WIDTH_LABEL_BORDER),
            fill=pg.mkBrush(255, 255, 255, 200)
        )
        text.setPos(event_time, value)
        self.plot_items[primitive].addItem(text)
        self.modified_labels[key] = text
    
    def _add_trajectory_marker_label(self, event_idx, primitive, x, y):
        """Add a timestamp label for a trajectory marker (red-bordered markers from trajectory clicks)."""
        key = (event_idx, primitive)
        
        # Create label with red border and timestamp (x is the time)
        text = pg.TextItem(
            text=str(x),
            color='red',
            anchor=(0, 1),
            border=pg.mkPen('red', width=LINE_WIDTH_LABEL_BORDER),
            fill=pg.mkBrush(255, 255, 255, 200)
        )
        text.setPos(x, y)
        self.plot_items[primitive].addItem(text)
        self.text_items[key] = text
    
    def _create_readouts(self):
        """Create readout displays for primitives and gamma_self."""
        from PySide6.QtWidgets import QLabel
        from PySide6.QtCore import Qt
        
        # Create primitive readout label (left side)
        self.primitive_readout = QLabel('')
        self.primitive_readout.setAlignment(Qt.AlignCenter)
        self.primitive_readout.setStyleSheet(
            'background-color: lightyellow; '
            'border: 1px solid black; '
            'border-radius: 5px; '
            'padding: 5px; '
            'font-size: 10pt;'
        )
        self.primitive_readout.setFixedWidth(80)
        self.primitive_readout.setVisible(False)
        self.layout.addWidget(self.primitive_readout)
    
    def _update_readout(self, event_index, primitive, value):
        """Update readout display with timestamp."""
        if self.primitive_readout and self.events_data:
            # Get timestamp from events_data
            if event_index < len(self.events_data):
                timestamp = self.events_data[event_index].time
                marker_id = f"{timestamp}{primitive}"
            else:
                marker_id = f"{event_index}{primitive}"
            self.primitive_readout.setText(f"{marker_id}\n{value:.2f}")
            self.primitive_readout.setVisible(True)
    
    def clear_readout(self):
        """Clear the readout display."""
        if self.primitive_readout:
            self.primitive_readout.setVisible(False)
    
    def _on_mouse_clicked(self, event):
        """Handle mouse clicks using scene signal (like trajectory panel)."""
        # Check for Ctrl+Shift+Click (insert event) first
        if event.button() == Qt.LeftButton and (event.modifiers() & Qt.ControlModifier) and (event.modifiers() & Qt.ShiftModifier):
            # Find which plot was clicked
            for prim, plot in self.plot_items.items():
                if plot.sceneBoundingRect().contains(event.scenePos()):
                    # Get click position in data coordinates
                    view_pos = plot.getViewBox().mapSceneToView(event.scenePos())
                    clicked_time = view_pos.x()
                    
                    print(f"\n[INSERT EVENT] Ctrl+Shift+click at time={clicked_time:.2f}")
                    
                    # Insert new event at calculated position
                    if self.events_data:
                        times = [e.time for e in self.events_data]
                        
                        # Find the markers before and after clicked position
                        markers_before = [(i, t) for i, t in enumerate(times) if t < clicked_time]
                        markers_after = [(i, t) for i, t in enumerate(times) if t > clicked_time]
                        
                        if not markers_before or not markers_after:
                            # Can't insert before first or after last
                            event.accept()
                            return
                        
                        # Get the previous marker (last one before click)
                        prev_idx, prev_time = markers_before[-1]
                        # Get the next marker (first one after click)
                        next_idx, next_time = markers_after[0]
                        
                        # Calculate standard spacing by looking at the gap BEFORE the previous marker
                        # This gives us the "expected" delta in this region
                        if prev_idx > 0:
                            standard_delta = prev_time - times[prev_idx - 1]
                        else:
                            # If previous is first event, use gap to next
                            standard_delta = times[1] - times[0]
                        
                        # New event should be placed at prev_time + standard_delta
                        insert_time = prev_time + standard_delta
                        
                        print(f"[INSERT] Click at {clicked_time:.1f}, prev={prev_time}, next={next_time}")
                        print(f"[INSERT] Standard delta={standard_delta}, insert_time={insert_time}")
                        
                        # Store insertion time for command to use
                        self.pending_insert_time = insert_time
                        self.event_insert_requested.emit(next_idx)
                        event.accept()
                        return
            
            # If we handled Ctrl+Shift+Click but didn't find a valid plot, still consume the event
            event.accept()
            return
        
        # Handle shift+left-click for diagnostic markers
        elif event.button() == Qt.LeftButton and event.modifiers() & Qt.ShiftModifier:
            # Find which plot was clicked
            for prim, plot in self.plot_items.items():
                if plot.sceneBoundingRect().contains(event.scenePos()):
                    # Get click position in data coordinates
                    view_pos = plot.getViewBox().mapSceneToView(event.scenePos())
                    clicked_time = view_pos.x()
                    clicked_value = view_pos.y()
                    
                    # Get view range for context
                    view_range = plot.viewRange()
                    y_min, y_max = view_range[1]
                    
                    print(f"\n[DIAGNOSTIC MARKER] Shift+click at ({clicked_time:.2f}, {clicked_value:.2f})")
                    print(f"  View Y range: [{y_min:.2f}, {y_max:.2f}]")
                    
                    # Find nearest event
                    if self.events_data:
                        times = [e.time for e in self.events_data]
                        nearest_idx = min(range(len(times)), key=lambda i: abs(times[i] - clicked_time))
                        nearest_time = times[nearest_idx]
                        
                        # Get current marker value for reference
                        current_value = self.events_data[nearest_idx].markers[prim].value
                        baseline_val = self.baseline_values.get((nearest_idx, prim))
                        
                        # Clamp clicked Y value to valid range
                        clicked_value = max(-10, min(10, clicked_value))
                        
                        # Clear all previous diagnostic markers
                        self.clear_diagnostic_marker()
                        
                        # Place diagnostic marker at clicked position (snap X to nearest event time)
                        self.diagnostic_markers[prim].setData([nearest_time], [clicked_value])
                        self.diagnostic_markers[prim].setVisible(True)
                        self.diagnostic_event_idx = nearest_idx
                        self.diagnostic_primitive = prim
                        
                        print(f"[DIAGNOSTIC] Placed X marker on '{prim}' at event {nearest_idx} (time={nearest_time:.1f})")
                        print(f"[DIAGNOSTIC]   Clicked at Y={clicked_value:.2f}, Current marker: {current_value:.2f}, Baseline: {baseline_val if baseline_val else 'N/A'}")
                        print(f"[DIAGNOSTIC] Drag the X marker up/down to test hypothetical values")
                        
                        # Emit signal to compute trajectory and update gauges
                        self.diagnostic_marker_placed.emit(nearest_idx, prim, clicked_value)
                        
                        event.accept()
                        return
            
            # If we handled Shift+Click but didn't find a valid plot, still consume the event
            event.accept()
            return
        
        # Consume any other modifier+click combinations to prevent system-level interference
        if event.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier | Qt.AltModifier):
            event.accept()
            return
    
    def reset_view(self):
        """Reset all plots to default view (-10 to 10 on Y, auto on X)."""
        for prim, plot in self.plot_items.items():
            # Auto-range X to fit data first
            plot.enableAutoRange(axis='x', enable=True)
            plot.enableAutoRange(axis='y', enable=False)  # Keep Y fixed
            plot.autoRange()
            plot.enableAutoRange(axis='x', enable=False)
            # Reset Y to default range (do this AFTER autoRange to prevent override)
            plot.setYRange(PRIMITIVE_MIN_VALUE, PRIMITIVE_MAX_VALUE, padding=PLOT_PADDING_NONE)
    
    def zoom_in(self):
        """Zoom in by 20% on all plots around current center."""
        for plot in self.plot_items.values():
            view_range = plot.viewRange()
            x_min, x_max = view_range[0]
            y_min, y_max = view_range[1]
            
            x_center = (x_min + x_max) / 2
            y_center = (y_min + y_max) / 2
            x_range = (x_max - x_min) * 0.8 / 2  # 20% zoom in
            y_range = (y_max - y_min) * 0.8 / 2
            
            plot.setXRange(x_center - x_range, x_center + x_range, padding=0)
            plot.setYRange(y_center - y_range, y_center + y_range, padding=0)
    
    def zoom_out(self):
        """Zoom out by 20% on all plots around current center."""
        for plot in self.plot_items.values():
            view_range = plot.viewRange()
            x_min, x_max = view_range[0]
            y_min, y_max = view_range[1]
            
            x_center = (x_min + x_max) / 2
            y_center = (y_min + y_max) / 2
            x_range = (x_max - x_min) * 1.25 / 2  # 20% zoom out
            y_range = (y_max - y_min) * 1.25 / 2
            
            plot.setXRange(x_center - x_range, x_center + x_range, padding=0)
            plot.setYRange(y_center - y_range, y_center + y_range, padding=0)
    
    def commit_all_previews(self):
        """
        Commit all preview changes (compatibility method).
        
        In PyQtGraph implementation, changes are committed automatically on drag release,
        so this method is a no-op for compatibility with the controller.
        """
        pass
    
    def _on_point_dragged(self, index, primitive, new_value):
        """Handle point drag event (preview)."""
        # Update line in real-time during drag
        if self.events_data:
            times = np.array([e.time for e in self.events_data])
            values = np.array([e.markers[primitive].value for e in self.events_data])
            values[index] = new_value
            self.line_items[primitive].setData(times, values)
        
        # Update readout gauge
        self._update_readout(index, primitive, new_value)
        
        # Emit preview signal (Phase 1 refactoring - parallel with callback)
        self.primitive_preview_requested.emit(index, primitive, new_value)
        
        # Call preview callback if set (kept for backward compatibility during refactoring)
        if self.on_primitive_preview:
            self.on_primitive_preview(index, primitive, new_value)
    
    def _on_point_released(self, index, primitive, new_value):
        """Handle point release event (commit)."""
        # Emit changed signal for undo/redo
        self.primitive_changed.emit(index, primitive, new_value)
    
    def _on_point_clicked(self, index, primitive, value):
        """Handle point click without drag (show readout and emit signal for note editing)."""
        print(f"[CLICK] index={index}, primitive={primitive}, value={value}")
        # Update readout gauge when user clicks a point
        self._update_readout(index, primitive, value)
        # Emit marker clicked signal for note editor
        self.marker_clicked.emit(index, primitive)
    
    def _on_point_double_clicked(self, index, primitive):
        """Handle double-click event (reset to baseline)."""
        print(f"[DOUBLE_CLICK] Requesting reset for index={index}, primitive={primitive}")
        # Emit reset signal - controller will handle undo command creation
        self.primitive_reset_requested.emit(index, primitive)
    
    def _on_point_ctrl_clicked(self, index, primitive):
        """Handle Ctrl+Click event (delete event)."""
        print(f"[CTRL+CLICK] Request to delete event {index} (clicked on '{primitive}' primitive)")
        # Emit delete signal
        self.event_delete_requested.emit(index)
    
    def _on_diagnostic_dragged(self, index, primitive, value):
        """Handle diagnostic marker being dragged - update trajectory in real-time."""
        if self.diagnostic_event_idx is not None and hasattr(self, 'on_diagnostic_marker'):
            # Clamp value to valid range
            clamped_value = max(-10, min(10, value))
            print(f"[DIAGNOSTIC] Dragging '{primitive}' to {clamped_value:.2f}, marker visible={self.diagnostic_markers[primitive].isVisible()}")
            
            # Notify controller to compute hypothetical trajectory
            self.on_diagnostic_marker(self.diagnostic_event_idx, primitive, clamped_value)
    
    def _on_diagnostic_released(self, index, primitive, value):
        """Handle diagnostic marker release - finalize the what-if display."""
        if self.diagnostic_event_idx is not None and hasattr(self, 'on_diagnostic_marker'):
            # Clamp value to valid range
            clamped_value = max(-10, min(10, value))
            print(f"[DIAGNOSTIC] Released '{primitive}' at {clamped_value:.2f}")
            print(f"[DIAGNOSTIC] Hypothetical result displayed. Shift+click elsewhere or press ESC to clear.")
            
            # Final update
            self.on_diagnostic_marker(self.diagnostic_event_idx, primitive, clamped_value)
            
            # Update readout to show hypothetical value
            self._update_readout(self.diagnostic_event_idx, primitive, clamped_value)


# Comparison test
if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys
    
    # Create dummy Event class
    class DummyMarker:
        def __init__(self, value):
            self.value = value
    
    class DummyEvent:
        def __init__(self, time, values):
            self.time = time
            self.markers = {
                prim: DummyMarker(val) 
                for prim, val in zip(PRIMITIVE_NAMES, values)
            }
    
    # Create test data
    import numpy as np
    n_events = 100  # Test with 100 events (500 draggable points!)
    events = []
    for i in range(n_events):
        time = i * 7
        values = np.sin(np.linspace(0, 4*np.pi, n_events))[i] * 5 + np.random.randn(5) * 0.5
        events.append(DummyEvent(time, values))
    
    # Create app and widget
    app = QApplication(sys.argv)
    panel = PrimitivePanelPyQtGraph()
    panel.setWindowTitle(f"PyQtGraph Performance Test ({n_events} events = {n_events*5} points)")
    panel.resize(800, 600)
    
    # Update with test data (this is what takes 4 seconds in matplotlib!)
    panel.update_from_model(events)
    
    panel.show()
    sys.exit(app.exec())
