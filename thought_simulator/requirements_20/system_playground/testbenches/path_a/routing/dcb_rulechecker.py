"""
DCB Rulechecker (Version 1.0)
Aligned with dcb_rules.yaml, 20.106 v5.3, dcb_py_struc_pgm.md,
progressive_lineup_testing.md v4.1
"""

from __future__ import annotations

from typing import List, Tuple

STATE_KEYS = ("position", "direction", "curvature", "step_index", "lane_id")


class DCBRuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors: List[Tuple[str, str]] = []

    def _assert(self, condition: bool, rule_id: str, message: str) -> None:
        if not condition:
            self.errors.append((rule_id, message))

    def _meta(self, tp: dict) -> dict:
        return (tp or {}).get("metadata") or {}

    def _state(self, tp: dict):
        return self._meta(tp).get("geometric_state")

    def deterministic_output_present(self, rule):
        self._assert(self.tp_out is not None, rule["id"], "DCB output TP is missing.")

    def geometric_state_five_scalars(self, rule):
        state = self._state(self.tp_out)
        self._assert(isinstance(state, dict), rule["id"], "geometric_state must be a dict")
        if not isinstance(state, dict):
            return
        for k in STATE_KEYS:
            self._assert(k in state, rule["id"], f"geometric_state missing {k}")
        if all(k in state for k in STATE_KEYS):
            self._assert(isinstance(state["position"], int), rule["id"], "position must be int")
            self._assert(isinstance(state["direction"], int), rule["id"], "direction must be int")
            self._assert(isinstance(state["curvature"], (int, float)), rule["id"], "curvature must be float")
            self._assert(isinstance(state["step_index"], int), rule["id"], "step_index must be int")
            self._assert(isinstance(state["lane_id"], int), rule["id"], "lane_id must be int")
            self._assert(len(state) >= 5, rule["id"], "geometric_state must have five core fields")

    def lane_id_zero(self, rule):
        state = self._state(self.tp_out) or {}
        self._assert(state.get("lane_id") == 0, rule["id"], f"lane_id must be 0, got {state.get('lane_id')}")

    def one_history_append(self, rule):
        in_hist = self._meta(self.tp_in).get("geometric_history") or []
        out_hist = self._meta(self.tp_out).get("geometric_history") or []
        if not isinstance(in_hist, list):
            in_hist = []
        if not isinstance(out_hist, list):
            out_hist = []
        self._assert(
            len(out_hist) == len(in_hist) + 1,
            rule["id"],
            f"history must grow by 1 (in={len(in_hist)}, out={len(out_hist)})",
        )

    def event_policy(self, rule):
        prev = self._state(self.tp_in)
        events = self._meta(self.tp_out).get("dcb_events") or []
        if not isinstance(events, list):
            events = []
        in_events = self._meta(self.tp_in).get("dcb_events") or []
        if not isinstance(in_events, list):
            in_events = []

        new_events = events[len(in_events) :]
        if prev is None:
            self._assert(len(new_events) == 1, rule["id"], "first cycle must emit exactly one event")
            if new_events:
                self._assert(
                    new_events[0].get("event_type") == "cycle_start",
                    rule["id"],
                    f"first cycle event_type must be cycle_start, got {new_events[0].get('event_type')}",
                )
                self._assert(
                    new_events[0].get("prev_position") is None,
                    rule["id"],
                    "cycle_start prev_position must be null",
                )
        else:
            self._assert(len(new_events) >= 1, rule["id"], "subsequent cycle with state change should emit delta")
            if new_events:
                self._assert(
                    new_events[-1].get("event_type") == "delta",
                    rule["id"],
                    f"subsequent event_type must be delta, got {new_events[-1].get('event_type')}",
                )

    def binary_curvature(self, rule):
        state = self._state(self.tp_out) or {}
        c = state.get("curvature")
        self._assert(
            c in (0.0, 1.0, 0, 1),
            rule["id"],
            f"curvature must be 0.0 or 1.0, got {c}",
        )

    def only_dcb_fields_written(self, rule):
        for key in ("ssg_signature", "ssg_layer_bitmap", "ssg_reason_code", "ssg_status"):
            if key in self.tp_in:
                self._assert(
                    self.tp_in.get(key) == self.tp_out.get(key),
                    rule["id"],
                    f"{key} was modified by DCB",
                )

        in_sem = self.tp_in.get("semantic")
        out_sem = self.tp_out.get("semantic")
        if in_sem is not None:
            self._assert(in_sem == out_sem, rule["id"], "semantic was modified by DCB")

        in_res = self._meta(self.tp_in).get("residue")
        out_res = self._meta(self.tp_out).get("residue")
        if in_res is not None:
            self._assert(in_res == out_res, rule["id"], "metadata.residue was modified by DCB")

    def provenance_dcb_last_update(self, rule):
        prov = self._meta(self.tp_out).get("provenance") or {}
        self._assert(
            "dcb_last_update" in prov,
            rule["id"],
            "metadata.provenance.dcb_last_update missing",
        )

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "DCB output missing; cannot validate progressive lineup.",
        )

    def run(self):
        for rule in self.rules:
            check = rule.get("check")
            if not check:
                continue
            method = getattr(self, check, None)
            if method is None:
                self.errors.append((rule["id"], f"Unknown rule check: {check}"))
                continue
            method(rule)
        return self.errors
