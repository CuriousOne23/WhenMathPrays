"""
gloss_extractor.py
------------------

Deterministic gloss extraction for the TS Path A
dictionary_conversion_pipeline.

Responsibilities:
    • Consume parsed WordNet synset objects
    • Extract and clean gloss text (definition + examples)
    • Provide stable, canonical gloss strings for downstream modules:
        primitive_classifier, invariant_generator,
        cue_envelope_generator, routing_signature_generator,
        identity_anchor_generator, ts_entry_builder

This module is lexical/structural only: no semantic classification.
"""

import re
from typing import List, Optional


class GlossExtractor:
    """
    Canonical gloss extraction for TS Path A.

    Assumes a synset-like object with at least:
        • synset.gloss  (raw gloss string from WordNet)
        • synset.examples (optional list of example strings)

    The exact synset type is left abstract to keep this module
    decoupled from the WordNet loader implementation.
    """

    _MULTISPACE_PATTERN = re.compile(r"\s+")
    _SEMICOLON_SPLIT_PATTERN = re.compile(r"\s*;\s*")
    _QUOTE_PATTERN = re.compile(r"^[\"']|[\"']$")

    def extract_gloss(
        self,
        raw_gloss: str,
        examples: Optional[List[str]] = None,
    ) -> str:
        """
        Extract a canonical gloss string from raw WordNet data.

        Steps:
            1. Trim and normalize whitespace
            2. Split on semicolons into definition + example fragments
            3. Clean example fragments (strip quotes, extra punctuation)
            4. Optionally append explicit examples list
            5. Return a single deterministic gloss string

        Parameters
        ----------
        raw_gloss : str
            Raw gloss from WordNet (definition + examples).
        examples : Optional[List[str]]
            Optional explicit examples from the synset.

        Returns
        -------
        str
            Canonical TS gloss string.
        """
        if not raw_gloss:
            return ""

        # 1. Normalize whitespace
        gloss = raw_gloss.strip()
        gloss = self._MULTISPACE_PATTERN.sub(" ", gloss)

        # 2. Split on semicolons
        parts = [p.strip() for p in self._SEMICOLON_SPLIT_PATTERN.split(gloss) if p.strip()]

        if not parts:
            return ""

        # First part is treated as the core definition
        definition = parts[0]

        # Remaining parts are treated as inline examples/hints
        inline_examples = [self._clean_example(p) for p in parts[1:]]

        # 3. Merge explicit examples if provided
        if examples:
            inline_examples.extend(self._clean_example(e) for e in examples if e)

        # 4. Build canonical gloss string
        if inline_examples:
            examples_str = "; examples: " + "; ".join(inline_examples)
        else:
            examples_str = ""

        canonical = definition + examples_str
        canonical = self._MULTISPACE_PATTERN.sub(" ", canonical).strip()

        return canonical

    def _clean_example(self, text: str) -> str:
        """
        Clean an example fragment.

        Removes leading/trailing quotes and normalizes whitespace.
        """
        if not text:
            return ""

        t = text.strip()
        t = self._QUOTE_PATTERN.sub("", t)
        t = self._MULTISPACE_PATTERN.sub(" ", t).strip()
        return t

    def extract_from_synset(self, synset) -> str:
        """
        High-level helper: extract gloss from a synset object.

        Expected minimal interface:
            synset.gloss: str
            synset.examples: Optional[List[str]]

        Parameters
        ----------
        synset : Any
            Parsed WordNet synset-like object.

        Returns
        -------
        str
            Canonical TS gloss string.
        """
        raw_gloss = getattr(synset, "gloss", "") or ""
        examples = getattr(synset, "examples", None)
        return self.extract_gloss(raw_gloss, examples)


# Convenience function for pipeline modules
def extract_gloss_from_synset(synset) -> str:
    return GlossExtractor().extract_from_synset(synset)
