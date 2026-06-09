"""Deterministic Conversation Object Basin (COB) prototype for 40.110.

This module is intentionally JSON-first and side-effect isolated to support
replayable verification in harness.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
import json


MODULE_NAME = "40.110_cob_prototypes"
CONTRACT_VERSION = "1.0"

EVENT_PROMOTE = "promote"
EVENT_DEPRECATE = "deprecate"
EVENT_MERGE = "merge"
EVENT_SPLIT = "split"
EVENT_COMPACT = "compact"
EVENT_REPLAY_MODE_CHANGE = "replay_mode_change"
EVENT_EXPORT = "export"

SUPPORTED_EVENTS = {
    EVENT_PROMOTE,
    EVENT_DEPRECATE,
    EVENT_MERGE,
    EVENT_SPLIT,
    EVENT_COMPACT,
    EVENT_REPLAY_MODE_CHANGE,
    EVENT_EXPORT,
}

REPLAY_MODES = {"full", "windowed", "summary_proof"}
SUPPORTED_PROFILE_SIGNATURES = {"P1", "P2"}

REASON_UNSUPPORTED_EVENT = "COB_RSN_001_UNSUPPORTED_EVENT"
REASON_SEQUENCE_VIOLATION = "COB_RSN_002_SEQUENCE_VIOLATION"
REASON_SAFE_BOUNDARY_REQUIRED = "COB_RSN_003_SAFE_BOUNDARY_REQUIRED"
REASON_UNSUPPORTED_REPLAY_MODE = "COB_RSN_004_UNSUPPORTED_REPLAY_MODE"
REASON_UNSUPPORTED_PROFILE = "COB_RSN_005_UNSUPPORTED_PROFILE"
REASON_INVALID_LIFECYCLE = "COB_RSN_006_INVALID_LIFECYCLE"


class COBDeterministicReject(ValueError):
    """Raised when input violates deterministic COB contracts."""

    def __init__(self, reason_code: str, message: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(payload: dict[str, Any]) -> str:
    return sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _require_non_empty_str(field_name: str, value: Any) -> str:
    if not isinstance(value, str):
        raise COBDeterministicReject(REASON_INVALID_LIFECYCLE, f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise COBDeterministicReject(REASON_INVALID_LIFECYCLE, f"{field_name} must be non-empty")
    return normalized


def _require_bool(field_name: str, value: Any) -> bool:
    if not isinstance(value, bool):
        raise COBDeterministicReject(REASON_INVALID_LIFECYCLE, f"{field_name} must be bool")
    return value


def _require_int(field_name: str, value: Any, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise COBDeterministicReject(REASON_INVALID_LIFECYCLE, f"{field_name} must be int")
    if value < minimum:
        raise COBDeterministicReject(REASON_INVALID_LIFECYCLE, f"{field_name} must be >= {minimum}")
    return value


def _ensure_list_of_strings(field_name: str, value: Any) -> list[str]:
    if not isinstance(value, list):
        raise COBDeterministicReject(REASON_INVALID_LIFECYCLE, f"{field_name} must be a list")
    normalized: list[str] = []
    for item in value:
        normalized.append(_require_non_empty_str(field_name, item))
    return normalized


@dataclass(slots=True)
class AuditRecord:
    sequence: int
    event_type: str
    status: str
    reason_code: str
    lifecycle_state: str
    replay_mode: str
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "event_type": self.event_type,
            "status": self.status,
            "reason_code": self.reason_code,
            "lifecycle_state": self.lifecycle_state,
            "replay_mode": self.replay_mode,
            "details": self.details,
        }


@dataclass(slots=True)
class COBState:
    cob_id: str
    profile_signature: str
    replay_mode: str
    sequence: int = 0
    lifecycle_state: str = "provisional"
    lineage: dict[str, Any] = field(default_factory=dict)
    exports: list[dict[str, Any]] = field(default_factory=list)
    audit_log: list[AuditRecord] = field(default_factory=list)
    summary_proof: str = ""
    cob_snapshot_pin: dict[str, Any] | None = None
    usp_pin_lineage: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.cob_id = _require_non_empty_str("cob_id", self.cob_id)
        self.profile_signature = _require_non_empty_str("profile_signature", self.profile_signature)
        if self.profile_signature not in SUPPORTED_PROFILE_SIGNATURES:
            raise COBDeterministicReject(REASON_UNSUPPORTED_PROFILE, "profile_signature is unsupported")
        self.replay_mode = _require_non_empty_str("replay_mode", self.replay_mode)
        if self.replay_mode not in REPLAY_MODES:
            raise COBDeterministicReject(REASON_UNSUPPORTED_REPLAY_MODE, "replay_mode is unsupported")
        self.sequence = _require_int("sequence", self.sequence, minimum=0)
        if not self.lineage:
            self.lineage = {
                "stable_id": self.cob_id,
                "parent_ids": [],
                "merge_sources": [],
                "split_children": [],
                "winner_lineage": None,
            }
        self._append_audit(
            sequence=self.sequence,
            event_type="create",
            status="ACCEPT",
            reason_code="COB_OK_000_CREATED",
            details={"contract_version": CONTRACT_VERSION},
        )

    def apply_event(self, event: dict[str, Any]) -> dict[str, Any]:
        event_type = _require_non_empty_str("event_type", event.get("event_type"))
        requested_sequence = _require_int("sequence", event.get("sequence"), minimum=1)
        safe_boundary = _require_bool("safe_boundary", event.get("safe_boundary"))
        payload = event.get("payload", {})
        if payload is None:
            payload = {}
        if not isinstance(payload, dict):
            self._reject(requested_sequence, event_type, REASON_INVALID_LIFECYCLE, "payload must be an object")

        if requested_sequence != self.sequence + 1:
            self._reject(requested_sequence, event_type, REASON_SEQUENCE_VIOLATION, "sequence must increment by one")

        if event_type not in SUPPORTED_EVENTS:
            self._reject(requested_sequence, event_type, REASON_UNSUPPORTED_EVENT, "unsupported event type")

        if not safe_boundary:
            self._reject(requested_sequence, event_type, REASON_SAFE_BOUNDARY_REQUIRED, "safe boundary required")

        if event_type == EVENT_PROMOTE:
            self._apply_promote(requested_sequence, event_type, payload)
        elif event_type == EVENT_DEPRECATE:
            self._apply_deprecate(requested_sequence, event_type, payload)
        elif event_type == EVENT_MERGE:
            self._apply_merge(requested_sequence, event_type, payload)
        elif event_type == EVENT_SPLIT:
            self._apply_split(requested_sequence, event_type, payload)
        elif event_type == EVENT_COMPACT:
            self._apply_compact(requested_sequence, event_type)
        elif event_type == EVENT_REPLAY_MODE_CHANGE:
            self._apply_replay_mode_change(requested_sequence, event_type, payload)
        elif event_type == EVENT_EXPORT:
            self._apply_export(requested_sequence, event_type, payload)

        self.sequence = requested_sequence
        return self.snapshot()

    def pin_usp_snapshot(
        self,
        *,
        sequence: int,
        usp_version_id: int,
        usp_version_ref: str,
        safe_boundary: bool = True,
    ) -> dict[str, Any]:
        """W2: record active usp_version_ref pin per 20.102-010 / 20.031-027."""
        if not safe_boundary:
            self._reject(sequence, "usp_pin", REASON_SAFE_BOUNDARY_REQUIRED, "safe boundary required for usp pin")
        ref = _require_non_empty_str("usp_version_ref", usp_version_ref)
        vid = _require_int("usp_version_id", usp_version_id, minimum=1)
        if sequence != self.sequence + 1:
            self._reject(sequence, "usp_pin", REASON_SEQUENCE_VIOLATION, "sequence must increment by one")
        pin = {"usp_version_id": vid, "usp_version_ref": ref, "cob_id": self.cob_id}
        self.cob_snapshot_pin = pin
        self.usp_pin_lineage.append({**pin, "sequence": sequence})
        self.sequence = sequence
        self._append_audit(
            sequence=sequence,
            event_type="usp_pin",
            status="ACCEPT",
            reason_code="COB_OK_108_USP_PIN",
            details=pin,
        )
        return self.snapshot()

    def snapshot(self) -> dict[str, Any]:
        body = {
            "module": MODULE_NAME,
            "contract_version": CONTRACT_VERSION,
            "cob_id": self.cob_id,
            "sequence": self.sequence,
            "lifecycle_state": self.lifecycle_state,
            "replay_mode": self.replay_mode,
            "profile_signature": self.profile_signature,
            "lineage": {
                "stable_id": self.lineage["stable_id"],
                "parent_ids": list(self.lineage["parent_ids"]),
                "merge_sources": list(self.lineage["merge_sources"]),
                "split_children": list(self.lineage["split_children"]),
                "winner_lineage": self.lineage["winner_lineage"],
            },
            "summary_proof": self.summary_proof,
            "exports": list(self.exports),
            "cob_snapshot_pin": self.cob_snapshot_pin,
            "usp_pin_lineage": list(self.usp_pin_lineage),
            "audit_log": [record.as_dict() for record in self.audit_log],
        }
        body["verification_digest"] = _digest(body)
        return body

    def _apply_promote(self, sequence: int, event_type: str, payload: dict[str, Any]) -> None:
        if self.lifecycle_state not in {"provisional"}:
            self._reject(sequence, event_type, REASON_INVALID_LIFECYCLE, "promotion requires provisional state")
        winner_lineage = _require_non_empty_str("winner_lineage", payload.get("winner_lineage"))
        self.lineage["winner_lineage"] = winner_lineage
        self.lifecycle_state = "active"
        self._append_audit(sequence, event_type, "ACCEPT", "COB_OK_101_PROMOTED", {"winner_lineage": winner_lineage})

    def _apply_deprecate(self, sequence: int, event_type: str, payload: dict[str, Any]) -> None:
        reason = _require_non_empty_str("reason", payload.get("reason", "deprecated"))
        if self.lifecycle_state in {"deprecated"}:
            self._reject(sequence, event_type, REASON_INVALID_LIFECYCLE, "already deprecated")
        self.lifecycle_state = "deprecated"
        self._append_audit(sequence, event_type, "ACCEPT", "COB_OK_102_DEPRECATED", {"reason": reason})

    def _apply_merge(self, sequence: int, event_type: str, payload: dict[str, Any]) -> None:
        sources = _ensure_list_of_strings("merge_sources", payload.get("merge_sources"))
        self.lineage["merge_sources"] = sorted(set(self.lineage["merge_sources"] + sources))
        self._append_audit(sequence, event_type, "ACCEPT", "COB_OK_103_MERGED", {"merge_sources": list(sources)})

    def _apply_split(self, sequence: int, event_type: str, payload: dict[str, Any]) -> None:
        children = _ensure_list_of_strings("split_children", payload.get("split_children"))
        self.lineage["split_children"] = sorted(set(self.lineage["split_children"] + children))
        self._append_audit(sequence, event_type, "ACCEPT", "COB_OK_104_SPLIT", {"split_children": list(children)})

    def _apply_compact(self, sequence: int, event_type: str) -> None:
        proof_payload = {
            "cob_id": self.cob_id,
            "sequence": sequence,
            "lineage": self.lineage,
            "lifecycle_state": self.lifecycle_state,
        }
        self.summary_proof = f"proof:{_digest(proof_payload)}"
        self._append_audit(sequence, event_type, "ACCEPT", "COB_OK_105_COMPACTED", {"summary_proof": self.summary_proof})

    def _apply_replay_mode_change(self, sequence: int, event_type: str, payload: dict[str, Any]) -> None:
        replay_mode = _require_non_empty_str("replay_mode", payload.get("replay_mode"))
        if replay_mode not in REPLAY_MODES:
            self._reject(sequence, event_type, REASON_UNSUPPORTED_REPLAY_MODE, "unsupported replay_mode")
        self.replay_mode = replay_mode
        self._append_audit(sequence, event_type, "ACCEPT", "COB_OK_106_REPLAY_MODE", {"replay_mode": replay_mode})

    def _apply_export(self, sequence: int, event_type: str, payload: dict[str, Any]) -> None:
        # Profile precedence is signature-bound: environment defaults are never selected over active signature.
        window_events = _require_int("window_events", payload.get("window_events", 0), minimum=0)
        manifest = {
            "cob_id": self.cob_id,
            "sequence": sequence,
            "replay_mode": self.replay_mode,
            "profile_signature": self.profile_signature,
            "env_default_profile": payload.get("env_default_profile"),
            "window_events": window_events,
            "empty_artifact": window_events == 0,
            "container": "json",
            "compression": "none",
            "manifest_version": "1.0",
        }
        manifest["manifest_digest"] = _digest(manifest)
        self.exports.append(manifest)
        self._append_audit(sequence, event_type, "ACCEPT", "COB_OK_107_EXPORTED", manifest)

    def _append_audit(
        self,
        sequence: int,
        event_type: str,
        status: str,
        reason_code: str,
        details: dict[str, Any],
    ) -> None:
        self.audit_log.append(
            AuditRecord(
                sequence=sequence,
                event_type=event_type,
                status=status,
                reason_code=reason_code,
                lifecycle_state=self.lifecycle_state,
                replay_mode=self.replay_mode,
                details=details,
            )
        )

    def _reject(self, sequence: int, event_type: str, reason_code: str, message: str) -> None:
        self._append_audit(
            sequence=sequence,
            event_type=event_type,
            status="REJECT",
            reason_code=reason_code,
            details={"message": message},
        )
        raise COBDeterministicReject(reason_code, message)
