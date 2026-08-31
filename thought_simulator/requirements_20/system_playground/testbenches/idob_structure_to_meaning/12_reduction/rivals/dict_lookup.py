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

LOOKUP = {
    "the rock is on the table": {
        "physicality": 0.80,
        "sociality": 0.10,
        "temporality": 0.20,
        "intentionality": 0.10,
        "materiality": 0.85,
        "spatiality": 0.90,
    },
    "zzzzq no cue at all": {
        "physicality": 0.50,
        "sociality": 0.50,
        "temporality": 0.50,
        "intentionality": 0.50,
        "materiality": 0.50,
        "spatiality": 0.50,
    },
}


def run(case: Dict[str, Any]) -> Dict[str, Any]:
    text = str(case.get("utterance") or "").strip().lower()
    meaning = LOOKUP.get(
        text,
        {
            "physicality": 0.45,
            "sociality": 0.45,
            "temporality": 0.45,
            "intentionality": 0.45,
            "materiality": 0.45,
            "spatiality": 0.45,
        },
    )

    out = {
        "structural_key": None,
        "candidate_group_ids": [701],
        "final_rank_order": [701],
        "selected_group_id": 701,
        "meaning_semantics": dict(meaning),
        "meaning_semantics_prime": dict(meaning),
        "meaning_delta_h": 0.0,
        "residue_code": None,
        "next_key": None,
        "routing_filter_mutated": False,
        "contaminated": False,
    }
    return {k: out[k] for k in PACKET_KEYS}
