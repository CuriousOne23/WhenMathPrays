"""
Controller for interactive scenario editor.

Coordinates between model and views, handles trajectory computation.
"""

import threading
import numpy as np
import pandas as pd
from typing import Optional, List
from PySide6.QtCore import QTimer
from tools.editor.constants import PRIMITIVE_NAMES, is_inserted_event
from tools.editor.editor_constants import FLOAT_TOLERANCE, TIME_MATCH_TOLERANCE
from tools.editor.editor_state import EditorState, PerspectiveState, FileLoadState
from tools.editor.editor_utils import (
    remove_event_markers, clear_modified_primitives_for_event,
    get_all_modified_markers, update_baseline_arrays
)

# Import GRP core
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.love import update_gamma_self, DEFAULT_WEIGHTS


class EditorController:
    """
    Main controller coordinating model and views.
    
    Architecture (Phase 3 refactoring - Clean MVC):
    - Owns model and view references (but views don't reference back)
    - Connects view signals to controller methods
    - Updates model based on user actions
    - Pushes model state to views via method calls
    - Views never access controller or model directly
    
    Handles:
    - Primitive value changes from UI (via signals)
    - Debounced trajectory recomputation
    - Lock/unlock actions
    - Auto-marking of modified events
    - Undo/Redo command management
    - Modified state synchronization to views
    """
    
    def __init__(self, model, primitive_panel, trajectory_panel, undo_stack=None, editor_state=None):
        """
        Initialize controller.
        
        Args:
            model: EditorModel instance
            primitive_panel: PrimitivePanel instance
            trajectory_panel: TrajectoryPanel instance
            undo_stack: QUndoStack instance (optional)
            editor_state: EditorState instance (optional, creates new if None)
        """
        self.model = model
        self.primitive_panel = primitive_panel
        self.trajectory_panel = trajectory_panel
        self.undo_stack = undo_stack
        
        # Centralized state management
        self.state = editor_state if editor_state is not None else EditorState()
        
        # Set up observer pattern for automatic cache invalidation
        self.model.modified_primitives.add_observer(self._on_modified_primitives_changed)
        
        self.debounce_timer: Optional[threading.Timer] = None
        
        # GRP computation parameters
        self.weights = DEFAULT_WEIGHTS.copy()
        self.delta_t = 1.0  # Time step for trajectory computation
        
        # Track last committed trajectory for comparison
        self.committed_gamma_trajectory = None
        
        # Store baseline values (from CSV) using time-keyed dictionary for reset
        # Key: (time, primitive) -> Value: baseline_value
        self.baseline_by_time = {}
    
    @property
    def perspective(self) -> str:
        """Get current perspective as string (for backward compatibility)."""
        return self.state.perspective.value
    
    @property
    def dirty(self) -> bool:
        """Get dirty flag from state (for backward compatibility)."""
        return self.state.dirty
    
    @property
    def initial_load_complete(self) -> bool:
        """Get initial load complete flag from state."""
        return self.state.initial_load_complete
    
    @initial_load_complete.setter
    def initial_load_complete(self, value: bool):
        """Set initial load complete flag in state."""
        self.state.initial_load_complete = value
    
    @property
    def in_undo_redo(self) -> bool:
        """Get undo/redo operation flag from state."""
        return self.state.is_in_undo_operation()
    
    def load_scenario(self, m1_filepath: str, m2_filepath: Optional[str] = None):
        """
        Load scenario from CSV and update views.
        
        Args:
            m1_filepath: Path to M1 CSV file
            m2_filepath: Path to M2 CSV file (None if doesn't exist)
        """
        # Load M1 data
        self.model.load_csv(m1_filepath, "M1")
        
        # Load M2 data if provided
        if m2_filepath:
            self.model.load_csv(m2_filepath, "M2")
            self.state.set_file_load_state(FileLoadState.DUAL_PERSPECTIVE)
        else:
            # Single file loaded - determine if M1 or M2
            # This is set later by interactive_editor based on file detection
            pass

        # Store baseline primitives using time-keyed dictionary (insertion-proof!)
        temp_primitives = self.model.get_primitives_array(self.perspective, include_preview=False)
        self.baseline_by_time = {}
        for i, time in enumerate(temp_primitives['time']):
            for prim in ['v', 'r', 'f', 'a', 'S']:
                key = (float(time), prim)
                self.baseline_by_time[key] = float(temp_primitives[prim][i])

        # Initialize modified_primitives as empty - will track user modifications only
        events = self.model.get_events(self.perspective)
        self.model.modified_primitives.clear()
        # Don't mark anything as modified on load - user hasn't modified anything yet

        # Set scenario name on both panels
        display_name = self.model.get_display_name(self.perspective)
        self.primitive_panel.set_scenario_name(display_name)
        self.trajectory_panel.set_scenario_name(display_name)

        # Update views
        self._update_all_views()

        # Compute initial trajectory (allow auto-zoom on first load)
        self.initial_load_complete = False
        self._recompute_trajectory_immediate()
        self.initial_load_complete = True  # Preserve view on all subsequent updates
    
    def switch_perspective(self, perspective: str):
        """
        Switch between M1 and M2 perspectives.
        
        Args:
            perspective: Either 'M1' or 'M2'
        """
        if perspective not in ['M1', 'M2']:
            raise ValueError(f"Invalid perspective: {perspective}. Must be 'M1' or 'M2'")
        
        if perspective == self.perspective:
            return  # Already on this perspective
        
        # Update perspective using state transition
        old_perspective = self.perspective
        target_state = PerspectiveState.M1 if perspective == 'M1' else PerspectiveState.M2
        self.state.switch_perspective(target_state)
        
        # Update display name on panels
        display_name = self.model.get_display_name(perspective)
        self.primitive_panel.set_scenario_name(display_name)
        self.trajectory_panel.set_scenario_name(display_name)
        
        # Update all views with new perspective data
        self._update_all_views()
        
        # Recompute trajectory for new perspective
        self._recompute_trajectory_immediate()
    
    def has_dual_perspective(self) -> bool:
        """
        Check if both M1 and M2 perspectives have data loaded.
        
        Used to determine whether to show perspective switcher UI and enable
        dual-perspective overlay visualization.
        
        Returns:
            True if both M1 and M2 have events loaded, False if only one perspective
        """
        return (hasattr(self.model, 'events_m1') and len(self.model.events_m1) > 0 and
                hasattr(self.model, 'events_m2') and len(self.model.events_m2) > 0)
    
    def on_diagnostic_marker_placed(self, event_idx: int):
        """
        Handle diagnostic marker placement from shift+click.
        Updates both primitive and gamma_self gauges, and places marker on trajectory.
        
        Args:
            event_idx: Event index where marker was placed
        """
        if not self.events_data or event_idx >= len(self.events_data):
            return
        
        event = self.events_data[event_idx]
        
        # Update primitive readout for first primitive (or could cycle through all)
        # For now, just show the time in the gauge
        if hasattr(self.primitive_panel, '_update_readout'):
            # Show marker on first primitive with non-zero value
            for prim in ['v', 'r', 'f', 'a', 'S']:
                value = event.markers[prim].value
                if abs(value) > FLOAT_TOLERANCE:
                    self.primitive_panel._update_readout(event_idx, prim, value)
                    break
        
        # Get gamma_self value at this event
        if hasattr(self, 'committed_gamma_trajectory') and self.committed_gamma_trajectory:
            if event_idx < len(self.committed_gamma_trajectory):
                gamma_val = self.committed_gamma_trajectory[event_idx]
                gamma_x = gamma_val.real
                gamma_y = gamma_val.imag
                
                # Place marker on trajectory
                self.trajectory_panel.place_diagnostic_marker(gamma_x, gamma_y)
                
                # Update gamma_self readout
                # The gamma_clicked signal handler will update the gauge
                # We can call it directly or emit the signal
                self.on_gamma_clicked(gamma_x, gamma_y)
                
                print(f"[DIAGNOSTIC] Event {event_idx} @ time={event.time}: gamma_self=({gamma_x:.2f}, {gamma_y:.2f})")
    
    def on_primitive_changed(self, event_index: int, primitive: str, value: float):
        """
        Handle primitive value change from UI drag (on release - commit to model).
        
        This is called when the user releases a draggable marker, finalizing the edit.
        Creates an undo command and updates the model, then recomputes the trajectory.
        
        Args:
            event_index: Index of the event being modified
            primitive: Name of primitive ('v', 'r', 'f', 'a', or 'S')
            value: New value for the primitive
        """
        print(f"[UNDO_DEBUG] on_primitive_changed called: event={event_index}, prim={primitive}, value={value:.2f}")
        # Get old value for undo
        old_value = self.model.get_event(event_index, self.perspective).markers[primitive].value
        print(f"[UNDO_DEBUG] old_value={old_value:.2f}, undo_stack={self.undo_stack is not None}, in_undo={self.state.is_in_undo_operation()}")
        
        # Skip if no actual change
        if abs(value - old_value) < FLOAT_TOLERANCE:
            print(f"[UNDO_DEBUG] Skipping - no change")
            return
        
        # Create undo command and push to stack (unless we're in undo/redo)
        if self.undo_stack and not self.state.is_in_undo_operation():
            from tools.editor.commands import EditPrimitiveCommand
            command = EditPrimitiveCommand(self, event_index, primitive, old_value, value)
            print(f"[UNDO] Pushing EditPrimitiveCommand to stack (event={event_index}, prim={primitive}, {old_value:.2f}->{value:.2f})")
            self.undo_stack.push(command)
            print(f"[UNDO] Stack size now: {self.undo_stack.count()}, can undo: {self.undo_stack.canUndo()}")
            return  # Command.redo() will handle the update
        
        # If no undo stack or in undo/redo, apply directly
        print(f"[UNDO_DEBUG] NOT creating undo command - applying directly")
        self._apply_primitive_change(event_index, primitive, value)
        # Commit the new value to the model
        self.model.update_primitive(event_index, primitive, value, self.perspective, preview=False)
        events = self.model.get_events(self.perspective)
        event_time = events[event_index].time
        if event_time not in self.model.modified_primitives:
            self.model.modified_primitives[event_time] = set()
        self.model.modified_primitives[event_time].add(primitive)
        
        # Store marker position from committed trajectory (must happen before display)
        # First compute trajectory to get the position
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
        
        # Store marker position using time as key
        marker_idx = event_index + 1 if event_index + 1 < len(gamma_trajectory) else event_index
        gamma_pos = gamma_trajectory[marker_idx]
        marker_key = (event_time, primitive)
        self.model.marker_positions[marker_key] = gamma_pos
        print(f"Marker ({event_time}, {primitive}) -> gamma_self[{marker_idx}] = {gamma_pos}")
        
        # === Phase 3: Incremental Update ===
        # Query modified status from Model (single source of truth)
        is_modified = self.model.is_primitive_modified(event_index, primitive, self.perspective)
        
        # Update only this marker in PrimitivePanel (O(1) operation)
        self.primitive_panel.update_marker(event_index, primitive, value, is_modified)
        
        # Update trajectory panel (full recompute, but marker update was instant)
        self._recompute_trajectory_immediate()
        # Note: trajectory panel updated via _display_trajectory
    
    def _apply_primitive_change(self, event_index: int, primitive: str, value: float):
        """
        Apply primitive change without undo tracking (used by undo commands).
        
        Updates the model and marker positions, checking if the value is back to baseline
        to determine modified state. Does not create undo commands (used internally by
        undo/redo operations to avoid infinite recursion).
        
        Args:
            event_index: Index of the event being modified
            primitive: Name of primitive ('v', 'r', 'f', 'a', or 'S')
            value: New value for the primitive
        
        Side Effects:
            - Updates model.modified_primitives dictionary
            - Updates model.marker_positions for trajectory visualization
            - Triggers incremental UI update for the modified marker
        """
        # Commit the new value to the model
        self.model.update_primitive(event_index, primitive, value, self.perspective, preview=False)
        
        # Check if this value is back to baseline
        events = self.model.get_events(self.perspective)
        event_time = events[event_index].time
        
        # Use time-keyed baseline (insertion-proof!)
        baseline_value = self.baseline_by_time[(event_time, primitive)]
        
        if abs(value - baseline_value) < FLOAT_TOLERANCE:
            # Back to baseline, remove from modified set
            if event_time in self.model.modified_primitives:
                self.model.modified_primitives[event_time].discard(primitive)
                if not self.model.modified_primitives[event_time]:
                    del self.model.modified_primitives[event_time]
            
            # Also remove marker position so it doesn't show on gamma_self graph
            marker_key = (event_time, primitive)
            if marker_key in self.model.marker_positions:
                del self.model.marker_positions[marker_key]
            
            # Remove the label from primitive panel
            self.primitive_panel.remove_marker_label(event_time, primitive)
        else:
            # Modified, add to set
            if event_time not in self.model.modified_primitives:
                self.model.modified_primitives[event_time] = set()
            self.model.modified_primitives[event_time].add(primitive)
            
            # Add or update the label
            self.primitive_panel._add_marker_label(event_time, primitive, value)
        
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
        if self.model.is_primitive_modified(event_index, primitive, self.perspective):
            marker_idx = event_index + 1 if event_index + 1 < len(gamma_trajectory) else event_index
            gamma_pos = gamma_trajectory[marker_idx]
            marker_key = (event_time, primitive)
            self.model.marker_positions[marker_key] = gamma_pos
            print(f"Marker ({event_time}, {primitive}) -> gamma_self[{marker_idx}] = {gamma_pos}")
        else:
            print(f"Primitive {event_index}/{primitive} (time {event_time}) back to baseline, not storing marker position")
        
        # === Phase 3: Incremental Update ===
        # Query modified status from Model (single source of truth)
        is_modified = self.model.is_primitive_modified(event_index, primitive, self.perspective)
        
        # Update only this marker in PrimitivePanel (O(1) operation)
        self.primitive_panel.update_marker(event_index, primitive, value, is_modified)
        
        # Add or update marker label if modified, remove if back to baseline
        event = self.model.get_event(event_index, self.perspective)
        if is_modified:
            # Use time-based key (survives insertion/deletion)
            self.primitive_panel._add_marker_label(event.time, primitive, value)
        else:
            self.primitive_panel.remove_marker_label(event.time, primitive)
        
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
        self.state.mark_dirty()
        self._schedule_recomputation_preview()
    
    def on_primitive_reset(self, event_index: int, primitive: str):
        """
        Handle double-click reset to baseline CSV value using Event/Marker objects.
        Args:
            event_index: Index in events list
            primitive: 'v', 'r', 'f', 'a', or 'S'
        """
        print(f"\n=== RESET PRIMITIVE {event_index}/{primitive} ===")
        
        try:
            # Get current value
            old_value = self.model.get_event(event_index, self.perspective).markers[primitive].value
            
            # Get original CSV baseline value using time-based lookup
            event = self.model.get_event(event_index, self.perspective)
            event_time = event.time
            
            # Check if this time exists in original baseline (not an inserted event)
            key = (event_time, primitive)
            if key in self.baseline_by_time:
                baseline_value = self.baseline_by_time[key]
                print(f"Resetting to baseline value: {baseline_value} (from original CSV at time {event_time})")
            else:
                # Inserted event - reset to 0
                baseline_value = 0.0
                print(f"Event at time {event_time} is inserted (not in original CSV), resetting to 0")
        except Exception as e:
            print(f"ERROR getting values: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Skip if already at baseline
        if abs(old_value - baseline_value) < FLOAT_TOLERANCE:
            print(f"Already at baseline, skipping")
            return
        
        # Create undo command and push to stack (unless we're in undo/redo)
        if self.undo_stack and not self.state.is_in_undo_operation():
            from tools.editor.commands import ResetPrimitiveCommand
            command = ResetPrimitiveCommand(self, event_index, primitive, old_value, baseline_value)
            print(f"[UNDO] Pushing ResetPrimitiveCommand to stack (event={event_index}, prim={primitive}, {old_value:.2f}->{baseline_value:.2f})")
            self.undo_stack.push(command)
            print(f"[UNDO] Stack size now: {self.undo_stack.count()}, can undo: {self.undo_stack.canUndo()}")
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
        try:
            # Reset using Model's method (Phase 1 query interface)
            self.model.reset_event_primitive(event_index, primitive, baseline_value, self.perspective)
            
            event = self.model.get_event(event_index, self.perspective)
            print(f"Reset complete. Event {event_index} (time={event.time}), modified_primitives: {self.model.modified_primitives}")
            
            # Remove marker position for this primitive (using time-based key)
            marker_key = (event.time, primitive)
            if marker_key in self.model.marker_positions:
                del self.model.marker_positions[marker_key]
                print(f"Removed marker position for {marker_key}")
            else:
                print(f"No marker position found for {marker_key}")
            
            # === Phase 3: Incremental Update ===
            # Update only this marker in PrimitivePanel (O(1) operation)
            is_modified = self.model.is_modified(event_index, primitive, self.perspective)
            print(f"After reset, is_modified({event_index}, {primitive}) = {is_modified}")
            self.primitive_panel.update_marker(event_index, primitive, baseline_value, is_modified)
            
            # Remove the marker label (use time-based key)
            self.primitive_panel.remove_marker_label(event.time, primitive)
            
            # Force visual refresh by calling update_marker again (ensures marker becomes filled)
            self.primitive_panel.update_marker(event_index, primitive, baseline_value, False)
            
            # Reset double-click state in the marker
            marker_obj = self.primitive_panel.draggable_points.get((event_index, primitive))
            if marker_obj:
                marker_obj.reset_double_click_state()
            
            # Recompute trajectory WITHOUT preview (this is a committed change, not a preview)
            self._recompute_trajectory_immediate()
            
            print(f"=== END RESET ===")
        except Exception as e:
            print(f"ERROR in _apply_primitive_reset: {e}")
            import traceback
            traceback.print_exc()
    
    def _delete_event(self, event_index: int):
        """
        Delete an event (used by undo commands).
        
        Args:
            event_index: Event index to delete
        """
        try:
            print(f"\n=== DELETE EVENT {event_index} ===")
            
            # Get event data before deletion
            events = self.model.get_events(self.perspective)
            event = events[event_index]
            event_time = event.time
            
            # Delete from model
            del events[event_index]
            
            # Remove from modified primitives tracking
            clear_modified_primitives_for_event(self.model, event_time)
            
            # Remove marker positions and labels for this event
            remove_event_markers(
                self.model, 
                event_time,
                remove_label_callback=self.primitive_panel.remove_marker_label,
                event_index=event_index
            )
            
            print(f"Deleted event at time={event_time}, remaining events: {len(events)}")
            
            # Update baseline - remove entries for deleted time
            for prim in ['v', 'r', 'f', 'a', 'S']:
                key = (event_time, prim)
                if key in self.baseline_by_time:
                    del self.baseline_by_time[key]
                    print(f"  Removed baseline entry: {key}")
            
            # Update views
            self.primitive_panel.update_from_model(events)
            self._recompute_trajectory_immediate()
            
            print("=== END DELETE ===")
        except Exception as e:
            print(f"ERROR in _delete_event: {e}")
            import traceback
            traceback.print_exc()
    
    def _insert_event(self, event_index: int, event_data: dict):
        """
        Insert an event (used by undo commands to restore deleted events).
        
        Args:
            event_index: Event index to insert at
            event_data: Dict with 'time', 'primitives', 'notes', 'locked'
        """
        try:
            print(f"\n=== INSERT EVENT at index {event_index} ===")
            
            # Import Event class from the correct module
            from tools.editor.event import Event
            
            # Create event using the actual Event class constructor
            event = Event(
                time=event_data['time'],
                primitives=event_data['primitives'],
                notes=event_data.get('notes', ''),
                marker='',  # Markers aren't preserved for now
                locked=event_data.get('locked', False)
            )
            
            # Insert into model
            events = self.model.get_events(self.perspective)
            events.insert(event_index, event)
            
            print(f"Inserted event at time={event_data['time']}, total events: {len(events)}")
            
            # Update baseline - add entries for inserted time
            for prim in ['v', 'r', 'f', 'a', 'S']:
                key = (event_data['time'], prim)
                self.baseline_by_time[key] = event_data['primitives'][prim]
                print(f"  Added baseline entry: {key} = {event_data['primitives'][prim]}")
            
            # Update views
            self.primitive_panel.update_from_model(events)
            self._recompute_trajectory_immediate()
            
            print("=== END INSERT ===")
        except Exception as e:
            print(f"ERROR in _insert_event: {e}")
            import traceback
            traceback.print_exc()
    
    def _insert_event_before(self, event_idx, insert_time, delta):
        """
        Insert new event at insert_time and shift event_idx+ forward by delta.
        
        Args:
            event_idx: Index where new event will be inserted
            insert_time: Time for new event
            delta: Time delta to shift subsequent events (from previous event to insert_time)
        """
        try:
            print(f"\n=== INSERT EVENT at time {insert_time} (index {event_idx}) ===")
            print(f"Delta for shifting subsequent events: {delta}")
            
            from tools.editor.event import Event
            from tools.editor.commands import DeleteEventCommand
            
            events = self.model.get_events(self.perspective)
            
            # Check if we're reinserting a recently deleted event with the same time
            # Look through undo stack for DeleteEventCommand with matching time
            restored_primitives = None
            if self.undo_stack:
                # Check the most recent command (top of stack)
                if self.undo_stack.count() > 0:
                    last_cmd = self.undo_stack.command(self.undo_stack.count() - 1)
                    if isinstance(last_cmd, DeleteEventCommand):
                        deleted_time = last_cmd.event_data['time']
                        if abs(deleted_time - insert_time) < 0.1:  # Same time
                            restored_primitives = last_cmd.event_data['primitives'].copy()
                            print(f"[RESTORE] Found deleted event at t={deleted_time}, restoring primitives: {restored_primitives}")
            
            # Create new event - use restored primitives if available, otherwise zeros
            if restored_primitives:
                new_event = Event(
                    time=insert_time,
                    primitives=restored_primitives,
                    notes='',
                    marker='',
                    locked=False
                )
            else:
                new_event = Event(
                    time=insert_time,
                    primitives={'v': 0.0, 'r': 0.0, 'f': 0.0, 'a': 0.0, 'S': 0.0},
                    notes='',
                    marker='',
                    locked=False
                )
            
            # FIRST: Shift all events from event_idx onwards forward by delta
            # This creates the gap where we'll insert the new event
            print(f"STEP 1: Shift events from index {event_idx} onwards by +{delta}")
            
            # Collect shifted times for marker position updates
            time_shifts = []  # [(old_time, new_time), ...]
            for idx in range(event_idx, len(events)):
                old_time = events[idx].time
                events[idx].time = old_time + delta
                time_shifts.append((old_time, old_time + delta))
                print(f"  Shifted event {idx}: {old_time} -> {events[idx].time}")
            
            # Update marker_positions keys for shifted times
            # Markers at shifted events need their keys updated
            print(f"STEP 1b: Update marker position keys for shifted times")
            new_marker_positions = {}
            for (old_time, prim), gamma_pos in list(self.model.marker_positions.items()):
                # Check if this marker's time was shifted
                shifted_time = None
                for shift_old, shift_new in time_shifts:
                    if abs(old_time - shift_old) < TIME_MATCH_TOLERANCE:
                        shifted_time = shift_new
                        break
                
                if shifted_time:
                    # Update the key to the new time
                    new_key = (shifted_time, prim)
                    new_marker_positions[new_key] = gamma_pos
                    print(f"  Updated marker key: ({old_time}, {prim}) -> ({shifted_time}, {prim})")
                else:
                    # Keep the old key
                    new_marker_positions[(old_time, prim)] = gamma_pos
            
            self.model.marker_positions = new_marker_positions
            
            # Update primitive panel labels for shifted times
            print(f"STEP 1b2: Update primitive panel labels for shifted times")
            for shift_old, shift_new in time_shifts:
                # For each primitive that has a label at the old time
                for prim in ['v', 'r', 'f', 'a', 'S']:
                    # Remove old label if it exists
                    try:
                        self.primitive_panel.remove_marker_label(shift_old, prim)
                        print(f"  Removed label at time {shift_old}, prim {prim}")
                    except:
                        pass  # Label didn't exist, that's fine
                    
                    # Check if this primitive should have a label at the new time
                    if shift_new in self.model.modified_primitives and prim in self.model.modified_primitives[shift_new]:
                        # Get the value from the event
                        events = self.model.get_events(self.perspective)
                        for idx, evt in enumerate(events):
                            if abs(evt.time - shift_new) < TIME_MATCH_TOLERANCE:
                                value = evt.markers[prim].value
                                self.primitive_panel._add_marker_label(shift_new, prim, value)
                                print(f"  Added label at time {shift_new}, prim {prim}, value {value}")
                                break
            
            # Update modified_primitives keys for shifted times
            print(f"STEP 1c: Update modified_primitives keys for shifted times")
            new_modified_primitives = {}
            for time_key, prim_set in list(self.model.modified_primitives.items()):
                # Check if this time was shifted
                shifted_time = None
                for shift_old, shift_new in time_shifts:
                    if abs(time_key - shift_old) < TIME_MATCH_TOLERANCE:
                        shifted_time = shift_new
                        break
                
                if shifted_time:
                    new_modified_primitives[shifted_time] = prim_set
                    print(f"  Updated modified_primitives key: {time_key} -> {shifted_time}")
                else:
                    new_modified_primitives[time_key] = prim_set
            
            self.model.modified_primitives = new_modified_primitives
            
            # THIRD: Insert new event at the calculated position
            events.insert(event_idx, new_event)
            print(f"STEP 2: Inserted new event at index {event_idx}, time={insert_time}")
            
            # Update baseline with time-keyed dictionary
            print(f"STEP 3: Update baseline for inserted event and shifted times")
            
            # For shifted times, update baseline keys (delete old, add new with same values)
            for shift_old, shift_new in time_shifts:
                for prim in ['v', 'r', 'f', 'a', 'S']:
                    old_key = (shift_old, prim)
                    new_key = (shift_new, prim)
                    if old_key in self.baseline_by_time:
                        # Preserve baseline value across time shift
                        baseline_val = self.baseline_by_time[old_key]
                        del self.baseline_by_time[old_key]
                        self.baseline_by_time[new_key] = baseline_val
                        print(f"  Shifted baseline key: {old_key} -> {new_key} (value={baseline_val})")
            
            # Add baseline for newly inserted event (neutral 0.0 values)
            prim_values = {prim: new_event.markers[prim].value if restored_primitives else 0.0 for prim in PRIMITIVE_NAMES}
            for prim in ['v', 'r', 'f', 'a', 'S']:
                key = (insert_time, prim)
                self.baseline_by_time[key] = prim_values[prim]
                print(f"  Added baseline for inserted event: {key} = {prim_values[prim]}")
            
            # Debug: verify event times before update_from_model
            print("\n[DEBUG] Event times before update_from_model:")
            for idx, evt in enumerate(events):
                print(f"  idx={idx}: time={evt.time}")
            
            self.primitive_panel.update_from_model(events)
            self._recompute_trajectory_immediate()
            
            print(f"Total events after insert: {len(events)}")
            print("=== END INSERT ===")
        except Exception as e:
            print(f"ERROR in _insert_event_before: {e}")
            import traceback
            traceback.print_exc()
    
    def _undo_insert_event_before(self, event_idx, shifted_events):
        """
        Undo insertion by removing event and restoring original times.
        
        Args:
            event_idx: Index of inserted event to remove
            shifted_events: List of (idx, old_time, new_time) tuples
        """
        try:
            print(f"\n=== UNDO INSERT BEFORE (remove index {event_idx}) ===")
            
            events = self.model.get_events(self.perspective)
            
            # Remove the inserted event
            removed_event = events.pop(event_idx)
            print(f"Removed event at time={removed_event.time}")
            
            # Restore original times
            # After removal, indices are back to their original positions
            for orig_idx, old_time, new_time in shifted_events:
                events[orig_idx].time = old_time
                print(f"  Restored event {orig_idx}: {new_time} -> {old_time}")
            
            # Update marker_position keys: shift back from new_time to old_time
            print("Restoring marker position keys:")
            new_marker_positions = {}
            for key, gamma_pos in list(self.model.marker_positions.items()):
                time, prim = key
                # Check if this time was shifted
                restored = False
                for orig_idx, old_time, new_time in shifted_events:
                    if abs(time - new_time) < 0.001:  # This was shifted
                        new_key = (old_time, prim)
                        new_marker_positions[new_key] = gamma_pos
                        print(f"  Restored marker key: ({new_time}, {prim}) -> ({old_time}, {prim})")
                        restored = True
                        break
                if not restored:
                    new_marker_positions[key] = gamma_pos
            self.model.marker_positions = new_marker_positions
            
            # Update primitive panel labels for restored times
            print("Restoring primitive panel labels:")
            for orig_idx, old_time, new_time in shifted_events:
                for prim in ['v', 'r', 'f', 'a', 'S']:
                    # Remove label at shifted time
                    try:
                        self.primitive_panel.remove_marker_label(new_time, prim)
                        print(f"  Removed label at time {new_time}, prim {prim}")
                    except:
                        pass
                    
                    # Add label at restored time if marker exists
                    if (old_time, prim) in self.model.marker_positions:
                        evt = events[orig_idx]
                        value = getattr(evt.markers[prim], 'value', None)
                        if value is not None:
                            self.primitive_panel._add_marker_label(old_time, prim, value)
                            print(f"  Added label at time {old_time}, prim {prim}, value={value:.2f}")
            
            # Update modified_primitives keys: shift back from new_time to old_time
            print("Restoring modified_primitives keys:")
            new_modified_primitives = {}
            for time, prims in list(self.model.modified_primitives.items()):
                restored = False
                for orig_idx, old_time, new_time in shifted_events:
                    if abs(time - new_time) < 0.001:  # This was shifted
                        new_modified_primitives[old_time] = prims
                        print(f"  Restored modified_primitives key: {new_time} -> {old_time}")
                        restored = True
                        break
                if not restored:
                    new_modified_primitives[time] = prims
            self.model.modified_primitives = new_modified_primitives
            
            # Update baseline - remove inserted event and shift back times
            print("Updating baseline:")
            
            # Remove baseline for inserted event
            for prim in ['v', 'r', 'f', 'a', 'S']:
                key = (removed_event.time, prim)
                if key in self.baseline_by_time:
                    del self.baseline_by_time[key]
                    print(f"  Removed baseline for inserted event: {key}")
            
            # Shift baseline keys back to original times
            for orig_idx, old_time, new_time in shifted_events:
                for prim in ['v', 'r', 'f', 'a', 'S']:
                    new_key = (new_time, prim)
                    old_key = (old_time, prim)
                    if new_key in self.baseline_by_time:
                        # Restore baseline with old time key
                        baseline_val = self.baseline_by_time[new_key]
                        del self.baseline_by_time[new_key]
                        self.baseline_by_time[old_key] = baseline_val
                        print(f"  Shifted baseline key: {new_key} -> {old_key} (value={baseline_val})")
            
            # Update views
            self.primitive_panel.update_from_model(events)
            self._recompute_trajectory_immediate()
            
            print(f"Total events after undo: {len(events)}")
            print("=== END UNDO INSERT BEFORE ===")
        except Exception as e:
            print(f"ERROR in _undo_insert_event_before: {e}")
            import traceback
            traceback.print_exc()
    
    def commit_changes(self):
        """
        Commit all preview changes to the model (finalize drag operations).
        
        Called when user releases mouse after dragging a marker. Moves changes from
        model.preview_changes to permanent state and triggers full UI update.
        """
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
        """
        Cancel all preview changes and revert to committed state.
        
        Clears model.preview_changes and restores UI to last committed values.
        Used when user cancels a drag operation or on escape key.
        """
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
    
    def insert_event_at_time(self, time: float):
        """
        Insert a new event at specified time with primitives set to 0 (neutral).
        Updates views immediately after insertion.
        
        Args:
            time: Time value for new event
        """
        # Insert into model
        new_idx = self.model.insert_event(time, self.perspective)
        
        # Update baseline primitives to include new event
        self._update_baseline_after_insert(new_idx)
        
        # Update all views immediately (shows dashed lines and markers at y=0)
        self._update_all_views()
        
        # Recompute trajectory (since primitives are 0, this should be fast)
        self._recompute_trajectory_immediate()
    
    def insert_event_at_time_no_update(self, time: float):
        """
        Insert a new event WITHOUT updating views (for batch operations).
        Caller must call _update_all_views() and _recompute_trajectory_immediate() after all insertions.
        
        Args:
            time: Time value for new event
        """
        # Insert into model
        new_idx = self.model.insert_event(time, self.perspective)
        
        # Update baseline primitives to include new event
        self._update_baseline_after_insert(new_idx)
    
    def delete_event_at_index(self, event_index: int):
        """
        Delete event at specified index.
        Updates views immediately after deletion.
        
        Args:
            event_index: Index of event to delete
        
        Raises:
            ValueError: If event is locked or first/last event
        """
        # Delete from model (will raise ValueError if locked or endpoint)
        deleted_event = self.model.delete_event(event_index, self.perspective)
        
        # Update baseline primitives to remove deleted event
        self._update_baseline_after_delete(event_index)
        
        # Update all views
        self._update_all_views()
        
        # Recompute trajectory
        self._recompute_trajectory_immediate()
        
        print(f"Deleted event at index {event_index}, time {deleted_event.time}")
    
    def delete_event_at_index_no_update(self, event_index: int):
        """
        Delete event WITHOUT updating views (for batch operations).
        Caller must call _update_all_views() and _recompute_trajectory_immediate() after all deletions.
        
        Args:
            event_index: Index of event to delete
        
        Raises:
            ValueError: If event is locked or first/last event
        """
        # Delete from model (will raise ValueError if locked or endpoint)
        deleted_event = self.model.delete_event(event_index, self.perspective)
        
        # Update baseline primitives to remove deleted event
        self._update_baseline_after_delete(event_index)
        
        return deleted_event
    
    def _update_baseline_after_insert(self, insert_idx: int):
        """Update baseline primitives after inserting an event."""
        events = self.model.get_events(self.perspective)
        new_event = events[insert_idx]
        
        # Add baseline entries for new time point (inserted events start at neutral 0.0)
        for prim in ['v', 'r', 'f', 'a', 'S']:
            key = (new_event.time, prim)
            self.baseline_by_time[key] = 0.0
        print(f"[BASELINE] Added time-keyed entries for t={new_event.time}")
        
        # NOTE: modified_primitives shifting is already handled by model.insert_event()
        # NOTE: marker_positions uses time-based keys, so they remain valid after insertion
    
    def _update_baseline_after_delete(self, deleted_idx: int):
        """Update baseline primitives after deleting an event.
        
        Args:
            deleted_idx: Index of the deleted event
        """
        # Get deleted event (still in list at this point)
        events = self.model.get_events(self.perspective)
        if deleted_idx < len(events):
            deleted_time = events[deleted_idx].time
            
            # Remove baseline entries for deleted time point
            for prim in ['v', 'r', 'f', 'a', 'S']:
                key = (deleted_time, prim)
                if key in self.baseline_by_time:
                    del self.baseline_by_time[key]
            print(f"[BASELINE] Removed time-keyed entries for t={deleted_time}")
        
        # NOTE: modified_primitives and marker_positions use time-based keys
        # so they remain valid after deletion (handled by model.delete_event())
    
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
        if self.debounce_timer and self.debounce_timer.isActive():
            self.debounce_timer.stop()
        
        # Create timer if needed
        if not self.debounce_timer:
            self.debounce_timer = QTimer()
            self.debounce_timer.setSingleShot(True)
            self.debounce_timer.timeout.connect(self._recompute_trajectory_with_preview)
        
        # Schedule new computation after 50ms (fast enough for real-time feel)
        self.debounce_timer.start(50)
    
    def cleanup(self):
        """Clean up resources (call on window close)."""
        if self.debounce_timer and self.debounce_timer.isActive():
            self.debounce_timer.stop()
    
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
        # Show computing indicator (thread-safe via Qt signal)
        QTimer.singleShot(0, lambda: self.trajectory_panel.show_computing(True))
        
        events = self.model.get_events(self.perspective)
        
        if len(events) == 0:
            # No events - just hide the computing indicator
            QTimer.singleShot(0, lambda: self.trajectory_panel.show_computing(False))
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
        
        for i in range(len(events)):
            # Get primitives at current time
            v = data['v'][i]
            r = data['r'][i]
            f = data['f'][i]
            a = data['a'][i]
            S = data['S'][i]
            
            # Time delta - use time to next event, or a small default for the last event
            if i + 1 < len(events):
                dt = times[i + 1] - times[i]
            else:
                # For the last event, use a nominal time step
                dt = 1.0 if i == 0 else (times[i] - times[i-1])
            
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
        
        # Compute and display overlay trajectory for inactive perspective (Phase 3.3)
        # Only show overlay if dual-perspective data is loaded
        if not preview_mode and self.has_dual_perspective():
            inactive_perspective = "M2" if self.perspective == "M1" else "M1"
            inactive_events = self.model.get_events(inactive_perspective)
            if len(inactive_events) > 0:
                self._compute_and_display_overlay(inactive_perspective)
        elif not preview_mode:
            # Clear overlay if no dual perspective
            self.trajectory_panel.set_overlay_trajectory(None, None)
        
        self.state.mark_clean()
    
    def _compute_and_display_overlay(self, inactive_perspective: str):
        """
        Compute and display overlay trajectory for inactive perspective (Phase 3.3).
        
        Args:
            inactive_perspective: "M1" or "M2"
        """
        events = self.model.get_events(inactive_perspective)
        if len(events) == 0:
            self.trajectory_panel.set_overlay_trajectory(None, None)
            return
        
        # Get primitives
        primitives_data = self.model.get_primitives_array(inactive_perspective, include_preview=False)
        times = primitives_data['time']
        data = {
            'v': primitives_data['v'],
            'r': primitives_data['r'],
            'f': primitives_data['f'],
            'a': primitives_data['a'],
            'S': primitives_data['S']
        }
        
        # Compute gamma_self trajectory
        gamma_self = self.model.gamma_self_0
        gamma_trajectory = [gamma_self]
        
        for i in range(len(events) - 1):
            v = data['v'][i]
            r = data['r'][i]
            f = data['f'][i]
            a = data['a'][i]
            S = data['S'][i]
            dt = times[i + 1] - times[i]
            
            gamma_self = update_gamma_self(
                gamma_self_current=gamma_self,
                v=v, r=r, f=f, a=a, S=S,
                time_delta=dt,
                weights=self.weights
            )
            gamma_trajectory.append(gamma_self)
        
        # Extract components and display
        gamma_x = [g.real for g in gamma_trajectory]
        gamma_y = [g.imag for g in gamma_trajectory]
        self.trajectory_panel.set_overlay_trajectory(gamma_x, gamma_y)
    
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
        
        # Find inserted events (all primitives = 0) for marking
        inserted_events = []  # List of (index, time, gamma_x, gamma_y)
        for idx, event in enumerate(events):
            if is_inserted_event(event, exclude_first_last=True, event_idx=idx, total_events=len(events)):
                if idx < len(gamma_trajectory):
                    inserted_events.append({
                        'index': idx,
                        'time': event.time,
                        'x': gamma_x[idx],
                        'y': gamma_y[idx]
                    })
        
        # Build time-to-index mapping for converting time-based keys to indices
        events = self.model.get_events(self.perspective)
        time_to_idx = {evt.time: idx for idx, evt in enumerate(events)}
        
        # Build marked_data: {event_idx: set of modified primitives}
        marked_data = {}
        
        # Add committed modifications (convert time keys to indices)
        for event_time, prims in self.model.modified_primitives.items():
            if event_time in time_to_idx:
                event_idx = time_to_idx[event_time]
                if event_idx not in marked_data:
                    marked_data[event_idx] = set()
                marked_data[event_idx].update(prims)
        
        # Add preview modifications (already using indices)
        if preview_mode and self.model.preview_changes:
            for event_idx, prim_dict in self.model.preview_changes.items():
                if event_idx not in marked_data:
                    marked_data[event_idx] = set()
                marked_data[event_idx].update(prim_dict.keys())
        
        # Build pinned marker positions for gamma_self display
        # Format: [(event_idx, primitive, x, y, color), ...]
        pinned_markers = []
        
        for (event_time, prim), gamma_pos in self.model.marker_positions.items():
            # Convert time to current index
            if event_time not in time_to_idx:
                continue  # Event was deleted
            event_idx = time_to_idx[event_time]
            
            prim_colors = {'v': '#1f77b4', 'r': '#ff7f0e', 'f': '#2ca02c', 'a': '#d62728', 'S': '#9467bd'}
            marker = {
                'event_idx': event_idx,
                'primitive': prim,
                'x': gamma_pos.real,
                'y': gamma_pos.imag,
                'color': prim_colors.get(prim, 'orange'),
                'label': f"{event_time}/{prim}"
            }
            pinned_markers.append(marker)
        
        # Find gamma position to display in gauge
        # NOTE: preview_gamma is only for the trajectory plot preview marker, NOT the gauge
        preview_gamma = None
        if preview_mode:
            # During preview, show the trajectory preview marker at the modified event's position
            if self.model.preview_changes:
                preview_idx = max(self.model.preview_changes.keys())
                print(f"[PREVIEW_GAMMA] preview_idx from preview_changes={preview_idx}, len(gamma_trajectory)={len(gamma_trajectory)}")
                # Show position AFTER this event (next trajectory point)
                if preview_idx + 1 < len(gamma_trajectory):
                    preview_gamma = (gamma_x[preview_idx + 1], gamma_y[preview_idx + 1])
                    print(f"[PREVIEW_GAMMA] Set to trajectory[{preview_idx + 1}] = {preview_gamma}")
                else:
                    print(f"[PREVIEW_GAMMA] preview_idx+1 out of range")
            else:
                # Fallback: use the trajectory endpoint during preview
                if len(gamma_trajectory) > 0:
                    preview_gamma = (gamma_x[-1], gamma_y[-1])
                    print(f"[PREVIEW_GAMMA] Using trajectory endpoint = {preview_gamma}")
        else:
            print(f"[PREVIEW_GAMMA] Not in preview mode")
        
        # Store committed trajectory if not in preview
        if not preview_mode:
            self.committed_gamma_trajectory = gamma_trajectory
            print(f"[TRAJECTORY] Stored committed trajectory, final point: {gamma_trajectory[-1] if gamma_trajectory else 'empty'}")
        
        # Update trajectory panel (preserve view after initial load)
        # Always preserve view except on very first render
        preserve_view = self.initial_load_complete or preview_mode
        print(f"[TRAJECTORY] Calling update_trajectory with preserve_view={preserve_view}")
        
        # Call GUI update directly (we're already on main thread via QTimer)
        self._update_gui(
            gamma_x, gamma_y, marked_data, pinned_markers, preview_gamma, preserve_view, inserted_events
        )
    
    def _update_gui(self, gamma_x, gamma_y, marked_data, pinned_markers, preview_gamma, preserve_view, inserted_events=None):
        """Update GUI components (must be called on main thread)."""
        print(f"[_UPDATE_GUI] Called with preview_gamma={preview_gamma}, preserve_view={preserve_view}")
        
        # Update trajectory plot
        self.trajectory_panel.update_trajectory(gamma_x, gamma_y, marked_data, 
                                               pinned_markers=pinned_markers,
                                               preview_gamma=preview_gamma,
                                               preserve_view=preserve_view,
                                               inserted_events=inserted_events)
        self.trajectory_panel.show_computing(False)
        
        # Note: gamma_self gauge is NOT updated here - it's only updated by clicking on trajectory plot
        
        # Update primitive panel markers
        self.primitive_panel.update_markers(marked_data)
    
    def _update_all_views(self):
        """Update all views from model."""
        events = self.model.get_events(self.perspective)
        
        # Get inactive perspective events for overlay (Phase 3.3)
        # Only show overlay if dual-perspective data is loaded
        overlay_events = None
        if self.has_dual_perspective():
            inactive_perspective = "M2" if self.perspective == "M1" else "M1"
            overlay_events = self.model.get_events(inactive_perspective)
        
        self.primitive_panel.update_from_model(events)
        self.primitive_panel.set_overlay_data(overlay_events)
        
        # Refresh view to show current model state
        events = self.model.get_events(self.perspective)
        self.primitive_panel.update_from_model(events)
        self.primitive_panel.set_overlay_data(overlay_events)
    
    def _on_modified_primitives_changed(self, *args, **kwargs):
        """
        Observer callback for model.modified_primitives changes.
        Automatically updates the view cached modified state.
        
        This implements the observer pattern for automatic cache invalidation.
        """
        self._update_view_modified_state()
    
    def _update_view_modified_state(self):
        """
        Phase 3 refactoring: Update primitive panel cached modified state.
        Replaces the view direct access to controller.model.
        
        Note: This is now called automatically via observer pattern when
        model.modified_primitives changes.
        """
        events = self.model.get_events(self.perspective)
        modified_state = get_all_modified_markers(self.model, events, self.perspective)
        self.primitive_panel.set_modified_state(modified_state, self.perspective)
    
    def save_scenario(self, filepath: str):
        """Save scenario to CSV file."""
        self.model.save_csv(filepath, self.perspective)
        print(f"Saved to {filepath}")
