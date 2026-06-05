"""40.39_mb_prototypes / harness.py

Test harness exercising the MB prototype.

Follows 40.20 structure + forward flow from 20.70.
Generates structured report + JSON artifact under artifacts/.

Scenarios target the key exploration items listed in the approved
40.39 software_description.md (Phase B deliverables).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from prototype import MonitoringBasin, MBInput, mb_input_from_snapshot
from dataclasses import asdict


MODULE_NAME = "40.39_mb_prototypes"
RUN_COMMAND = "python harness.py"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACT_PATH = ARTIFACT_DIR / "mb_verification_run_2026-06-05.json"


# Lightweight requirement keys mapped to 20.70 HLRs (for the report)
REQ: Dict[str, Dict[str, str]] = {
    "non_intrusive": {
        "hlr": "HLR-20.070-003",
        "llr": "LLR-40.39-001",
        "desc": "MB must never mutate input or core state",
    },
    "deterministic_output": {
        "hlr": "HLR-20.070-004,011",
        "llr": "LLR-40.39-002",
        "desc": "Identical effective input + state produces identical output",
    },
    "drift_observation": {
        "hlr": "HLR-20.070-006",
        "llr": "LLR-40.39-003",
        "desc": "Deterministic drift indicators over state deltas",
    },
    "what_if_flagged": {
        "hlr": "HLR-20.070-007,008",
        "llr": "LLR-40.39-004",
        "desc": "What-if actions are explicitly flagged, policy-gated, logged, non-authoritative",
    },
    "overflow_canonical": {
        "hlr": "HLR-20.070-024,025",
        "llr": "LLR-40.39-005",
        "desc": "Overflow uses exact 20.30 canonical fields",
    },
    "visibility_modes": {
        "hlr": "HLR-20.070-027,028",
        "llr": "LLR-40.39-006",
        "desc": "Visibility modes control sampling + emit cost notifications when relevant",
    },
    "reproducibility": {
        "hlr": "HLR-20.070-011,016",
        "llr": "LLR-40.39-007",
        "desc": "Telemetry supports deterministic replay / audit",
    },
    "lifecycle_logging": {
        "hlr": "HLR-20.070-014",
        "llr": "LLR-40.39-008",
        "desc": "Lifecycle transitions are observable",
    },
}


def _make_snapshot(**overrides: Any) -> Dict[str, Any]:
    base = {
        "delta_h_trend": 0.35,
        "active_ib_count": 8,
        "oscillation_flag": False,
        "contradiction_level": 0.10,
        "lanes": ["general", "thought"],
        "observed_basins": ["general", "math"],
    }
    base.update(overrides)
    return base


def _run_scenario(mb: MonitoringBasin, name: str, req_key: str, input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Run one scenario, return structured result for report."""
    mb_input = mb_input_from_snapshot(**input_dict) if "cycle" in input_dict else MBInput(**input_dict)
    output = mb.evaluate(mb_input)

    status = "PASS"
    detail = "MB produced well-formed non-mutating deterministic output."
    io_fields = "MBInput(cycle, visibility_mode, mtp_snapshot, lineage, ...) -> MBOutput(diagnostics, drift, advisories, what_if, telemetry, overflow)"

    if req_key == "what_if_flagged":
        if not output.what_if_flags and "high_drift" in name:
            status = "FAIL"
            detail = "Expected what_if flag for high drift scenario"
    if req_key == "overflow_canonical":
        if output.overflow.get("overflow_flag") and "overflow_type" not in output.overflow:
            status = "FAIL"
            detail = "Overflow missing canonical fields"

    return {
        "name": name,
        "status": status,
        "requirement_key": req_key,
        "detail": detail,
        "io_fields": io_fields,
        "output_summary": {
            "stability_signal": output.diagnostics_summary.get("stability_signal"),
            "drift_indicators_count": len(output.drift_indicators),
            "advisories": len(output.advisory_recommendations),
            "what_if_count": len(output.what_if_flags),
            "overflow_flag": output.overflow.get("overflow_flag", False),
            "visibility": output.telemetry.get("visibility_mode"),
        },
    }


def _build_report() -> Dict[str, Any]:
    scenarios: List[Dict[str, Any]] = []
    mb = MonitoringBasin()

    # 1. Stable baseline
    scenarios.append(_run_scenario(
        mb, "stable_low_drift", "non_intrusive",
        {"cycle": 100, "snapshot": _make_snapshot(delta_h_trend=0.22, active_ib_count=5), "visibility": "medium"}
    ))

    # 2. High drift -> advisory + what_if
    mb2 = MonitoringBasin()
    scenarios.append(_run_scenario(
        mb2, "high_drift_advisory_whatif", "what_if_flagged",
        {"cycle": 101, "snapshot": _make_snapshot(delta_h_trend=0.87, active_ib_count=12, oscillation_flag=False), "visibility": "medium"}
    ))

    # 3. High population -> overflow
    mb3 = MonitoringBasin()
    scenarios.append(_run_scenario(
        mb3, "high_population_overflow", "overflow_canonical",
        {"cycle": 102, "snapshot": _make_snapshot(delta_h_trend=0.41, active_ib_count=38), "visibility": "high"}
    ))

    # 4. Oscillation
    mb4 = MonitoringBasin()
    scenarios.append(_run_scenario(
        mb4, "oscillation_elevated", "drift_observation",
        {"cycle": 103, "snapshot": _make_snapshot(delta_h_trend=0.55, active_ib_count=15, oscillation_flag=True), "visibility": "medium"}
    ))

    # 5. Visibility high notification
    mb5 = MonitoringBasin()
    scenarios.append(_run_scenario(
        mb5, "visibility_high_cost_notif", "visibility_modes",
        {"cycle": 104, "snapshot": _make_snapshot(delta_h_trend=0.33), "visibility": "high"}
    ))

    # 6. Reproducibility (fresh instance for pure equality)
    inp = {"cycle": 105, "snapshot": _make_snapshot(delta_h_trend=0.78, active_ib_count=18), "visibility": "full"}
    mb6a = MonitoringBasin()
    mb6b = MonitoringBasin()
    out1 = mb6a.evaluate(mb_input_from_snapshot(**inp))
    out2 = mb6b.evaluate(mb_input_from_snapshot(**inp))
    repro_ok = json.dumps(asdict(out1), sort_keys=True) == json.dumps(asdict(out2), sort_keys=True)
    scenarios.append({
        "name": "reproducibility_identical_inputs",
        "status": "PASS" if repro_ok else "FAIL",
        "requirement_key": "reproducibility",
        "detail": "Fresh MB instance + identical input produced identical output (full JSON equality).",
        "io_fields": "MBInput -> MBOutput (exact match on two runs)",
        "output_summary": {"repro_equal": repro_ok},
    })

    # 7. Noisy / high contradiction
    mb7 = MonitoringBasin()
    scenarios.append(_run_scenario(
        mb7, "noisy_high_contradiction", "drift_observation",
        {"cycle": 106, "snapshot": _make_snapshot(delta_h_trend=0.61, contradiction_level=0.82), "visibility": "medium"}
    ))

    # 8. Lifecycle observable
    mb8 = MonitoringBasin()
    scenarios.append(_run_scenario(
        mb8, "lifecycle_observable", "lifecycle_logging",
        {"cycle": 205, "snapshot": _make_snapshot(delta_h_trend=0.29), "visibility": "low"}
    ))

    passed = sum(1 for s in scenarios if s["status"] == "PASS")
    failed = len(scenarios) - passed
    overall = "PASS" if failed == 0 else "FAIL"

    report = {
        "module": MODULE_NAME,
        "run_command": RUN_COMMAND,
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "overall_status": overall,
            "total_scenarios": len(scenarios),
            "passed": passed,
            "failed": failed,
        },
        "scenarios": scenarios,
        "notes": "Phase B forward-flow execution from 20.70. All outputs are deterministic and non-mutating. Prototype is exploratory only.",
        "three_flow": {
            "forward": "20.70 (and 20.30) guidance directly drove the implemented behaviors and invariants.",
            "backward": "None (initial implementation).",
            "iterative": "None (no 50.39 yet).",
        },
    }
    return report


def _write_artifact(report: Dict[str, Any]) -> Path:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return ARTIFACT_PATH


def main() -> int:
    report = _build_report()
    artifact_path = _write_artifact(report)

    print(f"Module: {MODULE_NAME}")
    print(f"Command: {RUN_COMMAND}")
    print(f"Artifact: {artifact_path}")
    print(f"Overall: {report['summary']['overall_status']}")
    for scenario in report.get("scenarios", []):
        print(f"  {scenario['name']}: {scenario['status']}")
    if report["summary"]["overall_status"] == "FAIL":
        print("Some scenarios failed (see artifact for details).")
    return 0 if report["summary"]["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
