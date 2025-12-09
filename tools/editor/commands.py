"""
Undo/Redo commands for interactive editor.

Qt's undo framework using QUndoCommand pattern.
"""

from PySide6.QtGui import QUndoCommand


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
        self.event_idx = event_idx
        self.primitive = primitive
        self.old_value = old_value
        self.new_value = new_value
        
        # Set command text for UI display
        self.setText(f"Edit {primitive} at event {event_idx}: {old_value:.1f} → {new_value:.1f}")
    
    def redo(self):
        """Apply the edit (or re-apply after undo)."""
        self._apply_value(self.new_value)
    
    def undo(self):
        """Revert the edit."""
        self._apply_value(self.old_value)
    
    def _apply_value(self, value):
        """
        Apply a primitive value and update UI.
        
        Args:
            value: New primitive value
        """
        # Use controller's method to ensure consistent behavior
        # Set flag to prevent recursive undo command creation
        self.controller.in_undo_redo = True
        try:
            # Use the controller's apply method which handles marker positions and labels
            self.controller._apply_primitive_change(self.event_idx, self.primitive, value)
        finally:
            self.controller.in_undo_redo = False
    
    def id(self):
        """Return command ID for merging consecutive edits."""
        # Each event/primitive combination gets unique ID
        # This prevents merging edits to different markers
        # Use a simple int that fits in Qt's signed 32-bit int range
        return (self.event_idx * 5 + ['v', 'r', 'f', 'a', 'S'].index(self.primitive)) % 2147483647
    
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
            event_idx: Event index
            primitive: Primitive name
            old_value: Value before reset
            baseline_value: Baseline value from CSV
        """
        super().__init__()
        self.controller = controller
        self.event_idx = event_idx
        self.primitive = primitive
        self.old_value = old_value
        self.baseline_value = baseline_value
        
        self.setText(f"Reset {primitive} at event {event_idx} to baseline ({baseline_value:.1f})")
    
    def redo(self):
        """Apply the reset."""
        # Use controller's method to ensure consistent behavior
        self.controller.in_undo_redo = True
        try:
            self.controller._apply_primitive_reset(self.event_idx, self.primitive, self.baseline_value)
        finally:
            self.controller.in_undo_redo = False
    
    def undo(self):
        """Restore the value before reset."""
        # Use controller's apply method to restore the modified value
        self.controller.in_undo_redo = True
        try:
            self.controller._apply_primitive_change(self.event_idx, self.primitive, self.old_value)
        finally:
            self.controller.in_undo_redo = False


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
            'locked': event.locked
        }
        
        self.setText(f"Delete event at day {event.time}")
    
    def redo(self):
        """Delete the event."""
        self.controller.in_undo_redo = True
        try:
            self.controller._delete_event(self.event_idx)
        finally:
            self.controller.in_undo_redo = False
    
    def undo(self):
        """Restore the deleted event."""
        self.controller.in_undo_redo = True
        try:
            self.controller._insert_event(self.event_idx, self.event_data)
        finally:
            self.controller.in_undo_redo = False


class InsertEventBeforeCommand(QUndoCommand):
    """
    Command for inserting a new event before an existing event.
    
    The new event takes the existing event's time position, and the existing
    event (plus all subsequent events) shift forward by delta time.
    
    Supports undo/redo of event insertion via Ctrl+Shift+Click.
    """
    
    def __init__(self, controller, event_idx):
        """
        Initialize insert command.
        
        Args:
            controller: EditorController instance
            event_idx: Event index to insert before (this event will shift forward)
        """
        super().__init__()
        self.controller = controller
        self.event_idx = event_idx
        
        # Calculate insertion details
        events = controller.model.get_events(controller.perspective)
        
        if event_idx == 0:
            # Can't insert before first event
            raise ValueError("Cannot insert before first event")
        
        # Get times for delta calculation
        current_time = events[event_idx].time
        previous_time = events[event_idx - 1].time
        self.delta = current_time - previous_time
        self.insert_time = current_time  # New event takes this position
        
        # Store original times of events that will be shifted
        self.shifted_events = []  # [(idx, old_time, new_time), ...]
        for idx in range(event_idx, len(events)):
            old_time = events[idx].time
            new_time = old_time + self.delta
            self.shifted_events.append((idx, old_time, new_time))
        
        self.setText(f"Insert event at day {self.insert_time}")
    
    def redo(self):
        """Insert the new event and shift subsequent events."""
        self.controller.in_undo_redo = True
        try:
            self.controller._insert_event_before(self.event_idx, self.insert_time, self.delta)
        finally:
            self.controller.in_undo_redo = False
    
    def undo(self):
        """Remove the inserted event and restore original times."""
        self.controller.in_undo_redo = True
        try:
            self.controller._undo_insert_event_before(self.event_idx, self.shifted_events)
        finally:
            self.controller.in_undo_redo = False
