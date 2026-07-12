"""
cue_envelope_generator.py
-------------------------

Deterministic cue envelope generation for the TS Path A
dictionary_conversion_pipeline.

Responsibilities:
    • Consume invariants (primitive + core_features + tags)
    • Produce a bounded, non-semantic cue envelope
    • Provide lexical/structural cues for downstream modules:
        routing_signature_generator, identity_anchor_generator,
        ts_entry_builder

Cue envelopes are:
    • small
    • deterministic
    • non-semantic
    • derived after cleanup but before entropy scoring
    • identical for clean and corrected paths
"""

from dataclasses import dataclass
from typing import List
from invariant_generator import Invariant


@dataclass(frozen=True)
class CueEnvelope:
    """
    A cue envelope is a compact, deterministic set of lexical/structural
    cues extracted from invariants.

    Fields:
        primitive_cue : str
            Primitive label (ENTITY, ACTION, etc.)
        feature_cues : List[str]
            Selected lexical features (bounded subset).
        tag_cues : List[str]
            Coarse invariant tags (bounded subset).
    """
    primitive_cue: str
    feature_cues: List[str]
    tag_cues: List[str]


class CueEnvelopeGenerator:
    """
    Rule-based cue envelope generator for TS Path A.

    The envelope is intentionally small and non-semantic:
        • primitive cue = primitive
        • feature cues = first N invariant features
        • tag cues = first M invariant tags
    """

    MAX_FEATURE_CUES = 5
    MAX_TAG_CUES = 3

    def generate(self, invariant: Invariant) -> CueEnvelope:
        """
        Generate a cue envelope from an invariant.

        Parameters
        ----------
        invariant : Invariant
            Semantic invariant object.

        Returns
        -------
        CueEnvelope
        """
        primitive_cue = invariant.primitive

        feature_cues = invariant.core_features[: self.MAX_FEATURE_CUES]
        tag_cues = invariant.tags[: self.MAX_TAG_CUES]

        return CueEnvelope(
            primitive_cue=primitive_cue,
            feature_cues=feature_cues,
            tag_cues=tag_cues,
        )


# Convenience function for pipeline modules
def generate_cue_envelope(invariant: Invariant) -> CueEnvelope:
    return CueEnvelopeGenerator().generate(invariant)
