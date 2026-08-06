"""
CEx‑CCR Rulechecker
-------------------

Validates the shape and basic consistency of TP.cex.ccr envelopes
produced by the CEx‑CCR primitive.

This module is used by:
    • cex_ccr_testbench.py
    • progressive_lineup_testing
    • development sanity checks

It does NOT enforce full semantic correctness — only structural
and enum-level constraints.
"""

import os
import yaml

# ============================================================
# LOAD RULES
# ============================================================

BASE_DIR = os.path.dirname(__file__)
RULES_PATH = os.path.join(BASE_DIR, "cex_ccr_rules.yaml")

with open(RULES_PATH, "r", encoding="utf-8") as f:
    CCR_RULES = yaml.safe_load(f)


# ============================================================
# ENUM HELPERS
# ============================================================

ALIGNMENT_ENUM = CCR_RULES.get("alignment_enum", {})


def _validate_alignment_value(field_name: str, value: str):
    if value not in ALIGNMENT_ENUM:
        raise ValueError(
            f"CEx‑CCR Rulechecker: alignment field '{field_name}' "
            f"has invalid value '{value}'. Allowed: {list(ALIGNMENT_ENUM.keys())}"
        )


# ============================================================
# ENVELOPE VALIDATION
# ============================================================

def validate_cex_ccr_envelope(ccr_envelope: dict) -> None:
    """
    Validate the structural envelope of TP.cex.ccr.

    Expected shape:

        ccr_envelope = {
            "alignment": {
                "identity": str,
                "clarifying": str,
                "context": str,
                "continuity": str,
                "reference": str,
                "semantic_residue": str,
            },
            "scores": {
                "ambiguity": float,
                "collapse": float,
                "drift": float,
                "stability": float,
            },
            "decision": str,
            "selected_conversation": str or None,
        }

    Raises ValueError on any structural or enum mismatch.
    """

    if not isinstance(ccr_envelope, dict):
        raise ValueError("CEx‑CCR Rulechecker: ccr_envelope must be a dict.")

    # ---------------- Alignment ----------------
    alignment = ccr_envelope.get("alignment")
    if not isinstance(alignment, dict):
        raise ValueError("CEx‑CCR Rulechecker: 'alignment' must be a dict.")

    required_alignment_fields = [
        "identity",
        "clarifying",
        "context",
        "continuity",
        "reference",
        "semantic_residue",
    ]

    for field in required_alignment_fields:
        if field not in alignment:
            raise ValueError(
                f"CEx‑CCR Rulechecker: alignment missing required field '{field}'."
            )
        value = alignment[field]
        if not isinstance(value, str):
            raise ValueError(
                f"CEx‑CCR Rulechecker: alignment field '{field}' must be a string."
            )
        _validate_alignment_value(field, value)

    # ---------------- Scores ----------------
    scores = ccr_envelope.get("scores")
    if not isinstance(scores, dict):
        raise ValueError("CEx‑CCR Rulechecker: 'scores' must be a dict.")

    required_score_fields = ["ambiguity", "collapse", "drift", "stability"]

    for field in required_score_fields:
        if field not in scores:
            raise ValueError(
                f"CEx‑CCR Rulechecker: scores missing required field '{field}'."
            )
        value = scores[field]
        if not isinstance(value, (int, float)):
            raise ValueError(
                f"CEx‑CCR Rulechecker: score field '{field}' must be numeric."
            )

    # ---------------- Decision ----------------
    decision = ccr_envelope.get("decision")
    if not isinstance(decision, str):
        raise ValueError("CEx‑CCR Rulechecker: 'decision' must be a string.")

    allowed_decisions = ["new", "specific", "fallback"]
    if decision not in allowed_decisions:
        raise ValueError(
            f"CEx‑CCR Rulechecker: 'decision' has invalid value '{decision}'. "
            f"Allowed: {allowed_decisions}"
        )

    # ---------------- Selected Conversation ----------------
    selected = ccr_envelope.get("selected_conversation", None)
    if selected is not None and not isinstance(selected, str):
        raise ValueError(
            "CEx‑CCR Rulechecker: 'selected_conversation' must be a string or None."
        )

    # If decision is "new", selected_conversation must be None
    if decision == "new" and selected is not None:
        raise ValueError(
            "CEx‑CCR Rulechecker: decision 'new' requires "
            "'selected_conversation' to be None."
        )

    # If decision is "specific" or "fallback", selected_conversation must be non-empty
    if decision in ["specific", "fallback"] and not selected:
        raise ValueError(
            f"CEx‑CCR Rulechecker: decision '{decision}' requires "
            "'selected_conversation' to be a non-empty string."
        )

    # If we reach here, envelope is structurally valid
    return

