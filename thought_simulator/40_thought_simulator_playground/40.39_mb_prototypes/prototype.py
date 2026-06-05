"""40.39_mb_prototypes / prototype.py

Minimal deterministic Monitoring Basin (MB) prototype.

Corresponds to 20.70_mb_requirements.md (forward flow from 20-series).
Explores non-intrusive diagnostics, drift observation, stability reporting,
bounded what-if, visibility modes, overflow telemetry, and reproducibility.

All operations are read-only on inputs. No mutation of core cognitive state.
Outputs are fully deterministic for identical inputs + internal bounded state.

Phase B implementation per 40.20 after software_description approval.
Now fully implements 10.50.39 Canonical Schemas (schema_version, full overflow, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class MBInput:
    """Canonical MB input object (per HLR-20.070-021 and 10.50.39 Canonical Schema)."""
    cycle: int
    schema_version: str = "1.0"
    visibility_mode: str = "medium"  # low | medium | high | full
    basin_telemetry: Dict[str, Any] = field(default_factory=dict)
    lane_identifiers: List[str] = field(default_factory=list)
    lineage: Dict[str, Any] = field(default_factory=dict)
    mtp_snapshot: Dict[str, Any] = field(default_factory=dict)
    stability_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MBOutput:
    """Canonical MB output object (per HLR-20.070-022 and 10.50.39 Canonical Schema)."""
    schema_version: str
    diagnostics_summary: Dict[str, Any]
    drift_indicators: List[Dict[str, Any]]
    advisory_recommendations: List[Dict[str, Any]]
    what_if_flags: List[Dict[str, Any]]
    execution_diagnostics: Dict[str, Any]
    telemetry: Dict[str, Any]
    overflow: Dict[str, Any]


class MonitoringBasin:
    """
    Deterministic MB prototype.

    - Non-intrusive: never mutates caller data.
    - Drift history bounded (eviction policy).
    - Visibility controls sampling only.
    - What-if actions always explicitly flagged + logged (non-authoritative).
    - Overflow uses exact 20.30 canonical fields.
    """

    def __init__(self, max_drift_history: int = 8):
        self._drift_history: List[Dict[str, Any]] = []
        self._max_history = max_drift_history
        self._intervention_count = 0
        self._last_cycle = -1

    def evaluate(self, mb_input: MBInput | Dict[str, Any]) -> MBOutput:
        if isinstance(mb_input, dict):
            # Accept loose dicts for harness flexibility, coerce safely
            mb_input = MBInput(
                schema_version=str(mb_input.get("schema_version", "1.0")),
                cycle=int(mb_input.get("cycle", 0)),
                visibility_mode=str(mb_input.get("visibility_mode", "medium")),
                basin_telemetry=dict(mb_input.get("basin_telemetry", {})),
                lane_identifiers=list(mb_input.get("lane_identifiers", [])),
                lineage=dict(mb_input.get("lineage", {})),
                mtp_snapshot=dict(mb_input.get("mtp_snapshot", {})),
                stability_metadata=dict(mb_input.get("stability_metadata", {})),
            )

        cycle = mb_input.cycle
        self._last_cycle = max(self._last_cycle, cycle)

        # Read-only extraction of signals (never mutate)
        delta_h = float(mb_input.mtp_snapshot.get("delta_h_trend", 0.0))
        active_ib = int(mb_input.mtp_snapshot.get("active_ib_count", 0))
        oscillation = bool(mb_input.mtp_snapshot.get("oscillation_flag", False))
        contradiction = float(mb_input.mtp_snapshot.get("contradiction_level", 0.0))

        # Deterministic drift indicator (HLR-20.070-006)
        drift_indicator = {
            "type": "delta_h_drift",
            "value": round(delta_h, 4),
            "cycle": cycle,
            "source": "mtp_snapshot",
            "lineage_ref": mb_input.lineage.get("id", "unknown") if mb_input.lineage else "unknown",
            "oscillation": oscillation,
        }
        self._drift_history.append(drift_indicator)
        if len(self._drift_history) > self._max_history:
            # bounded eviction (HLR-20.070-030)
            self._drift_history = self._drift_history[-self._max_history:]

        # Visibility mode (HLR-20.070-027/028)
        vm = (mb_input.visibility_mode or "medium").lower()
        if vm not in ("low", "medium", "high", "full"):
            vm = "medium"
        sampling = {"low": 0.25, "medium": 0.5, "high": 0.75, "full": 1.0}[vm]
        tcu_cost = round(4.0 * sampling, 2)

        user_notif = None
        if vm in ("high", "full") and tcu_cost > 2.0:
            user_notif = (
                f"MB visibility={vm} active; approx additional TCU cost ~{tcu_cost} "
                "(advisory only; does not alter core telemetry)"
            )

        # Diagnostics summary (HLR-20.070-005)
        basin_count = len(mb_input.basin_telemetry) if mb_input.basin_telemetry else 2
        diagnostics = {
            "basin_activations_observed": basin_count,
            "routing_lanes_sampled": mb_input.lane_identifiers[:3],
            "stability_signal": "elevated" if (delta_h > 0.6 or oscillation or contradiction > 0.5) else "nominal",
            "interpretation_sample_rate": "full" if sampling >= 0.75 else "light",
        }

        # Advisory recommendations + bounded what-if (HLR-20.070-007/008/026)
        advisories: List[Dict[str, Any]] = []
        what_ifs: List[Dict[str, Any]] = []

        elevated = delta_h > 0.7 or active_ib > 22 or oscillation or contradiction > 0.6
        if elevated:
            advisories.append({
                "type": "stability_monitor",
                "message": "Elevated drift / population / oscillation / contradiction observed",
                "suggested": "consider visibility bump or GB review" if vm == "low" else "log_for_supervision",
                "non_binding": True,
                "cycle": cycle,
            })

            if delta_h > 0.82:
                what_ifs.append({
                    "action": "what_if_drift_probe",
                    "flagged": True,
                    "policy_gated": "simulated_default_allow_for_exploration",
                    "logged": True,
                    "rationale": f"delta_h={delta_h:.2f}",
                    "cycle": cycle,
                    "non_authoritative": True,
                })
                self._intervention_count += 1

        # Overflow / degradation using exact canonical schema (HLR-20.070-024/025)
        # Per 10.50.39-014: always emit FULL canonical schema (no collapse when flag=false)
        is_overflow = (active_ib > 32) or (delta_h > 0.92)
        if is_overflow:
            overflow: Dict[str, Any] = {
                "overflow_flag": True,
                "overflow_type": "high_population" if active_ib > 32 else "high_drift",
                "overflow_source_basin": "MB",
                "overflow_cycle": cycle,
                "truncated_fields": ["detailed_basin_telemetry"] if vm == "full" else [],
                "ΔH%_normalization_applied": 0.0,
                "tcu_overrun_amount": round(max(0.0, (active_ib - 18) * 0.04 + (delta_h - 0.4) * 1.5), 3),
            }
        else:
            overflow = {
                "overflow_flag": False,
                "overflow_type": "none",
                "overflow_source_basin": "MB",
                "overflow_cycle": cycle,
                "truncated_fields": [],
                "ΔH%_normalization_applied": 0.0,
                "tcu_overrun_amount": 0.0,
            }

        # Execution diagnostics + lifecycle (HLR-20.070-014)
        exec_diag = {
            "cycle": cycle,
            "deterministic": True,
            "visibility_mode": vm,
            "lineage_preserved": bool(mb_input.lineage),
            "lifecycle_state": "running",
            "intervention_count_so_far": self._intervention_count,
            "drift_history_len": len(self._drift_history),
            "replay_safe": True,
        }

        # Telemetry (HLR-20.070-016/032)
        telemetry = {
            "visibility_mode": vm,
            "sampling_density": sampling,
            "tcu_cost_estimate": tcu_cost,
            "user_notification": user_notif,
            "drift_history_depth": len(self._drift_history),
            "flush_epoch": cycle // 5,  # simplistic deterministic flush
        }

        return MBOutput(
            schema_version="1.0",
            diagnostics_summary=diagnostics,
            drift_indicators=list(self._drift_history[-3:]),
            advisory_recommendations=advisories,
            what_if_flags=what_ifs,
            execution_diagnostics=exec_diag,
            telemetry=telemetry,
            overflow=overflow,
        )

    def get_state_for_debug(self) -> Dict[str, Any]:
        """Non-normative debug snapshot only."""
        return {
            "drift_history_len": len(self._drift_history),
            "intervention_count": self._intervention_count,
            "last_cycle": self._last_cycle,
        }


def mb_input_from_snapshot(
    cycle: int,
    snapshot: Dict[str, Any],
    visibility: str = "medium",
    lineage: Dict[str, Any] | None = None,
) -> MBInput:
    """Convenience constructor for harness / tests."""
    return MBInput(
        schema_version="1.0",
        cycle=cycle,
        visibility_mode=visibility,
        basin_telemetry={"observed": snapshot.get("observed_basins", ["general"])},
        lane_identifiers=snapshot.get("lanes", ["general"]),
        lineage=lineage or {"id": f"trace-{cycle}", "provenance": "harness"},
        mtp_snapshot={
            "delta_h_trend": snapshot.get("delta_h_trend", 0.0),
            "active_ib_count": snapshot.get("active_ib_count", 0),
            "oscillation_flag": snapshot.get("oscillation_flag", False),
            "contradiction_level": snapshot.get("contradiction_level", 0.0),
        },
        stability_metadata={"source": "synthetic"},
    )
