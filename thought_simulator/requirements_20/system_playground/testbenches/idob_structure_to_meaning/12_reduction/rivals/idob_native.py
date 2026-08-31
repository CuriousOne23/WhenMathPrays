from __future__ import annotations

from typing import Any, Dict, Tuple

from thought_simulator.requirements_20.system_playground.primitives.idob import idob as live_idob

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


def _subset_from_packet(pkt: Dict[str, Any]) -> Dict[str, Any]:
    out = {
        "structural_key": pkt.get("structural_key"),
        "candidate_group_ids": list(pkt.get("candidate_group_ids") or []),
        "final_rank_order": list(pkt.get("final_rank_order") or []),
        "selected_group_id": pkt.get("selected_group_id"),
        "meaning_semantics": pkt.get("meaning_semantics"),
        "meaning_semantics_prime": pkt.get("meaning_semantics_prime"),
        "meaning_delta_h": pkt.get("meaning_delta_h"),
        "residue_code": pkt.get("residue_code"),
        "next_key": None,
        "routing_filter_mutated": bool(pkt.get("routing_filter_mutated", False)),
        "contaminated": False,
    }
    return {k: out[k] for k in PACKET_KEYS}


def run_with_context(case: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    call = case.get("call") or "run_hop"
    kwargs = {
        "card_id": case.get("card_id"),
        "utterance": case.get("utterance"),
        "packs_loaded": case.get("packs_loaded"),
        "cie_id": case.get("cie_id", "neutral"),
        "prior_M": case.get("prior_M"),
    }

    context: Dict[str, Any] = {
        "routing_filter_before": case.get("routing_filter"),
        "routing_filter_after": None,
        "first_meaning_cycle": None,
    }

    if call == "process":
        tp_in: Dict[str, Any] = {}
        if case.get("routing_filter") is not None:
            tp_in["process"] = {"routing_filter": case.get("routing_filter")}
        tp_out = live_idob.process(tp_in, mode="general", **kwargs)
        pkt = (tp_out.get("idob") or {}) if isinstance(tp_out, dict) else {}
        if isinstance(tp_out, dict):
            context["routing_filter_after"] = (
                (tp_out.get("process") or {}).get("routing_filter")
            )
    else:
        pkt = live_idob.run_hop(**kwargs)

    context["first_meaning_cycle"] = pkt.get("first_meaning_cycle")
    return _subset_from_packet(pkt), context


def run(case: Dict[str, Any]) -> Dict[str, Any]:
    packet, _context = run_with_context(case)
    return packet
