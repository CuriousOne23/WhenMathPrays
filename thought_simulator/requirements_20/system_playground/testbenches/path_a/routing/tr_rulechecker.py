"""
TR Rulechecker (Version 1.0)
Aligned with tr_rules.yaml, 20.37 v3.0, tr_py_struc_pgm.md,
progressive_lineup_testing.md v4.2
"""

from __future__ import annotations

from typing import List, Tuple

REQUIRED_TR_KEYS = (
    "stance",
    "intent",
    "affect",
    "epistemic_shading",
    "tension",
    "politeness",
    "commitment",
    "reservation",
    "logical_structure",
    "epistemic_delta_h",
    "lineage_additions",
    "routing_fields",
)

ROUTING_FIELDS_KEYS = (
    "semantic_drift",
    "identity_drift",
    "commitment_instability",
    "freeze_conflict",
    "topology_instability",
    "curvature_level",
    "stance_instability",
    "shading_instability",
    "tension_instability",
    "lineage_instability",
    "adjacency_valence",
    "continuity_state",
    "invariant_delta_h",
    "routing_severity",
)

LINEAGE_BOUND_K = 3


class TRRuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors: List[Tuple[str, str]] = []

    def _assert(self, condition: bool, rule_id: str, message: str) -> None:
        if not condition:
            self.errors.append((rule_id, message))

    def deterministic_output_present(self, rule):
        self._assert(self.tp_out is not None, rule["id"], "TR output TP is missing.")

    def tr_block_present(self, rule):
        if not bool(self.tp_in.get("tr_needs_update")):
            return  # no-op path; block need not be rewritten
        tr = self.tp_out.get("TR")
        self._assert(isinstance(tr, dict), rule["id"], "TP.TR must be a dict after gated run")

    def tr_required_fields_present(self, rule):
        if not bool(self.tp_in.get("tr_needs_update")):
            return
        tr = self.tp_out.get("TR") or {}
        for k in REQUIRED_TR_KEYS:
            self._assert(k in tr, rule["id"], f"TP.TR missing required field {k}")

    def routing_fields_complete(self, rule):
        if not bool(self.tp_in.get("tr_needs_update")):
            return
        tr = self.tp_out.get("TR") or {}
        rf = tr.get("routing_fields")
        self._assert(isinstance(rf, dict), rule["id"], "routing_fields must be a dict")
        if not isinstance(rf, dict):
            return
        for k in ROUTING_FIELDS_KEYS:
            self._assert(k in rf, rule["id"], f"routing_fields missing key {k}")

    def dirty_flag_cleared_when_ran(self, rule):
        if not bool(self.tp_in.get("tr_needs_update")):
            return
        self._assert(
            self.tp_out.get("tr_needs_update") is False,
            rule["id"],
            "tr_needs_update must be False after successful gated TR run",
        )

    def noop_when_clean(self, rule):
        if bool(self.tp_in.get("tr_needs_update")):
            return
        self._assert(
            self.tp_in.get("TR") == self.tp_out.get("TR"),
            rule["id"],
            "TR must be unchanged when tr_needs_update is false",
        )
        self._assert(
            self.tp_out.get("tr_needs_update") is False,
            rule["id"],
            "tr_needs_update must remain false on no-op",
        )

    def idob_dcb_rb_untouched(self, rule):
        # semantic / idob view
        if self.tp_in.get("semantic") is not None:
            self._assert(
                self.tp_in.get("semantic") == self.tp_out.get("semantic"),
                rule["id"],
                "semantic was modified by TR",
            )
        # DCB ownership
        in_meta = self.tp_in.get("metadata") if isinstance(self.tp_in.get("metadata"), dict) else {}
        out_meta = self.tp_out.get("metadata") if isinstance(self.tp_out.get("metadata"), dict) else {}
        for key in ("geometric_state", "geometric_history", "residue"):
            if key in in_meta:
                self._assert(
                    in_meta.get(key) == out_meta.get(key),
                    rule["id"],
                    f"metadata.{key} was modified by TR",
                )
        # RB filter
        in_proc = self.tp_in.get("process") if isinstance(self.tp_in.get("process"), dict) else {}
        out_proc = self.tp_out.get("process") if isinstance(self.tp_out.get("process"), dict) else {}
        if "routing_filter" in in_proc:
            self._assert(
                in_proc.get("routing_filter") == out_proc.get("routing_filter"),
                rule["id"],
                "process.routing_filter was modified by TR",
            )

    def omission_defaults_when_minimal(self, rule):
        if not bool(self.tp_in.get("tr_needs_update")):
            return
        # Only apply when no STPX and no diagnostics
        has_stpx = isinstance(self.tp_in.get("STPX"), dict) and bool(self.tp_in.get("STPX"))
        diag = self.tp_in.get("_tr_diagnostics") if isinstance(self.tp_in.get("_tr_diagnostics"), dict) else {}
        has_diag = bool(diag.get("enable_diagnostics"))
        gs = (self.tp_in.get("metadata") or {}).get("geometric_state") if isinstance(self.tp_in.get("metadata"), dict) else None
        has_curv = isinstance(gs, dict) and gs.get("curvature") not in (None, 0, 0.0)
        if has_stpx or has_diag or has_curv:
            return
        tr = self.tp_out.get("TR") or {}
        self._assert(tr.get("stance") == "neutral", rule["id"], "minimal stance should be neutral")
        self._assert(tr.get("intent") == "inform", rule["id"], "minimal intent should be inform")
        self._assert(tr.get("affect") == "neutral", rule["id"], "minimal affect should be neutral")
        self._assert(tr.get("tension") == "low", rule["id"], "minimal tension should be low")

    def lineage_bounded(self, rule):
        if not bool(self.tp_in.get("tr_needs_update")):
            return
        tr = self.tp_out.get("TR") or {}
        la = tr.get("lineage_additions") or []
        if not isinstance(la, list):
            self._assert(False, rule["id"], "lineage_additions must be a list")
            return
        self._assert(
            len(la) <= LINEAGE_BOUND_K,
            rule["id"],
            f"lineage_additions length {len(la)} exceeds bound {LINEAGE_BOUND_K}",
        )

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "TR output missing; cannot validate progressive lineup.",
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
