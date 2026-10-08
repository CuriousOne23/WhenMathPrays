"""First IdOB mapping rung.

Consumes a finished packet. Does not reopen structure.
Does not compute M, the envelope, or delta-h.
Does not import the structure-to-meaning bench.

A mood with an empty core is not a mapped claim. The current sum
still activates the same cards for an unknown string as for
"The sky is blue." This rung does not repair that.
"""

from typing import Any, Dict


def _core_has_claim(core: Dict[str, Any]) -> bool:
    for value in core.values():
        if isinstance(value, list) and value:
            return True
        if isinstance(value, str) and value.strip():
            return True
    return False


def map_packet(tp: Dict[str, Any]) -> Dict[str, Any]:
    segments_before = list(tp.get("struct_segments") or [])
    packet = tp.get("idob") if isinstance(tp.get("idob"), dict) else {}
    core = packet.get("semantic_core") if isinstance(packet.get("semantic_core"), dict) else {}
    ops = [op for op in list(packet.get("selected_ops") or []) if op != "modifier_resolution"]
    claim = bool(ops) or _core_has_claim(core)
    meaning = {
        "status": "mapped" if claim else "claim_empty",
        "source": "idob_packet",
        "truth_relation": packet.get("truth_relation", ""),
        "selected_ops": ops,
        "semantic_core": core,
        "activation_set": list(packet.get("activation_set") or []),
        "structure_reopened": list(tp.get("struct_segments") or []) != segments_before,
        "instruments_not_computed": ["M", "envelope", "delta_h"],
    }
    if meaning["structure_reopened"]:
        meaning["status"] = "illegal"
    return meaning
