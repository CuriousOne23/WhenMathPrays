from __future__ import annotations

from typing import Any, Dict, List


def evaluate_dependencies(items: List[Dict[str, Any]], discovered: Dict[str, Any]) -> List[Dict[str, Any]]:
    majors = set(discovered.get("majors", []))
    results: List[Dict[str, Any]] = []
    for item in items:
        resource_class = item["resource_class"]
        identity = item["identity"]
        missing: List[str] = []

        if resource_class == "dictionary_entry":
            if identity.get("major") not in majors:
                missing.append(f"major:{identity.get('major')}")
        elif resource_class == "association":
            if identity.get("major") not in majors:
                missing.append(f"major:{identity.get('major')}")
        elif resource_class == "major":
            missing = []
        elif resource_class == "seed":
            missing.append("seed_generalization_unresolved")

        results.append(
            {
                "item_id": item["item_id"],
                "resource_class": resource_class,
                "missing_dependencies": missing,
                "has_missing_dependencies": bool(missing),
            }
        )
    return results

