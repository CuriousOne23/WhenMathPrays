"""
ts_entry_builder.py
-------------------

Final assembly of TS Path A dictionary entries.

Responsibilities:
    • Consume all upstream components:
        lemma_normalizer
        gloss_extractor
        primitive_classifier
        invariant_generator
        cue_envelope_generator
        routing_signature_generator
        identity_anchor_generator
    • Produce a complete TS dictionary entry object
    • Provide structured output for yaml_writer.py

TS entries are:
    • deterministic
    • bounded
    • reviewer-friendly
    • composed of lexical + structural + routing components
"""

from dataclasses import dataclass
from typing import Any, Dict

from lemma_normalizer import normalize_lemma
from gloss_extractor import extract_gloss_from_synset
from primitive_classifier import classify_primitive
from invariant_generator import generate_invariant
from cue_envelope_generator import generate_cue_envelope
from routing_signature_generator import generate_routing_signature
from identity_anchor_generator import generate_identity_anchor


@dataclass(frozen=True)
class TSEntry:
    """
    A complete TS Path A dictionary entry.

    Fields:
        lemma : str
            Canonical lemma.
        gloss : str
            Canonical gloss.
        primitive : str
            Primitive label.
        invariant : Any
            Invariant object.
        cue_envelope : Any
            Cue envelope object.
        routing_signature : Any
            Routing signature object.
        identity_anchor : Any
            Identity anchor object.
    """
    lemma: str
    gloss: str
    primitive: str
    invariant: Any
    cue_envelope: Any
    routing_signature: Any
    identity_anchor: Any

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert entry to a YAML-ready dictionary.
        """
        return {
            "lemma": self.lemma,
            "gloss": self.gloss,
            "primitive": self.primitive,
            "invariant": {
                "primitive": self.invariant.primitive,
                "core_features": self.invariant.core_features,
                "tags": self.invariant.tags,
            },
            "cue_envelope": {
                "primitive_cue": self.cue_envelope.primitive_cue,
                "feature_cues": self.cue_envelope.feature_cues,
                "tag_cues": self.cue_envelope.tag_cues,
            },
            "routing_signature": {
                "primitive_code": self.routing_signature.primitive_code,
                "feature_codes": self.routing_signature.feature_codes,
                "tag_codes": self.routing_signature.tag_codes,
            },
            "identity_anchor": {
                "anchor_vector": self.identity_anchor.anchor_vector,
                "checksum": self.identity_anchor.checksum,
            },
        }


class TSEntryBuilder:
    """
    High-level orchestrator for TS entry construction.

    Input:
        synset (from wordnet_loader)

    Output:
        TSEntry object
    """

    def build(self, synset) -> TSEntry:
        """
        Build a complete TS entry from a synset.

        Parameters
        ----------
        synset : Any
            Parsed WordNet synset-like object.

        Returns
        -------
        TSEntry
        """
        # 1. Normalize lemma
        # Primary lemma
        lemma = normalize_lemma(synset.lemmas[0])
        
        # Optional: alternate lemmas
        alternate_lemmas = [normalize_lemma(l) for l in synset.lemmas[1:]]

        # 2. Extract gloss
        gloss = extract_gloss_from_synset(synset)

        # 3. Classify primitive
        primitive = classify_primitive(lemma, gloss)

        # 4. Generate invariant
        invariant = generate_invariant(primitive, gloss)

        # 5. Generate cue envelope
        cue_envelope = generate_cue_envelope(invariant)

        # 6. Generate routing signature
        routing_signature = generate_routing_signature(cue_envelope)

        # 7. Generate identity anchor
        identity_anchor = generate_identity_anchor(routing_signature)

        # 8. Assemble final TS entry
        return TSEntry(
            lemma=lemma,
            gloss=gloss,
            primitive=primitive,
            invariant=invariant,
            cue_envelope=cue_envelope,
            routing_signature=routing_signature,
            identity_anchor=identity_anchor,
        )


# Convenience function for pipeline modules
def build_ts_entry(synset) -> TSEntry:
    return TSEntryBuilder().build(synset)
