from typing import Any, Dict, List


def write_meaning_relations(legitimized: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    relations: List[Dict[str, Any]] = []
    for relation in legitimized:
        item: Dict[str, Any] = {
            "from": relation.get("from", ""),
            "relation": relation.get("relation", ""),
            "to": relation.get("to", ""),
            "major": relation.get("major", ""),
            "legitimized": True,
        }
        subcategory = str(relation.get("subcategory", "")).strip()
        if subcategory:
            item["subcategory"] = subcategory
        relations.append(item)
    return relations

