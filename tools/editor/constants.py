"""
Central constants for the interactive scenario editor.

Defines primitive names, labels, colors, perspectives, and shared configuration values.
Architectural principle: Define once, use everywhere.
"""

from typing import List

# ============================================================================
# Perspectives
# ============================================================================

PERSPECTIVES: List[str] = ["M1", "M2"]

# ============================================================================
# Primitives
# ============================================================================

PRIMITIVE_NAMES = ['v', 'r', 'f', 'a', 'S']

PRIMITIVE_LABELS = {
    'v': 'Visibility',
    'r': 'Resonance', 
    'f': 'Fidelity',
    'a': 'Altruism',
    'S': 'Shared Breath'
}

PRIMITIVE_COLORS = {
    'v': '#1f77b4',  # blue
    'r': '#ff7f0e',  # orange
    'f': '#2ca02c',  # green
    'a': '#d62728',  # red
    'S': '#9467bd'   # purple
}

# Tolerance for detecting inserted events (all primitives near zero)
INSERTED_EVENT_TOLERANCE = 0.001

# Primitive value limits
PRIMITIVE_MIN: float = -10.0
PRIMITIVE_MAX: float = 10.0

# ============================================================================
# Validation Functions
# ============================================================================

def validate_perspective(perspective: str) -> None:
    """
    Validate perspective value.
    
    Args:
        perspective: Perspective string to validate
        
    Raises:
        ValueError: If perspective is not valid
    """
    if perspective not in PERSPECTIVES:
        raise ValueError(f"Invalid perspective '{perspective}'. Must be one of {PERSPECTIVES}")


def validate_primitive(primitive: str) -> None:
    """
    Validate primitive name.
    
    Args:
        primitive: Primitive name to validate
        
    Raises:
        ValueError: If primitive is not valid
    """
    if primitive not in PRIMITIVE_NAMES:
        raise ValueError(f"Invalid primitive '{primitive}'. Must be one of {PRIMITIVE_NAMES}")


def validate_primitive_value(value: float) -> None:
    """
    Validate primitive value is within valid range.
    
    Args:
        value: Primitive value to validate
        
    Raises:
        ValueError: If value is out of range
    """
    if not (PRIMITIVE_MIN <= value <= PRIMITIVE_MAX):
        raise ValueError(
            f"Primitive value {value} out of range [{PRIMITIVE_MIN}, {PRIMITIVE_MAX}]"
        )

# ============================================================================
# Helper Functions
# ============================================================================

def is_inserted_event(event, exclude_first_last: bool = True, event_idx: int = None, total_events: int = None) -> bool:
    """
    Detect if an event is an inserted event (all primitives near zero).
    
    Args:
        event: Event object with markers attribute
        exclude_first_last: If True, first/last events are never considered inserted
        event_idx: Index of event (required if exclude_first_last=True)
        total_events: Total number of events (required if exclude_first_last=True)
    
    Returns:
        True if event has all primitives near zero (and not first/last if excluded)
    """
    if exclude_first_last:
        if event_idx is None or total_events is None:
            raise ValueError("event_idx and total_events required when exclude_first_last=True")
        if event_idx == 0 or event_idx >= total_events - 1:
            return False
    
    return all(abs(event.markers[prim].value) < INSERTED_EVENT_TOLERANCE for prim in PRIMITIVE_NAMES)
