"""
CST-MS RuleChecker — progressive general-mode validation
Aligned with cst_ms_rules.yaml and patha_field_names TP.cst.ms lock.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


REQUIRED_COMMAND_KEYS = (
    "freeze",
    "thaw",
    "collapse_recovery",
    "create_identity_layer",
    "split",
    "merge",
)


class CSTMSRuleChecker:
    def __init__(self, tp_before: Dict[str, Any], tp_after: Dict[str, Any], rules: List[Dict[str, Any]]):
        self.tp_before = tp_before or {}
        self.tp_after = tp_after or {}
        self.rules = rules or []

    def _ms(self) -> Dict[str, Any]:
        return ((self.tp_after.get("cst") or {}).get("ms")) or {}

    def run(self) -> List[Tuple[str, str]]:
        errors: List[Tuple[str, str]] = []
        for rule in self.rules:
            rid = rule.get("id", "unknown")
            check = rule.get("check")
            msg = None

            if check == "cst_ms_envelope_exists":
                if not self._ms():
                    msg = "TP.cst.ms missing after process"

            elif check == "commands_six_keys":
                commands = self._ms().get("commands") or {}
                missing = [k for k in REQUIRED_COMMAND_KEYS if k not in commands]
                if missing:
                    msg = f"commands missing keys: {missing}"

            elif check == "window_le_10":
                window = self._ms().get("stability_window") or []
                wlen = (self._ms().get("history") or {}).get("window_len")
                if wlen != 10:
                    msg = f"history.window_len expected 10, got {wlen}"
                elif len(window) > 10:
                    msg = f"stability_window length {len(window)} exceeds 10"

            elif check == "provisional_metrics_true":
                audit = self._ms().get("audit") or {}
                if audit.get("provisional_metrics") is not True:
                    msg = "audit.provisional_metrics is not true"

            elif check == "no_forbidden_fields":
                forbidden = ["routing_filter", "geometric_state", "semantic_core"]
                for f in forbidden:
                    if f in self.tp_after and f not in self.tp_before:
                        msg = f"forbidden field written: {f}"
                        break

            elif check == "no_cob_snapshot_mutation":
                before = ((self.tp_before.get("identity") or {}).get("cob_state_snapshot"))
                after = ((self.tp_after.get("identity") or {}).get("cob_state_snapshot"))
                if before is not None and after != before:
                    msg = "identity.cob_state_snapshot mutated"

            elif check == "no_core_mutation":
                before = ((self.tp_before.get("cst") or {}).get("core"))
                after = ((self.tp_after.get("cst") or {}).get("core"))
                if before is not None and after != before:
                    msg = "TP.cst.core mutated"

            elif check == "routing_path_contains_cst_ms":
                rp = self.tp_after.get("routing_path") or []
                if "cst_ms" not in rp:
                    msg = "routing_path does not contain 'cst_ms'"

            if msg:
                errors.append((rid, msg))
        return errors
