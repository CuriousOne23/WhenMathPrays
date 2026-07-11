"""
lemma_normalizer.py
-------------------

Deterministic lemma normalization for the TS Path A
dictionary_conversion_pipeline.

Responsibilities:
    • Convert raw WordNet lemmas into canonical TS lemmas
    • Enforce stable, reproducible normalization rules
    • Remove WordNet artifacts (underscores, parentheticals, sense tags)
    • Provide pure functions suitable for unit testing
    • Serve as the normalization layer for all downstream modules:
        gloss_extractor, primitive_classifier, invariant_generator,
        cue_envelope_generator, routing_signature_generator,
        identity_anchor_generator, ts_entry_builder

This module performs *no* semantic interpretation. It is strictly lexical.
"""

import re
from typing import List


class LemmaNormalizer:
    """
    Canonical lemma normalization for TS Path A.

    All normalization rules must be:
        • deterministic
        • reversible only in the forward direction
        • stable across pipeline runs
        • independent of downstream semantics
    """

    # Regex patterns for cleanup
    _PAREN_PATTERN = re.compile(r"\([^)]*\)")
    _SENSE_PATTERN = re.compile(r"\b\d+$")  # trailing sense numbers
    _MULTISPACE_PATTERN = re.compile(r"\s+")

    def normalize(self, lemma: str) -> str:
        """
        Normalize a single lemma into TS canonical form.

        Steps:
            1. Lowercase
            2. Replace underscores with spaces
            3. Remove parenthetical artifacts (WordNet gloss hints)
            4. Remove trailing sense numbers (e.g., 'bank_1')
            5. Strip punctuation artifacts
            6. Collapse whitespace
            7. Return deterministic TS lemma

        Parameters
        ----------
        lemma : str
            Raw lemma from WordNet synset.

        Returns
        -------
        str
            Canonical TS lemma.
        """

        if not lemma:
            return ""

        # 1. Lowercase
        lemma = lemma.lower()

        # 2. Replace underscores with spaces
        lemma = lemma.replace("_", " ")

        # 3. Remove parenthetical artifacts
        lemma = self._PAREN_PATTERN.sub("", lemma)

        # 4. Remove trailing sense numbers
        lemma = self._SENSE_PATTERN.sub("", lemma)

        # 5. Remove stray punctuation (except hyphens inside words)
        lemma = re.sub(r"[^\w\s\-]", "", lemma)

        # 6. Collapse whitespace
        lemma = self._MULTISPACE_PATTERN.sub(" ", lemma).strip()

        return lemma

    def normalize_list(self, lemmas: List[str]) -> List[str]:
        """
        Normalize a list of lemmas.

        Pure function: no side effects.

        Parameters
        ----------
        lemmas : List[str]

        Returns
        -------
        List[str]
        """
        return [self.normalize(l) for l in lemmas]


# Convenience function for pipeline modules
def normalize_lemma(lemma: str) -> str:
    return LemmaNormalizer().normalize(lemma)
