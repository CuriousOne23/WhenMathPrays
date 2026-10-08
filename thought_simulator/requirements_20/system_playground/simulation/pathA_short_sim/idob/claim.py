"""S2M rung 1. A readable claim from the packet. Not M. Does not reopen structure."""

from typing import Any, Dict

from idob.mapping import map_packet


def _clean(value: Any) -> str:
    return str(value or "").strip()


def claim_from_packet(tp: Dict[str, Any]) -> Dict[str, Any]:
    segments_before = list(tp.get("struct_segments") or [])
    mapped = map_packet(tp)
    core = mapped.get("semantic_core") or {}
    theme = _clean(core.get("theme"))
    state = _clean(core.get("state"))
    location = _clean(core.get("location"))
    action = _clean(core.get("action"))
    patient = _clean(core.get("patient"))
    query = _clean(core.get("query_focus"))
    parts = []
    if query:
        parts.append(f"query {query}")
    if theme and action and patient:
        parts.append(f"{theme} {action} {patient}")
    elif theme and state:
        parts.append(f"{theme} is {state}")
    elif theme and location:
        parts.append(f"{theme} at {location}")
    elif action:
        parts.append(action)
    claim = "; ".join(parts)
    status = "claimed" if claim else mapped.get("status", "claim_empty")
    if list(tp.get("struct_segments") or []) != segments_before:
        status = "illegal"
    return {
        "status": status,
        "claim": claim,
        "source": "idob_packet",
        "structure_reopened": False,
        "instruments_not_computed": ["M", "envelope", "delta_h"],
    }
