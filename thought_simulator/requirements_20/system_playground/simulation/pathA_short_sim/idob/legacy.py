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


def _cue_or_rule(tp: Any, cue: str, rule: str) -> bool:
    cues = getattr(tp, "semantic_adjacent_cues", []) or []
    rules = getattr(tp, "constraints_matched", []) or []
    return cue in cues or rule in rules


def _has_speaker(tp: Any) -> bool:
    return _cue_or_rule(tp, "first_person_speaker", "first_person_state_rule")


def _has_passive(tp: Any) -> bool:
    return _cue_or_rule(tp, "passive_voice_clause", "passive_voice_rule")


def _has_quantifier(tp: Any) -> bool:
    return _cue_or_rule(tp, "quantified_np", "quantifier_scope_rule")


def _has_coordination(tp: Any) -> bool:
    return _cue_or_rule(tp, "coordinated_clauses", "coordination_composition_rule")


def _has_conditional(tp: Any) -> bool:
    return _cue_or_rule(tp, "conditional_clauses", "conditional_composition_rule")


def _has_fragment(tp: Any) -> bool:
    return _cue_or_rule(tp, "fragment_ellipsis", "fragment_ellipsis_rule")
