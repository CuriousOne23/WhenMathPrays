"""
ISc Rulechecker (Version 1.0)
Aligned with isc_rules.yaml, isc_py_struc_pgm.md v2.0, progressive_lineup_testing.md v4.0
"""

from __future__ import annotations


class IScRuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors = []

    def _assert(self, condition, rule_id, message):
        if not condition:
            self.errors.append((rule_id, message))

    def _latest_record(self):
        hist = self.tp_out.get("isc_output") or []
        if isinstance(hist, list) and hist:
            return hist[-1]
        return None

    def deterministic_output_present(self, rule):
        self._assert(self.tp_out is not None, rule["id"], "ISc output is missing.")

    def no_candidate_expansion(self, rule):
        in_cs = ((self.tp_in.get("ce") or {}).get("candidate_set"))
        if not isinstance(in_cs, list):
            in_cs = []
        rec = self._latest_record() or {}
        dist = rec.get("distribution") or []
        # Empty input may yield empty distribution (defect path)
        self._assert(
            len(dist) == len(in_cs),
            rule["id"],
            f"Candidate expansion/shrink: in={len(in_cs)} out_dist={len(dist)}",
        )

    def distribution_normalized(self, rule):
        rec = self._latest_record()
        if rec is None:
            self._assert(False, rule["id"], "No isc_output record.")
            return
        dist = rec.get("distribution") or []
        if not dist:
            return  # defect path OK
        total = sum(float(d.get("normalized_score", 0.0)) for d in dist)
        self._assert(
            abs(total - 1.0) < 1e-6,
            rule["id"],
            f"Distribution sum {total} != 1.0",
        )

    def entropy_present(self, rule):
        meta = (self.tp_out.get("metadata") or {}).get("scoring_metadata") or {}
        h = meta.get("entropy")
        self._assert(
            isinstance(h, (int, float)) and h == h,  # not NaN
            rule["id"],
            f"scoring_metadata.entropy missing or non-finite: {h!r}",
        )

    def cop_flag_boolean(self, rule):
        meta = (self.tp_out.get("metadata") or {}).get("scoring_metadata") or {}
        flag = meta.get("cop_triggered")
        self._assert(
            isinstance(flag, bool),
            rule["id"],
            f"cop_triggered must be bool, got {type(flag).__name__}",
        )

    def write_envelope_present(self, rule):
        hist = self.tp_out.get("isc_output")
        self._assert(
            isinstance(hist, list) and len(hist) >= 1,
            rule["id"],
            "isc_output missing or empty",
        )
        meta = (self.tp_out.get("metadata") or {}).get("scoring_metadata")
        self._assert(
            isinstance(meta, dict),
            rule["id"],
            "metadata.scoring_metadata missing",
        )

    def upstream_ce_read_only(self, rule):
        in_cs = (self.tp_in.get("ce") or {}).get("candidate_set")
        out_cs = (self.tp_out.get("ce") or {}).get("candidate_set")
        if in_cs is None and out_cs is None:
            return
        self._assert(
            in_cs == out_cs,
            rule["id"],
            "ce.candidate_set was modified by ISc",
        )

    def candidate_order_preserved(self, rule):
        in_cs = (self.tp_in.get("ce") or {}).get("candidate_set") or []
        rec = self._latest_record() or {}
        dist = rec.get("distribution") or []
        if not in_cs or not dist:
            return
        in_ids = [c.get("candidate_id") for c in in_cs]
        out_ids = [d.get("candidate_id") for d in dist]
        self._assert(
            in_ids == out_ids,
            rule["id"],
            f"Order mismatch: in={in_ids} out={out_ids}",
        )

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "ISc output missing; cannot validate progressive lineup.",
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
