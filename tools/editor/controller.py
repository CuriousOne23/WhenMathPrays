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
        
        # Phase 3 refactoring: Removed controller reference from view (violates MVC)
        # self.primitive_panel.controller = self
        
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
        # Store ORIGINAL CSV baseline values - never updated, used for reset comparison
        self.original_baseline_primitives = {}
        
        # Track initial load to allow auto-zoom only on first render
        self.initial_load_complete = False
        
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
        # Store original CSV values - these NEVER change, used for reset comparison
        self.original_baseline_primitives = {}
        for key, val in self.baseline_primitives.items():
            if isinstance(val, np.ndarray):
                self.original_baseline_primitives[key] = val.copy()
            else:
                self.original_baseline_primitives[key] = val

        # Initialize modified_primitives as empty - will track user modifications only
        events = self.model.get_events(self.perspective)
        print(f"[DEBUG] EditorController.load_scenario: get_events returned {len(events)} events")
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
                if abs(value) > 0.001:
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
        events = self.model.get_events(self.perspective)
        event_time = events[event_index].time
        if event_time not in self.model.modified_primitives:
            self.model.modified_primitives[event_time] = set()
        self.model.modified_primitives[event_time].add(primitive)
        print(f"[DEBUG] Updated modified_primitives: {self.model.modified_primitives}")
        
        # Phase 3 refactoring: Update view's cached modified state
        self._update_view_modified_state()
        
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
        print(f"Marker ({event_time}, {primitive}) → gamma_self[{marker_idx}] = {gamma_pos}")
        
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
        
        Args:
            event_index: Event index
            primitive: Primitive name
            value: New value
        """
        # Commit the new value to the model
        self.model.update_primitive(event_index, primitive, value, self.perspective, preview=False)
        
        # Check if this value is back to baseline
        baseline_value = self.baseline_primitives[primitive][event_index]
        events = self.model.get_events(self.perspective)
        event_time = events[event_index].time
        if abs(value - baseline_value) < 0.001:
            # Back to baseline, remove from modified set
            if event_time in self.model.modified_primitives:
                self.model.modified_primitives[event_time].discard(primitive)
                if not self.model.modified_primitives[event_time]:
                    del self.model.modified_primitives[event_time]
            
            # Also remove marker position so it doesn't show on gamma_self graph
            marker_key = (event_time, primitive)
            if marker_key in self.model.marker_positions:
                del self.model.marker_positions[marker_key]
                print(f"[DEBUG] Removed marker position for {marker_key} (back to baseline)")
        else:
            # Modified, add to set
            if event_time not in self.model.modified_primitives:
                self.model.modified_primitives[event_time] = set()
            self.model.modified_primitives[event_time].add(primitive)
        
        print(f"[DEBUG] Updated modified_primitives: {self.model.modified_primitives}")
        
        # Phase 3 refactoring: Update view's cached modified state
        self._update_view_modified_state()
        
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
            print(f"Marker ({event_time}, {primitive}) → gamma_self[{marker_idx}] = {gamma_pos}")
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
            self.primitive_panel._add_marker_label(event_index, primitive, event.time, value)
        else:
            self.primitive_panel.remove_marker_label(event_index, primitive)
        
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
        
        try:
            # Get current value
            old_value = self.model.get_event(event_index, self.perspective).markers[primitive].value
            
            # Get original CSV baseline value by finding the event's original position
            # After insertions, we need to map current time back to original CSV row
            event = self.model.get_event(event_index, self.perspective)
            event_time = event.time
            
            # Find the index in original baseline that matches this time
            original_times = np.array(self.original_baseline_primitives['time'])
            original_idx = np.where(np.abs(original_times - event_time) < 0.001)[0]
            
            if len(original_idx) == 0:
                print(f"Event at time {event_time} is not in original CSV (inserted event), cannot reset")
                return
            
            baseline_value = self.original_baseline_primitives[primitive][original_idx[0]]
            print(f"Resetting to baseline value: {baseline_value} (from original CSV)")
        except Exception as e:
            print(f"ERROR getting values: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Skip if already at baseline
        if abs(old_value - baseline_value) < 0.001:
            print(f"Already at baseline, skipping")
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
            
            # Remove the marker label
            self.primitive_panel.remove_marker_label(event_index, primitive)
            
            # Reset double-click state in the marker
            marker_obj = self.primitive_panel.draggable_points.get((event_index, primitive))
            if marker_obj:
                marker_obj.reset_double_click_state()
            
            # Recompute trajectory and update trajectory view
            self._recompute_trajectory_with_preview()
            
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
            if event_time in self.model.modified_primitives:
                del self.model.modified_primitives[event_time]
            
            # Remove marker positions for this event
            for prim in PRIMITIVE_NAMES:
                marker_key = (event_time, prim)
                if marker_key in self.model.marker_positions:
                    del self.model.marker_positions[marker_key]
            
            print(f"Deleted event at time={event_time}, remaining events: {len(events)}")
            
            # Update baseline primitives arrays (remove deleted index)
            for key in self.baseline_primitives:
                if isinstance(self.baseline_primitives[key], np.ndarray):
                    self.baseline_primitives[key] = np.delete(self.baseline_primitives[key], event_index)
                    self.original_baseline_primitives[key] = np.delete(self.original_baseline_primitives[key], event_index)
            
            # Update views
            self._update_view_modified_state()
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
            
            # Update baseline primitives arrays (insert at index)
            for prim in PRIMITIVE_NAMES:
                value = event_data['primitives'][prim]
                if prim in self.baseline_primitives:
                    self.baseline_primitives[prim] = np.insert(self.baseline_primitives[prim], event_index, value)
                    self.original_baseline_primitives[prim] = np.insert(self.original_baseline_primitives[prim], event_index, value)
            
            # Insert time
            if 'time' in self.baseline_primitives:
                self.baseline_primitives['time'] = np.insert(self.baseline_primitives['time'], event_index, event_data['time'])
                self.original_baseline_primitives['time'] = np.insert(self.original_baseline_primitives['time'], event_index, event_data['time'])
            
            # Update views
            self._update_view_modified_state()
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
            for idx in range(event_idx, len(events)):
                old_time = events[idx].time
                events[idx].time = old_time + delta
                print(f"  Shifted event {idx}: {old_time} → {events[idx].time}")
            
            # THIRD: Insert new event at the calculated position
            events.insert(event_idx, new_event)
            print(f"STEP 2: Inserted new event at index {event_idx}, time={insert_time}")
            
            # Update baseline arrays to match the new event structure
            print(f"STEP 3: Update baseline arrays")
            
            # After shifting events in-place and inserting new event, we need to:
            # 1. Insert new arrays for the new event at event_idx
            # 2. Update time array to match shifted event times
            
            # Insert new event's primitives into baseline
            for prim in PRIMITIVE_NAMES:
                if prim in self.baseline_primitives:
                    prim_value = new_event.markers[prim].value if restored_primitives else 0.0
                    self.baseline_primitives[prim] = np.insert(self.baseline_primitives[prim], event_idx, prim_value)
                    self.original_baseline_primitives[prim] = np.insert(self.original_baseline_primitives[prim], event_idx, prim_value)
            
            # Rebuild time array from events (since times were shifted)
            # After insert, baseline arrays have correct length, just need to sync times
            if 'time' in self.baseline_primitives:
                # Insert makes room at event_idx, but we need to update all times from event_idx onwards
                self.baseline_primitives['time'] = np.insert(self.baseline_primitives['time'], event_idx, insert_time)
                self.original_baseline_primitives['time'] = np.insert(self.original_baseline_primitives['time'], event_idx, insert_time)
                
                # Now update shifted times (from event_idx+1 onwards)
                for idx in range(event_idx + 1, len(events)):
                    self.baseline_primitives['time'][idx] = events[idx].time
                    self.original_baseline_primitives['time'][idx] = events[idx].time
                    print(f"  Updated baseline time[{idx}] = {events[idx].time}")
            
            # Update views
            self._update_view_modified_state()
            
            # Debug: verify event times before updating view
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
                print(f"  Restored event {orig_idx}: {new_time} → {old_time}")
            
            # Update baseline arrays - remove inserted event
            for prim in PRIMITIVE_NAMES:
                if prim in self.baseline_primitives:
                    self.baseline_primitives[prim] = np.delete(self.baseline_primitives[prim], event_idx)
                    self.original_baseline_primitives[prim] = np.delete(self.original_baseline_primitives[prim], event_idx)
            
            if 'time' in self.baseline_primitives:
                self.baseline_primitives['time'] = np.delete(self.baseline_primitives['time'], event_idx)
                self.original_baseline_primitives['time'] = np.delete(self.original_baseline_primitives['time'], event_idx)
            
            # Update restored times in baseline arrays
            for orig_idx, old_time, new_time in shifted_events:
                if 'time' in self.baseline_primitives:
                    self.baseline_primitives['time'][orig_idx] = old_time
                    self.original_baseline_primitives['time'][orig_idx] = old_time
            
            # Update views
            self._update_view_modified_state()
            self.primitive_panel.update_from_model(events)
            self._recompute_trajectory_immediate()
            
            print(f"Total events after undo: {len(events)}")
            print("=== END UNDO INSERT BEFORE ===")
        except Exception as e:
            print(f"ERROR in _undo_insert_event_before: {e}")
            import traceback
            traceback.print_exc()
    
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
        # Re-fetch baseline from model
        self.baseline_primitives = self.model.get_primitives_array(self.perspective, include_preview=False)
        
        # NOTE: modified_primitives shifting is already handled by model.insert_event()
        # Don't duplicate the shift logic here!
        
        # Clear marker positions - trajectory changes after insertion, so old gamma_self
        # coordinates no longer correspond to the same events. Markers will be regenerated
        # when user commits changes.
        self.model.marker_positions = {}
    
    def _update_baseline_after_delete(self, deleted_idx: int):
        """Update baseline primitives and modified_primitives after deleting an event."""
        # Re-fetch baseline from model
        self.baseline_primitives = self.model.get_primitives_array(self.perspective, include_preview=False)
        
        # NOTE: modified_primitives shifting is already handled by model.delete_event()
        # Don't duplicate the shift logic here!
        
        # Clear marker positions - trajectory changes after deletion, so old gamma_self
        # coordinates no longer correspond to the same events. Markers will be regenerated
        # when user commits changes.
        self.model.marker_positions = {}
    
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
        print(f"\n=== DISPLAY TRAJECTORY (preview={preview_mode}) ===")
        print(f"marker_positions dict: {self.model.marker_positions}")
        
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
            print(f"  Building marker: {marker}")
        
        print(f"Total pinned_markers: {len(pinned_markers)}")
        print("=== END DISPLAY ===")
        
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
        self.primitive_panel.update_from_model(events)
        
        # Phase 3 refactoring: Push modified state to view (no direct model access)
        self._update_view_modified_state()
    
    def _update_view_modified_state(self):
        """
        Phase 3 refactoring: Update primitive panel's cached modified state.
        Replaces view's direct access to controller.model.
        """
        modified_state = {}
        events = self.model.get_events(self.perspective)
        
        for event_idx in range(len(events)):
            for prim in ['v', 'r', 'f', 'a', 'S']:
                is_mod = self.model.is_modified(event_idx, prim, self.perspective)
                if is_mod:
                    modified_state[(event_idx, prim)] = True
        
        self.primitive_panel.set_modified_state(modified_state, self.perspective)
    
    def save_scenario(self, filepath: str):
        """
        Save scenario to CSV file.
        
        Args:
            filepath: Output path
        """
        self.model.save_csv(filepath, self.perspective)
        print(f"Saved to {filepath}")
