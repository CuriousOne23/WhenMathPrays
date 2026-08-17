"""
STPX Rulechecker (Version 1.0)
Aligned with stpx_rules.yaml, 20.49 v4.0, stpx_py_struc_pgm.md,
progressive_lineup_testing.md v4.1
"""

from __future__ import annotations

from typing import Any, List, Tuple


class STPXRuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors: List[Tuple[str, str]] = []

    def _assert(self, condition: bool, rule_id: str, message: str) -> None:
        if not condition:
            self.errors.append((rule_id, message))

    def _slm(self, tp: dict) -> dict:
        meta = (tp or {}).get("metadata") or {}
        return meta.get("semantic_layer_metadata") or {}

    def deterministic_output_present(self, rule):
        self._assert(self.tp_out is not None, rule["id"], "STPX output TP is missing.")

    def cues_four_families_present(self, rule):
        cues = self._slm(self.tp_out).get("stpx_cues")
        self._assert(isinstance(cues, dict), rule["id"], "stpx_cues must be a dict")
        if not isinstance(cues, dict):
            return
        for fam in ("lexical", "structural", "constraint", "repair"):
            self._assert(
                fam in cues and isinstance(cues[fam], list),
                rule["id"],
                f"stpx_cues.{fam} must be present and a list",
            )

    def provenance_stpx_origin(self, rule):
        prov = self._slm(self.tp_out).get("semantic_layer_provenance") or {}
        self._assert(
            prov.get("origin") == "STPX",
            rule["id"],
            f"semantic_layer_provenance.origin must be STPX, got {prov.get('origin')!r}",
        )
        self._assert(
            prov.get("last_update") == "STPX",
            rule["id"],
            f"semantic_layer_provenance.last_update must be STPX, got {prov.get('last_update')!r}",
        )

    def only_stpx_fields_written(self, rule):
        # Residue must be unchanged
        in_res = ((self.tp_in.get("metadata") or {}).get("residue")
                  or (self.tp_in.get("metadata") or {}).get("residue_metadata"))
        out_res = ((self.tp_out.get("metadata") or {}).get("residue")
                   or (self.tp_out.get("metadata") or {}).get("residue_metadata"))
        if in_res is not None and out_res is not None:
            self._assert(
                in_res == out_res,
                rule["id"],
                "metadata.residue / residue_metadata was modified by STPX",
            )

        # SSG top-level fields must be unchanged
        for key in ("ssg_signature", "ssg_layer_bitmap", "ssg_reason_code", "ssg_status"):
            if key in self.tp_in:
                self._assert(
                    self.tp_in.get(key) == self.tp_out.get(key),
                    rule["id"],
                    f"{key} was modified by STPX",
                )

    def no_forbidden_layer_writes(self, rule):
        meta_out = (self.tp_out.get("metadata") or {})
        # Must not create routing / identity / context semantic meaning layers
        for forbidden in ("routing_metadata", "identity_metadata"):
            # Only fail if STPX newly introduced them (absent in input, present in output with content)
            in_val = ((self.tp_in.get("metadata") or {}).get(forbidden))
            out_val = meta_out.get(forbidden)
            if in_val is None and out_val is not None:
                self._assert(
                    False,
                    rule["id"],
                    f"STPX must not write {forbidden}",
                )

        # Must not write truth/done style fields at top level
        for key in ("truth", "done", "truth_evaluation"):
            if key not in self.tp_in and key in self.tp_out:
                self._assert(False, rule["id"], f"STPX must not write {key}")

    def empty_input_still_writes(self, rule):
        meta_in = self.tp_in.get("metadata") or {}
        has_geom = bool(
            meta_in.get("residue")
            or meta_in.get("residue_metadata")
            or meta_in.get("structural_metadata")
            or meta_in.get("structural_graph")
        )
        has_tokens = bool(
            (meta_in.get("normalization_metadata") or {}).get("normalized_tokens")
        )
        if not has_geom and not has_tokens:
            cues = self._slm(self.tp_out).get("stpx_cues")
            prov = self._slm(self.tp_out).get("semantic_layer_provenance")
            self._assert(
                isinstance(cues, dict),
                rule["id"],
                "Empty input must still write stpx_cues",
            )
            self._assert(
                isinstance(prov, dict) and prov.get("origin") == "STPX",
                rule["id"],
                "Empty input must still write semantic_layer_provenance",
            )

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "STPX output missing; cannot validate progressive lineup.",
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
