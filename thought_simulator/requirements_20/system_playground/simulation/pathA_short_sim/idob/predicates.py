from typing import Any


def always_active(_: Any) -> bool:
    """Always-on activation for fallback and parity objects."""

    return True


def is_interrogative(tp: Any) -> bool:
    cues = getattr(tp, "semantic_adjacent_cues", [])
    raw_text = str(getattr(tp, "raw_text", "")).strip()
    return "interrogative_scope" in cues or raw_text.endswith("?")


def has_locative(tp: Any) -> bool:
    cues = getattr(tp, "semantic_adjacent_cues", [])
    return "locative_adjacent" in cues


def has_constraints(tp: Any) -> bool:
    return bool(getattr(tp, "constraints_matched", []))


def has_entity_role(tp: Any) -> bool:
    return any(role == "entity" for role in getattr(tp, "struct_roles", []))


def has_roles(tp: Any) -> bool:
    return bool(getattr(tp, "struct_roles", []))
