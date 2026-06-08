"""Deterministic Conversation Integration Layer (CIL) prototype for 40.33."""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
import json


MODULE_NAME = "40.33_cil_prototypes"
CONTRACT_VERSION = "1.0"

EVENT_INGEST = "ingest"
EVENT_PROCESS_NEXT = "process_next"
EVENT_GB_RESPONSE = "gb_response"
EVENT_PROFILE_CHANGE = "profile_change"

SUPPORTED_EVENTS = {EVENT_INGEST, EVENT_PROCESS_NEXT, EVENT_GB_RESPONSE, EVENT_PROFILE_CHANGE}
SUPPORTED_PROFILES = {"P1", "P2"}
SUPPORTED_DECISIONS = {"approve", "deny", "timeout", "late_approve"}

REASON_UNSUPPORTED_EVENT = "CIL_RSN_001_UNSUPPORTED_EVENT"
REASON_SEQUENCE_VIOLATION = "CIL_RSN_002_SEQUENCE_VIOLATION"
REASON_SAFE_BOUNDARY_REQUIRED = "CIL_RSN_003_SAFE_BOUNDARY_REQUIRED"
REASON_UNSUPPORTED_PROFILE = "CIL_RSN_004_UNSUPPORTED_PROFILE"
REASON_UNSUPPORTED_ENUM = "CIL_RSN_005_UNSUPPORTED_ENUM"
REASON_DIRECT_INQUIRY_BYPASS = "CIL_RSN_006_DIRECT_INQUIRY_BYPASS"
REASON_INVALID_PACKET = "CIL_RSN_007_INVALID_PACKET"


class CILDeterministicReject(ValueError):
    """Raised when deterministic CIL contracts are violated."""

    def __init__(self, reason_code: str, message: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(payload: dict[str, Any]) -> str:
    return sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _require_non_empty_str(field_name: str, value: Any) -> str:
    if not isinstance(value, str):
        raise CILDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise CILDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be non-empty")
    return normalized


def _require_int(field_name: str, value: Any, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise CILDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be int")
    if value < minimum:
        raise CILDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be >= {minimum}")
    return value


def _require_bool(field_name: str, value: Any) -> bool:
    if not isinstance(value, bool):
        raise CILDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be bool")
    return value


def _require_float01(field_name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CILDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be numeric")
    fv = float(value)
    if fv < 0.0 or fv > 1.0:
        raise CILDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be in [0,1]")
    return fv


def _profile_threshold(profile: str) -> float:
    return 0.75 if profile == "P1" else 0.65


@dataclass(slots=True)
class AuditRecord:
    sequence: int
    event_type: str
    status: str
    reason_code: str
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "event_type": self.event_type,
            "status": self.status,
            "reason_code": self.reason_code,
            "details": self.details,
        }


@dataclass(slots=True)
class CILState:
    active_profile: str
    env_default_profile: str = "P2"
    sequence: int = 0
    pending_queue: list[dict[str, Any]] = field(default_factory=list)
    escalation_requests: list[dict[str, Any]] = field(default_factory=list)
    integrated_packets: list[dict[str, Any]] = field(default_factory=list)
    audit_log: list[AuditRecord] = field(default_factory=list)
    clarification_events: list[dict[str, Any]] = field(default_factory=list)
    _integration_seq: int = 0

    def __post_init__(self) -> None:
        self.active_profile = _require_non_empty_str("active_profile", self.active_profile)
        self.env_default_profile = _require_non_empty_str("env_default_profile", self.env_default_profile)
        if self.active_profile not in SUPPORTED_PROFILES:
            raise CILDeterministicReject(REASON_UNSUPPORTED_PROFILE, "active_profile unsupported")
        if self.env_default_profile not in SUPPORTED_PROFILES:
            raise CILDeterministicReject(REASON_UNSUPPORTED_PROFILE, "env_default_profile unsupported")
        self.sequence = _require_int("sequence", self.sequence, minimum=0)
        self._append_audit(
            sequence=self.sequence,
            event_type="create",
            status="ACCEPT",
            reason_code="CIL_OK_000_CREATED",
            details={"contract_version": CONTRACT_VERSION},
        )

    def apply_event(self, event: dict[str, Any]) -> dict[str, Any]:
        event_type = _require_non_empty_str("event_type", event.get("event_type"))
        next_sequence = _require_int("sequence", event.get("sequence"), minimum=1)

        if next_sequence != self.sequence + 1:
            self._reject(next_sequence, event_type, REASON_SEQUENCE_VIOLATION, "sequence must increment by one")
        if event_type not in SUPPORTED_EVENTS:
            self._reject(next_sequence, event_type, REASON_UNSUPPORTED_EVENT, "unsupported event")

        safe_boundary = _require_bool("safe_boundary", event.get("safe_boundary"))
        if event_type in {EVENT_PROCESS_NEXT, EVENT_GB_RESPONSE, EVENT_PROFILE_CHANGE} and not safe_boundary:
            self._reject(next_sequence, event_type, REASON_SAFE_BOUNDARY_REQUIRED, "safe boundary required")

        payload = event.get("payload", {})
        if payload is None:
            payload = {}
        if not isinstance(payload, dict):
            self._reject(next_sequence, event_type, REASON_INVALID_PACKET, "payload must be object")

        if event_type == EVENT_INGEST:
            self._apply_ingest(next_sequence, payload)
        elif event_type == EVENT_PROCESS_NEXT:
            self._apply_process_next(next_sequence)
        elif event_type == EVENT_GB_RESPONSE:
            self._apply_gb_response(next_sequence, payload)
        elif event_type == EVENT_PROFILE_CHANGE:
            self._apply_profile_change(next_sequence, payload)

        self.sequence = next_sequence
        return self.snapshot()

    def snapshot(self) -> dict[str, Any]:
        body = {
            "module": MODULE_NAME,
            "contract_version": CONTRACT_VERSION,
            "active_profile": self.active_profile,
            "env_default_profile": self.env_default_profile,
            "sequence": self.sequence,
            "pending_queue": list(self.pending_queue),
            "escalation_requests": list(self.escalation_requests),
            "integrated_packets": list(self.integrated_packets),
            "audit_log": [record.as_dict() for record in self.audit_log],
        }
        body["clarification_events"] = list(self.clarification_events)
        body["verification_digest"] = _digest(body)
        return body

    def emit_clarification_event(
        self,
        *,
        sequence: int,
        escalation_ref: str,
        pattern: str,
        expansion: str,
        scope: str = "conversation",
    ) -> dict[str, Any]:
        """W2: emit clarification_event for UPI FIFO consume (20.032-027–030)."""
        if not pattern or not expansion or not scope:
            self._reject(sequence, "clarification_emit", REASON_INVALID_PACKET, "incomplete clarification payload")
        self._integration_seq += 1
        event = {
            "schema_version": "clarification_event_v1",
            "event_id": f"clar-{escalation_ref}",
            "integration_seq": self._integration_seq,
            "pattern": pattern,
            "expansion": expansion,
            "scope": scope,
            "source": "CIL",
            "escalation_ref": escalation_ref,
        }
        self.clarification_events.append(event)
        self._append_audit(
            sequence=sequence,
            event_type="clarification_emit",
            status="ACCEPT",
            reason_code="CIL_OK_110_CLARIFICATION_EVENT",
            details={"event_id": event["event_id"], "integration_seq": event["integration_seq"]},
        )
        return event

    def _apply_ingest(self, sequence: int, payload: dict[str, Any]) -> None:
        packet_id = _require_non_empty_str("packet_id", payload.get("packet_id"))
        snapshot_id = _require_non_empty_str("snapshot_id", payload.get("snapshot_id"))
        confidence = _require_float01("confidence", payload.get("confidence"))

        if payload.get("request_channel") == "direct_inquiry":
            self._reject(sequence, EVENT_INGEST, REASON_DIRECT_INQUIRY_BYPASS, "direct inquiry bypass prohibited")

        packet = {
            "packet_id": packet_id,
            "snapshot_id": snapshot_id,
            "confidence": confidence,
            "ingest_sequence": sequence,
        }
        self.pending_queue.append(packet)
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_INGEST,
            status="ACCEPT",
            reason_code="CIL_OK_101_INGESTED",
            details={"packet_id": packet_id, "snapshot_id": snapshot_id},
        )

    def _apply_process_next(self, sequence: int) -> None:
        if not self.pending_queue:
            self._append_audit(
                sequence=sequence,
                event_type=EVENT_PROCESS_NEXT,
                status="ACCEPT",
                reason_code="CIL_OK_102_NOOP_EMPTY_QUEUE",
                details={"note": "empty queue"},
            )
            return

        packet = self.pending_queue.pop(0)
        threshold = _profile_threshold(self.active_profile)
        confidence = float(packet["confidence"])

        if confidence > threshold:
            outcome = "integrate"
        elif confidence < threshold:
            outcome = "escalate"
        else:
            outcome = "fallback_integrate" if _digest({"packet_id": packet["packet_id"]})[-1] in "02468ace" else "escalate"

        if outcome in {"integrate", "fallback_integrate"}:
            self.integrated_packets.append(
                {
                    "packet_id": packet["packet_id"],
                    "snapshot_id": packet["snapshot_id"],
                    "classification": outcome,
                    "profile": self.active_profile,
                }
            )
            self._append_audit(
                sequence=sequence,
                event_type=EVENT_PROCESS_NEXT,
                status="ACCEPT",
                reason_code="CIL_OK_103_INTEGRATED",
                details={"packet_id": packet["packet_id"], "classification": outcome},
            )
            return

        request = {
            "request_id": f"escalate:{_digest({'packet_id': packet['packet_id'], 'sequence': sequence})[:12]}",
            "packet_id": packet["packet_id"],
            "snapshot_id": packet["snapshot_id"],
            "status": "pending",
            "default_on_timeout": "deny",
            "reentry_policy": "queue",
        }
        self.escalation_requests.append(request)
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_PROCESS_NEXT,
            status="ACCEPT",
            reason_code="CIL_OK_104_ESCALATED_TO_GB",
            details={"request_id": request["request_id"], "packet_id": packet["packet_id"]},
        )

    def _apply_gb_response(self, sequence: int, payload: dict[str, Any]) -> None:
        request_id = _require_non_empty_str("request_id", payload.get("request_id"))
        decision = _require_non_empty_str("decision", payload.get("decision"))
        if decision not in SUPPORTED_DECISIONS:
            self._reject(sequence, EVENT_GB_RESPONSE, REASON_UNSUPPORTED_ENUM, "unsupported decision enum")

        matched = None
        for item in self.escalation_requests:
            if item["request_id"] == request_id:
                matched = item
                break
        if matched is None:
            self._reject(sequence, EVENT_GB_RESPONSE, REASON_INVALID_PACKET, "request_id not found")

        if decision == "approve":
            matched["status"] = "approved"
            self.integrated_packets.append(
                {
                    "packet_id": matched["packet_id"],
                    "snapshot_id": matched["snapshot_id"],
                    "classification": "gb_approved",
                    "profile": self.active_profile,
                }
            )
            reason = "CIL_OK_105_GB_APPROVED"
        elif decision == "deny":
            matched["status"] = "denied"
            reason = "CIL_OK_106_GB_DENIED"
        elif decision == "timeout":
            matched["status"] = "timeout_default_deny"
            reason = "CIL_OK_107_TIMEOUT_DEFAULT"
        else:
            # late_approve uses deterministic re-entry policy.
            policy = matched.get("reentry_policy", "queue")
            if policy == "queue":
                matched["status"] = "late_approved_queued"
                self.integrated_packets.append(
                    {
                        "packet_id": matched["packet_id"],
                        "snapshot_id": matched["snapshot_id"],
                        "classification": "late_approved_reentry",
                        "profile": self.active_profile,
                    }
                )
            elif policy == "ignore":
                matched["status"] = "late_approved_ignored"
            else:
                matched["status"] = "late_approved_compensate"
            reason = "CIL_OK_108_LATE_APPROVAL_REENTRY"

        self._append_audit(
            sequence=sequence,
            event_type=EVENT_GB_RESPONSE,
            status="ACCEPT",
            reason_code=reason,
            details={"request_id": request_id, "decision": decision, "status": matched["status"]},
        )

    def _apply_profile_change(self, sequence: int, payload: dict[str, Any]) -> None:
        requested = _require_non_empty_str("profile", payload.get("profile"))
        if requested not in SUPPORTED_PROFILES:
            self._reject(sequence, EVENT_PROFILE_CHANGE, REASON_UNSUPPORTED_PROFILE, "unsupported profile")
        self.active_profile = requested
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_PROFILE_CHANGE,
            status="ACCEPT",
            reason_code="CIL_OK_109_PROFILE_CHANGED",
            details={"active_profile": self.active_profile, "env_default_profile": self.env_default_profile},
        )

    def _append_audit(self, sequence: int, event_type: str, status: str, reason_code: str, details: dict[str, Any]) -> None:
        self.audit_log.append(
            AuditRecord(
                sequence=sequence,
                event_type=event_type,
                status=status,
                reason_code=reason_code,
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
        raise CILDeterministicReject(reason_code, message)
