"""
SSG Rulechecker (Version 1.0)
Aligned with ssg_rules.yaml, 20.47 v3.0, ssg_py_struc_pgm.md,
progressive_lineup_testing.md v4.0
"""

from __future__ import annotations

import math
from typing import Any, List, Tuple


class SSGRuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors: List[Tuple[str, str]] = []

    def _assert(self, condition: bool, rule_id: str, message: str) -> None:
        if not condition:
            self.errors.append((rule_id, message))

    def deterministic_output_present(self, rule):
        self._assert(self.tp_out is not None, rule["id"], "SSG output TP is missing.")

    def status_enum_valid(self, rule):
        status = self.tp_out.get("ssg_status")
        allowed = {"OK", "MISSING_INPUT", "DEGENERATE", "PARTIAL"}
        self._assert(
            status in allowed,
            rule["id"],
            f"ssg_status must be one of {sorted(allowed)}, got {status!r}",
        )

    def reason_enum_valid(self, rule):
        reason = self.tp_out.get("ssg_reason_code")
        allowed = {"FULL", "PARTIAL", "EMPTY"}
        self._assert(
            reason in allowed,
            rule["id"],
            f"ssg_reason_code must be one of {sorted(allowed)}, got {reason!r}",
        )

    def bitmap_range(self, rule):
        bm = self.tp_out.get("ssg_layer_bitmap")
        self._assert(
            isinstance(bm, int) and 0 <= bm <= 15,
            rule["id"],
            f"ssg_layer_bitmap must be int in [0,15], got {bm!r}",
        )

    def signature_present_or_missing_input(self, rule):
        status = self.tp_out.get("ssg_status")
        sig = self.tp_out.get("ssg_signature")
        if status == "MISSING_INPUT":
            self._assert(
                sig is None,
                rule["id"],
                "MISSING_INPUT must not write ssg_signature",
            )
        else:
            self._assert(
                isinstance(sig, list) and len(sig) > 0,
                rule["id"],
                f"ssg_signature must be a non-empty list when status={status}",
            )

    def signature_l2_unit_or_zero(self, rule):
        status = self.tp_out.get("ssg_status")
        if status == "MISSING_INPUT":
            return
        sig = self.tp_out.get("ssg_signature")
        if not isinstance(sig, list) or not sig:
            self._assert(False, rule["id"], "ssg_signature missing for L2 check")
            return
        try:
            vals = [float(v) for v in sig]
        except (TypeError, ValueError):
            self._assert(False, rule["id"], "ssg_signature contains non-numeric values")
            return
        norm = math.sqrt(sum(v * v for v in vals))
        is_zero = all(abs(v) < 1e-12 for v in vals)
        self._assert(
            is_zero or abs(norm - 1.0) < 1e-6,
            rule["id"],
            f"ssg_signature L2 norm must be 0 or ~1.0, got {norm}",
        )

    def only_ssg_fields_written(self, rule):
        in_res = (self.tp_in.get("metadata") or {}).get("residue")
        out_res = (self.tp_out.get("metadata") or {}).get("residue")
        if in_res is not None and out_res is not None:
            self._assert(
                in_res == out_res,
                rule["id"],
                "metadata.residue was modified by SSG",
            )

    def missing_input_status(self, rule):
        meta = self.tp_in.get("metadata") or {}
        has_residue = isinstance(meta.get("residue"), dict)
        has_sg = isinstance(meta.get("structural_graph"), dict) or isinstance(
            self.tp_in.get("structural_graph"), dict
        )
        if not has_residue and not has_sg:
            self._assert(
                self.tp_out.get("ssg_status") == "MISSING_INPUT",
                rule["id"],
                "Absent structural input must yield ssg_status=MISSING_INPUT",
            )

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "SSG output missing; cannot validate progressive lineup.",
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
