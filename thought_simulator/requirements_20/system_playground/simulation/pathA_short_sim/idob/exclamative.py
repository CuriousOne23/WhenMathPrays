from typing import Any, Dict

from idob.object import IdOBObject


def exclamative_ops(tp: Any) -> list:
    cues = getattr(tp, "semantic_adjacent_cues", []) or []
    rules = getattr(tp, "constraints_matched", []) or []
    if "exclamative_force_clause" in cues or "exclamative_force_rule" in rules:
        return ["exclamative_force"]
    return []


def _exclamative_activate(tp: Any) -> bool:
    return bool(exclamative_ops(tp))


def _exclamative_apply(tp: Any) -> Dict[str, Any]:
    ops = exclamative_ops(tp)
    if not ops:
        return {}
    return {"selected_ops": ops, "truth_relation_family_hint": "exclamative"}


exclamative = IdOBObject(
    name="exclamative",
    family="residual_identity",
    priority=16,
    activate=_exclamative_activate,
    apply=_exclamative_apply,
)
