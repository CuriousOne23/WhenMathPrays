from typing import Any, Dict

from idob.object import IdOBObject


def _legacy_apply(tp: Any) -> Dict[str, Any]:
    # Lazy import avoids a module cycle with primitives_pathA_short.
    from primitives_pathA_short import _build_idob_packet

    packet = _build_idob_packet(tp)
    return dict(packet.get("idob_packet", {}))


legacy_monolith = IdOBObject(name="legacy_monolith", apply=_legacy_apply)
