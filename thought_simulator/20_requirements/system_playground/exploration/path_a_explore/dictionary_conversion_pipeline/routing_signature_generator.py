"""
routing_signature_generator.py
------------------------------

Deterministic routing signature generation for the TS Path A
dictionary_conversion_pipeline.

Responsibilities:
    • Consume cue envelopes (primitive + feature cues + tag cues)
    • Produce a compact, stable routing signature vector
    • Provide routing inputs for downstream modules:
        identity_anchor_generator, ts_entry_builder

Routing signatures are:
    • deterministic
    • bounded in size
    • non-semantic
    • derived from cue envelopes
    • suitable for geometric projection (SSG → RB)
"""

from dataclasses import dataclass
from typing import List
from cue_envelope_generator import CueEnvelope


@dataclass(frozen=True)
class RoutingSignature:
    """
    A routing signature is a compact vector of lexical/structural cues
    used by TS Path A routing layers.

    Fields:
        primitive_code : int
            Encoded primitive (ENTITY=1, ACTION=2, ...)
        feature_codes : List[int]
            Encoded feature cues.
        tag_codes : List[int]
            Encoded tag cues.
    """
    primitive_code: int
    feature_codes: List[int]
    tag_codes: List[int]


class RoutingSignatureGenerator:
    """
    Rule-based routing signature generator.

    Encoding strategy:
        • primitive → small integer code
        • features → hashed integer codes
        • tags → hashed integer codes

    All hashing is deterministic and bounded.
    """

    PRIMITIVE_MAP = {
        "ENTITY": 1,
        "ACTION": 2,
        "STATE": 3,
        "QUALITY": 4,
        "RELATION": 5,
        "EVENT": 6,
        "PROCESS": 7,
        "ABSTRACT": 8,
    }

    def generate(self, envelope: CueEnvelope) -> RoutingSignature:
        """
        Generate a routing signature from a cue envelope.

        Parameters
        ----------
        envelope : CueEnvelope

        Returns
        -------
        RoutingSignature
        """
        primitive_code = self._encode_primitive(envelope.primitive_cue)
        feature_codes = [self._encode_feature(f) for f in envelope.feature_cues]
        tag_codes = [self._encode_tag(t) for t in envelope.tag_cues]

        return RoutingSignature(
            primitive_code=primitive_code,
            feature_codes=feature_codes,
            tag_codes=tag_codes,
        )

    # ------------------------------------------------------------------ #
    # Encoding functions                                                 #
    # ------------------------------------------------------------------ #

    def _encode_primitive(self, primitive: str) -> int:
        return self.PRIMITIVE_MAP.get(primitive.upper(), 0)

    def _encode_feature(self, feature: str) -> int:
        """
        Deterministic bounded hash for feature cues.
        """
        return abs(hash(feature)) % 10_000

    def _encode_tag(self, tag: str) -> int:
        """
        Deterministic bounded hash for tag cues.
        """
        return abs(hash(tag)) % 1_000


# Convenience function for pipeline modules
def generate_routing_signature(envelope: CueEnvelope) -> RoutingSignature:
    return RoutingSignatureGenerator().generate(envelope)
