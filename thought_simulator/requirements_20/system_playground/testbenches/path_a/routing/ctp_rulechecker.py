"""
CTP Rulechecker (Version 1.0)
Aligned with ctp_rules.yaml, 20.145 v3.0, ctp_py_struc_pgm.md,
progressive_lineup_testing.md v4.2
"""

from __future__ import annotations

from typing import List, Tuple

INVARIANT_KEYS = (
    "I_stab",
    "R_res",
    "P_cont",
    "L_depth",
    "Rt_adj",
    "delta_H",
    "E_dens",
    "C_coh",
)

HISTORY_TOP_KEYS = (
    "cycle_id",
    "timestamp",
    "invariants",
    "idob_geometry",
    "idob_roles",
    "idob_residue",
    "idob_stability",
    "rb_adjacency_class",
    "rb_displacement_scale",
    "rb_regime_hint",
    "rb_route_proposal",
)


class CTPRuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors: List[Tuple[str, str]] = []

    def _assert(self, condition: bool, rule_id: str, message: str) -> None:
        if not condition:
            self.errors.append((rule_id, message))

    def _meta(self, tp: dict) -> dict:
        return (tp or {}).get("metadata") if isinstance((tp or {}).get("metadata"), dict) else {}

    def _hist(self, tp: dict) -> list:
        h = self._meta(tp).get("cognitive_history")
        return h if isinstance(h, list) else []

    def deterministic_output_present(self, rule):
        self._assert(self.tp_out is not None, rule["id"], "CTP output TP is missing.")

    def one_history_append(self, rule):
        in_len = len(self._hist(self.tp_in))
        out_len = len(self._hist(self.tp_out))
        self._assert(
            out_len == in_len + 1,
            rule["id"],
            f"history must grow by 1 (in={in_len}, out={out_len})",
        )

    def history_entry_schema_complete(self, rule):
        hist = self._hist(self.tp_out)
        self._assert(len(hist) >= 1, rule["id"], "no cognitive_history entry to validate")
        if not hist:
            return
        entry = hist[-1]
        self._assert(isinstance(entry, dict), rule["id"], "last history entry must be a dict")
        if not isinstance(entry, dict):
            return
        for k in HISTORY_TOP_KEYS:
            self._assert(k in entry, rule["id"], f"history entry missing key {k}")
        inv = entry.get("invariants")
        self._assert(isinstance(inv, dict), rule["id"], "invariants must be a dict")
        if isinstance(inv, dict):
            for k in INVARIANT_KEYS:
                self._assert(k in inv, rule["id"], f"invariants missing key {k}")
        geom = entry.get("idob_geometry")
        self._assert(isinstance(geom, dict), rule["id"], "idob_geometry must be a dict")
        if isinstance(geom, dict):
            self._assert("neighborhood" in geom, rule["id"], "idob_geometry missing neighborhood")
            self._assert("k_id" in geom, rule["id"], "idob_geometry missing k_id")

    def missing_sources_are_null(self, rule):
        # When no foundation/idob/rb sources, corresponding values must be null
        has_f = isinstance(self.tp_in.get("_ctp_foundation"), dict) and bool(
            self.tp_in.get("_ctp_foundation")
        )
        semantic = self.tp_in.get("semantic") if isinstance(self.tp_in.get("semantic"), dict) else {}
        has_idob = isinstance(semantic.get("idob"), dict) and bool(semantic.get("idob"))
        process = self.tp_in.get("process") if isinstance(self.tp_in.get("process"), dict) else {}
        rf = process.get("routing_filter") if isinstance(process.get("routing_filter"), dict) else {}
        has_rb = bool(rf)

        hist = self._hist(self.tp_out)
        if not hist:
            return
        entry = hist[-1]
        if not isinstance(entry, dict):
            return

        if not has_f:
            inv = entry.get("invariants") or {}
            if isinstance(inv, dict):
                for k in INVARIANT_KEYS:
                    if k in inv:
                        self._assert(
                            inv.get(k) is None,
                            rule["id"],
                            f"invariants.{k} should be null when foundation absent",
                        )

        if not has_idob:
            self._assert(entry.get("idob_roles") is None, rule["id"], "idob_roles should be null")
            self._assert(entry.get("idob_residue") is None, rule["id"], "idob_residue should be null")
            self._assert(
                entry.get("idob_stability") is None, rule["id"], "idob_stability should be null"
            )

        if not has_rb:
            self._assert(
                entry.get("rb_adjacency_class") is None,
                rule["id"],
                "rb_adjacency_class should be null when routing_filter absent",
            )

    def prior_history_unchanged(self, rule):
        in_hist = self._hist(self.tp_in)
        out_hist = self._hist(self.tp_out)
        if not in_hist:
            return
        if len(out_hist) < len(in_hist):
            self._assert(False, rule["id"], "history shrank")
            return
        for i, prev in enumerate(in_hist):
            self._assert(
                out_hist[i] == prev,
                rule["id"],
                f"prior history entry {i} was modified",
            )

    def provenance_ctp_last_update(self, rule):
        ctx = self.tp_in.get("_ctp_cycle_context") if isinstance(self.tp_in.get("_ctp_cycle_context"), dict) else {}
        ts = ctx.get("timestamp")
        if ts is None:
            return
        prov = self._meta(self.tp_out).get("provenance") or {}
        self._assert(
            "ctp_last_update" in prov,
            rule["id"],
            "metadata.provenance.ctp_last_update missing",
        )
        if "ctp_last_update" in prov:
            try:
                self._assert(
                    float(prov["ctp_last_update"]) == float(ts),
                    rule["id"],
                    f"ctp_last_update expected {ts}, got {prov.get('ctp_last_update')}",
                )
            except (TypeError, ValueError):
                self._assert(False, rule["id"], "ctp_last_update not numeric")

    def only_ctp_fields_written(self, rule):
        if self.tp_in.get("TR") is not None:
            self._assert(
                self.tp_in.get("TR") == self.tp_out.get("TR"),
                rule["id"],
                "TR was modified by CTP",
            )
        if "tr_needs_update" in self.tp_in:
            self._assert(
                self.tp_in.get("tr_needs_update") == self.tp_out.get("tr_needs_update"),
                rule["id"],
                "tr_needs_update was modified by CTP",
            )

        in_sem = self.tp_in.get("semantic")
        out_sem = self.tp_out.get("semantic")
        if in_sem is not None:
            self._assert(in_sem == out_sem, rule["id"], "semantic was modified by CTP")

        in_proc = self.tp_in.get("process") if isinstance(self.tp_in.get("process"), dict) else {}
        out_proc = self.tp_out.get("process") if isinstance(self.tp_out.get("process"), dict) else {}
        if "routing_filter" in in_proc:
            self._assert(
                in_proc.get("routing_filter") == out_proc.get("routing_filter"),
                rule["id"],
                "process.routing_filter was modified by CTP",
            )

        in_meta = self._meta(self.tp_in)
        out_meta = self._meta(self.tp_out)
        for key in ("geometric_state", "geometric_history", "residue", "context"):
            if key in in_meta:
                self._assert(
                    in_meta.get(key) == out_meta.get(key),
                    rule["id"],
                    f"metadata.{key} was modified by CTP",
                )

    def succeeds_without_idob(self, rule):
        semantic = self.tp_in.get("semantic") if isinstance(self.tp_in.get("semantic"), dict) else {}
        has_idob = isinstance(semantic.get("idob"), dict) and bool(semantic.get("idob"))
        if has_idob:
            return
        self._assert(self.tp_out is not None, rule["id"], "CTP failed without IdOB")
        self._assert(len(self._hist(self.tp_out)) >= 1, rule["id"], "no history when IdOB absent")

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "CTP output missing; cannot validate progressive lineup.",
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
