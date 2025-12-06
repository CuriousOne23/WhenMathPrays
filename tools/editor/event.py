# Event class for scenario editor
from .marker import Marker

class Event:
    def __init__(self, time, primitives, notes='', marker='', locked=''):
        """
        Represents a single scenario event.
        Args:
            time (float): Event time.
            primitives (dict): Primitive values, e.g. {'v': 5.0, 'r': 2.0, ...}
            notes (str): Optional notes/description for this event
            marker (str): Optional marker type (e.g., 'circle', 'square')
            locked (str or bool): Whether event is locked from editing
        """
        self.time = time
        # Create a Marker for each primitive
        self.markers = {prim: Marker(time, value) for prim, value in primitives.items()}
        self.notes = notes
        self.marker = marker
        self.locked = locked

    def get_marker(self, primitive):
        return self.markers.get(primitive)

    def set_marker_value(self, primitive, value, state='modified'):
        if primitive in self.markers:
            self.markers[primitive].set_value(value, state)
    
    def to_dict(self):
        """Convert event to dictionary for CSV export with 3-digit precision."""
        result = {
            'day': int(self.time) if self.time == int(self.time) else round(self.time, 3),
            'v': round(self.markers['v'].value, 3),
            'r': round(self.markers['r'].value, 3),
            'f': round(self.markers['f'].value, 3),
            'a': round(self.markers['a'].value, 3),
            'S': round(self.markers['S'].value, 3),
            'notes': self.notes if self.notes else '',
            'marker': self.marker if self.marker else '',
            'locked': self.locked if self.locked else ''
        }
        return result

    def __repr__(self):
        return f"Event(time={self.time}, markers={self.markers}, notes={self.notes}, marker={self.marker}, locked={self.locked})"
