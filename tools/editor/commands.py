"""
Undo/Redo commands for interactive editor.

Qt's undo framework using QUndoCommand pattern.
"""

from PySide6.QtGui import QUndoCommand
from tools.editor.state_viewer import StateViewer


class InsertEventCommand(QUndoCommand):
    """
    Command for inserting a new event at a specific time without shifting other events.
    
    Used for manual time entry in insertion options widget.
    """
    
    def __init__(self, controller, insert_time):
        """
        Initialize insert command.
        
        Args:
            controller: EditorController instance
            insert_time: Time for the new event
        """
        super().__init__()
        self.controller = controller
        self.insert_time = insert_time
        self.setText(f"Insert event at day {insert_time}")
    
    def redo(self):
        """Insert the new event."""
        StateViewer.record(
            operation='redo_insert_event',
            entity=(self.insert_time, self.controller.perspective),
            changes={
                'action': ('remove', 'insert')
            }
        )
        self.controller.state.enter_undo_operation()
        try:
            self.controller.insert_event_at_time(self.insert_time)
        finally:
            self.controller.state.exit_undo_operation()
    
    def undo(self):
        """Remove the inserted event."""
        StateViewer.record(
            operation='undo_insert_event',
            entity=(self.insert_time, self.controller.perspective),
            changes={
                'action': ('insert', 'remove')
            }
        )
        print(f"\n[INSERT_UNDO] InsertEventCommand.undo() called for time={self.insert_time}")
        self.controller.state.enter_undo_operation()
        try:
            # Find the event at this time and delete it
            events = self.controller.model.get_events(self.controller.perspective)
            print(f"[INSERT_UNDO] Searching {len(events)} events for time={self.insert_time}")
            for idx, evt in enumerate(events):
                if abs(evt.time - self.insert_time) < 0.001:
                    print(f"[INSERT_UNDO] Found event at idx={idx}, calling delete_event_at_index()")
                    self.controller.delete_event_at_index(idx)
                    print(f"[INSERT_UNDO] Delete complete")
                    break
            else:
                print(f"[INSERT_UNDO] ERROR: No event found at time={self.insert_time}")
        finally:
            self.controller.state.exit_undo_operation()


class EditPrimitiveCommand(QUndoCommand):
    """
    Command for editing a primitive value.
    
    Supports undo/redo of marker drag operations.
    """
    
    def __init__(self, controller, event_idx, primitive, old_value, new_value):
        """
        Initialize edit command.
        
        Args:
            controller: EditorController instance
            event_idx: Event index
            primitive: Primitive name ('v', 'r', 'f', 'a', 'S')
            old_value: Value before edit
            new_value: Value after edit
        """
        super().__init__()
        self.controller = controller
        # Store time, not index, so command survives insertions/deletions
        events = controller.model.get_events(controller.perspective)
        self.event_time = events[event_idx].time
        self.primitive = primitive
        self.old_value = old_value
        self.new_value = new_value
        
        # Set command text for UI display
        self.setText(f"Edit {primitive} at time {self.event_time}: {old_value:.1f} → {new_value:.1f}")
    
    def redo(self):
        """Apply the edit (or re-apply after undo)."""
        StateViewer.record(
            operation='redo_edit_primitive',
            entity=(self.event_time, self.primitive, self.controller.perspective),
            changes={
                'value': (self.old_value, self.new_value)
            }
        )
        self._apply_value(self.new_value)
    
    def undo(self):
        """Revert the edit."""
        StateViewer.record(
            operation='undo_edit_primitive',
            entity=(self.event_time, self.primitive, self.controller.perspective),
            changes={
                'value': (self.new_value, self.old_value)
            }
        )
        self._apply_value(self.old_value)
    
    def _apply_value(self, value):
        """
        Apply a primitive value and update UI.
        
        Args:
            value: New primitive value
        """
        # Use controller's method to ensure consistent behavior
        # Set flag to prevent recursive undo command creation using state
        self.controller.state.enter_undo_operation()
        try:
            # Find current index for this time (may have changed due to insertions)
            events = self.controller.model.get_events(self.controller.perspective)
            event_idx = None
            for idx, evt in enumerate(events):
                if abs(evt.time - self.event_time) < 0.001:
                    event_idx = idx
                    break
            
            if event_idx is None:
                print(f"[EDIT_CMD] Event at time {self.event_time} not found!")
                return
            
            # Use the controller's apply method which handles marker positions and labels
            self.controller._apply_primitive_change(event_idx, self.primitive, value)
        finally:
            self.controller.state.exit_undo_operation()
    
    def id(self):
        """Return command ID for merging consecutive edits."""
        # Each time/primitive combination gets unique ID
        # This prevents merging edits to different markers
        # Use hash of time and primitive, modulo to fit in signed 32-bit int
        return (hash((self.event_time, self.primitive)) % 2147483647)
    
    def mergeWith(self, other):
        """
        Merge with another command if possible.
        
        Currently disabled to allow each discrete edit to be undone separately.
        If enabled, multiple drags of the same marker would be treated as 
        a single undo/redo operation.
        
        Args:
            other: Another QUndoCommand
            
        Returns:
            True if merged, False otherwise
        """
        # Merging disabled - each edit is a separate undo step
        # This allows Ctrl+Z to step through each discrete value change
        return False
        
        # Original merging logic (commented out):
        # if not isinstance(other, EditPrimitiveCommand):
        #     return False
        # 
        # # Only merge if same event/primitive
        # if (other.event_idx != self.event_idx or 
        #     other.primitive != self.primitive):
        #     return False
        # 
        # # Merge by updating our new_value to the other's new_value
        # # Keep our old_value (the original starting point)
        # self.new_value = other.new_value
        # self.setText(f"Edit {self.primitive} at event {self.event_idx}: {self.old_value:.1f} → {self.new_value:.1f}")
        # 
        # return True


class ResetPrimitiveCommand(QUndoCommand):
    """
    Command for resetting a primitive to baseline via double-click.
    """
    
    def __init__(self, controller, event_idx, primitive, old_value, baseline_value):
        """
        Initialize reset command.
        
        Args:
            controller: EditorController instance
            event_idx: Event index (only used to get time)
            primitive: Primitive name
            old_value: Value before reset
            baseline_value: Baseline value from CSV
        """
        super().__init__()
        self.controller = controller
        # Store time, not index, so command survives insertions/deletions
        events = controller.model.get_events(controller.perspective)
        self.event_time = events[event_idx].time
        self.primitive = primitive
        self.old_value = old_value
        self.baseline_value = baseline_value
        
        self.setText(f"Reset {primitive} at time {self.event_time} to baseline ({baseline_value:.1f})")
    
    def redo(self):
        """Apply the reset."""
        StateViewer.record(
            operation='redo_reset_primitive',
            entity=(self.event_time, self.primitive, self.controller.perspective),
            changes={
                'value': (self.old_value, self.baseline_value)
            }
        )
        # Use controller's method to ensure consistent behavior
        self.controller.state.enter_undo_operation()
        try:
            # Find current index for this time
            events = self.controller.model.get_events(self.controller.perspective)
            event_idx = None
            for idx, evt in enumerate(events):
                if abs(evt.time - self.event_time) < 0.001:
                    event_idx = idx
                    break
            
            if event_idx is None:
                print(f"[RESET_CMD] Event at time {self.event_time} not found!")
                return
            
            self.controller._apply_primitive_reset(event_idx, self.primitive, self.baseline_value)
        finally:
            self.controller.state.exit_undo_operation()
    
    def undo(self):
        """Restore the value before reset."""
        StateViewer.record(
            operation='undo_reset_primitive',
            entity=(self.event_time, self.primitive, self.controller.perspective),
            changes={
                'value': (self.baseline_value, self.old_value)
            }
        )
        # Use controller's apply method to restore the modified value
        self.controller.state.enter_undo_operation()
        try:
            # Find current index for this time
            events = self.controller.model.get_events(self.controller.perspective)
            event_idx = None
            for idx, evt in enumerate(events):
                if abs(evt.time - self.event_time) < 0.001:
                    event_idx = idx
                    break
            
            if event_idx is None:
                print(f"[RESET_CMD] Event at time {self.event_time} not found!")
                return
            
            self.controller._apply_primitive_change(event_idx, self.primitive, self.old_value)
        finally:
            self.controller.state.exit_undo_operation()


class DeleteEventCommand(QUndoCommand):
    """
    Command for deleting an event.
    
    Supports undo/redo of event deletion via Ctrl+Click.
    """
    
    def __init__(self, controller, event_idx):
        """
        Initialize delete command.
        
        Args:
            controller: EditorController instance
            event_idx: Event index to delete
        """
        super().__init__()
        self.controller = controller
        self.event_idx = event_idx
        
        # Store event data for undo
        events = controller.model.get_events(controller.perspective)
        event = events[event_idx]
        self.event_data = {
            'time': event.time,
            'primitives': {prim: event.markers[prim].value for prim in ['v', 'r', 'f', 'a', 'S']},
            'notes': event.notes,
            'locked': event.locked,
            'event_id': event.id  # Preserve event ID for baseline lookup
        }
        
        # Store baseline values separately (from controller's baseline dict)
        baseline_dict = controller.baseline_by_id_m1 if controller.perspective == "M1" else controller.baseline_by_id_m2
        self.baseline_values = {}
        for prim in ['v', 'r', 'f', 'a', 'S']:
            key = (event.id, prim)
            if key in baseline_dict:
                self.baseline_values[prim] = baseline_dict[key]
        
        self.setText(f"Delete event at day {event.time}")
    
    def redo(self):
        """Delete the event."""
        StateViewer.record(
            operation='redo_delete_event',
            entity=(self.event_data['time'], self.controller.perspective, self.event_idx),
            changes={
                'action': ('restore', 'delete')
            }
        )
        self.controller.state.enter_undo_operation()
        try:
            self.controller._delete_event(self.event_idx)
        finally:
            self.controller.state.exit_undo_operation()
    
    def undo(self):
        """Restore the deleted event."""
        StateViewer.record(
            operation='undo_delete_event',
            entity=(self.event_data['time'], self.controller.perspective, self.event_idx),
            changes={
                'action': ('delete', 'restore')
            }
        )
        self.controller.state.enter_undo_operation()
        try:
            # Pass baseline_values to restore original baselines
            self.controller._insert_event(self.event_idx, self.event_data, self.baseline_values)
        finally:
            self.controller.state.exit_undo_operation()


class InsertEventBeforeCommand(QUndoCommand):
    """
    Command for inserting a new event before an existing event.
    
    The new event takes the existing event's time position, and the existing
    event (plus all subsequent events) shift forward by delta time.
    
    Supports undo/redo of event insertion via Ctrl+Shift+Click.
    """
    
    def __init__(self, controller, event_idx, insert_time=None):
        """
        Initialize insert command.
        
        Args:
            controller: EditorController instance
            event_idx: Event index to insert at (new event goes here, rest shift forward)
            insert_time: Optional specific time for insertion (if None, use event's time)
        """
        super().__init__()
        self.controller = controller
        self.event_idx = event_idx
        
        # Calculate insertion details
        events = controller.model.get_events(controller.perspective)
        
        if event_idx == 0:
            # Can't insert before first event
            raise ValueError("Cannot insert before first event")
        
        # Get the target event's time BEFORE we insert (this is where new event will be placed)
        target_time = events[event_idx].time
        
        # Get insertion time (use the target event's current time)
        if insert_time is not None:
            self.insert_time = insert_time
            print(f"[COMMAND] Using provided insert_time={insert_time}")
        else:
            # Use the target event's time (new event takes this position)
            self.insert_time = target_time
            print(f"[COMMAND] Using target event time={target_time}")
        
        # Calculate delta: gap from previous event to insertion point
        # This is the amount by which subsequent events will be shifted forward
        # Example: clicking at 8.77 between day 7 and day 30 creates delta = 8.77 - 7.0 = 1.77
        previous_time = events[event_idx - 1].time
        self.delta = self.insert_time - previous_time
        print(f"[COMMAND] event_idx={event_idx}, prev_time={previous_time}, insert_time={self.insert_time}, delta={self.delta}")
        
        # Store original times of events that will be shifted
        self.shifted_events = []  # [(idx, old_time, new_time), ...]
        for idx in range(event_idx, len(events)):
            old_time = events[idx].time
            new_time = old_time + self.delta
            self.shifted_events.append((idx, old_time, new_time))
        
        self.setText(f"Insert event at day {self.insert_time}")
    
    def redo(self):
        """Insert the new event and shift subsequent events."""
        StateViewer.record(
            operation='redo_insert_event_before',
            entity=(self.event_idx, self.controller.perspective, self.insert_time),
            changes={
                'action': ('remove', 'insert'),
                'shifted_events': (0, len(self.shifted_events))
            }
        )
        self.controller.state.enter_undo_operation()
        try:
            self.controller._insert_event_before(self.event_idx, self.insert_time, self.delta)
        finally:
            self.controller.state.exit_undo_operation()
    
    def undo(self):
        """Remove the inserted event and restore original times."""
        StateViewer.record(
            operation='undo_insert_event_before',
            entity=(self.event_idx, self.controller.perspective, self.insert_time),
            changes={
                'action': ('insert', 'remove'),
                'shifted_events': (len(self.shifted_events), 0)
            }
        )
        print(f"\n[INSERT_UNDO] InsertEventBeforeCommand.undo() called for event_idx={self.event_idx}")
        self.controller.state.enter_undo_operation()
        try:
            self.controller._undo_insert_event_before(self.event_idx, self.shifted_events)
        finally:
            self.controller.state.exit_undo_operation()
