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
    """
    
    def __init__(self, model, primitive_panel, trajectory_panel):
        """
        Initialize controller.
        
        Args:
            model: EditorModel instance
            primitive_panel: PrimitivePanel instance
            trajectory_panel: TrajectoryPanel instance
        """
        self.model = model
        self.primitive_panel = primitive_panel
        self.trajectory_panel = trajectory_panel
        
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
    
    def load_scenario(self, filepath: str):
        """
        Load scenario from CSV and update views.
        Args:
            filepath: Path to CSV file
        """
        # Load into model
        self.model.load_csv(filepath, self.perspective)

        # Store baseline primitives (for reset functionality)
        self.baseline_primitives = self.model.get_primitives_array(self.perspective, include_preview=False)

        # Mark all primitives for all events by default
        events = self.model.get_events(self.perspective)
        self.model.modified_primitives.clear()
        for event_idx, event in enumerate(events):
            self.model.modified_primitives[event_idx] = set(['v', 'r', 'f', 'a', 'S'])

        # Update views
        self._update_all_views()

        # Compute initial trajectory
        self._recompute_trajectory_immediate()
    
    def on_primitive_changed(self, event_index: int, primitive: str, value: float):
        """
        Handle primitive value change from UI drag (on release - store as preview).
        """
        self.model.update_primitive(event_index, primitive, value, self.perspective, preview=True)
        if event_index not in self.model.modified_primitives:
            self.model.modified_primitives[event_index] = set()
        self.model.modified_primitives[event_index].add(primitive)
        self._recompute_trajectory_with_preview()
        if hasattr(self, '_last_preview_trajectory') and self._last_preview_trajectory:
            marker_idx = event_index + 1 if event_index + 1 < len(self._last_preview_trajectory) else event_index
            gamma_pos = self._last_preview_trajectory[marker_idx]
            marker_key = (event_index, primitive)
            self.model.marker_positions[marker_key] = gamma_pos
            print(f"Marker {marker_key} → gamma_self[{marker_idx}] = {gamma_pos}")
            self._display_trajectory(self._last_preview_trajectory, preview_mode=True)
        self._update_all_views()
    
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
        Handle double-click reset to baseline CSV value.
        
        Args:
            event_index: Index in events list
            primitive: 'v', 'r', 'f', 'a', or 'S'
        """
        print(f"\n=== RESET PRIMITIVE {event_index}/{primitive} ===")
        
        # Get baseline value from CSV
        baseline_value = self.baseline_primitives[primitive][event_index]
        print(f"Resetting to baseline value: {baseline_value}")
        
        # Clear from preview changes
        if event_index in self.model.preview_changes:
            if primitive in self.model.preview_changes[event_index]:
                del self.model.preview_changes[event_index][primitive]
                print(f"Cleared from preview_changes")
            if not self.model.preview_changes[event_index]:
                del self.model.preview_changes[event_index]
        
        # Clear from modified primitives tracking
        if event_index in self.model.modified_primitives:
            if primitive in self.model.modified_primitives[event_index]:
                self.model.modified_primitives[event_index].discard(primitive)
                print(f"Cleared from modified_primitives")
            if not self.model.modified_primitives[event_index]:
                del self.model.modified_primitives[event_index]
        
        # Remove marker for this primitive
        marker_key = (event_index, primitive)
        if marker_key in self.model.marker_positions:
            del self.model.marker_positions[marker_key]
            print(f"Removed marker {marker_key}")
        
        # Reset the event primitive to baseline (directly, without marking as modified)
        events = self.model.get_events(self.perspective)
        setattr(events[event_index], primitive, baseline_value)
        self.model.dirty = True
        
        # Cancel preview on the draggable point (hide hollow marker, reset position)
        dp_key = (event_index, primitive)
        if dp_key in self.primitive_panel.draggable_points:
            dp = self.primitive_panel.draggable_points[dp_key]
            dp.original_y = baseline_value
            dp.y = baseline_value
            dp.point.set_ydata([baseline_value])
            dp.preview_point.set_visible(False)
        
        # Update primitive markers (clear annotations for reset event/primitive)
        self.primitive_panel.update_markers(self.model.modified_primitives)
        
        # Update the line data for the reset primitive
        primitives_data = self.model.get_primitives_array(self.perspective, include_preview=False)
        self.primitive_panel.lines[primitive].set_data(primitives_data['time'], primitives_data[primitive])
        self.primitive_panel.fig.canvas.draw_idle()
        
        # Recompute trajectory
        # If all markers are reset, clear fixed_view and manual view limits for auto-scaling
        if not self.model.modified_primitives:
            self.trajectory_panel.fixed_view = False
            self.trajectory_panel.manual_xlim = None
            self.trajectory_panel.manual_ylim = None
        self._recompute_trajectory_immediate()
        
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
        self.debounce_timer.start()
    
    def _schedule_recomputation_preview(self):
        """Schedule debounced trajectory recomputation (preview mode)."""
        # Cancel existing timer
        if self.debounce_timer and self.debounce_timer.is_alive():
            self.debounce_timer.cancel()
        
        # Schedule new computation after 300ms
        self.debounce_timer = threading.Timer(0.3, self._recompute_trajectory_with_preview)
        self.debounce_timer.start()
    
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
        # Show computing indicator
        self.trajectory_panel.show_computing(True)
        
        events = self.model.get_events(self.perspective)
        
        if len(events) == 0:
            self.trajectory_panel.clear()
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
        preserve_view = preview_mode  # Keep view fixed during preview edits
        print(f"[TRAJECTORY] Calling update_trajectory with preserve_view={preserve_view}")
        self.trajectory_panel.update_trajectory(gamma_x, gamma_y, marked_data, 
                                               pinned_markers=pinned_markers,
                                               preview_gamma=preview_gamma,
                                               preserve_view=preserve_view)
        self.trajectory_panel.show_computing(False)
        
        # Update primitive panel markers
        self.primitive_panel.update_markers(marked_data)
    
    def _update_all_views(self):
        """Update all views from model."""
        primitives = self.model.get_primitives_array(self.perspective)
        events = self.model.get_events(self.perspective)
        self.primitive_panel.update_from_model(primitives, events)
    
    def save_scenario(self, filepath: str):
        """
        Save scenario to CSV file.
        
        Args:
            filepath: Output path
        """
        self.model.save_csv(filepath, self.perspective)
        print(f"Saved to {filepath}")
