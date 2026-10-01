from typing import Any, Dict

from idob.object import IdOBObject


def imperative_ops(tp: Any) -> list:
    cues = getattr(tp, "semantic_adjacent_cues", []) or []
    rules = getattr(tp, "constraints_matched", []) or []
    ops = []
    if "imperative_voice_clause" in cues or "imperative_voice_rule" in rules:
        ops.append("bare_command")
    if "request_imperative_clause" in cues or "request_imperative_rule" in rules:
        ops.append("polite_request")
    return ops


def _imperative_activate(tp: Any) -> bool:
    return bool(imperative_ops(tp))


def _imperative_apply(tp: Any) -> Dict[str, Any]:
    ops = imperative_ops(tp)
    if not ops:
        return {}
    return {"selected_ops": ops, "truth_relation_family_hint": "imperative"}


imperative = IdOBObject(
    name="imperative",
    family="imperative",
    priority=15,
    activate=_imperative_activate,
    apply=_imperative_apply,
)
