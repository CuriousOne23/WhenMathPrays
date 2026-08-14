"""
WrdNm Rulechecker (Version 1.0)
Aligned with:
  - wrdnm_rules.yaml
  - 20.44_wrdnm_primitive.md
  - progressive_lineup_testing.md v4.0
"""


class WrdNmRuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors = []

    def _get(self, root, *keys):
        cur = root
        for k in keys:
            if cur is None or not isinstance(cur, dict):
                return None
            cur = cur.get(k)
        return cur

    def _assert(self, condition, rule_id, message):
        if not condition:
            self.errors.append((rule_id, message))

    # ----------------------------------------------------------
    # Rule implementations
    # ----------------------------------------------------------

    def deterministic_output_present(self, rule):
        self._assert(self.tp_out is not None,
                     rule["id"],
                     "WrdNm output is missing.")

    def wrdnm_list_present(self, rule):
        wrdnm = self.tp_out.get("wrdnm")
        self._assert(isinstance(wrdnm, list) and len(wrdnm) >= 1,
                     rule["id"],
                     "TP.wrdnm[] missing or empty after WrdNm.")

    def canonical_fields_present(self, rule):
        wrdnm = self.tp_out.get("wrdnm") or []
        if not wrdnm:
            self._assert(False, rule["id"], "No WrdNm record to check fields.")
            return
        rec = wrdnm[-1]
        required = [
            "surface_id", "lemma_id", "expression_id",
            "temporal_id", "causal_id", "continuity_id", "entity_id", "thread_hash",
            "adjacency", "ordering_id", "structural_importance",
            "constraint_family_id", "constraint_importance", "missing_slot",
            "modality", "affect", "underspec", "semantic_adjacent_importance",
            "routing_id", "transform_id",
            "identity_id", "next_context_id",
        ]
        for key in required:
            self._assert(key in rec,
                         rule["id"],
                         f"WrdNm record missing canonical field: {key}")

    def audit_record_present(self, rule):
        audit = self._get(self.tp_out, "metadata", "wrdnm_audit_record")
        self._assert(audit is not None,
                     rule["id"],
                     "metadata.wrdnm_audit_record missing.")
        if audit is None:
            return
        for key in ["dictionary_load_status", "scalar_table_load_status",
                    "hash_config_status", "conversion_decisions",
                    "missing_fields", "provenance_lineage"]:
            self._assert(key in audit,
                         rule["id"],
                         f"wrdnm_audit_record missing key: {key}")

    def upstream_read_only(self, rule):
        # Spot-check a few nested paths WrdNm reads; they must be unchanged.
        paths = [
            ("IE", "normalized_surface"),
            ("IE", "lemma"),
            ("CE", "temporal", "marker"),
            ("CnOB", "continuity", "marker"),
            ("SmOB", "adjacency", "flag"),
        ]
        for path in paths:
            vin = self._get(self.tp_in, *path)
            vout = self._get(self.tp_out, *path)
            if vin is not None and vout is not None:
                self._assert(vin == vout,
                             rule["id"],
                             f"Upstream field modified: {'.'.join(path)}")

    def numeric_type_integrity(self, rule):
        wrdnm = self.tp_out.get("wrdnm") or []
        if not wrdnm:
            return
        rec = wrdnm[-1]
        for key in ["surface_id", "lemma_id", "modality", "affect",
                    "structural_importance", "constraint_importance"]:
            val = rec.get(key)
            self._assert(isinstance(val, (int, float)),
                         rule["id"],
                         f"{key} must be numeric, got {type(val).__name__}")

        ms = rec.get("missing_slot")
        self._assert(ms in (0, 1, 0.0, 1.0),
                     rule["id"],
                     f"missing_slot must be 0 or 1, got {ms!r}")

        th = rec.get("thread_hash")
        self._assert(isinstance(th, int) and th >= 0,
                     rule["id"],
                     f"thread_hash must be non-negative int, got {th!r}")

    def no_semantic_inference(self, rule):
        wrdnm = self.tp_out.get("wrdnm") or []
        if not wrdnm:
            return
        rec = wrdnm[-1]
        self._assert("inferred_intent" not in rec,
                     rule["id"],
                     "Forbidden: WrdNm produced inferred_intent.")
        self._assert("semantic_meaning" not in rec,
                     rule["id"],
                     "Forbidden: WrdNm produced semantic_meaning.")

    def progressive_lineup_compatibility(self, rule):
        self._assert(self.tp_out is not None,
                     rule["id"],
                     "WrdNm output missing; cannot validate progressive lineup.")

    # ----------------------------------------------------------
    # Entry
    # ----------------------------------------------------------

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
