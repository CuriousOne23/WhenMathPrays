# Marker class for scenario editor

class Marker:
    def __init__(self, time, value, state='original', style=None, gamma_self_value=None):
        """
        Represents a marker for an event/primitive in the scenario editor.
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

    def set_value(self, new_value, new_state='modified'):
        self.value = new_value
        self.state = new_state

    def set_gamma_self(self, gamma_value):
        self.gamma_self_value = gamma_value

    def set_style(self, style):
        self.style = style

    def __repr__(self):
        return (f"Marker(time={self.time}, value={self.value}, state={self.state}, "
                f"gamma_self_value={self.gamma_self_value}, style={self.style})")
