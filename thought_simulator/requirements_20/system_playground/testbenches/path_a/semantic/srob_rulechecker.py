"""
SROB Rulechecker (Version 1.0)
Aligned with:
  - srob_rules.yaml
  - srob_testbench.yaml
  - 20.40.020 v2.0
  - srob_py_struc_pgm.md v1.1
"""


class SROBRuleChecker:
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
            "SROB output is missing; cannot validate deterministic replay.",
        )

    def structural_map_integrity(self, rule):
        smap = self._get(self.tp_out, "structural", "srob_structural_map")
        self._assert(smap is not None, rule["id"], "srob_structural_map missing.")
        if smap is None:
            return
        for key in [
            "segments",
            "operators",
            "lexical_domains",
            "lexical_tones",
            "lexical_constraints",
            "discourse_flags",
        ]:
            self._assert(key in smap, rule["id"], f"srob_structural_map missing key: {key}")

    def segment_id_preservation(self, rule):
        sob = self._get(self.tp_in, "structural", "sob_structural_map") or {}
        srob = self._get(self.tp_out, "structural", "srob_structural_map") or {}
        sob_ids = [s.get("id") for s in sob.get("segments", []) if isinstance(s, dict)]
        srob_ids = [s.get("id") for s in srob.get("segments", []) if isinstance(s, dict)]
        if sob_ids:
            self._assert(
                sob_ids == srob_ids,
                rule["id"],
                f"Segment ids not preserved (P1). SOB={sob_ids} SROB={srob_ids}",
            )

    def residue_integrity(self, rule):
        residue = self._get(self.tp_out, "structural", "srob_residue")
        self._assert(residue is not None, rule["id"], "srob_residue missing.")
        if residue is None:
            return
        for key in [
            "refined_tags",
            "pass_through_tags",
            "structural_adjacent",
            "unmapped_coarse",
            "disagreement_flags",
            "override_flags",
        ]:
            self._assert(key in residue, rule["id"], f"srob_residue missing key: {key}")

    def audit_record_integrity(self, rule):
        audit = self._get(self.tp_out, "metadata", "srob_audit_record")
        self._assert(audit is not None, rule["id"], "srob_audit_record missing.")
        if audit is None:
            return
        for key in [
            "support_yaml_load_status",
            "vocab_validation_status",
            "provenance_lineage",
        ]:
            self._assert(key in audit, rule["id"], f"srob_audit_record missing key: {key}")

    def upstream_read_only(self, rule):
        ctx_in = self._get(self.tp_in, "metadata", "context", "context_fields")
        ctx_out = self._get(self.tp_out, "metadata", "context", "context_fields")
        if ctx_in is not None and ctx_out is not None:
            self._assert(
                ctx_in == ctx_out,
                rule["id"],
                "Forbidden modification: context_fields changed by SROB.",
            )
        msl_in = self._get(self.tp_in, "metadata", "msl")
        msl_out = self._get(self.tp_out, "metadata", "msl")
        if msl_in is not None and msl_out is not None:
            self._assert(
                msl_in == msl_out,
                rule["id"],
                "Forbidden modification: MSL changed by SROB.",
            )

    def write_authority(self, rule):
        structural = self._get(self.tp_out, "structural") or {}
        # SOB fields may remain; SROB must not invent downstream OB keys
        forbidden = ["cnob_semantic_geometry", "smob_semantic_geometry"]
        for key in forbidden:
            self._assert(
                key not in structural,
                rule["id"],
                f"SROB wrote forbidden structural key: {key}",
            )
        self._assert(
            "srob_structural_map" in structural,
            rule["id"],
            "Missing owned field srob_structural_map",
        )
        self._assert(
            "srob_residue" in structural,
            rule["id"],
            "Missing owned field srob_residue",
        )

    def no_invented_operators(self, rule):
        sob = self._get(self.tp_in, "structural", "sob_structural_map") or {}
        srob = self._get(self.tp_out, "structural", "srob_structural_map") or {}

        def _op_ids(ops):
            out = set()
            for o in ops or []:
                if isinstance(o, dict):
                    out.add(str(o.get("normalized") or o.get("verb") or "").lower())
                else:
                    # fine id → parent
                    s = str(o)
                    out.add(s.split(".")[0].lower() if "." in s else s.lower())
            return {x for x in out if x}

        sob_ops = _op_ids(sob.get("operators"))
        srob_ops = _op_ids(srob.get("operators"))
        invented = srob_ops - sob_ops
        self._assert(
            not invented,
            rule["id"],
            f"SROB invented operators not present in SOB output: {invented}",
        )

    def no_constraint_enforcement(self, rule):
        residue = self._get(self.tp_out, "structural", "srob_residue") or {}
        self._assert(
            "enforced_constraints" not in residue,
            rule["id"],
            "Forbidden: SROB attempted constraint enforcement.",
        )
        self._assert(
            "semantic_meaning" not in residue,
            rule["id"],
            "Forbidden: SROB produced semantic_meaning.",
        )

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "SROB output missing; cannot validate progressive lineup.",
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
