from typing import Any, Dict

from idob.object import IdOBObject
from idob.predicates import (
    always_active,
    has_constraints,
    has_entity_role,
    has_locative,
    has_roles,
    is_interrogative,
    is_interrogative_polar,
    is_interrogative_wh,
    query_focus_text,
)


def _legacy_apply(tp: Any) -> Dict[str, Any]:
    # Lazy import avoids a module cycle with primitives_pathA_short.
    from primitives_pathA_short import _build_idob_packet

    packet = _build_idob_packet(tp)
    return dict(packet.get("idob_packet", {}))


def _legacy_truth_relation(tp: Any) -> str:
    if is_interrogative(tp):
        return "interrogative"
    if has_constraints(tp):
        return "declarative"
    return "unknown"


def _legacy_candidate_group_ids(tp: Any) -> list:
    interrogative = is_interrogative(tp)
    locative = has_locative(tp)
    if interrogative and locative:
        return [3001]
    if interrogative:
        return [2001]
    if locative:
        return [1002]
    if has_constraints(tp):
        return [1001]
    return []


def _legacy_identity_geometry(tp: Any, truth_relation: str) -> str:
    if truth_relation == "interrogative":
        return "referential_identity"
    if _legacy_candidate_group_ids(tp):
        return "structural_identity"
    return "semantic_identity"


def _legacy_semantic_core_tokens(tp: Any) -> list:
    semantic_core = []
    if has_entity_role(tp):
        semantic_core.append("entity")
    if has_locative(tp):
        semantic_core.append("locative_modifier")
    if not semantic_core and has_roles(tp):
        semantic_core.append("entity")
    return semantic_core


def _build_selected_ops(tp: Any) -> list:
    semantic_operations = []

    constraints_matched = getattr(tp, "constraints_matched", [])
    struct_roles = getattr(tp, "struct_roles", [])
    semantic_adjacent_cues = getattr(tp, "semantic_adjacent_cues", [])

    if "theme-state" in constraints_matched:
        semantic_operations.append("theme_state")

    if "state-location" in constraints_matched:
        semantic_operations.append("state_location")

    if "query-focus-predicate" in constraints_matched:
        semantic_operations.append("query_resolution")

        has_location_role = "location" in struct_roles
        has_state_role = "state" in struct_roles
        query_focus = query_focus_text(tp)

        if query_focus in ("where", "where?") or has_location_role:
            semantic_operations.append("interrogative_relation_request")
        elif query_focus in ("why", "why?") or has_state_role:
            semantic_operations.append("interrogative_property_request")
        else:
            semantic_operations.append("interrogative_identity_request")

    if "modifier_chain" in semantic_adjacent_cues or "relation" in struct_roles:
        semantic_operations.append("nested_modifier_resolution")

    if "nested_state_link" in semantic_adjacent_cues or "nested_locative_link" in semantic_adjacent_cues or (
        "state" in struct_roles and "location" in struct_roles
    ):
        semantic_operations.append("nested_state_location_resolution")

    if "agent-action" in constraints_matched:
        semantic_operations.append("agent_action")

    if "action-relation" in constraints_matched:
        semantic_operations.append("action_patient")

    if "relation-patient" in constraints_matched:
        semantic_operations.append("relation_modifier")

    if semantic_adjacent_cues:
        semantic_operations.append("modifier_resolution")

    return semantic_operations


def _build_semantic_core_dict(tp: Any, selected_ops: list) -> Dict[str, Any]:
    role_segments = getattr(tp, "role_segments", {}) or {}
    struct_segments = getattr(tp, "struct_segments", [])
    struct_roles = getattr(tp, "struct_roles", [])
    segment_tokens = getattr(tp, "segment_tokens", [])
    semantic_adjacent_cues = getattr(tp, "semantic_adjacent_cues", [])

    query_focus = " ".join(role_segments.get("query_focus", []))
    predicate = " ".join(role_segments.get("predicate", []))
    theme = " ".join(role_segments.get("theme", role_segments.get("agent", [])))
    relation_modifiers = " ".join(role_segments.get("relation", []))

    location_tokens = role_segments.get("location", [])
    has_location_tokens = bool(location_tokens)

    state_tokens = []
    if has_location_tokens:
        for seg, role, seg_tokens in zip(struct_segments, struct_roles, segment_tokens):
            if role == "state" and seg in ("CP", "ST"):
                state_tokens.extend(seg_tokens)
    else:
        for seg, role, seg_tokens in zip(struct_segments, struct_roles, segment_tokens):
            if role == "state" and seg != "CP":
                state_tokens.extend(seg_tokens)

    if not state_tokens:
        state_tokens = role_segments.get("state", [])

    return {
        "selected_ops": selected_ops,
        "query_focus": query_focus,
        "predicate": predicate,
        "theme": theme,
        "relation_modifiers": relation_modifiers,
        "complement": " ".join(location_tokens if location_tokens else state_tokens),
        "agent": theme,
        "state": " ".join(state_tokens),
        "location": " ".join(location_tokens),
        "action": " ".join(role_segments.get("action", [])),
        "patient": " ".join(role_segments.get("patient", [])),
        "modifiers": [
            cue
            for cue in semantic_adjacent_cues
            if cue not in ("copular_state_link", "locative_link", "interrogative_scope")
        ],
    }


def build_semantic_profile(tp: Any) -> Dict[str, Any]:
    selected_ops = _build_selected_ops(tp)
    return {
        "selected_ops": selected_ops,
        "semantic_core_dict": _build_semantic_core_dict(tp, selected_ops),
        "semantic_core_tokens": _legacy_semantic_core_tokens(tp),
    }


def _copular_state_apply(_: Any) -> Dict[str, Any]:
    return {"truth_relation": "declarative", "truth_relation_family_hint": "descriptive_state"}


def _locative_apply(_: Any) -> Dict[str, Any]:
    return {
        "semantic_core_tokens": ["locative_modifier"],
        "truth_relation_family_hint": "descriptive_locative",
    }


def _mixed_descriptive_apply(tp: Any) -> Dict[str, Any]:
    if has_entity_role(tp):
        return {
            "semantic_core_tokens": ["entity"],
            "truth_relation_family_hint": "descriptive_state",
        }
    return {}


def _interrogative_wh_apply(_: Any) -> Dict[str, Any]:
    return {
        "truth_relation": "interrogative",
        "truth_relation_family_hint": "interrogative_wh",
    }


def _interrogative_polar_apply(_: Any) -> Dict[str, Any]:
    return {
        "truth_relation": "interrogative",
        "truth_relation_family_hint": "interrogative_polar",
    }


def _agent_action_apply(tp: Any) -> Dict[str, Any]:
    selected_ops = _build_selected_ops(tp)
    if "agent_action" in selected_ops:
        return {"selected_ops_add": ["agent_action"]}
    return {}


def _modifier_resolution_apply(tp: Any) -> Dict[str, Any]:
    profile = build_semantic_profile(tp)
    return {
        "selected_ops": profile["selected_ops"],
        "semantic_core": profile["semantic_core_dict"],
        "semantic_core_tokens": profile["semantic_core_tokens"],
    }


def _residual_identity_apply(tp: Any) -> Dict[str, Any]:
    truth_relation = _legacy_truth_relation(tp)
    return {
        "identity_geometry": _legacy_identity_geometry(tp, truth_relation),
        "truth_relation": truth_relation,
    }


legacy_monolith = IdOBObject(
    name="legacy_monolith",
    family="residual_identity",
    priority=999,
    activate=always_active,
    apply=_legacy_apply,
)

copular_state = IdOBObject(
    name="copular_state",
    family="copular_state",
    priority=20,
    activate=lambda tp: (not is_interrogative(tp)) and has_constraints(tp),
    apply=_copular_state_apply,
)

locative = IdOBObject(
    name="locative",
    family="locative",
    priority=30,
    activate=has_locative,
    apply=_locative_apply,
)

mixed_descriptive = IdOBObject(
    name="mixed_descriptive",
    family="mixed_descriptive",
    priority=40,
    activate=has_entity_role,
    apply=_mixed_descriptive_apply,
)

interrogative_wh = IdOBObject(
    name="interrogative_wh",
    family="interrogative_wh",
    priority=10,
    activate=is_interrogative_wh,
    apply=_interrogative_wh_apply,
)

interrogative_polar = IdOBObject(
    name="interrogative_polar",
    family="interrogative_polar",
    priority=11,
    activate=is_interrogative_polar,
    apply=_interrogative_polar_apply,
)

agent_action = IdOBObject(
    name="agent_action",
    family="residual_identity",
    priority=50,
    activate=has_constraints,
    apply=_agent_action_apply,
)

modifier_resolution = IdOBObject(
    name="modifier_resolution",
    family="mixed_descriptive",
    priority=60,
    activate=has_roles,
    apply=_modifier_resolution_apply,
)

residual_identity = IdOBObject(
    name="residual_identity",
    family="residual_identity",
    priority=90,
    activate=always_active,
    apply=_residual_identity_apply,
)
