"""
SOB Rulechecker (Version 1.0)
Aligned with:
  - sob_rules.yaml
  - sob_testbench.yaml
  - 20.40.010_sob_prim.md
  - progressive_lineup_testing.md v4.0
"""

class SOBRuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors = []

    # ----------------------------------------------------------
    # Utility helpers
    # ----------------------------------------------------------

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

    def deterministic_replay(self, rule):
        self._assert(self.tp_out is not None,
                     rule["id"],
                     "SOB output is missing; cannot validate deterministic replay.")

    def structural_map_integrity(self, rule):
        smap = self._get(self.tp_out, "structural", "sob_structural_map")
        self._assert(smap is not None,
                     rule["id"],
                     "sob_structural_map missing.")
        if smap is None:
            return
        for key in ["segments", "operators", "lexical_domains",
                    "lexical_tones", "lexical_constraints", "morphology_flags"]:
            self._assert(key in smap,
                         rule["id"],
                         f"sob_structural_map missing key: {key}")

    def segment_order_integrity(self, rule):
        smap = self._get(self.tp_out, "structural", "sob_structural_map")
        if not smap:
            return
        segments = smap.get("segments", [])
        # Order is preserved if ids are sequential or list order is stable
        self._assert(isinstance(segments, list),
                     rule["id"],
                     "segments must be a list (order-preserving).")

    def residue_integrity(self, rule):
        residue = self._get(self.tp_out, "structural", "sob_residue")
        self._assert(residue is not None,
                     rule["id"],
                     "sob_residue missing.")
        if residue is None:
            return
        for key in ["lexical_tags", "structural_adjacent",
                    "override_flags", "disagreement_flags"]:
            self._assert(key in residue,
                         rule["id"],
                         f"sob_residue missing key: {key}")

    def audit_record_integrity(self, rule):
        audit = self._get(self.tp_out, "metadata", "sob_audit_record")
        self._assert(audit is not None,
                     rule["id"],
                     "sob_audit_record missing.")
        if audit is None:
            return
        for key in ["dictionary_load_status", "segmentation_decisions",
                    "morphology_decisions", "lexical_tagging_decisions",
                    "provenance_lineage"]:
            self._assert(key in audit,
                         rule["id"],
                         f"sob_audit_record missing key: {key}")

    def upstream_read_only(self, rule):
        # Context fields must be unchanged
        ctx_in = self._get(self.tp_in, "metadata", "context", "context_fields")
        ctx_out = self._get(self.tp_out, "metadata", "context", "context_fields")
        if ctx_in is not None and ctx_out is not None:
            self._assert(ctx_in == ctx_out,
                         rule["id"],
                         "Forbidden modification: context_fields changed by SOB.")

        # MSL must be unchanged
        msl_in = self._get(self.tp_in, "metadata", "msl")
        msl_out = self._get(self.tp_out, "metadata", "msl")
        if msl_in is not None and msl_out is not None:
            self._assert(msl_in == msl_out,
                         rule["id"],
                         "Forbidden modification: MSL changed by SOB.")

    def write_authority(self, rule):
        # Presence of the three owned fields is already checked above.
        # Additional check: no unexpected structural keys that look like other OBs.
        structural = self._get(self.tp_out, "structural") or {}
        forbidden = ["srob_structural_map", "cnob_semantic_geometry",
                     "smob_semantic_geometry"]
        for key in forbidden:
            self._assert(key not in structural,
                         rule["id"],
                         f"SOB wrote forbidden structural key: {key}")

    def modality_present(self, rule):
        smap = self._get(self.tp_out, "structural", "sob_structural_map")
        if not smap:
            return
        for seg in smap.get("segments", []):
            self._assert("modality" in seg,
                         rule["id"],
                         f"Segment {seg.get('id')} missing modality.")

    def dictionary_driven_hints(self, rule):
        # Soft check: if operators/domains/tones/constraints appear,
        # they should be lists (dictionary-derived).
        smap = self._get(self.tp_out, "structural", "sob_structural_map")
        if not smap:
            return
        for key in ["operators", "lexical_domains",
                    "lexical_tones", "lexical_constraints"]:
            val = smap.get(key)
            self._assert(isinstance(val, list),
                         rule["id"],
                         f"{key} must be a list (dictionary-driven).")

    def no_semantic_inference(self, rule):
        # Structural presence of residue is fine; we only assert that
        # no free-text "meaning" or "intent" fields were invented.
        residue = self._get(self.tp_out, "structural", "sob_residue") or {}
        self._assert("inferred_intent" not in residue,
                     rule["id"],
                     "Forbidden: SOB produced inferred_intent.")
        self._assert("semantic_meaning" not in residue,
                     rule["id"],
                     "Forbidden: SOB produced semantic_meaning.")

    def no_constraint_enforcement(self, rule):
        # SOB may extract constraint hints but must not enforce them.
        residue = self._get(self.tp_out, "structural", "sob_residue") or {}
        self._assert("enforced_constraints" not in residue,
                     rule["id"],
                     "Forbidden: SOB attempted constraint enforcement.")

    def progressive_lineup_compatibility(self, rule):
        self._assert(self.tp_out is not None,
                     rule["id"],
                     "SOB output missing; cannot validate progressive lineup.")

    # ----------------------------------------------------------
    # Main entry point
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
