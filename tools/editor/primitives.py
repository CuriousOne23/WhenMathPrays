"""
Primitive definitions - single source of truth for primitive metadata.

This module defines all primitive names, labels, colors, and descriptions.
Update here when primitive names change to maintain consistency across the codebase.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class PrimitiveInfo:
    """Metadata for a single primitive."""
    key: str           # Short key (v, r, f, a, S)
    name: str          # Full name (Visibility, Resonance, etc.)
    color: str         # Hex color code for visualization
    description: str   # Human-readable description


# Primitive definitions
PRIMITIVES: Dict[str, PrimitiveInfo] = {
    'v': PrimitiveInfo(
        key='v',
        name='Visibility',
        color='#1f77b4',  # Blue
        description='How visible/present each person is to the other'
    ),
    'r': PrimitiveInfo(
        key='r',
        name='Resonance',
        color='#ff7f0e',  # Orange
        description='Emotional alignment and attunement'
    ),
    'f': PrimitiveInfo(
        key='f',
        name='Fidelity',
        color='#2ca02c',  # Green
        description='Trustworthiness and reliability'
    ),
    'a': PrimitiveInfo(
        key='a',
        name='Altruism',
        color='#d62728',  # Red
        description='Selfless care and generosity'
    ),
    'S': PrimitiveInfo(
        key='S',
        name='Shared Breath',
        color='#9467bd',  # Purple
        description='Soul-level connection'
    )
}

# Canonical ordering for display
PRIMITIVE_ORDER = ['v', 'r', 'f', 'a', 'S']

# Convenience accessors
PRIMITIVE_NAMES = PRIMITIVE_ORDER
PRIMITIVE_LABELS = {k: f"{v.name} ({k})" for k, v in PRIMITIVES.items()}
PRIMITIVE_COLORS = {k: v.color for k, v in PRIMITIVES.items()}
