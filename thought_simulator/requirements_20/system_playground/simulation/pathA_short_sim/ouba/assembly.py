from __future__ import annotations


def build_ouba(mcb_packet: dict) -> dict:
    """
    Pure assembly: derive an OuBA packet from the MCB seam.
    No writes back into IdOB or MCB.
    No new semantics beyond outer boundary framing.
    """
    return {
        "ouba_identity_geometry": mcb_packet.get("mcb_identity_geometry"),
        "ouba_truth_relation": mcb_packet.get("mcb_truth_relation"),
        "ouba_truth_relation_family": mcb_packet.get("mcb_truth_relation_family"),
        "ouba_semantic_core": mcb_packet.get("mcb_semantic_core"),
        "ouba_claimed_fields": mcb_packet.get("mcb_claimed_fields"),
        "ouba_contributors": mcb_packet.get("mcb_contributors"),
        "ouba_overlap_events": mcb_packet.get("mcb_overlap_events"),
        "ouba_registry_digest": mcb_packet.get("mcb_registry_digest"),
        "ouba_complete": mcb_packet.get("mcb_complete"),
        "ouba_tru_hint": mcb_packet.get("mcb_tru_hint"),
    }
