"""
COB RuleChecker — progressive general-mode validation
Aligned with cob_rules.yaml and cob_py_struc_pgm.md write-boundary discipline.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


class COBRuleChecker:
    def __init__(self, tp_before: Dict[str, Any], tp_after: Dict[str, Any], rules: List[Dict[str, Any]]):
        self.tp_before = tp_before or {}
        self.tp_after = tp_after or {}
        self.rules = rules or []

    def _snapshot(self) -> Dict[str, Any]:
        identity = (self.tp_after.get("identity") or {})
        return identity.get("cob_state_snapshot") or {}

    def run(self) -> List[Tuple[str, str]]:
        errors: List[Tuple[str, str]] = []
        for rule in self.rules:
            rid = rule.get("id", "unknown")
            check = rule.get("check")
            msg = None
            if check == "object_count_le_20":
                snap = self._snapshot()
                count = snap.get("object_count", len(snap.get("objects") or []))
                if count > 20:
                    msg = f"object_count {count} exceeds bound 20"
            elif check == "cob_state_snapshot_exists":
                if not self._snapshot():
                    msg = "cob_state_snapshot missing after process"
            elif check == "lineage_module_id_cob":
                for ev in self.tp_after.get("lineage_log") or []:
                    if isinstance(ev, dict) and ev.get("event_type") in ("MERGE", "SPLIT"):
                        if ev.get("module_id") not in (None, "cob"):
                            msg = f"lineage event module_id expected cob, got {ev.get('module_id')}"
                            break
            elif check == "no_forbidden_fields":
                forbidden = ["routing_filter", "geometric_state", "semantic_core"]
                for f in forbidden:
                    if f in self.tp_after and f not in self.tp_before:
                        msg = f"forbidden field written: {f}"
                        break
            elif check == "routing_path_contains_cob":
                rp = self.tp_after.get("routing_path") or []
                if "cob" not in rp:
                    msg = "routing_path does not contain 'cob'"
            if msg:
                errors.append((rid, msg))
        return errors
