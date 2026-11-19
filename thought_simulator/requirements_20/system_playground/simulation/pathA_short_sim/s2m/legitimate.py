from typing import Any, Dict, List


def legitimate(proposals: List[Dict[str, str]], active_space: List[str]) -> List[Dict[str, Any]]:
    active_set = set(active_space)
    legitimized: List[Dict[str, Any]] = []
    for proposal in proposals:
        major = str(proposal.get("major", "")).strip()
        if not major or major not in active_set:
            continue
        legitimized.append(
            {
                "from": str(proposal.get("from", "")),
                "relation": str(proposal.get("relation", "")),
                "to": str(proposal.get("to", "")),
                "major": major,
                "legitimized": True,
            }
        )
    return legitimized

