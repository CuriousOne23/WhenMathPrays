"""
PyQtGraph-based primitive panel - HIGH PERFORMANCE version.

This is a prototype demonstrating 20-80x faster rendering compared to matplotlib.
Uses Qt's native graphics scene for real-time interactive updates.
"""

import pyqtgraph as pg
from tools.editor.views.trajectory_label_manager import TrajectoryLabelManager
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
from tools.editor.observability import ObservabilityLog

# Import debug configuration
from tools.editor.debug_config import get_logger, DEBUG_SPINBOX

# Get logger for this module
_logger = get_logger('primitive_panel')


class DraggableScatterItem(pg.ScatterPlotItem):
    """
    Custom scatter plot with draggable points.
    Emits signals when points are dragged, released, or double-clicked.
    """
    
    sigPointDragged = Signal(int, float, float)  # index, x, y (during drag)
    sigPointReleased = Signal(int, float, float)  # index, x, y (on release)
    sigPointClicked = Signal(int, float, float)  # index, x, y (on click without drag)
    sigPointCtrlClicked = Signal(int)  # index (Ctrl+Click for deletion)
    sigPointDoubleClicked = Signal(int)  # index (double-click for reset)
    
    def __init__(self, *args, is_diagnostic=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.dragging_idx = None
        self.click_idx = None
        self.did_drag = False
        self.x_data = None
        self.y_data = None
        self.is_diagnostic = is_diagnostic  # Flag to identify diagnostic markers
        self.setAcceptHoverEvents(True)
        # Enable mouse button events
        from PySide6.QtCore import Qt
        self.setAcceptedMouseButtons(Qt.LeftButton)
    
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
        # Check if double-click hits a point
        if ev.button() == Qt.LeftButton:
            pos = ev.pos()
            pts = self.pointsAt(pos)
            if len(pts) > 0:
                idx = pts[0].index()
                self.sigPointDoubleClicked.emit(idx)
                ev.accept()
                return
                
        # If no point hit or not left button, ignore
        ev.ignore()
    
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
                    # _logger.debug(f"CTRL+CLICK: Request to delete event index={idx}")
                    self.sigPointCtrlClicked.emit(idx)
                    ev.accept()
                    return
                
                # Normal click - readout
                if self.x_data is not None and self.y_data is not None:
                    if DEBUG_SPINBOX:
                        pass
                    self.sigPointClicked.emit(idx, self.x_data[idx], self.y_data[idx])
                    if DEBUG_SPINBOX:
                        pass
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
                # _logger.debug(f"DRAG START: index={self.dragging_idx}, time={time.time()-t0:.3f}s")
        elif ev.isFinish():
            if self.dragging_idx is not None:
                if self.did_drag:
                    # Emit release signal with final position after drag
                    # _logger.debug(f"DRAG FINISH: Dragged - emitting sigPointReleased")
                    if self.y_data is not None:
                        self.sigPointReleased.emit(
                            self.dragging_idx,
                            self.x_data[self.dragging_idx],
                            self.y_data[self.dragging_idx]
                        )
                else:
                    # Just a click without drag
                    # _logger.debug(f"DRAG FINISH: No drag - emitting sigPointClicked")
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
                # _logger.debug(f"DRAG MOVE: index={self.dragging_idx}, y={new_y:.1f}, time={time.time()-t0:.3f}s")


class DoubleClickPlotItem(pg.PlotItem):
    """Custom PlotItem that handles double-clicks on scatter points."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scatter_items = {}  # Will be set by parent panel
        self.primitive_reset_requested = None  # Will be set by parent panel

        # Import debugging tools
        try:
            from tools.editor.debug_gui import get_gui_debugger, event_correlation_context
            self._gui_debugger = get_gui_debugger()
        except ImportError:
            self._gui_debugger = None

    def mouseDoubleClickEvent(self, ev):
        """Handle double-click events by checking if they hit scatter points."""
        from tools.editor.debug_config import get_logger
        logger = get_logger('view.double_click')

        # Start event correlation
        correlation_id = None
        if self._gui_debugger:
            correlation_id = self._gui_debugger.event_tracker.start_event(
                'mouse_double_click',
                'DoubleClickPlotItem',
                button=ev.button(),
                pos=ev.pos()
            )

        logger.debug(f"[DOUBLE_CLICK] mouseDoubleClickEvent called, button={ev.button()}, correlation_id={correlation_id}")

        if ev.button() == Qt.LeftButton and self.scatter_items:
            # Get the click position in data coordinates
            pos = self.getViewBox().mapSceneToView(ev.scenePos())
            logger.debug(f"[DOUBLE_CLICK] Scene pos: {ev.scenePos()} -> Data pos: {pos}")

            # Check each scatter item to see if the click hits a point
            for prim, scatter in self.scatter_items.items():
                if scatter is not None:
                    pts = scatter.pointsAt(pos)
                    logger.debug(f"[DOUBLE_CLICK] {prim}: {len(pts)} points at {pos}")

                    if len(pts) > 0:
                        idx = pts[0].index()
                        logger.info(f"[DOUBLE_CLICK] Hit detected: {prim} point {idx} at {pos}")

                        if self.primitive_reset_requested:
                            logger.info(f"[DOUBLE_CLICK] Emitting primitive_reset_requested({idx}, {prim})")

                            # Track signal emission
                            if self._gui_debugger:
                                self._gui_debugger.event_tracker.add_event_step(
                                    correlation_id, 'signal_emit', 'DoubleClickPlotItem',
                                    signal='primitive_reset_requested', args=(idx, prim)
                                )

                            self.primitive_reset_requested.emit(idx, prim)

                            # Mark event as handled
                            if self._gui_debugger:
                                self._gui_debugger.event_tracker.end_event(
                                    correlation_id, "signal_emitted",
                                    primitive=prim, event_index=idx
                                )

                            ev.accept()
                            return
                        else:
                            logger.warning("[DOUBLE_CLICK] primitive_reset_requested signal not connected")
                            if self._gui_debugger:
                                self._gui_debugger.event_tracker.end_event(
                                    correlation_id, "signal_not_connected"
                                )

        # If no scatter point was hit, let the parent handle it
        logger.debug("[DOUBLE_CLICK] No scatter point hit, calling super()")

        if self._gui_debugger:
            self._gui_debugger.event_tracker.end_event(
                correlation_id, "no_hit"
            )

        super().mouseDoubleClickEvent(ev)

    def viewBoxDoubleClicked(self, viewBox):
        """Override to prevent ViewBox auto-ranging on double-click."""
        # Do nothing - prevent auto-ranging
        from tools.editor.debug_config import get_logger
        logger = get_logger('view.double_click')
        logger.debug("[DOUBLE_CLICK] ViewBox double-click suppressed")
        pass

class PrimitivePanelPyQtGraph(QWidget):

    def clear_all_plots(self):
        """Remove only non-essential items (labels, lines, stray markers) from all plots to ensure a clean state, but keep core plot objects (scatter, baseline, overlay, line)."""
        # _logger.debug("CLEAR_ALL_PLOTS: Removing non-essential items from all plots before initial draw.")
        from pyqtgraph import TextItem, InfiniteLine, ROI, LinearRegionItem
        for prim, plot in self.plot_items.items():
            # Keep references to core items
            core_items = set()
            if prim in self.scatter_items:
                core_items.add(self.scatter_items[prim])
            if prim in self.baseline_scatter_items:
                core_items.add(self.baseline_scatter_items[prim])
            if prim in self.overlay_scatter_items:
                core_items.add(self.overlay_scatter_items[prim])
            if prim in self.line_items:
                core_items.add(self.line_items[prim])
            if prim in self.overlay_line_items:
                core_items.add(self.overlay_line_items[prim])
            # Remove only non-core items
            items_to_remove = [item for item in list(plot.items)
                               if item not in core_items and isinstance(item, (TextItem, InfiniteLine, ROI, LinearRegionItem))]
            for item in items_to_remove:
                plot.removeItem(item)
            # _logger.debug(f"CLEAR_ALL_PLOTS: Plot '{prim}' non-essential items cleared. Items now: {len(plot.items)}")

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
    

    # Architectural: signal to indicate panel is fully constructed and ready for updates
    panel_ready = Signal()

    """
    Architectural Visibility:
    ------------------------
    This panel emits explicit StateViewer events for all readiness transitions and for any skipped update_from_model calls due to not-ready state.
    This ensures that even 'trivial' or deeply-buried UI readiness issues are always visible at the architectural/top level.
    All such events are structured and include context for easy tracing and debugging.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # --- Diagnostic/Architectural fields: must be initialized before any method calls ---
        self.diagnostic_markers = {}  # {primitive: DraggableScatterItem}
        self.diagnostic_event_idx = None  # Current diagnostic event index
        self.diagnostic_primitive = None  # Which primitive has the diagnostic marker

        # Architectural: ready flag for update visibility
        self.ready = False

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
        # Trajectory label manager for marker labels
        self.trajectory_label_manager = None  # Will be initialized after plots

        # Create plots and mark ready after complete
        self._create_plots()
        self.ready = True
        _logger.info(f"ARCH: PrimitivePanelPyQtGraph is now ready. diagnostic_markers keys: {list(self.diagnostic_markers.keys())}")
        # Architectural visibility: record ready state in StateViewer
        try:
            from tools.editor.state_viewer import StateViewer
            StateViewer.record(
                operation='panel_ready',
                entity=('PrimitivePanelPyQtGraph',),
                changes={'ready': (False, True)},
                location='primitive_panel_pyqtgraph.py:__init__'
            )
        except Exception as e:
            _logger.error(f"ARCH: StateViewer record failed: {e}")
        self.panel_ready.emit()

    def _init_trajectory_label_manager(self):
        # Assumes self.plot_items is already populated
        # One manager per primitive
        self.trajectory_label_manager = {}
        for prim in self.plot_items:
            self.trajectory_label_manager[prim] = TrajectoryLabelManager(self.plot_items[prim])
        self.modified_labels_m1 = {}  # {(event_time, prim): TextItem} - for M1 modified primitives
        self.modified_labels_m2 = {}  # {(event_time, prim): TextItem} - for M2 modified primitives
        self.current_perspective = 'M1'  # Track current perspective
        self.inserted_lines = []  # List of InfiniteLine objects for inserted events
        self.events_data = None
        self.overlay_events_data = None  # Events for inactive perspective (Phase 3.3)
        self.baseline_values = {}  # {(event_idx, prim): float}
        self.modified_markers = {}  # {event_idx: set of prims}
        
    def _create_plots(self):
        """Create 5 stacked primitive plots."""
        for i, prim in enumerate(PRIMITIVE_NAMES):
            # Remove old items if they exist (prevents infinite accumulation)
            if prim in self.plot_items:
                plot = self.plot_items[prim]
                # Remove old scatter, baseline, overlay, diagnostic_marker if present
                for item_dict in [self.scatter_items, self.baseline_scatter_items, self.overlay_scatter_items, self.diagnostic_markers]:
                    if prim in item_dict:
                        try:
                            plot.removeItem(item_dict[prim])
                        except Exception as e:
                            _logger.warning(f"CLEANUP: Could not remove old item for prim={prim}: {e}")
            # Now create new plot if not already present
            # Create plot
            plot = DoubleClickPlotItem()
            self.graphics_widget.addItem(plot, row=i, col=0)
            plot.setYRange(-10, 10)
            plot.showGrid(y=True, alpha=0.3)
            
            # Reduce y-axis tick font size and width for compact layout
            from PySide6.QtGui import QFont
            axis = plot.getAxis('left')
            axis.setStyle(tickFont=QFont("Arial", 7))
            axis.setWidth(35)  # Narrow left axis area
            # Set label with readable font (shorter labels now)
            label_style = {'color': '#000', 'font-size': '8pt'}
            axis.setLabel(PRIMITIVE_LABELS[prim], **label_style)
            
            # Enable mouse interaction (left-click drag to pan, wheel to zoom)
            plot.setMouseEnabled(x=True, y=True)  # Allow 2D pan/zoom like trajectory panel
            plot.enableAutoRange(axis='y', enable=False)  # Disable auto-range but allow manual zoom
            
            # Disable double-click auto-ranging so scatter items can handle double-clicks
            view_box = plot.getViewBox()
            view_box.enableAutoRange(x=False, y=False)  # Disable auto-range completely
            
            # Override ViewBox double-click to prevent auto-ranging
            def viewbox_double_click_override(ev):
                # print("[VIEWBOX_DOUBLE_CLICK] ViewBox double-click intercepted")
                # Do nothing - prevent auto-ranging
                ev.ignore()
            view_box.mouseDoubleClickEvent = viewbox_double_click_override
            
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
            _logger.debug(f"ADD_ITEM: overlay_scatter: prim={prim}, type={type(overlay_scatter).__name__}")
            plot.addItem(overlay_scatter)
            
            # Create baseline scatter (filled, semi-transparent)
            baseline_scatter = pg.ScatterPlotItem(
                size=MARKER_SIZE_BASELINE,
                pen=pg.mkPen(color, width=LINE_WIDTH_NORMAL_MARKER),
                brush=pg.mkBrush(color.red(), color.green(), color.blue(), 128)
            )
            _logger.debug(f"ADD_ITEM: baseline_scatter: prim={prim}, type={type(baseline_scatter).__name__}")
            plot.addItem(baseline_scatter)
            
            # Create scatter plot (draggable points)
            scatter = DraggableScatterItem(
                size=MARKER_SIZE_BASELINE,
                pen=pg.mkPen('k', width=1.5),
                brush=pg.mkBrush(color)
            )
            scatter.setZValue(10)  # Place above diagnostic markers for click priority
            _logger.debug(f"ADD_ITEM: scatter: prim={prim}, type={type(scatter).__name__}")
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
            scatter.sigPointCtrlClicked.connect(
                lambda idx, p=prim: self._on_point_ctrl_clicked(idx, p)
            )
            scatter.sigPointDoubleClicked.connect(
                lambda idx, p=prim: self._on_point_double_clicked(idx, p)
            )
            
            # Store references
            self.plot_items[prim] = plot
            self.line_items[prim] = line
            self.overlay_line_items[prim] = overlay_line
            self.overlay_scatter_items[prim] = overlay_scatter
            self.scatter_items[prim] = scatter
            self.baseline_scatter_items[prim] = baseline_scatter
            
            # Set up DoubleClickPlotItem attributes
            plot.scatter_items = self.scatter_items
            plot.primitive_reset_requested = self.primitive_reset_requested
            
            # Create diagnostic marker (red diamond, draggable, initially hidden)
            diagnostic_marker = DraggableScatterItem(
                size=MARKER_SIZE_DIAGNOSTIC,
                pen=pg.mkPen('red', width=3),
                brush=pg.mkBrush('red'),
                symbol='d',
                is_diagnostic=True  # Mark as diagnostic so it can be ignored for normal clicks
            )
            diagnostic_marker.setZValue(-1)  # Place below committed markers so they get priority
            _logger.debug(f"ADD_ITEM: diagnostic_marker: prim={prim}, type={type(diagnostic_marker).__name__}")
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

        # Initialize trajectory label managers for each primitive
        self._init_trajectory_label_manager()

        # Set up double-click handling for plots
        for prim, plot in self.plot_items.items():
            if isinstance(plot, DoubleClickPlotItem):
                plot.scatter_items = {prim: self.scatter_items[prim]}
                plot.primitive_reset_requested = self.primitive_reset_requested

        _logger.debug(f"_create_plots complete. diagnostic_markers keys: {list(self.diagnostic_markers.keys())}")
        # _logger.debug(f"_create_plots complete. diagnostic_markers keys: {list(self.diagnostic_markers.keys())}")
    
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
        """Update the name label with scenario name. Ensures name_label is initialized."""
        self.scenario_name = name
        if not hasattr(self, 'name_label') or self.name_label is None:
            self._create_name_label()
        if self.name_label:
            if name:
                self.name_label.setText(name)
                self.name_label.setVisible(True)
            else:
                self.name_label.setVisible(False)
    
    def set_time_unit(self, time_unit: str):
        """Update the time axis label with the appropriate time unit."""
        # Capitalize first letter for display
        display_unit = time_unit.capitalize() if time_unit else 'Time'
        
        # Update the bottom plot's x-axis label
        last_prim = PRIMITIVE_NAMES[-1]  # 'S' is the last plot
        if last_prim in self.plot_items:
            self.plot_items[last_prim].setLabel('bottom', display_unit)
    
    def switch_perspective_labels(self, perspective: str):
        """Hide current perspective labels and show new perspective labels.
        
        Args:
            perspective: 'M1' or 'M2'
        """
        # _logger.debug(f"PRIMITIVE_LABELS: Switching from {self.current_perspective} to {perspective}")
        if perspective == self.current_perspective:
            # _logger.debug(f"PRIMITIVE_LABELS: Already on {perspective}, skipping")
            return
        
        # Hide old perspective labels (remove from plot)
        old_labels = self.modified_labels_m1 if self.current_perspective == 'M1' else self.modified_labels_m2
        # _logger.debug(f"PRIMITIVE_LABELS: Hiding {len(old_labels)} labels for {self.current_perspective}")
        for (event_time, prim), text_item in old_labels.items():
            # _logger.debug(f"REMOVE_ITEM: switch_perspective_labels: prim={prim}, type={type(text_item).__name__}, text='{getattr(text_item, 'toPlainText', lambda: '?')()}', pos={getattr(text_item, 'pos', lambda: '?')()}")
            self.plot_items[prim].removeItem(text_item)
        
        # Show new perspective labels (add to plot)
        new_labels = self.modified_labels_m1 if perspective == 'M1' else self.modified_labels_m2
        # _logger.debug(f"PRIMITIVE_LABELS: Showing {len(new_labels)} labels for {perspective}")
        for (event_time, prim), text_item in new_labels.items():
            # _logger.debug(f"ADD_ITEM: switch_perspective_labels: prim={prim}, type={type(text_item).__name__}, text='{getattr(text_item, 'toPlainText', lambda: '?')()}', pos={getattr(text_item, 'pos', lambda: '?')()}")
            self.plot_items[prim].addItem(text_item)
        
        # Update current perspective
        self.current_perspective = perspective
        
        # Clear scatter items to prevent ghost markers from previous perspective
        # Use both parent clear() and setData() to fully reset the items
        for prim in PRIMITIVE_NAMES:
            # Call parent class clear to reset internal PyQtGraph state
            pg.ScatterPlotItem.clear(self.scatter_items[prim])
            pg.ScatterPlotItem.clear(self.baseline_scatter_items[prim])
            # Then set empty data to ensure DraggableScatterItem's cached arrays are cleared
            self.scatter_items[prim].setData(x=[], y=[])
            self.baseline_scatter_items[prim].setData(x=[], y=[])
            # Also clear diagnostic markers to prevent cross-perspective contamination
            self.diagnostic_markers[prim].setVisible(False)
            self.diagnostic_markers[prim].setData([], [])
            # Clear overlay scatter items (inactive perspective ghosts)
            self.overlay_line_items[prim].setData([], [])
            self.overlay_scatter_items[prim].clear()
            self.overlay_scatter_items[prim].setData([], [])
        
        _logger.debug(f"PRIMITIVE_LABELS: Current perspective now: {self.current_perspective}, all scatter items cleared")
        # _logger.debug(f"PRIMITIVE_LABELS: Current perspective now: {self.current_perspective}, all scatter items cleared")
    
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
        # _logger.debug(f"DIAGNOSTIC: Cleared all markers")
    
    def update_from_model(self, events):
        """
        Update display from model data.
        
        Args:
            events: List of Event objects
        """
        # _logger.debug("Entered update_from_model")
        if not getattr(self, 'ready', False):
            _logger.info("ARCH: update_from_model called before panel ready; skipping update.")
            # Architectural visibility: record skipped update in StateViewer
            try:
                from tools.editor.state_viewer import StateViewer
                StateViewer.record(
                    operation='update_skipped_not_ready',
                    entity=('PrimitivePanelPyQtGraph',),
                    changes={'ready': (False, False), 'event_count': (0, len(events))},
                    location='primitive_panel_pyqtgraph.py:update_from_model'
                )
            except Exception as e:
                _logger.error(f"ARCH: StateViewer record failed: {e}")
            return
        import time
        t0 = time.time()

        # (clear_all_plots temporarily disabled for debugging primitive plot disappearance)
        # self.clear_all_plots()

        # Clear diagnostic markers to prevent ghost images from previous edits or perspective switches
        if not hasattr(self, 'diagnostic_markers') or not self.diagnostic_markers:
            # _logger.debug("update_from_model: diagnostic_markers not initialized or empty, returning early")
            return
        _logger.debug("diagnostic_markers present, continuing")
            # _logger.debug("diagnostic_markers present, continuing")
        for prim in PRIMITIVE_NAMES:
            if prim in self.diagnostic_markers:
                self.diagnostic_markers[prim].setVisible(False)
                self.diagnostic_markers[prim].setData([], [])

        # Also clear scatter items to ensure no ghost markers from previous perspective
        # This is critical for preventing cross-perspective contamination
        for prim in PRIMITIVE_NAMES:
            pg.ScatterPlotItem.clear(self.scatter_items[prim])
            pg.ScatterPlotItem.clear(self.baseline_scatter_items[prim])
            # Explicitly clear baseline data to prevent ghosts
            self.baseline_scatter_items[prim].setData(x=[], y=[])
        
        # Clear baseline values dictionary to prevent cross-perspective contamination
        self.baseline_values = {}
        
        ObservabilityLog.event("primitive_panel_update_start",
                               perspective=self.current_perspective,
                               event_count=len(events),
                               m1_label_count=len(self.modified_labels_m1),
                               m2_label_count=len(self.modified_labels_m2))
        
        self.events_data = events
        
        # Clear old text labels (trajectory markers) using label manager
        if self.trajectory_label_manager:
            for prim, manager in self.trajectory_label_manager.items():
                manager.clear()
        
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
                # _logger.debug(f"ADD_ITEM: line: prim={prim}, type={type(line).__name__}")
                plot.addItem(line)
                self.inserted_lines.append(line)
        
        for prim in PRIMITIVE_NAMES:
            times = np.array([event.time for event in events])
            values = np.array([event.markers[prim].value for event in events])
            _logger.debug(f"setData line_items[{prim}]: times={times}, values={values}")
                        # _logger.debug(f"setData line_items[{prim}]: times={times}, values={values}")
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

            _logger.debug(f"setData scatter_items[{prim}]: x={times}, y={values}, brush={brushes}, pen={pens}")
                        # _logger.debug(f"setData scatter_items[{prim}]: x={times}, y={values}, brush={brushes}, pen={pens}")
            # Update scatter points - setData replaces old data automatically
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
            
            # (Removed auto-range here; handled below only if event count changes)
        
        # Only reset X range if number of events changed (prevents zoom reset on every update)
        if not hasattr(self, '_last_event_count') or self._last_event_count != len(events):
            for prim in PRIMITIVE_NAMES:
                times = np.array([event.time for event in events])
                if len(times) > 0:
                    self.plot_items[prim].setXRange(times.min() - PLOT_X_MARGIN, times.max() + PLOT_X_MARGIN, padding=PLOT_PADDING_NONE)
            self._last_event_count = len(events)

        # Sync labels from marker state (pull pattern - marker is source of truth)
        self._sync_labels_from_markers(events)

        # Do not force all labels visible; label visibility is now managed by the controller
        
        t1 = time.time()
        # _logger.debug(f"PYQTGRAPH: update_from_model: {(t1-t0)*1000:.1f}ms for {len(events)} events")
    
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
            is_modified: Whether marker has been edited (from controller)
        """
        if not self.events_data or event_index >= len(self.events_data):
            return
        
        # Update the data
        self.events_data[event_index].markers[primitive].value = value
        
        # UPDATE: Cache the modified state so marker appearance updates immediately
        self._modified_state[(event_index, primitive)] = is_modified
        
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
        
        # Force visual update
        self.scatter_items[primitive].update()
        
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
        
        # Update label position if it exists for this marker
        event_time = self.events_data[event_index].time
        key = (event_time, primitive)
        modified_labels = self.modified_labels_m1 if self.current_perspective == 'M1' else self.modified_labels_m2
        updated = False
        if key in modified_labels:
            text_item = modified_labels[key]
            text_item.setPos(event_time, value)
            # _logger.debug(f"UPDATE_MARKER: Updated label position for {key} to ({event_time}, {value:.2f})")
            updated = True
        # If not in modified_labels, search for the TextItem in the plot and update its position
        if not updated:
            for item in self.plot_items[primitive].items:
                if type(item).__name__ == 'TextItem':
                    label_text = f"{event_time:.1f}/{primitive}"
                    if hasattr(item, 'toPlainText') and item.toPlainText() == label_text:
                        item.setPos(event_time, value)
                        # _logger.debug(f"UPDATE_MARKER: Fallback: Updated label position for {key} to ({event_time}, {value:.2f})")
                        break

        # After updating, sync label visibility so only the moved marker's label is visible
        self._sync_labels_from_markers(self.events_data)
    
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
        
        if not hasattr(self, 'overlay_line_items') or not hasattr(self, 'overlay_scatter_items'):
            # Defensive: skip if not yet initialized
            return
        if overlay_events is None or len(overlay_events) == 0:
            # Hide overlay - clear first to remove all items
            for prim in PRIMITIVE_NAMES:
                if prim in self.overlay_line_items:
                    self.overlay_line_items[prim].setData([], [])
                if prim in self.overlay_scatter_items:
                    self.overlay_scatter_items[prim].clear()
                    self.overlay_scatter_items[prim].setData([], [])
            return

        # Update overlay with faded/dotted style
        for prim in PRIMITIVE_NAMES:
            if prim not in self.overlay_line_items or prim not in self.overlay_scatter_items:
                continue
            times = np.array([event.time for event in overlay_events])
            values = np.array([event.markers[prim].value for event in overlay_events])

            # Update overlay line (dotted, faded)
            self.overlay_line_items[prim].setData(times, values)

            # Update overlay scatter (faded, non-interactive) - clear first
            self.overlay_scatter_items[prim].clear()
            color = QColor(PRIMITIVE_COLORS[prim])
            self.overlay_scatter_items[prim].setData(
                x=times,
                y=values,
                pen=pg.mkPen(color, width=1, alpha=128),
                brush=pg.mkBrush(color.red(), color.green(), color.blue(), 100)
            )
    
    def _sync_labels_from_markers(self, events):
        """
        Sync label visibility from Marker state (pull pattern).
        Marker is the authoritative source of truth for label visibility.
        View reads marker state and ensures rendering matches.
        """
        # _logger.debug(f"SYNC_LABELS: ===== Starting sync, perspective={self.current_perspective} =====")
        modified_labels = self.modified_labels_m1 if self.current_perspective == 'M1' else self.modified_labels_m2
        
        # Build set of what SHOULD be visible from marker state
        should_be_visible = set()
        for event_idx, event in enumerate(events):
            for prim in ['v', 'r', 'f', 'a', 'S']:
                visible = event.markers[prim].get_label_visible(self.current_perspective)
                # if prim == 'v':
                #     _logger.debug(f"DIAG: view: event_idx={event_idx}, time={event.time}, Visibility get_label_visible={visible}")
                # if prim == 'S':
                #     _logger.debug(f"DIAG[S]: event_idx={event_idx}, time={event.time}, perspective={self.current_perspective}, get_label_visible={visible}, marker_obj={event.markers[prim]}")
                if visible:
                    should_be_visible.add((event.time, prim))
        
        # _logger.debug(f"SYNC_LABELS: should_be_visible = {should_be_visible}")
        # _logger.debug(f"SYNC_LABELS: modified_labels keys BEFORE sync = {set(modified_labels.keys())}")
        
        # Remove labels that shouldn't be visible
        to_remove = []
        for key in modified_labels.keys():
            if key not in should_be_visible:
                to_remove.append(key)
        
        _logger.debug(f"SYNC_LABELS: to_remove = {to_remove}")
            # _logger.debug(f"SYNC_LABELS: to_remove = {to_remove}")
        
        for key in to_remove:
            text_item = modified_labels[key]
            # _logger.debug(f"REMOVE_ITEM: _sync_labels_from_markers: key={key}, type={type(text_item).__name__}, text='{getattr(text_item, 'toPlainText', lambda: '?')()}', pos={getattr(text_item, 'pos', lambda: '?')()}")
            for plot in self.plot_items.values():
                plot.removeItem(text_item)
            del modified_labels[key]

        # After all label add/remove operations:
        # Print all current TextItems on every plot
        for prim, plot in self.plot_items.items():
            text_items = [item for item in plot.items if type(item).__name__ == 'TextItem']
            # _logger.debug(f"LABEL_INVENTORY: Plot '{prim}': {len(text_items)} TextItems")
            for idx, item in enumerate(text_items):
                # _logger.debug(f"LABEL_INVENTORY:   TextItem {idx}: text='{getattr(item, 'toPlainText', lambda: '?')()}', pos={getattr(item, 'pos', lambda: '?')()}, id={id(item)}")
                pass
        # Add labels that should be visible but aren't
        to_add = []
        for event in events:
            for prim in ['v', 'r', 'f', 'a', 'S']:
                if event.markers[prim].get_label_visible(self.current_perspective):
                    key = (event.time, prim)
                    if key not in modified_labels:
                        to_add.append((event.time, prim, event.markers[prim].value))
        
        _logger.debug(f"SYNC_LABELS: to_add = {[(t, p) for t, p, v in to_add]}")
            # _logger.debug(f"SYNC_LABELS: to_add = {[(t, p) for t, p, v in to_add]}")
        
        for event_time, prim, value in to_add:
            # Actually create and add label TextItems for primitive panel markers
            from pyqtgraph import TextItem
            label_text = f"{event_time:.1f}/{prim}"
            text_item = TextItem(label_text, anchor=(0.5, 1.2), color=PRIMITIVE_COLORS[prim])
            text_item.setPos(event_time, value)
            self.plot_items[prim].addItem(text_item)
            modified_labels[(event_time, prim)] = text_item
        
        # _logger.debug(f"SYNC_LABELS: modified_labels keys AFTER sync = {set(modified_labels.keys())}")
        # for key, text_item in modified_labels.items():
        #     _logger.debug(f"SYNC_LABELS: ACTIVE LABEL: key={key}, text='{text_item.toPlainText()}', pos={text_item.pos()}")
        # _logger.debug("SYNC_LABELS: ===== Sync complete =====")
    
    def remove_marker_label(self, event_time, primitive):
        """Remove modified primitive label for a specific event/primitive.
        
        Args:
            event_time: Event time (not index - uses time-based keys)
            primitive: Primitive name ('v', 'r', 'f', 'a', 'S')
        """
        key = (event_time, primitive)
        modified_labels = self.modified_labels_m1 if self.current_perspective == 'M1' else self.modified_labels_m2
        # print(f"[PANEL_REMOVE] remove_marker_label called: key={key}, perspective={self.current_perspective}, key_exists={key in modified_labels}")
        # for k, text_item in modified_labels.items():
        #     print(f"[PANEL_REMOVE] BEFORE REMOVE: key={k}, text='{text_item.toPlainText()}', pos={text_item.pos()}")
        if key in modified_labels:
            text_item = modified_labels[key]
            # print(f"[REMOVE_ITEM] remove_marker_label: prim={primitive}, type={type(text_item).__name__}, text='{getattr(text_item, 'toPlainText', lambda: '?')()}', pos={getattr(text_item, 'pos', lambda: '?')()}")
            self.plot_items[primitive].removeItem(text_item)
            del modified_labels[key]
            # print(f"[PANEL_REMOVE] Successfully removed label for {key}")
        else:
            # print(f"[PANEL_REMOVE] Label not found for {key} (may have already been removed)")
            pass
    
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
        # import traceback
        # print(f"\n{'='*80}")
        # print(f"[LABEL_ADD] _add_marker_label called: time={event_time}, prim={primitive}, value={value:.2f}, perspective={self.current_perspective}")
        # print(f"[LABEL_ADD] Call stack:")
        # for line in traceback.format_stack()[-6:-1]:  # Show last 5 stack frames
        #     print(line.strip())
        # # CRITICAL FIX: Check if this event_time exists in the current perspective's events
        # # This prevents M1 modifications from showing labels in M2 and vice versa
        if self.events_data:
            event_times = [e.time for e in self.events_data]
            if event_time not in event_times:
                # print(f"[LABEL_ADD] Event time {event_time} not in current events, skipping")
                return
        key = (event_time, primitive)
        modified_labels = self.modified_labels_m1 if self.current_perspective == 'M1' else self.modified_labels_m2
        # print(f"[LABEL_ADD] key={key}, exists_in_dict={key in modified_labels}")
        # num_items_before = len(self.plot_items[primitive].items)
        # print(f"[LABEL_ADD] Plot items BEFORE operations: {num_items_before}")
        # print(f"[LABEL_ADD] Plot items types: {[type(item).__name__ for item in self.plot_items[primitive].items]}")
        # text_items_before = [item for item in self.plot_items[primitive].items if isinstance(item, pg.TextItem)]
        # print(f"[LABEL_ADD] TextItem count BEFORE: {len(text_items_before)}")
        # if text_items_before:
        #     for i, item in enumerate(text_items_before):
        #         print(f"[LABEL_ADD]   TextItem {i}: text='{item.toPlainText()}', pos={item.pos()}, id={id(item)}")
        if key in modified_labels:
            old_text = modified_labels[key]
            # print(f"[LABEL_ADD] Removing old label object: {id(old_text)}")
            self.plot_items[primitive].removeItem(old_text)
            # num_items_after_remove = len(self.plot_items[primitive].items)
            # print(f"[LABEL_ADD] Plot items AFTER removal: {num_items_after_remove}")
        text = pg.TextItem(
            text=str(event_time),
            color=PRIMITIVE_COLORS[primitive],
            anchor=(0, 1),
            border=pg.mkPen(PRIMITIVE_COLORS[primitive], width=LINE_WIDTH_LABEL_BORDER),
            fill=pg.mkBrush(255, 255, 255, 200)
        )
        # print(f"[LABEL_ADD] Created new label object: {id(text)}")
        text.setPos(event_time, value)
        # print(f"[ADD_ITEM] _add_marker_label: prim={primitive}, type={type(text).__name__}, text='{text.toPlainText()}', pos={text.pos()}")
        self.plot_items[primitive].addItem(text)
        modified_labels[key] = text
        # num_items_final = len(self.plot_items[primitive].items)
        # print(f"[LABEL_ADD] Plot items AFTER adding: {num_items_final}")
        # text_items_after = [item for item in self.plot_items[primitive].items if isinstance(item, pg.TextItem)]
        # print(f"[LABEL_ADD] TextItem count AFTER: {len(text_items_after)}")
        # if text_items_after:
        #     for i, item in enumerate(text_items_after):
        #         print(f"[LABEL_ADD]   TextItem {i}: text='{item.toPlainText()}', pos={item.pos()}, id={id(item)}")
        # print(f"[LABEL_ADD] Checking ALL plots for TextItems:")
        # for prim_name in ['v', 'r', 'f', 'a', 'S']:
        #     text_items_in_plot = [item for item in self.plot_items[prim_name].items if isinstance(item, pg.TextItem)]
        #     if text_items_in_plot:
        #         print(f"[LABEL_ADD]   Plot '{prim_name}': {len(text_items_in_plot)} TextItems")
        #         for item in text_items_in_plot:
        #             print(f"[LABEL_ADD]     - text='{item.toPlainText()}', pos={item.pos()}")
        # print(f"{'='*80}\n")
    
    def _add_trajectory_marker_label(self, event_idx, primitive, x, y):
        """Add a timestamp label for a trajectory marker (red-bordered markers from trajectory clicks) using the label manager."""
        key = (event_idx, primitive)
        manager = self.trajectory_label_manager[primitive]
        label = manager.add_label(
            key=key,
            text=str(x),
            x=x,
            y=y,
            color='red',
            border_pen=pg.mkPen('red', width=LINE_WIDTH_LABEL_BORDER),
            fill_brush=pg.mkBrush(255, 255, 255, 200)
        )
        # print(f"[TRAJ_LABEL_ADD] event_idx={event_idx}, prim={primitive}, text='{label.toPlainText()}', pos={label.pos()} (x={x}, y={y})")
        # print(f"[TRAJ_LABEL_DICT] manager.all_labels: {list(manager.all_labels().keys())}")
    
    def _create_readouts(self):
        """Create readout displays (primitive readout removed - replaced by spinbox editor)."""
        # Primitive readout removed in v2.4 - now using spinbox editor instead
        self.primitive_readout = None
    
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
                    
                    # print(f"\n[INSERT EVENT] Ctrl+Shift+click at time={clicked_time:.2f}")
                    
                    # Find the nearest existing marker to the click position
                    if self.events_data:
                        times = [e.time for e in self.events_data]
                        
                        # Find nearest marker by calculating distance to each marker
                        distances = [(i, t, abs(t - clicked_time)) for i, t in enumerate(times)]
                        distances.sort(key=lambda x: x[2])  # Sort by distance
                        
                        # Get the nearest marker
                        nearest_idx, nearest_time, _ = distances[0]
                        
                        # Can't insert at first or last event
                        if nearest_idx == 0 or nearest_idx == len(times) - 1:
                            # print(f"[INSERT] Cannot insert at first or last event (nearest={nearest_time})")
                            event.accept()
                            return
                        
                        # Insert a new event at the nearest marker's position
                        # This will shift the nearest marker and all subsequent markers forward
                        insert_time = nearest_time
                        
                        # The command will insert before nearest_idx, which means:
                        # - New event takes position of nearest marker
                        # - Nearest marker and all after it shift forward by delta
                        # - Delta = nearest_time - previous_time
                        prev_time = times[nearest_idx - 1]
                        
                        # print(f"[INSERT] Click at {clicked_time:.1f}, nearest marker at {nearest_time}, prev={prev_time}")
                        # print(f"[INSERT] Will insert at {insert_time}, shifting {nearest_time} and later by delta={nearest_time - prev_time}")
                        
                        # Store insertion time for command to use
                        self.pending_insert_time = insert_time
                        self.event_insert_requested.emit(nearest_idx)
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
                        print(f"[DEBUG] Emitting diagnostic_marker_placed: nearest_idx={nearest_idx}, prim={prim}, clicked_value={clicked_value}")
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
        if DEBUG_SPINBOX:
            _logger.debug(f"index={index}, primitive={primitive}, value={value}")
        # Update readout gauge when user clicks a point
        self._update_readout(index, primitive, value)
        # Emit marker clicked signal for note editor
        if DEBUG_SPINBOX:
            _logger.debug(f"About to emit marker_clicked signal: index={index}, primitive={primitive}")
        self.marker_clicked.emit(index, primitive)
        if DEBUG_SPINBOX:
            _logger.debug("marker_clicked signal emitted")
    
    def _on_point_ctrl_clicked(self, index, primitive):
        """Handle Ctrl+Click event (delete event)."""
        print(f"[CTRL+CLICK] Request to delete event {index} (clicked on '{primitive}' primitive)")
        # Emit delete signal
        self.event_delete_requested.emit(index)
    
    def _on_point_double_clicked(self, index, primitive):
        """Handle double-click event (reset to baseline)."""
        # Emit reset signal
        self.primitive_reset_requested.emit(index, primitive)
    
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
