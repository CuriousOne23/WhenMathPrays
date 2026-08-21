"""
CST-Mux rulechecker for progressive dual-mode testbench.
General mode: rules are authoritative.
Testbench mode: rules are diagnostic alongside expected blocks.
"""

from __future__ import annotations

from typing import List, Tuple


def _mux(tp: dict) -> dict:
    return ((tp or {}).get("cst") or {}).get("mux") or {}


def _usp(tp: dict) -> dict:
    return _mux(tp).get("unified_stability_packet") or {}


class CSTMUXRuleChecker:
    def __init__(self, tp_before: dict, tp_after: dict, rules: list):
        self.tp_before = tp_before or {}
        self.tp_after = tp_after or {}
        self.rules = rules or []

    def run(self) -> List[Tuple[str, str]]:
        errors: List[Tuple[str, str]] = []
        for rule in self.rules:
            rid = rule.get("id", "unknown")
            fn = getattr(self, f"_check_{rid}", None)
            if fn is None:
                continue
            msg = fn()
            if msg:
                errors.append((rid, msg))
        return errors

    def _check_mux_envelope_present(self):
        if not _mux(self.tp_after):
            return "TP.cst.mux missing"
        return None

    def _check_usp_present(self):
        if not _usp(self.tp_after):
            return "unified_stability_packet missing"
        return None

    def _check_layer_index_present(self):
        if "layer_index" not in _mux(self.tp_after):
            return "layer_index missing"
        return None

    def _check_routing_path_marker(self):
        rp = self.tp_after.get("routing_path") or []
        if "cst_mux" not in rp:
            return "routing_path missing 'cst_mux'"
        return None

    def _check_no_cob_mutation(self):
        b = ((self.tp_before.get("identity") or {}).get("cob_state_snapshot"))
        a = ((self.tp_after.get("identity") or {}).get("cob_state_snapshot"))
        if b is not None and a != b:
            return "cob_state_snapshot mutated"
        return None

    def _check_no_core_mutation(self):
        b = ((self.tp_before.get("cst") or {}).get("core"))
        a = ((self.tp_after.get("cst") or {}).get("core"))
        if b is not None and a != b:
            return "TP.cst.core mutated"
        return None

    def _check_no_ms_mutation(self):
        b = ((self.tp_before.get("cst") or {}).get("ms"))
        a = ((self.tp_after.get("cst") or {}).get("ms"))
        if b is not None and a != b:
            return "TP.cst.ms mutated"
        return None

    def _check_new_context_passthrough(self):
        ms_flag = (
            (((self.tp_before.get("cst") or {}).get("ms") or {}).get("metadata") or {}).get(
                "new_context_required"
            )
        )
        if ms_flag is None:
            return None
        usp_flag = _usp(self.tp_after).get("new_context_required")
        if bool(usp_flag) != bool(ms_flag):
            return f"new_context_required mismatch: MS={ms_flag} USP={usp_flag}"
        return None
