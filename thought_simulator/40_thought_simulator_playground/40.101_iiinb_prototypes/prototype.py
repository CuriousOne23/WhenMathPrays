"""Exploratory IIInB (Input Inference/Repair Basin) prototype.

Stage wire: input_semantic_repair — profile-gated, read-only USP apply,
intake-bound TP writes only. Ordering: InB -> IIInB -> RB.

Envelope guard checks (semantic_core, TP.TR, exec_plan, exec_trace) are positive-only
in this module; FAIL_ENVELOPE negative replay verdicts deferred to 40.510-207.
"""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Optional

MAX_SEGMENTS = 32
MAX_RULE_APPLICATIONS = 16

REASON_CODES = frozenset({
    "PROFILE_DISABLED",
    "USP_LOAD_FAILED",
    "SEGMENT_CAP",
    "APPLY_CAP",
    "NO_MATCHING_RULE",
    "INB_HANDOFF_REJECTED",
})

BASIN_CHAIN_STAGES = frozenset({"routing_basin", "output_basin", "truth_basin", "termination_basin"})
INTAKE_PATH_STAGES = frozenset({"inb_surface_norm", "input_semantic_repair", "routing"})


def _assert_reason_code(code: str) -> None:
    assert code in REASON_CODES, f"unknown_reason_code: {code}"


def _canonical_digest(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def compute_usp_version_ref(snapshot: dict[str, Any]) -> str:
    """Content-addressed USP snapshot ref per 20.102 / 20.95 canonical ordering."""
    canonical = {
        "rules": sorted(
            snapshot.get("rules", []),
            key=lambda r: (r.get("scope", ""), r.get("version", 0), r.get("rule_id", "")),
        ),
        "usp_version_id": snapshot.get("usp_version_id"),
    }
    return _canonical_digest(canonical)


@dataclass
class UspRule:
    rule_id: str
    pattern: str
    expansion: str
    state: str = "ACTIVE"
    scope: str = "conversation"
    version: int = 1
    precedence: int = 0


@dataclass
class UspSnapshot:
    usp_version_id: int
    rules: list[UspRule] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "usp_version_id": self.usp_version_id,
            "rules": [asdict(r) for r in self.rules],
        }

    @property
    def version_ref(self) -> str:
        return compute_usp_version_ref(self.to_dict())


class IIInB:
    """Deterministic input_semantic_repair stage (exploratory)."""

    def __init__(self, deterministic_mode: bool = True):
        self.deterministic_mode = deterministic_mode
        self._event_counter = 0

    def _next_event_id(self, cycle_id: str) -> str:
        self._event_counter += 1
        if self.deterministic_mode:
            return f"iiinb-evt-{cycle_id}-{self._event_counter:04d}"
        return str(uuid.uuid4())

    def _segment_intake(self, canonical_content: str) -> list[dict[str, Any]]:
        """Deterministic whitespace token segmentation."""
        tokens = canonical_content.split()
        segments: list[dict[str, Any]] = []
        for idx, token in enumerate(tokens):
            if len(segments) >= MAX_SEGMENTS:
                break
            clean = re.sub(r"^[^a-z0-9]+|[^a-z0-9]+$", "", token.lower())
            if not clean:
                continue
            segments.append(
                {
                    "segment_ref": f"seg-{idx + 1:03d}",
                    "segment_text": clean,
                    "segment_class": "SHORTHAND_ELIGIBLE",
                }
            )
        return segments

    def _active_rules(self, snapshot: UspSnapshot) -> list[UspRule]:
        active = [r for r in snapshot.rules if r.state == "ACTIVE"]
        return sorted(active, key=lambda r: (-r.precedence, -r.version, r.rule_id))

    def _envelope_snapshot(self, tp_state: dict[str, Any]) -> dict[str, str]:
        return {
            "semantic_core": json.dumps(tp_state.get("semantic_core", {}), sort_keys=True),
            "tp_tr": json.dumps(tp_state.get("tp_tr", {}), sort_keys=True),
            "exec_plan": json.dumps(tp_state.get("exec_plan", {}), sort_keys=True),
            "exec_trace": json.dumps(tp_state.get("exec_trace", {}), sort_keys=True),
        }

    def _envelope_guard(self, before: dict[str, str], after: dict[str, str]) -> dict[str, bool]:
        guard = {key: before[key] == after[key] for key in before}
        guard["semantic_core_unchanged"] = guard["semantic_core"]
        guard["tp_tr_unchanged"] = guard["tp_tr"]
        guard["exec_plan_unchanged"] = guard["exec_plan"]
        guard["exec_trace_unchanged"] = guard["exec_trace"]
        return guard

    def export_repair_diagnostics(self, records: list[dict[str, Any]]) -> str:
        """Deterministic diagnostic export for MB consumption (HLR-20.101-027, 028)."""
        ordered = sorted(
            records,
            key=lambda r: (r.get("cycle_id", ""), r.get("iiinb_event_id", "")),
        )
        return json.dumps(ordered, sort_keys=True, separators=(",", ":"))

    def repair_pass(
        self,
        inb_output: dict[str, Any],
        *,
        profile_enabled: bool,
        usp_snapshot: Optional[UspSnapshot] = None,
        cycle_id: str = "cycle-001",
        input_packet_id: str = "pkt-001",
        tp_state: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Run one input_semantic_repair pass.

        Writes only intake-bound TP fields. Never mutates semantic_core or TP.TR.
        """
        tp_state = tp_state or {
            "semantic_core": {},
            "tp_tr": {},
            "exec_plan": {},
            "exec_trace": {},
            "input_repair_tags": [],
            "input_segments": [],
            "iiinb_escalation_refs": [],
        }

        envelope_before = self._envelope_snapshot(tp_state)

        if not profile_enabled:
            _assert_reason_code("PROFILE_DISABLED")
            return {
                "skipped": True,
                "stage": None,
                "usp_loaded": False,
                "handoff_next_stage": "routing",
                "tp_intake_fields": {},
                "iiinb_repair_record": None,
                "envelope_guard": self._envelope_guard(envelope_before, envelope_before),
                "reason_codes": ["PROFILE_DISABLED"],
            }

        if inb_output.get("provenance", {}).get("outcome") != "accepted":
            _assert_reason_code("INB_HANDOFF_REJECTED")
            return {
                "skipped": True,
                "stage": "input_semantic_repair",
                "usp_loaded": False,
                "handoff_next_stage": "routing",
                "tp_intake_fields": {},
                "iiinb_repair_record": None,
                "error": "inb_not_accepted",
                "envelope_guard": self._envelope_guard(envelope_before, envelope_before),
                "reason_codes": ["INB_HANDOFF_REJECTED"],
            }

        if usp_snapshot is None:
            _assert_reason_code("USP_LOAD_FAILED")
            return {
                "skipped": False,
                "stage": "input_semantic_repair",
                "usp_loaded": False,
                "handoff_next_stage": "routing",
                "tp_intake_fields": {},
                "iiinb_repair_record": None,
                "error": "usp_load_failed",
                "envelope_guard": self._envelope_guard(envelope_before, envelope_before),
                "reason_codes": ["USP_LOAD_FAILED"],
            }

        usp_ref = usp_snapshot.version_ref
        event_id = self._next_event_id(cycle_id)
        canonical = inb_output.get("canonical_content", "") or ""
        segments = self._segment_intake(canonical)
        cap_status = "OK"
        reason_codes: list[str] = []

        if len(canonical.split()) > MAX_SEGMENTS:
            cap_status = "SEGMENT_CAP"
            _assert_reason_code("SEGMENT_CAP")
            reason_codes.append("SEGMENT_CAP")

        rules = self._active_rules(usp_snapshot)
        repair_tags: list[dict[str, Any]] = []
        escalation_refs: list[dict[str, Any]] = []
        applied_count = 0
        outcomes: list[str] = []

        for seg in segments:
            matched: Optional[UspRule] = None
            for rule in rules:
                if rule.pattern == seg["segment_text"]:
                    matched = rule
                    break

            if matched and applied_count < MAX_RULE_APPLICATIONS:
                resolved = matched.expansion
                repair_tags.append(
                    {
                        "segment_ref": seg["segment_ref"],
                        "repair_outcome": "APPLIED",
                        "rule_id": matched.rule_id,
                        "resolved_segment_ref": f"res-{seg['segment_ref']}",
                        "usp_version_ref": usp_ref,
                        "iiinb_event_id": event_id,
                    }
                )
                seg["repair_outcome"] = "APPLIED"
                seg["iiinb_event_id"] = event_id
                applied_count += 1
                outcomes.append("APPLIED")
            else:
                if matched and applied_count >= MAX_RULE_APPLICATIONS:
                    cap_status = "APPLY_CAP"
                    _assert_reason_code("APPLY_CAP")
                    reason_codes.append("APPLY_CAP")
                    outcomes.append("TRUNCATED")
                else:
                    _assert_reason_code("NO_MATCHING_RULE")
                    repair_tags.append(
                        {
                            "segment_ref": seg["segment_ref"],
                            "repair_outcome": "ESCALATED",
                            "usp_version_ref": usp_ref,
                            "iiinb_event_id": event_id,
                        }
                    )
                    escalation_refs.append(
                        {
                            "escalation_id": f"esc-{seg['segment_ref']}",
                            "segment_ref": seg["segment_ref"],
                            "iiinb_event_id": event_id,
                            "escalation_reason_code": "NO_MATCHING_RULE",
                        }
                    )
                    seg["repair_outcome"] = "ESCALATED"
                    seg["iiinb_event_id"] = event_id
                    outcomes.append("ESCALATED")

        tp_intake = {
            "input_segments": segments,
            "input_repair_tags": repair_tags,
            "iiinb_escalation_refs": escalation_refs,
        }

        record = {
            "iiinb_event_id": event_id,
            "cycle_id": cycle_id,
            "input_packet_id": input_packet_id,
            "usp_version_ref": usp_ref,
            "profile_enabled": True,
            "segment_count": len(segments),
            "applied_rule_count": applied_count,
            "repair_outcomes": outcomes,
            "rule_ids": sorted(
                [t["rule_id"] for t in repair_tags if t.get("rule_id")],
            ),
            "escalation_refs": [e["escalation_id"] for e in escalation_refs],
            "cap_status": cap_status,
            "tcu_cost": len(segments) + applied_count,
            "reason_codes": sorted(set(reason_codes)),
            "rationale_codes": [],
        }

        # Apply intake-bound writes only
        tp_state["input_segments"] = segments
        tp_state["input_repair_tags"] = repair_tags
        tp_state["iiinb_escalation_refs"] = escalation_refs

        envelope_after = self._envelope_snapshot(tp_state)
        guard = self._envelope_guard(envelope_before, envelope_after)

        return {
            "skipped": False,
            "stage": "input_semantic_repair",
            "usp_loaded": True,
            "usp_version_ref": usp_ref,
            "handoff_next_stage": "routing",
            "tp_intake_fields": tp_intake,
            "iiinb_repair_record": record,
            "audit_records": [record],
            "envelope_guard": guard,
            "reason_codes": sorted(set(reason_codes)),
            "state_digest": _canonical_digest(
                {"record": record, "tp_intake_fields": tp_intake}
            ),
        }


def run_intake_path(
    inb_output: dict[str, Any],
    *,
    profile_enabled: bool,
    usp_snapshot: Optional[UspSnapshot] = None,
    cycle_id: str = "cycle-001",
) -> dict[str, Any]:
    """Minimal InB -> IIInB -> RB path recorder for replay fixtures."""
    stages: list[dict[str, Any]] = [
        {"stage_name": "inb_surface_norm", "pipeline_id": "A", "outcome": inb_output.get("provenance", {})}
    ]

    iiinb = IIInB()
    repair = iiinb.repair_pass(
        inb_output,
        profile_enabled=profile_enabled,
        usp_snapshot=usp_snapshot,
        cycle_id=cycle_id,
    )

    if profile_enabled and not repair.get("skipped"):
        stages.append(
            {
                "stage_name": "input_semantic_repair",
                "pipeline_id": "A",
                "iiinb_repair_record": repair.get("iiinb_repair_record"),
                "tp_intake_fields": repair.get("tp_intake_fields"),
            }
        )

    stages.append({"stage_name": "routing", "pipeline_id": "A", "handoff": "rb"})

    return {
        "intake_path": stages,
        "repair_result": repair,
        "profile_enabled": profile_enabled,
        "usp_loaded": repair.get("usp_loaded", False),
    }