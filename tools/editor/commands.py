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
