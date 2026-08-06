"""
CEx‑CCR Primitive
-----------------

Conversation Extraction — Conversation Continuity Resolution (CEx‑CCR)

This primitive:
    • Receives TP.cex.ie (structural hints)
    • Receives TP.semantic.importance (bounded semantic residues)
    • Receives TP.cil (static 10‑conversation substrate)
    • Performs cross‑correlation between CEX‑IE and CIL across:
        identity, clarifying, context, continuity, reference, semantic_residue
    • Extracts scores from CIL metrics
    • Applies deterministic decision logic:
        new / specific / fallback (including default conversation)
    • Returns TP.cex.ccr envelope

Matches:
    • 20.107.020_cex-ccr_primitive.md
    • cex_ccr_py_struc_pgm.md
    • cex_ccr_rules.yaml
    • cex_ccr_testbench.yaml
    • cex_ccr_input.yaml
"""

import os
import yaml
import copy

# ============================================================
# LOAD RULES
# ============================================================

BASE_DIR = os.path.dirname(__file__)
RULES_PATH = os.path.join(
    BASE_DIR,
    "../../testbenches/path_a/semantic/cex_ccr_rules.yaml"
)

with open(RULES_PATH, "r", encoding="utf-8") as f:
    CCR_RULES = yaml.safe_load(f)

ALIGNMENT_ENUM = CCR_RULES["alignment_enum"]
IDENTITY_RULES = CCR_RULES["identity_alignment"]
CLARIFYING_RULES = CCR_RULES["clarifying_alignment"]
CONTEXT_RULES = CCR_RULES["context_alignment"]
CONTINUITY_RULES = CCR_RULES["continuity_alignment"]
REFERENCE_RULES = CCR_RULES["reference_alignment"]
SEMANTIC_RESIDUE_RULES = CCR_RULES["semantic_residue_alignment"]
DECISION_LOGIC = CCR_RULES["decision_logic"]
SCORE_THRESHOLDS = CCR_RULES["score_thresholds"]
TIE_BREAKING = CCR_RULES["tie_breaking"]


# ============================================================
# Helper: alignment level
# ============================================================

def _alignment_level(name: str) -> int:
    return ALIGNMENT_ENUM.get(name, 0)


# ============================================================
# Cross‑correlation alignment computer
# ============================================================

class CCRAlignmentComputer:
    """
    Computes alignment between a single CIL conversation and
    the current CEX‑IE + semantic importance envelope.
    """

    def __init__(self, ie: dict, semantic_importance: dict, cil_conv: dict):
        self.ie = ie
        self.semantic = semantic_importance
        self.cil = cil_conv

    # ---------------- Identity ----------------
    def compute_identity(self) -> str:
        topic = self.ie.get("topic_hint")
        intent = self.ie.get("intent_hint")
        lineage = self.cil.get("identity_lineage")
        phrases = self.ie.get("structural_phrases", [])

        # Strong: topic + intent + structural support
        if topic == lineage and intent in ["request", "inform"] and phrases:
            return "strong"
        # Moderate: topic matches, intent may differ
        if topic == lineage:
            return "moderate"
        # Weak: topic differs but structural phrases present
        if topic != lineage and phrases:
            return "weak"
        # None: no meaningful match
        return "none"

    # ---------------- Clarifying ----------------
    def compute_clarifying(self) -> str:
        reg = self.ie.get("register_hint")
        pol = self.ie.get("politeness_hint")
        clar_lineage = self.cil.get("clarifying_lineage")

        if reg == clar_lineage and pol == "normal":
            return "strong"
        if reg == clar_lineage:
            return "moderate"
        if reg != clar_lineage and reg is not None:
            return "weak"
        return "none"

    # ---------------- Context ----------------
    def compute_context(self) -> str:
        topic = self.ie.get("topic_hint")
        direction = self.ie.get("direction_hint")
        ctx_lineage = self.cil.get("context_lineage")

        if topic == ctx_lineage and direction == "forward":
            return "strong"
        if topic == ctx_lineage:
            return "moderate"
        if direction == "forward":
            return "weak"
        return "none"

    # ---------------- Continuity ----------------
    def compute_continuity(self) -> str:
        cont_hint = self.ie.get("continuity_hint")
        cont_lineage = self.cil.get("continuity_lineage")

        if cont_hint == cont_lineage:
            return "strong"
        if cont_hint in ["continue", "shift"]:
            return "moderate"
        if cont_hint in ["unknown"]:
            return "none"
        return "weak"

    # ---------------- Reference ----------------
    def compute_reference(self) -> str:
        ref_hint = self.ie.get("reference_hint")

        if ref_hint in ["previous", "specific_previous"]:
            return "strong"
        if ref_hint == "previous":
            return "moderate"
        if ref_hint == "ambiguous_previous":
            return "weak"
        return "none"

    # ---------------- Semantic Residue ----------------
    def compute_semantic_residue(self) -> str:
        imp_entities = self.semantic.get("entities", [])
        imp_facts = self.semantic.get("facts", [])
        cil_residue = self.cil.get("semantic_residue", {})
        cil_entities = cil_residue.get("important_entities", [])
        cil_facts = cil_residue.get("important_facts", [])

        if not imp_entities and not imp_facts:
            return "none"

        ent_match = any(e.get("value") in cil_entities for e in imp_entities)
        fact_match = any(f.get("value") in cil_facts for f in imp_facts)

        if ent_match and fact_match:
            return "strong"
        if ent_match:
            return "moderate"
        if imp_entities or imp_facts:
            return "weak"
        return "none"

    # ---------------- Combined ----------------
    def compute_all(self) -> dict:
        return {
            "identity": self.compute_identity(),
            "clarifying": self.compute_clarifying(),
            "context": self.compute_context(),
            "continuity": self.compute_continuity(),
            "reference": self.compute_reference(),
            "semantic_residue": self.compute_semantic_residue(),
        }


# ============================================================
# Decision engine
# ============================================================

class CCRDecisionEngine:
    """
    Applies decision logic (new / specific / fallback) based on
    alignments and scores, including default conversation handling.
    """

    def __init__(self, alignments: dict, scores: dict):
        self.align = alignments
        self.scores = scores

    def decide(self) -> str:
        ambiguity = self.scores["ambiguity"]
        continuity = self.align["continuity"]
        identity = self.align["identity"]

        # NEW conversation
        if (
            identity == "none"
            and ambiguity >= SCORE_THRESHOLDS["ambiguity"]["high"]
            and continuity == "none"
        ):
            return "new"

        # SPECIFIC conversation
        if (
            identity == "strong"
            and ambiguity <= SCORE_THRESHOLDS["ambiguity"]["low"]
            and continuity == "strong"
        ):
            return "specific"

        # FALLBACK (including default)
        return "fallback"


# ============================================================
# Main primitive
# ============================================================

class CExCCR:
    """
    CEx‑CCR primitive entry point.

    Usage:
        ccr = CExCCR(TP)
        TP_out = ccr.inspect()
    """

    def __init__(self, TP: dict):
        self.ie = TP["cex"]["ie"]
        self.semantic = TP["semantic"]["importance"]
        self.cil = TP["cil"]

    def _extract_scores(self, conv: dict) -> dict:
        m = conv["metrics"]
        return {
            "ambiguity": m["ambiguity_score"],
            "collapse": m["collapse_risk"],
            "drift": m["drift_score"],
            "stability": m["stability_score"],
        }

    def inspect(self) -> dict:
        best_conv_name = None
        best_alignments = None
        best_scores = None

        best_alignment_sum = -1.0
        best_stability = -1.0

        # ----------------------------------------------------
        # Cross‑correlate CEX‑IE + semantic importance with
        # each CIL conversation
        # ----------------------------------------------------
        for conv_name, conv in self.cil.items():
            aligner = CCRAlignmentComputer(self.ie, self.semantic, conv)
            alignments = aligner.compute_all()
            scores = self._extract_scores(conv)

            # numeric alignment score (weighted sum)
            alignment_sum = sum(_alignment_level(v) for v in alignments.values())
            stability = scores["stability"]

            # tie‑breaking: alignment_sum, then stability
            if alignment_sum > best_alignment_sum:
                best_alignment_sum = alignment_sum
                best_stability = stability
                best_conv_name = conv_name
                best_alignments = alignments
                best_scores = scores
            elif alignment_sum == best_alignment_sum and stability > best_stability:
                best_alignment_sum = alignment_sum
                best_stability = stability
                best_conv_name = conv_name
                best_alignments = alignments
                best_scores = scores

        # ----------------------------------------------------
        # If no conversation found (should not happen), fall
        # back to default conv_10
        # ----------------------------------------------------
        if best_conv_name is None and "conv_10" in self.cil:
            best_conv_name = "conv_10"
            conv = self.cil["conv_10"]
            aligner = CCRAlignmentComputer(self.ie, self.semantic, conv)
            best_alignments = aligner.compute_all()
            best_scores = self._extract_scores(conv)

        # ----------------------------------------------------
        # Decision logic (new / specific / fallback)
        # ----------------------------------------------------
        decision_engine = CCRDecisionEngine(best_alignments, best_scores)
        decision = decision_engine.decide()

        # Default conversation handling:
        # If decision is fallback and stability is below threshold,
        # choose conv_10 as default if available.
        selected_conversation = None
        if decision == "new":
            selected_conversation = None
        else:
            stability_threshold = SCORE_THRESHOLDS["stability"]["fallback_minimum"]
            if decision == "fallback" and best_scores["stability"] < stability_threshold:
                if "conv_10" in self.cil:
                    selected_conversation = "conv_10"
                else:
                    selected_conversation = best_conv_name
            else:
                selected_conversation = best_conv_name

        # ----------------------------------------------------
        # Build output envelope
        # ----------------------------------------------------
        ccr_envelope = {
            "alignment": best_alignments,
            "scores": best_scores,
            "decision": decision,
            "selected_conversation": selected_conversation,
        }

        return {
            "cex": {
                "ccr": ccr_envelope
            }
        }
