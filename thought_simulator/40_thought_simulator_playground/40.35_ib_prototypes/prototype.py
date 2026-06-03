"""Deterministic Inquiry Basin (IB) prototype for 40.35."""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
import json


MODULE_NAME = "40.35_ib_prototypes"
CONTRACT_VERSION = "1.0"
MAX_DEPTH = 2

EVENT_REQUEST_CREATE = "request_create"
EVENT_GB_DECISION = "gb_decision"
EVENT_EVOLVE = "evolve"
EVENT_SPLIT = "split"
EVENT_MERGE = "merge"
EVENT_PROMOTE = "promote"
EVENT_RETIRE = "retire"

SUPPORTED_EVENTS = {
    EVENT_REQUEST_CREATE,
    EVENT_GB_DECISION,
    EVENT_EVOLVE,
    EVENT_SPLIT,
    EVENT_MERGE,
    EVENT_PROMOTE,
    EVENT_RETIRE,
}
SUPPORTED_DECISIONS = {"approve", "deny"}

REASON_UNSUPPORTED_EVENT = "IB_RSN_001_UNSUPPORTED_EVENT"
REASON_SEQUENCE_VIOLATION = "IB_RSN_002_SEQUENCE_VIOLATION"
REASON_SAFE_BOUNDARY_REQUIRED = "IB_RSN_003_SAFE_BOUNDARY_REQUIRED"
REASON_UNSUPPORTED_ENUM = "IB_RSN_004_UNSUPPORTED_ENUM"
REASON_INVALID_PACKET = "IB_RSN_005_INVALID_PACKET"
REASON_DIRECT_OUB_BYPASS = "IB_RSN_006_DIRECT_OUB_BYPASS"
REASON_UNKNOWN_REQUEST = "IB_RSN_007_UNKNOWN_REQUEST"
REASON_UNKNOWN_IB = "IB_RSN_008_UNKNOWN_IB"
REASON_DEPTH_LIMIT = "IB_RSN_009_DEPTH_LIMIT"
REASON_INVALID_MERGE = "IB_RSN_010_INVALID_MERGE"
REASON_DUPLICATE_ID = "IB_RSN_011_DUPLICATE_ID"


class IBDeterministicReject(ValueError):
    """Raised when deterministic IB contracts are violated."""

    def __init__(self, reason_code: str, message: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(payload: dict[str, Any]) -> str:
    return sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _require_non_empty_str(field_name: str, value: Any) -> str:
    if not isinstance(value, str):
        raise IBDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise IBDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be non-empty")
    return normalized


def _require_int(field_name: str, value: Any, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise IBDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be int")
    if value < minimum:
        raise IBDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be >= {minimum}")
    return value


def _require_bool(field_name: str, value: Any) -> bool:
    if not isinstance(value, bool):
        raise IBDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be bool")
    return value


def _require_list_of_str(field_name: str, value: Any, minimum_len: int = 0) -> list[str]:
    if not isinstance(value, list):
        raise IBDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must be list")
    normalized: list[str] = []
    for index, item in enumerate(value):
        normalized.append(_require_non_empty_str(f"{field_name}[{index}]", item))
    if len(normalized) < minimum_len:
        raise IBDeterministicReject(REASON_INVALID_PACKET, f"{field_name} must have at least {minimum_len} items")
    return normalized


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
class IBState:
    profile_signature: str = "P1"
    sequence: int = 0
    pending_requests: list[dict[str, Any]] = field(default_factory=list)
    active_ibs: list[dict[str, Any]] = field(default_factory=list)
    retired_ibs: list[dict[str, Any]] = field(default_factory=list)
    promoted_outputs: list[dict[str, Any]] = field(default_factory=list)
    audit_log: list[AuditRecord] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.profile_signature = _require_non_empty_str("profile_signature", self.profile_signature)
        self.sequence = _require_int("sequence", self.sequence, minimum=0)
        self._append_audit(
            sequence=self.sequence,
            event_type="create",
            status="ACCEPT",
            reason_code="IB_OK_000_CREATED",
            details={"contract_version": CONTRACT_VERSION, "profile_signature": self.profile_signature},
        )

    def apply_event(self, event: dict[str, Any]) -> dict[str, Any]:
        event_type = _require_non_empty_str("event_type", event.get("event_type"))
        next_sequence = _require_int("sequence", event.get("sequence"), minimum=1)

        if next_sequence != self.sequence + 1:
            self._reject(next_sequence, event_type, REASON_SEQUENCE_VIOLATION, "sequence must increment by one")
        if event_type not in SUPPORTED_EVENTS:
            self._reject(next_sequence, event_type, REASON_UNSUPPORTED_EVENT, "unsupported event")

        safe_boundary = _require_bool("safe_boundary", event.get("safe_boundary"))
        if event_type != EVENT_REQUEST_CREATE and not safe_boundary:
            self._reject(next_sequence, event_type, REASON_SAFE_BOUNDARY_REQUIRED, "safe boundary required")

        payload = event.get("payload", {})
        if payload is None or not isinstance(payload, dict):
            self._reject(next_sequence, event_type, REASON_INVALID_PACKET, "payload must be object")

        if event_type == EVENT_REQUEST_CREATE:
            self._apply_request_create(next_sequence, payload)
        elif event_type == EVENT_GB_DECISION:
            self._apply_gb_decision(next_sequence, payload)
        elif event_type == EVENT_EVOLVE:
            self._apply_evolve(next_sequence, payload)
        elif event_type == EVENT_SPLIT:
            self._apply_split(next_sequence, payload)
        elif event_type == EVENT_MERGE:
            self._apply_merge(next_sequence, payload)
        elif event_type == EVENT_PROMOTE:
            self._apply_promote(next_sequence, payload)
        elif event_type == EVENT_RETIRE:
            self._apply_retire(next_sequence, payload)

        self.sequence = next_sequence
        return self.snapshot()

    def snapshot(self) -> dict[str, Any]:
        body = {
            "module": MODULE_NAME,
            "contract_version": CONTRACT_VERSION,
            "profile_signature": self.profile_signature,
            "sequence": self.sequence,
            "pending_requests": list(self.pending_requests),
            "active_ibs": list(self.active_ibs),
            "retired_ibs": list(self.retired_ibs),
            "promoted_outputs": list(self.promoted_outputs),
            "audit_log": [record.as_dict() for record in self.audit_log],
        }
        body["verification_digest"] = _digest(body)
        return body

    def _apply_request_create(self, sequence: int, payload: dict[str, Any]) -> None:
        snapshot_id = _require_non_empty_str("snapshot_id", payload.get("snapshot_id"))
        triggering_ob_ids = sorted(_require_list_of_str("triggering_ob_ids", payload.get("triggering_ob_ids"), minimum_len=1))
        request_reason = _require_non_empty_str("request_reason", payload.get("request_reason"))
        source_channel = _require_non_empty_str("source_channel", payload.get("source_channel"))
        if source_channel != "ob_ib":
            self._reject(sequence, EVENT_REQUEST_CREATE, REASON_DIRECT_OUB_BYPASS, "IB accepts requests only from OB<->IB path")

        request_id = f"ibr:{_digest({'snapshot_id': snapshot_id, 'sequence': sequence})[:12]}"
        request = {
            "request_id": request_id,
            "snapshot_id": snapshot_id,
            "triggering_ob_ids": triggering_ob_ids,
            "request_reason": request_reason,
            "status": "pending_gb_approval",
            "request_sequence": sequence,
        }
        self.pending_requests.append(request)
        self.pending_requests.sort(key=lambda item: item["request_id"])
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_REQUEST_CREATE,
            status="ACCEPT",
            reason_code="IB_OK_101_REQUEST_CREATED",
            details={"request_id": request_id, "snapshot_id": snapshot_id, "triggering_ob_ids": triggering_ob_ids},
        )

    def _apply_gb_decision(self, sequence: int, payload: dict[str, Any]) -> None:
        request_id = _require_non_empty_str("request_id", payload.get("request_id"))
        decision = _require_non_empty_str("decision", payload.get("decision"))
        if decision not in SUPPORTED_DECISIONS:
            self._reject(sequence, EVENT_GB_DECISION, REASON_UNSUPPORTED_ENUM, "unsupported decision enum")

        request_index = next((index for index, request in enumerate(self.pending_requests) if request["request_id"] == request_id), None)
        if request_index is None:
            self._reject(sequence, EVENT_GB_DECISION, REASON_UNKNOWN_REQUEST, "request not found")
        request = self.pending_requests.pop(request_index)

        if decision == "deny":
            self._append_audit(
                sequence=sequence,
                event_type=EVENT_GB_DECISION,
                status="ACCEPT",
                reason_code="IB_OK_102_REQUEST_DENIED",
                details={"request_id": request_id, "decision": decision},
            )
            return

        ib_id = _require_non_empty_str("ib_id", payload.get("ib_id"))
        if self._ib_exists(ib_id):
            self._reject(sequence, EVENT_GB_DECISION, REASON_DUPLICATE_ID, "ib_id already exists")
        hypotheses = sorted(_require_list_of_str("hypotheses", payload.get("hypotheses", [])))
        pending_evidence_requests = sorted(_require_list_of_str("pending_evidence_requests", payload.get("pending_evidence_requests", [])))
        gb_reference = _require_non_empty_str("gb_reference", payload.get("gb_reference"))
        node = {
            "ib_id": ib_id,
            "status": "active",
            "origin_snapshot": request["snapshot_id"],
            "triggering_ob_ids": request["triggering_ob_ids"],
            "gb_approval_reference": gb_reference,
            "hypotheses": hypotheses,
            "pending_evidence_requests": pending_evidence_requests,
            "partial_interpretations": [],
            "depth_state": 0,
            "branch_state": [],
            "lineage": [request_id],
            "tp_log": [
                self._tp_tag(
                    ib_id=ib_id,
                    event_type="IB_CREATED",
                    gb_reference=gb_reference,
                    safe_boundary=True,
                    reason_code="IB_OK_102_REQUEST_APPROVED",
                    details={"request_id": request_id},
                )
            ],
        }
        self.active_ibs.append(node)
        self.active_ibs.sort(key=lambda item: item["ib_id"])
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_GB_DECISION,
            status="ACCEPT",
            reason_code="IB_OK_102_REQUEST_APPROVED",
            details={"request_id": request_id, "ib_id": ib_id, "gb_reference": gb_reference},
        )

    def _apply_evolve(self, sequence: int, payload: dict[str, Any]) -> None:
        ib = self._require_active_ib(sequence, EVENT_EVOLVE, payload)
        hypothesis_delta = sorted(_require_list_of_str("hypothesis_delta", payload.get("hypothesis_delta", [])))
        evidence_request_delta = sorted(_require_list_of_str("evidence_request_delta", payload.get("evidence_request_delta", [])))
        partial_interpretations = sorted(_require_list_of_str("partial_interpretations", payload.get("partial_interpretations", [])))
        depth_increment = _require_int("depth_increment", payload.get("depth_increment", 0), minimum=0)
        if ib["depth_state"] + depth_increment > MAX_DEPTH:
            self._reject(sequence, EVENT_EVOLVE, REASON_DEPTH_LIMIT, "depth limit exceeded")

        ib["hypotheses"] = sorted(set(ib["hypotheses"] + hypothesis_delta))
        ib["pending_evidence_requests"] = sorted(set(ib["pending_evidence_requests"] + evidence_request_delta))
        ib["partial_interpretations"] = sorted(set(ib["partial_interpretations"] + partial_interpretations))
        ib["depth_state"] += depth_increment
        ib["tp_log"].append(
            self._tp_tag(
                ib_id=ib["ib_id"],
                event_type="IB_EVOLVED",
                gb_reference=_require_non_empty_str("gb_reference", payload.get("gb_reference")),
                safe_boundary=True,
                reason_code="IB_OK_103_EVOLVED",
                details={
                    "hypothesis_delta": hypothesis_delta,
                    "evidence_request_delta": evidence_request_delta,
                    "partial_interpretations": partial_interpretations,
                    "depth_state": ib["depth_state"],
                },
            )
        )
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_EVOLVE,
            status="ACCEPT",
            reason_code="IB_OK_103_EVOLVED",
            details={"ib_id": ib["ib_id"], "depth_state": ib["depth_state"]},
        )

    def _apply_split(self, sequence: int, payload: dict[str, Any]) -> None:
        ib = self._require_active_ib(sequence, EVENT_SPLIT, payload)
        child_suffixes = sorted(_require_list_of_str("child_suffixes", payload.get("child_suffixes"), minimum_len=2))
        gb_reference = _require_non_empty_str("gb_reference", payload.get("gb_reference"))
        child_ids = [f"{ib['ib_id']}:{suffix}" for suffix in child_suffixes]
        for child_id in child_ids:
            if self._ib_exists(child_id):
                self._reject(sequence, EVENT_SPLIT, REASON_DUPLICATE_ID, "split child id already exists")
        ib["status"] = "dampened_after_split"
        ib["branch_state"] = child_ids
        ib["tp_log"].append(
            self._tp_tag(
                ib_id=ib["ib_id"],
                event_type="IB_SPLIT",
                gb_reference=gb_reference,
                safe_boundary=True,
                reason_code="IB_OK_104_SPLIT_PARENT_DAMPENED",
                details={"child_ids": child_ids},
            )
        )
        for child_id in child_ids:
            child = {
                "ib_id": child_id,
                "status": "active",
                "origin_snapshot": ib["origin_snapshot"],
                "triggering_ob_ids": list(ib["triggering_ob_ids"]),
                "gb_approval_reference": gb_reference,
                "hypotheses": list(ib["hypotheses"]),
                "pending_evidence_requests": list(ib["pending_evidence_requests"]),
                "partial_interpretations": list(ib["partial_interpretations"]),
                "depth_state": ib["depth_state"],
                "branch_state": [],
                "lineage": list(ib["lineage"]) + [ib["ib_id"]],
                "tp_log": [
                    self._tp_tag(
                        ib_id=child_id,
                        event_type="IB_CREATED_FROM_SPLIT",
                        gb_reference=gb_reference,
                        safe_boundary=True,
                        reason_code="IB_OK_105_SPLIT_CHILD_CREATED",
                        details={"parent_ib_id": ib["ib_id"]},
                    )
                ],
            }
            self.active_ibs.append(child)
        self.active_ibs.sort(key=lambda item: item["ib_id"])
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_SPLIT,
            status="ACCEPT",
            reason_code="IB_OK_104_SPLIT_PARENT_DAMPENED",
            details={"parent_ib_id": ib["ib_id"], "child_ids": child_ids},
        )

    def _apply_merge(self, sequence: int, payload: dict[str, Any]) -> None:
        source_ib_ids = sorted(_require_list_of_str("source_ib_ids", payload.get("source_ib_ids"), minimum_len=2))
        merged_ib_id = _require_non_empty_str("merged_ib_id", payload.get("merged_ib_id"))
        gb_reference = _require_non_empty_str("gb_reference", payload.get("gb_reference"))
        if self._ib_exists(merged_ib_id):
            self._reject(sequence, EVENT_MERGE, REASON_DUPLICATE_ID, "merged_ib_id already exists")

        source_nodes: list[dict[str, Any]] = []
        for ib_id in source_ib_ids:
            source_nodes.append(self._require_active_ib_by_id(sequence, EVENT_MERGE, ib_id))
        if len({node["origin_snapshot"] for node in source_nodes}) != 1:
            self._reject(sequence, EVENT_MERGE, REASON_INVALID_MERGE, "merge requires shared origin snapshot")

        merged = {
            "ib_id": merged_ib_id,
            "status": "active",
            "origin_snapshot": source_nodes[0]["origin_snapshot"],
            "triggering_ob_ids": sorted({ob_id for node in source_nodes for ob_id in node["triggering_ob_ids"]}),
            "gb_approval_reference": gb_reference,
            "hypotheses": sorted({item for node in source_nodes for item in node["hypotheses"]}),
            "pending_evidence_requests": sorted({item for node in source_nodes for item in node["pending_evidence_requests"]}),
            "partial_interpretations": sorted({item for node in source_nodes for item in node["partial_interpretations"]}),
            "depth_state": max(node["depth_state"] for node in source_nodes),
            "branch_state": [],
            "lineage": sorted({item for node in source_nodes for item in node["lineage"]} | set(source_ib_ids)),
            "tp_log": [
                self._tp_tag(
                    ib_id=merged_ib_id,
                    event_type="IB_MERGED",
                    gb_reference=gb_reference,
                    safe_boundary=True,
                    reason_code="IB_OK_106_MERGED_CREATED",
                    details={"source_ib_ids": source_ib_ids},
                )
            ],
        }
        for source_ib_id in source_ib_ids:
            source = self._pop_active_ib(source_ib_id)
            if source is None:
                self._reject(sequence, EVENT_MERGE, REASON_UNKNOWN_IB, "source ib disappeared during merge")
            source["status"] = "retired_after_merge"
            source["tp_log"].append(
                self._tp_tag(
                    ib_id=source_ib_id,
                    event_type="IB_RETIRED_AFTER_MERGE",
                    gb_reference=gb_reference,
                    safe_boundary=True,
                    reason_code="IB_OK_107_MERGE_SOURCE_RETIRED",
                    details={"merged_ib_id": merged_ib_id},
                )
            )
            self.retired_ibs.append(source)
        self.retired_ibs.sort(key=lambda item: item["ib_id"])
        self.active_ibs.append(merged)
        self.active_ibs.sort(key=lambda item: item["ib_id"])
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_MERGE,
            status="ACCEPT",
            reason_code="IB_OK_106_MERGED_CREATED",
            details={"source_ib_ids": source_ib_ids, "merged_ib_id": merged_ib_id},
        )

    def _apply_promote(self, sequence: int, payload: dict[str, Any]) -> None:
        ib = self._require_active_ib(sequence, EVENT_PROMOTE, payload)
        gb_reference = _require_non_empty_str("gb_reference", payload.get("gb_reference"))
        oub_output_id = _require_non_empty_str("oub_output_id", payload.get("oub_output_id"))
        ib["status"] = "promoted_to_oub"
        ib["tp_log"].append(
            self._tp_tag(
                ib_id=ib["ib_id"],
                event_type="IB_PROMOTED_TO_OUB",
                gb_reference=gb_reference,
                safe_boundary=True,
                reason_code="IB_OK_108_PROMOTED",
                details={"oub_output_id": oub_output_id},
            )
        )
        self.promoted_outputs.append({
            "ib_id": ib["ib_id"],
            "oub_output_id": oub_output_id,
            "gb_reference": gb_reference,
            "status": "ready",
        })
        self.promoted_outputs.sort(key=lambda item: item["ib_id"])
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_PROMOTE,
            status="ACCEPT",
            reason_code="IB_OK_108_PROMOTED",
            details={"ib_id": ib["ib_id"], "oub_output_id": oub_output_id},
        )

    def _apply_retire(self, sequence: int, payload: dict[str, Any]) -> None:
        ib_id = _require_non_empty_str("ib_id", payload.get("ib_id"))
        gb_reference = _require_non_empty_str("gb_reference", payload.get("gb_reference"))
        ib = self._pop_active_ib(ib_id)
        if ib is None:
            self._reject(sequence, EVENT_RETIRE, REASON_UNKNOWN_IB, "ib not found")
        ib["status"] = "retired"
        ib["tp_log"].append(
            self._tp_tag(
                ib_id=ib_id,
                event_type="IB_RETIRED",
                gb_reference=gb_reference,
                safe_boundary=True,
                reason_code="IB_OK_109_RETIRED",
                details={},
            )
        )
        self.retired_ibs.append(ib)
        self.retired_ibs.sort(key=lambda item: item["ib_id"])
        self._append_audit(
            sequence=sequence,
            event_type=EVENT_RETIRE,
            status="ACCEPT",
            reason_code="IB_OK_109_RETIRED",
            details={"ib_id": ib_id},
        )

    def _require_active_ib(self, sequence: int, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        ib_id = _require_non_empty_str("ib_id", payload.get("ib_id"))
        return self._require_active_ib_by_id(sequence, event_type, ib_id)

    def _require_active_ib_by_id(self, sequence: int, event_type: str, ib_id: str) -> dict[str, Any]:
        match = next((item for item in self.active_ibs if item["ib_id"] == ib_id), None)
        if match is None:
            self._reject(sequence, event_type, REASON_UNKNOWN_IB, "ib not found")
        return match

    def _pop_active_ib(self, ib_id: str) -> dict[str, Any] | None:
        for index, ib in enumerate(self.active_ibs):
            if ib["ib_id"] == ib_id:
                return self.active_ibs.pop(index)
        return None

    def _ib_exists(self, ib_id: str) -> bool:
        for item in self.active_ibs + self.retired_ibs:
            if item["ib_id"] == ib_id:
                return True
        return False

    def _tp_tag(
        self,
        ib_id: str,
        event_type: str,
        gb_reference: str,
        safe_boundary: bool,
        reason_code: str,
        details: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "ib_id": ib_id,
            "event_type": event_type,
            "gb_reference": gb_reference,
            "safe_boundary": safe_boundary,
            "reason_code": reason_code,
            "profile_signature": self.profile_signature,
            "tp_seq": self.sequence + 1,
            "details": details,
        }

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
        raise IBDeterministicReject(reason_code, message)
