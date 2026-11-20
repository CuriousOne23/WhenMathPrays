from typing import Any, Dict

from s2m.active_space import resolve_active_space
from s2m.legitimate import legitimate
from s2m.propose import propose
from s2m.record import build_record
from s2m.write import write_meaning_relations


def _structural_relation(seed: Dict[str, Any]) -> str:
    written_relations = seed.get("written_relations", [])
    if not isinstance(written_relations, list) or not written_relations:
        return ""
    first = written_relations[0]
    if not isinstance(first, dict):
        return ""
    return str(first.get("relation", "")).strip()


def _category_result(tp: Any) -> Dict[str, Any]:
    semantic = getattr(tp, "semantic", {})
    if not isinstance(semantic, dict):
        return {}
    result = semantic.get("isc_category_result", {})
    return result if isinstance(result, dict) else {}


def apply(seed: Dict[str, Any], tp: Any = None, space_name: str = "default") -> Dict[str, Any]:
    proposals = propose(seed)
    category_result = _category_result(tp)
    category_cue = category_result.get("category_cue", [])
    if not isinstance(category_cue, list):
        category_cue = []
    cue_values = [str(value).strip().lower() for value in category_cue if str(value).strip()]
    top_category = str(category_result.get("top_category", "")).strip().lower()
    cue_active = bool(cue_values or top_category)

    active_space = resolve_active_space(space_name) if cue_active else []
    if cue_active and top_category and top_category in active_space:
        selected_space = [top_category]
    elif cue_active:
        selected_space = [major for major in active_space if major in set(cue_values)]
    else:
        selected_space = []

    proposal_trace = []
    selected_for_legitimation = []
    for proposal in proposals:
        if not isinstance(proposal, dict):
            continue
        major = str(proposal.get("major", "")).strip().lower()
        category_supported = major in set(selected_space)
        state = "category_supported" if category_supported else "candidate_unselected"
        traced = dict(proposal)
        traced["selection_state"] = state
        proposal_trace.append(traced)
        if category_supported:
            selected_for_legitimation.append(proposal)

    legitimized = legitimate(
        selected_for_legitimation,
        selected_space,
        cue_active=cue_active,
        structural_relation=_structural_relation(seed),
    )
    meaning_relations = write_meaning_relations(legitimized)
    legitimized_keys = {
        (
            str(item.get("from", "")),
            str(item.get("relation", "")),
            str(item.get("to", "")),
            str(item.get("major", "")),
        )
        for item in legitimized
        if isinstance(item, dict)
    }
    for traced in proposal_trace:
        key = (
            str(traced.get("from", "")),
            str(traced.get("relation", "")),
            str(traced.get("to", "")),
            str(traced.get("major", "")),
        )
        if key in legitimized_keys:
            traced["selection_state"] = "legitimized"
        elif traced.get("selection_state") == "category_supported":
            traced["selection_state"] = "refused"

    return build_record(
        seed,
        proposal_trace,
        meaning_relations,
        selected_space,
        category_result,
    )

