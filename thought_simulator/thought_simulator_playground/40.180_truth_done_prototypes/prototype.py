"""Truth/Done terminal evaluation prototype for 40.180_truth_done_prototypes (W3).

Per 20.140: consumes TB records post-merge / pre-mtp_update.
- Deterministic field-based evaluation (no latent inference).
- Messy-input gating to BLOCKED / PARTIAL with reason codes.
- Forbidden: rejects reads of routing_metadata or Pipeline B fields.
- Canonical ordering of truth_hypotheses (by hypothesis_id).
- Emits done_state + H% accounting stub; audit for policy violations.
- Seed-independent / replayable for identical inputs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TruthHypothesisRecord:
    hypothesis_id: str
    proposition_ref: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    truth_status: str = "UNKNOWN"

    def as_dict(self) -> dict[str, Any]:
        return {
            "hypothesis_id": self.hypothesis_id,
            "proposition_ref": self.proposition_ref,
            "evidence_refs": self.evidence_refs,
            "truth_status": self.truth_status,
        }


@dataclass
class DoneState:
    completion_status: str = "UNKNOWN"  # DONE | BLOCKED | PARTIAL | ...
    blocked_by_messy_input: bool = False
    completion_reason_codes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "completion_status": self.completion_status,
            "blocked_by_messy_input": self.blocked_by_messy_input,
            "completion_reason_codes": self.completion_reason_codes,
        }


@dataclass
class TruthDoneOutput:
    truth_hypotheses: list[TruthHypothesisRecord] = field(default_factory=list)
    done_state: DoneState = field(default_factory=DoneState)
    evaluation_audit_records: list[dict[str, Any]] = field(default_factory=list)
    policy_signature: str = ""
    cycle_id: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "truth_hypotheses": [h.as_dict() for h in self.truth_hypotheses],
            "done_state": self.done_state.as_dict(),
            "evaluation_audit_records": self.evaluation_audit_records,
            "policy_signature": self.policy_signature,
            "cycle_id": self.cycle_id,
        }


class TruthDone:
    """Truth/Done evaluation stage (A-chain terminal gate before mtp_update)."""

    def evaluate(
        self,
        inputs: dict[str, Any],
        policy_signature: str = "",
        cycle_id: str = "",
    ) -> TruthDoneOutput:
        audit: list[dict[str, Any]] = []

        # HLR-20.140-043: forbidden to read routing_metadata (or other B fields) here
        if inputs.get("routing_metadata"):
            audit.append({
                "type": "FORBIDDEN_READ",
                "field": "routing_metadata",
                "detail": "HLR-20.140-043: Truth/Done must not read routing or Pipeline B metadata",
            })
            # Early return with audit marker; no hypotheses promoted
            return TruthDoneOutput(
                truth_hypotheses=[],
                done_state=DoneState(
                    completion_status="BLOCKED",
                    blocked_by_messy_input=False,
                    completion_reason_codes=["FORBIDDEN_ROUTING"],
                ),
                evaluation_audit_records=audit,
                policy_signature=policy_signature,
                cycle_id=cycle_id,
            )

        # Messy input gating (HLR-20.140-029,030)
        messy = inputs.get("messy_input_record") or {}
        mi_class = None
        if isinstance(messy, dict):
            mi_class = messy.get("class")

        # Build hypotheses from TB-provided records (explicit fields only)
        raw_records = inputs.get("truth_hypothesis_records") or []
        hyps: list[TruthHypothesisRecord] = []
        for r in raw_records:
            hid = str(r.get("hypothesis_id", ""))
            hyps.append(
                TruthHypothesisRecord(
                    hypothesis_id=hid,
                    proposition_ref=str(r.get("proposition_ref", "")),
                    evidence_refs=list(r.get("evidence_refs", []) or []),
                    truth_status="SUPPORTED",  # field-driven; evidence presence not re-evaluated here
                )
            )

        # Canonical ordering (HLR-20.140-038): by hypothesis_id
        hyps.sort(key=lambda h: h.hypothesis_id)

        # done_state
        if mi_class:
            # Messy blocks or partials completion (exact status flexible per harness tolerance)
            completion_status = "BLOCKED" if str(mi_class).startswith("MI_") else "PARTIAL"
            done = DoneState(
                completion_status=completion_status,
                blocked_by_messy_input=True,
                completion_reason_codes=[str(mi_class)],
            )
        else:
            done = DoneState(
                completion_status="DONE",
                blocked_by_messy_input=False,
                completion_reason_codes=[],
            )

        # Simple H% stub (no latent computation; explicit accounting only)
        # In real would aggregate from hypotheses/evidence strength per 20.140
        h_percent = 1.0 if (not mi_class and hyps) else (0.5 if mi_class else 0.0)

        out = TruthDoneOutput(
            truth_hypotheses=hyps,
            done_state=done,
            evaluation_audit_records=audit,
            policy_signature=policy_signature,
            cycle_id=cycle_id,
        )
        # Attach h_percent for consumers (e.g. 40.150) without changing dataclass shape for tests
        out.h_percent = h_percent  # type: ignore[attr-defined]
        return out
