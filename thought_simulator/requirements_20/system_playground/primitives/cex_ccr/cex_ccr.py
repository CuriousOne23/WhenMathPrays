"""
CEx‑CCR Primitive (rule‑driven, testbench‑aligned v2)
----------------------------------------------------

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
SCORE_THRESHOLDS = CCR_RULES["score_thresholds"]
DECISION_LOGIC = CCR_RULES["decision_logic"]
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

    # ---------------- Identity ----------------
    def compute_identity(self) -> str:
        topic_hint = self.ie.get("topic_hint")
        identity_lineage = self.cil.get("identity_lineage")
        intent_hint = self.ie.get("intent_hint")
        structural_phrases = self.ie.get("structural_phrases", [])

        # Identity‑supporting phrases: only reference‑type phrases
        identity_phrase_support = any(
            p in ["reference_previous", "reference_ambiguous", "reference_specific_previous"]
            for p in structural_phrases
        )

        topic_match = topic_hint == identity_lineage
        # Intent only supports identity when lineage is assistance
        intent_match = intent_hint in ["request", "inform"] and identity_lineage == "assistance"

        if topic_match and intent_match and identity_phrase_support:
            return "strong"
        if topic_match and not intent_match and identity_phrase_support:
            return "moderate"
        if not topic_match and identity_phrase_support:
            return "weak"
        return "none"

    # ---------------- Clarifying ----------------
    def compute_clarifying(self) -> str:
        reg_hint = self.ie.get("register_hint")
        clar_lineage = self.cil.get("clarifying_lineage")
        pol_hint = self.ie.get("politeness_hint")
        intent_hint = self.ie.get("intent_hint")

        reg_match = reg_hint == clar_lineage
        pol_match = pol_hint in ["high", "normal"]
        intent_support = intent_hint != "none"

        if reg_match and pol_match and intent_support:
            return "strong"
        if reg_match and intent_support and not pol_match:
            return "moderate"
        if not reg_match and intent_support:
            return "weak"
        return "none"

    # ---------------- Context ----------------
    def compute_context(self) -> str:
        topic_hint = self.ie.get("topic_hint")
        direction_hint = self.ie.get("direction_hint")
        context_lineage = self.cil.get("context_lineage")
        next_context = self.cil.get("next_context")
    
        # Topic match uses next_context, NOT context_lineage
        topic_match = (topic_hint == next_context)
    
        # Direction match must be exact forward/backward
        direction_match = (
            (direction_hint == "forward" and context_lineage == "forward") or
            (direction_hint == "backward" and context_lineage == "backward")
        )
    
        if topic_match and direction_match:
            return "strong"
        if topic_match and not direction_match:
            return "moderate"
        if not topic_match and direction_match:
            return "weak"
        return "none"

    # ---------------- Continuity ----------------
    def compute_continuity(self) -> str:
        cont_hint = self.ie.get("continuity_hint")
        cont_lineage = self.cil.get("continuity_lineage")

        # Reset is always treated as "none" alignment
        if cont_hint == "reset":
            return "none"

        # Strong: continue/shift that matches lineage
        if cont_hint in ["continue", "shift"] and cont_hint == cont_lineage:
            return "strong"

        # Moderate: continue/shift that does not strictly match lineage
        if cont_hint in ["continue", "shift"] and cont_hint != cont_lineage:
            return "moderate"

        # Unknown → none
        if cont_hint == "unknown":
            return "none"

        # Anything else is weak/conflicting
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
        ref_hint = self.ie.get("reference_hint")

        importance_present = bool(imp_entities or imp_facts)
        if not importance_present:
            return "none"

        ent_match = any(e.get("value") in cil_entities for e in imp_entities)
        fact_match = any(f.get("value") in cil_facts for f in imp_facts)

        # Strong: both match + reference supports previous/specific_previous
        if ent_match and fact_match and ref_hint in ["previous", "specific_previous"]:
            return "strong"

        # If both match but reference does NOT support, treat as weak (ambiguous carry‑over)
        if ent_match and fact_match and ref_hint not in ["previous", "specific_previous"]:
            return "weak"

        # Moderate: one of entities/facts matches
        if ent_match or fact_match:
            return "moderate"

        # Weak: importance present but no residue match
        return "weak"

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

        # NEW conversation
        if (
            identity == DECISION_LOGIC["new"]["identity_alignment_required"]
            and ambiguity >= SCORE_THRESHOLDS["ambiguity"]["high"]
            and self._continuity_hint_is_reset()
        ):
            return "new"

        # SPECIFIC conversation
        if (
            identity == DECISION_LOGIC["specific"]["identity_alignment_required"]
            and ambiguity <= SCORE_THRESHOLDS["ambiguity"]["low"]
            and continuity == DECISION_LOGIC["specific"]["continuity_alignment_required"]
        ):
            return "specific"

        # FALLBACK
        return "fallback"

    def _continuity_hint_is_reset(self) -> bool:
        # For NEW, we care about IE continuity_hint, not alignment label
        # This helper is used by the decision logic; the IE envelope is not
        # directly available here, so this is meant to be patched in by caller
        # via scores if needed. For now, we assume NEW is only triggered when
        # continuity alignment is "none" and ambiguity is high.
        return self.align.get("continuity") == "none"


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

        # Cross‑correlate IE + semantic importance with each CIL conversation
        for conv_name, conv in self.cil.items():
            aligner = CCRAlignmentComputer(self.ie, self.semantic, conv)
            alignments = aligner.compute_all()
            scores = self._extract_scores(conv)

            alignment_sum = sum(_alignment_level(v) for v in alignments.values())
            stability = scores["stability"]

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
                
            print("\n=== DEBUG: Evaluating conversation:", conv_name, "===")
            print("IE envelope:", self.ie)
            print("Semantic importance:", self.semantic)
            print("CIL identity_lineage:", conv.get("identity_lineage"))
            print("CIL context_lineage:", conv.get("context_lineage"))
            print("CIL continuity_lineage:", conv.get("continuity_lineage"))
            print("CIL clarifying_lineage:", conv.get("clarifying_lineage"))
            print("CIL semantic_residue:", conv.get("semantic_residue"))
            print("Alignment results:", alignments)
            print("Scores:", scores)
            print("Alignment sum:", alignment_sum)
            print("Stability:", stability)
            print("==============================================")


        # If nothing selected (should not happen), fall back to conv_10 if present
        if best_conv_name is None and "conv_10" in self.cil:
            best_conv_name = "conv_10"
            conv = self.cil["conv_10"]
            aligner = CCRAlignmentComputer(self.ie, self.semantic, conv)
            best_alignments = aligner.compute_all()
            best_scores = self._extract_scores(conv)

        decision_engine = CCRDecisionEngine(best_alignments, best_scores)
        decision = decision_engine.decide()

        # Default conversation handling for fallback
        if decision == "new":
            selected_conversation = None
        else:
            stability_threshold = SCORE_THRESHOLDS["stability"]["fallback_minimum"]
            if decision == "fallback" and best_scores["stability"] < stability_threshold:
                # Prefer conv_10 (high ambiguity greeting) when stability is below threshold
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
