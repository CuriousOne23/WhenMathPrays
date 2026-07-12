"""
primitive_classifier.py
-----------------------

Deterministic primitive assignment for the TS Path A
dictionary_conversion_pipeline.

Responsibilities:
    • Consume normalized lemmas + canonical gloss strings
    • Apply rule-based, deterministic primitive classification
    • Produce one primitive label per synset (no stochasticity)
    • Provide stable inputs for downstream modules:
        invariant_generator, cue_envelope_generator,
        routing_signature_generator, identity_anchor_generator,
        ts_entry_builder

This module performs *semantic pattern classification* but does not
compute invariants, envelopes, or routing geometry.
"""

from typing import Optional


class PrimitiveClassifier:
    """
    Rule-based primitive classifier for TS Path A.

    Primitive space (example set):
        • ENTITY
        • ACTION
        • STATE
        • QUALITY
        • RELATION
        • EVENT
        • PROCESS
        • ABSTRACT

    These can be expanded or refined as TS Path A evolves.
    """

    def classify(self, lemma: str, gloss: str) -> str:
        """
        Assign a deterministic primitive based on lexical + gloss cues.

        Parameters
        ----------
        lemma : str
            Canonical lemma (already normalized).
        gloss : str
            Canonical gloss string.

        Returns
        -------
        str
            Primitive label.
        """

        lemma = lemma.lower().strip()
        gloss = gloss.lower().strip()

        # --- ACTION ---------------------------------------------------------
        if self._looks_like_action(lemma, gloss):
            return "ACTION"

        # --- ENTITY ---------------------------------------------------------
        if self._looks_like_entity(lemma, gloss):
            return "ENTITY"

        # --- STATE ----------------------------------------------------------
        if self._looks_like_state(lemma, gloss):
            return "STATE"

        # --- QUALITY --------------------------------------------------------
        if self._looks_like_quality(lemma, gloss):
            return "QUALITY"

        # --- RELATION -------------------------------------------------------
        if self._looks_like_relation(lemma, gloss):
            return "RELATION"

        # --- EVENT ----------------------------------------------------------
        if self._looks_like_event(lemma, gloss):
            return "EVENT"

        # --- PROCESS --------------------------------------------------------
        if self._looks_like_process(lemma, gloss):
            return "PROCESS"

        # --- ABSTRACT -------------------------------------------------------
        if self._looks_like_abstract(lemma, gloss):
            return "ABSTRACT"

        # Fallback primitive
        return "ENTITY"

    # ----------------------------------------------------------------------
    # Primitive detectors (pure functions)
    # ----------------------------------------------------------------------

    def _looks_like_action(self, lemma: str, gloss: str) -> bool:
        return (
            gloss.startswith("to ") or
            "act" in gloss or
            "perform" in gloss or
            "do something" in gloss
        )

    def _looks_like_entity(self, lemma: str, gloss: str) -> bool:
        return (
            "object" in gloss or
            "person" in gloss or
            "animal" in gloss or
            "thing" in gloss or
            "device" in gloss
        )

    def _looks_like_state(self, lemma: str, gloss: str) -> bool:
        return (
            "state of" in gloss or
            "condition" in gloss or
            "being" in gloss
        )

    def _looks_like_quality(self, lemma: str, gloss: str) -> bool:
        return (
            "characteristic" in gloss or
            "quality" in gloss or
            "attribute" in gloss
        )

    def _looks_like_relation(self, lemma: str, gloss: str) -> bool:
        return (
            "relationship" in gloss or
            "relation" in gloss or
            "between" in gloss
        )

    def _looks_like_event(self, lemma: str, gloss: str) -> bool:
        return (
            "event" in gloss or
            "occurrence" in gloss or
            "happening" in gloss
        )

    def _looks_like_process(self, lemma: str, gloss: str) -> bool:
        return (
            "process" in gloss or
            "series of" in gloss or
            "sequence" in gloss
        )

    def _looks_like_abstract(self, lemma: str, gloss: str) -> bool:
        return (
            "concept" in gloss or
            "idea" in gloss or
            "abstract" in gloss
        )


# Convenience function for pipeline modules
def classify_primitive(lemma: str, gloss: str) -> str:
    return PrimitiveClassifier().classify(lemma, gloss)
