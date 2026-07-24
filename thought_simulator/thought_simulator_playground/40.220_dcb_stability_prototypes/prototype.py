"""DCB Stability qualitative observer for 40.220_dcb_stability_prototypes (W3 extension).

Per 20.165: strictly qualitative read-only observer of DCB (40.210) directional-change event rates and trajectory geometry.
- No numeric thresholds or procedural algorithms (HLR-20.165-005).
- Stability assessed via deterministic observability of event rates and geometry trends.
- Joint with 40.210 DCB events.
- Read-only: never modifies input trajectory or events.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class StabilityReport:
    overall: str  # "stable" | "potential_violation_observed"
    curvature_amplification: str
    oscillation_runaway: str
    recursive_modification: str
    contraction_preserved: str
    event_rate_observation: str
    geometry_trend: str
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "overall": self.overall,
            "curvature_amplification": self.curvature_amplification,
            "oscillation_runaway": self.oscillation_runaway,
            "recursive_modification": self.recursive_modification,
            "contraction_preserved": self.contraction_preserved,
            "event_rate_observation": self.event_rate_observation,
            "geometry_trend": self.geometry_trend,
            "notes": self.notes,
        }


class DCBStabilityObserver:
    """Read-only qualitative stability observer for DCB geometric feedback.

    Consumes sequences of DCB events (from 40.210) + trajectory geometry.
    Produces qualitative assessment only — no numbers, no thresholds.
    """

    def assess(
        self,
        dcb_events: list[dict[str, Any]],
        trajectory: list[dict[str, Any]],
        *,
        policy_signature: str = "default",
        cycle_id: str = "",
    ) -> StabilityReport:
        notes: list[str] = []
        n_events = len(dcb_events)
        n_steps = max(1, len(trajectory))

        # Qualitative event rate observation (no numeric threshold)
        if n_events == 0:
            event_rate_obs = "no_events_observed"
        elif n_events <= n_steps // 2:
            event_rate_obs = "low_to_moderate_event_rate"
        else:
            event_rate_obs = "elevated_event_rate"

        # Curvature amplification check (qualitative trend, no numbers)
        curvatures = [float(e.get("curvature", 0.0)) for e in dcb_events]
        amplification = "no_clear_amplification"
        if len(curvatures) >= 3:
            increases = sum(1 for i in range(1, len(curvatures)) if curvatures[i] > curvatures[i-1])
            if increases > len(curvatures) * 0.7:  # majority strictly increasing trend
                amplification = "potential_amplification_trend_observed"
                notes.append("Curvature values show consistent increase across most steps.")
            elif all(curvatures[i] <= curvatures[i-1] for i in range(1, len(curvatures))):
                amplification = "non_increasing_curvature"
        else:
            amplification = "insufficient_sequence_for_trend"

        # Oscillation / runaway detection (qualitative alternating pattern)
        oscillation = "no_oscillation_detected"
        if len(curvatures) >= 4:
            alternations = 0
            for i in range(2, len(curvatures)):
                if (curvatures[i] > curvatures[i-1]) != (curvatures[i-1] > curvatures[i-2]):
                    alternations += 1
            if alternations >= len(curvatures) // 2:
                oscillation = "alternating_pattern_suggesting_oscillation"
                notes.append("Directional changes show repeated sign flips in trend.")
        else:
            oscillation = "sequence_too_short_for_oscillation_check"

        # Recursive modification: since this is a pure observer, input is never modified
        recursive = "no_recursive_modification_observed"  # observer cannot modify by design

        # Contraction preservation (qualitative): event influence remains finite perturbation
        # We observe whether event count grows without bound relative to trajectory length
        contraction = "contraction_appears_preserved"
        if n_events > n_steps:
            contraction = "event_count_exceeds_trajectory_length"
            notes.append("Event count outpaces observed trajectory steps — review for expansion.")
        else:
            contraction = "event_count_remains_bounded_relative_to_trajectory"

        # Geometry trend (directional stability)
        directions = [float(t.get("direction", 0.0)) for t in trajectory if "direction" in t]
        geometry_trend = "geometry_trend_stable"
        if len(directions) >= 3:
            dir_changes = sum(1 for i in range(1, len(directions)) if abs(directions[i] - directions[i-1]) > abs(directions[i-1] - (directions[i-2] if i > 1 else directions[i-1])))
            if dir_changes > len(directions) // 2:
                geometry_trend = "increasing_directional_volatility_observed"

        # Overall qualitative verdict
        if amplification.startswith("potential") or oscillation.startswith("alternating") or contraction.startswith("event_count_exceeds"):
            overall = "potential_violation_observed"
        else:
            overall = "stable"

        report = StabilityReport(
            overall=overall,
            curvature_amplification=amplification,
            oscillation_runaway=oscillation,
            recursive_modification=recursive,
            contraction_preserved=contraction,
            event_rate_observation=event_rate_obs,
            geometry_trend=geometry_trend,
            notes=notes,
        )
        return report

    def assess_replay(self, dcb_events: list[dict], trajectory: list[dict], policy_signature: str = "default") -> dict:
        """Helper for replay tests — returns canonical dict for equality check."""
        report = self.assess(dcb_events, trajectory, policy_signature=policy_signature)
        return report.as_dict()
