"""
CST-Core RuleChecker — progressive general-mode validation
Aligned with cst_core_rules.yaml and patha_field_names TP.cst.core lock.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


REQUIRED_SIGNAL_KEYS = (
    "freeze",
    "thaw",
    "continuity_restoration",
    "drift",
    "oscillation",
    "ambiguity",
    "collapse",
)


class CSTCoreRuleChecker:
    def __init__(self, tp_before: Dict[str, Any], tp_after: Dict[str, Any], rules: List[Dict[str, Any]]):
        self.tp_before = tp_before or {}
        self.tp_after = tp_after or {}
        self.rules = rules or []

    def _core(self) -> Dict[str, Any]:
        return ((self.tp_after.get("cst") or {}).get("core")) or {}

    def run(self) -> List[Tuple[str, str]]:
        errors: List[Tuple[str, str]] = []
        for rule in self.rules:
            rid = rule.get("id", "unknown")
            check = rule.get("check")
            msg = None

            if check == "cst_core_envelope_exists":
                if not self._core():
                    msg = "TP.cst.core missing after process"

            elif check == "signals_required_keys":
                signals = self._core().get("signals") or {}
                missing = [k for k in REQUIRED_SIGNAL_KEYS if k not in signals]
                if missing:
                    msg = f"signals missing keys: {missing}"

            elif check == "history_window_le_10":
                hist = self._core().get("history") or {}
                turns = hist.get("turns") or []
                wlen = hist.get("window_len")
                if wlen != 10:
                    msg = f"history.window_len expected 10, got {wlen}"
                elif len(turns) > 10:
                    msg = f"history.turns length {len(turns)} exceeds 10"

            elif check == "provisional_metrics_true":
                audit = self._core().get("audit") or {}
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

            elif check == "routing_path_contains_cst_core":
                rp = self.tp_after.get("routing_path") or []
                if "cst_core" not in rp:
                    msg = "routing_path does not contain 'cst_core'"

            if msg:
                errors.append((rid, msg))
        return errors
