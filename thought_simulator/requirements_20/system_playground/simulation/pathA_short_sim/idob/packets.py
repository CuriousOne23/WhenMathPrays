from typing import Any, Dict, Iterable, List, Tuple


def as_packet(packet: Dict[str, Any]) -> Dict[str, Any]:
    """Pass-through packet helper kept for staged evolution."""

    return packet


def merge_packet_fields(base: Dict[str, Any], contribution: Dict[str, Any]) -> Dict[str, Any]:
    """Merge contribution keys into a packet-sized dict with dict-only semantic_core."""

    merged = dict(base)
    for key, value in contribution.items():
        if key == "semantic_core" and key in merged:
            existing = merged.get(key, {})
            if not isinstance(existing, dict):
                existing = {}
            add = value if isinstance(value, dict) else {}
            merged[key] = {**existing, **add}
            continue
        if key == "semantic_core_tokens":
            existing_tokens = merged.get(key, [])
            if not isinstance(existing_tokens, list):
                existing_tokens = []
            add_tokens = value if isinstance(value, list) else [value]
            merged[key] = list(dict.fromkeys(existing_tokens + add_tokens))
            continue
        merged[key] = value
    return merged


def apply_overlap_modes(
    active_names: Iterable[str],
    packet: Dict[str, Any],
    overlap_graph: Dict[str, Dict[Tuple[str, str], str]],
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Apply declared overlap modes and return executed overlap events."""

    near = overlap_graph.get("near", {})
    far = overlap_graph.get("far", {})
    name_set = set(active_names)
    result = dict(packet)
    events: List[Dict[str, Any]] = []

    for (a, b), mode in sorted(near.items()):
        if a in name_set and b in name_set:
            events.append({"a": a, "b": b, "mode": mode, "fields": []})

    for (a, b), mode in sorted(far.items()):
        if a in name_set and b in name_set:
            events.append({"a": a, "b": b, "mode": mode, "fields": []})

    # Keep behavior aligned with R0: interrogative suppresses declarative mood.
    if "interrogative_wh" in name_set or "interrogative_polar" in name_set:
        if near.get(("interrogative_wh", "interrogative_polar")) == "suppress" or far.get(
            ("interrogative_wh", "copular_state")
        ) == "suppress":
            result["truth_relation"] = "interrogative"

    return result, events


def claimed_fields_from_contributions(contributions: List[Dict[str, Any]]) -> List[str]:
    fields: List[str] = []
    for contribution in contributions:
        fragment = contribution.get("fragment", {})
        if not isinstance(fragment, dict):
            continue
        for field_name in fragment.keys():
            if field_name not in fields:
                fields.append(field_name)
    return fields
