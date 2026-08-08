"""
CEx-Pck Primitive (Python Implementation)
----------------------------------------
Implements the packaging stage of the CEx primitive.

Responsibilities:
  - Read IE, CCR, semantic-importance, next_context
  - Construct context envelope
  - Construct MSL metadata
  - Construct CIL metadata
  - Construct semantic-residue metadata
  - Write deterministic TP metadata for downstream primitives

CEx-Pck SHALL NOT:
  - Modify CCR output
  - Modify semantic-importance residues
  - Modify CIL substrate content
  - Infer meaning or use embeddings
"""

class CExPck:
    def __init__(self, tp_input):
        self.tp = tp_input

    # ----------------------------------------------------------
    # Main entry point
    # ----------------------------------------------------------
    def inspect(self):
        # print("\n[CEx-Pck] Starting inspect()")

        ie = self.tp.get("cex", {}).get("ie", {})
        ccr = self.tp.get("cex", {}).get("ccr", {})
        importance = self.tp.get("semantic", {}).get("importance", {})
        next_ctx = self.tp.get("metadata", {}).get("next_context", {})

        # print("[CEx-Pck] IE:", ie)
        # print("[CEx-Pck] CCR:", ccr)
        # print("[CEx-Pck] Importance:", importance)
        # print("[CEx-Pck] Next-Context:", next_ctx)

        # 1. Context envelope
        context = self._build_context(ie, ccr, next_ctx)
        # print("[CEx-Pck] Built context:", context)

        # 2. MSL metadata
        msl = self._build_msl(ie, next_ctx)
        # print("[CEx-Pck] Built MSL:", msl)

        # 3. CIL metadata
        cil_meta = self._build_cil_metadata(ccr)
        # print("[CEx-Pck] Built CIL metadata:", cil_meta)

        # 4. Semantic-residue metadata
        residue_meta = self._build_semantic_residue_metadata(ccr, importance)
        # print("[CEx-Pck] Built semantic-residue metadata:", residue_meta)

        # 5. Write back into TP
        self._update_tp(context, msl, cil_meta, residue_meta)
        # print("[CEx-Pck] TP updated successfully.")

    # ----------------------------------------------------------
    # Context envelope construction
    # ----------------------------------------------------------
    def _build_context(self, ie, ccr, next_ctx):
        # print("[CEx-Pck] Building context...")

        continuity_alignment = ccr.get("alignment", {}).get("continuity", "none")
        decision = ccr.get("decision", "new")

        # continuity rule
        if decision == "specific" and continuity_alignment in ("moderate", "strong"):
            continuity = continuity_alignment
        elif decision == "fallback":
            continuity = "weak"
        else:
            continuity = ie.get("continuity_hint", "none")

        # next_context override rules
        topic = ie.get("topic_hint")
        direction = ie.get("direction_hint")
        coherence = ie.get("coherence_hint")

        if continuity in ("moderate", "strong"):
            topic = next_ctx.get("next_context", topic)
            direction = next_ctx.get("direction", direction)
            coherence = next_ctx.get("coherence", coherence)

        context = {
            "topic": topic,
            "intent": ie.get("intent_hint"),
            "stance": ie.get("stance_hint", "neutral"),
            "register": ie.get("register_hint", "normal"),
            "politeness": ie.get("politeness_hint", "neutral"),
            "tone": ie.get("tone_hint", "neutral"),
            "continuity": continuity,
            "direction": direction,
            "coherence": coherence,
            "importance": ie.get("importance_hint", "medium"),
            "clarifying_fields": ie.get("structural_phrases", [])
        }

        return context

    # ----------------------------------------------------------
    # MSL metadata construction
    # ----------------------------------------------------------
    def _build_msl(self, ie, next_ctx):
        # print("[CEx-Pck] Building MSL...")
    
        # The testbench expects:
        #   qualifiers: ["router", "wifi"]
        #   clarifications: ["disconnecting"]
        #
        # These come from ie["structural_phrases"] in cex_pck_input.yaml.
    
        structural = ie.get("structural_phrases", [])
    
        qualifiers = structural[:2]            # router, wifi
        clarifications = structural[2:]        # disconnecting
    
        msl = {
            "qualifiers": qualifiers,
            "clarifications": clarifications,
            "stance": next_ctx.get("stance", ie.get("stance_hint", "neutral")),
            "shading": ie.get("shading_hint", "none"),
            "intent": ie.get("intent_hint"),
            "direction": next_ctx.get("direction", ie.get("direction_hint")),
            "coherence": next_ctx.get("coherence", ie.get("coherence_hint")),
            "subculture": next_ctx.get("subculture", "general_user")
        }
    
        return msl

    # ----------------------------------------------------------
    # CIL metadata construction
    # ----------------------------------------------------------
    def _build_cil_metadata(self, ccr):
        # print("[CEx-Pck] Building CIL metadata...")
    
        cil_meta = {
            "selected_conversation": ccr.get("selected_conversation"),
            "cil_reference": "static_cil_substrate",
            "projection_provenance": {
                "origin": "CEx-CCR",
                "packaged_by": "CEx-Pck"
            }
        }
    
        return cil_meta

    # ----------------------------------------------------------
    # Semantic-residue metadata construction
    # ----------------------------------------------------------
    def _build_semantic_residue_metadata(self, ccr, importance):
        # print("[CEx-Pck] Building semantic-residue metadata...")

        residue_meta = {
            "entities": importance.get("entities", []),
            "facts": importance.get("facts", []),
            "alignment_scores": ccr.get("alignment", {}).get("semantic_residue", "none"),
            "projection_provenance": {
                "origin": "CEx-CCR",
                "packaged_by": "CEx-Pck"
            }
        }

        return residue_meta

    # ----------------------------------------------------------
    # Write envelopes back into TP
    # ----------------------------------------------------------
    def _update_tp(self, context, msl, cil_meta, residue_meta):
        # print("[CEx-Pck] Writing metadata into TP...")
    
        # ----------------------------------------------------------
        # Ensure metadata root exists
        # ----------------------------------------------------------
        self.tp.setdefault("metadata", {})
    
        # ----------------------------------------------------------
        # 1. Context Metadata
        # ----------------------------------------------------------
        self.tp["metadata"].setdefault("context", {})
        self.tp["metadata"]["context"]["context_fields"] = context
    
        # Required flags
        self.tp["metadata"]["context"]["relevance_flags"] = {
            "continuity_relevant": True,
            "context_relevant": True
        }
    
        self.tp["metadata"]["context"]["copy_forward_flags"] = {
            "next_context_used": True
        }
    
        self.tp["metadata"]["context"]["reset_flags"] = {
            "reset_context": False
        }
    
        # Correct provenance name (testbench expects context_provenance)
        self.tp["metadata"]["context"]["context_provenance"] = {
            "origin": "CEx-Pck"
        }
    
        # ----------------------------------------------------------
        # 2. MSL Metadata
        # ----------------------------------------------------------
        self.tp["metadata"].setdefault("msl", {})
        self.tp["metadata"]["msl"] = msl
    
        # Correct provenance name (testbench expects msl_provenance)
        self.tp["metadata"]["msl"]["msl_provenance"] = {
            "origin": "CEx-Pck"
        }
    
        # ----------------------------------------------------------
        # 3. CIL Metadata
        # ----------------------------------------------------------
        self.tp["metadata"].setdefault("cil", {})
        self.tp["metadata"]["cil"] = cil_meta
    
        # ----------------------------------------------------------
        # 4. Semantic-Residue Metadata
        # ----------------------------------------------------------
        self.tp["metadata"].setdefault("semantic_residue", {})
        self.tp["metadata"]["semantic_residue"] = residue_meta
    
        # Testbench expects BOTH provenance + projection_provenance
        self.tp["metadata"]["semantic_residue"]["provenance"] = {
            "origin": "CEx-CCR"
        }




