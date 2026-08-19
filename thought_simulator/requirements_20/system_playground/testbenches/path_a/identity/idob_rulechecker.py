"""
IdOB Rulechecker (Version 0.1)
Aligned with idob_rules.yaml, 20.40.050 v3.0, idob_py_struc_pgm.md v0.1,
progressive_lineup_testing.md v4.2
"""

from __future__ import annotations

from typing import Any, List, Tuple


class IdOBRuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors: List[Tuple[str, str]] = []

    def _assert(self, condition: bool, rule_id: str, message: str) -> None:
        if not condition:
            self.errors.append((rule_id, message))

    def _meta(self, tp: dict) -> dict:
        return (tp or {}).get("metadata") or {}

    def _identity(self, tp: dict) -> dict:
        return self._meta(tp).get("identity") or {}

    def deterministic_output_present(self, rule):
        self._assert(self.tp_out is not None, rule["id"], "IdOB output TP is missing.")

    def identity_envelope_present(self, rule):
        ident = self._identity(self.tp_out)
        for key in ("geometry", "continuity", "pressure", "residuals", "freeze", "basin_surface"):
            self._assert(
                key in ident,
                rule["id"],
                f"metadata.identity.{key} must be present after IdOB",
            )
        residuals = ident.get("residuals") or {}
        self._assert(
            "magnitude" in residuals and "pattern" in residuals,
            rule["id"],
            "metadata.identity.residuals must have magnitude and pattern",
        )
        freeze = ident.get("freeze") or {}
        self._assert("state" in freeze, rule["id"], "metadata.identity.freeze.state must be present")
        basin = ident.get("basin_surface") or {}
        self._assert("region" in basin, rule["id"], "metadata.identity.basin_surface.region must be present")

    def no_routing_or_dcb_writes(self, rule):
        def _get(d, *keys):
            cur = d
            for k in keys:
                if not isinstance(cur, dict):
                    return None
                cur = cur.get(k)
            return cur

        # routing_filter unchanged if present
        before_rf = _get(self.tp_in, "process", "routing_filter")
        after_rf = _get(self.tp_out, "process", "routing_filter")
        if before_rf is not None:
            self._assert(
                before_rf == after_rf,
                rule["id"],
                "IdOB must not mutate process.routing_filter",
            )

        # geometric_state unchanged if present
        before_gs = _get(self.tp_in, "metadata", "geometric_state")
        after_gs = _get(self.tp_out, "metadata", "geometric_state")
        if before_gs is not None:
            self._assert(
                before_gs == after_gs,
                rule["id"],
                "IdOB must not mutate metadata.geometric_state (DCB-owned)",
            )

    def no_structural_writes(self, rule):
        in_meta = self._meta(self.tp_in)
        out_meta = self._meta(self.tp_out)
        for key in ("residue", "residue_metadata", "structural_metadata", "structural_graph"):
            if key in in_meta and in_meta.get(key) is not None:
                self._assert(
                    in_meta.get(key) == out_meta.get(key),
                    rule["id"],
                    f"metadata.{key} was modified by IdOB",
                )
        for key in ("ssg_signature", "ssg_layer_bitmap", "ssg_reason_code", "ssg_status"):
            if key in self.tp_in:
                self._assert(
                    self.tp_in.get(key) == self.tp_out.get(key),
                    rule["id"],
                    f"{key} was modified by IdOB",
                )

    def completion_flags_consistent(self, rule):
        complete = self.tp_out.get("idob_complete")
        eligible = self.tp_out.get("path_b_eligible")
        self._assert(isinstance(complete, bool), rule["id"], "idob_complete must be bool")
        self._assert(isinstance(eligible, bool), rule["id"], "path_b_eligible must be bool")
        geom = self._identity(self.tp_out).get("geometry")
        if complete:
            self._assert(
                geom == "closure",
                rule["id"],
                f"idob_complete=True requires geometry=closure, got {geom!r}",
            )
        if geom in ("alignment", "closure"):
            self._assert(
                eligible is True,
                rule["id"],
                f"geometry {geom!r} should set path_b_eligible=True",
            )

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "IdOB output missing; cannot validate progressive lineup.",
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
