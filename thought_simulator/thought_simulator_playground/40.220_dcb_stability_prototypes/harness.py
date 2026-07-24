"""Verification harness for 40.220_dcb_stability_prototypes (W3 Phase B extension).

Per 20.165: qualitative-only stability observer over DCB (40.210) events and geometry.
All scenarios remain strictly qualitative — no numeric thresholds asserted.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import DCBStabilityObserver

ARTIFACT_NAME = "dcb_stability_verification_run_2026-06-09.json"


def _mk_events(curvatures: list[float]) -> list[dict]:
    return [{"step": i, "curvature": c, "direction_delta": 0.1} for i, c in enumerate(curvatures)]


def _mk_trajectory(length: int, direction_deltas: list[float] | None = None) -> list[dict]:
    if direction_deltas is None:
        direction_deltas = [0.05] * length
    return [{"step": i, "direction": sum(direction_deltas[:i+1])} for i in range(length)]


def scenario_non_amplifying_stable() -> dict:
    obs = DCBStabilityObserver()
    events = _mk_events([0.1, 0.12, 0.11, 0.13, 0.12])
    traj = _mk_trajectory(5)
    report = obs.assess(events, traj, policy_signature="pol1", cycle_id="c-stable")
    ok = report.overall == "stable" and "no_clear_amplification" in report.curvature_amplification
    return {"scenario": "non_amplifying_stable_sequence", "hlr": ["HLR-20.165-001"], "result": "PASS" if ok else "FAIL"}


def scenario_no_oscillation_or_runaway() -> dict:
    obs = DCBStabilityObserver()
    events = _mk_events([0.1, 0.15, 0.12, 0.14, 0.11, 0.13])
    traj = _mk_trajectory(6)
    report = obs.assess(events, traj, policy_signature="pol1", cycle_id="c-bounded")
    ok = report.overall == "stable" and "no_oscillation_detected" in report.oscillation_runaway
    return {"scenario": "bounded_no_runaway", "hlr": ["HLR-20.165-002"], "result": "PASS" if ok else "FAIL"}


def scenario_observer_read_only_no_recursive() -> dict:
    obs = DCBStabilityObserver()
    events = _mk_events([0.2, 0.18, 0.19])
    traj = _mk_trajectory(3)
    # capture input identity
    events_before = json.dumps(events, sort_keys=True)
    traj_before = json.dumps(traj, sort_keys=True)
    report = obs.assess(events, traj, policy_signature="pol1", cycle_id="c-readonly")
    events_after = json.dumps(events, sort_keys=True)
    traj_after = json.dumps(traj, sort_keys=True)
    ok = (report.recursive_modification == "no_recursive_modification_observed"
          and events_before == events_after and traj_before == traj_after)
    return {"scenario": "read_only_no_recursive_modification", "hlr": ["HLR-20.165-003"], "result": "PASS" if ok else "FAIL"}


def scenario_contraction_preserved() -> dict:
    obs = DCBStabilityObserver()
    events = _mk_events([0.05, 0.06, 0.04, 0.07])  # low relative to steps
    traj = _mk_trajectory(10)
    report = obs.assess(events, traj, policy_signature="pol1", cycle_id="c-contraction")
    ok = "contraction_appears_preserved" in report.contraction_preserved
    return {"scenario": "contraction_preserved_bounded_influence", "hlr": ["HLR-20.165-004"], "result": "PASS" if ok else "FAIL"}


def scenario_replay_identical_qualitative_verdict() -> dict:
    obs = DCBStabilityObserver()
    events = _mk_events([0.1, 0.09, 0.11, 0.08])
    traj = _mk_trajectory(4)
    r1 = obs.assess_replay(events, traj, policy_signature="pol-replay")
    r2 = obs.assess_replay(events, traj, policy_signature="pol-replay")
    ok = json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)
    return {"scenario": "replay_identical_qualitative_assessment", "hlr": ["HLR-20.165-006"], "result": "PASS" if ok else "FAIL"}


def main() -> int:
    scenarios = [
        scenario_non_amplifying_stable(),
        scenario_no_oscillation_or_runaway(),
        scenario_observer_read_only_no_recursive(),
        scenario_contraction_preserved(),
        scenario_replay_identical_qualitative_verdict(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {
        "module": "40.220_dcb_stability_prototypes",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "phase": "B",
        "status": status,
        "scenarios": scenarios,
        "summary": {
            "total_scenarios": len(scenarios),
            "passed": sum(1 for s in scenarios if s["result"] == "PASS"),
        },
    }
    report["summary"]["failed_scenarios"] = [s["scenario"] for s in scenarios if s["result"] != "PASS"]
    artifact_dir = Path(__file__).resolve().parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    path = artifact_dir / ARTIFACT_NAME
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(f"DCB Stability harness status: {status}")
    print(f"Scenarios: {report['summary']['passed']}/{report['summary']['total_scenarios']} PASS")
    print(f"Artifact: {path}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
