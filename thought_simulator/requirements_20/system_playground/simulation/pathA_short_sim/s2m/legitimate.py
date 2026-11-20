from typing import Any, Dict, List


def legitimate(
    proposals: List[Dict[str, Any]],
    active_space: List[str],
    cue_active: bool,
) -> List[Dict[str, Any]]:
    if not cue_active:
        return []

    active_set = set(active_space)
    legitimized: List[Dict[str, Any]] = []
    for proposal in proposals:
        major = str(proposal.get("major", "")).strip()
        if not major or major not in active_set:
            continue
        relation: Dict[str, Any] = {
            "from": str(proposal.get("from", "")),
            "relation": str(proposal.get("relation", "")),
            "to": str(proposal.get("to", "")),
            "major": major,
            "legitimized": True,
        }
        subcategory = str(proposal.get("subcategory", "")).strip()
        if subcategory:
            relation["subcategory"] = subcategory
        legitimized.append(relation)
    return legitimized

