    # Global debug: show which primitives are being processed for each event
    # This should be inside the method where events are iterated, not at the top level

    # (Find the main event loop, e.g., in _apply_primitive_change or similar)
    # Example placement inside the event loop:
    # for event_index, event in enumerate(events):
    #     for primitive, value in event.primitives.items():
    #         if primitive == 'S' and (abs(event.time - 0.0) < 0.01 or abs(event.time - 49.0) < 0.01):
    #             print(f"[DEBUG][LOOP] event_idx={event_index}, time={event.time}, primitive={primitive}, value={value}")
"""
Controller for interactive scenario editor.

Coordinates between model and views, handles trajectory computation.
"""

import threading
import numpy as np
import pandas as pd
from typing import Optional, List
from PySide6.QtCore import QTimer
from PySide6.QtGui import QUndoStack
from PySide6.QtWidgets import QApplication
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
from tools.editor.observability import ObservabilityLog
from tools.editor.baseline_protocol import (
    BaselineDebugLog, BaselineCommunicator, BaselineType, BaselineEvent
)

# Import debug configuration
from tools.editor.debug_config import get_logger, DEBUG_SPINBOX

# Get logger for this module
_logger = get_logger('controller')


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
        
        # Initialize observer for operation visibility
        from tools.editor.simple_observer import SimpleObserver
        from tools.editor.config import DEBUG_OBSERVER_ENABLED
        self.observer = SimpleObserver(enabled=DEBUG_OBSERVER_ENABLED)
        
        # Separate undo stacks for each perspective
        self.undo_stack_m1 = undo_stack if undo_stack else None
        self.undo_stack_m2 = QUndoStack() if undo_stack else None
        
        # Active undo stack (points to current perspective's stack)
        self.undo_stack = self.undo_stack_m1
        
        # Centralized state management
        self.state = editor_state if editor_state is not None else EditorState()
        
        # Set up observer pattern for automatic cache invalidation
        # Register observers for BOTH perspectives
        self.model.get_modified_primitives("M1").add_observer(self._on_modified_primitives_changed)
        self.model.get_modified_primitives("M2").add_observer(self._on_modified_primitives_changed)
        
        self.debounce_timer: Optional[threading.Timer] = None
        
        # GRP computation parameters
        self.weights = DEFAULT_WEIGHTS.copy()
        self.delta_t = 1.0  # Time step for trajectory computation
        
        # Entropy parameters (editable via UI) - Option 3: Separate real/imag targets and rates
        self.entropy_real_target = -150.0  # Real axis attractor (Ego)
        self.entropy_imag_target = 0.0     # Imaginary axis attractor (Neutral affect)
        self.entropy_delS_real = 0.02      # Decay rate toward ego
        self.entropy_delS_imag = 0.02      # Decay rate toward neutral
        
        # Active primitive state tracking (for spinbox editor - ARCHITECTURE.md)
        # SEPARATE STATE PER PERSPECTIVE - so switching M1<->M2 preserves what you were editing
        self.active_primitive_state_m1 = {
            'primitive': None,   # 'v', 'r', 'f', 'a', 'S', or None
            'event_id': None,    # Which event is being edited
            'event_time': None   # Time of the event (for logging)
        }
        self.active_primitive_state_m2 = {
            'primitive': None,
            'event_id': None,
            'event_time': None
        }
        
        # Track last committed trajectory for comparison
        self.committed_gamma_trajectory = None
        
        # Store baseline values (from CSV) using ID-keyed dictionary for reset
        # Key: (event_id, primitive) -> Value: baseline_value
        # Separate baselines for M1 and M2 perspectives
        self.baseline_by_id_m1 = {}
        self.baseline_by_id_m2 = {}
        
        # Baseline communication protocol - rigorous sync between primitive and gamma_self spaces
        self.baseline_comm_m1 = BaselineCommunicator("M1")
        self.baseline_comm_m2 = BaselineCommunicator("M2")
        self._trajectory_reindex_needed = False  # Flag when gamma_self needs reindexing

        # Explicit mapping: (event_id, primitive) <-> gamma_self (trajectory_idx, x, y, label)
        # Updated on each trajectory recompute
        self.primitive_to_gamma_self = {}  # {(event_id, primitive): {'trajectory_idx': int, 'x': float, 'y': float, 'label': str}}
    
    @property
    def active_primitive_state(self):
        """Get active primitive state for current perspective."""
        return self.active_primitive_state_m1 if self.perspective == 'M1' else self.active_primitive_state_m2
    
    def _find_event_index_by_id(self, event_id: int) -> int:
        """
        Find current index of event by its permanent ID.
        
        ARCHITECTURE RULE: Never store indices in persistent state - they become stale
        when events are inserted/deleted. Always store IDs and look up current index.
        
        Args:
            event_id: Permanent event ID to find
            
        Returns:
            Current index of event in timeline, or -1 if not found (deleted)
        """
        events = self.model.get_events(self.perspective)
        for i, event in enumerate(events):
            if event.id == event_id:
                return i
        return -1  # Event not found (was deleted)
    
    def initialize_spinbox_widget(self, widget):
        """
        Initialize spinbox widget reference and connect signals.
        
        Called once during application startup. Replaces direct signal
        connection from interactive_editor.py.
        
        Args:
            widget: PrimitiveSpinboxEditor instance
        """
        self._spinbox_widget = widget
        widget.value_changed.connect(self.on_spinbox_value_changed)
    
    def update_spinbox_value(self, value: float):
        """
        Update spinbox value programmatically.
        
        Called when user clicks primitive marker in plot and the clicked
        primitive is already active in the spinbox. Updates the spinbox
        to show the new value without changing which primitive is selected.
        
        This is a proxy method that maintains single controller ownership
        of spinbox widget access.
        
        Args:
            value: New value to display in spinbox
        """
        if self._spinbox_widget.is_editing():
            self._spinbox_widget.update_value(value)
    
    def _restore_spinbox_state_for_perspective(self, perspective: str):
        """
        Restore spinbox widget state when switching to a perspective.
        
        Each perspective remembers what primitive was being edited, so switching
        M1->M2->M1 brings back the M1 editing state.
        
        Args:
            perspective: 'M1' or 'M2'
        """
        if not hasattr(self, '_spinbox_widget') or not self._spinbox_widget:
            return
        
        # Get state for this perspective
        state = self.active_primitive_state_m1 if perspective == 'M1' else self.active_primitive_state_m2
        
        if state['primitive'] is None:
            # Nothing was being edited in this perspective
            self._spinbox_widget.clear_active()
            return
        
        # Look up current index from stored ID
        event_id = state['event_id']
        event_index = self._find_event_index_by_id(event_id)
        
        if event_index < 0:
            # Event was deleted - clear state
            self._spinbox_widget.clear_active()
            state['primitive'] = None
            return
        
        # Get current event data
        events = self.model.get_events(perspective)
        event = events[event_index]
        primitive = state['primitive']
        current_value = event.markers[primitive].value
        event_time = event.time
        
        # Update stored time (may have changed due to insertions)
        state['event_time'] = event_time
        
        # Restore spinbox display
        self._spinbox_widget.set_active_primitive(primitive, current_value, event_time)
    
    def _refresh_spinbox_after_time_shift(self):
        """
        Refresh spinbox time label after insertions cause event times to shift.
        
        Example: User editing event at t=49. Ctrl+Shift+Click inserts event before it.
        Event is now at t=56, but spinbox label still says t=49. This updates the label.
        """
        if not hasattr(self, '_spinbox_widget') or not self._spinbox_widget:
            return
        
        if not self._spinbox_widget.is_editing():
            return
        
        state = self.active_primitive_state  # Property returns current perspective's state
        if state['primitive'] is None:
            return
        
        # Look up current event by ID
        event_id = state['event_id']
        event_index = self._find_event_index_by_id(event_id)
        
        if event_index < 0:
            # Event deleted
            self._spinbox_widget.clear_active()
            state['primitive'] = None
            return
        
        # Get current time (may have shifted)
        events = self.model.get_events(self.perspective)
        event = events[event_index]
        new_time = event.time
        old_time = state['event_time']
        
        # If time changed, update the label
        if abs(new_time - old_time) > 0.01:
            primitive = state['primitive']
            current_value = event.markers[primitive].value
            state['event_time'] = new_time
            self._spinbox_widget.set_active_primitive(primitive, current_value, new_time)
    
    def enable_baseline_protocol_logging(self):
        """
        Enable debug logging for baseline communication protocol.
        
        Use this to trace communication between primitive space (time-indexed)
        and gamma_self space (index-based) during insertions and edits.
        """
        BaselineDebugLog.enable()
    
    def disable_baseline_protocol_logging(self):
        """Disable debug logging for baseline communication protocol."""
        BaselineDebugLog.disable()
    
    def dump_baseline_protocol_log(self, filepath: str = None):
        """
        Dump baseline protocol log to file or console.
        
        Args:
            filepath: Path to save log. Options:
                     - None: Print to console
                     - "auto": Auto-generate timestamped JSON in logs/baseline/ (default)
                     - "path/to/file.json": Custom JSON file (machine-readable)
                     - "path/to/file.txt" or ".log": Custom text file (human-readable)
        """
        BaselineDebugLog.dump(filepath)
    
    def _get_weights_with_entropy(self):
        """
        Get weights dictionary with current entropy parameters.
        
        Returns:
            Dict with custom entropy parameters (Option 3: separate real/imag)
        """
        weights = self.weights.copy()
        weights['entropy_real_target'] = self.entropy_real_target
        weights['entropy_imag_target'] = self.entropy_imag_target
        weights['delS_real'] = self.entropy_delS_real
        weights['delS_imag'] = self.entropy_delS_imag
        return weights
    
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

        # Store baseline primitives using ID-keyed dictionary (immutable identity!)
        # Also initialize Marker objects with baseline state
        # Store baselines for M1
        events_m1 = self.model.get_events("M1")
        self.baseline_by_id_m1 = {}
        for event in events_m1:
            for prim in ['v', 'r', 'f', 'a', 'S']:
                key = (event.id, prim)
                self.baseline_by_id_m1[key] = float(event.markers[prim].value)
                # Initialize marker as not modified (at baseline)
                event.markers[prim].set_is_modified('M1', False)
        
        # Store baselines for M2 if loaded
        if m2_filepath:
            events_m2 = self.model.get_events("M2")
            self.baseline_by_id_m2 = {}
            for event in events_m2:
                for prim in ['v', 'r', 'f', 'a', 'S']:
                    key = (event.id, prim)
                    self.baseline_by_id_m2[key] = float(event.markers[prim].value)
                    # Initialize marker as not modified (at baseline)
                    event.markers[prim].set_is_modified('M2', False)

        # Initialize modified_primitives as empty - will track user modifications only
        events = self.model.get_events(self.perspective)
        self.model.get_modified_primitives(self.perspective).clear()
        # Don't mark anything as modified on load - user hasn't modified anything yet

        # Set scenario name on both panels
        display_name = self.model.get_display_name(self.perspective)
        self.primitive_panel.set_scenario_name(display_name)
        self.trajectory_panel.set_scenario_name(display_name)
        
        # Set time unit on primitive panel
        self.primitive_panel.set_time_unit(self.model.time_unit)
        
        # Initialize perspective in panels to match controller
        self.primitive_panel.current_perspective = self.perspective
        self.trajectory_panel.current_perspective = self.perspective
        print(f"[CONTROLLER] Initialized panel perspectives to {self.perspective}")

        # Update views
        self._update_all_views()

        # Compute initial trajectory (allow auto-zoom on first load)
        self.initial_load_complete = False
        self._recompute_trajectory_immediate()
        self.initial_load_complete = True  # Preserve view on all subsequent updates
    
    def _sync_baseline_to_view(self):
        """
        Synchronize baseline values from controller's ID-keyed dictionaries 
        to view's event-index-keyed dictionary. Must be called after any baseline changes.
        
        PROTOCOL: Converts from ID space (immutable) to view space (event-index).
        """
        events = self.model.get_events(self.perspective)
        baseline_dict = self.baseline_by_id_m1 if self.perspective == "M1" else self.baseline_by_id_m2
        baseline_comm = self.baseline_comm_m1 if self.perspective == "M1" else self.baseline_comm_m2
        
        # Build view's baseline_values from controller's baseline_by_id
        view_baseline = {}
        id_to_index_map = {}
        for event_idx, event in enumerate(events):
            id_to_index_map[event.id] = event_idx
            for prim in ['v', 'r', 'f', 'a', 'S']:
                key = (event.id, prim)
                if key in baseline_dict:
                    view_baseline[(event_idx, prim)] = baseline_dict[key]
        
        # Log protocol event
        baseline_comm.sync_primitive_baseline_to_view(id_to_index_map)
        
        # Update the view
        self.primitive_panel.set_baseline_values(view_baseline)
        print(f"[BASELINE] Synced {len(view_baseline)} baseline values to view for {self.perspective}")
    
    def switch_perspective(self, perspective: str):
        """
        Switch between M1 and M2 perspectives.
        
        Args:
            perspective: Either 'M1' or 'M2'
        """
        from tools.editor.state_viewer import StateViewer
        
        if perspective not in ['M1', 'M2']:
            raise ValueError(f"Invalid perspective: {perspective}. Must be 'M1' or 'M2'")
        
        if perspective == self.perspective:
            return  # Already on this perspective
        
        # Update perspective using state transition
        old_perspective = self.perspective
        target_state = PerspectiveState.M1 if perspective == 'M1' else PerspectiveState.M2
        
        ObservabilityLog.section(f"=== PERSPECTIVE SWITCH: {old_perspective} → {perspective} ===")
        ObservabilityLog.event("perspective_switch_start", 
                               old_perspective=old_perspective, 
                               new_perspective=perspective,
                               m1_labels=len(self.primitive_panel.modified_labels_m1),
                               m2_labels=len(self.primitive_panel.modified_labels_m2))
        
        self.state.switch_perspective(target_state)
        
        # Update display name on panels
        display_name = self.model.get_display_name(perspective)
        self.primitive_panel.set_scenario_name(display_name)
        self.trajectory_panel.set_scenario_name(display_name)
        
        # Set time unit on primitive panel
        self.primitive_panel.set_time_unit(self.model.time_unit)
        
        # Store old labels for debugging
        print(f"[CONTROLLER] Hiding {len(self.primitive_panel.modified_labels_m1 if old_perspective == 'M1' else self.primitive_panel.modified_labels_m2)} primitive labels for {old_perspective}")
        
        # Update current_perspective in panels BEFORE updating views
        # This ensures labels are added to the correct perspective storage
        print(f"[CONTROLLER] Updating panel perspectives from {old_perspective} to {perspective}")
        self.primitive_panel.current_perspective = perspective
        self.trajectory_panel.current_perspective = perspective
        
        # Restore spinbox state for new perspective
        self._restore_spinbox_state_for_perspective(perspective)
        
        # Remove ALL TextItems from all plots before switching
        import pyqtgraph as pg
        
        # Clear tracking dictionaries
        self.primitive_panel.modified_labels_m1.clear()
        self.primitive_panel.modified_labels_m2.clear()
        
        # Remove every TextItem from scene
        for prim, plot_item in self.primitive_panel.plot_items.items():
            to_remove = [item for item in plot_item.items[:] if isinstance(item, pg.TextItem)]
            for item in to_remove:
                plot_item.removeItem(item)
                item.deleteLater()
        
        QApplication.processEvents()
        
        # Query model to determine labels needed for NEW perspective
        labels_to_recreate = []
        
        # Scan marker_positions to find what needs labels (more reliable than modified_primitives)
        events = self.model.get_events(perspective)
        marker_positions = self.model.get_marker_positions(perspective)
        
        for (event_time, prim), gamma_pos in marker_positions.items():
            # Find event index by time
            event_idx = None
            for idx, event in enumerate(events):
                if abs(event.time - event_time) < 0.001:
                    event_idx = idx
                    break
            
            if event_idx is None:
                continue
            
            event = self.model.get_event(event_idx, perspective)
            value = event.markers[prim].value
            # If there's a marker position, the user modified it, so add label
            labels_to_recreate.append((event_time, prim, value))
        
        # Switch to the appropriate undo stack for this perspective
        if perspective == "M1":
            self.undo_stack = self.undo_stack_m1
            print(f"[UNDO] Switched to M1 undo stack (size: {self.undo_stack.count() if self.undo_stack else 0})")
        else:  # M2
            self.undo_stack = self.undo_stack_m2
            print(f"[UNDO] Switched to M2 undo stack (size: {self.undo_stack.count() if self.undo_stack else 0})")
        
        # Notify any UI components about the stack change
        # This allows the main window to update its undo/redo actions
        if hasattr(self, '_window_ref') and self._window_ref is not None:
            self._window_ref.switch_undo_stack(self.undo_stack)
        
        # Continue with view rebuild
        QApplication.processEvents()
        
        # Sync baseline values for new perspective to avoid ghost markers
        self._sync_baseline_to_view()
        
        # Update modified state cache for new perspective BEFORE updating views
        # This ensures markers show correct hollow/solid state
        self._update_view_modified_state()
        
        # Update all views with new perspective data
        self._update_all_views()
        
        # Labels will be synced from marker state by view's _sync_labels_from_markers()
        # (called automatically in update_from_model)
        
        # Recompute trajectory for new perspective
        # This will recreate all trajectory labels automatically via _display_trajectory
        self._recompute_trajectory_immediate()
        
        # Record state transition
        StateViewer.record(
            operation='switch_perspective',
            entity=(old_perspective, perspective),
            changes={
                'active_perspective': (old_perspective, perspective),
                'undo_stack_size': (self.undo_stack_m1.count() if old_perspective == 'M1' else self.undo_stack_m2.count(),
                                   self.undo_stack.count())
            }
        )
        
        ObservabilityLog.event("perspective_switch_complete", 
                               old_perspective=old_perspective, 
                               new_perspective=perspective,
                               m1_labels_final=len(self.primitive_panel.modified_labels_m1),
                               m2_labels_final=len(self.primitive_panel.modified_labels_m2))
    
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
        # Get old value for undo
        old_value = self.model.get_event(event_index, self.perspective).markers[primitive].value
        
        # Skip if no actual change
        if abs(value - old_value) < FLOAT_TOLERANCE:
            return
        
        # Create undo command and push to stack (unless we're in undo/redo)
        if self.undo_stack and not self.state.is_in_undo_operation():
            from tools.editor.commands import EditPrimitiveCommand
            command = EditPrimitiveCommand(self, event_index, primitive, old_value, value)
            self.undo_stack.push(command)
            return  # Command.redo() will handle the update
        
        # If no undo stack or in undo/redo, apply directly
        self._apply_primitive_change(event_index, primitive, value, self.perspective)
        # Commit the new value to the model
        self.model.update_primitive(event_index, primitive, value, self.perspective, preview=False)
        events = self.model.get_events(self.perspective)
        event_time = events[event_index].time
        modified_prims = self.model.get_modified_primitives(self.perspective)
        if event_time not in modified_prims:
            modified_prims[event_time] = set()
        modified_prims[event_time].add(primitive)
        
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
        gamma_self = self.model.get_gamma_self_0(self.perspective)
        gamma_trajectory = [gamma_self]
        for i in range(len(times) - 1):
            dt = times[i+1] - times[i]
            v, r, f, a, S = data['v'][i], data['r'][i], data['f'][i], data['a'][i], data['S'][i]
            gamma_self = update_gamma_self(gamma_self, v, r, f, a, S, self._get_weights_with_entropy(), dt)
            gamma_trajectory.append(gamma_self)
        
        # Marker pinning is now handled in _display_trajectory after recompute, using the updated trajectory.
        
        # === Phase 3: Incremental Update ===
        # Query modified status from Model (single source of truth)
        is_modified = self.model.is_primitive_modified(event_index, primitive, self.perspective)
        
        # Update only this marker in PrimitivePanel (O(1) operation)
        self.primitive_panel.update_marker(event_index, primitive, value, is_modified)
        
        # Update trajectory panel (full recompute, but marker update was instant)
        self._recompute_trajectory_immediate()
        # Note: trajectory panel updated via _display_trajectory

        # Log the explicit mapping for State Viewer/debugging immediately after update
        try:
            from tools.editor.state_viewer import StateViewer
            # Build mapping from current marker positions
            mapping = {}
            events = self.model.get_events(self.perspective)
            time_to_idx = {evt.time: idx for idx, evt in enumerate(events)}
            for (event_time, prim), gamma_pos in self.model.get_marker_positions(self.perspective).items():
                if event_time not in time_to_idx:
                    continue
                event_idx = time_to_idx[event_time]
                event_id = None
                for idx, evt in enumerate(events):
                    if abs(evt.time - event_time) < 1e-6:
                        event_id = evt.id
                        break
                if event_id is not None:
                    mapping[(event_id, prim)] = {
                        'trajectory_idx': event_idx,
                        'x': gamma_pos.real,
                        'y': gamma_pos.imag,
                        'label': f"{event_time}/{prim}"
                    }
            StateViewer.record(
                operation="update_primitive_to_gamma_self_mapping",
                entity=(self.perspective,),
                changes={"primitive_to_gamma_self": (None, mapping)},
                location="controller.py:on_primitive_changed (post-edit)"
            )
        except Exception as e:
            print(f"[STATE_VIEWER] Logging mapping after edit failed: {e}")
    
    def on_primitive_selected(self, event_index: int, primitive: str):
        """
        Handle primitive selection (user clicked marker or primitive label).
        
        Updates active_primitive_state and notifies spinbox widget.
        Implements "Active Primitive State Tracking" pattern from ARCHITECTURE.md.
        
        Args:
            event_index: Index of the event
            primitive: Name of primitive ('v', 'r', 'f', 'a', or 'S')
        """
        if DEBUG_SPINBOX:
            _logger.debug(f"on_primitive_selected called: event_index={event_index}, primitive={primitive}")
            _logger.debug(f"Has spinbox_widget? {hasattr(self, '_spinbox_widget')}")
            if hasattr(self, '_spinbox_widget'):
                _logger.debug(f"spinbox_widget is None? {self._spinbox_widget is None}")
        
        events = self.model.get_events(self.perspective)
        if event_index < 0 or event_index >= len(events):
            print(f"[PRIMITIVE_SELECT] Invalid event_index={event_index}")
            return
        
        event = events[event_index]
        event_time = event.time
        current_value = event.markers[primitive].value
        
        # Update active primitive state
        # ARCHITECTURE RULE: Store event.id (permanent), NOT index (changes on insert/delete)
        # Update dict in-place (can't assign since active_primitive_state is now a property)
        state = self.active_primitive_state
        state['primitive'] = primitive
        state['event_id'] = event.id  # Store permanent ID
        state['event_time'] = event_time
        
        if DEBUG_SPINBOX:
            _logger.debug(f"perspective={self.perspective}, event_id={event.id}, "
                         f"day={event_time}, primitive={primitive}, value={current_value}")
        
        # Notify spinbox widget (if it exists)
        if hasattr(self, '_spinbox_widget') and self._spinbox_widget is not None:
            if DEBUG_SPINBOX:
                _logger.debug(f"Calling spinbox_widget.set_active_primitive({primitive}, {current_value}, {event_time})")
            self._spinbox_widget.set_active_primitive(primitive, current_value, event_time)
            if DEBUG_SPINBOX:
                _logger.debug(f"Spinbox updated, label={self._spinbox_widget.get_active_label_text()}")
        else:
            if DEBUG_SPINBOX:
                _logger.debug("WARNING: spinbox_widget not available!")
    
    def on_spinbox_value_changed(self, new_value: float):
        """
        Handle value change from spinbox widget.
        
        Creates undo command and updates model with new primitive value.
        Implements unidirectional signal flow from ARCHITECTURE.md.
        
        Args:
            new_value: New value entered in spinbox
        """
        if self.active_primitive_state['primitive'] is None:
            print("[SPINBOX_EDIT] Warning: value changed but no active primitive")
            return
        
        # ARCHITECTURE RULE: Look up current index from stored ID
        # (Index may have changed due to insertions/deletions)
        event_id = self.active_primitive_state['event_id']
        event_index = self._find_event_index_by_id(event_id)
        
        if event_index < 0:
            print(f"[SPINBOX_EDIT] Event ID={event_id} not found (was deleted?)")
            # Clear spinbox since event no longer exists
            if hasattr(self, '_spinbox_widget') and self._spinbox_widget:
                self._spinbox_widget.clear_active()
            self.active_primitive_state['primitive'] = None
            return
        
        primitive = self.active_primitive_state['primitive']
        event_time = self.active_primitive_state['event_time']
        
        # Get old value for undo
        events = self.model.get_events(self.perspective)
        
        old_value = events[event_index].markers[primitive].value
        
        # Skip if no actual change
        if abs(new_value - old_value) < FLOAT_TOLERANCE:
            return
        
        print(f"[PRIMITIVE_EDIT] perspective={self.perspective}, event_id={event_id}, "
              f"day={event_time}, primitive={primitive}, old={old_value:.1f}, new={new_value:.1f}")
        
        # Use same path as on_primitive_changed (creates undo command, etc.)
        self.on_primitive_changed(event_index, primitive, new_value)
    
    def _apply_primitive_change(self, event_index: int, primitive: str, value: float, perspective: str):
        # Global debug: print every call to this function
        events = self.model.get_events(perspective)
        event = events[event_index]
        print(f"[DEBUG][GLOBAL] _apply_primitive_change called: event_idx={event_index}, time={event.time}, primitive={primitive}, value={value}, perspective={perspective}")
        # Debug: log when S is processed for each event at 0.0 or 49.0
        import os
        if primitive == 'S' and (abs(event.time - 0.0) < 0.01 or abs(event.time - 49.0) < 0.01):
            log_dir = os.path.join(os.path.dirname(__file__), '../../logs')
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, 'debug_S_baseline.log')
            print(f"[DEBUG][APPLY_PRIMITIVE_CHANGE] About to log S at event_idx={event_index}, time={event.time}, value={value}")
            with open(log_path, 'a') as f:
                f.write(f"[DEBUG][APPLY_PRIMITIVE_CHANGE] event_idx={event_index}, time={event.time}, primitive={primitive}, value={value}\n")
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
        events = self.model.get_events(perspective)
        event_time = events[event_index].time if event_index < len(events) else None
        self.observer.log('APPLY_PRIMITIVE_CHANGE', index=event_index, time=event_time, 
                         primitive=primitive, value=f'{value:.2f}', perspective=perspective)
        
        # Commit the new value to the model
        self.model.update_primitive(event_index, primitive, value, self.perspective, preview=False)
        
        # Check if this value is back to baseline
        events = self.model.get_events(perspective)
        event = events[event_index]
        
        # Use ID-keyed baseline (immutable identity!)
        # Use .get() with default 0.0 for inserted events that may not have baseline yet
        baseline_dict = self.baseline_by_id_m1 if perspective == "M1" else self.baseline_by_id_m2
        baseline_value = baseline_dict.get((event.id, primitive), 0.0)
        

        
        if abs(value - baseline_value) < FLOAT_TOLERANCE:
            # Back to baseline, remove from modified set
            modified_prims = self.model.get_modified_primitives(perspective)
            if event.id in modified_prims:
                modified_prims[event.id].discard(primitive)
                if not modified_prims[event.id]:
                    del modified_prims[event.id]
            # Update Marker object's modification state
            event.markers[primitive].set_is_modified(perspective, False)
            # Also remove marker position so it doesn't show on gamma_self graph
            marker_key = (event.id, primitive)
            marker_positions = self.model.get_marker_positions(perspective)
            if marker_key in marker_positions:
                del marker_positions[marker_key]
            # Hide label for this marker
            event.markers[primitive].set_label_visible(perspective, False)
        else:
            # Modified, add to set
            modified_prims = self.model.get_modified_primitives(perspective)
            if event.id not in modified_prims:
                modified_prims[event.id] = set()
            modified_prims[event.id].add(primitive)
            # Update Marker object's modification state
            event.markers[primitive].set_is_modified(perspective, True)
            # Show label for this marker (do not hide others)
            event.markers[primitive].set_label_visible(perspective, True)
        
        # Store marker position from committed trajectory (only if still modified)
        # First compute trajectory to get the position
        events = self.model.get_events(perspective)
        primitives_data = self.model.get_primitives_array(perspective, include_preview=False)
        times = primitives_data['time']
        data = {
            'v': primitives_data['v'],
            'r': primitives_data['r'],
            'f': primitives_data['f'],
            'a': primitives_data['a'],
            'S': primitives_data['S']
        }
        gamma_self = self.model.get_gamma_self_0(self.perspective)
        gamma_trajectory = [gamma_self]
        for i in range(len(times) - 1):
            dt = times[i+1] - times[i]
            v, r, f, a, S = data['v'][i], data['r'][i], data['f'][i], data['a'][i], data['S'][i]
            gamma_self = update_gamma_self(gamma_self, v, r, f, a, S, self._get_weights_with_entropy(), dt)
            gamma_trajectory.append(gamma_self)
        
        # Check if value is back at baseline (use perspective-aware baseline)
        baseline_dict = self.baseline_by_id_m1 if perspective == "M1" else self.baseline_by_id_m2
        baseline_value = baseline_dict.get((event.id, primitive), 0.0)
        at_baseline = abs(value - baseline_value) < 0.001  # Small tolerance for float comparison

        # Always print debug for S primitive
        if primitive == 'S':
            print(f"[DEBUG][S BASELINE] event_idx={event_index}, time={event.time}, value={value}, baseline={baseline_value}, at_baseline={at_baseline}")
        print(f"[BASELINE_CHECK] event_idx={event_index}, prim={primitive}, time={event.time}, value={value:.3f}, baseline={baseline_value:.3f}, at_baseline={at_baseline}")
        
        # Clear modification tracking if back at baseline
        if at_baseline:
            print(f"Primitive {event_index}/{primitive} (id={event.id}, time={event.time}) back to baseline, clearing modification")
            self.model.clear_primitive_modification(event.id, primitive, perspective)
            self.model.unpin_marker(event.id, primitive, perspective)
            # Hide the label since primitive is back to baseline
            event.markers[primitive].set_label_visible(perspective, False)
            print(f"[BASELINE_CHECK] Cleared modification for ({event.id}, {primitive})")
        
        # Store marker position only if still modified (not back to baseline)
        if self.model.is_primitive_modified(event_index, primitive, perspective):
            marker_idx = event_index + 1 if event_index + 1 < len(gamma_trajectory) else event_index
            gamma_pos = gamma_trajectory[marker_idx]
            self.model.pin_marker(event.id, primitive, gamma_pos, self.perspective)
            print(f"Marker (id={event.id}, {primitive}) -> gamma_self[{marker_idx}] = {gamma_pos}")
        
        # === Phase 3: Incremental Update ===
        # Query modified status from Model (single source of truth)
        is_modified = self.model.is_primitive_modified(event_index, primitive, self.perspective)
        
        # Update Marker state for label visibility (view will sync from this)
        # (No longer globally hiding all other labels; only update the marker being changed)
        event = self.model.get_event(event_index, self.perspective)
        if primitive == 'v':
            print(f"[DIAG] controller: Setting label_visible for Visibility (event_idx={event_index}, is_modified={is_modified})")
        
        # If this was undo/redo, force visual update of all markers after label changes
        if self.in_undo_redo:
            # Update modified state cache before updating view
            self._update_view_modified_state()
            events = self.model.get_events(self.perspective)
            self.primitive_panel.update_from_model(events)
            # Restore overlay data after update
            if self.has_dual_perspective():
                inactive_perspective = "M2" if self.perspective == "M1" else "M1"
                overlay_events = self.model.get_events(inactive_perspective)
                self.primitive_panel.set_overlay_data(overlay_events)
        else:
            # Normal drag operation - update single marker incrementally
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
            
            # Get original CSV baseline value using ID-based lookup
            event = self.model.get_event(event_index, self.perspective)
            event_id = event.id
            
            # Check if this ID exists in original baseline (not an inserted event)
            baseline_dict = self.baseline_by_id_m1 if self.perspective == "M1" else self.baseline_by_id_m2
            key = (event_id, primitive)
            if key in baseline_dict:
                baseline_value = baseline_dict[key]
                print(f"Resetting to baseline value: {baseline_value} (from original CSV, event ID {event_id})")
            else:
                # Inserted event - reset to 0
                baseline_value = 0.0
                print(f"Event ID {event_id} is inserted (not in original CSV), resetting to 0")
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
            command = ResetPrimitiveCommand(self, event_id, primitive, baseline_value, self.perspective)
            print(f"[UNDO] Pushing ResetPrimitiveCommand to stack (event={event_id}, prim={primitive}, {old_value:.2f}->{baseline_value:.2f})")
            self.undo_stack.push(command)
            print(f"[UNDO] Stack size now: {self.undo_stack.count()}, can undo: {self.undo_stack.canUndo()}")
            return  # Command.redo() will handle the update
        
        # If no undo stack or in undo/redo, apply directly
        self._apply_primitive_reset(event_index, primitive, baseline_value, self.perspective)
    
    def _apply_primitive_reset(self, event_index: int, primitive: str, baseline_value: float, perspective: str):
        """
        Apply primitive reset without undo tracking (used by undo commands).
        
        Args:
            event_index: Event index
            primitive: Primitive name
            baseline_value: Baseline value to reset to
            perspective: Perspective (M1 or M2)
        """
        print(f"_apply_primitive_reset called for event_idx={event_index}, primitive={primitive}, baseline_value={baseline_value}, perspective={perspective}")
        try:
            # Reset using Model's method (Phase 1 query interface)
            self.model.reset_event_primitive(event_index, primitive, baseline_value, perspective)
            
            event = self.model.get_event(event_index, perspective)
            modified_prims = self.model.get_modified_primitives(perspective)
            print(f"Reset complete. Event {event_index} (time={event.time}), modified_primitives: {modified_prims}")
            
            # Hide the label since primitive is reset to baseline
            event.markers[primitive].set_label_visible(perspective, False)
            
            # Remove marker position for this primitive (using event ID, not time!)
            # NOTE: marker_positions uses (event_id, primitive) as keys
            marker_key = (event.id, primitive)
            marker_positions = self.model.get_marker_positions(perspective)
            if marker_key in marker_positions:
                del marker_positions[marker_key]
                print(f"Removed marker position for {marker_key} (event_id={event.id}, time={event.time})")
            else:
                print(f"No marker position found for {marker_key} (event_id={event.id}, time={event.time})")
            
            # === Phase 3: Incremental Update ===
            # Update only this marker in PrimitivePanel (O(1) operation)
            is_modified = self.model.is_modified(event_index, primitive, perspective)
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
            
            # Update baseline - remove entries for deleted event
            baseline_dict = self.baseline_by_id_m1 if self.perspective == "M1" else self.baseline_by_id_m2
            for prim in ['v', 'r', 'f', 'a', 'S']:
                key = (event.id, prim)
                if key in baseline_dict:
                    del baseline_dict[key]
            
            # Update views
            self.primitive_panel.update_from_model(events)
            self._recompute_trajectory_immediate()
            
            print("=== END DELETE ===")
        except Exception as e:
            print(f"ERROR in _delete_event: {e}")
            import traceback
            traceback.print_exc()
    
    def _insert_event(self, event_index: int, event_data: dict, baseline_values: dict = None):
        """
        Insert an event (used by undo commands to restore deleted events).
        
        Args:
            event_index: Event index to insert at
            event_data: Dict with 'time', 'primitives', 'notes', 'locked', optionally 'event_id'
            baseline_values: Optional dict of {prim: baseline_value} to restore original baselines
        """
        try:
            print(f"\n=== INSERT EVENT at index {event_index} ===")
            
            # Import Event class from the correct module
            from tools.editor.event import Event
            
            # Create event using the actual Event class constructor
            # Preserve event_id if provided (for deleted event restoration)
            event = Event(
                time=event_data['time'],
                primitives=event_data['primitives'],
                notes=event_data.get('notes', ''),
                marker='',  # Markers aren't preserved for now
                locked=event_data.get('locked', False),
                event_id=event_data.get('event_id')  # Preserve ID if available
            )
            
            # Insert into model
            events = self.model.get_events(self.perspective)
            events.insert(event_index, event)
            
            print(f"Inserted event at time={event_data['time']}, total events: {len(events)}")
            
            # Update baseline - use provided baseline_values if available, otherwise use current primitives
            baseline_dict = self.baseline_by_id_m1 if self.perspective == "M1" else self.baseline_by_id_m2
            for prim in ['v', 'r', 'f', 'a', 'S']:
                key = (event.id, prim)
                if baseline_values and prim in baseline_values:
                    # Restore original baseline (for deleted event restoration)
                    baseline_dict[key] = baseline_values[prim]
                else:
                    # Use current primitive value as baseline (for new insertions)
                    baseline_dict[key] = event_data['primitives'][prim]
            
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
            
            # Create new event - use restored primitives if available, 
            # otherwise copy from previous event for visual continuity
            if restored_primitives:
                new_event = Event(
                    time=insert_time,
                    primitives=restored_primitives,
                    notes='',
                    marker='',
                    locked=False
                )
            else:
                # Initialize inserted events with zero primitives (neutral state)
                inserted_primitives = {'v': 0.0, 'r': 0.0, 'f': 0.0, 'a': 0.0, 'S': 0.0}
                
                # Create new event with next available ID
                new_event = Event(
                    time=insert_time,
                    primitives=inserted_primitives,
                    notes='',
                    marker='',
                    locked=False,
                    event_id=self.model.next_event_id,
                    source='inserted'  # Mark as user-inserted event
                )
                # Increment ID counter for next event
                self.model.next_event_id += 1
                print(f"[INSERT] New event ID={new_event.id}, source={new_event.source}, primitives: {inserted_primitives}")
            
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
            marker_positions = self.model.get_marker_positions(self.perspective)
            new_marker_positions = {}
            for (old_time, prim), gamma_pos in list(marker_positions.items()):
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
            
            marker_positions.clear()
            marker_positions.update(new_marker_positions)
            
            # Labels will be synced from marker state by view (no manual shifting needed)
            
            # THIRD: Insert new event at the calculated position
            events.insert(event_idx, new_event)
            print(f"STEP 2: Inserted new event at index {event_idx}, time={insert_time}")
            
            # Update baseline for newly inserted event (ID-based, no shifting needed!)
            print(f"STEP 3: Update baseline for inserted event")
            
            # Add baseline for newly inserted event (use actual values from the event)
            baseline_dict = self.baseline_by_id_m1 if self.perspective == "M1" else self.baseline_by_id_m2
            for prim in ['v', 'r', 'f', 'a', 'S']:
                key = (new_event.id, prim)
                baseline_dict[key] = new_event.markers[prim].value
            
            # PROTOCOL: Notify that Ctrl+Shift+Click insertion happened
            baseline_comm = self.baseline_comm_m1 if self.perspective == "M1" else self.baseline_comm_m2
            baseline_comm.notify_primitive_insert_shift(insert_time, time_shifts)
            
            # Mark that gamma_self trajectory needs reindexing after recomputation
            self._trajectory_reindex_needed = True
            
            # Debug: verify event times before update_from_model
            print("\n[DEBUG] Event times before update_from_model:")
            for idx, evt in enumerate(events):
                print(f"  idx={idx}: time={evt.time}")
            
            # Sync baseline to view BEFORE update_from_model so markers get correct appearance
            self._sync_baseline_to_view()
            
            # Update modified state cache with new indices after insertion
            self._update_view_modified_state()
            
            self.primitive_panel.update_from_model(events)
            self._recompute_trajectory_immediate()
            
            # Refresh spinbox label if active event's time changed
            self._refresh_spinbox_after_time_shift()
            
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
            # shifted_events contains (index_before_insert, old_time, new_time)
            # After removing the inserted event, events return to their original indices
            print(f"Events list now has {len(events)} events (indices 0-{len(events)-1})")
            print(f"Need to restore {len(shifted_events)} shifted events: {[(idx, old, new) for idx, old, new in shifted_events]}")
            
            for orig_idx, old_time, new_time in shifted_events:
                if orig_idx >= len(events):
                    print(f"  ERROR: Cannot restore index {orig_idx}, list only has {len(events)} events")
                    print(f"  Skipping this restoration")
                    continue
                    
                events[orig_idx].time = old_time
                print(f"  Restored event {orig_idx}: {new_time} -> {old_time}")
            
            # Update marker_position keys: shift back from new_time to old_time
            print("Restoring marker position keys:")
            marker_positions = self.model.get_marker_positions(self.perspective)
            new_marker_positions = {}
            for key, gamma_pos in list(marker_positions.items()):
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
            marker_positions.clear()
            marker_positions.update(new_marker_positions)
            
            # Update primitive panel labels for restored times
            print("Restoring primitive panel labels:")
            marker_positions = self.model.get_marker_positions(self.perspective)
            for orig_idx, old_time, new_time in shifted_events:
                for prim in ['v', 'r', 'f', 'a', 'S']:
                    # Remove label at shifted time
                    try:
                        self.primitive_panel.remove_marker_label(new_time, prim)
                        print(f"  Removed label at time {new_time}, prim {prim}")
                    except:
                        pass
                    
                    # Add label at restored time if there's a marker position
                    # (marker_positions is the source of truth - if it exists, user modified it)
                    if (old_time, prim) in marker_positions:
                        evt = events[orig_idx]
                        value = getattr(evt.markers[prim], 'value', None)
                        if value is not None:
                            self.primitive_panel._add_marker_label(old_time, prim, value)
                            print(f"  Added label at time {old_time}, prim {prim}, value={value:.2f}")
            
            # Update modified_primitives keys: shift back from new_time to old_time
            print("Restoring modified_primitives keys:")
            modified_prims = self.model.get_modified_primitives(self.perspective)
            new_modified_primitives = {}
            for time, prims in list(modified_prims.items()):
                restored = False
                for orig_idx, old_time, new_time in shifted_events:
                    if abs(time - new_time) < 0.001:  # This was shifted
                        new_modified_primitives[old_time] = prims
                        print(f"  Restored modified_primitives key: {new_time} -> {old_time}")
                        restored = True
                        break
                if not restored:
                    new_modified_primitives[time] = prims
            # Replace the entire dictionary
            modified_prims.clear()
            modified_prims.update(new_modified_primitives)
            
            # Update baseline - remove inserted event and shift back times
            print("Updating baseline:")
            
            # Remove baseline for inserted event (ID-based, no shifting needed!)
            baseline_dict = self.baseline_by_id_m1 if self.perspective == "M1" else self.baseline_by_id_m2
            for prim in ['v', 'r', 'f', 'a', 'S']:
                key = (removed_event.id, prim)
                if key in baseline_dict:
                    del baseline_dict[key]
            
            # Sync baseline to view BEFORE update_from_model so markers get correct appearance
            self._sync_baseline_to_view()
            
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
        preview_count = len(self.model.preview_changes)
        self.observer.log('COMMIT_CHANGES', preview_count=preview_count, perspective=self.perspective)
        
        print("\n=== COMMIT CHANGES ===")
        print("Note: Markers already stored on drag. Commit just finalizes to model.")
        
        # Commit the changes to the model
        self.model.commit_all_previews(self.perspective)
        self.primitive_panel.commit_all_previews()
        self._update_all_views()
        
        # Recompute trajectory as committed
        self._recompute_trajectory_immediate()
        
        marker_positions = self.model.get_marker_positions(self.perspective)
        print(f"Total markers: {len(marker_positions)}")
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
        self.observer.log('INSERT_EVENT', time=time, perspective=self.perspective)
        
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
        events = self.model.get_events(self.perspective)
        event_time = events[event_index].time if event_index < len(events) else None
        self.observer.log('DELETE_EVENT', index=event_index, time=event_time, perspective=self.perspective)
        
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
        """Update baseline primitives after inserting an event (fractional time insertion)."""
        events = self.model.get_events(self.perspective)
        new_event = events[insert_idx]
        
        baseline_dict = self.baseline_by_id_m1 if self.perspective == "M1" else self.baseline_by_id_m2
        baseline_comm = self.baseline_comm_m1 if self.perspective == "M1" else self.baseline_comm_m2
        
        # PROTOCOL: Notify that fractional insertion is happening
        baseline_comm.notify_primitive_insert_fractional(new_event.time)
        
        # Add baseline entries for new event ID (inserted events start at neutral 0.0)
        # For fractional insertion (no shift), baseline stays at CSV values (0.0 for new events)
        for prim in ['v', 'r', 'f', 'a', 'S']:
            key = (new_event.id, prim)
            baseline_dict[key] = 0.0
        print(f"[BASELINE] Added ID-keyed entries for event ID={new_event.id} (fractional insertion)")
        
        # NOTE: modified_primitives shifting is already handled by model.insert_event()
        # NOTE: marker_positions uses time-based keys, so they remain valid after insertion
    
    def _update_baseline_after_delete(self, deleted_idx: int):
        """Update baseline primitives after deleting an event.
        
        Args:
            deleted_idx: Index of the deleted event
        """
        # Get deleted event (still in list at this point)
        events = self.model.get_events(self.perspective)
        baseline_dict = self.baseline_by_id_m1 if self.perspective == "M1" else self.baseline_by_id_m2
        if deleted_idx < len(events):
            deleted_event = events[deleted_idx]
            
            # Remove baseline entries for deleted event
            for prim in ['v', 'r', 'f', 'a', 'S']:
                key = (deleted_event.id, prim)
                if key in baseline_dict:
                    del baseline_dict[key]
            print(f"[BASELINE] Removed ID-keyed entries for event ID={deleted_event.id}")
        
        # NOTE: modified_primitives and marker_positions use ID-based keys
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
        gamma_self = self.model.get_gamma_self_0(self.perspective)  # Start from configured initial position
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

            # Debug: Print event time, v value, and gamma_self before update
            print(f"[DEBUG GAMMA] i={i}, event_time={events[i].time}, v={v}, gamma_self_before={gamma_self}")

            # Update gamma_self using GRP core
            gamma_self = update_gamma_self(
                gamma_self_current=gamma_self,
                v=v, r=r, f=f, a=a, S=S,
                time_delta=dt,
                weights=self._get_weights_with_entropy()
            )

            # Debug: Print gamma_self after update
            print(f"[DEBUG GAMMA] i={i}, event_time={events[i].time}, gamma_self_after={gamma_self}")

            gamma_trajectory.append(gamma_self)
        
        # Store preview trajectory for marker positioning
        if preview_mode:
            self._last_preview_trajectory = gamma_trajectory
        
        # PROTOCOL: Notify that gamma_self trajectory was recomputed
        # After insertions, trajectory indices shift - need to reindex gamma baselines
        if not preview_mode and hasattr(self, '_trajectory_reindex_needed'):
            if self._trajectory_reindex_needed:
                baseline_comm = self.baseline_comm_m1 if self.perspective == "M1" else self.baseline_comm_m2
                
                # Build index mapping: old_index -> new_index
                # For now, we don't have the exact mapping, so just notify
                # TODO: Track old trajectory and compute precise mapping
                baseline_comm.notify_gamma_reindex({})
                
                self._trajectory_reindex_needed = False
        
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
        
        # Compute gamma_self trajectory - use inactive perspective's gamma_self_0
        gamma_self = self.model.get_gamma_self_0(inactive_perspective)
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
                weights=self._get_weights_with_entropy()
            )
            gamma_trajectory.append(gamma_self)
        
        # Extract components and display
        gamma_x = [g.real for g in gamma_trajectory]
        gamma_y = [g.imag for g in gamma_trajectory]
        self.trajectory_panel.set_overlay_trajectory(gamma_x, gamma_y)
    
    def _display_trajectory(self, gamma_trajectory, preview_mode=False):
        # Pin all markers to the updated gamma_self trajectory after recompute
        events = self.model.get_events(self.perspective)
        for idx, event in enumerate(events):
            for prim in ['v', 'r', 'f', 'a', 'S']:
                gamma_pos = None
                if idx + 1 < len(gamma_trajectory):
                    gamma_pos = gamma_trajectory[idx + 1]
                elif idx < len(gamma_trajectory):
                    gamma_pos = gamma_trajectory[idx]
                if gamma_pos is not None:
                    self.model.pin_marker(event.time, prim, gamma_pos, self.perspective)
                    # Only print for the edited primitive for clarity
                    if hasattr(self, 'active_primitive_state') and \
                        event.id == self.active_primitive_state.get('event_id') and \
                        prim == self.active_primitive_state.get('primitive'):
                        print(f"[FIXED] Marker ({event.time}, {prim}) -> gamma_self[{idx + 1}] = {gamma_pos}")
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
        # Use perspective-specific modified_primitives - no filtering needed
        for event_time, prims in self.model.get_modified_primitives(self.perspective).items():
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
        

        # Only show pinned_markers after user moves a primitive (i.e., if there are modifications)
        pinned_markers = []
        self.primitive_to_gamma_self.clear()
        has_modifications = bool(self.model.get_modified_primitives(self.perspective)) or (preview_mode and self.model.preview_changes)
        if has_modifications:
            marker_positions = self.model.get_marker_positions(self.perspective)
            events = self.model.get_events(self.perspective)
            prim_colors = {'v': '#1f77b4', 'r': '#ff7f0e', 'f': '#2ca02c', 'a': '#d62728', 'S': '#9467bd'}
            modified_prims = self.model.get_modified_primitives(self.perspective)
            for (event_time, prim), gamma_pos in marker_positions.items():
                event_idx = None
                event_id = None
                matched_event_time = None
                for idx, evt in enumerate(events):
                    if abs(evt.time - event_time) < 1e-6:
                        event_idx = idx
                        event_id = evt.id
                        matched_event_time = evt.time
                        break
                if event_idx is None or event_id is None:
                    continue  # Event was deleted
                # Only show marker if this event_id/prim is actually modified
                if event_id not in modified_prims or prim not in modified_prims[event_id]:
                    continue
                gamma_traj_idx = event_idx + 1
                if gamma_traj_idx >= len(gamma_trajectory):
                    gamma_traj_idx = len(gamma_trajectory) - 1
                gamma_val = gamma_trajectory[gamma_traj_idx]
                label_time = matched_event_time if matched_event_time is not None else event_time
                label_text = f"{label_time}/{prim}"
                print(f"[DEBUG][PINNED_MARKER_LABEL] Creating marker label: event_idx={event_idx}, event_time={event_time}, event_id={event_id}, matched_event_time={matched_event_time}, primitive={prim}, label_text='{label_text}'")
                marker = {
                    'event_idx': event_idx,
                    'primitive': prim,
                    'x': gamma_val.real,
                    'y': gamma_val.imag,
                    'color': prim_colors.get(prim, 'orange'),
                    'label': label_text
                }
                pinned_markers.append(marker)
                self.primitive_to_gamma_self[(event_id, prim)] = {
                    'trajectory_idx': gamma_traj_idx,
                    'x': gamma_val.real,
                    'y': gamma_val.imag,
                    'label': marker['label']
                }

        # Restore label visibility for all events of the current primitive in the primitive panel
        # This ensures all event markers for the selected primitive are visible in the primitive panel
        # (Do not restrict label visibility globally)
        
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
            gamma_x, gamma_y, marked_data, pinned_markers, preview_gamma, preserve_view, inserted_events,
            primitive_to_gamma_self=dict(self.primitive_to_gamma_self)
        )

        # Log the explicit mapping for State Viewer/debugging AFTER all updates
        try:
            from tools.editor.state_viewer import StateViewer
            StateViewer.record(
                operation="update_primitive_to_gamma_self_mapping",
                entity=(self.perspective,),
                changes={"primitive_to_gamma_self": (None, dict(self.primitive_to_gamma_self))},
                location="controller.py:update_trajectory (post-update)"
            )
        except Exception as e:
            print(f"[STATE_VIEWER] Logging mapping failed: {e}")
    
    def _update_gui(self, gamma_x, gamma_y, marked_data, pinned_markers, preview_gamma, preserve_view, inserted_events=None, primitive_to_gamma_self=None):
        """Update GUI components (must be called on main thread)."""
        print(f"[_UPDATE_GUI] Called with preview_gamma={preview_gamma}, preserve_view={preserve_view}")

        # Update trajectory plot with explicit mapping for robust label placement
        self.trajectory_panel.update_trajectory(
            gamma_x, gamma_y, marked_data,
            pinned_markers=pinned_markers,
            preview_gamma=preview_gamma,
            preserve_view=preserve_view,
            inserted_events=inserted_events,
            primitive_to_gamma_self=primitive_to_gamma_self
        )
        self.trajectory_panel.show_computing(False)

        # Note: gamma_self gauge is NOT updated here - it's only updated by clicking on trajectory plot

        # DO NOT update primitive panel markers here!
        # marked_data contains ALL modified primitives for trajectory visualization,
        # but primitive panel markers (red-bordered labels) should ONLY be shown
        # when explicitly clicking on the trajectory plot, not for every modification.
        # Trajectory click markers are managed separately via on_trajectory_point_clicked().
    
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
    
    def save_both_perspectives(self, m1_filepath: str, m2_filepath: str) -> bool:
        """
        Save both M1 and M2 perspectives to separate files.
        
        Args:
            m1_filepath: Path for M1 CSV file
            m2_filepath: Path for M2 CSV file
            
        Returns:
            True if both saves successful, False otherwise
        """
        try:
            self.model.save_csv(m1_filepath, "M1")
            print(f"Saved M1 to {m1_filepath}")
            self.model.save_csv(m2_filepath, "M2")
            print(f"Saved M2 to {m2_filepath}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save both perspectives: {e}")
            return False
