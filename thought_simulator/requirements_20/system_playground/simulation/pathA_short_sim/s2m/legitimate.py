from typing import Any, Dict, List


LICENSED_EXTENSIONS: Dict[str, List[tuple[str, str, str]]] = {
    "is": [
        ("sky", "affords", "openness"),
        ("blue", "evokes", "cold"),
        ("blue", "denotes", "color"),
    ],
    "is_on": [
        ("table", "provides", "support"),
        ("book", "is", "object"),
    ],
    "queries_location_of": [],
}


def legitimate(
    proposals: List[Dict[str, Any]],
    active_space: List[str],
    cue_active: bool,
    structural_relation: str,
) -> List[Dict[str, Any]]:
    if not cue_active:
        return []

    active_set = set(active_space)
    licensed = set(LICENSED_EXTENSIONS.get(structural_relation, []))
    legitimized: List[Dict[str, Any]] = []
    for proposal in proposals:
        major = str(proposal.get("major", "")).strip()
        if not major or major not in active_set:
            continue
        from_value = str(proposal.get("from", "")).strip()
        relation_value = str(proposal.get("relation", "")).strip()
        to_value = str(proposal.get("to", "")).strip()
        if licensed and (from_value, relation_value, to_value) not in licensed:
            continue
        relation: Dict[str, Any] = {
            "from": from_value,
            "relation": relation_value,
            "to": to_value,
            "major": major,
            "legitimized": True,
        }
        subcategory = str(proposal.get("subcategory", "")).strip()
        if subcategory:
            relation["subcategory"] = subcategory
        legitimized.append(relation)
    return legitimized

