from typing import Any, Dict, List


def _build_written_relations(utterance: str) -> List[Dict[str, str]]:
    lowered = utterance.lower()
    if "where" in lowered and "book" in lowered and utterance.strip().endswith("?"):
        return [
            {
                "from": "query_location",
                "relation": "queries_location_of",
                "to": "book",
                "source": "floor",
            }
        ]
    if "book" in lowered and "table" in lowered and " on " in f" {lowered} ":
        return [
            {
                "from": "book",
                "relation": "is_on",
                "to": "table",
                "source": "floor",
            }
        ]
    if "sky" in lowered and "blue" in lowered:
        return [
            {
                "from": "sky",
                "relation": "is",
                "to": "blue",
                "source": "floor",
            }
        ]
    return []


def apply_seed(tp: Any, packet: Dict[str, Any]) -> Dict[str, Any]:
    """Additive seed. Does not mutate packet or tp.idob."""
    _ = packet
    utterance = getattr(tp, "raw_text", "") or ""
    written = _build_written_relations(utterance)

    nulls = [
        {"from": None, "relation": None, "to": None, "reason": "no_floor_source"},
    ]

    return {
        "utterance": utterance,
        "written_relations": written,
        "null_relations": nulls,
        "crossing_fields": {
            "structure_ids": None,
            "structural_key": None,
            "rank": None,
            "meaning_semantics": None,
            "cie_id": None,
            "meaning_delta_h": None,
        },
        "active_context_stores": [],
        "selection_cues": [],
        "seed_complete": True,
    }
