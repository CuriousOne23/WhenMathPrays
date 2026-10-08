"""S2M connection record. Packet in. Cut not reopened. No likelihood."""

from pathlib import Path
from typing import Any, Dict, List

import yaml

from idob.mapping import map_packet


RELATIONS_PATH = Path(__file__).resolve().parents[1] / "support/s2m/relations.yaml"


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _relations() -> List[str]:
    data = yaml.safe_load(RELATIONS_PATH.read_text(encoding="utf-8"))
    return list(data.get("relations") or [])


def connections_from_packet(tp: Dict[str, Any]) -> Dict[str, Any]:
    segments_before = list(tp.get("struct_segments") or [])
    mapped = map_packet(tp)
    core = mapped.get("semantic_core") or {}
    ops = list(mapped.get("selected_ops") or [])
    relations = _relations()
    connections = []
    holes = []
    theme = _clean(core.get("theme"))
    for relation in relations:
        value = _clean(core.get(relation))
        if not value:
            continue
        right = theme if relation != "theme" and theme else "utterance"
        connections.append({"left": value, "relation": relation, "right": right, "status": "supported"})
    if "reporting" in ops and _clean(core.get("speaker")):
        connections.append({"left": _clean(core.get("speaker")), "relation": "reporting", "right": theme or "utterance", "status": "supported"})
    elif "reporting" in ops:
        holes.append({"left": "", "relation": "speaker", "right": theme or "utterance", "status": "missing"})
    copula = _clean(core.get("copula"))
    if copula and not _clean(core.get("state")) and not _clean(core.get("location")):
        holes.append({"left": "", "relation": "state", "right": theme or "utterance", "status": "missing"})
    if not connections:
        holes.append({"left": "", "relation": "neighborhood", "right": "", "status": "missing"})
    if list(tp.get("struct_segments") or []) != segments_before:
        holes.append({"left": "", "relation": "cut", "right": "", "status": "missing"})
    notices = ["underspecified"] if len(connections) >= 2 else []
    return {"utterance": str(tp.get("raw_text") or ""), "connections": connections, "holes": holes, "notices": notices}
