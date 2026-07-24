"""Exploratory InB (Input Basin) memory buffer skeleton.

Focus: deterministic non-semantic canonicalization, bounded intake,
provenance/audit emission, reject-with-code, FIFO order preservation,
clean handoff contract. No inference or truth arbitration.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass, asdict
from typing import Any, Optional


CANONICAL_PROFILE = "v1.0"
SUPPORTED_PROFILES = frozenset({CANONICAL_PROFILE, "v1.1"})
INTAKE_SCHEMA_VERSION = "inb_intake_v1"
WIRE_MAP_VERSION = "inb_wire_v1"
MAX_PAYLOAD_CHARS = 4096
MAX_TOKENS = 512

REASON_CODES = frozenset({
    "MALFORMED_INPUT",
    "UNSUPPORTED_PROFILE",
    "UNSUPPORTED_SCHEMA",
    "UNSUPPORTED_WIRE_MAP",
    "INVALID_FIELD_TYPE",
    "OVERSIZE_PAYLOAD",
    "TOO_MANY_TOKENS",
    "ZERO_EVENT_WINDOW",
    "PROFILE_ACTIVATION_DEFERRED",
    "PROFILE_ACTIVATION_FAILED",
})


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
        if profile not in SUPPORTED_PROFILES:
            raise ValueError(f"unsupported_profile: expected one of {sorted(SUPPORTED_PROFILES)}")
        self.profile = profile
        self._pending_profile: Optional[str] = None

    def _normalize_text(self, text: str) -> str:
        """Purely syntactic, non-semantic canonicalization."""
        text = unicodedata.normalize("NFKC", text)
        text = text.lower().strip()
        text = " ".join(text.split())
        text = re.sub(r"!+", "!", text)
        text = re.sub(r"\?+", "?", text)
        text = re.sub(r"\.+", ".", text)
        return text

    def _check_bounds(self, text: str) -> tuple[bool, Optional[str]]:
        if len(text) > MAX_PAYLOAD_CHARS:
            return False, "OVERSIZE_PAYLOAD"
        token_count = len(text.split())
        if token_count > MAX_TOKENS:
            return False, "TOO_MANY_TOKENS"
        return True, None

    def _validate_schema(self, raw_input: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Schema/wire-map validation (HLR-20.100-004, 016). Returns reject dict or None."""
        schema_version = raw_input.get("schema_version")
        if schema_version is not None and schema_version != INTAKE_SCHEMA_VERSION:
            return self._make_reject(
                raw_input,
                reason_code="UNSUPPORTED_SCHEMA",
                detail=f"expected_{INTAKE_SCHEMA_VERSION}",
            )

        wire_map_version = raw_input.get("wire_map_version")
        if wire_map_version is not None and wire_map_version != WIRE_MAP_VERSION:
            return self._make_reject(
                raw_input,
                reason_code="UNSUPPORTED_WIRE_MAP",
                detail=f"expected_{WIRE_MAP_VERSION}",
            )

        if "content" in raw_input and not isinstance(raw_input["content"], str):
            return self._make_reject(
                raw_input,
                reason_code="INVALID_FIELD_TYPE",
                detail="content_must_be_str",
            )

        return None

    def request_profile_activation(self, profile: str) -> dict[str, Any]:
        """Defer profile activation until safe boundary (HLR-20.100-014, 015)."""
        if profile not in SUPPORTED_PROFILES:
            return {
                "deferred": False,
                "active_profile": self.profile,
                "reason_code": "PROFILE_ACTIVATION_FAILED",
                "detail": "unsupported_profile_version",
            }
        if profile == self.profile:
            return {
                "deferred": False,
                "active_profile": self.profile,
                "reason_code": None,
            }
        self._pending_profile = profile
        return {
            "deferred": True,
            "active_profile": self.profile,
            "pending_profile": profile,
            "reason_code": "PROFILE_ACTIVATION_DEFERRED",
        }

    def apply_safe_boundary(self) -> dict[str, Any]:
        """Apply deferred profile at deterministic safe boundary."""
        if self._pending_profile:
            self.profile = self._pending_profile
            self._pending_profile = None
        return {"active_profile": self.profile, "pending_profile": self._pending_profile}

    def normalize(self, raw_input: dict[str, Any]) -> dict[str, Any]:
        """Ingest, validate, canonicalize, emit provenance + handoff object."""
        if not isinstance(raw_input, dict):
            return self._make_reject(
                raw_input or {},
                reason_code="MALFORMED_INPUT",
                detail="input_must_be_dict",
            )

        schema_reject = self._validate_schema(raw_input)
        if schema_reject is not None:
            return schema_reject

        content = str(raw_input.get("content", ""))
        source = raw_input.get("source", "unknown")
        intake_order = raw_input.get("intake_order", 0)
        requested_profile = raw_input.get("profile")
        timestamp = raw_input.get("timestamp")

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
        provenance: dict[str, Any] = {
            "source": source,
            "profile": self.profile,
            "intake_order": intake_order,
            "outcome": "accepted",
            "reason_code": None,
            "schema_version": INTAKE_SCHEMA_VERSION,
        }
        if timestamp is not None:
            provenance["timestamp"] = timestamp

        metadata: dict[str, Any] = {
            "original_length": len(content),
            "token_count": len(content.split()),
            "intake_order": intake_order,
        }
        if self._pending_profile is not None:
            metadata["profile_activation_deferred"] = True
            metadata["pending_profile"] = self._pending_profile

        output = InBOutput(
            canonical_content=canonical,
            provenance=provenance,
            metadata=metadata,
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
        assert reason_code in REASON_CODES, f"unknown_reason_code: {reason_code}"
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

    def process_tick_intake(self, raw_inputs: list[dict[str, Any]]) -> dict[str, Any]:
        """Process a tick intake window; handle zero-event semantics (HLR-20.100-023)."""
        if not raw_inputs:
            provenance = {
                "outcome": "empty_window",
                "reason_code": "ZERO_EVENT_WINDOW",
                "profile": self.profile,
                "event_count": 0,
            }
            return {
                "events": [],
                "zero_event": True,
                "provenance": provenance,
                "state_digest": _canonical_digest(
                    {"zero_event": True, "reason_code": "ZERO_EVENT_WINDOW", "provenance": provenance}
                ),
            }
        events = self.batch_normalize(raw_inputs)
        return {"events": events, "zero_event": False, "provenance": {"event_count": len(events)}}

    def export_intake_diagnostics(self, outputs: list[dict[str, Any]]) -> str:
        """Deterministic diagnostic export (HLR-20.100-022)."""
        records = []
        for out in outputs:
            records.append(
                {
                    "intake_order": out.get("metadata", {}).get("intake_order"),
                    "outcome": out.get("provenance", {}).get("outcome"),
                    "reason_code": out.get("provenance", {}).get("reason_code"),
                    "source": out.get("provenance", {}).get("source"),
                }
            )
        records.sort(key=lambda r: (r.get("intake_order") is None, r.get("intake_order", 0)))
        return json.dumps(records, sort_keys=True, separators=(",", ":"))


def run_first_stage(
    inb: InB, raw_input: dict[str, Any], mtp_snapshot: dict[str, Any]
) -> dict[str, Any]:
    """InB first-stage tick boundary helper (HLR-20.100-019, 10.10.10)."""
    mtp_before = copy.deepcopy(mtp_snapshot)
    output = inb.normalize(raw_input)
    mtp_after = copy.deepcopy(mtp_snapshot)
    return {
        "output": output,
        "mtp_unchanged": mtp_before == mtp_after,
        "handoff_emitted": "handoff" in output and output.get("provenance", {}).get("outcome") == "accepted",
        "downstream_invoked": False,
        "stage": "inb_surface_norm",
    }
