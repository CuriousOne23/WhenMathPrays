from __future__ import annotations

from typing import Any, Dict


def copy_from_idob(packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "mcb_identity_geometry": packet["identity_geometry"],
        "mcb_truth_relation": packet["truth_relation"],
        "mcb_truth_relation_family": packet["truth_relation_family"],
        "mcb_semantic_core": packet["semantic_core"],
        "mcb_claimed_fields": packet["claimed_fields"],
        "mcb_contributors": packet["contributors"],
        "mcb_overlap_events": packet["overlap_events"],
        "mcb_registry_digest": packet["registry_digest"],
        "mcb_complete": packet["complete"],
        "mcb_tru_hint": packet["tru_hint"],
    }
