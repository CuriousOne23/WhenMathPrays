"""DCB (Directional Change Basin) prototype for 40.210_dcb_prototypes (W3).

Per 20.106: geometric meta-basin for trajectory observation.
- Observes only persisted geometric fields (position, direction, curvature) from TP/MTP trajectory projections.
- Emits ephemeral directional-change events when curvature exceeds bounded geometric invariant.
- Events are finite per cycle (non-expansive bound).
- Events are canonical-ordered, geometric-only (no semantic labels).
- Strictly no writes to TP (no tr_needs_update, no persistence of events).
- Forbidden: any read of semantic fields (propositions, truth_hypotheses, routing_metadata, etc.) triggers audit and degrade.
- All emission deterministic and replayable.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DirectionalChangeEvent:
    step: int
    curvature: float
    direction_delta: float
    position: list[float] | None = None
    rationale: str = "curvature_exceed"

    def as_dict(self) -> dict[str, Any]:
        d = {
            "step": self.step,
            "curvature": round(self.curvature, 6),
            "direction_delta": round(self.direction_delta, 6),
            "rationale": self.rationale,
        }
        if self.position:
            d["position"] = [round(x, 6) for x in self.position]
        return d


@dataclass
class DCBOutput:
    events: list[DirectionalChangeEvent] = field(default_factory=list)
    audit_records: list[dict[str, Any]] = field(default_factory=list)
    emission_count: int = 0
    policy_signature: str = ""
    cycle_id: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "events": [e.as_dict() for e in self.events],
            "audit_records": self.audit_records,
            "emission_count": self.emission_count,
            "policy_signature": self.policy_signature,
            "cycle_id": self.cycle_id,
        }


class DCB:
    """Geometric trajectory observer. Emits ephemeral directional-change events for TR only."""

    def __init__(self, max_events_per_cycle: int = 4, curvature_threshold: float = 0.25):
        self.max_events_per_cycle = max_events_per_cycle
        self.curvature_threshold = curvature_threshold
        self._last_output: DCBOutput | None = None

    def observe(
        self,
        trajectory: list[dict[str, Any]],
        *,
        policy_signature: str = "default",
        cycle_id: str = "",
    ) -> DCBOutput:
        audit: list[dict[str, Any]] = []
        events: list[DirectionalChangeEvent] = []

        # Forbidden semantic field check (HLR-20.106-035)
        forbidden = ["propositions", "truth_hypotheses", "messy_input_record", "routing_metadata", "thought_router_fields", "exec_plan"]
        for rec in trajectory:
            for f in forbidden:
                if f in rec:
                    audit.append({
                        "type": "FORBIDDEN_READ",
                        "field": f,
                        "detail": "HLR-20.106-035: DCB must observe only geometric trajectory fields",
                    })
                    # Degrade: no events on forbidden read
                    out = DCBOutput(
                        events=[],
                        audit_records=audit,
                        emission_count=0,
                        policy_signature=policy_signature,
                        cycle_id=cycle_id,
                    )
                    self._last_output = out
                    return out

        # Simple geometric observation (synthetic trajectory points with direction/curvature)
        # trajectory items expected to have: step, direction (float), curvature (float), position (optional list)
        prev_dir = None
        for i, rec in enumerate(trajectory):
            step = rec.get("step", i)
            direction = float(rec.get("direction", 0.0))
            curvature = float(rec.get("curvature", 0.0))
            position = rec.get("position")

            # Compute delta if not provided
            direction_delta = abs(direction - (prev_dir or direction))
            if prev_dir is not None:
                direction_delta = abs(direction - prev_dir)

            # Emit on curvature exceed (bounded invariant)
            if abs(curvature) > self.curvature_threshold:
                if len(events) < self.max_events_per_cycle:
                    evt = DirectionalChangeEvent(
                        step=step,
                        curvature=curvature,
                        direction_delta=direction_delta,
                        position=position,
                        rationale="curvature_exceed",
                    )
                    events.append(evt)
                else:
                    # bound hit — still record but do not emit more (per-cycle bound)
                    pass

            prev_dir = direction

        # Enforce per-cycle bound (HLR-20.106-036)
        if len(events) > self.max_events_per_cycle:
            events = events[: self.max_events_per_cycle]
            audit.append({
                "type": "EMISSION_BOUND",
                "count": len(events),
                "limit": self.max_events_per_cycle,
                "detail": "per-cycle emission bound enforced",
            })

        # Canonical order (by step, then curvature for determinism)
        events.sort(key=lambda e: (e.step, abs(e.curvature)))

        out = DCBOutput(
            events=events,
            audit_records=audit,
            emission_count=len(events),
            policy_signature=policy_signature,
            cycle_id=cycle_id,
        )
        self._last_output = out
        return out

    def get_last_output(self) -> dict[str, Any] | None:
        return self._last_output.as_dict() if self._last_output else None
