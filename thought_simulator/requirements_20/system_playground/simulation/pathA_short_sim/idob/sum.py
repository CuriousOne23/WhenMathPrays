from typing import Any, Dict, Iterable, List, Sequence

from idob.object import IdOBObject
from idob.packets import (
    apply_overlap_modes,
    as_packet,
    claimed_fields_from_contributions,
    merge_packet_fields,
)


def _active_objects(tp: Any, registry: Sequence[IdOBObject]) -> Iterable[IdOBObject]:
    for obj in registry:
        if obj.activate(tp):
            yield obj


def _truth_relation_family(truth_relation: str, active_names: List[str]) -> str:
    if truth_relation == "interrogative":
        if "interrogative_wh" in active_names:
            return "interrogative_wh"
        if "interrogative_polar" in active_names:
            return "interrogative_polar"
        return "unknown"

    if truth_relation == "declarative":
        has_locative = "locative" in active_names
        has_descriptive = "mixed_descriptive" in active_names or "copular_state" in active_names
        if has_locative and has_descriptive:
            return "descriptive_mixed"
        if has_locative:
            return "descriptive_locative"
        if has_descriptive:
            return "descriptive_state"

    return "unknown"


def _meaning_delta(legacy_packet: Dict[str, Any], split_state: Dict[str, Any]) -> Dict[str, Any]:
    delta: Dict[str, Any] = {}

    if legacy_packet.get("truth_relation") != split_state.get("truth_relation"):
        delta["truth_relation"] = {
            "legacy": legacy_packet.get("truth_relation"),
            "split": split_state.get("truth_relation"),
        }

    if legacy_packet.get("identity_geometry") != split_state.get("identity_geometry"):
        delta["identity_geometry"] = {
            "legacy": legacy_packet.get("identity_geometry"),
            "split": split_state.get("identity_geometry"),
        }

    legacy_core = legacy_packet.get("semantic_core", [])
    split_core_tokens = split_state.get("semantic_core_tokens", [])
    if legacy_core != split_core_tokens:
        delta["semantic_core_tokens"] = {
            "legacy": legacy_core,
            "split": split_core_tokens,
        }

    return delta


def _sum_split_packet(
    tp: Any,
    registry: Sequence[IdOBObject],
    overlap_graph: Dict[str, Dict[tuple, str]],
) -> Dict[str, Any]:
    packet: Dict[str, Any] = {}
    active = list(_active_objects(tp, registry))
    contributions: List[Dict[str, Any]] = []

    for obj in active:
        fragment = obj.apply(tp)
        packet = merge_packet_fields(packet, fragment)
        contributions.append(
            {
                "name": obj.name,
                "family": obj.family,
                "priority": obj.priority,
                "fragment": fragment,
            }
        )

    active_names = [obj.name for obj in active]
    packet, overlap_events = apply_overlap_modes(active_names, packet, overlap_graph)

    selected_ops = packet.get("selected_ops", [])
    if not isinstance(selected_ops, list):
        selected_ops = []

    semantic_core = packet.get("semantic_core", {})
    if not isinstance(semantic_core, dict):
        semantic_core = {}
    semantic_core = dict(semantic_core)
    semantic_core["selected_ops"] = selected_ops

    truth_relation = str(packet.get("truth_relation", "unknown"))
    tru_hint = (
        (getattr(tp, "routing_metadata", {}) or {}).get("tru_hint")
        or getattr(tp, "truth_relation", "unknown")
        or "unknown"
    )
    if tru_hint in ("declarative", "interrogative", "unknown"):
        truth_relation = str(tru_hint)

    truth_relation_family = _truth_relation_family(truth_relation, active_names)

    identity_geometry = str(packet.get("identity_geometry", "semantic_identity"))
    if truth_relation == "interrogative":
        identity_geometry = "referential_identity"

    from idob.registry import evaluate_psc_after_apply, registry_digest
    from idob.registry import parity_oracle

    legacy_packet = as_packet(parity_oracle.apply(tp))

    split_state = {
        "identity_geometry": identity_geometry,
        "truth_relation": truth_relation,
        "semantic_core_tokens": packet.get("semantic_core_tokens", []),
    }

    meaning_delta = _meaning_delta(legacy_packet, split_state)

    ordered_registry = sorted(registry, key=lambda obj: (obj.priority, obj.name))
    inactive_objects = [obj.name for obj in ordered_registry if obj.name not in set(active_names)]

    idob_packet = {
        "identity_geometry": identity_geometry,
        "truth_relation": truth_relation,
        "truth_relation_family": truth_relation_family,
        "semantic_core": semantic_core,
        "selected_ops": selected_ops,
        "claimed_fields": claimed_fields_from_contributions(contributions),
        "contributors": active_names,
        "contributions": contributions,
        "activation_set": active_names,
        "inactive_objects": inactive_objects,
        "residual_activated": "residual_identity" in active_names,
        "overlap_events": overlap_events,
        "meaning_delta": meaning_delta,
        "psc_violations": [],
        "registry_digest": registry_digest,
        "complete": True,
        "tru_hint": str(tru_hint),
    }

    # R4b PSC runs after apply and reports only; no value mutation.
    idob_packet["psc_violations"] = evaluate_psc_after_apply(tp, contributions, idob_packet)

    return as_packet(idob_packet)


def sum_idob(tp: Any, registry: Sequence[IdOBObject]) -> dict:
    """R3 sum: split objects are the real writer and emit the full IdOB packet."""

    from idob.registry import overlap_graph

    return _sum_split_packet(tp, registry, overlap_graph)
