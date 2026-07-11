"""
identity_anchor_generator.py
----------------------------

Deterministic identity anchor generation for the TS Path A
dictionary_conversion_pipeline.

Responsibilities:
    • Consume routing signatures (primitive_code + feature_codes + tag_codes)
    • Produce stable identity anchors for TS Path A runtime layers
    • Provide identity anchors for downstream modules:
        ts_entry_builder

Identity anchors are:
    • deterministic
    • bounded
    • non-semantic
    • derived from routing signatures
    • used to stabilize meaning across contexts (IdOB → SSR)
"""

from dataclasses import dataclass
from typing import List
from routing_signature_generator import RoutingSignature


@dataclass(frozen=True)
class IdentityAnchor:
    """
    Identity anchor for TS Path A.

    Fields:
        anchor_vector : List[int]
            Deterministic vector derived from routing signature.
        checksum : int
            Bounded checksum for quick identity verification.
    """
    anchor_vector: List[int]
    checksum: int


class IdentityAnchorGenerator:
    """
    Rule-based identity anchor generator.

    Strategy:
        • Concatenate routing signature components
        • Apply deterministic compression
        • Compute bounded checksum
    """

    def generate(self, signature: RoutingSignature) -> IdentityAnchor:
        """
        Generate an identity anchor from a routing signature.

        Parameters
        ----------
        signature : RoutingSignature

        Returns
        -------
        IdentityAnchor
        """
        # 1. Build anchor vector
        anchor_vector = (
            [signature.primitive_code]
            + signature.feature_codes
            + signature.tag_codes
        )

        # 2. Compute bounded checksum
        checksum = self._compute_checksum(anchor_vector)

        return IdentityAnchor(
            anchor_vector=anchor_vector,
            checksum=checksum,
        )

    # ------------------------------------------------------------------ #
    # Checksum                                                           #
    # ------------------------------------------------------------------ #

    def _compute_checksum(self, vector: List[int]) -> int:
        """
        Deterministic bounded checksum.

        Uses a simple rolling hash modulo a fixed bound.
        """
        total = 0
        for v in vector:
            total = (total * 131 + v) % 1_000_000
        return total


# Convenience function for pipeline modules
def generate_identity_anchor(signature: RoutingSignature) -> IdentityAnchor:
    return IdentityAnchorGenerator().generate(signature)
