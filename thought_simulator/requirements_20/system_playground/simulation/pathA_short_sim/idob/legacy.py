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


def _legacy_semantic_core_tokens(tp: Any) -> list:
    semantic_core = []
    if has_entity_role(tp):
        semantic_core.append("entity")
    if has_locative(tp):
        semantic_core.append("locative_modifier")
    if not semantic_core and has_roles(tp):
        semantic_core.append("entity")
    return semantic_core


def _has_coordination(tp: Any) -> bool:
    cues = getattr(tp, "semantic_adjacent_cues", []) or []
    rules = getattr(tp, "constraints_matched", []) or []
    return "coordinated_clauses" in cues or "coordination_composition_rule" in rules


def _build_selected_ops(tp: Any) -> list:
    semantic_operations = []

    constraints_matched = getattr(tp, "constraints_matched", [])
    struct_roles = getattr(tp, "struct_roles", [])
    semantic_adjacent_cues = getattr(tp, "semantic_adjacent_cues", [])

    if "theme-state" in constraints_matched:
        semantic_operations.append("theme_state")

    if "negated_state" in semantic_adjacent_cues or "negation_scope_rule" in constraints_matched:
        semantic_operations.append("negated_state")

    if _has_coordination(tp):
        semantic_operations.append("coordinated_clauses")

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
