"""
CEx‑CCR Primitive
-----------------

Conversation Extraction — Conversation Continuity Resolution (CEx‑CCR)

This primitive:
    • Receives TP.cex.ie (structural hints)
    • Receives TP.semantic.importance (bounded semantic residues)
    • Receives TP.cil (static 10‑conversation substrate)
    • Computes alignment across 6 dimensions:
        identity, clarifying, context, continuity, reference, semantic_residue
    • Extracts scores from CIL metrics
    • Applies deterministic decision logic:
        new / specific / fallback
    • Returns TP.cex.ccr envelope

This implementation matches:
    • cex_ccr_py_struc_pgm.md (v2.1)
    • cex_ccr_rules.yaml
    • cex_ccr_testbench.yaml
    • cex_ccr_input.yaml
"""

import os
import yaml
import copy

BASE_DIR = os.path.dirname(__file__)
RULES_PATH = os.path.join(BASE_DIR, "../../testbenches/path_a/semantic/cex_ccr_rules.yaml")

with open(RULES_PATH, "r", encoding="utf-8") as f:
    CCR_RULES = yaml.safe_load(f)

ALIGNMENT_ENUM = CCR_RULES["alignment_enum"]
DECISION_LOGIC = CCR_RULES["decision_logic"]
SCORE_THRESHOLDS = CCR_RULES["score_thresholds"]


# ============================================================
# Helper: alignment scoring
# ============================================================

def _alignment_level(name: str) -> int:
    return ALIGNMENT_ENUM.get(name, 0)


# ============================================================
# Alignment Computation
# ============================================================

class CCRAlignmentComputer:

    def __init__(self, ie, semantic_importance, cil_conv):
        self.ie = ie
        self.semantic = semantic_importance
        self.cil = cil_conv

    # ---------------- Identity ----------------
    def compute_identity(self):
        topic = self.ie.get("topic_hint")
        intent = self.ie.get("intent_hint")
        lineage = self.cil.get("identity_lineage")

        if topic == lineage and intent in ["request", "inform"]:
            return "strong"
        if topic == lineage:
            return "moderate"
        if topic != lineage:
            return "weak"
        return "none"

    # ---------------- Clarifying ----------------
    def compute_clarifying(self):
        reg = self.ie.get("register_hint")
        pol = self.ie.get("politeness_hint")
        clar_lineage = self.cil.get("clarifying_lineage")

        if reg == clar_lineage and pol == "normal":
            return "strong"
        if reg == clar_lineage:
            return "moderate"
        if reg != clar_lineage:
            return "weak"
        return "none"

    # ---------------- Context ----------------
    def compute_context(self):
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
    def compute_continuity(self):
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
    def compute_reference(self):
        ref_hint = self.ie.get("reference_hint")
        if ref_hint in ["previous", "specific_previous"]:
            return "strong"
        if ref_hint == "previous":
            return "moderate"
        if ref_hint == "ambiguous_previous":
            return "weak"
        return "none"

    # ---------------- Semantic Residue ----------------
    def compute_semantic_residue(self):
        imp_entities = self.semantic.get("entities", [])
        imp_facts = self.semantic.get("facts", [])
        cil_entities = self.cil.get("semantic_residue", {}).get("important_entities", [])
        cil_facts = self.cil.get("semantic_residue", {}).get("important_facts", [])

        if not imp_entities and not imp_facts:
            return "none"

        ent_match = any(e["value"] in cil_entities for e in imp_entities)
        fact_match = any(f["value"] in cil_facts for f in imp_facts)

        if ent_match and fact_match:
            return "strong"
        if ent_match:
            return "moderate"
        if imp_entities or imp_facts:
            return "weak"
        return "none"

    # ---------------- Combined ----------------
    def compute_all(self):
        return {
            "identity": self.compute_identity(),
            "clarifying": self.compute_clarifying(),
            "context": self.compute_context(),
            "continuity": self.compute_continuity(),
            "reference": self.compute_reference(),
            "semantic_residue": self.compute_semantic_residue(),
        }


# ============================================================
# Decision Logic
# ============================================================

class CCRDecisionEngine:

    def __init__(self, alignments, scores):
        self.align = alignments
        self.scores = scores

    def decide(self):
        # NEW
        if (
            self.align["identity"] == "none"
            and self.scores["ambiguity"] >= SCORE_THRESHOLDS["ambiguity"]["high"]
            and self.align["continuity"] == "none"
        ):
            return "new"

        # SPECIFIC
        if (
            self.align["identity"] == "strong"
            and self.scores["ambiguity"] <= SCORE_THRESHOLDS["ambiguity"]["low"]
            and self.align["continuity"] == "strong"
        ):
            return "specific"

        # FALLBACK
        return "fallback"


# ============================================================
# Main Primitive
# ============================================================

class CExCCR:

    def __init__(self, TP):
        self.ie = TP["cex"]["ie"]
        self.semantic = TP["semantic"]["importance"]
        self.cil = TP["cil"]

    def inspect(self):
        best_conv = None
        best_align_score = -1
        best_stability = -1

        # Evaluate all CIL conversations
        for conv_name, conv in self.cil.items():
            aligner = CCRAlignmentComputer(self.ie, self.semantic, conv)
            alignments = aligner.compute_all()

            # numeric alignment score
            score = sum(_alignment_level(v) for v in alignments.values())

            stability = conv["metrics"]["stability_score"]

            # tie-break: highest alignment score, then stability
            if score > best_align_score or (score == best_align_score and stability > best_stability):
                best_align_score = score
                best_stability = stability
                best_conv = conv_name
                best_alignments = alignments
                best_scores = conv["metrics"]

        # Decision
        decision_engine = CCRDecisionEngine(best_alignments, best_scores)
        decision = decision_engine.decide()

        selected = None if decision == "new" else best_conv

        return {
            "cex": {
                "ccr": {
                    "alignment": best_alignments,
                    "scores": {
                        "ambiguity": best_scores["ambiguity_score"],
                        "collapse": best_scores["collapse_risk"],
                        "drift": best_scores["drift_score"],
                        "stability": best_scores["stability_score"],
                    },
                    "decision": decision,
                    "selected_conversation": selected,
                }
            }
        }

