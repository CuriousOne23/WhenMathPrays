"""Deterministic Conversation Coprocessor (COP) prototype for 40.340."""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
import json


MODULE_NAME = "40.340_cop_prototypes"
CONTRACT_VERSION = "1.0"

EVENT_SUBMIT_PROPOSAL = "submit_proposal"
EVENT_GB_DECISION = "gb_decision"
EVENT_COMMIT_READY = "commit_ready"
EVENT_PROFILE_CHANGE = "profile_change"

SUPPORTED_EVENTS = {
    EVENT_SUBMIT_PROPOSAL,
    EVENT_GB_DECISION,
    EVENT_COMMIT_READY,
    EVENT_PROFILE_CHANGE,
}
SUPPORTED_PROFILES = {"P1", "P2"}
SUPPORTED_PRIORITIES = {"normal", "safety_critical"}
SUPPORTED_GB_DECISIONS = {"approve", "reject", "expire"}

REASON_UNSUPPORTED_EVENT = "COP_RSN_001_UNSUPPORTED_EVENT"
REASON_SEQUENCE_VIOLATION = "COP_RSN_002_SEQUENCE_VIOLATION"
REASON_SAFE_BOUNDARY_REQUIRED = "COP_RSN_003_SAFE_BOUNDARY_REQUIRED"
REASON_UNSUPPORTED_PROFILE = "COP_RSN_004_UNSUPPORTED_PROFILE"
REASON_UNSUPPORTED_ENUM = "COP_RSN_005_UNSUPPORTED_ENUM"
REASON_OVERLOAD_REJECT = "COP_RSN_006_OVERLOAD_REJECT"
REASON_INVALID_PACKET = "COP_RSN_007_INVALID_PACKET"
REASON_UNKNOWN_PROPOSAL = "COP_RSN_008_UNKNOWN_PROPOSAL"
REASON_COMMIT_NOT_STAGED = "COP_RSN_009_COMMIT_NOT_STAGED"
REASON_FORBIDDEN_MUTATION = "COP_RSN_010_FORBIDDEN_MUTATION"


class COPDeterministicReject(ValueError):
    """Raised when deterministic COP contracts are violated."""

    def __init__(self, reason_code: str, message: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(payload: dict[str, Any]) -> str:
    return sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _require_non_empty_str(field_name: str, value: Any) -> str:
    if not isinstance(value, str):
        raise COPDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise COPDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be non-empty")
    return normalized


def _require_int(field_name: str, value: Any, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise COPDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be int")
    if value < minimum:
        raise COPDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be >= {minimum}")
    return value


def _require_bool(field_name: str, value: Any) -> bool:
    if not isinstance(value, bool):
        raise COPDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be bool")
    return value


def _require_object(field_name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise COPDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be object")
    return value


def _profile_policy(profile: str) -> dict[str, Any]:
    if profile == "P1":
        return {
            "profile": "P1",
            "fairness_policy": "fifo_strict",
            "overload_policy": "reject_new",
            "max_queue": 2,
        }
    return {
        "profile": "P2",
        "fairness_policy": "safety_first",
        "overload_policy": "preempt_noncritical",
        "max_queue": 2,
    }


def _priority_rank(priority: str) -> int:
    return 0 if priority == "safety_critical" else 1


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
class COPState:
    active_profile: str
    env_default_profile: str = "P1"
    sequence: int = 0
    pending_queue: list[dict[str, Any]] = field(default_factory=list)
    staged_commits: list[dict[str, Any]] = field(default_factory=list)
    visible_commits: list[dict[str, Any]] = field(default_factory=list)
    audit_log: list[AuditRecord] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.active_profile = _require_non_empty_str("active_profile", self.active_profile)
        self.env_default_profile = _require_non_empty_str("env_default_profile", self.env_default_profile)
        if self.active_profile not in SUPPORTED_PROFILES:
            raise COPDeterministicReject(REASON_UNSUPPORTED_PROFILE, "active_profile unsupported")
        if self.env_default_profile not in SUPPORTED_PROFILES:
            raise COPDeterministicReject(REASON_UNSUPPORTED_PROFILE, "env_default_profile unsupported")
        self.sequence = _require_int("sequence", self.sequence, minimum=0)
        self._append_audit(
            sequence=self.sequence,
            event_type="create",
            status="ACCEPT",
            reason_code="COP_OK_000_CREATED",
            details={"contract_version": CONTRACT_VERSION, "policy": self.policy_snapshot()},
        )

    def policy_snapshot(self) -> dict[str, Any]:
        return _profile_policy(self.active_profile)

    def apply_event(self, event: dict[str, Any]) -> dict[str, Any]:
        event_type = _require_non_empty_str("event_type", event.get("event_type"))
        next_sequence = _require_int("sequence", event.get("sequence"), minimum=1)

        if next_sequence != self.sequence + 1:
            self._reject(next_sequence, event_type, REASON_SEQUENCE_VIOLATION, "sequence must increment by one")
        if event_type not in SUPPORTED_EVENTS:
            self._reject(next_sequence, event_type, REASON_UNSUPPORTED_EVENT, "unsupported event")

        safe_boundary = _require_bool("safe_boundary", event.get("safe_boundary"))
        if event_type in {EVENT_GB_DECISION, EVENT_COMMIT_READY, EVENT_PROFILE_CHANGE} and not safe_boundary:
            self._reject(next_sequence, event_type, REASON_SAFE_BOUNDARY_REQUIRED, "safe boundary required")

        payload = event.get("payload", {})
        if payload is None:
            payload = {}
        if not isinstance(payload, dict):
            self._reject(next_sequence, event_type, REASON_INVALID_PACKET, "payload must be object")

        if event_type == EVENT_SUBMIT_PROPOSAL:
            self._apply_submit_proposal(next_sequence, payload)
        elif event_type == EVENT_GB_DECISION:
            self._apply_gb_decision(next_sequence, payload)
        elif event_type == EVENT_COMMIT_READY:
            self._apply_commit_ready(next_sequence, payload)
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
            "policy": self.policy_snapshot(),
            "sequence": self.sequence,
            "pending_queue": list(self.pending_queue),
            "staged_commits": list(self.staged_commits),
            "visible_commits": list(self.visible_commits),
            "audit_log": [record.as_dict() for record in self.audit_log],
        }
        body["verification_digest"] = _digest(body)
        return body

    def _apply_submit_proposal(self, sequence: int, payload: dict[str, Any]) -> None:
        proposal_id = _require_non_empty_str("proposal_id", payload.get("proposal_id"))
        source = _require_non_empty_str("source", payload.get("source"))
        basis_snapshot = _require_non_empty_str("basis_snapshot", payload.get("basis_snapshot"))
        priority = _require_non_empty_str("priority", payload.get("priority"))
        proposal_input = _require_object("proposal_input", payload.get("proposal_input"))

        if priority not in SUPPORTED_PRIORITIES:
            self._reject(sequence, EVENT_SUBMIT_PROPOSAL, REASON_UNSUPPORTED_ENUM, "unsupported priority")
        if "authoritative_state_patch" in proposal_input:
            self._reject(sequence, EVENT_SUBMIT_PROPOSAL, REASON_FORBIDDEN_MUTATION, "authoritative mutation prohibited")
        if self._proposal_exists(proposal_id):
            self._reject(sequence, EVENT_SUBMIT_PROPOSAL, REASON_INVALID_PACKET, "proposal_id must be unique")

        proposal = {
            "proposal_id": proposal_id,
            "source": source,
            "basis_snapshot": basis_snapshot,
            "priority": priority,
            "enqueue_sequence": sequence,
            "deterministic_input_hash": _digest(proposal_input),
            "status": "queued",
        }

        preempted = self._apply_overload_policy(sequence, proposal)
        self.pending_queue.append(proposal)
        self._resort_pending_queue()

        details = {
            "proposal_id": proposal_id,
            "priority": priority,
            "deterministic_input_hash": proposal["deterministic_input_hash"],
            "queue_depth": len(self.pending_queue),
        }
        if preempted is not None:
            details["preempted_proposal_id"] = preempted["proposal_id"]
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_SUBMIT_PROPOSAL,
            status="ACCEPT",
            reason_code="COP_OK_101_PROPOSAL_QUEUED",
            details=details,
        )

    def _apply_gb_decision(self, sequence: int, payload: dict[str, Any]) -> None:
        proposal_id = _require_non_empty_str("proposal_id", payload.get("proposal_id"))
        decision = _require_non_empty_str("decision", payload.get("decision"))
        if decision not in SUPPORTED_GB_DECISIONS:
            self._reject(sequence, EVENT_GB_DECISION, REASON_UNSUPPORTED_ENUM, "unsupported decision enum")

        proposal = self._pop_pending_proposal(proposal_id)
        if proposal is None:
            self._reject(sequence, EVENT_GB_DECISION, REASON_UNKNOWN_PROPOSAL, "proposal not found in pending queue")

        if decision == "approve":
            staged = {
                **proposal,
                "status": "approved_pending_commit",
                "decision": decision,
                "decision_sequence": sequence,
            }
            self.staged_commits.append(staged)
            self._append_audit(
                sequence=sequence,
                event_type=EVENT_GB_DECISION,
                status="ACCEPT",
                reason_code="COP_OK_102_APPROVED_STAGED",
                details={"proposal_id": proposal_id, "visibility": "staged_only"},
            )
            return

        final_status = "rejected" if decision == "reject" else "expired"
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_GB_DECISION,
            status="ACCEPT",
            reason_code="COP_OK_103_TERMINATED",
            details={"proposal_id": proposal_id, "decision": decision, "final_status": final_status},
        )

    def _apply_commit_ready(self, sequence: int, payload: dict[str, Any]) -> None:
        proposal_id = _require_non_empty_str("proposal_id", payload.get("proposal_id"))
        staged_index = next(
            (index for index, proposal in enumerate(self.staged_commits) if proposal["proposal_id"] == proposal_id),
            None,
        )
        if staged_index is None:
            self._reject(sequence, EVENT_COMMIT_READY, REASON_COMMIT_NOT_STAGED, "proposal must be staged before commit")

        proposal = self.staged_commits.pop(staged_index)
        committed = {
            "proposal_id": proposal["proposal_id"],
            "basis_snapshot": proposal["basis_snapshot"],
            "source": proposal["source"],
            "priority": proposal["priority"],
            "deterministic_input_hash": proposal["deterministic_input_hash"],
            "decision_sequence": proposal["decision_sequence"],
            "commit_sequence": sequence,
            "status": "visible_commit",
        }
        self.visible_commits.append(committed)
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_COMMIT_READY,
            status="ACCEPT",
            reason_code="COP_OK_104_VISIBLE_COMMIT",
            details={"proposal_id": proposal_id, "visible_commits": len(self.visible_commits)},
        )

    def _apply_profile_change(self, sequence: int, payload: dict[str, Any]) -> None:
        profile = _require_non_empty_str("profile", payload.get("profile"))
        if profile not in SUPPORTED_PROFILES:
            self._reject(sequence, EVENT_PROFILE_CHANGE, REASON_UNSUPPORTED_PROFILE, "unsupported profile")
        self.active_profile = profile
        self._resort_pending_queue()
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_PROFILE_CHANGE,
            status="ACCEPT",
            reason_code="COP_OK_105_PROFILE_CHANGED",
            details={"active_profile": self.active_profile, "policy": self.policy_snapshot()},
        )

    def _apply_overload_policy(self, sequence: int, proposal: dict[str, Any]) -> dict[str, Any] | None:
        policy = self.policy_snapshot()
        if len(self.pending_queue) < int(policy["max_queue"]):
            return None

        if proposal["priority"] == "safety_critical" and policy["overload_policy"] == "preempt_noncritical":
            candidate_index = next(
                (index for index, existing in enumerate(self.pending_queue) if existing["priority"] != "safety_critical"),
                None,
            )
            if candidate_index is not None:
                preempted = self.pending_queue.pop(candidate_index)
                self._append_audit(
                    sequence=sequence,
                    event_type=EVENT_SUBMIT_PROPOSAL,
                    status="ACCEPT",
                    reason_code="COP_OK_106_PREEMPT_NONCRITICAL",
                    details={
                        "proposal_id": proposal["proposal_id"],
                        "preempted_proposal_id": preempted["proposal_id"],
                    },
                )
                return preempted

        self._reject(sequence, EVENT_SUBMIT_PROPOSAL, REASON_OVERLOAD_REJECT, "queue is full under active policy")

    def _proposal_exists(self, proposal_id: str) -> bool:
        for proposal in self.pending_queue + self.staged_commits + self.visible_commits:
            if proposal["proposal_id"] == proposal_id:
                return True
        return False

    def _pop_pending_proposal(self, proposal_id: str) -> dict[str, Any] | None:
        for index, proposal in enumerate(self.pending_queue):
            if proposal["proposal_id"] == proposal_id:
                return self.pending_queue.pop(index)
        return None

    def _resort_pending_queue(self) -> None:
        policy = self.policy_snapshot()
        if policy["fairness_policy"] == "safety_first":
            self.pending_queue.sort(key=lambda proposal: (_priority_rank(proposal["priority"]), proposal["enqueue_sequence"]))
            return
        self.pending_queue.sort(key=lambda proposal: proposal["enqueue_sequence"])

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
        raise COPDeterministicReject(reason_code, message)
