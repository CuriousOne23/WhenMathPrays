"""First IdOB mapping rung.

Consumes a finished packet. Does not reopen structure.
Does not compute M, the envelope, or delta-h.
Does not import the structure-to-meaning bench.
"""

from typing import Any, Dict


def map_packet(tp: Dict[str, Any]) -> Dict[str, Any]:
    segments_before = list(tp.get("struct_segments") or [])
    packet = tp.get("idob") if isinstance(tp.get("idob"), dict) else {}
    core = packet.get("semantic_core") if isinstance(packet.get("semantic_core"), dict) else {}
    ops = list(packet.get("selected_ops") or [])
    complete = bool(packet.get("complete"))
    bound = complete and (bool(ops) or any(str(v).strip() for v in core.values() if not isinstance(v, list)))
    # A packet with only empty strings and no ops is not a mapped claim.
    if ops:
        bound = True
    if not packet:
        bound = False
    meaning = {
        "status": "mapped" if bound else "unbound",
        "source": "idob_packet",
        "truth_relation": packet.get("truth_relation", ""),
        "selected_ops": ops,
        "semantic_core": core,
        "activation_set": list(packet.get("activation_set") or []),
        "structure_reopened": False,
        "instruments_not_computed": ["M", "envelope", "delta_h"],
    }
    if list(tp.get("struct_segments") or []) != segments_before:
        meaning["structure_reopened"] = True
        meaning["status"] = "illegal"
    return meaning
