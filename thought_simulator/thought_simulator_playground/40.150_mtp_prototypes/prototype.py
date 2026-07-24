"""MTP (Meaning Trajectory Point) prototype for 40.150_mtp_prototypes.

Implements core lifecycle per 20.115 and 20.120:
- Lane TP aggregation / merge into semantic_core
- Truth/Done gate before mtp_update
- mtp_update emits immutable commit_id + semantic_snapshot_ref
- Rejects pre-truth update and B-envelope fields on core
- Deterministic replay for identical inputs
"""


from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

@dataclass
class SemanticCore:
    propositions: list[dict] = field(default_factory=list)
    stance: dict[str, Any] = field(default_factory=dict)
    affect: dict[str, Any] = field(default_factory=dict)
    intent: dict[str, Any] = field(default_factory=dict)
    truth_hypotheses: list[dict] = field(default_factory=list)
    lineage: list[dict] = field(default_factory=list)
    delta_h: dict[str, Any] = field(default_factory=dict)
    stability_metadata: dict[str, Any] = field(default_factory=dict)

    def content_hash(self) -> str:
        data = {
            "propositions": sorted(self.propositions, key=lambda x: x.get("id", "")),
            "stance": self.stance,
            "affect": self.affect,
            "intent": self.intent,
            "truth_hypotheses": sorted(self.truth_hypotheses, key=lambda x: x.get("id", "")),
            "lineage": self.lineage,
            "delta_h": self.delta_h,
        }
        serialized = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]

@dataclass
class MTPCommitRecord:
    commit_id: str
    cycle_id: str
    mtp_id: str
    semantic_snapshot_ref: str
    policy_signature: str
    execution_signature: str
    audit_token: str

@dataclass
class CommitResult:
    ok: bool
    commit_id: str | None = None
    semantic_snapshot_ref: str | None = None
    commit_record: MTPCommitRecord | None = None
    reason_codes: list[str] = field(default_factory=list)

REASON_PRE_TRUTH = "MTP_RSN_001_PRE_TRUTH"
REASON_B_ENVELOPE = "MTP_RSN_002_B_ENVELOPE"
REASON_ALREADY_COMMITTED = "MTP_RSN_003_ALREADY_COMMITTED"
REASON_INVALID_MERGE = "MTP_RSN_004_INVALID_MERGE"

class MTPStore:
    """MTP lifecycle owner: aggregation, mtp_update, commit_id emission."""

    def __init__(self, mtp_id: str = "mtp-001", cycle_id: str = "c-20260609-001"):
        self.mtp_id = mtp_id
        self.cycle_id = cycle_id
        self.semantic_core = SemanticCore()
        self.audit: list[dict] = []
        self.committed = False
        self.commit_id: str | None = None
        self.semantic_snapshot_ref: str | None = None
        self._lane_contribs: list[dict] = []

    def add_lane_contribution(self, lane_id: str, contribution: dict[str, Any]) -> None:
        if self.committed:
            raise ValueError(REASON_ALREADY_COMMITTED)
        self._lane_contribs.append({"lane_id": lane_id, "contrib": contribution})
        if "propositions" in contribution:
            self.semantic_core.propositions.extend(contribution["propositions"])
        if "lineage" in contribution:
            self.semantic_core.lineage.extend(contribution["lineage"])
        self.audit.append({"event": "lane_contrib", "lane_id": lane_id, "when": "pre_mtp_update"})

    def truth_done(self, passed: bool, reason_code: str | None = None) -> None:
        self._truth_passed = passed
        self._truth_reason = reason_code
        self.audit.append({"event": "truth_done", "passed": passed, "reason_code": reason_code})

    def mtp_update(self, policy_signature: str = "pol-v1", execution_signature: str = "exec-v1") -> CommitResult:
        if self.committed:
            return CommitResult(ok=False, reason_codes=[REASON_ALREADY_COMMITTED])
        if not getattr(self, "_truth_passed", False):
            if not getattr(self, "_truth_reason", None):
                return CommitResult(ok=False, reason_codes=[REASON_PRE_TRUTH])
        core_dict = self.semantic_core.__dict__
        if any(k in core_dict for k in ["exec_plan", "exec_trace", "xp_id"]):
            return CommitResult(ok=False, reason_codes=[REASON_B_ENVELOPE])
        core_hash = self.semantic_core.content_hash()
        preimage = f"{self.mtp_id}|{self.cycle_id}|{core_hash}|{policy_signature}|{execution_signature}"
        commit_id = "commit-" + hashlib.sha256(preimage.encode("utf-8")).hexdigest()[:16]
        snapshot_ref = core_hash
        record = MTPCommitRecord(commit_id=commit_id, cycle_id=self.cycle_id, mtp_id=self.mtp_id, semantic_snapshot_ref=snapshot_ref, policy_signature=policy_signature, execution_signature=execution_signature, audit_token=f"audit-{len(self.audit)}")
        self.commit_id = commit_id
        self.semantic_snapshot_ref = snapshot_ref
        self.committed = True
        self.audit.append({"event": "mtp_update", "commit_id": commit_id, "semantic_snapshot_ref": snapshot_ref})
        return CommitResult(ok=True, commit_id=commit_id, semantic_snapshot_ref=snapshot_ref, commit_record=record)

    def export_snapshot(self) -> dict:
        core = {
            "propositions": sorted(self.semantic_core.propositions, key=lambda x: str(x.get("id", ""))),
            "stance": self.semantic_core.stance,
            "affect": self.semantic_core.affect,
            "intent": self.semantic_core.intent,
            "truth_hypotheses": self.semantic_core.truth_hypotheses,
            "lineage": self.semantic_core.lineage,
            "delta_h": self.semantic_core.delta_h,
            "stability_metadata": self.semantic_core.stability_metadata,
        }
        snap = {
            "mtp_id": self.mtp_id,
            "cycle_id": self.cycle_id,
            "semantic_core": core,
            "committed": self.committed,
            "commit_id": self.commit_id,
            "semantic_snapshot_ref": self.semantic_snapshot_ref,
            "audit_len": len(self.audit),
        }
        if self.committed:
            snap["commit_id"] = self.commit_id
        return snap

    def get_audit(self) -> list[dict]:
        return list(self.audit)
    raise NotImplementedError(
        "Scaffold module 40.150: implementation pending (Phase B approval required)"
    )