"""Canonical conversation-layer struct prototypes for W2 wire-up (40.100).

Field-compatible with 40.60 inline types; digest algorithm matches 40.60
compute_usp_version_ref for cross-module replay evidence.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any

SCHEMA_USP_SNAPSHOT = "usp_snapshot_v1"
SCHEMA_CONVERSATION_LAYER = "conversation_layer_v1"
SCHEMA_CLARIFICATION_EVENT = "clarification_event_v1"

FORBIDDEN_ENVELOPE_FIELDS = frozenset({
    "semantic_core",
    "tp_tr",
    "TP.TR",
    "exec_plan",
    "exec_trace",
    "lane_id",
    "tp_id",
})

REASON_UNKNOWN_SCHEMA = "STRUCT_RSN_001_UNKNOWN_SCHEMA"
REASON_FORBIDDEN_FIELD = "STRUCT_RSN_002_FORBIDDEN_ENVELOPE_FIELD"


class StructReject(ValueError):
    def __init__(self, reason_code: str, message: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def canonical_digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def compute_usp_version_ref(snapshot: dict[str, Any]) -> str:
    """Content-addressed ref — matches 40.60 digest inputs.

    Sort key is (scope, version, rule_id) only. ``precedence`` is excluded —
    it governs IIInB apply ordering (20.102-012), not snapshot identity.
    """
    canonical = {
        "rules": sorted(
            snapshot.get("rules", []),
            key=lambda r: (r.get("scope", ""), r.get("version", 0), r.get("rule_id", "")),
        ),
        "usp_version_id": snapshot.get("usp_version_id"),
    }
    return canonical_digest(canonical)


@dataclass
class UspRule:
    rule_id: str
    pattern: str
    expansion: str
    state: str = "ACTIVE"
    scope: str = "conversation"
    version: int = 1
    precedence: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class UspSnapshot:
    usp_version_id: int
    rules: list[UspRule] = field(default_factory=list)
    schema_version: str = SCHEMA_USP_SNAPSHOT

    def active_rules(self) -> list[UspRule]:
        return [r for r in self.rules if r.state == "ACTIVE"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "usp_version_id": self.usp_version_id,
            "usp_version_ref": self.version_ref,
            "rules": [r.to_dict() for r in self.active_rules()],
        }

    def to_storage_dict(self) -> dict[str, Any]:
        return {
            "usp_version_id": self.usp_version_id,
            "rules": [r.to_dict() for r in self.rules],
        }

    @property
    def version_ref(self) -> str:
        return compute_usp_version_ref(self.to_storage_dict())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UspSnapshot:
        if data.get("schema_version", SCHEMA_USP_SNAPSHOT) != SCHEMA_USP_SNAPSHOT:
            raise StructReject(REASON_UNKNOWN_SCHEMA, "unsupported usp snapshot schema")
        rules = [UspRule(**r) for r in data.get("rules", [])]
        return cls(
            usp_version_id=int(data["usp_version_id"]),
            rules=rules,
            schema_version=SCHEMA_USP_SNAPSHOT,
        )


@dataclass
class InputRepairTag:
    tag_id: str
    segment_index: int
    rule_id: str | None
    outcome: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ConversationLayerState:
    conversation_id: str
    usp_version_ref_pinned: str | None = None
    pending_clarifications: int = 0
    schema_version: str = SCHEMA_CONVERSATION_LAYER

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def validate_envelope_clean(cls, payload: dict[str, Any]) -> None:
        for key in payload:
            if key in FORBIDDEN_ENVELOPE_FIELDS:
                raise StructReject(REASON_FORBIDDEN_FIELD, f"forbidden field: {key}")


@dataclass
class ClarificationEvent:
    event_id: str
    integration_seq: int
    pattern: str
    expansion: str
    scope: str = "conversation"
    source: str = "CIL"
    schema_version: str = SCHEMA_CLARIFICATION_EVENT

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def validate_complete(self) -> None:
        if not self.pattern or not self.expansion or not self.scope:
            raise StructReject("STRUCT_RSN_003_INCOMPLETE", "incomplete clarification_event")


@dataclass
class UpiCommitRecord:
    commit_status: str
    usp_version_id: int | None = None
    usp_version_ref: str | None = None
    gb_reason_code: str | None = None
    reason_codes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class UspVersionRecord:
    usp_version_id: int
    usp_version_ref: str
    prior_version_ref: str | None
    transition: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CobUspSnapshotPin:
    cob_id: str
    usp_version_ref: str
    usp_version_id: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def export_sorted_tags(tags: list[InputRepairTag]) -> str:
    ordered = sorted(tags, key=lambda t: (t.segment_index, t.tag_id))
    payload = [t.to_dict() for t in ordered]
    return canonical_json({"tags": payload})