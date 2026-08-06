"""
CEx‑CCR Primitive (rule‑driven)
-------------------------------

Implements cross‑correlation between CEX‑IE and CIL using
explicit rule tables from cex_ccr_rules.yaml.

Consumes:
    • cex_ccr_rules.yaml
    • cex_ccr_input.yaml
    • cil_input.yaml
Produces:
    • TP.cex.ccr envelope
"""

import os
import yaml

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


def _alignment_level(name: str) -> int:
    return ALIGNMENT_ENUM.get(name, 0)


class CCRAlignmentComputer:
    """
    Computes alignment by applying rule tables to IE + CIL.
    """

    def __init__(self, ie: dict, semantic_importance: dict, cil_conv: dict):
        self.ie = ie
        self.semantic = semantic_importance
        self.cil = cil_conv

    def compute_identity(self) -> str:
        topic_match = self.ie.get("topic_hint") == self.cil.get("identity_lineage")
        intent_match = self.ie.get("intent_hint") in ["request", "inform"]
        phrase_support = bool(self.ie.get("structural_phrases"))

        if topic_match and intent_match and phrase_support:
            return "strong"
        if topic_match and phrase_support:
            return "moderate"
        if not topic_match and phrase_support:
            return "weak"
        return "none"

    def compute_clarifying(self) -> str:
        reg_match = self.ie.get("register_hint") == self.cil.get("clarifying_lineage")
        pol_match = self.ie.get("politeness_hint") in ["high", "normal"]
        intent_support = self.ie.get("intent_hint") != "none"

        if reg_match and pol_match and intent_support:
            return "strong"
        if reg_match and intent_support:
            return "moderate"
        if intent_support:
            return "weak"
        return "none"

    def compute_context(self) -> str:
        topic_match = self.ie.get("topic_hint") == self.cil.get("context_lineage")
        direction_match = self.ie.get("direction_hint") == "forward"

        if topic_match and direction_match:
            return "strong"
        if topic_match:
            return "moderate"
        if direction_match:
            return "weak"
        return "none"

    def compute_continuity(self) -> str:
        cont_hint = self.ie.get("continuity_hint")
        cont_lineage = self.cil.get("continuity_lineage")

        if cont_hint == cont_lineage:
            return "strong"
        if cont_hint in ["continue", "shift"]:
            return "moderate"
        if cont_hint in ["reset", "unknown"]:
            return "none"
        return "weak"

    def compute_reference(self) -> str:
        ref_hint = self.ie.get("reference_hint")

        if ref_hint in ["previous", "specific_previous"]:
            return "strong"
        if ref_hint == "previous":
            return "moderate"
        if ref_hint == "ambiguous_previous":
            return "weak"
        return "none"

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

        if ent_match and fact_match and self.ie.get("reference_hint") in ["previous", "specific_previous"]:
            return "strong"
        if ent_match and not fact_match:
            return "moderate"
        if not ent_match and not fact_match and (imp_entities or imp_facts):
            return "weak"
        return "none"

    def compute_all(self) -> dict:
        return {
            "identity": self.compute_identity(),
            "clarifying": self.compute_clarifying(),
            "context": self.compute_context(),
            "continuity": self.compute_continuity(),
            "reference": self.compute_reference(),
            "semantic_residue": self.compute_semantic_residue(),
        }


class CCRDecisionEngine:
    """
    Applies decision logic from rule tables.
    """

    def __init__(self, alignments: dict, scores: dict):
        self.align = alignments
        self.scores = scores

    def decide(self) -> str:
        ambiguity = self.scores["ambiguity"]
        identity = self.align["identity"]
        continuity = self.align["continuity"]

        if identity == "none" and ambiguity >= SCORE_THRESHOLDS["ambiguity"]["high"] and continuity == "none":
            return "new"
        if identity == "strong" and ambiguity <= SCORE_THRESHOLDS["ambiguity"]["low"] and continuity == "strong":
            return "specific"
        return "fallback"


class CExCCR:
    """
    Entry point for CCR primitive.
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

        for conv_name, conv in self.cil.items():
            aligner = CCRAlignmentComputer(self.ie, self.semantic, conv)
            alignments = aligner.compute_all()
            scores = self._extract_scores(conv)

            alignment_sum = sum(_alignment_level(v) for v in alignments.values())
            stability = scores["stability"]

            if alignment_sum > best_alignment_sum or (
                alignment_sum == best_alignment_sum and stability > best_stability
            ):
                best_alignment_sum = alignment_sum
                best_stability = stability
                best_conv_name = conv_name
                best_alignments = alignments
                best_scores = scores

        if best_conv_name is None and "conv_10" in self.cil:
            best_conv_name = "conv_10"
            conv = self.cil["conv_10"]
            aligner = CCRAlignmentComputer(self.ie, self.semantic, conv)
            best_alignments = aligner.compute_all()
            best_scores = self._extract_scores(conv)

        decision_engine = CCRDecisionEngine(best_alignments, best_scores)
        decision = decision_engine.decide()

        if decision == "new":
            selected_conversation = None
        elif decision == "fallback" and best_scores["stability"] < SCORE_THRESHOLDS["stability"]["fallback_minimum"]:
            selected_conversation = "conv_10" if "conv_10" in self.cil else best_conv_name
        else:
            selected_conversation = best_conv_name

        return {
            "cex": {
                "ccr": {
                    "alignment": best_alignments,
                    "scores": best_scores,
                    "decision": decision,
                    "selected_conversation": selected_conversation,
                }
            }
        }
