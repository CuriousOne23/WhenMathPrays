"""
CE Rulechecker (Version 2.0)
Aligned with:
  - ce_rules.yaml v2.0
  - ce_testbench.yaml (multi-test)
  - ce_py_struc_pgm.md (Version 2.0)
  - 20.108 / 20.108.010
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


class CERuleChecker:
    def __init__(self, tp_input, tp_output, rules):
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.rules = rules or []
        self.errors: List[Tuple[str, str]] = []

    def _get(self, root, *keys):
        cur = root
        for k in keys:
            if cur is None or not isinstance(cur, dict):
                return None
            cur = cur.get(k, None)
        return cur

    def _assert(self, condition, rule_id, message):
        if not condition:
            self.errors.append((rule_id, message))

    # ----------------------------------------------------------
    # Classic rules (preserved)
    # ----------------------------------------------------------

    def deterministic_replay(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "CE output is missing; cannot validate deterministic replay.",
        )

    def context_normalization(self, rule):
        ctx_out = self._get(self.tp_out, "metadata", "context") or {}
        ctx_in = self._get(self.tp_in, "metadata", "context", "context_fields")
        if ctx_in is None:
            # Already flattened input
            ctx_in = self._get(self.tp_in, "metadata", "context") or {}

        required_fields = [
            "topic",
            "stance",
            "intent",
            "register",
            "politeness",
            "tone",
            "continuity",
            "direction",
            "coherence",
            "importance",
            "clarifying_fields",
        ]

        for field in required_fields:
            self._assert(
                field in ctx_out,
                rule["id"],
                f"Missing normalized context field: {field}",
            )

        cf_in = (ctx_in or {}).get("clarifying_fields", []) or []
        cf_out = ctx_out.get("clarifying_fields", []) or []
        # Only enforce preservation when input had clarifying_fields and no reset
        reset_flags = (
            self._get(self.tp_in, "metadata", "context", "reset_flags") or {}
        )
        if not reset_flags.get("clarifying_fields"):
            self._assert(
                list(cf_in) == list(cf_out),
                rule["id"],
                "clarifying_fields not preserved deterministically.",
            )

    def bounded_category_integrity(self, rule):
        return

    def msl_reconciliation(self, rule):
        ctx = self._get(self.tp_out, "metadata", "context") or {}
        msl = self._get(self.tp_in, "metadata", "msl") or {}

        for field in ["stance", "direction", "coherence"]:
            msl_val = msl.get(field, None)
            if msl_val is None:
                continue
            if ctx.get(field) != msl_val:
                # Allow override only when reset flag is set for that field
                reset_flags = (
                    self._get(self.tp_in, "metadata", "context", "reset_flags") or {}
                )
                if reset_flags.get(field):
                    continue
                self._assert(
                    False,
                    rule["id"],
                    f"MSL reconciliation failed for field: {field}",
                )

    def msl_alignment_integrity(self, rule):
        self.msl_reconciliation(rule)

    def continuity_validation(self, rule):
        return

    def continuity_integrity(self, rule):
        ctx_out = self._get(self.tp_out, "metadata", "context") or {}
        self._assert(
            "continuity" in ctx_out,
            rule["id"],
            "Continuity missing from CE output.",
        )

    def importance_validation(self, rule):
        return

    def clarifying_fields_integrity(self, rule):
        ctx_in = self._get(self.tp_in, "metadata", "context", "context_fields")
        if ctx_in is None:
            ctx_in = self._get(self.tp_in, "metadata", "context") or {}
        ctx_out = self._get(self.tp_out, "metadata", "context") or {}

        cf_in = (ctx_in or {}).get("clarifying_fields", []) or []
        cf_out = ctx_out.get("clarifying_fields", []) or []
        reset_flags = (
            self._get(self.tp_in, "metadata", "context", "reset_flags") or {}
        )
        if reset_flags.get("clarifying_fields"):
            return
        self._assert(
            list(cf_in) == list(cf_out),
            rule["id"],
            "clarifying_fields not preserved deterministically.",
        )

    def extraction_audit_integrity(self, rule):
        audit = self._get(self.tp_out, "metadata", "context", "extraction_audit")
        self._assert(audit is not None, rule["id"], "Extraction audit missing.")
        if audit is None:
            return
        required_sections = [
            "normalized_fields",
            "msl_reconciliation",
            "continuity_validation",
            "importance_validation",
            "clarifying_validation",
        ]
        for sec in required_sections:
            self._assert(
                sec in audit,
                rule["id"],
                f"Extraction audit missing section: {sec}",
            )

    def extraction_audit_replay_stability(self, rule):
        audit = self._get(self.tp_out, "metadata", "context", "extraction_audit")
        self._assert(
            audit is not None,
            rule["id"],
            "Extraction audit missing; cannot validate replay stability.",
        )

    def provenance_integrity(self, rule):
        prov = self._get(self.tp_out, "metadata", "context", "context_provenance")
        self._assert(prov is not None, rule["id"], "CE provenance missing.")
        if prov is None:
            return
        self._assert(
            prov.get("origin") == "CE",
            rule["id"],
            "CE provenance origin incorrect.",
        )

    def provenance_extension_integrity(self, rule):
        prov = self._get(self.tp_out, "metadata", "context", "context_provenance") or {}
        lineage = prov.get("commit_lineage", []) or []
        self._assert(
            len(lineage) >= 1,
            rule["id"],
            "Commit lineage missing or empty.",
        )

    def version_tag_integrity(self, rule):
        tag = self._get(self.tp_out, "metadata", "context", "ce_version_tag")
        self._assert(
            isinstance(tag, str) and tag.startswith("CE_v"),
            rule["id"],
            "CE version tag incorrect or missing.",
        )

    def forbidden_behavior_integrity(self, rule):
        ccr_in = self._get(self.tp_in, "cex", "ccr")
        ccr_out = self._get(self.tp_out, "cex", "ccr")
        self._assert(
            ccr_in == ccr_out,
            rule["id"],
            "Forbidden modification: CCR fields changed by CE.",
        )

    def semantic_boundary_integrity(self, rule):
        imp_in = self._get(self.tp_in, "semantic", "importance")
        imp_out = self._get(self.tp_out, "semantic", "importance")
        self._assert(
            imp_in == imp_out,
            rule["id"],
            "Forbidden modification: semantic-importance changed by CE.",
        )

    def progressive_lineup_compatibility(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "CE output missing; cannot validate progressive lineup compatibility.",
        )

    def progressive_lineup_strictness(self, rule):
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "CE output missing; cannot validate progressive lineup strictness.",
        )

    # ----------------------------------------------------------
    # Candidate-set rules (20.108.010)
    # ----------------------------------------------------------

    def candidate_set_present(self, rule):
        cs = self._get(self.tp_out, "ce", "candidate_set")
        self._assert(
            isinstance(cs, list) and len(cs) >= 1,
            rule["id"],
            "TP.ce.candidate_set[] missing or empty.",
        )

    def candidate_set_schema(self, rule):
        cs = self._get(self.tp_out, "ce", "candidate_set") or []
        required_top = [
            "candidate_id",
            "fftm_fields",
            "structural_features",
            "semantic_adjacent_features",
            "next_context",
            "provenance",
        ]
        required_fftm = [
            "token_surface",
            "token_base",
            "token_expression",
            "token_intent",
        ]
        required_struct = [
            "surface_id",
            "lemma_id",
            "expression_id",
            "ordering_id",
            "constraint_family_id",
            "next_context_id",
        ]
        required_sa = ["semantic_residue", "structural_residue"]

        for i, cand in enumerate(cs):
            if not isinstance(cand, dict):
                self._assert(False, rule["id"], f"candidate[{i}] is not an object")
                continue
            for k in required_top:
                self._assert(
                    k in cand,
                    rule["id"],
                    f"candidate[{i}] missing key: {k}",
                )
            fftm = cand.get("fftm_fields") or {}
            for k in required_fftm:
                self._assert(
                    k in fftm,
                    rule["id"],
                    f"candidate[{i}].fftm_fields missing: {k}",
                )
            sf = cand.get("structural_features") or {}
            for k in required_struct:
                self._assert(
                    k in sf,
                    rule["id"],
                    f"candidate[{i}].structural_features missing: {k}",
                )
            sa = cand.get("semantic_adjacent_features") or {}
            for k in required_sa:
                self._assert(
                    k in sa,
                    rule["id"],
                    f"candidate[{i}].semantic_adjacent_features missing: {k}",
                )

    def candidate_set_unique_ids(self, rule):
        cs = self._get(self.tp_out, "ce", "candidate_set") or []
        ids = [c.get("candidate_id") for c in cs if isinstance(c, dict)]
        self._assert(
            len(ids) == len(set(ids)),
            rule["id"],
            "candidate_id values are not unique.",
        )

    def candidate_set_ordering(self, rule):
        cs = self._get(self.tp_out, "ce", "candidate_set") or []

        def key_fn(c):
            cid = c.get("candidate_id", 0)
            oid = (c.get("structural_features") or {}).get("ordering_id", 0.0)
            surface = (c.get("fftm_fields") or {}).get("token_surface", "") or ""
            return (cid, oid, surface)

        ordered = sorted([c for c in cs if isinstance(c, dict)], key=key_fn)
        self._assert(
            cs == ordered,
            rule["id"],
            "candidate_set is not in canonical order.",
        )

    def candidate_set_no_scoring(self, rule):
        cs = self._get(self.tp_out, "ce", "candidate_set") or []
        for i, c in enumerate(cs):
            if not isinstance(c, dict):
                continue
            for forbidden in ("normalized_score", "raw_score", "distribution", "entropy"):
                self._assert(
                    forbidden not in c,
                    rule["id"],
                    f"candidate[{i}] contains scoring field '{forbidden}' (ISc-only).",
                )

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
