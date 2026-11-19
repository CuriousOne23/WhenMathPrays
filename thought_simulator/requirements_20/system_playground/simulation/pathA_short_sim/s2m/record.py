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


def build_record(
    seed: Dict[str, Any],
    meaning_relations: List[Dict[str, Any]],
    active_space: List[str],
) -> Dict[str, Any]:
    return {
        "meaning_relations": meaning_relations,
        "active_space": active_space,
        "story_id": _build_story_id(seed),
        "extendable": True,
    }

