"""Exploratory InB (Input Basin) memory buffer skeleton.

Focus: deterministic non-semantic canonicalization, bounded intake,
provenance/audit emission, reject-with-code, FIFO order preservation,
clean handoff contract. No inference or truth arbitration.
"""

from __future__ import annotations
import hashlib
import json
import unicodedata
from dataclasses import dataclass, asdict
from typing import Any, Optional


CANONICAL_PROFILE = "v1.0"
MAX_PAYLOAD_CHARS = 4096
MAX_TOKENS = 512


def _canonical_digest(payload: dict[str, Any]) -> str:
    """Deterministic digest for replay verification."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass
class InBOutput:
    canonical_content: Optional[str]
    provenance: dict[str, Any]
    metadata: dict[str, Any]


class InB:
    """Deterministic Input Basin skeleton for memory buffer exploration."""

    def __init__(self, profile: str = CANONICAL_PROFILE):
        if profile != CANONICAL_PROFILE:
            raise ValueError(f"unsupported_profile: expected {CANONICAL_PROFILE}")
        self.profile = profile

    def _normalize_text(self, text: str) -> str:
        """Purely syntactic, non-semantic canonicalization."""
        import re
        # Unicode normalization (NFKC for compatibility)
        text = unicodedata.normalize("NFKC", text)
        # Lowercase, strip whitespace
        text = text.lower().strip()
        # Collapse multiple whitespace
        text = " ".join(text.split())
        # Collapse repeated punctuation (deterministic, still non-semantic)
        text = re.sub(r'!+', '!', text)
        text = re.sub(r'\?+', '?', text)
        text = re.sub(r'\.+', '.', text)
        return text

    def _check_bounds(self, text: str) -> tuple[bool, Optional[str]]:
        if len(text) > MAX_PAYLOAD_CHARS:
            return False, "OVERSIZE_PAYLOAD"
        token_count = len(text.split())
        if token_count > MAX_TOKENS:
            return False, "TOO_MANY_TOKENS"
        return True, None

    def normalize(self, raw_input: dict[str, Any]) -> dict[str, Any]:
        """Ingest, validate, canonicalize, emit provenance + handoff object."""
        if not isinstance(raw_input, dict):
            return self._make_reject(
                raw_input or {},
                reason_code="MALFORMED_INPUT",
                detail="input_must_be_dict",
            )

        content = str(raw_input.get("content", ""))
        source = raw_input.get("source", "unknown")
        intake_order = raw_input.get("intake_order", 0)
        requested_profile = raw_input.get("profile")

        # Profile check (HLR-20.100-013 / 016)
        if requested_profile and requested_profile != self.profile:
            return self._make_reject(
                raw_input,
                reason_code="UNSUPPORTED_PROFILE",
                detail=f"expected_{self.profile}",
            )

        ok, reason = self._check_bounds(content)
        if not ok:
            return self._make_reject(
                raw_input, reason_code=reason, detail="exceeded_limit"
            )

        # Core canonicalization (no semantic work)
        canonical = self._normalize_text(content)

        # Provenance (HLR-20.100-011, 012)
        provenance = {
            "source": source,
            "profile": self.profile,
            "intake_order": intake_order,
            "outcome": "accepted",
            "reason_code": None,
        }

        output = InBOutput(
            canonical_content=canonical,
            provenance=provenance,
            metadata={
                "original_length": len(content),
                "token_count": len(content.split()),
                "intake_order": intake_order,
            },
        )

        result = asdict(output)
        result["state_digest"] = _canonical_digest(
            {
                "content": canonical,
                "provenance": provenance,
                "metadata": result["metadata"],
            }
        )
        # Handoff contract: InB -> IIInB -> RB (HLR-20.100-020, 20.101-003)
        result["handoff"] = {
            "contract_version": "inb_to_iiinb_v1",
            "next_stage": "input_semantic_repair",
            "downstream_after_repair": "routing",
            "ordering": ["inb_surface_norm", "input_semantic_repair", "routing"],
        }
        return result

    def _make_reject(
        self, raw_input: dict[str, Any], reason_code: str, detail: str
    ) -> dict[str, Any]:
        source = raw_input.get("source", "unknown") if isinstance(raw_input, dict) else "unknown"
        intake_order = raw_input.get("intake_order", 0) if isinstance(raw_input, dict) else 0

        provenance = {
            "source": source,
            "profile": self.profile,
            "intake_order": intake_order,
            "outcome": "rejected",
            "reason_code": reason_code,
            "detail": detail,
        }

        output = InBOutput(
            canonical_content=None,
            provenance=provenance,
            metadata={"rejected": True, "intake_order": intake_order},
        )

        result = asdict(output)
        result["state_digest"] = _canonical_digest(
            {"outcome": "rejected", "reason_code": reason_code, "provenance": provenance}
        )
        return result

    def batch_normalize(self, raw_inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Process multiple inputs preserving FIFO order (HLR-20.100-006)."""
        results = []
        for i, raw in enumerate(raw_inputs):
            if isinstance(raw, dict) and "intake_order" not in raw:
                raw = dict(raw)
                raw["intake_order"] = i
            results.append(self.normalize(raw))
        return results
