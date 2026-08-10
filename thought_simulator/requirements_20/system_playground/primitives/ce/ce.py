"""
CE Primitive (Version 1.0)
Canonical Context Engine for Path-A.

Aligned with:
  - ce_py_struc_pgm.md (Version 1.0)
  - 20.108 (CE Envelope)
  - 20.107.030 (CEx-Pck)
  - 20.105.*, 20.15
"""

import copy


class CE:
    def __init__(self, tp_input):
        # TP is mutated in-place, but we keep a deep copy of input for audit
        self.tp = tp_input
        self.tp_in = copy.deepcopy(tp_input)

    # ------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------
    def inspect(self):
        ctx = self.tp.get("metadata", {}).get("context", {})
        ctx_fields = ctx.get("context_fields", {})
        flags = {
            "relevance": ctx.get("relevance_flags", {}),
            "copy_forward": ctx.get("copy_forward_flags", {}),
            "reset": ctx.get("reset_flags", {})
        }

        msl = self.tp.get("metadata", {}).get("msl", {})
        next_ctx = self.tp.get("metadata", {}).get("next_context", {})

        normalized = self._normalize_context(ctx_fields, msl, next_ctx, flags)
        audit = self._build_extraction_audit(normalized, msl, next_ctx, flags)

        self._update_tp(normalized, audit)

    # ------------------------------------------------------------
    # Context Normalization
    # ------------------------------------------------------------
    def _normalize_context(self, ctx_fields, msl, next_ctx, flags):
        """
        Deterministic normalization of context fields.
        CE does not infer meaning; it only reconciles bounded categories.
        """

        normalized = {}

        # Copy all bounded structural categories directly
        for field in [
            "topic", "stance", "intent", "register", "politeness",
            "tone", "continuity", "direction", "coherence",
            "importance", "clarifying_fields"
        ]:
            normalized[field] = ctx_fields.get(field)

        # Reconcile stance/direction/coherence with MSL tokens
        # (bounded categories only, no semantic interpretation)
        if "stance" in msl:
            normalized["stance"] = msl["stance"]
        if "direction" in msl:
            normalized["direction"] = msl["direction"]
        if "coherence" in msl:
            normalized["coherence"] = msl["coherence"]

        # Continuity handling (bounded categories)
        continuity = ctx_fields.get("continuity")
        if continuity in ["none", "weak", "moderate", "strong"]:
            normalized["continuity"] = continuity

        # Clarifying fields preserved deterministically
        normalized["clarifying_fields"] = ctx_fields.get("clarifying_fields", [])

        # Copy-forward behavior (bounded structural categories only)
        if flags["copy_forward"].get("topic"):
            normalized["topic"] = ctx_fields.get("topic")
        if flags["copy_forward"].get("direction"):
            normalized["direction"] = ctx_fields.get("direction")
        if flags["copy_forward"].get("coherence"):
            normalized["coherence"] = ctx_fields.get("coherence")

        return normalized

    # ------------------------------------------------------------
    # Extraction Audit
    # ------------------------------------------------------------
    def _build_extraction_audit(self, normalized, msl, next_ctx, flags):
        """
        CE extraction audit: deterministic, bounded, replay-safe.
        """

        audit = {
            "normalized_fields": [
                "topic", "stance", "intent", "direction", "coherence"
            ],
            "msl_reconciliation": {
                "stance": normalized.get("stance"),
                "direction": normalized.get("direction"),
                "coherence": normalized.get("coherence")
            },
            "continuity_validation": normalized.get("continuity"),
            "importance_validation": normalized.get("importance"),
            "clarifying_validation": normalized.get("clarifying_fields", [])
        }

        return audit

    # ------------------------------------------------------------
    # Update TP with CE envelope
    # ------------------------------------------------------------
    def _update_tp(self, normalized, audit):
        """
        Writes CE envelope into TP.
        """

        ctx = self.tp.setdefault("metadata", {}).setdefault("context", {})

        # Write normalized fields
        for k, v in normalized.items():
            ctx[k] = v

        # Preserve flags from CEx-Pck
        ctx["relevance_flags"] = self.tp_in.get("metadata", {}).get("context", {}).get("relevance_flags", {})
        ctx["copy_forward_flags"] = self.tp_in.get("metadata", {}).get("context", {}).get("copy_forward_flags", {})
        ctx["reset_flags"] = self.tp_in.get("metadata", {}).get("context", {}).get("reset_flags", {})

        # Write extraction audit
        ctx["extraction_audit"] = audit

        # Write CE provenance
        ctx["context_provenance"] = {
            "origin": "CE",
            "last_update": "CE",
            "commit_lineage": self._extend_commit_lineage()
        }

        # Version tag
        ctx["ce_version_tag"] = "CE_v1.0"

    # ------------------------------------------------------------
    # Commit lineage extension
    # ------------------------------------------------------------
    def _extend_commit_lineage(self):
        """
        CE extends commit lineage deterministically.
        """

        prov_in = self.tp_in.get("metadata", {}).get("context", {}).get("context_provenance", {})
        lineage = prov_in.get("commit_lineage", [])
        lineage = copy.deepcopy(lineage)
        lineage.append("c003")  # deterministic extension for CE
        return lineage

