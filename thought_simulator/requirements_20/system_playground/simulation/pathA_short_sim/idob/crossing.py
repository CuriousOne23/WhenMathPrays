"""tp.idob shell. Mechanical copy. Null means absent, not born."""

from typing import Any, Dict

from idob.connections import connections_from_packet


ABSENT = (
    "structural_key",
    "candidate_group_ids",
    "final_rank_order",
    "selected_group_id",
    "cie_id",
    "meaning_semantics",
    "meaning_semantics_prime",
    "meaning_delta_h",
    "ready_for_ouba",
    "path_b_eligible",
    "idob_complete",
    "routing_filter_mutated",
)


def crossing_from_packet(tp: Dict[str, Any]) -> Dict[str, Any]:
    segments_before = list(tp.get("struct_segments") or [])
    packet = tp.get("idob") or {}
    shell = {
        "utterance": tp.get("raw_text"),
        "semantic_core": packet.get("semantic_core"),
        "selected_ops": list(packet.get("selected_ops") or []),
        "structure_ids": None,
        "semantic_field_id": None,
        "semantic_role_id": None,
        "semantic_object_id": None,
        "gradient_id": None,
        "universe_id": None,
        "subfield_id": None,
        "connection_witness": connections_from_packet(tp),
    }
    for name in ABSENT:
        shell[name] = None
    if list(tp.get("struct_segments") or []) != segments_before:
        raise RuntimeError("crossing reopened the cut")
    return shell
