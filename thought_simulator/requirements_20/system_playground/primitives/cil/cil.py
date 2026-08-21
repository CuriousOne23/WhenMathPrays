"""
CIL — Conversation Integration Layer
System Playground Version (v0.1 — identity-selection slice)

Aligned with:
- 20.33_cil_requirements.md
- system_playground/primitives/cil/cil_requirements.md
- cil_py_struc_pgm.md
- cil_testbench_schema.md (identity-selection slice)
- patha_field_names.md
- progressive_lineup_testing.md

CIL is a normalize / freeze / package layer only.
It does NOT compute new ordering scores or importance values.
It reflects COB's stabilized identity-layer snapshot into TP.cil.intake_packet.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
import copy


PRIMITIVE_NAME = "cil"


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


# ---------------------------------------------------------------------------
# Pure extract views (read-only)
# ---------------------------------------------------------------------------

def extract_cob_snapshot(tp: Dict[str, Any]) -> Dict[str, Any]:
    """Read-only COB stabilized identity-layer snapshot."""
    if not isinstance(tp, dict):
        return {}
    identity = tp.get("identity") or {}
    snap = identity.get("cob_state_snapshot")
    if isinstance(snap, dict) and snap:
        return snap
    # Alternate transfer surfaces sometimes used in fixtures
    cob = tp.get("cob") or {}
    if isinstance(cob, dict):
        alt = cob.get("cob_state_snapshot") or cob.get("snapshot")
        if isinstance(alt, dict):
            return alt
    return {}


def extract_usp(tp: Dict[str, Any]) -> Dict[str, Any]:
    """Read-only Unified Stability Packet from CST-Mux (opaque for v0.1)."""
    if not isinstance(tp, dict):
        return {}
    cst = tp.get("cst") or {}
    mux = cst.get("mux") or {}
    usp = mux.get("unified_stability_packet") or tp.get("unified_stability_packet") or {}
    return usp if isinstance(usp, dict) else {}


def extract_structural_cues(tp: Dict[str, Any]) -> Dict[str, Any]:
    process = (tp or {}).get("process") or {}
    cues = process.get("structural_cues") or {}
    return cues if isinstance(cues, dict) else {}


def extract_intake_metadata(tp: Dict[str, Any]) -> Dict[str, Any]:
    metadata = (tp or {}).get("metadata") or {}
    intake = metadata.get("intake_metadata") or {}
    return intake if isinstance(intake, dict) else {}


def extract_register_cues(tp: Dict[str, Any]) -> Dict[str, Any]:
    process = (tp or {}).get("process") or {}
    cues = process.get("register_cues") or {}
    return cues if isinstance(cues, dict) else {}


def extract_next_context(tp: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(tp, dict):
        return {}
    nxt = tp.get("next_context")
    if isinstance(nxt, dict):
        return nxt
    metadata = tp.get("metadata") or {}
    nxt = metadata.get("next_context") or metadata.get("next_context_metadata") or {}
    return nxt if isinstance(nxt, dict) else {}


def extract_importance_signals(tp: Dict[str, Any]) -> Dict[str, Any]:
    """Read-only importance signals (reflected later; not used for ranking)."""
    snap = extract_cob_snapshot(tp)
    return {
        "structural_importance": snap.get("structural_importance"),
        "constraint_importance": snap.get("constraint_importance"),
        "semantic_adjacent_importance": snap.get("semantic_adjacent_importance"),
        "identity_importance": snap.get("identity_importance"),
        "long_horizon_importance": snap.get("long_horizon_importance")
        or snap.get("importance_continuity"),
    }


# ---------------------------------------------------------------------------
# Identity selection (reflection-only)
# ---------------------------------------------------------------------------

def _object_id(obj: Dict[str, Any]) -> Optional[str]:
    return obj.get("id") or obj.get("layer_id") or obj.get("stable_id")


def _object_ordering_score(obj: Dict[str, Any]) -> float:
    """
    Reflect COB-provided ordering_score when present.
    When absent, fall back to COB ordering_metrics tuple as a stable key
    without inventing a named alternative score field in the packet.
    """
    if "ordering_score" in obj and obj["ordering_score"] is not None:
        try:
            return float(obj["ordering_score"])
        except (TypeError, ValueError):
            pass
    om = obj.get("ordering_metrics") or {}
    # Deterministic composite used only for ranking; never written as a computed score
    # unless COB already supplied ordering_score.
    try:
        r = float(om.get("recency", 0) or 0)
        f = float(om.get("frequency", 0) or 0)
        d = float(om.get("density", 0) or 0)
        return r * 1_000_000 + f * 1_000 + d
    except (TypeError, ValueError):
        return 0.0


def _rank_objects(objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deterministic descending rank by COB ordering_score (or metrics fallback)."""
    decorated: List[Tuple[float, str, Dict[str, Any]]] = []
    for obj in objects:
        if not isinstance(obj, dict):
            continue
        oid = _object_id(obj)
        if oid is None:
            continue
        score = _object_ordering_score(obj)
        decorated.append((score, str(oid), obj))
    # Higher score first; ties broken by stable id for determinism
    decorated.sort(key=lambda t: (-t[0], t[1]))
    return [t[2] for t in decorated]


def build_identity_selection_block(
    cob_snapshot: Dict[str, Any],
    structural_cues: Optional[Dict[str, Any]] = None,
    intake_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Reflect-only IdentitySelectionBlock per cil_testbench_schema.md §4.

    CIL SHALL NOT compute new scores or expose alternative ranking fields.
    primary/secondary are selected by COB ordering_score (deterministic ties by id).
    """
    objects = cob_snapshot.get("objects") or []
    if not isinstance(objects, list):
        objects = []

    ranked = _rank_objects(objects)

    primary = ranked[0] if len(ranked) >= 1 else None
    secondary = ranked[1] if len(ranked) >= 2 else None

    primary_id = _object_id(primary) if primary else None
    secondary_id = _object_id(secondary) if secondary else None

    # ordering_score in packet is COB-provided for primary when present;
    # otherwise omit inventing a score — use the reflected metrics-derived key only
    # if COB left ordering_score absent (still a reflection of ranking inputs).
    if primary is not None and "ordering_score" in primary and primary["ordering_score"] is not None:
        try:
            ordering_score = float(primary["ordering_score"])
        except (TypeError, ValueError):
            ordering_score = _object_ordering_score(primary)
    elif primary is not None:
        ordering_score = _object_ordering_score(primary)
    else:
        ordering_score = 0.0

    om_src = (primary or {}).get("ordering_metrics") or {}
    ordering_metrics = {
        "recency": int(om_src.get("recency", 0) or 0),
        "frequency": int(om_src.get("frequency", 0) or 0),
        "density": float(om_src.get("density", 0) or 0),
        "conversation_count": int(
            cob_snapshot.get("conversation_access_count")
            or cob_snapshot.get("conversation_count")
            or om_src.get("conversation_count")
            or 0
        ),
        "chronological_ordering_vector": list(
            cob_snapshot.get("conversation_access_order")
            or cob_snapshot.get("chronological_ordering_vector")
            or om_src.get("chronological_ordering_vector")
            or []
        ),
        "sliding_window_frequency": list(
            _normalize_sliding_window(
                cob_snapshot.get("conversation_frequency_last_10")
                or cob_snapshot.get("sliding_window_frequency")
                or om_src.get("sliding_window_frequency")
                or []
            )
        ),
    }

    return {
        "primary_identity": primary_id,
        "secondary_identity": secondary_id,
        "ordering_score": ordering_score,
        "ordering_metrics": ordering_metrics,
    }


def _normalize_sliding_window(value: Any) -> List[int]:
    if isinstance(value, list):
        out = []
        for v in value:
            try:
                out.append(int(v))
            except (TypeError, ValueError):
                out.append(0)
        return out
    if isinstance(value, dict):
        # Preserve insertion order of dict values as list[int]
        out = []
        for v in value.values():
            try:
                out.append(int(v))
            except (TypeError, ValueError):
                out.append(0)
        return out
    return []


# ---------------------------------------------------------------------------
# Write-boundary guard
# ---------------------------------------------------------------------------

FORBIDDEN_TOP_LEVEL = {
    "semantic",
    "semantic_core",
    "routing_filter",
    "geometric_state",
    "geometric_history",
    "dcb_events",
}


def write_boundary_guard(tp_before: Dict[str, Any], tp_after: Dict[str, Any]) -> List[str]:
    """
    Assert CIL only writes TP.cil.intake_packet (and optional routing_path / lineage_log markers).
    Returns list of violation messages (empty = ok).
    """
    violations: List[str] = []
    before = tp_before or {}
    after = tp_after or {}

    for key in FORBIDDEN_TOP_LEVEL:
        if key in after and after.get(key) != before.get(key):
            violations.append(f"forbidden field mutated: {key}")

    # cob_state_snapshot must not be mutated by CIL
    before_snap = ((before.get("identity") or {}).get("cob_state_snapshot"))
    after_snap = ((after.get("identity") or {}).get("cob_state_snapshot"))
    if before_snap != after_snap:
        violations.append("CIL mutated identity.cob_state_snapshot")

    # USP must not be mutated
    before_usp = extract_usp(before)
    after_usp = extract_usp(after)
    if before_usp != after_usp:
        violations.append("CIL mutated USP / unified_stability_packet")

    return violations


# ---------------------------------------------------------------------------
# Packet assembly (identity-selection slice)
# ---------------------------------------------------------------------------

def assemble_intake_packet(
    identity_selection: Dict[str, Any],
    audit: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Assemble v0.1 packet containing identity_selection (+ optional audit shell)."""
    packet: Dict[str, Any] = {
        "identity_selection": identity_selection,
    }
    if audit is not None:
        packet["audit"] = audit
    return packet


def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    """
    Main entry. Returns updated TP carrying TP.cil.intake_packet.

    v0.1 scope: identity_selection block only (cil_testbench_schema.md).
    mode is injected by run.py / testbench ("testbench" | "general").
    """
    tp_before = copy.deepcopy(tp) if tp is not None else {}
    tp_after = copy.deepcopy(tp_before)

    cob_snapshot = extract_cob_snapshot(tp_after)
    structural_cues = extract_structural_cues(tp_after)
    intake_metadata = extract_intake_metadata(tp_after)

    identity_selection = build_identity_selection_block(
        cob_snapshot,
        structural_cues=structural_cues,
        intake_metadata=intake_metadata,
    )

    # v0.1: audit shell present but empty for this slice (schema: audit not required yet)
    audit: Dict[str, Any] = {
        "slice": "identity_selection",
        "drops": [],
        "truncations": [],
    }

    packet = assemble_intake_packet(identity_selection, audit=audit)

    cil_block = tp_after.setdefault("cil", {})
    if not isinstance(cil_block, dict):
        cil_block = {}
        tp_after["cil"] = cil_block
    cil_block["intake_packet"] = packet

    # Provenance markers (allowed)
    routing_path = tp_after.setdefault("routing_path", [])
    if isinstance(routing_path, list) and "cil" not in routing_path:
        routing_path.append("cil")

    violations = write_boundary_guard(tp_before, tp_after)
    if violations:
        # Attach diagnostics; hard-fail is the testbench's responsibility in testbench mode
        cil_block.setdefault("intake_packet", {}).setdefault("audit", {})["write_boundary_violations"] = (
            violations
        )
        if mode == "testbench":
            raise RuntimeError("CIL write-boundary violations: " + "; ".join(violations))

    return tp_after


# ---------------------------------------------------------------------------
# Legacy compatibility shim (older testbench called CIL().run(...))
# ---------------------------------------------------------------------------

class CIL:
    """Thin wrapper preserving older class-style entry for transitional fixtures."""

    def __init__(self):
        self.last_packet: Optional[Dict[str, Any]] = None

    def process(self, tp: dict, mode: str = "general", **kwargs) -> dict:
        return process(tp, mode=mode, **kwargs)

    def run(self, cob_objects, core_signals, ms_signals, turn_index):
        """Legacy path: synthesize a minimal TP from cob_objects and process."""
        objects = []
        for obj in cob_objects or []:
            if hasattr(obj, "__dict__"):
                objects.append(
                    {
                        "id": getattr(obj, "id", None),
                        "referent_map": getattr(obj, "referent_map", {}),
                        "anchors": getattr(obj, "anchors", []),
                        "lineage": getattr(obj, "lineage", {}),
                        "ambiguity": getattr(obj, "ambiguity", {}),
                        "stability_metrics": getattr(obj, "stability_metrics", {}),
                        "ordering_metrics": getattr(obj, "ordering_metrics", {}),
                        "ordering_score": getattr(obj, "ordering_score", None),
                    }
                )
            elif isinstance(obj, dict):
                objects.append(obj)
        tp = {
            "turn_index": turn_index,
            "identity": {"cob_state_snapshot": {"objects": objects}},
            "signals": {**(core_signals or {}), **(ms_signals or {})},
            "routing_path": [],
        }
        out = process(tp, mode="testbench")
        self.last_packet = ((out.get("cil") or {}).get("intake_packet") or {})
        return self.last_packet
