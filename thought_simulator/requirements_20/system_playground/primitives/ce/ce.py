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
import json


class CE:
    """
    CE is a deterministic, bounded-context envelope constructor.
    It performs NO semantic inference. All operations are:
      - bounded
      - deterministic
      - replay-stable
      - structurally aligned with 20.108 CE Envelope
    """

    def __init__(self, tp_input):
        # TP is mutated in-place, but we keep a deep copy of input for audit
        self.tp = tp_input
        self.tp_in = copy.deepcopy(tp_input)

    # ------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------
    def inspect(self):
        """
        CE main execution pipeline:
          1. Extract raw context_fields
          2. Flatten into top-level context
          3. Reconcile bounded categories with MSL
          4. Validate continuity + importance
          5. Build extraction_audit
          6. Update provenance + version tag
          7. Write final CE envelope
        """

        # Extract raw blocks
        ctx = self.tp.get("metadata", {}).get("context", {})
        ctx_fields = ctx.get("context_fields", {})
        flags = {
            "relevance": ctx.get("relevance_flags", {}),
            "copy_forward": ctx.get("copy_forward_flags", {}),
            "reset": ctx.get("reset_flags", {})
        }

        msl = self.tp.get("metadata", {}).get("msl", {})
        next_ctx = self.tp.get("metadata", {}).get("next_context", {})

        # Step 1–3: Flatten + normalize + reconcile
        normalized = self._normalize_context(ctx_fields, msl, next_ctx, flags)

        # Step 4–5: Validation + audit
        audit = self._build_extraction_audit(normalized, msl, next_ctx, flags)

        # Step 6–7: Write CE envelope
        self._update_tp(normalized, audit)

        # Debug print
        print("\n===== CE DEBUG OUTPUT =====")
        print(json.dumps(self.tp["metadata"]["context"], indent=2))
        print("===== END CE DEBUG OUTPUT =====\n")

        return self.tp

    # ------------------------------------------------------------
    # Context Normalization + Flattening
    # ------------------------------------------------------------
    def _normalize_context(self, ctx_fields, msl, next_ctx, flags):
        """
        Deterministic normalization of context fields.
        CE does not infer meaning; it only reconciles bounded categories.

        This step:
          - FLATTENS context_fields → top-level context
          - Reconciles stance/direction/coherence with MSL
          - Applies copy-forward flags
          - Preserves clarifying_fields
          - Validates continuity category
        """

        normalized = {}

        # Flatten all bounded structural categories
        for field in [
            "topic", "stance", "intent", "register", "politeness",
            "tone", "continuity", "direction", "coherence",
            "importance", "clarifying_fields"
        ]:
            normalized[field] = ctx_fields.get(field)

        # MSL reconciliation (bounded categories only)
        if "stance" in msl:
            normalized["stance"] = msl["stance"]
        if "direction" in msl:
            normalized["direction"] = msl["direction"]
        if "coherence" in msl:
            normalized["coherence"] = msl["coherence"]

        # Continuity validation (bounded categories)
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
    # Extraction Audit (MSL reconciliation + validation)
    # ------------------------------------------------------------
    def _build_extraction_audit(self, normalized, msl, next_ctx, flags):
        """
        CE extraction audit: deterministic, bounded, replay-safe.

        This block must match 20.108 CE Envelope exactly:
          - normalized_fields
          - msl_reconciliation
          - continuity_validation
          - importance_validation
          - clarifying_validation

        CE performs NO semantic inference. All operations are:
          - bounded category checks
          - deterministic reconciliation
          - replay-stable validation
        """

        # -----------------------------
        # 1. Normalized fields list
        # -----------------------------
        normalized_fields = [
            "topic",
            "stance",
            "intent",
            "direction",
            "coherence"
        ]

        # -----------------------------
        # 2. MSL reconciliation
        # -----------------------------
        msl_recon = {
            "stance": normalized.get("stance"),
            "direction": normalized.get("direction"),
            "coherence": normalized.get("coherence")
        }

        # -----------------------------
        # 3. Continuity validation
        # -----------------------------
        continuity = normalized.get("continuity")
        if continuity not in ["none", "weak", "moderate", "strong"]:
            continuity_validation = "invalid"
        else:
            continuity_validation = continuity

        # -----------------------------
        # 4. Importance validation
        # -----------------------------
        importance = normalized.get("importance")
        if importance not in ["low", "normal", "high"]:
            importance_validation = "normal"  # deterministic fallback
        else:
            importance_validation = importance

        # -----------------------------
        # 5. Clarifying fields validation
        # -----------------------------
        clarifying_validation = normalized.get("clarifying_fields", [])
        if not isinstance(clarifying_validation, list):
            clarifying_validation = []

        # -----------------------------
        # Final audit block
        # -----------------------------
        audit = {
            "normalized_fields": normalized_fields,
            "msl_reconciliation": msl_recon,
            "continuity_validation": continuity_validation,
            "importance_validation": importance_validation,
            "clarifying_validation": clarifying_validation
        }

        return audit

    # ------------------------------------------------------------
    # Update TP with CE envelope
    # ------------------------------------------------------------
    def _update_tp(self, normalized, audit):
        """
        Writes CE envelope into TP.

        This step must match 20.108 CE Envelope exactly:
          - flattened context fields
          - relevance_flags / copy_forward_flags / reset_flags preserved
          - extraction_audit written
          - provenance updated
          - CE version tag written
          - context_fields removed
        """

        # Ensure metadata/context exists
        ctx = self.tp.setdefault("metadata", {}).setdefault("context", {})

        # --------------------------------------------------------
        # 1. Write normalized fields (flattened)
        # --------------------------------------------------------
        for k, v in normalized.items():
            ctx[k] = v

        # --------------------------------------------------------
        # 2. Preserve flags from CEx-Pck
        # --------------------------------------------------------
        ctx["relevance_flags"] = self.tp_in.get("metadata", {}).get("context", {}).get("relevance_flags", {})
        ctx["copy_forward_flags"] = self.tp_in.get("metadata", {}).get("context", {}).get("copy_forward_flags", {})
        ctx["reset_flags"] = self.tp_in.get("metadata", {}).get("context", {}).get("reset_flags", {})

        # --------------------------------------------------------
        # 3. Write extraction audit
        # --------------------------------------------------------
        ctx["extraction_audit"] = audit

        # --------------------------------------------------------
        # 4. Write CE provenance
        # --------------------------------------------------------
        ctx["context_provenance"] = {
            "origin": "CE",
            "last_update": "CE",
            "commit_lineage": self._extend_commit_lineage()
        }

        # --------------------------------------------------------
        # 5. CE version tag
        # --------------------------------------------------------
        ctx["ce_version_tag"] = "CE_v1.0"

        # --------------------------------------------------------
        # 6. Remove context_fields (flattening complete)
        # --------------------------------------------------------
        if "context_fields" in ctx:
            del ctx["context_fields"]

    # ------------------------------------------------------------
    # Commit lineage extension
    # ------------------------------------------------------------
    def _extend_commit_lineage(self):
        """
        CE extends commit lineage deterministically.

        Expected behavior:
          - read commit_lineage from input provenance
          - append "c003"
          - return new lineage
        """

        prov_in = self.tp_in.get("metadata", {}).get("context", {}).get("context_provenance", {})
        lineage = prov_in.get("commit_lineage", [])
        lineage = copy.deepcopy(lineage)
        lineage.append("c003")  # deterministic extension for CE
        return lineage
