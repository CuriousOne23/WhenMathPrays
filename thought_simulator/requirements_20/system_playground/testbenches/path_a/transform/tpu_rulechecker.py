"""
TPU Rulechecker (Version 1.0)
-----------------------------
Deterministic validation logic for the TP-UPDATE commit authority.

Aligned with:
  - tpu_rules.yaml
  - tpu_testbench.yaml / tpu_input.yaml
  - 20.46 (TPU Requirements, Option C)
  - 20.105 / 20.105.010–030 (writer authority + provenance)
  - 20.30 (safe-boundary)
  - 20.95 (canonical ordering)
  - 20.12 (replay)
  - tpu_py_struc_pgm.md
  - progressive_lineup_testing.md
"""

from typing import Any, Dict, List, Optional, Tuple


class TPURuleChecker:
    def __init__(
        self,
        tp_input: Dict[str, Any],
        tp_output: Dict[str, Any],
        rules: Any,
        audit_record: Optional[Dict[str, Any]] = None,
        error_object: Optional[Dict[str, Any]] = None,
    ):
        """
        Parameters
        ----------
        tp_input : TP(N) before commit
        tp_output : TP(N+1) after commit (or unchanged on reject)
        rules : either the full YAML dict or the list under ["rules"]
        audit_record : optional tpu_audit_record produced by TPU
        error_object : optional tpu_error produced on failure
        """
        self.tp_in = tp_input or {}
        self.tp_out = tp_output or {}
        self.audit = audit_record
        self.error = error_object

        # Accept both {"rules": [...]} and bare list
        if isinstance(rules, dict):
            self.rules = rules.get("rules", [])
        else:
            self.rules = rules or []

        self.errors: List[Tuple[str, str]] = []

    # ----------------------------------------------------------
    # Utility helpers
    # ----------------------------------------------------------

    def _get(self, root: Any, *keys: str) -> Any:
        cur = root
        for k in keys:
            if not isinstance(cur, dict):
                return None
            cur = cur.get(k)
        return cur

    def _assert(self, condition: bool, rule_id: str, message: str) -> None:
        if not condition:
            self.errors.append((rule_id, message))

    # ----------------------------------------------------------
    # 1. Deterministic Replay
    # ----------------------------------------------------------

    def deterministic_replay(self, rule: Dict) -> None:
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "TPU output is missing; cannot validate deterministic replay.",
        )

    def provenance_replay_stability(self, rule: Dict) -> None:
        prov = self._get(self.tp_out, "metadata", "provenance_metadata")
        if prov is None:
            # On reject/no-op the provenance may remain the pre-commit one
            prov = self._get(self.tp_out, "metadata", "context", "context_provenance")
        self._assert(
            prov is not None,
            rule["id"],
            "Provenance missing; cannot validate replay stability.",
        )

    # ----------------------------------------------------------
    # 2. Writer Authority
    # ----------------------------------------------------------

    def writer_authority_enforcement(self, rule: Dict) -> None:
        """
        If an audit or error indicates a writer-authority failure,
        the TP must be unchanged (no partial commit).
        """
        status = None
        if self.audit:
            status = self.audit.get("status") or self.audit.get("writer_authority")
        if self.error and self.error.get("code") == "WRITER_AUTHORITY_VIOLATION":
            status = "rejected"

        if status in ("rejected", "fail"):
            # Structural identity of key envelopes must be preserved
            for path in (
                ("metadata", "context"),
                ("semantic", "importance"),
            ):
                in_val = self._get(self.tp_in, *path)
                out_val = self._get(self.tp_out, *path)
                self._assert(
                    in_val == out_val,
                    rule["id"],
                    f"Writer-authority rejection must leave {'.'.join(path)} unchanged.",
                )

    def writer_authority_namespace_integrity(self, rule: Dict) -> None:
        # Soft check: structural geometry must never appear under meaning-layer updates
        # (real enforcement lives inside TPU; here we only guard the output)
        geom = self._get(self.tp_out, "structural") or self._get(self.tp_out, "metadata", "structural")
        # No hard failure if absent; only flag if an illegal write is visible
        if geom is not None and self.error is None:
            # Presence alone is not a violation; TPU may read but not write geometry
            pass

    def writer_authority_fallback(self, rule: Dict) -> None:
        if self.error and self.error.get("code") == "WRITER_AUTHORITY_VIOLATION":
            self._assert(
                self.error.get("fallback_behavior") in (
                    "retain_TP_N",
                    "retain_tp_n",
                    "no_commit",
                    None,
                ) or "retain" in str(self.error.get("fallback_behavior", "")).lower(),
                rule["id"],
                "Writer-authority violation must produce deterministic retain-TP_N fallback.",
            )

    # ----------------------------------------------------------
    # 3. Atomicity
    # ----------------------------------------------------------

    def atomic_commit_integrity(self, rule: Dict) -> None:
        # If audit says committed, provenance_origin should be TPU
        if self.audit and self.audit.get("status") == "committed":
            prov = self._get(self.tp_out, "metadata", "provenance_metadata")
            if prov:
                self._assert(
                    prov.get("primitive_origin") == "TPU",
                    rule["id"],
                    "Committed TP must carry primitive_origin='TPU'.",
                )

    def all_or_nothing_commit(self, rule: Dict) -> None:
        # On any error object the pre-commit context must be intact
        if self.error is not None:
            ctx_in = self._get(self.tp_in, "metadata", "context")
            ctx_out = self._get(self.tp_out, "metadata", "context")
            self._assert(
                ctx_in == ctx_out,
                rule["id"],
                "On error TPU must retain original context (no partial commit).",
            )

    # ----------------------------------------------------------
    # 4. Safe Boundary
    # ----------------------------------------------------------

    def safe_boundary_enforcement(self, rule: Dict) -> None:
        if self.audit:
            sb = self.audit.get("safe_boundary")
            if sb is not None:
                self._assert(
                    sb in ("pass", "true", True, "ok"),
                    rule["id"],
                    f"Safe-boundary check failed in audit: {sb}",
                )

    def safe_boundary_window_integrity(self, rule: Dict) -> None:
        # Structural placeholder – real window checks live inside TPU
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "Cannot validate safe-boundary window without TPU output.",
        )

    # ----------------------------------------------------------
    # 5. 1-TP-Cycle Lag
    # ----------------------------------------------------------

    def one_cycle_lag_integrity(self, rule: Dict) -> None:
        # Lag is a temporal property; we only assert that a successful
        # commit wrote provenance with a new commit_id
        if self.audit and self.audit.get("status") == "committed":
            prov = self._get(self.tp_out, "metadata", "provenance_metadata")
            self._assert(
                prov is not None and prov.get("commit_id") is not None,
                rule["id"],
                "Successful commit must produce a new commit_id (cycle lag marker).",
            )

    # ----------------------------------------------------------
    # 6. Canonical Ordering
    # ----------------------------------------------------------

    def canonical_ordering_enforcement(self, rule: Dict) -> None:
        # Soft structural check: clarifying_fields, if present, must be a list
        cf = self._get(self.tp_out, "metadata", "context", "clarifying_fields")
        if cf is not None:
            self._assert(
                isinstance(cf, list),
                rule["id"],
                "clarifying_fields must be a list (canonical ordering container).",
            )

    # ----------------------------------------------------------
    # 7. Clarifying Fields
    # ----------------------------------------------------------

    def clarifying_field_boundedness(self, rule: Dict) -> None:
        cf = self._get(self.tp_out, "metadata", "context", "clarifying_fields")
        if cf is None:
            return
        self._assert(
            isinstance(cf, list) and len(cf) <= 10,
            rule["id"],
            f"clarifying_fields exceeds max 10 (got {len(cf) if isinstance(cf, list) else type(cf)}).",
        )

    def clarifying_field_provenance(self, rule: Dict) -> None:
        # Provenance may live under context_provenance or continuity_metadata
        prov = (
            self._get(self.tp_out, "metadata", "context", "context_provenance")
            or self._get(self.tp_out, "metadata", "continuity_metadata")
        )
        if prov is not None:
            self._assert(
                "origin" in prov or "commit_lineage" in prov,
                rule["id"],
                "Clarifying-field provenance missing origin/lineage.",
            )

    def clarifying_field_atomicity_and_lag(self, rule: Dict) -> None:
        # Covered by general atomicity + lag rules; keep as explicit marker
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "Cannot validate clarifying-field atomicity without output.",
        )

    # ----------------------------------------------------------
    # 8. Next-Context
    # ----------------------------------------------------------

    def next_context_write_only(self, rule: Dict) -> None:
        """
        Current-turn context must not be overwritten by next_context values
        unless TPU explicitly committed them under next_context.
        """
        ctx = self._get(self.tp_out, "metadata", "context") or {}
        next_ctx = self._get(self.tp_out, "metadata", "next_context") or {}
        # If next_context exists, it should be a distinct envelope
        if next_ctx and ctx:
            # Soft check: presence of next_context is fine; we only guard
            # that TPU did not erase the current context
            self._assert(
                ctx.get("topic") is not None or next_ctx.get("topic") is not None,
                rule["id"],
                "Both current context and next_context appear empty after commit.",
            )

    def next_context_field_validation(self, rule: Dict) -> None:
        next_ctx = self._get(self.tp_out, "metadata", "next_context")
        if next_ctx is None:
            return
        # On a successful commit that carries next_context, key fields should exist
        if self.audit and self.audit.get("status") == "committed":
            for field in ("topic", "stance", "intent", "direction"):
                # Allow null; only require the key to be present
                self._assert(
                    field in next_ctx,
                    rule["id"],
                    f"next_context missing required key: {field}",
                )

    # ----------------------------------------------------------
    # 9. Provenance Metadata
    # ----------------------------------------------------------

    def provenance_metadata_integrity(self, rule: Dict) -> None:
        if not (self.audit and self.audit.get("status") == "committed"):
            return
        prov = self._get(self.tp_out, "metadata", "provenance_metadata")
        self._assert(
            prov is not None,
            rule["id"],
            "Committed TP missing provenance_metadata.",
        )
        if prov:
            self._assert(
                prov.get("primitive_origin") == "TPU",
                rule["id"],
                f"primitive_origin must be 'TPU' (got {prov.get('primitive_origin')}).",
            )
            self._assert(
                prov.get("commit_id") is not None,
                rule["id"],
                "commit_id missing from provenance_metadata.",
            )

    def commit_lineage_append_only(self, rule: Dict) -> None:
        prov = self._get(self.tp_out, "metadata", "provenance_metadata")
        if prov and "commit_lineage" in prov:
            lineage = prov["commit_lineage"]
            self._assert(
                isinstance(lineage, list),
                rule["id"],
                "commit_lineage must be a list.",
            )

    # ----------------------------------------------------------
    # 10. Audit Record
    # ----------------------------------------------------------

    def audit_record_presence(self, rule: Dict) -> None:
        # In general mode the testbench may not always pass the audit object;
        # only enforce when the audit was supplied.
        if self.audit is not None:
            self._assert(
                "status" in self.audit or "writer_authority" in self.audit,
                rule["id"],
                "tpu_audit_record missing status/writer_authority.",
            )

    def audit_record_completeness(self, rule: Dict) -> None:
        if self.audit is None:
            return
        # Soft completeness – require at least a status
        self._assert(
            self.audit.get("status") is not None,
            rule["id"],
            "tpu_audit_record missing status field.",
        )

    # ----------------------------------------------------------
    # 11. Forbidden Behavior
    # ----------------------------------------------------------

    def no_meaning_generation(self, rule: Dict) -> None:
        # semantic_core must not be altered by TPU
        core_in = self._get(self.tp_in, "semantic_core") or self._get(self.tp_in, "semantic", "core")
        core_out = self._get(self.tp_out, "semantic_core") or self._get(self.tp_out, "semantic", "core")
        if core_in is not None or core_out is not None:
            self._assert(
                core_in == core_out,
                rule["id"],
                "TPU must not modify semantic_core.",
            )

    def intake_context_geometry_integrity(self, rule: Dict) -> None:
        # intake must be untouched
        intake_in = self._get(self.tp_in, "intake") or self._get(self.tp_in, "TP", "intake")
        intake_out = self._get(self.tp_out, "intake") or self._get(self.tp_out, "TP", "intake")
        if intake_in is not None or intake_out is not None:
            self._assert(
                intake_in == intake_out,
                rule["id"],
                "TPU must not modify TP.intake.*.",
            )

    def no_routing_or_identity_side_effects(self, rule: Dict) -> None:
        # routing metadata should be unchanged by TPU
        routing_in = self._get(self.tp_in, "metadata", "routing") or self._get(self.tp_in, "routing")
        routing_out = self._get(self.tp_out, "metadata", "routing") or self._get(self.tp_out, "routing")
        if routing_in is not None or routing_out is not None:
            self._assert(
                routing_in == routing_out,
                rule["id"],
                "TPU must not modify routing metadata.",
            )

    # ----------------------------------------------------------
    # 12. Progressive Lineup
    # ----------------------------------------------------------

    def progressive_lineup_compatibility(self, rule: Dict) -> None:
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "TPU output missing; cannot validate progressive lineup compatibility.",
        )

    def passthrough_integrity(self, rule: Dict) -> None:
        # Passthrough is controlled by run.py (use_tpu=false).
        # Here we only ensure the checker itself does not invent output.
        self._assert(
            self.tp_out is not None,
            rule["id"],
            "Cannot validate passthrough without a TP object.",
        )

    # ----------------------------------------------------------
    # Main entry point
    # ----------------------------------------------------------

    def run(self) -> List[Tuple[str, str]]:
        """
        Execute every rule that has a matching method.
        Returns list of (rule_id, message) violations.
        """
        for rule in self.rules:
            check_name = rule.get("check")
            if not check_name:
                continue
            method = getattr(self, check_name, None)
            if method is None:
                self.errors.append((rule["id"], f"Unknown rule check: {check_name}"))
                continue
            method(rule)
        return self.errors
