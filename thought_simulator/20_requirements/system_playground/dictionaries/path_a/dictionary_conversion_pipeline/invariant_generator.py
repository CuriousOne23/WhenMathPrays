"""
invariant_generator.py
----------------------

Deterministic semantic invariant generation for the TS Path A
dictionary_conversion_pipeline.

Responsibilities:
    • Consume primitives + canonical gloss strings
    • Derive stable, human-auditable semantic invariants
    • Provide invariant structures for downstream modules:
        cue_envelope_generator, routing_signature_generator,
        identity_anchor_generator, ts_entry_builder

This module does *not* handle routing geometry or envelopes; it only
builds invariant descriptors.
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Invariant:
    """
    A semantic invariant is a stable descriptor of meaning that
    does not depend on local context or runtime state.

    Fields:
        primitive : str
            The primitive assigned to the synset (e.g., ENTITY, ACTION).
        core_features : List[str]
            Key lexical/semantic features extracted from the gloss.
        tags : List[str]
            Additional invariant tags (e.g., 'physical', 'social').
    """
    primitive: str
    core_features: List[str]
    tags: List[str]


class InvariantGenerator:
    """
    Rule-based invariant generator for TS Path A.

    Uses primitive + gloss cues to derive a small, stable set of
    core features and tags.
    """

    def generate(self, primitive: str, gloss: str) -> Invariant:
        """
        Generate a semantic invariant from primitive + gloss.

        Parameters
        ----------
        primitive : str
            Primitive label (e.g., 'ENTITY', 'ACTION').
        gloss : str
            Canonical gloss string.

        Returns
        -------
        Invariant
        """
        gloss = gloss.lower().strip()
        core_features = self._extract_core_features(gloss)
        tags = self._infer_tags(primitive, gloss)

        return Invariant(
            primitive=primitive,
            core_features=core_features,
            tags=tags,
        )

    # ------------------------------------------------------------------ #
    # Core feature extraction                                            #
    # ------------------------------------------------------------------ #

    def _extract_core_features(self, gloss: str) -> List[str]:
        """
        Very simple, deterministic feature extraction.

        For now, we:
            • split on spaces
            • keep content-like words (length >= 4)
            • deduplicate while preserving order
        """
        tokens = [t for t in gloss.split() if len(t) >= 4]
        seen = set()
        features: List[str] = []
        for t in tokens:
            if t not in seen:
                seen.add(t)
                features.append(t)
        return features

    # ------------------------------------------------------------------ #
    # Tag inference                                                      #
    # ------------------------------------------------------------------ #

    def _infer_tags(self, primitive: str, gloss: str) -> List[str]:
        """
        Infer invariant tags from primitive + gloss.

        Tags are coarse, stable descriptors (e.g., 'physical', 'social').
        """
        tags: List[str] = []

        # Primitive-based tags
        if primitive == "ENTITY":
            tags.append("object-like")
        elif primitive == "ACTION":
            tags.append("dynamic")
        elif primitive == "STATE":
            tags.append("static")
        elif primitive == "QUALITY":
            tags.append("descriptive")
        elif primitive == "RELATION":
            tags.append("relational")
        elif primitive == "EVENT":
            tags.append("temporal")
        elif primitive == "PROCESS":
            tags.append("procedural")
        elif primitive == "ABSTRACT":
            tags.append("conceptual")

        # Gloss-based tags
        if any(w in gloss for w in ["person", "people", "social", "group"]):
            tags.append("social")
        if any(w in gloss for w in ["object", "physical", "material", "body"]):
            tags.append("physical")
        if any(w in gloss for w in ["idea", "concept", "belief"]):
            tags.append("mental")
        if any(w in gloss for w in ["time", "period", "duration"]):
            tags.append("temporal")

        # Deduplicate while preserving order
        seen = set()
        unique_tags: List[str] = []
        for t in tags:
            if t not in seen:
                seen.add(t)
                unique_tags.append(t)

        return unique_tags


# Convenience function for pipeline modules
def generate_invariant(primitive: str, gloss: str) -> Invariant:
    return InvariantGenerator().generate(primitive, gloss)
