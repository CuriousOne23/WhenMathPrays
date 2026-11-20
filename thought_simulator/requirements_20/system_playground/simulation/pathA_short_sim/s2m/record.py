import re
from typing import Any, Dict, List


def _build_story_id(seed: Dict[str, Any]) -> str:
    written_relations = seed.get("written_relations", [])
    if not isinstance(written_relations, list) or not written_relations:
        return "s2m-story-001"

    first = written_relations[0]
    if not isinstance(first, dict):
        return "s2m-story-001"

    left = str(first.get("from", "")).strip().lower()
    right = str(first.get("to", "")).strip().lower()
    left = re.sub(r"[^a-z0-9]+", "-", left).strip("-")
    right = re.sub(r"[^a-z0-9]+", "-", right).strip("-")
    if not left or not right:
        return "s2m-story-001"
    return f"{left}-{right}-001"


def _default_meaning(seed: Dict[str, Any]) -> Dict[str, str]:
    written_relations = seed.get("written_relations", [])
    if not isinstance(written_relations, list) or not written_relations:
        return {
            "relation": "",
            "description": "",
        }

    first = written_relations[0]
    if not isinstance(first, dict):
        return {
            "relation": "",
            "description": "",
        }

    relation = str(first.get("relation", "")).strip()
    left = str(first.get("from", "")).strip()
    right = str(first.get("to", "")).strip()
    if relation == "is":
        description = f"The entity {left} is characterized by the state/property {right}."
    elif relation == "is_on":
        description = f"The entity {left} is located on the entity {right}."
    elif relation == "queries_location_of":
        description = (
            f"A request/query for the location of the entity {right}; "
            "the requested locative continuation remains unresolved/potential."
        )
    else:
        description = f"The entity {left} stands in relation {relation} with the entity {right}."

    return {
        "from": left,
        "relation": relation,
        "to": right,
        "description": description,
    }


def build_record(
    seed: Dict[str, Any],
    candidate_interpretations: List[Dict[str, Any]],
    meaning_relations: List[Dict[str, Any]],
    active_space: List[str],
    category_result: Dict[str, Any],
) -> Dict[str, Any]:
    cue_values = category_result.get("category_cue", []) if isinstance(category_result, dict) else []
    if not isinstance(cue_values, list):
        cue_values = []
    return {
        "default_meaning": _default_meaning(seed),
        "candidate_interpretations": candidate_interpretations,
        "meaning_relations": meaning_relations,
        "active_space": active_space,
        "active_context_stores": seed.get("active_context_stores", []),
        "cue_state": {
            "category_cue": cue_values,
            "cue_active": bool(cue_values),
            "provenance": category_result.get("provenance", {}) if isinstance(category_result, dict) else {},
        },
        "category_result": category_result if isinstance(category_result, dict) else {},
        "story_id": _build_story_id(seed),
        "extendable": True,
    }

