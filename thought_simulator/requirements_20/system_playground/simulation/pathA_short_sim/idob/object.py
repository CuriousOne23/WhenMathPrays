from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass(frozen=True)
class IdOBObject:
    """R3 object wrapper with activation, ordering, and contribution extraction."""

    name: str
    family: str
    priority: int
    activate: Callable[[Any], bool]
    apply: Callable[[Any], Dict[str, Any]]
