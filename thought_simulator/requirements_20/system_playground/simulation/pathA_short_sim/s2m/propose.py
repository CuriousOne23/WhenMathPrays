from typing import Any, Dict, List

from s2m.loader import load_endpoint_associations


def _seed_endpoints(seed: Dict[str, Any]) -> List[str]:
    written_relations = seed.get("written_relations", [])
    if not isinstance(written_relations, list):
        return []

    endpoints: List[str] = []
    for relation in written_relations:
        if not isinstance(relation, dict):
            continue
        for key in ("from", "to"):
            endpoint = str(relation.get(key, "")).strip().lower()
            if endpoint in ("", "none", "null"):
                continue
            if endpoint not in endpoints:
                endpoints.append(endpoint)
    return endpoints


def propose(seed: Dict[str, Any]) -> List[Dict[str, Any]]:
    proposals: List[Dict[str, Any]] = []
    for endpoint in _seed_endpoints(seed):
        for association in load_endpoint_associations(endpoint):
            proposal: Dict[str, Any] = {
                "from": endpoint,
                "relation": association["relation"],
                "to": association["to"],
                "major": association["major"],
            }
            subcategory = str(association.get("subcategory", "")).strip()
            if subcategory:
                proposal["subcategory"] = subcategory
            proposals.append(proposal)
    return proposals

