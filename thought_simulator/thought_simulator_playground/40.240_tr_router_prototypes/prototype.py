"""40.240_tr_router_prototypes Phase B (W3 extension).

Extends the legacy proxy to full on-TP 20.37 integration:
- Consume OB TR-input + optional DCB ephemeral events (from 40.210) when tr_needs_update=true
- Atomic TP.TR write; clear tr_needs_update on success only
- Negatives: reject when flag false; reject DCB-direct (must come via proper RB path)
- Preserve legacy proxy route() as regression subset

Proxy scenarios from 2026-06-03 are retained for regression.
New W3 scenarios exercise the on-TP flow contract.
"""

from typing import Dict, Any, List, Optional
import json
from hashlib import sha256


class ThoughtRouter:
    """
    Thought Router (TR) - Full on-TP integration per 20.37.
    Strictly deterministic.
    """

    def __init__(self):
        self.initialized = True

    # --- Legacy proxy (regression baseline, unchanged behavior) ---
    def route(self, input_message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Proxy routing (pre-W3 basin selection + ΔH%).
        Preserved exactly for regression.
        """
        if not input_message or "content" not in input_message:
            return {"route": "error", "reason": "invalid_input"}

        content = input_message["content"].strip().lower()

        if any(word in content for word in ["math", "calculate", "number"]):
            return {"route": "math_basin", "priority": "high", "delta_h": 0.15}
        elif any(word in content for word in ["think", "reason", "understand"]):
            return {"route": "thought_basin", "priority": "medium", "delta_h": 0.08}
        else:
            return {"route": "general_basin", "priority": "low", "delta_h": 0.05}

    # --- W3 on-TP implementation (new for Phase B) ---
    def process_tr_step(self, tp_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the TR step on a TP state dict (simulating on-TP structures).

        Expected tp_state (from OB + optional DCB, per 20.37):
        - tr_input: dict (pre-semantic from OB)
        - tr_needs_update: bool
        - dcb_events: optional list (ephemeral from 40.210 when enabled)
        - Other TP/MTP snapshot fields as needed for interpretation.

        Returns:
        - On success: {"status": "success", "TP.TR": {...}, "tr_needs_update": False, ...}
        - On skip/reject: {"status": "skipped" or "rejected", "reason": "..."}
        """
        if not isinstance(tp_state, dict):
            return {"status": "error", "reason": "invalid_tp_state"}

        tr_input = tp_state.get("tr_input", {})
        needs_update = bool(tp_state.get("tr_needs_update", False))
        dcb_events = tp_state.get("dcb_events", []) or []

        # Negative: reject if flag false (20.37 step 4)
        if not needs_update:
            return {
                "status": "skipped",
                "reason": "tr_needs_update_false",
                "tr_input_consumed": False,
                "dcb_events_consumed": False,
            }

        # Negative: reject DCB-direct (must come through proper path; no RB-direct consumption)
        # In this sim, if tr_input is empty but dcb_events present without OB context, treat as direct
        if not tr_input and dcb_events:
            # Pure DCB-direct attempt
            return {
                "status": "rejected",
                "reason": "dcb_direct_without_tr_input",
                "tr_input_consumed": False,
                "dcb_events_consumed": False,
            }

        # Consume TR-input (from OB) + permitted DCB events
        # Simple deterministic interpretation (extendable; no latent inference)
        interpretation = self._interpret(tr_input, dcb_events)

        # Atomic TP.TR write (simulated)
        tr_record = {
            "semantic_interpretation": interpretation,
            "source_tr_input": dict(tr_input),
            "dcb_events_used": len(dcb_events),
            "delta_h_contrib": interpretation.get("delta_h", 0.0),
            "cycle_id": tp_state.get("cycle_id", "c-unknown"),
        }

        # Write back and clear flag on success only
        tp_state["TR"] = tr_record
        tp_state["tr_needs_update"] = False

        return {
            "status": "success",
            "TP.TR": tr_record,
            "tr_needs_update": False,
            "tr_input_consumed": True,
            "dcb_events_consumed": bool(dcb_events),
        }

    def _interpret(self, tr_input: Dict[str, Any], dcb_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Minimal deterministic interpretation combining OB cues + DCB geometric hints."""
        cues = tr_input.get("cues", []) or []
        content_hint = str(tr_input.get("content_hint", "")).lower()

        # Base from TR-input (OB-derived)
        base = {}
        if any("math" in str(c).lower() or "calculate" in str(c).lower() for c in cues) or "math" in content_hint:
            base = {"route": "math_basin", "priority": "high", "delta_h": 0.15}
        elif any("think" in str(c).lower() or "reason" in str(c).lower() for c in cues) or "reason" in content_hint:
            base = {"route": "thought_basin", "priority": "medium", "delta_h": 0.08}
        else:
            base = {"route": "general_basin", "priority": "low", "delta_h": 0.05}

        # Incorporate DCB geometric overlay if present (ephemeral, non-persisted)
        dcb_contrib = 0.0
        if dcb_events:
            for ev in dcb_events:
                curv = abs(float(ev.get("curvature", 0.0)))
                dcb_contrib += min(curv * 0.05, 0.03)  # small bounded geometric hint

        base["delta_h"] = round(base.get("delta_h", 0.0) + dcb_contrib, 4)
        base["dcb_events_incorporated"] = len(dcb_events)
        base["interpretation_note"] = "combined OB TR-input + permitted DCB events"

        return base


# For harness compatibility (legacy proxy path)
def create_router() -> ThoughtRouter:
    return ThoughtRouter()
