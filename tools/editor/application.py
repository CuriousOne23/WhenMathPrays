"""
EditorApplication - Main application lifecycle manager for interactive scenario editor.

Orchestrates FileManager, UIBuilder, EditorController, and MainWindow
to create a clean separation of concerns and eliminate the "god class" pattern.

Phase 3.5 Architecture Refactoring
"""

from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt

from tools.editor.file_manager import FileManager, FileLoadResult
from tools.editor.ui_builder import UIBuilder
from tools.editor.main_window import EditorMainWindow
from tools.editor.model import EditorModel
from tools.editor.controller import EditorController
from tools.editor.config import get_config
from tools.editor.constants import is_inserted_event


class EditorApplication:
    """
    Main application class orchestrating the interactive scenario editor.
    
    Responsibilities:
        - Application lifecycle (initialization, execution, cleanup)
        - Component coordination (FileManager, UIBuilder, Controller, MainWindow)
        - Signal connection orchestration
        - Save/export operations
        - User interaction event routing
    
    Does NOT:
        - Manage individual file paths (FileManager's job)
        - Create widgets (UIBuilder's job)
        - Handle business logic (Controller's job)
        - Manage window lifecycle (MainWindow's job)
    """
    
    def __init__(self, input_path: str, qt_app: QApplication):
        """
        Initialize the editor application.
        
        Args:
            input_path: Path to CSV file to load (M1, M2, or single-perspective)
            qt_app: QApplication instance
        """
        self.qt_app = qt_app
        self.config = get_config()
        
        # Phase 3.5: Use FileManager for path resolution
        self.file_manager = FileManager(input_path)
        load_result = self.file_manager.validate_and_resolve()
        
        if not load_result.is_success:
            raise ValueError(load_result.error_message)
        
        # Store resolved paths and initial perspective
        self.m1_path = load_result.m1_path
        self.m2_path = load_result.m2_path
        self.initial_perspective = load_result.initial_perspective
        
        # Create main window with appropriate file path
        primary_path = self.m1_path if self.initial_perspective == "M1" else self.m2_path
        self.window = EditorMainWindow(primary_path)
        
        # Create model
        self.model = EditorModel()
        
        # Phase 3.5: Use UIBuilder to create UI components (pass window)
        self.ui_builder = UIBuilder(self.window)
        panels_result = self.ui_builder.build_panels()
        self.primitive_panel = panels_result['primitive_panel']
        self.trajectory_panel = panels_result['trajectory_panel']
        
        # Create controller (with EditorState integration)
        self.controller = EditorController(
            model=self.model,
            primitive_panel=self.primitive_panel,
            trajectory_panel=self.trajectory_panel,
            undo_stack=self.window.undo_stack
        )
        
        # Load scenario data
        self.controller.load_scenario(
            str(self.m1_path), 
            str(self.m2_path) if self.m2_path else None
        )
        
        # Build editor widgets
        widgets_result = self.ui_builder.build_editor_widgets(
            initial_gamma_self_0=self.model.gamma_self_0,
            initial_perspective=self.initial_perspective,
            initial_name=self.model.get_display_name(self.controller.perspective)
        )
        self.gamma_self0_editor = widgets_result['gamma_self0_editor']
        self.insertion_options = widgets_result['insertion_options']
        self.perspective_switcher = widgets_result['perspective_switcher']
        self.name_editor = widgets_result['name_editor']
        self.note_editor = widgets_result['note_editor']
        
        # Build dock widgets (calls build_gauges internally)
        self.ui_builder.build_dock_widgets()
        self.ui_builder.build_controls_dock()
        
        self.primitive_dock = self.ui_builder.primitive_dock
        self.trajectory_dock = self.ui_builder.trajectory_dock
        self.controls_dock = self.ui_builder.controls_dock
        self.primitive_gauge = self.ui_builder.primitive_gauge
        self.gamma_self_gauge = self.ui_builder.gamma_self_gauge
        
        # Configure layout
        self.ui_builder.configure_layout()
        
        # Set initial perspective if loading M2-only file
        if self.initial_perspective == "M2":
            self.perspective_switcher.set_perspective("M2")
        
        # Connect all signals (Phase 3.5: direct connections, no forwarding)
        self._connect_signals()
        
        # Connect primitive panel readout to gauge
        self.primitive_panel.primitive_readout = self.primitive_gauge
        
        # Load window geometry/state
        self._load_window_state()
    
    def _connect_signals(self):
        """
        Connect all signals between components.
        
        Phase 3.5: Direct signal-to-slot connections, no callback forwarding.
        This eliminates the middleman pattern and improves performance.
        """
        # Primitive panel → Controller
        self.primitive_panel.primitive_changed.connect(self.controller.on_primitive_changed)
        self.primitive_panel.primitive_preview_requested.connect(self.controller.on_primitive_preview)
        self.primitive_panel.primitive_reset_requested.connect(self.controller.on_primitive_reset)
        self.primitive_panel.diagnostic_marker_placed.connect(self._on_diagnostic_marker)
        self.primitive_panel.event_delete_requested.connect(self._on_event_delete_requested)
        self.primitive_panel.event_insert_requested.connect(self._on_event_insert_requested)
        self.primitive_panel.marker_clicked.connect(self._on_marker_clicked)
        
        # Trajectory panel → Application (gauge updates)
        self.trajectory_panel.gamma_clicked.connect(self._update_gamma_self_gauge)
        self.trajectory_panel.gamma_clicked.connect(self._on_trajectory_clicked)
        self.trajectory_panel.event_insert_requested.connect(self._on_trajectory_insert_requested)
        
        # Editor widgets → Application handlers
        self.gamma_self0_editor.value_changed.connect(self._on_gamma_self0_changed)
        self.gamma_self0_editor.reset_requested.connect(self._on_gamma_self0_reset)
        self.insertion_options.insertions_changed.connect(self._on_insertions_changed)
        self.perspective_switcher.perspective_changed.connect(self._on_perspective_changed)
        self.name_editor.name_changed.connect(self._on_name_changed)
        self.note_editor.note_changed.connect(self._on_note_changed)
        
        # Main window → Application handlers
        self.window.save_requested.connect(self._handle_save_request)
        self.window.cleanup_requested.connect(self._handle_cleanup)
        self.window.zoom_in_action.triggered.connect(self._handle_zoom_in)
        self.window.zoom_out_action.triggered.connect(self._handle_zoom_out)
        self.window.zoom_reset_action.triggered.connect(self._handle_zoom_reset)
    
    def _update_gamma_self_gauge(self, x, y):
        """Update gamma_self gauge display."""
        if x is not None and y is not None:
            self.gamma_self_gauge.setText(f"γ_self\n{x:.2f} + {y:.2f}i")
        else:
            self.gamma_self_gauge.setText("--")
    
    def _handle_save_request(self, options: dict):
        """
        Handle save request from main window.
        
        Args:
            options: Dict with 'csv' and 'png' boolean flags
        """
        # Commit any preview changes first
        self.controller.commit_changes()
        
        save_csv = options.get('csv', True)
        save_png = options.get('png', False)
        
        # Phase 3.5: Use FileManager for save path resolution
        current_perspective = self.controller.perspective
        save_path = self.file_manager.get_save_path(current_perspective)
        
        # Save CSV if requested
        if save_csv:
            self.controller.save_scenario(str(save_path))
            self.window.show_message(f"Saved CSV to: {save_path}")
            self.file_manager.mark_modified(save_path)
            self.window.update_window_title(save_path)
        
        # Save PNG if requested
        if save_png:
            png_path = self.file_manager.get_png_path(current_perspective)
            self._save_combined_plot(str(png_path))
            self.window.show_message(f"Saved combined plot to: {png_path}")
        
        if not save_csv and not save_png:
            self.window.show_message("No save operation performed", 'warning')
    
    def _handle_zoom_in(self):
        """Handle zoom in toolbar button."""
        self.trajectory_panel.zoom_in()
        self.primitive_panel.zoom_in()
        self.window.show_message("Zoomed in (all panels)")
    
    def _handle_zoom_out(self):
        """Handle zoom out toolbar button."""
        self.trajectory_panel.zoom_out()
        self.primitive_panel.zoom_out()
        self.window.show_message("Zoomed out (all panels)")
    
    def _handle_zoom_reset(self):
        """Handle reset view toolbar button."""
        self.trajectory_panel.reset_view()
        self.primitive_panel.reset_view()
        self.primitive_panel.clear_readout()
        self.window.show_message("Reset all views")
    
    def _handle_cleanup(self):
        """Handle application cleanup before exit."""
        self._save_window_state()
        if hasattr(self, 'controller'):
            self.controller.cleanup()
    
    def _save_combined_plot(self, filepath: str):
        """
        Save combined PNG plot (primitives + trajectory).
        
        Args:
            filepath: Output PNG file path
        
        Note: PNG export currently disabled during PyQtGraph migration.
        """
        self.window.show_message("PNG export temporarily unavailable (PyQtGraph migration)", 'warning')
        print(f"[PNG EXPORT] Skipped - needs reimplementation for PyQtGraph")
        # TODO: Reimplement using pyqtgraph.exporters module
    
    def _on_diagnostic_marker(self, event_index: int, primitive: str, hypothetical_value: float):
        """
        Handle diagnostic marker placement (Shift+Click for "what-if" analysis).
        
        Args:
            event_index: Event index where marker was placed
            primitive: Primitive name ('v', 'r', 'f', 'a', 'S')
            hypothetical_value: Hypothetical primitive value
        """
        from core.love import update_gamma_self
        import numpy as np
        
        # Get current events
        events = self.model.get_events(self.controller.perspective)
        if event_index >= len(events):
            return
        
        # Create hypothetical primitives array
        primitives_data = self.model.get_primitives_array(
            self.controller.perspective, 
            include_preview=False
        )
        times = primitives_data['time']
        
        # Modify the one primitive with hypothetical value
        primitives_data[primitive][event_index] = hypothetical_value
        
        # Compute hypothetical gamma_self trajectory
        gamma_self = self.model.gamma_self_0
        gamma_trajectory = [gamma_self]
        
        for i in range(len(events) - 1):
            v = primitives_data['v'][i]
            r = primitives_data['r'][i]
            f = primitives_data['f'][i]
            a = primitives_data['a'][i]
            S = primitives_data['S'][i]
            dt = times[i + 1] - times[i]
            
            gamma_self = update_gamma_self(gamma_self, v, r, f, a, S, dt)
            gamma_trajectory.append(gamma_self)
        
        gamma_array = np.array(gamma_trajectory)
        
        # Show hypothetical trajectory on trajectory panel
        self.trajectory_panel.show_diagnostic_trajectory(
            times, 
            gamma_array, 
            event_index, 
            primitive, 
            hypothetical_value
        )
        
        # Show diagnostic marker on primitive panel
        self.primitive_panel.show_diagnostic_marker(event_index, primitive, hypothetical_value)
        
        # Update gauges with hypothetical values
        event_time = times[event_index]
        hypothetical_gamma = gamma_trajectory[event_index]
        self.primitive_gauge.setText(
            f"Day {event_time:.1f}\n{primitive} = {hypothetical_value:.2f}\n(DIAGNOSTIC)"
        )
        self.gamma_self_gauge.setText(
            f"γ_self (WHAT-IF)\n{hypothetical_gamma.real:.2f} + {hypothetical_gamma.imag:.2f}i"
        )
        
        print(f"[DIAGNOSTIC] Event {event_index}: {primitive}={hypothetical_value:.2f} "
              f"→ final γ_self={gamma_trajectory[-1]:.3f}")
    
    def _on_event_delete_requested(self, event_index):
        """
        Handle event deletion request (Ctrl+Click).
        
        Args:
            event_index: Event index to delete
        """
        from PySide6.QtWidgets import QMessageBox
        from tools.editor.commands import DeleteEventCommand
        
        events = self.model.get_events(self.controller.perspective)
        
        # Validation: need at least 2 events
        if len(events) <= 2:
            QMessageBox.warning(
                self.window,
                "Cannot Delete",
                "Cannot delete event. Scenarios must have at least 2 events (start and end)."
            )
            return
        
        # Can't delete first or last event
        if event_index == 0 or event_index == len(events) - 1:
            QMessageBox.warning(
                self.window,
                "Cannot Delete",
                "Cannot delete the first or last event."
            )
            return
        
        # Can't delete locked events
        event = events[event_index]
        if event.locked:
            QMessageBox.warning(
                self.window,
                "Cannot Delete",
                f"Cannot delete locked event at day {event.time}.\n\nRight-click to unlock first."
            )
            return
        
        # Push delete command to undo stack
        if self.controller.undo_stack:
            command = DeleteEventCommand(self.controller, event_index)
            self.controller.undo_stack.push(command)
            print(f"[DELETE] Pushed DeleteEventCommand for event {event_index}")
    
    def _on_event_insert_requested(self, event_index):
        """
        Handle event insertion request (Ctrl+Shift+Click).
        
        Args:
            event_index: Event index to insert before
        """
        from PySide6.QtWidgets import QMessageBox
        from tools.editor.commands import InsertEventBeforeCommand
        
        events = self.model.get_events(self.controller.perspective)
        
        # Can't insert before first event
        if event_index == 0:
            QMessageBox.warning(
                self.window,
                "Cannot Insert",
                "Cannot insert an event before the first event (start time cannot change)."
            )
            return
        
        # Push insert command to undo stack
        if self.controller.undo_stack:
            try:
                insert_time = getattr(self.primitive_panel, 'pending_insert_time', None)
                command = InsertEventBeforeCommand(self.controller, event_index, insert_time)
                self.controller.undo_stack.push(command)
                
                # Clear pending time
                if hasattr(self.primitive_panel, 'pending_insert_time'):
                    delattr(self.primitive_panel, 'pending_insert_time')
            except ValueError as e:
                QMessageBox.warning(self.window, "Cannot Insert", str(e))
    
    def _on_marker_clicked(self, event_index):
        """Handle marker click in primitive panel."""
        self._update_note_editor_from_event(event_index)
    
    def _on_trajectory_clicked(self, x, y):
        """Handle trajectory panel click."""
        # Find closest event to clicked time
        events = self.model.get_events(self.controller.perspective)
        if not events:
            return
        
        # Find closest event
        closest_index = min(range(len(events)), key=lambda i: abs(events[i].time - x))
        self._update_note_editor_from_event(closest_index)
    
    def _on_trajectory_insert_requested(self, insert_time: float):
        """Handle Ctrl+Shift+Click event insertion from trajectory panel."""
        try:
            # Find the event index where this insertion should occur
            events = self.model.get_events(self.controller.perspective)
            
            # Find the first event after the clicked time
            event_idx = 0
            for idx, evt in enumerate(events):
                if evt.time > insert_time:
                    event_idx = idx
                    break
            else:
                # Clicked after last event
                event_idx = len(events)
            
            # Use controller's insert command
            from tools.editor.commands import InsertEventBeforeCommand
            command = InsertEventBeforeCommand(
                controller=self.controller,
                event_idx=event_idx,
                insert_time=insert_time
            )
            
            # Push to undo stack
            if self.controller.undo_stack:
                try:
                    self.controller.undo_stack.push(command)
                    print(f"[INSERT] Pushed InsertEventCommand for time={insert_time} at index {event_idx}")
                except Exception as e:
                    print(f"[INSERT] Failed to push command: {e}")
                    raise
        except Exception as e:
            QMessageBox.warning(self.window, "Cannot Insert", str(e))
    
    def _update_note_editor_from_event(self, event_index):
        """Update note editor with event data."""
        events = self.model.get_events(self.controller.perspective)
        if event_index < len(events):
            event = events[event_index]
            self.note_editor.set_event(event.time, event.notes if event.notes else "")
    
    def _on_gamma_self0_changed(self, gamma_complex):
        """Handle gamma_self_0 value change."""
        self.model.gamma_self_0 = gamma_complex
        self.controller._recompute_trajectory()
    
    def _on_gamma_self0_reset(self):
        """Handle gamma_self_0 reset request."""
        self.model.gamma_self_0 = self.model.original_gamma_self_0
        self.gamma_self0_editor.set_value(self.model.gamma_self_0)
        self.controller._recompute_trajectory()
    
    def _on_insertions_changed(self, times: list):
        """Handle insertion time changes from InsertionOptions widget."""
        # Get current events
        events = self.model.get_events(self.controller.perspective)
        
        # Find currently inserted events
        from tools.editor.constants import is_inserted_event
        current_inserted_times = []
        for idx, evt in enumerate(events):
            if is_inserted_event(evt, exclude_first_last=True, event_idx=idx, total_events=len(events)):
                current_inserted_times.append(evt.time)
        
        # Determine what to add
        existing_times = [evt.time for evt in events]
        to_add = []
        for t in times:
            is_existing = any(abs(t - existing_t) < 0.001 for existing_t in existing_times if existing_t not in current_inserted_times)
            if is_existing:
                print(f"Event occupied at time {t}, please enter an unoccupied event time to insert.")
            elif t not in current_inserted_times:
                to_add.append(t)
        
        # Determine what to remove
        to_remove = [t for t in current_inserted_times if t not in times]
        
        # Apply insertions with undo support
        from tools.editor.commands import InsertEventCommand, DeleteEventCommand
        
        for t in sorted(to_add):
            # Create and push insert command (does not shift times)
            if self.controller.undo_stack:
                command = InsertEventCommand(self.controller, t)
                self.controller.undo_stack.push(command)
                print(f"[INSERT_OPTIONS] Pushed InsertEventCommand for time={t}")
            else:
                # Fallback if no undo stack
                self.controller.insert_event_at_time(t)
        
        # Apply removals with undo support
        for t in to_remove:
            # Find event at this time and delete it
            events = self.model.get_events(self.controller.perspective)
            for idx, evt in enumerate(events):
                if abs(evt.time - t) < 0.001:
                    if self.controller.undo_stack:
                        command = DeleteEventCommand(self.controller, idx)
                        self.controller.undo_stack.push(command)
                        print(f"[INSERT_OPTIONS] Pushed DeleteEventCommand for time={t}")
                    else:
                        self.controller.delete_event(idx)
                    break
        
        # Update views only if we used the fallback path
        if (to_add or to_remove) and not self.controller.undo_stack:
            self.controller._update_all_views()
            self.controller._recompute_trajectory_immediate()
    
    def _on_perspective_changed(self, perspective):
        """Handle perspective switch (M1 ↔ M2)."""
        self.controller.switch_perspective(perspective)
        
        # Update name editor
        new_name = self.model.get_display_name(perspective)
        self.name_editor.set_name(new_name)
        
        # Update window title
        save_path = self.file_manager.get_save_path(perspective)
        self.window.update_window_title(save_path)
    
    def _on_name_changed(self, name):
        """Handle name change."""
        self.model.set_display_name(self.controller.perspective, name)
    
    def _on_note_changed(self, event_index, note):
        """Handle note change for an event."""
        events = self.model.get_events(self.controller.perspective)
        if event_index < len(events):
            events[event_index].note = note
    
    def _load_window_state(self):
        """Load saved window geometry and dock layout."""
        from PySide6.QtCore import QSettings
        settings = QSettings('WhenMathPrays', 'InteractiveEditor')
        
        if settings.contains('geometry'):
            self.window.restoreGeometry(settings.value('geometry'))
        if settings.contains('windowState'):
            self.window.restoreState(settings.value('windowState'))
    
    def _save_window_state(self):
        """Save window geometry and dock layout."""
        from PySide6.QtCore import QSettings
        settings = QSettings('WhenMathPrays', 'InteractiveEditor')
        settings.setValue('geometry', self.window.saveGeometry())
        settings.setValue('windowState', self.window.saveState())
    
    def run(self):
        """Show UI and enter Qt event loop."""
        self.window.show()
        return self.qt_app.exec()
