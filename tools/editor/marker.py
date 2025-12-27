# Marker class for scenario editor

class Marker:
    def __init__(self, time, value, state='original', style=None, gamma_self_value=None):
        """
        Represents a marker for an event/primitive in the scenario editor.
        
        Perspective-aware attributes store per-perspective state, enabling
        single-point debugging via accessor methods.
        
        Args:
            time (float): Event time.
            value (float): Primitive value at this event.
            state (str): 'original', 'modified', or 'preview'.
            style (dict or str): Visual style info (color, shape, etc.).
            gamma_self_value (float, optional): Computed gamma_self value at this event.
        """
        self.time = time
        self.value = value
        self.state = state
        self.style = style or {}
        self.gamma_self_value = gamma_self_value
        
        # Perspective-aware state (dict keyed by perspective: 'M1', 'M2', etc.)
        self.gamma_self_position = {}  # {perspective: complex} - where gamma_self was when modified
        self.is_modified = {}           # {perspective: bool} - modified from baseline
        self.label_visible = {}         # {perspective: bool} - label currently shown

    def set_value(self, new_value, new_state='modified'):
        self.value = new_value
        self.state = new_state

    def set_gamma_self(self, gamma_value):
        self.gamma_self_value = gamma_value

    def set_style(self, style):
        self.style = style
    
    # Perspective-aware accessors for debugging and extensibility
    
    def get_gamma_position(self, perspective: str):
        """Get gamma_self position for this perspective. Returns None if not set."""
        return self.gamma_self_position.get(perspective)
    
    def set_gamma_position(self, perspective: str, position: complex):
        """Set gamma_self position for this perspective. Single entry point for debugging."""
        self.gamma_self_position[perspective] = position
    
    def clear_gamma_position(self, perspective: str):
        """Clear gamma_self position for this perspective."""
        self.gamma_self_position.pop(perspective, None)
    
    def get_is_modified(self, perspective: str) -> bool:
        """Check if modified from baseline for this perspective."""
        return self.is_modified.get(perspective, False)
    
    def set_is_modified(self, perspective: str, modified: bool):
        """Set modification status for this perspective. Single entry point for debugging."""
        self.is_modified[perspective] = modified
    
    def clear_is_modified(self, perspective: str):
        """Clear modification status for this perspective."""
        self.is_modified.pop(perspective, None)
    
    def get_label_visible(self, perspective: str) -> bool:
        """Check if label is visible for this perspective."""
        return self.label_visible.get(perspective, False)
    
    def set_label_visible(self, perspective: str, visible: bool):
        """Set label visibility for this perspective. Single entry point for debugging."""
        self.label_visible[perspective] = visible

    def __repr__(self):
        return (f"Marker(time={self.time}, value={self.value}, state={self.state}, "
                f"gamma_self_value={self.gamma_self_value}, style={self.style})")
