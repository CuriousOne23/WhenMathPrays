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


class InteractiveEditor:
    """Main application class for interactive scenario editor."""
    
    def __init__(self, csv_file: str, qt_app: QApplication):
        """
        Initialize interactive editor.
        
        Args:
            csv_file: Path to CSV file to load
            qt_app: QApplication instance
        """
        self.csv_file = Path(csv_file)
        self.qt_app = qt_app
        
        # Load configuration (with fallback to defaults)
        config = get_config()
        self.LAYOUT = config.get_layout()
        
        # Create Qt main window (Phase 2)
        self.window = EditorMainWindow(self.csv_file)
        
        # Create pure PyQtGraph layout (both panels)
        from PySide6.QtWidgets import QWidget, QHBoxLayout
        
        # Container widget for layout
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)  # Spacing between panels
        
        # Initialize PyQtGraph primitive panel
        self.primitive_panel = PrimitivePanelPyQtGraph()
        self.primitive_panel.setMaximumWidth(600)  # Constrain primitive panel width
        layout.addWidget(self.primitive_panel, stretch=2)
        
        # Connect signals from primitive panel
        self.primitive_panel.primitive_changed.connect(self._on_primitive_changed)
        self.primitive_panel.diagnostic_marker_placed.connect(self._on_diagnostic_marker)
        
        # Phase 2 refactoring: Connect new signals (replacing callbacks)
        self.primitive_panel.primitive_preview_requested.connect(self._on_primitive_preview)
        self.primitive_panel.primitive_reset_requested.connect(self._on_primitive_reset)
        
        # Phase 2 refactoring: Removed callback assignments (now using signals above)
        # self.primitive_panel.on_primitive_preview = self._on_primitive_preview
        # self.primitive_panel.on_primitive_reset = self._on_primitive_reset
        
        # Initialize PyQtGraph trajectory panel
        self.trajectory_panel = TrajectoryPanelPyQtGraph()
        layout.addWidget(self.trajectory_panel, stretch=3)  # Larger stretch for trajectory
        
        # Set central widget
        self.window.setCentralWidget(central_widget)
        
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
        
        # Disable Shift+Click insertion (now using explicit time inputs)
        # self.primitive_panel.on_insert_event = self._on_insert_event

        # Load scenario (structured: Event/Marker)
        self.controller.load_scenario(str(self.csv_file))
        
        # Create gamma_self_0 editor widget (Phase 2.1)
        self.gamma_self0_editor = GammaSelf0Editor(self.model.gamma_self_0)
        self.gamma_self0_editor.value_changed.connect(self._on_gamma_self0_changed)
        self.gamma_self0_editor.reset_requested.connect(self._on_gamma_self0_reset)
        
        # Create insertion options widget (Phase 2.1)
        from tools.editor.widgets import InsertionOptionsWidget
        self.insertion_options = InsertionOptionsWidget()
        self.insertion_options.insertions_changed.connect(self._on_insertions_changed)
        
        # Create gauge widgets
        from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout, QWidget
        from PySide6.QtCore import Qt
        
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
        dock_layout.addWidget(self.gamma_self0_editor)
        dock_layout.addWidget(primitive_gauge_frame)
        dock_layout.addWidget(gamma_gauge_frame)
        dock_layout.addWidget(self.insertion_options)
        dock_layout.addStretch()
        dock_container.setLayout(dock_layout)
        
        # Add as dock widget on the right
        dock = QDockWidget("Editor Controls", self.window)
        dock.setWidget(dock_container)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.window.addDockWidget(Qt.RightDockWidgetArea, dock)
        
        # Connect primitive panel readout to Qt gauge (now that gauges exist)
        self.primitive_panel.primitive_readout = self.primitive_gauge
        
        # Connect gamma_self gauge to trajectory panel click events (Qt Signal - clean!)
        self.trajectory_panel.gamma_clicked.connect(self._update_gamma_self_gauge)

        # Set up callbacks AFTER panels and controller are initialized
        self.window.save_callback = self._handle_save_request
        self.window.cleanup_callback = self._handle_cleanup
        
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
        print(f"[GAUGE UPDATE] gamma_self gauge called with x={x}, y={y}")
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
            self.csv_file.parent.name == 'data' and
            not self.csv_file.stem.endswith('_modified')
        )
        
        # Determine base name for output files (without _modified suffix and without extension)
        if self.csv_file.stem.endswith('_modified'):
            base_name = self.csv_file.stem[:-9]  # Remove '_modified'
        else:
            base_name = self.csv_file.stem
        
        # Output directory is data/
        data_dir = self.csv_file.parent if self.csv_file.parent.name == 'data' else self.csv_file.parent.parent / 'data'
        
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
    
    # Matplotlib event handlers removed - PyQtGraph has built-in pan/zoom
    # TODO: Add Qt-based keyboard shortcuts if needed
    
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
    
    def _on_diagnostic_marker(self, event_index: int, primitive: str, hypothetical_value: float):
        """
        Handle diagnostic 'what-if' marker placement.
        Computes hypothetical gamma_self trajectory if this primitive had the clicked value.
        
        Args:
            event_index: Event index where marker was placed
            primitive: Which primitive was clicked ('v', 'r', 'f', 'a', 'S')
            hypothetical_value: The Y value where user shift+clicked
        """
        print(f"[DIAGNOSTIC HANDLER] Called with event_index={event_index}, primitive={primitive}, value={hypothetical_value:.2f}")
        
        from core.love import update_gamma_self
        import numpy as np
        
        # Get current events
        events = self.model.get_events(self.controller.perspective)
        if event_index >= len(events):
            print(f"[DIAGNOSTIC HANDLER] Error: event_index {event_index} >= {len(events)} events")
            return
        
        # Create hypothetical primitives array (copy of current state)
        primitives_data = self.model.get_primitives_array(self.controller.perspective, include_preview=False)
        times = primitives_data['time']
        
        # Modify the one primitive with hypothetical value
        old_value = primitives_data[primitive][event_index]
        primitives_data[primitive][event_index] = hypothetical_value
        print(f"[DIAGNOSTIC HANDLER] Changed {primitive}[{event_index}] from {old_value:.2f} to {hypothetical_value:.2f}")
        print(f"[DIAGNOSTIC HANDLER] Event {event_index} primitives: v={primitives_data['v'][event_index]:.2f}, r={primitives_data['r'][event_index]:.2f}, f={primitives_data['f'][event_index]:.2f}, a={primitives_data['a'][event_index]:.2f}, S={primitives_data['S'][event_index]:.2f}")
        
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
        
        print(f"[DIAGNOSTIC HANDLER] Computed {len(gamma_trajectory)} gamma_self values")
        
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
        """Handle lock toggle from primitive panel."""
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
    
    # Validate file exists
    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"Error: File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    
    # Create Qt application (Phase 2)
    app = QApplication(sys.argv)
    app.setApplicationName('GRP Interactive Scenario Editor')
    
    # Create and run editor
    editor = InteractiveEditor(args.csv_file, app)
    sys.exit(editor.run())


if __name__ == '__main__':
    main()
