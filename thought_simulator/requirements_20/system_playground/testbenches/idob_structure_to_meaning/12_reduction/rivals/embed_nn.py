from __future__ import annotations

from typing import Any, Dict

PACKET_KEYS = [
    "structural_key",
    "candidate_group_ids",
    "final_rank_order",
    "selected_group_id",
    "meaning_semantics",
    "meaning_semantics_prime",
    "meaning_delta_h",
    "residue_code",
    "next_key",
    "routing_filter_mutated",
    "contaminated",
]

CARD_TO_KEY = {
    "S_rock_burst": "SK|1|10|100|1000|10000|100000",
    "S_deadline_friday": "SK|2|20|200|2000|20000|200000",
    "S_sleepy": "SK|3|30|300|3000|30000|300000",
    "S_unmapped": "SK|9|90|900|9000|90000|900000",
}

PROTOTYPES = {
    "rock": {
        "group": 811,
        "vec": {
            "physicality": 0.85,
            "sociality": 0.10,
            "temporality": 0.25,
            "intentionality": 0.15,
            "materiality": 0.80,
            "spatiality": 0.75,
        },
    },
    "deadline": {
        "group": 812,
        "vec": {
            "physicality": 0.20,
            "sociality": 0.35,
            "temporality": 0.90,
            "intentionality": 0.70,
            "materiality": 0.10,
            "spatiality": 0.25,
        },
    },
    "default": {
        "group": 899,
        "vec": {
            "physicality": 0.40,
            "sociality": 0.40,
            "temporality": 0.40,
            "intentionality": 0.40,
            "materiality": 0.40,
            "spatiality": 0.40,
        },
    },
}


def _nearest_label(case: Dict[str, Any]) -> str:
    text = str(case.get("utterance") or case.get("card_id") or "").lower()
    if "rock" in text or "burst" in text:
        return "rock"
    if "deadline" in text or "friday" in text:
        return "deadline"
    return "default"


def run(case: Dict[str, Any]) -> Dict[str, Any]:
    label = _nearest_label(case)
    proto = PROTOTYPES[label]

    out = {
        "structural_key": CARD_TO_KEY.get(case.get("card_id")),
        "candidate_group_ids": [proto["group"]],
        "final_rank_order": [proto["group"]],
        "selected_group_id": proto["group"],
        "meaning_semantics": dict(proto["vec"]),
        "meaning_semantics_prime": dict(proto["vec"]),
        "meaning_delta_h": 0.0,
        "residue_code": None,
        "next_key": None,
        "routing_filter_mutated": False,
        "contaminated": False,
    }
    return {k: out[k] for k in PACKET_KEYS}
