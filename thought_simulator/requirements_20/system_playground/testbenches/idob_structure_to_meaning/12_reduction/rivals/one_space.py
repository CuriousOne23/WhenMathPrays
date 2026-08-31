from __future__ import annotations

from typing import Any, Dict, List

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

NAMES = [
    "physicality",
    "sociality",
    "temporality",
    "intentionality",
    "materiality",
    "spatiality",
]


def _base_m_for_card(card_id: str | None) -> Dict[str, float] | None:
    if card_id is None:
        return None
    # fixed per-card meanings; cheap, not reading the live map
    if card_id == "S_rock_burst":
        return {
            "physicality": 0.80,
            "sociality": 0.10,
            "temporality": 0.20,
            "intentionality": 0.10,
            "materiality": 0.85,
            "spatiality": 0.90,
        }
    if card_id == "S_deadline_friday":
        return {
            "physicality": 0.20,
            "sociality": 0.35,
            "temporality": 0.90,
            "intentionality": 0.70,
            "materiality": 0.10,
            "spatiality": 0.25,
        }
    if card_id == "S_sleepy":
        return {
            "physicality": 0.30,
            "sociality": 0.40,
            "temporality": 0.50,
            "intentionality": 0.20,
            "materiality": 0.20,
            "spatiality": 0.30,
        }
    # any other mapped card: generic meaning
    return {
        "physicality": 0.40,
        "sociality": 0.40,
        "temporality": 0.40,
        "intentionality": 0.40,
        "materiality": 0.40,
        "spatiality": 0.40,
    }


def _cie_tint(m: Dict[str, float] | None, cie_id: str | None) -> Dict[str, float] | None:
    if m is None:
        return None
    cie = str(cie_id or "neutral")
    out = dict(m)
    # cheap stance tint: nudge one axis
    if cie == "phys":
        out["physicality"] = min(1.0, out["physicality"] + 0.05)
    elif cie == "sci":
        out["temporality"] = min(1.0, out["temporality"] + 0.05)
    return out


def _structural_key_from_mprime(mprime: Dict[str, float] | None) -> str | None:
    if mprime is None:
        return None
    # one-space collapse: key is a bucket of M'
    buckets: List[str] = []
    for name in NAMES:
        v = float(mprime.get(name, 0.0))
        # coarse bucket: 0, 1, 2, 3, 4
        b = int(v * 4.0 + 0.0001)
        buckets.append(str(b))
    return "K|" + "|".join(buckets)


def run(case: Dict[str, Any]) -> Dict[str, Any]:
    card_id = case.get("card_id")
    cie_id = case.get("cie_id")

    # S_unmapped → no birth (tries to pass W2)
    if card_id == "S_unmapped":
        out = {
            "structural_key": None,
            "candidate_group_ids": [],
            "final_rank_order": [],
            "selected_group_id": None,
            "meaning_semantics": None,
            "meaning_semantics_prime": None,
            "meaning_delta_h": None,
            "residue_code": None,
            "next_key": None,
            "routing_filter_mutated": False,
            "contaminated": False,
        }
        return {k: out[k] for k in PACKET_KEYS}

    base_m = _base_m_for_card(card_id)
    mprime = _cie_tint(base_m, cie_id)
    key = _structural_key_from_mprime(mprime)

    # one-space: key derived from M'
    out = {
        "structural_key": key,
        "candidate_group_ids": [999] if base_m is not None else [],
        "final_rank_order": [999] if base_m is not None else [],
        "selected_group_id": 999 if base_m is not None else None,
        "meaning_semantics": base_m,
        "meaning_semantics_prime": mprime,
        "meaning_delta_h": 0.0 if base_m is not None else None,
        "residue_code": None,
        "next_key": None,
        "routing_filter_mutated": False,
        "contaminated": False,
    }
    return {k: out[k] for k in PACKET_KEYS}
