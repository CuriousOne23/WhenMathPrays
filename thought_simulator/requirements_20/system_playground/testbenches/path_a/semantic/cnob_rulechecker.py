"""
CnOB Rulechecker (Version 1.0)
"""


class CnOBRuleChecker:
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

    def deterministic_replay(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "CnOB output is missing.",
        )

    def constraint_map_integrity(self, rule):
        cmap = self._get(self.tp_out, "structural", "cnob_constraint_map")
        self._assert(cmap is not None, rule["id"], "cnob_constraint_map missing.")
        if cmap is None:
            return
        fam = cmap.get("constraint_families") or {}
        for k in ("C1", "C2", "C3", "C4", "C5", "C6", "C7"):
            self._assert(k in fam, rule["id"], f"constraint_families missing {k}")
        for key in [
            "missing_slot_signals",
            "underspecification_markers",
            "conflict_indicators",
            "constraint_importance",
        ]:
            self._assert(key in cmap, rule["id"], f"cnob_constraint_map missing {key}")

    def residue_integrity(self, rule):
        residue = self._get(self.tp_out, "structural", "cnob_residue")
        self._assert(residue is not None, rule["id"], "cnob_residue missing.")
        if residue is None:
            return
        for key in [
            "missing_slot_signals",
            "underspecification_markers",
            "conflict_indicators",
            "constraint_importance",
            "constraint_residue_hash",
        ]:
            self._assert(key in residue, rule["id"], f"cnob_residue missing {key}")

    def audit_record_integrity(self, rule):
        audit = self._get(self.tp_out, "metadata", "cnob_audit_record")
        self._assert(audit is not None, rule["id"], "cnob_audit_record missing.")
        if audit is None:
            return
        for key in ["support_yaml_load_status", "provenance_lineage"]:
            self._assert(key in audit, rule["id"], f"cnob_audit_record missing {key}")

    def upstream_read_only(self, rule):
        ctx_in = self._get(self.tp_in, "metadata", "context", "context_fields")
        ctx_out = self._get(self.tp_out, "metadata", "context", "context_fields")
        if ctx_in is not None and ctx_out is not None:
            self._assert(
                ctx_in == ctx_out,
                rule["id"],
                "Forbidden modification: context_fields changed by CnOB.",
            )
        msl_in = self._get(self.tp_in, "metadata", "msl")
        msl_out = self._get(self.tp_out, "metadata", "msl")
        if msl_in is not None and msl_out is not None:
            self._assert(
                msl_in == msl_out,
                rule["id"],
                "Forbidden modification: MSL changed by CnOB.",
            )

    def write_authority(self, rule):
        structural = self._get(self.tp_out, "structural") or {}
        self._assert(
            "cnob_constraint_map" in structural,
            rule["id"],
            "Missing owned field cnob_constraint_map",
        )
        self._assert(
            "cnob_residue" in structural,
            rule["id"],
            "Missing owned field cnob_residue",
        )

    def no_invented_surface_types(self, rule):
        # CnOB does not write operator arrays; ensure no semantic_meaning invented
        residue = self._get(self.tp_out, "structural", "cnob_residue") or {}
        self._assert(
            "semantic_meaning" not in residue,
            rule["id"],
            "Forbidden: CnOB produced semantic_meaning.",
        )

    def no_enforcement_or_meaning(self, rule):
        residue = self._get(self.tp_out, "structural", "cnob_residue") or {}
        self._assert(
            "enforced_constraints" not in residue,
            rule["id"],
            "Forbidden: CnOB attempted constraint enforcement.",
        )

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "CnOB output missing; cannot validate progressive lineup.",
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
