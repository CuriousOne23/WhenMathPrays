from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass(frozen=True)
class IdOBObject:
    """R2 object wrapper with activation and contribution extraction."""

    name: str
    family: str
    activate: Callable[[Any], bool]
    apply: Callable[[Any], Dict[str, Any]]
