"""RB (Routing Basin) prototype for 40.190_rb_prototypes (W3).

Per 20.50: deterministic post-intake (InB / IIInB) routing fan-out.
- Computes inspectable, replayable `routing_filter` each cycle.
- TR invocation gated strictly on `tr_needs_update` (read-only; RB does not clear or write TR).
- Split/merge arbitration decisions logged under explicit policy.
- Messy-input routing preserved (no semantic smoothing or repair in RB).
- Overflow produces audit record; no silent drops.
- All outputs deterministic and seed-independent for replay.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RoutingFilter:
    selected_ob_ids: list[str] = field(default_factory=list)
    lane_projections: list[dict] = field(default_factory=list)
    delta_h_routing_context: dict[str, Any] = field(default_factory=dict)
    firing_order: list[str] = field(default_factory=list)
    transition_rationale: list[str] = field(default_factory=list)
    policy_justification: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "selected_ob_ids": self.selected_ob_ids,
            "lane_projections": self.lane_projections,
            "delta_h_routing_context": self.delta_h_routing_context,
            "firing_order": self.firing_order,
            "transition_rationale": self.transition_rationale,
            "policy_justification": self.policy_justification,
        }


@dataclass
class RBDecision:
    lane_id: str
    action: str  # "direct" | "invoke_tr" | "split_candidate" | "merge_candidate"
    rationale: str
    tr_eligible: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "lane_id": self.lane_id,
            "action": self.action,
            "rationale": self.rationale,
            "tr_eligible": self.tr_eligible,
        }


@dataclass
class RBOutput:
    routing_filter: RoutingFilter
    decisions: list[RBDecision] = field(default_factory=list)
    lanes: list[dict] = field(default_factory=list)
    audit_records: list[dict[str, Any]] = field(default_factory=list)
    policy_signature: str = ""
    cycle_id: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "routing_filter": self.routing_filter.as_dict(),
            "decisions": [d.as_dict() for d in self.decisions],
            "lanes": self.lanes,
            "audit_records": self.audit_records,
            "policy_signature": self.policy_signature,
            "cycle_id": self.cycle_id,
        }


class RoutingBasin:
    """RB routing stage: InB/IIInB → lane fan-out, TR gate, split/merge arb, overflow audit."""

    def __init__(self, max_active_lanes: int = 8):
        self.max_active_lanes = max_active_lanes
        self._last_filter: RoutingFilter | None = None

    def route(
        self,
        intake_records: list[dict[str, Any]],
        *,
        iiinb_enabled: bool = False,
        tr_needs_update: bool = False,
        policy_signature: str = "default",
        cycle_id: str = "",
        overflow_limit: int = 16,
    ) -> RBOutput:
        audit: list[dict[str, Any]] = []
        records = list(intake_records or [])

        # Overflow detection (HLR-20.050-024, 029) — audit, no silent drop
        if len(records) > overflow_limit:
            audit.append({
                "type": "OVERFLOW",
                "count": len(records),
                "limit": overflow_limit,
                "code": "RB_OVERFLOW_029",
                "detail": "fan-out bound exceeded; telemetry only, partial routing emitted",
            })

        # Deterministic routing filter (HLR-20.050-021, 022, 004, 036)
        ob_ids = sorted(str(r.get("ob_id", f"ob-{i}")) for i, r in enumerate(records))
        lane_projections = [
            {"lane_id": f"lane-{i}", "ob_id": oid, "source_index": i}
            for i, oid in enumerate(ob_ids)
        ]
        firing_order = ob_ids[:]  # stable order
        delta_h_ctx = {"h_delta": round(0.01 * len(records), 4)}

        routing_filter = RoutingFilter(
            selected_ob_ids=ob_ids,
            lane_projections=lane_projections,
            delta_h_routing_context=delta_h_ctx,
            firing_order=firing_order,
            transition_rationale=["post_intake_fanout", "iiinb" if iiinb_enabled else "inb_direct"],
            policy_justification={
                "policy": policy_signature,
                "iiinb_enabled": iiinb_enabled,
                "cycle": cycle_id,
            },
        )
        self._last_filter = routing_filter

        # Lane fan-out + decisions
        decisions: list[RBDecision] = []
        lanes: list[dict] = []

        for i, rec in enumerate(records):
            lane_id = f"lane-{i}"
            messy = rec.get("messy_input_record") or {}
            messy_note = ";messy_preserved" if messy else ""

            if tr_needs_update:
                action = "invoke_tr"
                rationale = f"tr_dirty_flag{messy_note}"
                tr_eligible = True
            else:
                action = "direct"
                rationale = f"fresh_routing{messy_note}"
                tr_eligible = False

            dec = RBDecision(
                lane_id=lane_id,
                action=action,
                rationale=rationale,
                tr_eligible=tr_eligible,
            )
            decisions.append(dec)

            lane_rec = dict(rec)  # preserve input (including messy) — no smoothing
            lane_rec["lane_id"] = lane_id
            lane_rec["routed_action"] = action
            lanes.append(lane_rec)

        # Simple split/merge arbitration signals for downstream (40.170 joint)
        if len(records) >= 4:
            decisions.append(
                RBDecision(
                    lane_id="arb",
                    action="split_candidate",
                    rationale="high_fanout_arbitration_policy",
                    tr_eligible=False,
                )
            )

        return RBOutput(
            routing_filter=routing_filter,
            decisions=decisions,
            lanes=lanes,
            audit_records=audit,
            policy_signature=policy_signature,
            cycle_id=cycle_id,
        )

    def get_last_routing_filter(self) -> dict[str, Any]:
        return self._last_filter.as_dict() if self._last_filter else {}
