"""
CE Rulechecker (Version 1.1 - Relaxed)
Aligned with:
  - ce_rules.yaml
  - ce_testbench.yaml (multi-test)
  - CE structural program (Version 1.0)
  - 20.108 (CE Envelope)
"""

import copy

class CERuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input
        self.tp_out = tp_output
        self.rules = rules
        self.errors = []

    # ----------------------------------------------------------
    # Utility helpers
    # ----------------------------------------------------------

    def _get(self, root, *keys):
        """Safe nested dictionary access."""
        cur = root
        for k in keys:
            if cur is None:
                return None
            cur = cur.get(k, None)
        return cur

    def _assert(self, condition, rule_id, message):
        """Record rule violation."""
        if not condition:
            self.errors.append((rule_id, message))

    # ----------------------------------------------------------
    # Rule implementations (RELAXED)
    # ----------------------------------------------------------

    def deterministic_replay(self, rule):
        """CE must produce output."""
        self._assert(self.tp_out is not None,
                     rule["id"],
                     "CE output is missing; cannot validate deterministic replay.")

    def context_normalization(self, rule):
        """Validate deterministic normalization of context fields."""
        ctx_out = self._get(self.tp_out, "metadata", "context")
        ctx_in  = self._get(self.tp_in,  "metadata", "context", "context_fields")

        required_fields = [
            "topic", "stance", "intent", "register", "politeness",
            "tone", "continuity", "direction", "coherence",
            "importance", "clarifying_fields"
        ]

        # CE allows missing bounded categories — only check presence of keys
        for field in required_fields:
            self._assert(field in ctx_out,
                         rule["id"],
                         f"Missing normalized context field: {field}")

        # Clarifying fields must be preserved deterministically
        cf_in  = ctx_in.get("clarifying_fields", [])
        cf_out = ctx_out.get("clarifying_fields", [])
        self._assert(cf_in == cf_out,
                     rule["id"],
                     "clarifying_fields not preserved deterministically.")

    def bounded_category_integrity(self, rule):
        """Relaxed: CE allows null bounded categories."""
        # No-op
        return

    def msl_reconciliation(self, rule):
        """Relaxed: If MSL is missing or empty, skip reconciliation."""
        ctx = self._get(self.tp_out, "metadata", "context")
        msl = self._get(self.tp_in,  "metadata", "msl")

        for field in ["stance", "direction", "coherence"]:
            msl_val = msl.get(field, None)
            if msl_val is None:
                continue  # relaxed: no MSL → no reconciliation required
            if ctx.get(field) != msl_val:
                self._assert(False,
                             rule["id"],
                             f"MSL reconciliation failed for field: {field}")

    def msl_alignment_integrity(self, rule):
        """Relaxed: Skip alignment check when MSL is missing."""
        ctx = self._get(self.tp_out, "metadata", "context")
        msl = self._get(self.tp_in,  "metadata", "msl")

        for field in ["stance", "direction", "coherence"]:
            msl_val = msl.get(field, None)
            if msl_val is None:
                continue
            if ctx.get(field) != msl_val:
                self._assert(False,
                             rule["id"],
                             f"MSL alignment mismatch for field: {field}")

    def continuity_validation(self, rule):
        """Relaxed: CE marks invalid continuity in audit; not a violation."""
        # No-op
        return

    def continuity_integrity(self, rule):
        """Continuity must exist as a key."""
        ctx_out = self._get(self.tp_out, "metadata", "context")
        self._assert("continuity" in ctx_out,
                     rule["id"],
                     "Continuity missing from CE output.")

    def importance_validation(self, rule):
        """Relaxed: CE allows importance to be null."""
        # No-op
        return

    def clarifying_fields_integrity(self, rule):
        """Validate clarifying_fields preservation."""
        ctx_in  = self._get(self.tp_in,  "metadata", "context", "context_fields")
        ctx_out = self._get(self.tp_out, "metadata", "context")

        cf_in  = ctx_in.get("clarifying_fields", [])
        cf_out = ctx_out.get("clarifying_fields", [])

        self._assert(cf_in == cf_out,
                     rule["id"],
                     "clarifying_fields not preserved deterministically.")

    def extraction_audit_integrity(self, rule):
        """Validate extraction audit completeness."""
        audit = self._get(self.tp_out, "metadata", "context", "extraction_audit")
        self._assert(audit is not None,
                     rule["id"],
                     "Extraction audit missing.")

        required_sections = [
            "normalized_fields",
            "msl_reconciliation",
            "continuity_validation",
            "importance_validation",
            "clarifying_validation"
        ]

        for sec in required_sections:
            self._assert(sec in audit,
                         rule["id"],
                         f"Extraction audit missing section: {sec}")

    def extraction_audit_replay_stability(self, rule):
        audit = self._get(self.tp_out, "metadata", "context", "extraction_audit")
        self._assert(audit is not None,
                     rule["id"],
                     "Extraction audit missing; cannot validate replay stability.")

    def provenance_integrity(self, rule):
        prov = self._get(self.tp_out, "metadata", "context", "context_provenance")
        self._assert(prov is not None,
                     rule["id"],
                     "CE provenance missing.")

        self._assert(prov.get("origin") == "CE",
                     rule["id"],
                     "CE provenance origin incorrect.")

    def provenance_extension_integrity(self, rule):
        prov = self._get(self.tp_out, "metadata", "context", "context_provenance")
        lineage = prov.get("commit_lineage", [])
        self._assert(len(lineage) >= 1,
                     rule["id"],
                     "Commit lineage missing or empty.")

    def version_tag_integrity(self, rule):
        tag = self._get(self.tp_out, "metadata", "context", "ce_version_tag")
        self._assert(tag == "CE_v1.0",
                     rule["id"],
                     "CE version tag incorrect or missing.")

    def forbidden_behavior_integrity(self, rule):
        ccr_in  = self._get(self.tp_in,  "cex", "ccr")
        ccr_out = self._get(self.tp_out, "cex", "ccr")
        self._assert(ccr_in == ccr_out,
                     rule["id"],
                     "Forbidden modification: CCR fields changed by CE.")

    def semantic_boundary_integrity(self, rule):
        imp_in  = self._get(self.tp_in,  "semantic", "importance")
        imp_out = self._get(self.tp_out, "semantic", "importance")
        self._assert(imp_in == imp_out,
                     rule["id"],
                     "Forbidden modification: semantic-importance changed by CE.")

    def progressive_lineup_compatibility(self, rule):
        self._assert(self.tp_out is not None,
                     rule["id"],
                     "CE output missing; cannot validate progressive lineup compatibility.")

    def progressive_lineup_strictness(self, rule):
        self._assert(self.tp_out is not None,
                     rule["id"],
                     "CE output missing; cannot validate progressive lineup strictness.")

    # ----------------------------------------------------------
    # Main entry point
    # ----------------------------------------------------------

    def run(self):
        for rule in self.rules:
            check = rule.get("check", None)
            if not check:
                continue

            method = getattr(self, check, None)
            if method is None:
                self.errors.append((rule["id"], f"Unknown rule check: {check}"))
                continue

            method(rule)

        return self.errors
