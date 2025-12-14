"""
Data model for interactive scenario editor.

Handles event data, CSV I/O, and modification tracking.
"""

import csv
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from pathlib import Path
from tools.editor.observable import ObservableDict
from tools.editor.state_viewer import StateViewer


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
    """
    Model for interactive scenario editing.
    
    Manages event data, CSV I/O, and modification tracking for dual-perspective editing.
    Supports both M1 (first person) and M2 (second person) perspectives with independent
    event lists and shared modification tracking.
    
    Attributes:
        events_m1: List of EventPoint objects for M1 perspective
        events_m2: List of EventPoint objects for M2 perspective
        name_m1: Scenario name for M1 perspective
        name_m2: Scenario name for M2 perspective
        modified_primitives: ObservableDict tracking which primitives have been modified (time-based keys)
        preview_changes: Dict storing temporary preview changes during drag operations
        marker_positions: Dict storing gamma_self positions for modified event markers
        gamma_self_0: Initial gamma_self position (complex number)
        time_unit: Time unit for scenario (e.g., "days")
    """
    
    def __init__(self):
        self.name: str = ""  # Deprecated: use name_m1 and name_m2
        self.name_m1: str = ""  # Name for M1 perspective
        self.name_m2: str = ""  # Name for M2 perspective
        self.time_unit: str = "days"
        self.filepath: str = ""  # Store filepath for fallback name extraction
        self.gamma_self_0: complex = 0 + 0j  # Initial gamma_self position
        self.gamma_self_0_original: complex = 0 + 0j  # Original value from CSV
        self.gamma_self_0_modified: bool = False  # Whether gamma_self_0 has been changed
        self.events: list = []  # List of Event objects (new structure)
        self.events_m1: list = []  # Events for perspective M1
        self.events_m2: list = []  # Events for perspective M2
        self.next_event_id: int = 0  # Monotonically increasing event ID counter
        self.filepath: Optional[Path] = None
        self.dirty: bool = False  # Unsaved changes?
        self.modified_indices: set = set()  # Track which events were modified
        
        # Perspective-specific modification tracking (ID-based for immutable identity)
        self.modified_primitives_m1: ObservableDict = ObservableDict()  # {event_id: {'v', 'r', ...}}
        self.modified_primitives_m2: ObservableDict = ObservableDict()  # {event_id: {'v', 'r', ...}}
        
        # Preview state (uncommitted changes)
        self.preview_changes: Dict[int, Dict[str, float]] = {}  # {event_idx: {primitive: value}}
        
        # DEPRECATED: Marker positions now stored in Marker objects themselves
        # These dicts kept for backward compatibility only, built on-demand by get_marker_positions()
        self.marker_positions_m1: Dict[tuple, complex] = {}  # {(event_id, primitive): gamma_self_position}
        self.marker_positions_m2: Dict[tuple, complex] = {}  # {(event_id, primitive): gamma_self_position}
    
    def load_csv(self, filepath: str, perspective: str = "M1") -> None:
        """
        Load scenario from CSV file using new Event/Marker structure.
        Args:
            filepath: Path to CSV file
            perspective: "M1" or "M2"
        """
        from tools.editor.load_events import load_events_from_csv
        self.filepath = Path(filepath)
        
        # Pass current next_event_id as start_id for this perspective's events
        events, metadata, next_id = load_events_from_csv(filepath, start_id=self.next_event_id)
        self.next_event_id = next_id  # Update counter with next available ID
        print(f"[DEBUG] EditorModel.load_csv: loaded {len(events)} events from {filepath}, next_event_id now {self.next_event_id}")
        
        # Apply metadata to model
        self.gamma_self_0 = metadata.get('gamma_self_0', 0+0j)
        self.gamma_self_0_original = self.gamma_self_0  # Store original for reset
        self.gamma_self_0_modified = False  # Not modified on load
        self.time_unit = metadata.get('time_unit', 'days')
        
        # Store perspective-specific name
        if metadata.get('name'):
            if perspective == "M1":
                self.name_m1 = metadata['name']
            else:
                self.name_m2 = metadata['name']
        
        print(f"[DEBUG] EditorModel.load_csv: gamma_self_0 = {self.gamma_self_0}")
        
        if perspective == "M1":
            self.events_m1 = events
        else:
            self.events_m2 = events
        
        # Record file loading for State Viewer
        if perspective == "M1":
            StateViewer.set_loaded_files(m1_path=filepath)
        else:
            StateViewer.set_loaded_files(m2_path=filepath)
    
    def save_csv(self, filepath: str, perspective: str = "M1") -> None:
        """
        Save scenario to CSV file.
        Always exports with full format (marker and locked columns).
        Ensures marker is set for edited events and locked column is set for locked events.
        Args:
            filepath: Output path
            perspective: "M1" or "M2"
        """
        # Capture before state
        before_dirty = self.dirty
        
        events = self.events_m1 if perspective == "M1" else self.events_m2

        # Ensure marker and locked columns are set for edited/locked events
        modified_prims = self.get_modified_primitives(perspective)
        print(f"[SAVE] modified_primitives before save: {modified_prims}")
        # Build time-to-index mapping
        time_to_idx = {evt.time: idx for idx, evt in enumerate(events)}
        for mod_time, mod_prims_set in modified_prims.items():
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
                print(f"[SAVE] Set locked=True for event at time {mod_time} (index {idx}), modified prims: {mod_prims_set}")

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            # Write metadata if present
            # Use perspective-specific name
            name = self.name_m1 if perspective == "M1" else self.name_m2
            if name:
                f.write(f"name,{name}\n")
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
        
        # Record state transition
        StateViewer.record(
            operation='save_csv',
            entity=(perspective, filepath),
            changes={
                'dirty': (before_dirty, False),
                'event_count': (len(events), len(events))
            }
        )
        
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
            # Capture before state
            event = events[event_index]
            marker_obj = event.markers[primitive]
            event_id = event.id
            before_value = marker_obj.value
            before_in_modified = event_id in self.get_modified_primitives(perspective) and primitive in self.get_modified_primitives(perspective).get(event_id, set())
            
            # Commit change
            events[event_index].markers[primitive].value = value

            # Auto-mark as modified (set style or a marker property)
            if not getattr(marker_obj, 'style', None):
                marker_obj.style = 'circle'  # Or set a property to indicate modified

            # Track which primitive was modified (by event ID, not time or index)
            modified_prims = self.get_modified_primitives(perspective)
            if event_id not in modified_prims:
                modified_prims[event_id] = set()
            modified_prims[event_id].add(primitive)

            # Capture after state
            after_value = marker_obj.value
            after_in_modified = event_id in modified_prims and primitive in modified_prims.get(event_id, set())
            
            # Record state transition
            StateViewer.record(
                operation='update_primitive',
                entity=(event_id, primitive, perspective),
                changes={
                    'value': (before_value, after_value),
                    'in_modified_dict': (before_in_modified, after_in_modified)
                }
            )

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
        
        # Capture before state
        event = events[event_index]
        event_id = event.id
        before_locked = event.locked
        
        events[event_index].locked = not events[event_index].locked
        self.dirty = True
        
        # Capture after state
        after_locked = events[event_index].locked
        
        # Record state transition
        StateViewer.record(
            operation='toggle_lock',
            entity=(event_id, perspective, event_index),
            changes={
                'locked': (before_locked, after_locked)
            }
        )
        
        return events[event_index].locked
    
    def get_events(self, perspective: str = "M1") -> List[EventPoint]:
        """
        Get events list for the specified perspective.
        
        Returns a copy of the events list to prevent external modification of the
        internal state. Use update methods to modify events.
        
        Args:
            perspective: "M1" or "M2"
            
        Returns:
            List of EventPoint objects for the specified perspective
        """
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
        
        # Capture before state
        before_count = len(events)
        
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
        
        # Mark this event as an inserted event for visual distinction
        if not hasattr(self, 'inserted_events'):
            self.inserted_events = set()
        self.inserted_events.add(insert_idx)
        
        # Capture after state
        after_count = len(events)
        
        # Record state transition
        StateViewer.record(
            operation='insert_event',
            entity=(insert_idx, perspective, time),
            changes={
                'event_count': (before_count, after_count),
                'inserted_at_index': (None, insert_idx)
            }
        )
        
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
        
        # Capture before state
        before_count = len(events)
        deleted_event_id = events[event_index].id
        deleted_time = events[event_index].time
        
        deleted_event = events.pop(event_index)
        self.dirty = True
        
        # Shift modified_primitives indices for all events after event_index
        # Remove modifications for the deleted event (by event ID)
        modified_prims = self.get_modified_primitives(perspective)
        was_in_modified = deleted_event_id in modified_prims
        if was_in_modified:
            print(f"[DELETE] Removing modifications for deleted event ID {deleted_event_id}")
            del modified_prims[deleted_event_id]
        print(f"[DELETE] modified_primitives after delete: {modified_prims}")
        
        # Capture after state
        after_count = len(events)
        
        # Record state transition
        StateViewer.record(
            operation='delete_event',
            entity=(deleted_event_id, perspective, event_index),
            changes={
                'event_count': (before_count, after_count),
                'deleted_time': (deleted_time, None),
                'was_in_modified_dict': (was_in_modified, False)
            }
        )
        
        return deleted_event
    
    def get_display_name(self, perspective: str = "M1") -> str:
        """
        Get display name for the scenario.
        
        Returns:
            - name_m1 or name_m2 if set in CSV
            - "M1" or "M2" if filename contains _M1 or _M2
            - perspective ("M1" or "M2") as fallback
        """
        # Use perspective-specific name
        if perspective == "M1" and self.name_m1:
            return self.name_m1
        elif perspective == "M2" and self.name_m2:
            return self.name_m2
        
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
        
        event_id = events[event_idx].id
        modified_prims = self.get_modified_primitives(perspective)
        
        if event_id not in modified_prims:
            return False
        
        return prim in modified_prims[event_id]
    
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
        modified_prims = self.get_modified_primitives(perspective)
        modified_indices = set()
        time_to_idx = {evt.time: idx for idx, evt in enumerate(events)}
        for mod_time in modified_prims.keys():
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
        
        # Capture before state
        event = events[event_idx]
        marker = event.markers[prim]
        event_id = event.id
        before_value = marker.value
        before_gamma = marker.gamma_self_position.get(perspective)
        before_in_modified = event_id in self.get_modified_primitives(perspective) and prim in self.get_modified_primitives(perspective).get(event_id, set())
        
        # Reset the value
        event.markers[prim].value = baseline_value
        
        # Clear the gamma_self position for this marker
        event.markers[prim].clear_gamma_position(perspective)
        print(f"[MODEL_RESET] Cleared gamma position for event {event.id}, primitive {prim}, perspective {perspective}")
        
        # Remove from modified set (using event ID, not time!)
        # NOTE: modified_primitives uses event.id as keys, despite some confusion in comments
        modified_prims = self.get_modified_primitives(perspective)
        if event_id in modified_prims:
            modified_prims[event_id].discard(prim)
            if not modified_prims[event_id]:
                del modified_prims[event_id]
                print(f"[MODEL_RESET] Removed event {event_id} from modified_primitives (no more modified prims)")
            else:
                print(f"[MODEL_RESET] Removed {prim} from event {event_id} modified set, remaining: {modified_prims[event_id]}")
        else:
            print(f"[MODEL_RESET] Event {event_id} not in modified_primitives")
        
        # Capture after state
        after_value = marker.value
        after_gamma = marker.gamma_self_position.get(perspective)
        after_in_modified = event_id in self.get_modified_primitives(perspective) and prim in self.get_modified_primitives(perspective).get(event_id, set())
        
        # Record state transition
        StateViewer.record(
            operation='reset_primitive',
            entity=(event_id, prim, perspective),
            changes={
                'value': (before_value, after_value),
                'gamma_position': (before_gamma, after_gamma),
                'in_modified_dict': (before_in_modified, after_in_modified)
            }
        )
        
        self.dirty = True
        return baseline_value
    
    # === Perspective-Aware API Methods ===
    
    def get_modified_primitives(self, perspective: str = "M1") -> ObservableDict:
        """
        Get modified primitives dictionary for specific perspective.
        
        Args:
            perspective: "M1" or "M2"
        
        Returns:
            ObservableDict mapping event_time to set of modified primitive names
        """
        return self.modified_primitives_m1 if perspective == "M1" else self.modified_primitives_m2
    
    def get_marker_positions(self, perspective: str = "M1") -> Dict[tuple, complex]:
        """
        Get pinned marker positions for specific perspective.
        Builds dict from Marker objects for backward compatibility with view code.
        
        Args:
            perspective: "M1" or "M2"
        
        Returns:
            Dict mapping (event_time, primitive) to gamma_self position
        """
        # Build dictionary from Marker objects
        positions = {}
        events = self.get_events(perspective)
        for event in events:
            for prim in ['v', 'r', 'f', 'a', 'S']:
                gamma_pos = event.markers[prim].get_gamma_position(perspective)
                if gamma_pos is not None:
                    positions[(event.time, prim)] = gamma_pos
        return positions
    
    def pin_marker(self, event_id: int, primitive: str, gamma_self_position: complex, perspective: str = "M1"):
        """
        Pin a marker at specific gamma_self position for given perspective.
        Single entry point for debugging marker position changes.
        
        Args:
            event_id: Event ID (immutable identifier)
            primitive: Primitive name ('v', 'r', 'f', 'a', 'S')
            gamma_self_position: Complex number representing gamma_self value
            perspective: "M1" or "M2"
        """
        # Find event by ID and set gamma position on its marker
        events = self.get_events(perspective)
        for event in events:
            if event.id == event_id:
                event.markers[primitive].set_gamma_position(perspective, gamma_self_position)
                return
    
    def unpin_marker(self, event_id: int, primitive: str, perspective: str = "M1"):
        """
        Remove a marker from pinned positions (when primitive returns to baseline).
        Single entry point for debugging marker position removal.
        
        Args:
            event_id: Event ID (immutable identifier)
            primitive: Primitive name ('v', 'r', 'f', 'a', 'S')
            perspective: "M1" or "M2"
        """
        # Find event by ID and clear gamma position on its marker
        events = self.get_events(perspective)
        for event in events:
            if event.id == event_id:
                event.markers[primitive].clear_gamma_position(perspective)
                return
    
    def clear_primitive_modification(self, event_id: int, primitive: str, perspective: str = "M1"):
        """
        Clear modification flag for a primitive (when reset to baseline).
        Single entry point for debugging modification state changes.
        
        Args:
            event_id: Event ID (immutable identifier)
            primitive: Primitive name ('v', 'r', 'f', 'a', 'S')
            perspective: "M1" or "M2"
        """
        # Clear from Model's tracking dict (for backward compatibility)
        modified_prims = self.get_modified_primitives(perspective)
        if event_id in modified_prims:
            modified_prims[event_id].discard(primitive)
            # If no more modifications for this event, remove the event ID key
            if not modified_prims[event_id]:
                del modified_prims[event_id]
        
        # Also clear on Marker object itself
        events = self.get_events(perspective)
        for event in events:
            if event.id == event_id:
                event.markers[primitive].set_is_modified(perspective, False)
                return
