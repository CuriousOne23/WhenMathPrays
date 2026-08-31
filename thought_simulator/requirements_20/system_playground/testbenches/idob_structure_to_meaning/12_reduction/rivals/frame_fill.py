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

BASE_M = {
    "physicality": 0.55,
    "sociality": 0.25,
    "temporality": 0.40,
    "intentionality": 0.45,
    "materiality": 0.35,
    "spatiality": 0.60,
}


def run(case: Dict[str, Any]) -> Dict[str, Any]:
    card_id = case.get("card_id")
    births = card_id is not None
    candidate_group_ids = [901] if births else []
    final_rank_order = [901] if births else []
    selected_group_id = 901 if births else None
    meaning = dict(BASE_M) if births else None
    meaning_prime = dict(BASE_M) if births else None

    out = {
        "structural_key": CARD_TO_KEY.get(card_id),
        "candidate_group_ids": candidate_group_ids,
        "final_rank_order": final_rank_order,
        "selected_group_id": selected_group_id,
        "meaning_semantics": meaning,
        "meaning_semantics_prime": meaning_prime,
        "meaning_delta_h": 0.0 if births else None,
        "residue_code": None,
        "next_key": None,
        "routing_filter_mutated": False,
        "contaminated": False,
    }
    return {k: out[k] for k in PACKET_KEYS}
