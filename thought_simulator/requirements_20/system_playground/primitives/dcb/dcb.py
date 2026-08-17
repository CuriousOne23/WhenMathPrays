"""
DCB — Directional Conversation Basin (Version 1.0)
Aligned with:
  - 20.106 (v5.3) implementation-bound
  - dcb_py_struc_pgm.md
  - progressive_lineup_testing.md v4.1

Execution-flow indexer for Path-A routing loop. Writes only:
  TP.metadata.geometric_state
  TP.metadata.geometric_history[]
  TP.metadata.dcb_events[]
  TP.metadata.provenance.dcb_last_update
No semantic, structural, identity, or routing interpretation.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional

PRIMITIVE_NAME = "dcb"

PATH_A = ["STPX", "RBU", "DCB", "TR", "CTP", "ISc", "RTU", "RB", "IdOB", "MCB"]
N = len(PATH_A)

STATE_KEYS = ("position", "direction", "curvature", "step_index", "lane_id")


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


def ordinal(primitive_id: str) -> int:
    if primitive_id not in PATH_A:
        raise ValueError(
            f"current_primitive_id {primitive_id!r} not in PATH_A {PATH_A}"
        )
    return PATH_A.index(primitive_id)


class DCB:
    """
    Directional Conversation Basin.

    Usage:
        dcb = DCB(tp_input)  # cycle context from tp['_dcb_cycle_context']
        # or
        dcb = DCB(tp_input, current_primitive_id="RBU", cycle_id=0, timestamp=1000.0)
        tp_out = dcb.process()
    """

    def __init__(
        self,
        tp_input: Optional[dict] = None,
        current_primitive_id: Optional[str] = None,
        cycle_id: Optional[int] = None,
        timestamp: Optional[float] = None,
    ):
        self.tp = copy.deepcopy(tp_input) if tp_input is not None else {}
        ctx = self.tp.get("_dcb_cycle_context") or {}
        if not isinstance(ctx, dict):
            ctx = {}

        self.current_primitive_id = current_primitive_id or ctx.get("current_primitive_id")
        self.cycle_id = cycle_id if cycle_id is not None else ctx.get("cycle_id")
        self.timestamp = timestamp if timestamp is not None else ctx.get("timestamp")

    def process(self) -> dict:
        self._validate_cycle_context()
        prev = self._read_prev_geometric_state()
        new_state = self._compute_geometric_state(prev)
        self._write_geometric_state(new_state)
        event_type = self._emit_events(prev, new_state)
        self._append_history(new_state)
        self._write_provenance()
        self._append_audit(event_type)
        return self.tp

    # ------------------------------------------------------------------
    # Validation / read
    # ------------------------------------------------------------------

    def _validate_cycle_context(self) -> None:
        if not self.current_primitive_id:
            raise ValueError("DCB requires current_primitive_id from runner cycle context")
        if self.cycle_id is None:
            raise ValueError("DCB requires cycle_id from runner cycle context")
        if self.timestamp is None:
            raise ValueError("DCB requires timestamp from runner cycle context")
        ordinal(str(self.current_primitive_id))

    def _read_prev_geometric_state(self) -> Optional[dict]:
        meta = self.tp.get("metadata") or {}
        if not isinstance(meta, dict):
            return None
        prev = meta.get("geometric_state")
        if prev is None:
            return None
        if not isinstance(prev, dict):
            raise ValueError("metadata.geometric_state must be a dict when present")
        for k in STATE_KEYS:
            if k not in prev:
                raise ValueError(f"previous geometric_state missing field {k!r}")
        return {
            "position": int(prev["position"]),
            "direction": int(prev["direction"]),
            "curvature": float(prev["curvature"]),
            "step_index": int(prev["step_index"]),
            "lane_id": int(prev["lane_id"]),
        }

    # ------------------------------------------------------------------
    # Compute (pure)
    # ------------------------------------------------------------------

    def _compute_geometric_state(self, prev: Optional[dict]) -> dict:
        curr = ordinal(str(self.current_primitive_id))
        position = curr
        direction = (curr + 1) % N
        lane_id = 0

        if prev is None:
            step_index = 0
            curvature = 0.0
        else:
            step_index = int(prev["step_index"]) + 1
            expected_direction = (int(prev["position"]) + 1) % N
            curvature = 0.0 if direction == expected_direction else 1.0

        return {
            "position": position,
            "direction": direction,
            "curvature": float(curvature),
            "step_index": step_index,
            "lane_id": lane_id,
        }

    def _fields_changed(self, prev: dict, new_state: dict) -> bool:
        for k in STATE_KEYS:
            if prev[k] != new_state[k]:
                return True
        return False

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def _write_geometric_state(self, state: dict) -> None:
        meta = self.tp.setdefault("metadata", {})
        if not isinstance(meta, dict):
            self.tp["metadata"] = {}
            meta = self.tp["metadata"]
        meta["geometric_state"] = dict(state)

    def _emit_events(self, prev: Optional[dict], new_state: dict) -> str:
        meta = self.tp.setdefault("metadata", {})
        if not isinstance(meta, dict):
            self.tp["metadata"] = {}
            meta = self.tp["metadata"]
        events = meta.setdefault("dcb_events", [])
        if not isinstance(events, list):
            meta["dcb_events"] = []
            events = meta["dcb_events"]

        if prev is None:
            events.append(
                {
                    "prev_position": None,
                    "new_position": new_state["position"],
                    "prev_direction": None,
                    "new_direction": new_state["direction"],
                    "prev_curvature": None,
                    "new_curvature": new_state["curvature"],
                    "prev_step_index": None,
                    "new_step_index": new_state["step_index"],
                    "prev_lane_id": None,
                    "new_lane_id": new_state["lane_id"],
                    "cycle_id": int(self.cycle_id),
                    "timestamp": float(self.timestamp),
                    "event_type": "cycle_start",
                }
            )
            return "cycle_start"

        if self._fields_changed(prev, new_state):
            events.append(
                {
                    "prev_position": prev["position"],
                    "new_position": new_state["position"],
                    "prev_direction": prev["direction"],
                    "new_direction": new_state["direction"],
                    "prev_curvature": prev["curvature"],
                    "new_curvature": new_state["curvature"],
                    "prev_step_index": prev["step_index"],
                    "new_step_index": new_state["step_index"],
                    "prev_lane_id": prev["lane_id"],
                    "new_lane_id": new_state["lane_id"],
                    "cycle_id": int(self.cycle_id),
                    "timestamp": float(self.timestamp),
                    "event_type": "delta",
                }
            )
            return "delta"

        return "none"

    def _append_history(self, state: dict) -> None:
        meta = self.tp.setdefault("metadata", {})
        if not isinstance(meta, dict):
            self.tp["metadata"] = {}
            meta = self.tp["metadata"]
        history = meta.setdefault("geometric_history", [])
        if not isinstance(history, list):
            meta["geometric_history"] = []
            history = meta["geometric_history"]

        history.append(
            {
                "position": state["position"],
                "direction": state["direction"],
                "curvature": state["curvature"],
                "step_index": state["step_index"],
                "lane_id": state["lane_id"],
                "cycle_id": int(self.cycle_id),
                "timestamp": float(self.timestamp),
            }
        )

    def _write_provenance(self) -> None:
        meta = self.tp.setdefault("metadata", {})
        if not isinstance(meta, dict):
            self.tp["metadata"] = {}
            meta = self.tp["metadata"]
        prov = meta.setdefault("provenance", {})
        if not isinstance(prov, dict):
            meta["provenance"] = {}
            prov = meta["provenance"]
        prov["dcb_last_update"] = float(self.timestamp)

    def _append_audit(self, event_type: str) -> None:
        self.tp.setdefault("exec_trace", [])
        if not isinstance(self.tp["exec_trace"], list):
            self.tp["exec_trace"] = []
        self.tp["exec_trace"].append(
            {
                "dcb_ref": {
                    "origin": "DCB",
                    "last_update": "DCB",
                    "cycle_id": int(self.cycle_id),
                    "event_type": event_type,
                }
            }
        )


def run(tp: dict, **kwargs) -> dict:
    """Functional entrypoint matching dcb_py_struc_pgm.md."""
    return DCB(tp, **kwargs).process()
