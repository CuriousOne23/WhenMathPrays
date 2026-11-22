"""Characterization dispatcher scaffold for milestone-1.

This module will own type/version resolution and dispatch boundaries.
Execution logic is intentionally deferred to later batches.
"""

from typing import Any, Dict


def resolve_characterization(_type_name: str, _version: str) -> Dict[str, Any]:
    """Placeholder for later dispatch resolution implementation."""
    raise NotImplementedError("Dispatcher resolution is implemented in a later batch.")

