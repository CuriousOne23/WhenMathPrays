#!/usr/bin/env python3
"""
Interactive Scenario Editor

Visual diagnostic tool for GRP scenario primitives with real-time
gamma_self trajectory preview.

Usage:
    python tools/interactive_editor.py <csv_file>

Example:
    python tools/interactive_editor.py data/single_dating_to_love_M1.csv

Phase 2 Update:
    Migrated to PySide6 for professional UI framework with native
    toolbars, dialogs, and undo/redo support.
"""

import sys
import argparse
from pathlib import Path
from typing import Tuple, Optional

# PySide6 imports
from PySide6.QtWidgets import QApplication, QDockWidget
from PySide6.QtCore import Qt

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.editor.model import EditorModel
from tools.editor.controller import EditorController
from tools.editor.views.primitive_panel_pyqtgraph import PrimitivePanelPyQtGraph
from tools.editor.views.trajectory_panel_pyqtgraph import TrajectoryPanelPyQtGraph
from tools.editor.config import get_config
from tools.editor.qt_window import EditorMainWindow
from tools.editor.widgets import GammaSelf0Editor
from tools.editor.constants import is_inserted_event


def validate_and_resolve_paths(input_path: str) -> Tuple[Optional[Path], Optional[Path], Optional[str], bool]:
    """
    Validate input file and resolve M1/M2 paths.
    
    Returns:
        (m1_path, m2_path, error_message, was_originally_m2)
        - m1_path: Path to M1 file (None if not found)
        - m2_path: Path to M2 file (None if not found)
        - error_message: Error string if validation failed, None if successful
        - was_originally_m2: True if user loaded M2-only file (to set initial perspective)
    
    Handles:
        - User loads M1 → looks for M2
        - User loads M2 → looks for M1
        - User loads M2 with no M1 → treat M2 as M1
        - Invalid file extension → error
        - File not found → error
    """
    input_file = Path(input_path)
    
    # Check if file exists
    if not input_file.exists():
        return None, None, f"File not found: {input_file}", False
    
    # Check if file is CSV
    if input_file.suffix.lower() != '.csv':
        return None, None, f"Invalid file type: {input_file.suffix}. Must be a CSV file (.csv)", False
    
    # Determine if input is M1 or M2
    is_m1 = "_M1" in input_file.stem
    is_m2 = "_M2" in input_file.stem
    
    if not is_m1 and not is_m2:
        # File doesn't have M1 or M2 suffix - treat as M1 only
        return input_file, None, None, False
    
    if is_m1:
        # User loaded M1 - look for M2
        m1_path = input_file
        # Replace last occurrence of _M1 with _M2 (handles _M1.csv and _M1_modified.csv)
        m2_path_str = str(input_file).replace("_M1", "_M2", 1)
        m2_path = Path(m2_path_str)
        
        if m2_path.exists():
            # Both M1 and M2 exist
            return m1_path, m2_path, None, False
        else:
            # M1 exists but no M2 - load M1 into both M1 and M2 slots
            print(f"[INFO] No M2 file found. Loading M1 file into both perspectives: {m1_path}")
            return m1_path, m1_path, None, False
    
    else:  # is_m2
        # User loaded M2 - look for M1
        m2_path = input_file
        # Replace last occurrence of _M2 with _M1 (handles _M2.csv and _M2_modified.csv)
        m1_path_str = str(input_file).replace("_M2", "_M1", 1)
        m1_path = Path(m1_path_str)
        
        if m1_path.exists():
            # Both M1 and M2 exist
            return m1_path, m2_path, None, False
        else:
            # M2 exists but no M1 - load M2 into both M1 and M2 slots, select M2
            print(f"[INFO] No M1 file found. Loading M2 file into both perspectives: {m2_path}")
            return m2_path, m2_path, None, True


class InteractiveEditor:
    """Main application class for interactive scenario editor."""
    
    def __init__(self, csv_file: str, qt_app: QApplication, m1_path: Optional[Path] = None, m2_path: Optional[Path] = None, initial_perspective: str = "M1"):
        """
        Initialize interactive editor.
        
        Args:
            csv_file: Path to CSV file to load (primary file - typically M1)
            qt_app: QApplication instance
            m1_path: Path to M1 file (if different from csv_file)
            m2_path: Path to M2 file (None if doesn't exist)
            initial_perspective: Initial perspective to display ("M1" or "M2")
        """
        self.csv_file = Path(csv_file)
        self.original_csv_file = self.csv_file  # Track original for perspective-based saves
        self.m1_path = m1_path or self.csv_file
        self.m2_path = m2_path
        self.initial_perspective = initial_perspective
        self.qt_app = qt_app
        
        # Load configuration (with fallback to defaults)
        config = get_config()
        self.LAYOUT = config.get_layout()
        
        # Create Qt main window
        self.window = EditorMainWindow(self.csv_file)
        
        # Flexible workspace with QDockWidget panels
        
        # Initialize PyQtGraph primitive panel
        self.primitive_panel = PrimitivePanelPyQtGraph()
        
        # Connect signals from primitive panel
        self.primitive_panel.primitive_changed.connect(self._on_primitive_changed)
        self.primitive_panel.diagnostic_marker_placed.connect(self._on_diagnostic_marker)
        self.primitive_panel.event_delete_requested.connect(self._on_event_delete_requested)
        self.primitive_panel.event_insert_requested.connect(self._on_event_insert_requested)
        
        # Phase 2 refactoring: Connect new signals (replacing callbacks)
        self.primitive_panel.primitive_preview_requested.connect(self._on_primitive_preview)
        self.primitive_panel.primitive_reset_requested.connect(self._on_primitive_reset)
        
        # Initialize PyQtGraph trajectory panel
        self.trajectory_panel = TrajectoryPanelPyQtGraph()
        
        # Wrap panels in QDockWidget for flexible workspace
        self.primitive_dock = QDockWidget("Primitives", self.window)
        self.primitive_dock.setWidget(self.primitive_panel)
        self.primitive_dock.setFeatures(
            QDockWidget.DockWidgetMovable | 
            QDockWidget.DockWidgetFloatable | 
            QDockWidget.DockWidgetClosable
        )
        self.window.addDockWidget(Qt.LeftDockWidgetArea, self.primitive_dock)
        
        self.trajectory_dock = QDockWidget("Trajectory", self.window)
        self.trajectory_dock.setWidget(self.trajectory_panel)
        self.trajectory_dock.setFeatures(
            QDockWidget.DockWidgetMovable | 
            QDockWidget.DockWidgetFloatable | 
            QDockWidget.DockWidgetClosable
        )
        self.window.addDockWidget(Qt.RightDockWidgetArea, self.trajectory_dock)
        
        # Initialize model (structured: uses Event/Marker)
        self.model = EditorModel()

        # Initialize trajectory panel - PyQtGraph for performance and clean events
        # (Already created above in layout)

        # Initialize controller (structured)
        self.controller = EditorController(
            model=self.model,
            primitive_panel=self.primitive_panel,
            trajectory_panel=self.trajectory_panel,
            undo_stack=self.window.undo_stack
        )

        # Load scenario (structured: Event/Marker)
        self.controller.load_scenario(str(self.m1_path), str(self.m2_path) if self.m2_path else None)
        
        # Create editor widgets
        self.gamma_self0_editor = GammaSelf0Editor(self.model.gamma_self_0)
        self.gamma_self0_editor.value_changed.connect(self._on_gamma_self0_changed)
        self.gamma_self0_editor.reset_requested.connect(self._on_gamma_self0_reset)
        
        from tools.editor.widgets import InsertionOptionsWidget
        self.insertion_options = InsertionOptionsWidget()
        self.insertion_options.insertions_changed.connect(self._on_insertions_changed)
        
        from tools.editor.widgets import PerspectiveSwitcher
        self.perspective_switcher = PerspectiveSwitcher()
        self.perspective_switcher.perspective_changed.connect(self._on_perspective_changed)
        
        from tools.editor.widgets import NameEditor
        initial_name = self.model.get_display_name(self.controller.perspective)
        self.name_editor = NameEditor(initial_name)
        self.name_editor.name_changed.connect(self._on_name_changed)
        
        from tools.editor.widgets import NoteEditor
        from tools.editor.widgets import NoteEditor
        self.note_editor = NoteEditor()
        self.note_editor.note_changed.connect(self._on_note_changed)
        
        # Set initial perspective AFTER all widgets created
        if self.initial_perspective == "M2":
            self.perspective_switcher.set_perspective("M2")
        
        # Create gauge widgets
        from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout, QWidget
        
        # Primitive gauge
        primitive_gauge_frame = QFrame()
        primitive_gauge_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        primitive_gauge_layout = QVBoxLayout()
        primitive_gauge_label = QLabel("Primitive Readout")
        primitive_gauge_label.setAlignment(Qt.AlignCenter)
        primitive_gauge_label.setStyleSheet("font-weight: bold; font-size: 10pt;")
        self.primitive_gauge = QLabel("--")
        self.primitive_gauge.setAlignment(Qt.AlignCenter)
        self.primitive_gauge.setStyleSheet(
            'background-color: lightyellow; '
            'border: 1px solid black; '
            'border-radius: 5px; '
            'padding: 10px; '
            'font-size: 12pt; '
            'font-weight: bold;'
        )
        self.primitive_gauge.setMinimumHeight(60)
        primitive_gauge_layout.addWidget(primitive_gauge_label)
        primitive_gauge_layout.addWidget(self.primitive_gauge)
        primitive_gauge_frame.setLayout(primitive_gauge_layout)
        
        # Gamma_self gauge
        gamma_gauge_frame = QFrame()
        gamma_gauge_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        gamma_gauge_layout = QVBoxLayout()
        gamma_gauge_label = QLabel("γ_self Readout")
        gamma_gauge_label.setAlignment(Qt.AlignCenter)
        gamma_gauge_label.setStyleSheet("font-weight: bold; font-size: 10pt;")
        self.gamma_self_gauge = QLabel("--")
        self.gamma_self_gauge.setAlignment(Qt.AlignCenter)
        self.gamma_self_gauge.setStyleSheet(
            'background-color: lightblue; '
            'border: 1px solid black; '
            'border-radius: 5px; '
            'padding: 10px; '
            'font-size: 11pt; '
            'font-weight: bold;'
        )
        self.gamma_self_gauge.setMinimumHeight(60)
        gamma_gauge_layout.addWidget(gamma_gauge_label)
        gamma_gauge_layout.addWidget(self.gamma_self_gauge)
        gamma_gauge_frame.setLayout(gamma_gauge_layout)
        
        # Combine widgets in a container
        dock_container = QWidget()
        dock_layout = QVBoxLayout()
        dock_layout.addWidget(self.perspective_switcher)  # Phase 3.2: Add perspective switcher at top
        dock_layout.addWidget(self.name_editor)  # Phase 3.2: Add name editor
        dock_layout.addWidget(self.note_editor)  # Phase 3.2: Add note editor
        dock_layout.addWidget(self.gamma_self0_editor)
        dock_layout.addWidget(primitive_gauge_frame)
        dock_layout.addWidget(gamma_gauge_frame)
        dock_layout.addWidget(self.insertion_options)
        dock_layout.addStretch()
        dock_container.setLayout(dock_layout)
        
        # Add controls as dock widget
        self.controls_dock = QDockWidget("Editor Controls", self.window)
        self.controls_dock.setWidget(dock_container)
        self.controls_dock.setFeatures(
            QDockWidget.DockWidgetMovable | 
            QDockWidget.DockWidgetFloatable |
            QDockWidget.DockWidgetClosable
        )
        self.window.addDockWidget(Qt.RightDockWidgetArea, self.controls_dock)
        
        # Split the right area horizontally: Trajectory on left, Controls on right
        # This creates the 3-column layout: [Primitives | Trajectory | Controls]
        self.window.splitDockWidget(self.trajectory_dock, self.controls_dock, Qt.Horizontal)
        
        # Setup View menu for dock widget visibility
        self.window._setup_view_menu({
            'Primitives': self.primitive_dock,
            'Trajectory': self.trajectory_dock,
            'Controls': self.controls_dock
        })
        
        # Configure initial layout widths
        # First set the main left/right split (Primitives vs rest)
        self.window.resizeDocks(
            [self.primitive_dock, self.trajectory_dock],
            [500, 1000],  # Primitives=500px, Right side (Trajectory+Controls)=1000px
            Qt.Horizontal
        )
        
        # Then set the Trajectory/Controls split within the right area
        self.window.resizeDocks(
            [self.trajectory_dock, self.controls_dock],
            [700, 300],  # Trajectory=700px, Controls=300px
            Qt.Horizontal
        )
        
        # Connect primitive panel readout to Qt gauge (now that gauges exist)
        self.primitive_panel.primitive_readout = self.primitive_gauge
        
        # Connect gamma_self gauge to trajectory panel click events (Qt Signal - clean!)
        self.trajectory_panel.gamma_clicked.connect(self._update_gamma_self_gauge)
        
        # Connect primitive panel clicks to note editor
        self.primitive_panel.marker_clicked.connect(self._on_marker_clicked)
        
        # Connect trajectory panel clicks to note editor
        self.trajectory_panel.gamma_clicked.connect(self._on_trajectory_clicked)

        # Set up callbacks AFTER panels and controller are initialized
        self.window.save_callback = self._handle_save_request
        self.window.cleanup_callback = self._handle_cleanup
        
        # Load window geometry and dock layout from saved state
        self._load_window_state()
        
        # Connect zoom toolbar buttons (will zoom both panels)
        self.window.zoom_in_action.triggered.connect(self._handle_zoom_in)
        self.window.zoom_out_action.triggered.connect(self._handle_zoom_out)
        self.window.zoom_reset_action.triggered.connect(self._handle_zoom_reset)
        
        # Pan state
        self.pan_active = False
        self.pan_start = None
        self.pan_axes = None
    
    def _update_gamma_self_gauge(self, x, y):
        """Update gamma_self gauge in right panel."""
        if x is not None and y is not None:
            self.gamma_self_gauge.setText(f"γ_self\n{x:.2f} + {y:.2f}i")
        else:
            self.gamma_self_gauge.setText("--")
    
    def _handle_save_request(self, options: dict):
        """
        Handle save request from Qt toolbar.
        
        Args:
            options: Dict with 'csv' and 'png' boolean flags
        """
        # Commit any preview changes first
        self.controller.commit_changes()
        
        save_csv = options.get('csv', True)
        save_png = options.get('png', False)
        
        # Determine if current file is the original (in data/ and does not end with _modified.csv)
        original = (
            self.original_csv_file.parent.name == 'data' and
            not self.original_csv_file.stem.endswith('_modified')
        )
        
        # Determine base name for output files (without _modified suffix and without extension)
        # Always use original_csv_file to ensure consistent perspective-based naming
        if self.original_csv_file.stem.endswith('_modified'):
            base_name = self.original_csv_file.stem[:-9]  # Remove '_modified'
        else:
            base_name = self.original_csv_file.stem
        
        # Adjust base name for current perspective (M1 vs M2)
        current_perspective = self.controller.perspective
        if current_perspective == "M2":
            # Replace M1 with M2 in the base name
            base_name = base_name.replace("_M1", "_M2")
        
        # Output directory is data/
        data_dir = self.original_csv_file.parent if self.original_csv_file.parent.name == 'data' else self.original_csv_file.parent.parent / 'data'
        
        # Determine output paths
        csv_path = data_dir / f"{base_name}_modified.csv"
        combined_png = data_dir / f"{base_name}_modified.png"
        
        # Save CSV if requested
        if save_csv:
            self.controller.save_scenario(str(csv_path))
            self.window.show_message(f"Saved CSV to: {csv_path}")
            # Update self.csv_file to point to the new file for future saves
            self.csv_file = csv_path
            self.window.update_window_title(self.csv_file)
        
        # Save PNG plots if requested (combined primitives + trajectory)
        if save_png:
            self._save_combined_plot(str(combined_png))
            self.window.show_message(f"Saved combined plot to: {combined_png}")
        
        if not save_csv and not save_png:
            self.window.show_message("No save operation performed", 'warning')
    
    def _handle_zoom_in(self):
        """Handle zoom in toolbar button - zoom all panels uniformly."""
        self.trajectory_panel.zoom_in()
        self.controller.primitive_panel.zoom_in()
        self.window.show_message("Zoomed in (all panels)")
    
    def _handle_zoom_out(self):
        """Handle zoom out toolbar button - zoom all panels uniformly."""
        self.controller.trajectory_panel.zoom_out()
        self.controller.primitive_panel.zoom_out()
        self.window.show_message("Zoomed out (all panels)")
    
    def _handle_zoom_reset(self):
        """Handle reset view toolbar button - reset both panels."""
        self.controller.trajectory_panel.reset_view()
        self.controller.primitive_panel.reset_view()
        self.controller.primitive_panel.clear_readout()
        self.window.show_message("Reset all views")
    
    def _handle_cleanup(self):
        """Handle application cleanup before exit."""
        # Phase 3.1: Save window state before exit
        self._save_window_state()
        
        if hasattr(self, 'controller'):
            self.controller.cleanup()
    
    def _save_combined_plot(self, filepath: str):
        """
        Save a combined PNG with primitives on the left and trajectory on the right.
        
        Args:
            filepath: Output PNG file path
        
        Note: PNG export is currently disabled during PyQtGraph migration.
        Use PyQtGraph's built-in export or screenshot functionality instead.
        """
        self.window.show_message("PNG export temporarily unavailable (PyQtGraph migration in progress)", 'warning')
        print(f"[PNG EXPORT] Skipped - needs reimplementation for PyQtGraph")
        return
        
        # TODO: Reimplement using PyQtGraph export functionality
        # Could use: self.primitive_panel.graphics_widget.grab() and self.trajectory_panel.plot_widget.grab()
        # Or use pyqtgraph.exporters module

    
    def _on_primitive_changed(self, event_index, primitive, value):
        """Handle primitive change from primitive panel (on release)."""
        self.controller.on_primitive_changed(event_index, primitive, value)
    
    def _on_primitive_preview(self, event_index, primitive, value):
        """Handle primitive preview from primitive panel (during drag)."""
        self.controller.on_primitive_preview(event_index, primitive, value)
    
    def _on_primitive_reset(self, event_index, primitive):
        """Handle primitive reset from primitive panel (double-click)."""
        self.controller.on_primitive_reset(event_index, primitive)
    
    def _on_event_delete_requested(self, event_index):
        """
        Handle event deletion request from primitive panel (Ctrl+Click).
        
        Args:
            event_index: Event index to delete
        """
        print(f"\n[DELETE REQUEST] Event {event_index}")
        
        # Validation: Get events
        events = self.model.get_events(self.controller.perspective)
        
        # Can't delete if only 2 events (need at least start and end)
        if len(events) <= 2:
            print(f"[DELETE] Cannot delete - need at least 2 events (start and end)")
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self.window,
                "Cannot Delete",
                "Cannot delete event. Scenarios must have at least 2 events (start and end)."
            )
            return
        
        # Can't delete first or last event
        if event_index == 0 or event_index == len(events) - 1:
            print(f"[DELETE] Cannot delete first ({event_index}=0) or last ({event_index}={len(events)-1}) event")
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self.window,
                "Cannot Delete",
                "Cannot delete the first or last event."
            )
            return
        
        # Can't delete locked events
        event = events[event_index]
        if event.locked:
            print(f"[DELETE] Cannot delete locked event at time={event.time}")
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self.window,
                "Cannot Delete",
                f"Cannot delete locked event at day {event.time}.\n\nRight-click to unlock first."
            )
            return
        
        # Create and push delete command to undo stack
        if self.controller.undo_stack:
            from tools.editor.commands import DeleteEventCommand
            command = DeleteEventCommand(self.controller, event_index)
            self.controller.undo_stack.push(command)
            print(f"[DELETE] Pushed DeleteEventCommand to undo stack")
        else:
            # No undo stack - delete directly
            self.controller._delete_event(event_index)
    
    def _on_event_insert_requested(self, event_index):
        """
        Handle event insertion request from primitive panel (Ctrl+Shift+Click).
        
        Inserts a new event before the specified event, with the new event taking
        the existing event's time, and the existing event (plus all subsequent)
        shifting forward by the time delta to the previous event.
        
        Args:
            event_index: Event index to insert before
        """
        print(f"\n[INSERT REQUEST] Insert before event {event_index}")
        
        # Validation: Get events
        events = self.model.get_events(self.controller.perspective)
        
        # Can't insert before first event (would shift start time)
        if event_index == 0:
            print(f"[INSERT] Cannot insert before first event")
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self.window,
                "Cannot Insert",
                "Cannot insert an event before the first event (start time cannot change)."
            )
            return
        
        # Create and push insert command to undo stack
        if self.controller.undo_stack:
            try:
                from tools.editor.commands import InsertEventBeforeCommand
                # Check if primitive panel has pending insert time
                insert_time = getattr(self.primitive_panel, 'pending_insert_time', None)
                command = InsertEventBeforeCommand(self.controller, event_index, insert_time)
                self.controller.undo_stack.push(command)
                # Clear pending time
                if hasattr(self.primitive_panel, 'pending_insert_time'):
                    delattr(self.primitive_panel, 'pending_insert_time')
            except ValueError as e:
                # Command validation failed
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self.window,
                    "Cannot Insert",
                    str(e)
                )
    
    def _on_diagnostic_marker(self, event_index: int, primitive: str, hypothetical_value: float):
        """
        Handle Shift+Click diagnostic marker placement (counterfactual exploration).
        
        Computes and displays a hypothetical gamma_self trajectory showing what would
        happen if the clicked primitive had the hypothetical value. Useful for exploring
        "what-if" scenarios without committing changes.
        
        Args:
            event_index: Event index where marker was placed
            primitive: Which primitive was clicked ('v', 'r', 'f', 'a', 'S')
            hypothetical_value: The Y value where user shift+clicked
        """
        from core.love import update_gamma_self
        import numpy as np
        
        # Get current events
        events = self.model.get_events(self.controller.perspective)
        if event_index >= len(events):
            return
        
        # Create hypothetical primitives array (copy of current state)
        primitives_data = self.model.get_primitives_array(self.controller.perspective, include_preview=False)
        times = primitives_data['time']
        
        # Modify the one primitive with hypothetical value
        primitives_data[primitive][event_index] = hypothetical_value
        
        # Compute hypothetical gamma_self trajectory using same logic as controller
        gamma_self = self.model.gamma_self_0
        gamma_trajectory = [gamma_self]
        
        for i in range(len(events) - 1):
            v = primitives_data['v'][i]
            r = primitives_data['r'][i]
            f = primitives_data['f'][i]
            a = primitives_data['a'][i]
            S = primitives_data['S'][i]
            
            time_delta = times[i + 1] - times[i]
            gamma_self = update_gamma_self(
                gamma_self, v, r, f, a, S,
                weights=self.controller.weights,
                time_delta=time_delta
            )
            gamma_trajectory.append(gamma_self)
        
        # Get gamma_self AFTER the clicked event's primitives are applied
        # gamma_trajectory[0] = gamma_self_0 (before event 0)
        # gamma_trajectory[1] = gamma after event 0's primitives applied
        # gamma_trajectory[event_index + 1] = gamma after event's primitives applied
        if event_index + 1 < len(gamma_trajectory):
            gamma_val = gamma_trajectory[event_index + 1]  # Gamma AFTER this event
            gamma_x = gamma_val.real
            gamma_y = gamma_val.imag
            
            print(f"[DIAGNOSTIC HANDLER] Gamma_self after event {event_index} with {primitive}={hypothetical_value:.2f}: ({gamma_x:.2f}, {gamma_y:.2f}i)")
            
            # Place marker on trajectory panel at event position
            self.trajectory_panel.place_diagnostic_marker(gamma_x, gamma_y)
            print(f"[DIAGNOSTIC HANDLER] Placed trajectory marker at event {event_index} position ({gamma_x:.2f}, {gamma_y:.2f})")
            
            # Update primitive readout
            event = events[event_index]
            self.primitive_panel._update_readout(event_index, primitive, hypothetical_value)
            print(f"[DIAGNOSTIC HANDLER] Updated primitive readout")
            
            # Update gamma_self readout (simulate a click at that position)
            if hasattr(self, 'gamma_self_gauge') and self.gamma_self_gauge:
                self.gamma_self_gauge.setText(f"γ_self\n{gamma_x:.2f} + {gamma_y:.2f}i")
                self.gamma_self_gauge.setVisible(True)
                print(f"[DIAGNOSTIC HANDLER] Updated gamma_self readout")
            else:
                print(f"[DIAGNOSTIC HANDLER] Warning: gamma_self_gauge not available")
            
            print(f"[DIAGNOSTIC WHAT-IF] If event {event_index} {primitive}={hypothetical_value:.2f}: γ_self=({gamma_x:.2f}, {gamma_y:.2f}i)")
    
    def _on_lock_toggle(self, event_index):
        """
        Handle lock toggle from primitive panel right-click menu.
        
        Toggles the lock state of an event. Locked events cannot be edited or deleted,
        protecting critical scenario moments.
        
        Args:
            event_index: Index of event to lock/unlock
        """
        self.controller.on_lock_toggle(event_index)
    
    def _on_insert_event(self, time: float):
        """
        Handle event insertion from Shift+Click.
        
        Args:
            time: Raw time value from click (will be rounded per user preference)
        """
        try:
            # Round time according to insertion mode
            rounded_time = self.insertion_options.round_time(time)
            self.controller.insert_event_at_time(rounded_time)
            self.window.show_message(f"Inserted event at time {rounded_time}")
        except Exception as e:
            self.window.show_message(f"Error inserting event: {str(e)}", 'error')
    
    def _on_insertions_changed(self, times: list):
        """
        Handle changes to insertion time list.
        
        Args:
            times: List of time values where events should be inserted
        """
        # Get current events
        events = self.model.get_events(self.controller.perspective)
        
        # Find which events are currently inserted (all primitives = 0, not first/last)
        current_inserted_times = []
        current_inserted_indices = []
        for idx, evt in enumerate(events):
            if is_inserted_event(evt, exclude_first_last=True, event_idx=idx, total_events=len(events)):
                current_inserted_times.append(evt.time)
                current_inserted_indices.append(idx)
        
        # Determine what to add and what to remove
        # Check existing event times to avoid duplicates
        existing_times = [evt.time for evt in events]
        to_add = []
        rejected_times = []  # Track rejected duplicate times
        for t in times:
            # Check if this time already exists as a non-inserted event
            is_existing = any(abs(t - existing_t) < 0.001 for existing_t in existing_times if existing_t not in current_inserted_times)
            if is_existing:
                rejected_times.append(t)
                print(f"Event occupied at time {t}, please enter an unoccupied event time to insert.")
            elif t not in current_inserted_times:
                to_add.append(t)
        
        to_remove_times = [t for t in current_inserted_times if t not in times]
        
        # Track if any changes were made
        changes_made = False
        
        # Remove events that are no longer in the list (in reverse order to maintain indices)
        if to_remove_times:
            # Build list of indices to remove, sorted in reverse
            indices_to_remove = []
            for time_to_remove in to_remove_times:
                for idx, evt in enumerate(events):
                    if abs(evt.time - time_to_remove) < 0.001:
                        indices_to_remove.append(idx)
                        break
            
            indices_to_remove.sort(reverse=True)
            
            for idx in indices_to_remove:
                try:
                    # Use no_update version for batch operation
                    self.controller.delete_event_at_index_no_update(idx)
                    changes_made = True
                except Exception as e:
                    print(f"[INSERTIONS] Error removing event at index {idx}: {e}")
        
        # Add new insertion events
        for time_to_add in to_add:
            try:
                # Use no_update version for batch operation
                print(f"[INSERTIONS] Adding event at time {time_to_add}")
                self.controller.insert_event_at_time_no_update(time_to_add)
                changes_made = True
            except Exception as e:
                print(f"[INSERTIONS] Error adding event at {time_to_add}: {e}")
                self.window.show_message(f"Error inserting at {time_to_add}: {str(e)}", 'error')
        
        # Update views only ONCE at the end if any changes were made
        if changes_made:
            import time
            t0 = time.time()
            self.controller._update_all_views()
            t1 = time.time()
            self.controller._recompute_trajectory_immediate()
            t2 = time.time()
            print(f"[PERF] update_all_views: {(t1-t0)*1000:.1f}ms, recompute_trajectory: {(t2-t1)*1000:.1f}ms, total: {(t2-t0)*1000:.1f}ms")
            
            # Sync widget with actual inserted events in model
            # Find current inserted events after all changes
            updated_events = self.model.get_events(self.controller.perspective)
            actual_inserted_times = []
            for idx, evt in enumerate(updated_events):
                if is_inserted_event(evt, exclude_first_last=True, event_idx=idx, total_events=len(updated_events)):
                    actual_inserted_times.append(evt.time)
            
            # Update widget to reflect actual state (without triggering another change event)
            self.insertion_options.update_from_times(actual_inserted_times)
            
            self.window.show_message(f"Insertion points updated: {len(actual_inserted_times)} total")
        elif rejected_times:
            # No changes made, but we need to remove rejected entries from widget
            # Sync widget with current model state (this will remove rejected times)
            updated_events = self.model.get_events(self.controller.perspective)
            actual_inserted_times = []
            for idx, evt in enumerate(updated_events):
                if is_inserted_event(evt, exclude_first_last=True, event_idx=idx, total_events=len(updated_events)):
                    actual_inserted_times.append(evt.time)
            
            # Update widget to reflect actual state (removes rejected entries)
            self.insertion_options.update_from_times(actual_inserted_times)
    
    def _on_gamma_self0_changed(self, new_value: complex):
        """
        Handle gamma_self_0 change from editor widget.
        
        Args:
            new_value: New gamma_self_0 complex value
        """
        # Store original value if this is the first modification
        if not hasattr(self.model, 'gamma_self_0_original'):
            self.model.gamma_self_0_original = self.model.gamma_self_0
            self.model.gamma_self_0_modified = False
        
        # Update model
        old_value = self.model.gamma_self_0
        self.model.gamma_self_0 = new_value
        self.model.gamma_self_0_modified = (
            abs(new_value - self.model.gamma_self_0_original) > 0.001
        )
        
        # Recompute trajectory with new initial state
        self.controller._recompute_trajectory_immediate()
        
        # Update start marker appearance on trajectory panel
        self.trajectory_panel.update_start_marker_style(
            self.model.gamma_self_0_modified
        )
        
        self.window.show_message(
            f"gamma_self_0 updated: {new_value.real:+.2f}{new_value.imag:+.2f}j"
        )
    
    def _on_gamma_self0_reset(self):
        """Handle reset of gamma_self_0 to original CSV value."""
        if hasattr(self.model, 'gamma_self_0_original'):
            self.model.gamma_self_0 = self.model.gamma_self_0_original
            self.model.gamma_self_0_modified = False
            
            # Recompute trajectory
            self.controller._recompute_trajectory_immediate()
            
            # Update start marker appearance
            self.trajectory_panel.update_start_marker_style(False)
            
            self.window.show_message("gamma_self_0 reset to CSV default")
    
    def _on_perspective_changed(self, perspective: str):
        """
        Handle perspective switch from UI (M1 ↔ M2).
        
        Args:
            perspective: Either 'M1' or 'M2'
        """
        self.controller.switch_perspective(perspective)
        
        # Update name editor to show current perspective's name
        current_name = self.model.get_display_name(perspective)
        print(f"[DEBUG] Switching to {perspective}, name_m1='{self.model.name_m1}', name_m2='{self.model.name_m2}', display_name='{current_name}'")
        self.name_editor.set_name(current_name)
        
        self.window.show_message(f"Switched to {perspective} perspective")
    
    def _on_name_changed(self, new_name: str):
        """
        Handle name change from name editor.
        
        Args:
            new_name: New name entered by user
        """
        perspective = self.controller.perspective
        
        # Update model with perspective-specific name
        if perspective == "M1":
            self.model.name_m1 = new_name
            print(f"[DEBUG] Updated name_m1 to '{new_name}'")
        else:
            self.model.name_m2 = new_name
            print(f"[DEBUG] Updated name_m2 to '{new_name}'")
        
        # Update name editor display to confirm change
        self.name_editor.set_name(new_name)
        
        # Update panel titles
        self.primitive_panel.set_scenario_name(new_name)
        self.trajectory_panel.set_scenario_name(new_name)
        
        self.window.show_message(f"{perspective} name updated to: {new_name}")
    
    def _on_note_changed(self, event_time: float, note_text: str):
        """
        Handle note change from note editor.
        
        Args:
            event_time: Time of the event
            note_text: New note text
        """
        # Find the event at this time
        events = self.model.get_events(self.controller.perspective)
        for event in events:
            if abs(event.time - event_time) < 0.001:  # Float comparison
                event.notes = note_text
                self.window.show_message(f"Note updated for event at time {event_time}")
                return
        
        self.window.show_message(f"Warning: Event at time {event_time} not found", "warning")
    
    def _on_marker_clicked(self, event_idx: int, primitive: str):
        """
        Handle marker click from primitive panel.
        Update note editor with event notes.
        
        Args:
            event_idx: Index of selected event
            primitive: Primitive that was clicked
        """
        # Get the event
        event = self.model.get_event(event_idx, self.controller.perspective)
        if event:
            self.note_editor.set_event(event.time, event.notes)
    
    def _on_trajectory_clicked(self, x: float, y: float):
        """
        Handle trajectory panel click (gamma_self marker).
        Find nearest event and show its notes.
        
        Args:
            x: Real component (clicked position)
            y: Imaginary component (clicked position)
        """
        # Find nearest event by time (using trajectory x-axis which represents time indirectly)
        # For now, we'll use the gamma_self readout which already finds the nearest point
        # We need to map this back to an event time
        
        # Get all events and find the one closest to the clicked trajectory point
        events = self.model.get_events(self.controller.perspective)
        if not events:
            return
        
        # For simplicity, find the event whose trajectory point is closest
        # This would require trajectory computation - for now, just show first event
        # TODO: Implement proper trajectory-to-event mapping
        
        # Temporary: Just show the last clicked event from primitive panel
        # Better implementation would map trajectory point to nearest event time
        pass
    
    # NOTE: Keyboard shortcuts removed with matplotlib event handlers
    # PyQtGraph trajectory panel uses built-in Qt key events
    # TODO: Re-implement shortcuts via Qt keyPressEvent if needed (Ctrl+S, ESC, Delete, etc.)
    
    def _edit_gamma_self_0(self):
        """Edit initial gamma_self position."""
        from PySide6.QtWidgets import QInputDialog
        
        current = self.controller.model.gamma_self_0
        
        # Get real part
        real_part, ok = QInputDialog.getDouble(
            self.window,
            "Edit Gamma_self_0",
            f"Enter REAL part (Ego↔We axis):\n\nCurrent: {current.real:+.1f}{current.imag:+.1f}j\n\nExamples:\n  Strangers: 0\n  Friends: +5\n  Exes (hurt): -5",
            value=current.real,
            decimals=1
        )
        
        if not ok:
            return
        
        # Get imaginary part
        imag_part, ok = QInputDialog.getDouble(
            self.window,
            "Edit Gamma_self_0",
            f"Enter IMAGINARY part (Hate↔Love axis):\n\nCurrent: {current.real:+.1f}{current.imag:+.1f}j\n\nExamples:\n  Strangers: 0\n  Friends: +8\n  Exes (hurt): -3",
            value=current.imag,
            decimals=1
        )
        
        if not ok:
            return
        
        # Update gamma_self_0
        self.controller.model.gamma_self_0 = complex(real_part, imag_part)
        
        # Recompute trajectory from new starting point
        self.controller._recompute_trajectory_immediate()
        
        self.window.show_message(f"Gamma_self_0 set to {real_part:+.1f}{imag_part:+.1f}j")
    
    def _save_as(self):
        """Open Save As dialog and save CSV."""
        from PySide6.QtWidgets import QFileDialog
        
        # Suggest filename with _modified suffix
        original_stem = self.csv_file.stem
        original_parent = self.csv_file.parent
        suggested_name = original_parent / f"{original_stem}_modified.csv"
        
        # Open Qt file dialog
        filepath, _ = QFileDialog.getSaveFileName(
            self.window,
            "Save Modified Scenario",
            str(suggested_name),
            "CSV files (*.csv);;All files (*.*)"
        )
        
        if filepath:
            self.controller.save_scenario(filepath)
            self.window.show_message(f"Saved to: {filepath}")
    
    def _load_window_state(self):
        """Load window geometry and dock layout from QSettings."""
        from PySide6.QtCore import QSettings
        
        settings = QSettings('WhenMathPrays', 'InteractiveEditor')
        
        # Restore window geometry
        geometry = settings.value('geometry')
        if geometry:
            self.window.restoreGeometry(geometry)
        
        # Restore window state (dock positions, sizes, visibility)
        state = settings.value('windowState')
        if state:
            self.window.restoreState(state)
    
    def _save_window_state(self):
        """Save window geometry and dock layout to QSettings."""
        from PySide6.QtCore import QSettings
        
        settings = QSettings('WhenMathPrays', 'InteractiveEditor')
        settings.setValue('geometry', self.window.saveGeometry())
        settings.setValue('windowState', self.window.saveState())
    
    def run(self):
        """Show UI and enter Qt event loop."""
        self.window.show()
        return self.qt_app.exec()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Interactive Scenario Editor for GRP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/interactive_editor.py data/single_dating_to_love_M1.csv
  
Usage:
  - Drag primitive points vertically to change values (shows hollow preview)
  - Click HOLLOW point to continue editing from preview position
  - Double-click HOLLOW point to cancel preview and return to original
  - Press 'C' to COMMIT changes (hollow → filled, pins marker at current gamma_self)
  - Press ESC to CANCEL changes (revert to committed)
  - Press 'G' to edit Gamma_self_0 initial position (strangers=0+0j, exes=-5-3j, etc.)
  - Right-click on point to lock/unlock
  - Press 'F' to toggle Fixed View (prevent auto-zoom during edits)
  - Press '+' or '=' to ZOOM IN (context-aware: zooms panel under cursor)
  - Press '-' to ZOOM OUT (context-aware: zooms panel under cursor)
  - Press '0' to RESET view (context-aware: resets panel under cursor)
  - Modified points marked with colored numbers (color = primitive type)
  - Gamma_self markers PINNED at commit time (stay at original position)
  - Watch gamma_self trajectory update in real-time
  - Press Ctrl+S to SAVE (commits all previews to CSV)
  
Phase 1.5 Features:
  ✓ Single perspective (M1) editing
  ✓ Drag primitives (v, r, f, a, S) with Fidelity label
  ✓ Preview (hollow) vs Commit (filled) workflow
  ✓ Click hollow to continue editing
  ✓ Lock/unlock events
  ✓ Auto-mark modified points with numbers
  ✓ Real-time trajectory preview
  ✓ Zoom in/out/reset controls
  ✓ Fixed view mode (preserve zoom during edits)
  ✓ Gamma_self_0 initial position support
  ✓ Save As with new filename (commits previews)
        """
    )
    
    parser.add_argument('csv_file', type=str, 
                       help='Path to CSV file to edit')
    
    args = parser.parse_args()
    
    # Validate file and resolve M1/M2 paths
    m1_path, m2_path, error, was_originally_m2 = validate_and_resolve_paths(args.csv_file)
    
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    
    # Initial perspective: M2 if M2-only file, otherwise M1
    initial_perspective = "M2" if was_originally_m2 else "M1"
    
    # Show M2 status
    if m2_path:
        if m1_path == m2_path:
            # Single file loaded into both slots
            if was_originally_m2:
                print(f"[INFO] M2-only: Loaded into both perspectives (M2 selected)")
            else:
                print(f"[INFO] M1-only: Loaded into both perspectives (M1 selected)")
            print(f"[INFO] You can edit from either perspective and save to M1 or M2")
        else:
            # Dual perspective
            print(f"[INFO] Loading dual-perspective data:")
            print(f"  M1: {m1_path}")
            print(f"  M2: {m2_path}")
    else:
        print(f"[INFO] Loading single-perspective data: {m1_path}")
        print(f"[INFO] No M2 file found - perspective switching disabled")
    
    # Create Qt application (Phase 2)
    app = QApplication(sys.argv)
    app.setApplicationName('GRP Interactive Scenario Editor')
    
    # Create and run editor
    editor = InteractiveEditor(str(m1_path), app, m1_path=m1_path, m2_path=m2_path, initial_perspective=initial_perspective)
    sys.exit(editor.run())


if __name__ == '__main__':
    main()
