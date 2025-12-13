"""
Centralized state management for interactive scenario editor.

Consolidates scattered state variables into explicit state enums with
validation, transitions, and clear contracts.
"""

from enum import Enum, auto
from typing import Optional, Set, Callable
from dataclasses import dataclass, field


class PerspectiveState(Enum):
    """Active perspective being edited."""
    M1 = "M1"
    M2 = "M2"


class EditState(Enum):
    """Current edit operation state."""
    IDLE = auto()           # No active edit
    PREVIEW = auto()        # Dragging marker, changes uncommitted
    COMMITTED = auto()      # Changes committed to model, not yet saved to file


class TrajectoryComputeState(Enum):
    """Trajectory computation status."""
    CURRENT = auto()        # Display matches data
    SCHEDULED = auto()      # Debounce timer active
    COMPUTING = auto()      # Actively calculating


class UndoRedoState(Enum):
    """Undo/redo stack status."""
    CLEAN = auto()          # At save point
    DIRTY = auto()          # Unsaved changes
    IN_OPERATION = auto()   # Executing undo/redo (prevents recursion)


class FileLoadState(Enum):
    """File loading configuration."""
    DUAL_PERSPECTIVE = auto()   # Both M1 and M2 files loaded
    SINGLE_M1 = auto()          # Only M1 file, used for both perspectives
    SINGLE_M2 = auto()          # Only M2 file, used for both perspectives
    NONE = auto()               # No files loaded (error state)


@dataclass
class EditorState:
    """
    Centralized state container for the editor.
    
    Consolidates all state variables with validation and transition logic.
    Replaces scattered boolean flags across multiple classes.
    """
    
    # Core states
    perspective: PerspectiveState = PerspectiveState.M1
    edit_state: EditState = EditState.IDLE
    compute_state: TrajectoryComputeState = TrajectoryComputeState.CURRENT
    undo_state: UndoRedoState = UndoRedoState.CLEAN
    file_load_state: FileLoadState = FileLoadState.NONE
    
    # Flags
    initial_load_complete: bool = False
    dirty: bool = False  # Has unsaved changes
    
    # Observers for state changes
    _observers: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize observer dictionary."""
        if not isinstance(self._observers, dict):
            self._observers = {}
    
    def add_observer(self, state_name: str, callback: Callable):
        """
        Register callback for state changes.
        
        Args:
            state_name: Name of state to observe (e.g., 'perspective', 'edit_state')
            callback: Function called when state changes, receives (old_value, new_value)
        """
        if state_name not in self._observers:
            self._observers[state_name] = []
        self._observers[state_name].append(callback)
    
    def _notify_observers(self, state_name: str, old_value, new_value):
        """Notify all observers of state change."""
        if state_name in self._observers:
            for callback in self._observers[state_name]:
                callback(old_value, new_value)
    
    # Perspective state transitions
    def switch_perspective(self, new_perspective: PerspectiveState) -> bool:
        """
        Switch active perspective.
        
        Args:
            new_perspective: Target perspective
            
        Returns:
            True if switched, False if already at target
        """
        if new_perspective == self.perspective:
            return False
        
        old = self.perspective
        self.perspective = new_perspective
        self._notify_observers('perspective', old, new_perspective)
        return True
    
    def can_switch_perspective(self) -> bool:
        """Check if perspective switching is allowed."""
        # Cannot switch during active edit preview
        return self.edit_state != EditState.PREVIEW
    
    # Edit state transitions
    def start_preview(self) -> bool:
        """
        Transition to preview state (start dragging).
        
        Returns:
            True if transitioned, False if blocked
        """
        if self.edit_state != EditState.IDLE:
            return False  # Already in edit
        
        old = self.edit_state
        self.edit_state = EditState.PREVIEW
        self._notify_observers('edit_state', old, EditState.PREVIEW)
        return True
    
    def commit_preview(self) -> bool:
        """
        Commit preview to model (release drag).
        
        Returns:
            True if committed, False if no preview active
        """
        if self.edit_state != EditState.PREVIEW:
            return False
        
        old = self.edit_state
        self.edit_state = EditState.COMMITTED
        self.mark_dirty()
        self._notify_observers('edit_state', old, EditState.COMMITTED)
        return True
    
    def cancel_preview(self) -> bool:
        """
        Cancel preview and return to idle.
        
        Returns:
            True if cancelled, False if no preview active
        """
        if self.edit_state != EditState.PREVIEW:
            return False
        
        old = self.edit_state
        self.edit_state = EditState.IDLE
        self._notify_observers('edit_state', old, EditState.IDLE)
        return True
    
    def finish_commit(self) -> bool:
        """
        Finish commit and return to idle (after commit operations complete).
        
        Returns:
            True if finished, False if not in committed state
        """
        if self.edit_state != EditState.COMMITTED:
            return False
        
        old = self.edit_state
        self.edit_state = EditState.IDLE
        self._notify_observers('edit_state', old, EditState.IDLE)
        return True
    
    # Undo/redo state transitions
    def mark_dirty(self):
        """Mark editor as having unsaved changes."""
        if not self.dirty:
            self.dirty = True
            old = self.undo_state
            self.undo_state = UndoRedoState.DIRTY
            self._notify_observers('undo_state', old, UndoRedoState.DIRTY)
    
    def mark_clean(self):
        """Mark editor as clean (saved)."""
        if self.dirty:
            self.dirty = False
            old = self.undo_state
            self.undo_state = UndoRedoState.CLEAN
            self._notify_observers('undo_state', old, UndoRedoState.CLEAN)
    
    def enter_undo_operation(self) -> bool:
        """
        Enter undo/redo operation to prevent recursion.
        
        Returns:
            True if entered, False if already in operation
        """
        if self.undo_state == UndoRedoState.IN_OPERATION:
            return False
        
        old = self.undo_state
        self.undo_state = UndoRedoState.IN_OPERATION
        self._notify_observers('undo_state', old, UndoRedoState.IN_OPERATION)
        return True
    
    def exit_undo_operation(self):
        """Exit undo/redo operation."""
        if self.undo_state == UndoRedoState.IN_OPERATION:
            # Return to previous state (dirty if changes exist)
            new_state = UndoRedoState.DIRTY if self.dirty else UndoRedoState.CLEAN
            old = self.undo_state
            self.undo_state = new_state
            self._notify_observers('undo_state', old, new_state)
    
    def is_in_undo_operation(self) -> bool:
        """Check if currently executing undo/redo."""
        return self.undo_state == UndoRedoState.IN_OPERATION
    
    # Trajectory compute state transitions
    def schedule_computation(self):
        """Mark computation as scheduled (debounce timer active)."""
        old = self.compute_state
        self.compute_state = TrajectoryComputeState.SCHEDULED
        self._notify_observers('compute_state', old, TrajectoryComputeState.SCHEDULED)
    
    def start_computation(self):
        """Mark computation as in progress."""
        old = self.compute_state
        self.compute_state = TrajectoryComputeState.COMPUTING
        self._notify_observers('compute_state', old, TrajectoryComputeState.COMPUTING)
    
    def finish_computation(self):
        """Mark computation as complete and current."""
        old = self.compute_state
        self.compute_state = TrajectoryComputeState.CURRENT
        self._notify_observers('compute_state', old, TrajectoryComputeState.CURRENT)
    
    # File state management
    def set_file_load_state(self, state: FileLoadState):
        """Set the file loading configuration."""
        old = self.file_load_state
        self.file_load_state = state
        self._notify_observers('file_load_state', old, state)
    
    def has_dual_perspective(self) -> bool:
        """Check if both M1 and M2 are loaded independently."""
        return self.file_load_state == FileLoadState.DUAL_PERSPECTIVE
    
    # Validation methods
    def can_edit_primitive(self, event_locked: bool, is_first: bool, is_last: bool) -> bool:
        """
        Check if a primitive can be edited.
        
        Args:
            event_locked: Whether the event is locked
            is_first: Whether this is the first event
            is_last: Whether this is the last event
            
        Returns:
            True if edit is allowed
        """
        # Cannot edit during active preview of another marker
        if self.edit_state == EditState.PREVIEW:
            return False
        
        # Cannot edit locked events
        if event_locked:
            return False
        
        return True
    
    def can_delete_event(self, event_locked: bool, is_first: bool, is_last: bool, num_events: int) -> bool:
        """
        Check if an event can be deleted.
        
        Args:
            event_locked: Whether the event is locked
            is_first: Whether this is the first event
            is_last: Whether this is the last event
            num_events: Total number of events
            
        Returns:
            True if deletion is allowed
        """
        # Must have at least 3 events (to leave 2 after deletion)
        if num_events < 3:
            return False
        
        # Cannot delete first or last
        if is_first or is_last:
            return False
        
        # Cannot delete locked events
        if event_locked:
            return False
        
        return True
    
    def can_insert_event(self, is_first: bool) -> bool:
        """
        Check if an event can be inserted before a target.
        
        Args:
            is_first: Whether inserting before first event
            
        Returns:
            True if insertion is allowed
        """
        # Cannot insert before first event (would require negative time)
        return not is_first
    
    # Status queries
    def get_state_summary(self) -> dict:
        """Get summary of current state for debugging."""
        return {
            'perspective': self.perspective.value,
            'edit_state': self.edit_state.name,
            'compute_state': self.compute_state.name,
            'undo_state': self.undo_state.name,
            'file_load_state': self.file_load_state.name,
            'dirty': self.dirty,
            'initial_load_complete': self.initial_load_complete,
        }


# Singleton state instance (can be passed to components)
_editor_state: Optional[EditorState] = None


def get_editor_state() -> EditorState:
    """Get the singleton editor state instance."""
    global _editor_state
    if _editor_state is None:
        _editor_state = EditorState()
    return _editor_state


def reset_editor_state():
    """Reset state to initial values (for testing or restart)."""
    global _editor_state
    _editor_state = EditorState()
    return _editor_state
