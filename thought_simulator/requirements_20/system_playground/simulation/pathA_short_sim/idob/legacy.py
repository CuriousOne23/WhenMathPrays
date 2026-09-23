from typing import Any, Dict

from idob.object import IdOBObject
from idob.predicates import (
    always_active,
    has_constraints,
    has_entity_role,
    has_locative,
    has_roles,
    is_interrogative,
)


def _legacy_apply(tp: Any) -> Dict[str, Any]:
    # Lazy import avoids a module cycle with primitives_pathA_short.
    from primitives_pathA_short import _build_idob_packet

    packet = _build_idob_packet(tp)
    return dict(packet.get("idob_packet", {}))


def _copular_state_apply(_: Any) -> Dict[str, Any]:
    return {"truth_relation": "declarative"}


def _locative_apply(_: Any) -> Dict[str, Any]:
    return {"semantic_core": ["locative_modifier"]}


def _mixed_descriptive_apply(tp: Any) -> Dict[str, Any]:
    if has_entity_role(tp):
        return {"semantic_core": ["entity"]}
    return {}


def _interrogative_wh_apply(_: Any) -> Dict[str, Any]:
    return {
        "truth_relation": "interrogative",
        "identity_geometry": "referential_identity",
    }


def _interrogative_polar_apply(_: Any) -> Dict[str, Any]:
    return {
        "truth_relation": "interrogative",
        "identity_geometry": "referential_identity",
    }


def _agent_action_apply(_: Any) -> Dict[str, Any]:
    return {}


def _modifier_resolution_apply(tp: Any) -> Dict[str, Any]:
    if has_roles(tp) and not has_entity_role(tp):
        return {"semantic_core": ["entity"]}
    return {}


def _residual_identity_apply(tp: Any) -> Dict[str, Any]:
    if has_constraints(tp):
        return {"identity_geometry": "structural_identity"}
    return {"identity_geometry": "semantic_identity"}


legacy_monolith = IdOBObject(
    name="legacy_monolith",
    family="residual_identity",
    activate=always_active,
    apply=_legacy_apply,
)

copular_state = IdOBObject(
    name="copular_state",
    family="copular_state",
    activate=lambda tp: (not is_interrogative(tp)) and has_constraints(tp),
    apply=_copular_state_apply,
)

locative = IdOBObject(
    name="locative",
    family="locative",
    activate=has_locative,
    apply=_locative_apply,
)

mixed_descriptive = IdOBObject(
    name="mixed_descriptive",
    family="mixed_descriptive",
    activate=has_entity_role,
    apply=_mixed_descriptive_apply,
)

interrogative_wh = IdOBObject(
    name="interrogative_wh",
    family="interrogative_wh",
    activate=is_interrogative,
    apply=_interrogative_wh_apply,
)

interrogative_polar = IdOBObject(
    name="interrogative_polar",
    family="interrogative_polar",
    activate=is_interrogative,
    apply=_interrogative_polar_apply,
)

agent_action = IdOBObject(
    name="agent_action",
    family="residual_identity",
    activate=always_active,
    apply=_agent_action_apply,
)

modifier_resolution = IdOBObject(
    name="modifier_resolution",
    family="mixed_descriptive",
    activate=has_roles,
    apply=_modifier_resolution_apply,
)

residual_identity = IdOBObject(
    name="residual_identity",
    family="residual_identity",
    activate=always_active,
    apply=_residual_identity_apply,
)
