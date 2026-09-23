from typing import Any, Dict, Iterable, Tuple


def as_packet(packet: Dict[str, Any]) -> Dict[str, Any]:
    """Pass-through packet helper kept for staged evolution."""

    return packet


def merge_packet_fields(base: Dict[str, Any], contribution: Dict[str, Any]) -> Dict[str, Any]:
    """Merge contribution keys into a packet-sized dict using R0-compatible semantics."""

    merged = dict(base)
    for key, value in contribution.items():
        if key == "semantic_core" and key in merged:
            # Keep stable, de-duplicated order for list-based semantic core.
            existing = merged.get(key, [])
            if not isinstance(existing, list):
                existing = []
            add = value if isinstance(value, list) else [value]
            merged[key] = list(dict.fromkeys(existing + add))
            continue
        merged[key] = value
    return merged


def apply_overlap_modes(
    active_names: Iterable[str],
    packet: Dict[str, Any],
    overlap_graph: Dict[str, Dict[Tuple[str, str], str]],
) -> Dict[str, Any]:
    """Apply declared overlap modes internally without emitting overlap metadata in R2."""

    near = overlap_graph.get("near", {})
    far = overlap_graph.get("far", {})
    name_set = set(active_names)
    result = dict(packet)

    # Keep behavior aligned with R0: interrogative suppresses declarative mood.
    if "interrogative_wh" in name_set or "interrogative_polar" in name_set:
        if near.get(("interrogative_wh", "interrogative_polar")) == "suppress" or far.get(
            ("interrogative_wh", "copular_state")
        ) == "suppress":
            result["truth_relation"] = "interrogative"

    return result
