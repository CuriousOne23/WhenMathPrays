"""
RBU Rulechecker (Version 1.0)
Aligned with rbu_rules.yaml, 20.51 v4.0, rbu_py_struc_pgm.md,
progressive_lineup_testing.md v4.1
"""

from __future__ import annotations

from typing import Any, List, Tuple


class RBURuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors: List[Tuple[str, str]] = []

    def _assert(self, condition: bool, rule_id: str, message: str) -> None:
        if not condition:
            self.errors.append((rule_id, message))

    def _semantic(self, tp: dict) -> dict:
        return (tp or {}).get("semantic") or {}

    def _meta(self, tp: dict) -> dict:
        return (tp or {}).get("metadata") or {}

    def deterministic_output_present(self, rule):
        self._assert(self.tp_out is not None, rule["id"], "RBU output TP is missing.")

    def meaning_fields_present(self, rule):
        sem = self._semantic(self.tp_out)
        meta = self._meta(self.tp_out)
        for key in ("identity", "stance", "register", "tone", "tags"):
            self._assert(
                key in sem,
                rule["id"],
                f"semantic.{key} must be present after RBU commit",
            )
        self._assert(
            "lineage_markers" in meta,
            rule["id"],
            "metadata.lineage_markers must be present after RBU commit",
        )
        if "tags" in sem:
            self._assert(
                isinstance(sem.get("tags"), list),
                rule["id"],
                "semantic.tags must be a list",
            )

    def provenance_rbu_origin(self, rule):
        prov = self._meta(self.tp_out).get("provenance") or {}
        self._assert(
            prov.get("origin") == "RBU",
            rule["id"],
            f"metadata.provenance.origin must be RBU, got {prov.get('origin')!r}",
        )
        self._assert(
            prov.get("last_update") == "RBU",
            rule["id"],
            f"metadata.provenance.last_update must be RBU, got {prov.get('last_update')!r}",
        )

    def only_rbu_fields_written(self, rule):
        # SSG top-level fields must be unchanged
        for key in ("ssg_signature", "ssg_layer_bitmap", "ssg_reason_code", "ssg_status"):
            if key in self.tp_in:
                self._assert(
                    self.tp_in.get(key) == self.tp_out.get(key),
                    rule["id"],
                    f"{key} was modified by RBU",
                )

        # process / intake / context (top-level or under metadata) must not be newly introduced or altered
        for key in ("process", "intake"):
            if key in self.tp_in:
                self._assert(
                    self.tp_in.get(key) == self.tp_out.get(key),
                    rule["id"],
                    f"{key} was modified by RBU",
                )

        # residue / structural must be unchanged when present
        in_meta = self._meta(self.tp_in)
        out_meta = self._meta(self.tp_out)
        for key in ("residue", "residue_metadata", "structural_metadata", "structural_graph"):
            if key in in_meta and in_meta.get(key) is not None:
                self._assert(
                    in_meta.get(key) == out_meta.get(key),
                    rule["id"],
                    f"metadata.{key} was modified by RBU",
                )

    def no_forbidden_layer_writes(self, rule):
        sem_out = self._semantic(self.tp_out)
        # Must not write TPTB / TPSF
        for key in ("tptb", "tpsf"):
            if key not in self._semantic(self.tp_in) and key in sem_out:
                self._assert(False, rule["id"], f"RBU must not write semantic.{key}")

        # Must not write truth/done style fields at top level
        for key in ("truth", "done", "truth_evaluation"):
            if key not in self.tp_in and key in self.tp_out:
                self._assert(False, rule["id"], f"RBU must not write {key}")

        # Must not newly introduce routing_metadata
        in_meta = self._meta(self.tp_in)
        out_meta = self._meta(self.tp_out)
        if "routing_metadata" not in in_meta and out_meta.get("routing_metadata") is not None:
            self._assert(False, rule["id"], "RBU must not write metadata.routing_metadata")

    def empty_input_still_writes(self, rule):
        sem_in = self._semantic(self.tp_in)
        has_meaning = bool(
            sem_in.get("identity")
            or sem_in.get("stance")
            or sem_in.get("register")
            or sem_in.get("tone")
            or sem_in.get("tags")
            or (self._meta(self.tp_in).get("lineage_markers"))
        )
        if not has_meaning:
            sem_out = self._semantic(self.tp_out)
            prov = self._meta(self.tp_out).get("provenance") or {}
            self._assert(
                "identity" in sem_out and "stance" in sem_out,
                rule["id"],
                "Empty input must still write semantic.identity and semantic.stance",
            )
            self._assert(
                isinstance(prov, dict) and prov.get("origin") == "RBU",
                rule["id"],
                "Empty input must still write metadata.provenance with origin RBU",
            )

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "RBU output missing; cannot validate progressive lineup.",
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
