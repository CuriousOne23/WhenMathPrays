"""
RB Rulechecker (Version 1.0)
Aligned with rb_rules.yaml, 20.50 v3.0, rb_py_struc_pgm.md,
progressive_lineup_testing.md v4.2
"""

from __future__ import annotations

from typing import List, Tuple


class RBRuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors: List[Tuple[str, str]] = []

    def _assert(self, condition: bool, rule_id: str, message: str) -> None:
        if not condition:
            self.errors.append((rule_id, message))

    def _rf(self, tp):
        process = (tp or {}).get("process") or {}
        if not isinstance(process, dict):
            return {}
        rf = process.get("routing_filter") or {}
        return rf if isinstance(rf, dict) else {}

    def deterministic_output_present(self, rule):
        self._assert(self.tp_out is not None, rule["id"], "RB output TP is missing.")

    def routing_filter_present(self, rule):
        process = (self.tp_out or {}).get("process") or {}
        self._assert(
            isinstance(process, dict) and "routing_filter" in process,
            rule["id"],
            "process.routing_filter missing",
        )

    def canonical_ob_ordering(self, rule):
        ids = self._rf(self.tp_out).get("selected_ob_ids") or []
        if not isinstance(ids, list):
            self._assert(False, rule["id"], "selected_ob_ids must be a list")
            return
        self._assert(ids == sorted(ids), rule["id"], f"selected_ob_ids not sorted: {ids}")

    def tr_fields_unchanged(self, rule):
        self._assert(
            self.tp_in.get("TR") == self.tp_out.get("TR"),
            rule["id"],
            "TR was modified by RB",
        )
        self._assert(
            self.tp_in.get("tr_needs_update") == self.tp_out.get("tr_needs_update"),
            rule["id"],
            "tr_needs_update was modified by RB",
        )

    def no_foreign_core_obs(self, rule):
        rm = ((self.tp_in.get("process") or {}).get("routing_metadata") or {})
        core_id = rm.get("core_id")
        if core_id is None:
            return
        candidates = {str(c.get("ob_id")): c for c in (rm.get("candidate_obs") or []) if isinstance(c, dict)}
        for oid in self._rf(self.tp_out).get("selected_ob_ids") or []:
            ob = candidates.get(str(oid))
            if ob is None:
                continue
            self._assert(
                ob.get("core_id") == core_id,
                rule["id"],
                f"selected {oid} has foreign core {ob.get('core_id')}",
            )

    def idob_dcb_semantic_untouched(self, rule):
        if self.tp_in.get("semantic") is not None:
            self._assert(
                self.tp_in.get("semantic") == self.tp_out.get("semantic"),
                rule["id"],
                "semantic was modified by RB",
            )
        in_meta = self.tp_in.get("metadata") or {}
        out_meta = self.tp_out.get("metadata") or {}
        if not isinstance(in_meta, dict):
            in_meta = {}
        if not isinstance(out_meta, dict):
            out_meta = {}
        if "residue" in in_meta:
            self._assert(
                in_meta.get("residue") == out_meta.get("residue"),
                rule["id"],
                "metadata.residue was modified by RB",
            )
        if "geometric_state" in in_meta:
            self._assert(
                in_meta.get("geometric_state") == out_meta.get("geometric_state"),
                rule["id"],
                "metadata.geometric_state was modified by RB",
            )

    def red_fields_consistent(self, rule):
        adj = self._rf(self.tp_out).get("adjacency_class")
        if adj is None:
            return
        self._assert(
            adj in ("local", "non_local"),
            rule["id"],
            f"adjacency_class invalid: {adj}",
        )

    def tr_gate_rationale_present(self, rule):
        rationales = self._rf(self.tp_out).get("transition_rationale") or []
        need = bool(self.tp_in.get("tr_needs_update", False))
        token = "tr_gate:true" if need else "tr_gate:false"
        self._assert(
            token in rationales,
            rule["id"],
            f"expected rationale token {token}, got {rationales}",
        )

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None and self._rf(self.tp_out) is not None,
            rule["id"],
            "RB output missing for progressive lineup",
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
