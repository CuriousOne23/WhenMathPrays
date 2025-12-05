# Event class for scenario editor
from .marker import Marker

class Event:
    def __init__(self, time, primitives):
        """
        Represents a single scenario event.
        Args:
            time (float): Event time.
            primitives (dict): Primitive values, e.g. {'v': 5.0, 'r': 2.0, ...}
        """
        self.time = time
        # Create a Marker for each primitive
        self.markers = {prim: Marker(time, value) for prim, value in primitives.items()}

    def get_marker(self, primitive):
        return self.markers.get(primitive)

    def set_marker_value(self, primitive, value, state='modified'):
        if primitive in self.markers:
            self.markers[primitive].set_value(value, state)

    def __repr__(self):
        return f"Event(time={self.time}, markers={self.markers})"
