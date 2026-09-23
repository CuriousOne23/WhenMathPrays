from typing import Any, Sequence

from idob.object import IdOBObject


def sum_idob(tp: Any, registry: Sequence[IdOBObject]) -> dict:
    """R1 sum: execute the sole legacy object and return its packet unchanged."""

    for obj in registry:
        if obj.name == "legacy_monolith":
            return obj.apply(tp)
    raise ValueError("R1 registry must contain legacy_monolith")
