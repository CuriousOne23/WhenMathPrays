"""Minimal IdOB packet print helpers."""

from . import vector6


def empty_packet():
    return {
        "structural_hash": None,
        "card_id": None,
        "candidate_group_ids": [],
        "final_rank_order": [],
        "selected_group_id": None,
        "meaning_semantics": vector6.zeros(),
        "meaning_delta_h": None,
        "identity_delta": None,
        "refinement_cycles": 0,
        "resolution_status": None,
        "ready_for_ouba": False,
    }


def print_packet(packet):
    print("---- IdOB packet (min) ----")
    for key in (
        "card_id",
        "structural_hash",
        "candidate_group_ids",
        "final_rank_order",
        "selected_group_id",
        "meaning_semantics",
        "meaning_delta_h",
        "identity_delta",
        "refinement_cycles",
        "resolution_status",
        "ready_for_ouba",
    ):
        value = packet.get(key)
        if key == "meaning_semantics" and isinstance(value, dict):
            value = vector6.fmt(value)
        print(f"  {key}: {value}")
    print("---------------------------")
