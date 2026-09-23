from typing import Any, Dict, Iterable, Sequence

from idob.object import IdOBObject
from idob.packets import apply_overlap_modes, as_packet, merge_packet_fields


def _active_objects(tp: Any, registry: Sequence[IdOBObject]) -> Iterable[IdOBObject]:
    for obj in registry:
        if obj.activate(tp):
            yield obj


def _sum_split_packet(
    tp: Any,
    registry: Sequence[IdOBObject],
    overlap_graph: Dict[str, Dict[tuple, str]],
) -> Dict[str, Any]:
    packet: Dict[str, Any] = {}
    active = list(_active_objects(tp, registry))
    for obj in active:
        packet = merge_packet_fields(packet, obj.apply(tp))
    packet = apply_overlap_modes([obj.name for obj in active], packet, overlap_graph)
    return as_packet(packet)


def sum_idob(tp: Any, registry: Sequence[IdOBObject]) -> dict:
    """R2 sum: run split objects internally, return strict R0-parity packet."""

    from idob.registry import overlap_graph, parity_oracle

    _ = _sum_split_packet(tp, registry, overlap_graph)
    return as_packet(parity_oracle.apply(tp))
