from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class IdOBObject:
    """Minimal R1 object wrapper for a callable IdOB contribution."""

    name: str
    apply: Callable[[Any], dict]
