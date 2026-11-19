from typing import Any, Dict, List


def write_meaning_relations(legitimized: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    relations: List[Dict[str, Any]] = []
    for relation in legitimized:
        relations.append(
            {
                "from": relation.get("from", ""),
                "relation": relation.get("relation", ""),
                "to": relation.get("to", ""),
                "major": relation.get("major", ""),
                "legitimized": True,
            }
        )
    return relations

