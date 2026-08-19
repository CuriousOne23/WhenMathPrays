"""
MCB Rulechecker (Version 0.1)
Aligned with mcb_rules.yaml, 20.40.055 v2.0, mcb_py_struc_pgm.md v0.1,
progressive_lineup_testing.md v4.2
"""

from __future__ import annotations

from typing import Any, List, Tuple


class MCBRuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors: List[Tuple[str, str]] = []

    def _assert(self, condition: bool, rule_id: str, message: str) -> None:
        if not condition:
            self.errors.append((rule_id, message))

    def _get(self, d, *keys):
        cur = d
        for k in keys:
            if not isinstance(cur, dict):
                return None
            cur = cur.get(k)
        return cur

    def deterministic_output_present(self, rule):
        self._assert(self.tp_out is not None, rule["id"], "MCB output TP is missing.")

    def next_context_present(self, rule):
        nc = self.tp_out.get("next_context")
        self._assert(isinstance(nc, dict), rule["id"], "TP.next_context must be a dict")
        if not isinstance(nc, dict):
            return
        required = (
            "topic",
            "stance",
            "intent",
            "register",
            "politeness",
            "epistemic_shading",
            "continuity",
            "direction",
            "coherence",
            "shift_required",
            "importance",
        )
        for key in required:
            self._assert(
                key in nc,
                rule["id"],
                f"TP.next_context.{key} must be present after MCB",
            )

    def no_forbidden_writes(self, rule):
        # routing_filter unchanged if present
        before_rf = self._get(self.tp_in, "process", "routing_filter")
        after_rf = self._get(self.tp_out, "process", "routing_filter")
        if before_rf is not None:
            self._assert(
                before_rf == after_rf,
                rule["id"],
                "MCB must not mutate process.routing_filter",
            )

        # geometric_state unchanged if present
        before_gs = self._get(self.tp_in, "metadata", "geometric_state")
        after_gs = self._get(self.tp_out, "metadata", "geometric_state")
        if before_gs is not None:
            self._assert(
                before_gs == after_gs,
                rule["id"],
                "MCB must not mutate metadata.geometric_state (DCB-owned)",
            )

        # current-turn clarifying block unchanged if present
        before_clar = self._get(self.tp_in, "metadata", "clarifying") or self._get(
            self.tp_in, "metadata", "clarifying_metadata"
        )
        after_clar = self._get(self.tp_out, "metadata", "clarifying") or self._get(
            self.tp_out, "metadata", "clarifying_metadata"
        )
        if before_clar is not None:
            self._assert(
                before_clar == after_clar,
                rule["id"],
                "MCB must not mutate current-turn clarifying fields",
            )

        # diagnostic markers from primitive itself
        diag = self.tp_out.get("_mcb_diagnostics") or {}
        self._assert(
            not diag.get("routing_filter_mutated"),
            rule["id"],
            "MCB diagnostic reports routing_filter_mutated",
        )
        self._assert(
            not diag.get("geometric_state_mutated"),
            rule["id"],
            "MCB diagnostic reports geometric_state_mutated",
        )
        self._assert(
            not diag.get("current_turn_clarifying_mutated"),
            rule["id"],
            "MCB diagnostic reports current_turn_clarifying_mutated",
        )

    def tpu_mcb_update_shape(self, rule):
        tpu = self.tp_out.get("tpu") or {}
        update = tpu.get("mcb_update")
        self._assert(isinstance(update, dict), rule["id"], "tpu.mcb_update must be present")
        if not isinstance(update, dict):
            return
        required = (
            "mcb_delta_h",
            "mcb_semantics",
            "meaning_semantics",
            "next_context",
            "mcb_context_coherence",
            "mcb_context_shift_required",
            "mcb_complete",
            "mcb_next_ob_candidates",
        )
        for key in required:
            self._assert(
                key in update,
                rule["id"],
                f"tpu.mcb_update.{key} must be present (HLR-030)",
            )

        # Semantic mirrors
        semantic = self.tp_out.get("semantic") or {}
        if "mcb_delta_h" in update:
            self._assert(
                isinstance(update["mcb_delta_h"], (int, float)),
                rule["id"],
                "mcb_delta_h must be numeric",
            )
        self._assert(
            isinstance(update.get("mcb_complete"), bool),
            rule["id"],
            "mcb_complete must be bool",
        )

    def completion_flags_consistent(self, rule):
        complete = self.tp_out.get("mcb_complete")
        candidates = self.tp_out.get("mcb_next_ob_candidates")
        self._assert(isinstance(complete, bool), rule["id"], "mcb_complete must be bool")
        self._assert(
            isinstance(candidates, list),
            rule["id"],
            "mcb_next_ob_candidates must be a list",
        )
        if complete is True:
            self._assert(
                candidates == [] or candidates is None,
                rule["id"],
                "mcb_complete=True should have empty mcb_next_ob_candidates",
            )
        # Mirror consistency with TPU payload
        tpu_complete = self._get(self.tp_out, "tpu", "mcb_update", "mcb_complete")
        if tpu_complete is not None:
            self._assert(
                tpu_complete == complete,
                rule["id"],
                "tpu.mcb_update.mcb_complete must match TP.mcb_complete",
            )

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "MCB output missing; cannot validate progressive lineup.",
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
