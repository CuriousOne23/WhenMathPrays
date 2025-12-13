# tools/editor/editor_utils.py
"""
Utility functions for the interactive editor.
Reduces code duplication and improves maintainability.
"""

from typing import Callable, Dict, Any, Optional
from tools.editor.constants import PRIMITIVE_NAMES


def for_each_primitive(callback: Callable[[str], None]) -> None:
    """
    Execute a callback function for each primitive.
    
    Args:
        callback: Function that takes primitive name as parameter
        
    Example:
        def process_primitive(prim):
            print(f"Processing {prim}")
        
        for_each_primitive(process_primitive)
    """
    for prim in PRIMITIVE_NAMES:
        callback(prim)


def for_each_primitive_with_result(callback: Callable[[str], Any]) -> Dict[str, Any]:
    """
    Execute a callback for each primitive and collect results.
    
    Args:
        callback: Function that takes primitive name and returns a value
        
    Returns:
        Dictionary mapping primitive names to callback results
        
    Example:
        results = for_each_primitive_with_result(lambda p: model.get_value(p))
    """
    return {prim: callback(prim) for prim in PRIMITIVE_NAMES}


def remove_event_markers(model, event_time: float, remove_label_callback: Optional[Callable] = None, event_index: Optional[int] = None) -> None:
    """
    Remove all marker positions and optionally labels for an event.
    
    With marker-centric architecture (v2.2.0), this clears gamma_self positions
    from the Marker objects themselves for the current perspective.
    
    Args:
        model: Editor model
        event_time: Time of the event to clear markers for
        remove_label_callback: Optional callback(event_time, prim) to remove labels
        event_index: Event index (DEPRECATED - no longer used, kept for compatibility)
        
    Example:
        remove_event_markers(
            model, 
            event_time=42.0,
            remove_label_callback=primitive_panel.remove_marker_label,
            event_index=5  # No longer used
        )
    """
    # Find the event with this time in the current events list
    # Note: We need to determine the perspective - this is a limitation of the current API
    # For now, try both perspectives since we don't know which one we're operating on
    for perspective in ['M1', 'M2']:
        events = model.get_events(perspective)
        for event in events:
            if abs(event.time - event_time) < 0.001:  # Float comparison tolerance
                # Clear marker positions from Marker objects
                for prim in PRIMITIVE_NAMES:
                    event.markers[prim].clear_gamma_position(perspective)
                break
        
    # Call label removal callback if provided
    if remove_label_callback:
        for prim in PRIMITIVE_NAMES:
            remove_label_callback(event_time, prim)


def clear_modified_primitives_for_event(model, event_time: float, perspective: str = "M1") -> None:
    """
    Clear modified primitives tracking for a specific event time.
    DEPRECATED: Use model.clear_primitive_modification() instead.
    
    Args:
        model: Editor model with modified_primitives_m1/m2 dicts
        event_time: Time of the event to clear
        perspective: "M1" or "M2"
    """
    # This function is deprecated but kept for backward compatibility
    # Find event by time and clear all its primitives
    events = model.get_events(perspective)
    for event in events:
        if abs(event.time - event_time) < 0.001:
            for prim in ['v', 'r', 'f', 'a', 'S']:
                model.clear_primitive_modification(event.id, prim, perspective)
            break


def get_all_modified_markers(model, events, perspective: str = 'baseline') -> Dict[tuple, bool]:
    """
    Build a dictionary of all modified marker states.
    
    Args:
        model: Editor model with is_modified() method
        events: List of events
        perspective: Which perspective to check ('baseline' or 'partner')
        
    Returns:
        Dictionary mapping (event_idx, primitive) -> is_modified bool
        
    Example:
        modified_state = get_all_modified_markers(controller.model, events, 'baseline')
        # Returns: {(0, 'v'): False, (0, 'r'): True, ...}
    """
    modified_state = {}
    for event_idx in range(len(events)):
        for prim in PRIMITIVE_NAMES:
            if model.is_modified(event_idx, prim, perspective):
                modified_state[(event_idx, prim)] = True
    return modified_state


def count_modified_markers(model, events) -> int:
    """
    Count total number of modified markers across all events.
    
    Args:
        model: Editor model with is_modified() method
        events: List of events
        
    Returns:
        Total count of modified markers
    """
    count = 0
    for event_idx in range(len(events)):
        for prim in PRIMITIVE_NAMES:
            if model.is_modified(event_idx, prim, 'baseline'):
                count += 1
    return count


def validate_primitive_value(value: float, min_val: float = -10.0, max_val: float = 10.0) -> float:
    """
    Clamp primitive value to valid range.
    
    Args:
        value: Input value
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        
    Returns:
        Clamped value within [min_val, max_val]
    """
    return max(min_val, min(max_val, value))


def update_baseline_arrays(baseline_dict: Dict[str, Any], operation: str, index: int, values: Optional[Dict[str, float]] = None) -> None:
    """
    Update baseline primitive arrays with insert or delete operation.
    
    Args:
        baseline_dict: Dictionary containing numpy arrays for each primitive
        operation: Either 'insert' or 'delete'
        index: Index at which to insert/delete
        values: For 'insert', dict mapping primitive names to values (default 0.0)
        
    Example:
        # Insert new event at index 5
        update_baseline_arrays(baseline_primitives, 'insert', 5, {'v': 0.5, 'r': 0.3})
        
        # Delete event at index 7
        update_baseline_arrays(baseline_primitives, 'delete', 7)
    """
    import numpy as np
    
    if operation == 'insert':
        for prim in PRIMITIVE_NAMES:
            if prim in baseline_dict:
                value = values.get(prim, 0.0) if values else 0.0
                baseline_dict[prim] = np.insert(baseline_dict[prim], index, value)
    
    elif operation == 'delete':
        for prim in PRIMITIVE_NAMES:
            if prim in baseline_dict:
                baseline_dict[prim] = np.delete(baseline_dict[prim], index)
