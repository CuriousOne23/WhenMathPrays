"""
Data model for interactive scenario editor.

Handles event data, CSV I/O, and modification tracking.
"""

import csv
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from pathlib import Path


@dataclass
class EventPoint:
    """Single event in scenario timeline."""
    
    time: float
    v: float  # Ego primitive
    r: float  # Resonance primitive
    f: float  # Freedom primitive
    a: float  # Vulnerability primitive
    S: float  # Shared Breath primitive
    notes: str = ""
    marker: str = ""  # Empty or "circle", "star", etc.
    locked: bool = False
    
    def __post_init__(self):
        """Validate primitive values."""
        for prim in ['v', 'r', 'f', 'a', 'S']:
            val = getattr(self, prim)
            if not -10 <= val <= 10:
                raise ValueError(f"Primitive {prim}={val} outside valid range [-10, 10]")
    
    def to_dict(self) -> Dict:
        """Export to CSV row format."""
        return {
            'step': self.time,
            'v': self.v,
            'r': self.r,
            'f': self.f,
            'a': self.a,
            'S': self.S,
            'notes': self.notes,
            'marker': self.marker,
            'locked': '*' if self.locked else ''
        }
    
    @classmethod
    def from_dict(cls, row: Dict) -> 'EventPoint':
        """Create EventPoint from CSV row. Returns None if required columns are missing."""
        # Skip rows missing required columns
        required = ['v', 'r', 'f', 'a', 'S']
        if any(k not in row or row[k] is None or row[k] == '' for k in required):
            return None
        # Handle both 'step' and 'day' column names
        time = float(row.get('step', row.get('day', 0)))
        return cls(
            time=time,
            v=float(row['v']),
            r=float(row['r']),
            f=float(row['f']),
            a=float(row['a']),
            S=float(row['S']),
            notes=row.get('notes', ''),
            marker=row.get('marker', ''),
            locked=(row.get('locked', '') == '*')
        )


class EditorModel:
    """Model for interactive scenario editing."""
    
    def __init__(self):
        self.name: str = ""
        self.time_unit: str = "days"
        self.gamma_self_0: complex = 0 + 0j  # Initial gamma_self position
        self.events_m1: List[EventPoint] = []
        self.events_m2: List[EventPoint] = []  # For future dual perspective
        self.filepath: Optional[Path] = None
        self.dirty: bool = False  # Unsaved changes?
        self.modified_indices: set = set()  # Track which events were modified
        self.modified_primitives: Dict[int, set] = {}  # {event_idx: {'v', 'r', ...}}
        
        # Preview state (uncommitted changes)
        self.preview_changes: Dict[int, Dict[str, float]] = {}  # {event_idx: {primitive: value}}
        # Pinned marker positions: where gamma_self was when each primitive was first modified
        self.marker_positions: Dict[tuple, complex] = {}  # {(event_idx, primitive): gamma_self_position}
    
    def load_csv(self, filepath: str, perspective: str = "M1") -> None:
        """
        Load scenario from CSV file.
        
        Args:
            filepath: Path to CSV file
            perspective: "M1" or "M2" (currently only M1 supported)
        """
        self.filepath = Path(filepath)
        events = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            # Robustly parse metadata and header lines, skipping empty lines and tolerating any order
            header_line = None
            self.name = ''
            self.time_unit = 'days'
            self.gamma_self_0 = 0+0j
            while True:
                line = f.readline()
                if not line:
                    break  # EOF
                line = line.strip()
                if not line:
                    continue  # skip blank lines
                if line.lower().startswith('name,'):
                    self.name = line.split(',', 1)[1].strip()
                elif line.lower().startswith('time_unit,'):
                    self.time_unit = line.split(',', 1)[1].strip()
                elif line.lower().startswith('gamma_self_0,'):
                    import re
                    # Split after 'gamma_self_0,' and get first non-empty token
                    tokens = [t for t in line.split(',')[1:] if t.strip()]
                    if tokens:
                        gamma_str = tokens[0].strip()
                        gamma_str = re.sub(r'^["\']+|["\']+$', '', gamma_str).strip()
                        self.gamma_self_0 = complex(gamma_str)
                    else:
                        self.gamma_self_0 = 0+0j
                elif line.lower().startswith('step,') or line.lower().startswith('day,'):
                    header_line = line
                    break
                else:
                    # Assume this is the CSV header if not recognized
                    header_line = line
                    break

            # Read CSV data with explicit header
            if header_line:
                fieldnames = [h.strip() for h in header_line.split(',')]
                # Ensure marker and locked columns exist for old files
                if 'marker' not in fieldnames:
                    fieldnames.append('marker')
                if 'locked' not in fieldnames:
                    fieldnames.append('locked')
                reader = csv.DictReader(f, fieldnames=fieldnames)
                for row in reader:
                    # Fill missing optional columns with empty string
                    if 'marker' not in row or row['marker'] is None:
                        row['marker'] = ''
                    if 'locked' not in row or row['locked'] is None:
                        row['locked'] = ''
                    event = EventPoint.from_dict(row)
                    if event is not None:
                        events.append(event)
        
        if perspective == "M1":
            self.events_m1 = events
        else:
            self.events_m2 = events
        
        self.dirty = False
        self.modified_indices.clear()
        
        print(f"Loaded {len(events)} events from {filepath}")
        if self.name:
            print(f"  Scenario: {self.name}")
        print(f"  Time unit: {self.time_unit}")
    
    def save_csv(self, filepath: str, perspective: str = "M1") -> None:
        """
        Save scenario to CSV file.
        Always exports with full format (marker and locked columns).
        Ensures marker is set for edited events and locked column is set for locked events.
        Args:
            filepath: Output path
            perspective: "M1" or "M2"
        """
        events = self.events_m1 if perspective == "M1" else self.events_m2

        # Ensure marker and locked columns are set for edited/locked events
        for idx, event in enumerate(events):
            # Set marker and locked if event was edited (fractional value or in modified_primitives)
            if idx in self.modified_primitives or any(
                isinstance(getattr(event, prim), float) and not float(getattr(event, prim)).is_integer()
                for prim in ['v', 'r', 'f', 'a', 'S']
            ):
                if not event.marker:
                    event.marker = 'circle'
                event.locked = True

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            # Write metadata if present
            if self.name:
                f.write(f"name,{self.name}\n")
            f.write(f"time_unit,{self.time_unit}\n")
            # Write gamma_self_0 (format: -5+3j or 0+0j)
            gamma_str = f"{self.gamma_self_0.real:+.0f}{self.gamma_self_0.imag:+.0f}j"
            gamma_str = gamma_str.replace('+-', '-')  # Fix double sign
            f.write(f"gamma_self_0,{gamma_str}\n")

            # Write CSV data
            fieldnames = ['step', 'v', 'r', 'f', 'a', 'S', 'notes', 'marker', 'locked']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for event in events:
                writer.writerow(event.to_dict())

        self.dirty = False
        print(f"Saved {len(events)} events to {filepath}")
    
    def update_primitive(self, event_index: int, primitive: str, value: float, 
                        perspective: str = "M1", preview: bool = True) -> None:
        """
        Update a primitive value at specific event.
        
        Args:
            event_index: Index in events list
            primitive: 'v', 'r', 'f', 'a', or 'S'
            value: New value (will be clamped to [-10, 10])
            perspective: "M1" or "M2"
            preview: If True, store as preview (uncommitted)
        """
        events = self.events_m1 if perspective == "M1" else self.events_m2
        
        if not 0 <= event_index < len(events):
            raise IndexError(f"Event index {event_index} out of range")
        
        # Clamp value
        value = max(-10, min(10, value))
        
        if preview:
            # Store in preview (don't modify event yet)
            if event_index not in self.preview_changes:
                self.preview_changes[event_index] = {}
            self.preview_changes[event_index][primitive] = value
        else:
            # Commit change
            setattr(events[event_index], primitive, value)
            
            # Auto-mark as modified
            if not events[event_index].marker:
                events[event_index].marker = "circle"
            
            # Track which primitive was modified
            if event_index not in self.modified_primitives:
                self.modified_primitives[event_index] = set()
            self.modified_primitives[event_index].add(primitive)
            
            self.dirty = True
            self.modified_indices.add(event_index)
            
            # Clear preview for this event
            if event_index in self.preview_changes:
                if primitive in self.preview_changes[event_index]:
                    del self.preview_changes[event_index][primitive]
                if not self.preview_changes[event_index]:
                    del self.preview_changes[event_index]
    
    def toggle_lock(self, event_index: int, perspective: str = "M1") -> bool:
        """
        Toggle lock status of event.
        
        Returns:
            New lock status
        """
        events = self.events_m1 if perspective == "M1" else self.events_m2
        
        if not 0 <= event_index < len(events):
            raise IndexError(f"Event index {event_index} out of range")
        
        events[event_index].locked = not events[event_index].locked
        self.dirty = True
        
        return events[event_index].locked
    
    def get_events(self, perspective: str = "M1") -> List[EventPoint]:
        """Get events for specified perspective."""
        return self.events_m1 if perspective == "M1" else self.events_m2
    
    def get_primitives_array(self, perspective: str = "M1", include_preview: bool = False) -> Dict[str, List[float]]:
        """
        Get primitives as arrays for plotting.
        
        Args:
            perspective: "M1" or "M2"
            include_preview: If True, merge preview changes into values
        
        Returns:
            Dict with keys: 'time', 'v', 'r', 'f', 'a', 'S'
        """
        events = self.get_events(perspective)
        
        result = {
            'time': [e.time for e in events],
            'v': [e.v for e in events],
            'r': [e.r for e in events],
            'f': [e.f for e in events],
            'a': [e.a for e in events],
            'S': [e.S for e in events]
        }
        
        # Apply preview changes if requested
        if include_preview:
            for event_idx, changes in self.preview_changes.items():
                if event_idx < len(events):
                    for prim, value in changes.items():
                        result[prim][event_idx] = value
        
        return result
    
    def commit_all_previews(self, perspective: str = "M1") -> None:
        """Commit all preview changes to the model (safe against dict size change)."""
        to_remove = []
        for event_idx, changes in list(self.preview_changes.items()):
            for prim, value in list(changes.items()):
                self.update_primitive(event_idx, prim, value, perspective, preview=False)
            to_remove.append(event_idx)
        # Remove committed events from preview_changes after iteration
        for event_idx in to_remove:
            if event_idx in self.preview_changes:
                del self.preview_changes[event_idx]
    
    def clear_previews(self) -> None:
        """Clear all preview changes without committing."""
        self.preview_changes.clear()
