"""
CIL RuleChecker — progressive general-mode validation
Aligned with cil_rules.yaml, cil_py_struc_pgm.md, and cil_testbench_schema.md.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


class CILRuleChecker:
    def __init__(self, tp_before: Dict[str, Any], tp_after: Dict[str, Any], rules: List[Dict[str, Any]]):
        self.tp_before = tp_before or {}
        self.tp_after = tp_after or {}
        self.rules = rules or []

    def _packet(self) -> Dict[str, Any]:
        cil = self.tp_after.get("cil") or {}
        return cil.get("intake_packet") or {}

    def _identity_selection(self) -> Dict[str, Any]:
        return self._packet().get("identity_selection") or {}

    def run(self) -> List[Tuple[str, str]]:
        errors: List[Tuple[str, str]] = []
        for rule in self.rules:
            rid = rule.get("id", "unknown")
            check = rule.get("check")
            msg = None

            if check == "intake_packet_exists":
                if not self._packet():
                    msg = "TP.cil.intake_packet missing after process"

            elif check == "identity_selection_exists":
                if not self._identity_selection():
                    msg = "identity_selection missing under intake_packet"

            elif check == "identity_selection_required_fields":
                block = self._identity_selection()
                required = [
                    "primary_identity",
                    "secondary_identity",
                    "ordering_score",
                    "ordering_metrics",
                ]
                missing = [k for k in required if k not in block]
                if missing:
                    msg = f"identity_selection missing fields: {missing}"
                else:
                    om = block.get("ordering_metrics") or {}
                    om_required = [
                        "recency",
                        "frequency",
                        "density",
                        "conversation_count",
                        "chronological_ordering_vector",
                        "sliding_window_frequency",
                    ]
                    om_missing = [k for k in om_required if k not in om]
                    if om_missing:
                        msg = f"ordering_metrics missing fields: {om_missing}"

            elif check == "no_forbidden_fields":
                forbidden = ["routing_filter", "geometric_state", "semantic_core"]
                for f in forbidden:
                    if f in self.tp_after and f not in self.tp_before:
                        msg = f"forbidden field written: {f}"
                        break

            elif check == "cob_snapshot_unchanged":
                before = ((self.tp_before.get("identity") or {}).get("cob_state_snapshot"))
                after = ((self.tp_after.get("identity") or {}).get("cob_state_snapshot"))
                if before != after:
                    msg = "identity.cob_state_snapshot was mutated by CIL"

            elif check == "routing_path_contains_cil":
                rp = self.tp_after.get("routing_path") or []
                if "cil" not in rp:
                    msg = "routing_path does not contain 'cil'"

            if msg:
                errors.append((rid, msg))
        return errors
