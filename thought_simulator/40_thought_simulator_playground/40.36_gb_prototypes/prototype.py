"""
40.36_gb_prototypes / prototype.py

Deterministic Global Basin (GB) prototype.

Constraints (from software_description.md):
- Non-mutating: does NOT change TP/MTP meaning-construction state.
- Reads only lane-local TP snapshots + MPs (no OB/RB/TB/IB/InB/OuB internal state).
- Applies supervisory actions only at deterministic safe boundaries.
- Operates within a bounded TCU envelope with deterministic fallback.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class GBConfig:
    """Deterministic configuration for GB behavior."""
    tcu_min: int = 1
    tcu_typ: int = 3
    tcu_max: int = 5
    # Future: drift thresholds, oscillation windows, IB population limits, etc.


@dataclass
class GBDecision:
    """Deterministic supervisory decision object."""
    supervisory_action: str
    action_rationale: str
    request_class: str
    applied_bounds: Dict[str, Any]
    execution_diagnostics: Dict[str, Any]
    supervisory_log_entry: Dict[str, Any]
    gb_reference: str


class GlobalBasinPrototype:
    """
    Deterministic GB prototype.

    Public contract:
    - process_event(event: dict) -> GBDecision
    - No mutation of TP/MTP meaning-construction state.
    - Deterministic for identical (event, config) tuples.
    """

    def __init__(self, config: Optional[GBConfig] = None) -> None:
        self.config = config or GBConfig()

    # ---------- Public API ----------

    def process_event(self, event: Dict[str, Any]) -> GBDecision:
        """
        Deterministically process a supervisory event.

        Expected event fields (JSON-compatible, see software_description.md):
        - event_type
        - sequence
        - safe_boundary
        - tp_lane_state
        - mp_state
        - request_class
        - ib_metadata / ob_metadata / cop_metadata / external_command (optional)

        This method:
        - classifies the request
        - enforces TCU envelope (stubbed)
        - selects a deterministic supervisory action
        - emits a deterministic GBDecision object
        """
        event_type = event.get("event_type", "unknown")
        sequence = event.get("sequence", 0)
        safe_boundary = bool(event.get("safe_boundary", False))
        request_class = event.get("request_class", "unknown")

        # Deterministic classification (stubbed but structured)
        classified_request_class = self._classify_request(event_type, request_class)

        # TCU envelope enforcement (stubbed)
        tcu_usage, tcu_fallback = self._enforce_tcu_envelope(event)

        # Deterministic action selection (stubbed)
        supervisory_action, rationale = self._decide_action(
            event_type=event_type,
            safe_boundary=safe_boundary,
            request_class=classified_request_class,
            tcu_fallback=tcu_fallback,
        )

        gb_ref = self._make_gb_reference(event_type, sequence)

        log_entry = self._build_log_entry(
            event=event,
            supervisory_action=supervisory_action,
            rationale=rationale,
            gb_reference=gb_ref,
            tcu_usage=tcu_usage,
            tcu_fallback=tcu_fallback,
        )

        applied_bounds = {
            "tcu_min": self.config.tcu_min,
            "tcu_typ": self.config.tcu_typ,
            "tcu_max": self.config.tcu_max,
        }

        execution_diagnostics = {
            "tcu_usage": tcu_usage,
            "tcu_fallback": tcu_fallback,
        }

        return GBDecision(
            supervisory_action=supervisory_action,
            action_rationale=rationale,
            request_class=classified_request_class,
            applied_bounds=applied_bounds,
            execution_diagnostics=execution_diagnostics,
            supervisory_log_entry=log_entry,
            gb_reference=gb_ref,
        )

    # ---------- Internal deterministic helpers ----------

    def _classify_request(self, event_type: str, request_class: str) -> str:
        """
        Deterministic mapping from (event_type, request_class) -> canonical request_class.
        No side effects.
        """
        # Simple deterministic mapping stub; extend as needed.
        if request_class != "unknown":
            return request_class

        mapping = {
            "inquiry_request": "global_inquiry",
            "ib_update": "ib_evolution",
            "ib_merge": "ib_population",
            "ib_split": "ib_population",
            "ib_promotion": "ib_promotion",
            "ob_decomposition": "ob_lifecycle",
            "cop_proposal": "cop_gating",
            "external_command": "external_supervisory",
        }
        return mapping.get(event_type, "unspecified")

    def _enforce_tcu_envelope(self, event: Dict[str, Any]) -> Tuple[int, bool]:
        """
        Deterministic TCU envelope enforcement.

        Returns:
        - tcu_usage: deterministic integer
        - tcu_fallback: bool indicating whether fallback/degradation was triggered
        """
        # For now, use a deterministic, trivial function of sequence.
        seq = int(event.get("sequence", 0))
        # Keep usage within [tcu_min, tcu_max] deterministically.
        span = max(1, self.config.tcu_max - self.config.tcu_min)
        tcu_usage = self.config.tcu_min + (seq % (span + 1))

        tcu_fallback = tcu_usage > self.config.tcu_typ
        return tcu_usage, tcu_fallback

    def _decide_action(
        self,
        event_type: str,
        safe_boundary: bool,
        request_class: str,
        tcu_fallback: bool,
    ) -> Tuple[str, str]:
        """
        Deterministic supervisory action selection.

        - Never mutates TP/MTP.
        - Applies actions only if safe_boundary is True.
        """
        if not safe_boundary:
            return "None", "Unsafe boundary: supervisory action deferred."

        # Simple deterministic policy stub.
        if tcu_fallback:
            return "SafeMode", "TCU envelope exceeded; entering SafeMode under deterministic fallback policy."

        if event_type == "inquiry_request":
            return "Approve", "IB-Creation-Request approved under deterministic inquiry policy."
        if event_type == "ib_promotion":
            return "Approve", "IB promotion approved under deterministic stability criteria."
        if event_type == "ob_decomposition":
            return "Reshape", "OB decomposition request reshapes conversation topology under policy."
        if event_type == "cop_proposal":
            return "Approve", "COP proposal accepted as advisory; no direct state mutation."

        # Default conservative behavior.
        return "None", f"No supervisory action required for request_class={request_class}."

    def _make_gb_reference(self, event_type: str, sequence: int) -> str:
        """
        Deterministic GB reference ID.
        """
        return f"GBREF-{event_type}-{sequence:08d}"

    def _build_log_entry(
        self,
        event: Dict[str, Any],
        supervisory_action: str,
        rationale: str,
        gb_reference: str,
        tcu_usage: int,
        tcu_fallback: bool,
    ) -> Dict[str, Any]:
        """
        Deterministic append-only log entry structure.
        """
        return {
            "gb_reference": gb_reference,
            "event_type": event.get("event_type", "unknown"),
            "sequence": event.get("sequence", 0),
            "request_class": event.get("request_class", "unknown"),
            "supervisory_action": supervisory_action,
            "action_rationale": rationale,
            "safe_boundary": bool(event.get("safe_boundary", False)),
            "tcu_usage": tcu_usage,
            "tcu_fallback": tcu_fallback,
            # Overflow/degradation fields can be wired to 20.30 §8.3 later.
            "overflow_flag": tcu_fallback,
            "overflow_type": "tcu_overrun" if tcu_fallback else "none",
        }
