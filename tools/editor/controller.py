"""
Controller for interactive scenario editor.

Coordinates between model and views, handles trajectory computation.
"""

import threading
import numpy as np
import pandas as pd
from typing import Optional, List

# Import GRP core
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.love import update_gamma_self, DEFAULT_WEIGHTS


class EditorController:
    """
    Main controller coordinating model and views.
    
    Handles:
    - Primitive value changes from UI
    - Debounced trajectory recomputation
    - Lock/unlock actions
    - Auto-marking of modified events
    - Undo/Redo command management
    """
    
    def __init__(self, model, primitive_panel, trajectory_panel, undo_stack=None):
        """
        Initialize controller.
        
        Args:
            model: EditorModel instance
            primitive_panel: PrimitivePanel instance
            trajectory_panel: TrajectoryPanel instance
            undo_stack: QUndoStack instance (optional)
        """
        self.model = model
        self.primitive_panel = primitive_panel
        self.trajectory_panel = trajectory_panel
        self.undo_stack = undo_stack
        
        # Set controller reference in primitive_panel so it can access model.modified_primitives
        self.primitive_panel.controller = self
        
        self.debounce_timer: Optional[threading.Timer] = None
        self.dirty = False
        self.perspective = "M1"  # Currently only M1 supported
        
        # GRP computation parameters
        self.weights = DEFAULT_WEIGHTS.copy()
        self.delta_t = 1.0  # Time step for trajectory computation
        
        # Track last committed trajectory for comparison
        self.committed_gamma_trajectory = None
        
        # Store baseline values (from CSV) for reset
        self.baseline_primitives = {}
        
        # Track if we're in undo/redo operation (to prevent recursive undo commands)
        self.in_undo_redo = False
    
    def load_scenario(self, filepath: str):
        """
        Load scenario from CSV and update views.
        Args:
            filepath: Path to CSV file
        """
        # Load into model
        self.model.load_csv(filepath, self.perspective)
        print(f"[DEBUG] EditorController.load_scenario: events_m1 count = {len(self.model.events_m1) if hasattr(self.model, 'events_m1') else 'N/A'}")

        # Store baseline primitives (for reset functionality)
        self.baseline_primitives = self.model.get_primitives_array(self.perspective, include_preview=False)

        # Initialize modified_primitives as empty - will track user modifications only
        events = self.model.get_events(self.perspective)
        print(f"[DEBUG] EditorController.load_scenario: get_events returned {len(events)} events")
        self.model.modified_primitives.clear()
        # Don't mark anything as modified on load - user hasn't modified anything yet

        # Update views
        self._update_all_views()

        # Compute initial trajectory
        self._recompute_trajectory_immediate()
    
    def on_primitive_changed(self, event_index: int, primitive: str, value: float):
        """
        Handle primitive value change from UI drag (on release - commit to model).
        """
        # Get old value for undo
        old_value = self.model.get_event(event_index, self.perspective).markers[primitive].value
        
        # Skip if no actual change
        if abs(value - old_value) < 0.001:
            return
        
        # Create undo command and push to stack (unless we're in undo/redo)
        if self.undo_stack and not self.in_undo_redo:
            from tools.editor.commands import EditPrimitiveCommand
            command = EditPrimitiveCommand(self, event_index, primitive, old_value, value)
            self.undo_stack.push(command)
            return  # Command.redo() will handle the update
        
        # If no undo stack or in undo/redo, apply directly
        self._apply_primitive_change(event_index, primitive, value)
        # Commit the new value to the model
        self.model.update_primitive(event_index, primitive, value, self.perspective, preview=False)
        if event_index not in self.model.modified_primitives:
            self.model.modified_primitives[event_index] = set()
        self.model.modified_primitives[event_index].add(primitive)
        print(f"[DEBUG] Updated modified_primitives: {self.model.modified_primitives}")
        
        # Store marker position from committed trajectory (must happen before display)
        # First compute trajectory to get the position
        events = self.model.get_events(self.perspective)
        primitives_data = self.model.get_primitives_array(self.perspective, include_preview=False)
        times = primitives_data['time']
        data = {
            'v': primitives_data['v'],
            'r': primitives_data['r'],
            'f': primitives_data['f'],
            'a': primitives_data['a'],
            'S': primitives_data['S']
        }
        gamma_self = self.model.gamma_self_0
        gamma_trajectory = [gamma_self]
        for i in range(len(times) - 1):
            dt = times[i+1] - times[i]
            v, r, f, a, S = data['v'][i], data['r'][i], data['f'][i], data['a'][i], data['S'][i]
            gamma_self = update_gamma_self(gamma_self, v, r, f, a, S, DEFAULT_WEIGHTS, dt)
            gamma_trajectory.append(gamma_self)
        
        # Store marker position
        marker_idx = event_index + 1 if event_index + 1 < len(gamma_trajectory) else event_index
        gamma_pos = gamma_trajectory[marker_idx]
        marker_key = (event_index, primitive)
        self.model.marker_positions[marker_key] = gamma_pos
        print(f"Marker {marker_key} → gamma_self[{marker_idx}] = {gamma_pos}")
        
        # === Phase 3: Incremental Update ===
        # Query modified status from Model (single source of truth)
        is_modified = self.model.is_modified(event_index, primitive)
        
        # Update only this marker in PrimitivePanel (O(1) operation)
        self.primitive_panel.update_marker(event_index, primitive, value, is_modified)
        
        # Update trajectory panel (full recompute, but marker update was instant)
        self._recompute_trajectory_immediate()
        # Note: trajectory panel updated via _display_trajectory
    
    def _apply_primitive_change(self, event_index: int, primitive: str, value: float):
        """
        Apply primitive change without undo tracking (used by undo commands).
        
        Args:
            event_index: Event index
            primitive: Primitive name
            value: New value
        """
        # Commit the new value to the model
        self.model.update_primitive(event_index, primitive, value, self.perspective, preview=False)
        
        # Check if this value is back to baseline
        baseline_value = self.baseline_primitives[primitive][event_index]
        if abs(value - baseline_value) < 0.001:
            # Back to baseline, remove from modified set
            if event_index in self.model.modified_primitives:
                self.model.modified_primitives[event_index].discard(primitive)
                if not self.model.modified_primitives[event_index]:
                    del self.model.modified_primitives[event_index]
            
            # Also remove marker position so it doesn't show on gamma_self graph
            marker_key = (event_index, primitive)
            if marker_key in self.model.marker_positions:
                del self.model.marker_positions[marker_key]
                print(f"[DEBUG] Removed marker position for {marker_key} (back to baseline)")
        else:
            # Modified, add to set
            if event_index not in self.model.modified_primitives:
                self.model.modified_primitives[event_index] = set()
            self.model.modified_primitives[event_index].add(primitive)
        
        print(f"[DEBUG] Updated modified_primitives: {self.model.modified_primitives}")
        
        # Store marker position from committed trajectory (only if still modified)
        # First compute trajectory to get the position
        events = self.model.get_events(self.perspective)
        primitives_data = self.model.get_primitives_array(self.perspective, include_preview=False)
        times = primitives_data['time']
        data = {
            'v': primitives_data['v'],
            'r': primitives_data['r'],
            'f': primitives_data['f'],
            'a': primitives_data['a'],
            'S': primitives_data['S']
        }
        gamma_self = self.model.gamma_self_0
        gamma_trajectory = [gamma_self]
        for i in range(len(times) - 1):
            dt = times[i+1] - times[i]
            v, r, f, a, S = data['v'][i], data['r'][i], data['f'][i], data['a'][i], data['S'][i]
            gamma_self = update_gamma_self(gamma_self, v, r, f, a, S, DEFAULT_WEIGHTS, dt)
            gamma_trajectory.append(gamma_self)
        
        # Store marker position only if still modified (not back to baseline)
        if self.model.is_modified(event_index, primitive):
            marker_idx = event_index + 1 if event_index + 1 < len(gamma_trajectory) else event_index
            gamma_pos = gamma_trajectory[marker_idx]
            marker_key = (event_index, primitive)
            self.model.marker_positions[marker_key] = gamma_pos
            print(f"Marker {marker_key} → gamma_self[{marker_idx}] = {gamma_pos}")
        else:
            print(f"Primitive {event_index}/{primitive} back to baseline, not storing marker position")
        
        # === Phase 3: Incremental Update ===
        # Query modified status from Model (single source of truth)
        is_modified = self.model.is_modified(event_index, primitive)
        
        # Update only this marker in PrimitivePanel (O(1) operation)
        self.primitive_panel.update_marker(event_index, primitive, value, is_modified)
        
        # Update trajectory panel (full recompute, but marker update was instant)
        self._recompute_trajectory_immediate()
    
    def on_primitive_preview(self, event_index: int, primitive: str, value: float):
        """
        Handle live preview during drag (motion).
        
        Args:
            event_index: Index in events list
            primitive: 'v', 'r', 'f', 'a', or 'S'
            value: New value
        """
        # Update preview in model
        self.model.update_primitive(event_index, primitive, value, self.perspective, preview=True)
        
        # Schedule debounced recomputation
        self.dirty = True
        self._schedule_recomputation_preview()
    
    def on_primitive_reset(self, event_index: int, primitive: str):
        """
        Handle double-click reset to baseline CSV value using Event/Marker objects.
        Args:
            event_index: Index in events list
            primitive: 'v', 'r', 'f', 'a', or 'S'
        """
        print(f"\n=== RESET PRIMITIVE {event_index}/{primitive} ===")
        
        # Get current and baseline values
        old_value = self.model.get_event(event_index, self.perspective).markers[primitive].value
        baseline_value = self.baseline_primitives[primitive][event_index]
        print(f"Resetting to baseline value: {baseline_value}")
        
        # Skip if already at baseline
        if abs(old_value - baseline_value) < 0.001:
            return
        
        # Create undo command and push to stack (unless we're in undo/redo)
        if self.undo_stack and not self.in_undo_redo:
            from tools.editor.commands import ResetPrimitiveCommand
            command = ResetPrimitiveCommand(self, event_index, primitive, old_value, baseline_value)
            self.undo_stack.push(command)
            return  # Command.redo() will handle the update
        
        # If no undo stack or in undo/redo, apply directly
        self._apply_primitive_reset(event_index, primitive, baseline_value)
    
    def _apply_primitive_reset(self, event_index: int, primitive: str, baseline_value: float):
        """
        Apply primitive reset without undo tracking (used by undo commands).
        
        Args:
            event_index: Event index
            primitive: Primitive name
            baseline_value: Baseline value to reset to
        """
        # Reset using Model's method (Phase 1 query interface)
        self.model.reset_event_primitive(event_index, primitive, baseline_value, self.perspective)
        
        print(f"Reset complete. modified_primitives: {self.model.modified_primitives}")
        
        # Remove marker position for this primitive
        marker_key = (event_index, primitive)
        if marker_key in self.model.marker_positions:
            del self.model.marker_positions[marker_key]
        
        # === Phase 3: Incremental Update ===
        # Update only this marker in PrimitivePanel (O(1) operation)
        is_modified = False  # Just reset, so not modified
        self.primitive_panel.update_marker(event_index, primitive, baseline_value, is_modified)
        
        # Remove the label annotation immediately for instant feedback
        self.primitive_panel.remove_marker_label(event_index, primitive)
        
        # Reset double-click state in the marker
        marker_obj = self.primitive_panel.draggable_points.get((event_index, primitive))
        if marker_obj:
            marker_obj.reset_double_click_state()
        
        # Recompute trajectory and update trajectory view
        self._recompute_trajectory_with_preview()
        
        print(f"=== END RESET ===")
    
    def commit_changes(self):
        """Commit all preview changes."""
        print("\n=== COMMIT CHANGES ===")
        print("Note: Markers already stored on drag. Commit just finalizes to model.")
        
        # Commit the changes to the model
        self.model.commit_all_previews(self.perspective)
        self.primitive_panel.commit_all_previews()
        self._update_all_views()
        
        # Recompute trajectory as committed
        self._recompute_trajectory_immediate()
        
        print(f"Total markers: {len(self.model.marker_positions)}")
        print("=== END COMMIT ===")
    
    def cancel_changes(self):
        """Cancel all preview changes."""
        self.model.clear_previews()
        self.primitive_panel.cancel_all_previews()
        
        # Recompute trajectory from committed state
        self._recompute_trajectory_immediate()
        
        print("Changes cancelled")
    
    def on_lock_toggle(self, event_index: int):
        """
        Handle lock/unlock toggle from right-click.
        
        Args:
            event_index: Index in events list
        """
        # Toggle in model
        new_lock_status = self.model.toggle_lock(event_index, self.perspective)
        
        # Update primitive panel visuals
        self.primitive_panel.update_lock_status(event_index, new_lock_status)
        
        print(f"Event {event_index} {'locked' if new_lock_status else 'unlocked'}")
    
    def _schedule_recomputation(self):
        """Schedule debounced trajectory recomputation (committed)."""
        # Cancel existing timer
        if self.debounce_timer and self.debounce_timer.is_alive():
            self.debounce_timer.cancel()
        
        # Schedule new computation after 300ms
        self.debounce_timer = threading.Timer(0.3, self._recompute_trajectory)
        self.debounce_timer.daemon = True  # Allow clean exit
        self.debounce_timer.start()
    
    def _schedule_recomputation_preview(self):
        """Schedule debounced trajectory recomputation (preview mode)."""
        # Cancel existing timer
        if self.debounce_timer and self.debounce_timer.is_alive():
            self.debounce_timer.cancel()
        
        # Schedule new computation after 300ms
        self.debounce_timer = threading.Timer(0.3, self._recompute_trajectory_with_preview)
        self.debounce_timer.daemon = True  # Allow clean exit
        self.debounce_timer.start()
    
    def cleanup(self):
        """Clean up resources (call on window close)."""
        if self.debounce_timer and self.debounce_timer.is_alive():
            self.debounce_timer.cancel()
    
    def _recompute_trajectory_immediate(self):
        """Immediate trajectory computation (no debounce)."""
        self._recompute_trajectory()
    
    def _recompute_trajectory(self):
        """Compute gamma_self trajectory from COMMITTED primitives."""
        self._compute_and_display(preview_mode=False)
    
    def _recompute_trajectory_with_preview(self):
        """Compute gamma_self trajectory INCLUDING preview changes."""
        self._compute_and_display(preview_mode=True)
    
    def _compute_and_display(self, preview_mode=False):
        """
        Compute trajectory and display.
        
        Args:
            preview_mode: If True, include preview changes in computation
        """
        # Import here to avoid circular dependency
        from PySide6.QtCore import QTimer
        
        # Show computing indicator (thread-safe via Qt signal)
        QTimer.singleShot(0, lambda: self.trajectory_panel.show_computing(True))
        
        events = self.model.get_events(self.perspective)
        
        if len(events) == 0:
            QTimer.singleShot(0, self.trajectory_panel.clear)
            return
        
        # Get primitives (with or without preview)
        primitives_data = self.model.get_primitives_array(self.perspective, include_preview=preview_mode)
        times = primitives_data['time']
        data = {
            'v': primitives_data['v'],
            'r': primitives_data['r'],
            'f': primitives_data['f'],
            'a': primitives_data['a'],
            'S': primitives_data['S']
        }
        
        # Compute gamma_self trajectory
        gamma_self = self.model.gamma_self_0  # Start from configured initial position
        gamma_trajectory = [gamma_self]
        
        for i in range(len(events) - 1):
            # Get primitives at current time
            v = data['v'][i]
            r = data['r'][i]
            f = data['f'][i]
            a = data['a'][i]
            S = data['S'][i]
            
            # Time delta
            dt = times[i + 1] - times[i]
            
            # Update gamma_self using GRP core
            gamma_self = update_gamma_self(
                gamma_self_current=gamma_self,
                v=v, r=r, f=f, a=a, S=S,
                time_delta=dt,
                weights=self.weights
            )
            gamma_trajectory.append(gamma_self)
        
        # Store preview trajectory for marker positioning
        if preview_mode:
            self._last_preview_trajectory = gamma_trajectory
        
        # Store or display
        self._display_trajectory(gamma_trajectory, preview_mode=preview_mode)
        
        self.dirty = False
    
    def _display_trajectory(self, gamma_trajectory, preview_mode=False):
        """
        Display computed trajectory.
        
        Args:
            gamma_trajectory: List of complex gamma_self values
            preview_mode: If True, show preview marker
        """
        events = self.model.get_events(self.perspective)
        
        # Extract real and imaginary components
        gamma_x = [g.real for g in gamma_trajectory]
        gamma_y = [g.imag for g in gamma_trajectory]
        
        # Build marked_data: {event_idx: set of modified primitives}
        marked_data = {}
        
        # Add committed modifications
        for event_idx, prims in self.model.modified_primitives.items():
            if event_idx not in marked_data:
                marked_data[event_idx] = set()
            marked_data[event_idx].update(prims)
        
        # Add preview modifications
        if preview_mode and self.model.preview_changes:
            for event_idx, prim_dict in self.model.preview_changes.items():
                if event_idx not in marked_data:
                    marked_data[event_idx] = set()
                marked_data[event_idx].update(prim_dict.keys())
        
        # Build pinned marker positions for gamma_self display
        # Format: [(event_idx, primitive, x, y, color), ...]
        pinned_markers = []
        print(f"\n=== DISPLAY TRAJECTORY (preview={preview_mode}) ===")
        print(f"marker_positions dict: {self.model.marker_positions}")
        
        for (event_idx, prim), gamma_pos in self.model.marker_positions.items():
            prim_colors = {'v': '#1f77b4', 'r': '#ff7f0e', 'f': '#2ca02c', 'a': '#d62728', 'S': '#9467bd'}
            marker = {
                'event_idx': event_idx,
                'primitive': prim,
                'x': gamma_pos.real,
                'y': gamma_pos.imag,
                'color': prim_colors.get(prim, 'orange'),
                'label': f"{event_idx}/{prim}"
            }
            pinned_markers.append(marker)
            print(f"  Building marker: {marker}")
        
        print(f"Total pinned_markers: {len(pinned_markers)}")
        print("=== END DISPLAY ===")
        
        # Find preview position (if in preview mode)
        preview_gamma = None
        if preview_mode and self.model.preview_changes:
            # Find last preview change index
            preview_idx = max(self.model.preview_changes.keys())
            if preview_idx < len(gamma_trajectory):
                preview_gamma = (gamma_x[preview_idx], gamma_y[preview_idx])
        
        # Store committed trajectory if not in preview
        if not preview_mode:
            self.committed_gamma_trajectory = gamma_trajectory
            print(f"[TRAJECTORY] Stored committed trajectory, final point: {gamma_trajectory[-1] if gamma_trajectory else 'empty'}")
        
        # Update trajectory panel (preserve view during edits)
        # Use QTimer to ensure GUI updates happen on main thread
        from PySide6.QtCore import QTimer
        preserve_view = preview_mode  # Keep view fixed during preview edits
        print(f"[TRAJECTORY] Calling update_trajectory with preserve_view={preserve_view}")
        
        # Schedule GUI update on main thread
        QTimer.singleShot(0, lambda: self._update_gui(
            gamma_x, gamma_y, marked_data, pinned_markers, preview_gamma, preserve_view
        ))
    
    def _update_gui(self, gamma_x, gamma_y, marked_data, pinned_markers, preview_gamma, preserve_view):
        """Update GUI components (must be called on main thread)."""
        self.trajectory_panel.update_trajectory(gamma_x, gamma_y, marked_data, 
                                               pinned_markers=pinned_markers,
                                               preview_gamma=preview_gamma,
                                               preserve_view=preserve_view)
        self.trajectory_panel.show_computing(False)
        
        # Update primitive panel markers
        self.primitive_panel.update_markers(marked_data)
    
    def _update_all_views(self):
        """Update all views from model."""
        events = self.model.get_events(self.perspective)
        self.primitive_panel.update_from_model(events)
    
    def save_scenario(self, filepath: str):
        """
        Save scenario to CSV file.
        
        Args:
            filepath: Output path
        """
        self.model.save_csv(filepath, self.perspective)
        print(f"Saved to {filepath}")
