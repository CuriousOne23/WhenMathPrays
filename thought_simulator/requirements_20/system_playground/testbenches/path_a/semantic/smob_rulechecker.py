"""
SmOB Rulechecker (Version 1.0)
"""


class SmOBRuleChecker:
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
        self._assert(self.tp_out is not None, rule["id"], "SmOB output is missing.")

    def cue_map_integrity(self, rule):
        cmap = self._get(self.tp_out, "structural", "smob_cue_map")
        self._assert(cmap is not None, rule["id"], "smob_cue_map missing.")
        if cmap is None:
            return
        for key in [
            "semantic_adjacent_cues",
            "modality_cues",
            "affect_markers",
            "conflict_adjacent_signals",
            "underspecification_adjacent_signals",
            "constraint_importance_adjacent_signals",
            "discourse_adjacent_cues",
            "routing_semantic_cues",
            "delta_h_semantic_adjacent",
        ]:
            self._assert(key in cmap, rule["id"], f"smob_cue_map missing {key}")

    def residue_integrity(self, rule):
        residue = self._get(self.tp_out, "structural", "smob_residue")
        self._assert(residue is not None, rule["id"], "smob_residue missing.")
        if residue is None:
            return
        for key in ["tr_input_cues", "presemantic_residue_hash"]:
            self._assert(key in residue, rule["id"], f"smob_residue missing {key}")

    def audit_record_integrity(self, rule):
        audit = self._get(self.tp_out, "metadata", "smob_audit_record")
        self._assert(audit is not None, rule["id"], "smob_audit_record missing.")
        if audit is None:
            return
        for key in ["support_yaml_load_status", "provenance_lineage"]:
            self._assert(key in audit, rule["id"], f"smob_audit_record missing {key}")

    def upstream_read_only(self, rule):
        ctx_in = self._get(self.tp_in, "metadata", "context", "context_fields")
        ctx_out = self._get(self.tp_out, "metadata", "context", "context_fields")
        if ctx_in is not None and ctx_out is not None:
            self._assert(
                ctx_in == ctx_out,
                rule["id"],
                "Forbidden modification: context_fields changed by SmOB.",
            )
        msl_in = self._get(self.tp_in, "metadata", "msl")
        msl_out = self._get(self.tp_out, "metadata", "msl")
        if msl_in is not None and msl_out is not None:
            self._assert(
                msl_in == msl_out,
                rule["id"],
                "Forbidden modification: MSL changed by SmOB.",
            )

    def write_authority(self, rule):
        structural = self._get(self.tp_out, "structural") or {}
        self._assert(
            "smob_cue_map" in structural,
            rule["id"],
            "Missing owned field smob_cue_map",
        )
        self._assert(
            "smob_residue" in structural,
            rule["id"],
            "Missing owned field smob_residue",
        )

    def no_enforcement_or_meaning(self, rule):
        residue = self._get(self.tp_out, "structural", "smob_residue") or {}
        self._assert(
            "enforced_constraints" not in residue,
            rule["id"],
            "Forbidden: SmOB attempted constraint enforcement.",
        )
        self._assert(
            "semantic_meaning" not in residue,
            rule["id"],
            "Forbidden: SmOB produced semantic_meaning.",
        )

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "SmOB output missing; cannot validate progressive lineup.",
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
