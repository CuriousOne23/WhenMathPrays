"""
Data model for interactive scenario editor.

Handles event data, CSV I/O, and modification tracking.
"""

import csv
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from pathlib import Path
from tools.editor.observable import ObservableDict


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
        self.filepath: str = ""  # Store filepath for fallback name extraction
        self.gamma_self_0: complex = 0 + 0j  # Initial gamma_self position
        self.gamma_self_0_original: complex = 0 + 0j  # Original value from CSV
        self.gamma_self_0_modified: bool = False  # Whether gamma_self_0 has been changed
        self.events: list = []  # List of Event objects (new structure)
        self.events_m1: list = []  # Events for perspective M1
        self.events_m2: list = []  # Events for perspective M2
        self.filepath: Optional[Path] = None
        self.dirty: bool = False  # Unsaved changes?
        self.modified_indices: set = set()  # Track which events were modified
        self.modified_primitives: ObservableDict = ObservableDict()  # {event_time: {'v', 'r', ...}}
        # Preview state (uncommitted changes)
        self.preview_changes: Dict[int, Dict[str, float]] = {}  # {event_idx: {primitive: value}}
        # Pinned marker positions: where gamma_self was when each primitive was first modified
        self.marker_positions: Dict[tuple, complex] = {}  # {(event_time, primitive): gamma_self_position}
    
    def load_csv(self, filepath: str, perspective: str = "M1") -> None:
        """
        Load scenario from CSV file using new Event/Marker structure.
        Args:
            filepath: Path to CSV file
            perspective: "M1" or "M2" (currently only M1 supported)
        """
        from tools.editor.load_events import load_events_from_csv
        self.filepath = Path(filepath)
        events, metadata = load_events_from_csv(filepath)
        print(f"[DEBUG] EditorModel.load_csv: loaded {len(events)} events from {filepath}")
        
        # Apply metadata to model
        self.gamma_self_0 = metadata.get('gamma_self_0', 0+0j)
        self.gamma_self_0_original = self.gamma_self_0  # Store original for reset
        self.gamma_self_0_modified = False  # Not modified on load
        self.time_unit = metadata.get('time_unit', 'days')
        if metadata.get('name'):
            self.name = metadata['name']
        print(f"[DEBUG] EditorModel.load_csv: gamma_self_0 = {self.gamma_self_0}")
        
        if perspective == "M1":
            self.events_m1 = events
        else:
            self.events_m2 = events
    
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
        print(f"[SAVE] modified_primitives before save: {self.modified_primitives}")
        # Build time-to-index mapping
        time_to_idx = {evt.time: idx for idx, evt in enumerate(events)}
        for mod_time, mod_prims in self.modified_primitives.items():
            if mod_time in time_to_idx:
                idx = time_to_idx[mod_time]
                event = events[idx]
                # Only set marker if not already set
                if not event.marker:
                    event.marker = 'circle'
                    print(f"[SAVE] Set marker='circle' for event at time {mod_time} (index {idx})")
                else:
                    print(f"[SAVE] Event at time {mod_time} (index {idx}) already has marker='{event.marker}'")
                # Always lock modified events
                event.locked = True
                print(f"[SAVE] Set locked=True for event at time {mod_time} (index {idx}), modified prims: {mod_prims}")

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
            fieldnames = ['day', 'v', 'r', 'f', 'a', 'S', 'notes', 'marker', 'locked']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for event in events:
                writer.writerow(event.to_dict())
        
        self.dirty = False
        print(f"Saved {len(events)} events to {filepath}")
    
    def update_primitive(self, event_index: int, primitive: str, value: float, 
                        perspective: str = "M1", preview: bool = True) -> None:
        print(f"[DEBUG] update_primitive called: event={event_index}, prim={primitive}, value={value}, preview={preview}")
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
            events[event_index].markers[primitive].value = value

            # Auto-mark as modified (set style or a marker property)
            marker_obj = events[event_index].markers[primitive]
            if not getattr(marker_obj, 'style', None):
                marker_obj.style = 'circle'  # Or set a property to indicate modified

            # Track which primitive was modified (by event TIME, not index)
            event_time = events[event_index].time
            if event_time not in self.modified_primitives:
                self.modified_primitives[event_time] = set()
            self.modified_primitives[event_time].add(primitive)

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
            'v': [e.markers['v'].value for e in events],
            'r': [e.markers['r'].value for e in events],
            'f': [e.markers['f'].value for e in events],
            'a': [e.markers['a'].value for e in events],
            'S': [e.markers['S'].value for e in events]
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
    
    def insert_event(self, time: float, perspective: str = "M1") -> int:
        """
        Insert a new event at specified time with all primitives set to 0 (neutral).
        This creates a visible insertion point with no effect on gamma_self trajectory.
        User can then drag primitives to non-zero values to shape the trajectory.
        
        Args:
            time: Time value for new event
            perspective: "M1" or "M2"
        
        Returns:
            Index of newly inserted event
        """
        from tools.editor.event import Event
        
        events = self.events_m1 if perspective == "M1" else self.events_m2
        
        # Find insertion index (maintain sorted order by time)
        insert_idx = 0
        for i, event in enumerate(events):
            if event.time < time:
                insert_idx = i + 1
            else:
                break
        
        # Set all primitives to 0 (neutral - no effect on trajectory)
        primitives = {'v': 0.0, 'r': 0.0, 'f': 0.0, 'a': 0.0, 'S': 0.0}
        
        # Create and insert new event
        new_event = Event(time, primitives, notes=f"Inserted at t={time}")
        events.insert(insert_idx, new_event)
        self.dirty = True
        
        # NOTE: modified_primitives uses time values as keys, so no shifting needed
        print(f"[INSERT] modified_primitives (time-based, no shift needed): {self.modified_primitives}")
        
        # Mark this event as an inserted event for visual distinction
        if not hasattr(self, 'inserted_events'):
            self.inserted_events = set()
        self.inserted_events.add(insert_idx)
        
        return insert_idx
    
    def delete_event(self, event_index: int, perspective: str = "M1") -> Event:
        """
        Delete an event at specified index.
        
        Args:
            event_index: Index of event to delete
            perspective: "M1" or "M2"
        
        Returns:
            Deleted event (for undo support)
        
        Raises:
            ValueError: If event is locked or if trying to delete first/last event
        """
        events = self.events_m1 if perspective == "M1" else self.events_m2
        
        if not 0 <= event_index < len(events):
            raise IndexError(f"Event index {event_index} out of range")
        
        if events[event_index].locked:
            raise ValueError("Cannot delete locked event")
        
        if event_index == 0 or event_index == len(events) - 1:
            raise ValueError("Cannot delete first or last event")
        
        deleted_event = events.pop(event_index)
        self.dirty = True
        
        # Shift modified_primitives indices for all events after event_index
        # Remove modifications for the deleted event (by time value)
        deleted_time = events[event_index].time
        if deleted_time in self.modified_primitives:
            print(f"[DELETE] Removing modifications for deleted event at time {deleted_time}")
            del self.modified_primitives[deleted_time]
        print(f"[DELETE] modified_primitives after delete: {self.modified_primitives}")
        
        return deleted_event
    
    def get_display_name(self, perspective: str = "M1") -> str:
        """
        Get display name for the scenario.
        
        Returns:
            - self.name if set in CSV
            - "M1" or "M2" if filename contains _M1 or _M2
            - perspective ("M1" or "M2") as fallback
        """
        if self.name:
            return self.name
        
        # Try to extract from filename
        if self.filepath:
            import os
            filename = os.path.basename(self.filepath)
            if '_M1' in filename or filename.startswith('M1'):
                return 'M1'
            elif '_M2' in filename or filename.startswith('M2'):
                return 'M2'
        
        # Fallback to perspective
        return perspective
    
    # === Phase 1: Query Interface (Single Source of Truth) ===
    
    def get_event(self, event_idx: int, perspective: str = "M1"):
        """
        Get single event by index.
        
        Args:
            event_idx: Zero-based event index
            perspective: "M1" or "M2"
        
        Returns:
            Event object
        
        Raises:
            IndexError: If event_idx out of range
        """
        events = self.get_events(perspective)
        if not 0 <= event_idx < len(events):
            raise IndexError(f"Event index {event_idx} out of range [0, {len(events)})")
        return events[event_idx]
    
    def is_modified(self, event_idx: int, prim: str, perspective: str = "M1") -> bool:
        """
        Check if primitive has been modified from baseline.
        
        Args:
            event_idx: Zero-based event index
            prim: Primitive name ('v', 'r', 'f', 'a', 'S')
            perspective: "M1" or "M2"
        
        Returns:
            True if modified, False if at baseline
        """
        events = self.get_events(perspective)
        if event_idx >= len(events):
            return False
        event_time = events[event_idx].time
        if event_time not in self.modified_primitives:
            return False
        return prim in self.modified_primitives[event_time]
    
    def is_primitive_modified(self, event_idx: int, prim: str, perspective: str = "M1") -> bool:
        """Alias for is_modified() for backwards compatibility."""
        return self.is_modified(event_idx, prim, perspective)
    
    def get_baseline_value(self, event_idx: int, prim: str, perspective: str = "M1") -> float:
        """
        Get the original (pre-edit) value of a primitive.
        
        Args:
            event_idx: Zero-based event index
            prim: Primitive name
            perspective: "M1" or "M2"
        
        Returns:
            Original value from file load or last save
        
        Raises:
            IndexError: If event_idx out of range
            KeyError: If prim invalid
        """
        # Use controller's baseline_primitives if available, otherwise current value
        # Note: This requires baseline to be stored separately during load
        # For now, return current value if not modified (assumes unchanged = baseline)
        events = self.get_events(perspective)
        if not 0 <= event_idx < len(events):
            raise IndexError(f"Event index {event_idx} out of range")
        
        event = events[event_idx]
        if prim not in ['v', 'r', 'f', 'a', 'S']:
            raise KeyError(f"Invalid primitive: {prim}")
        
        # Return the marker value (baseline stored elsewhere in controller)
        # This method will be improved when we add baseline storage to model
        return event.markers[prim].value
    
    def get_modified_events(self, perspective: str = "M1") -> set:
        """
        Get indices of all events with modifications.
        
        Args:
            perspective: "M1" or "M2"
        
        Returns:
            Set of event indices with at least one modified primitive
        """
        # modified_primitives keys are time values, convert to current indices
        events = self.get_events(perspective)
        modified_indices = set()
        time_to_idx = {evt.time: idx for idx, evt in enumerate(events)}
        for mod_time in self.modified_primitives.keys():
            if mod_time in time_to_idx:
                modified_indices.add(time_to_idx[mod_time])
        return modified_indices
    
    def reset_event_primitive(self, event_idx: int, prim: str, baseline_value: float, perspective: str = "M1") -> float:
        """
        Reset single primitive to baseline value.
        
        Args:
            event_idx: Zero-based event index
            prim: Primitive name
            baseline_value: The baseline value to restore
            perspective: "M1" or "M2"
        
        Returns:
            The baseline value that was restored
        
        Raises:
            IndexError: If event_idx out of range
            KeyError: If prim invalid
        """
        events = self.get_events(perspective)
        if not 0 <= event_idx < len(events):
            raise IndexError(f"Event index {event_idx} out of range")
        
        if prim not in ['v', 'r', 'f', 'a', 'S']:
            raise KeyError(f"Invalid primitive: {prim}")
        
        # Reset the value
        event = events[event_idx]
        event.markers[prim].value = baseline_value
        
        # Remove from modified set (by time)
        event_time = event.time
        if event_time in self.modified_primitives:
            self.modified_primitives[event_time].discard(prim)
            if not self.modified_primitives[event_time]:
                del self.modified_primitives[event_time]
        
        self.dirty = True
        return baseline_value
