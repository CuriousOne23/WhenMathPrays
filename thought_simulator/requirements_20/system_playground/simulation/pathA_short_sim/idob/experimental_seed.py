from typing import Any, Dict, List


def apply_seed(tp: Any, packet: Dict[str, Any]) -> Dict[str, Any]:
    """Additive seed. Does not mutate packet or tp.idob."""
    _ = packet
    utterance = getattr(tp, "raw_text", "") or ""

    written: List[Dict[str, str]] = []
    lowered = utterance.lower()
    if "sky" in lowered and "blue" in lowered:
        written.append(
            {
                "from": "sky",
                "relation": "is",
                "to": "blue",
                "source": "floor",
            }
        )

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
        "seed_complete": True,
    }
