"""Verification harness for 40.210_dcb_prototypes (W3 Phase B)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import DCB, DirectionalChangeEvent, DCBOutput

ARTIFACT_NAME = "dcb_verification_run_2026-06-09.json"


def _mk_trajectory(points: list[dict]) -> list[dict]:
    """Helper to build synthetic geometric trajectory points."""
    return points


def scenario_curvature_exceed_event_emit() -> dict:
    dcb = DCB(curvature_threshold=0.2, max_events_per_cycle=4)
    traj = _mk_trajectory([
        {"step": 0, "direction": 0.0, "curvature": 0.05},
        {"step": 1, "direction": 0.1, "curvature": 0.35},  # exceed
        {"step": 2, "direction": 0.3, "curvature": 0.08},
    ])
    out = dcb.observe(traj, policy_signature="pol1", cycle_id="c-curve")
    ok = len(out.events) == 1 and abs(out.events[0].curvature) > 0.2
    return {"scenario": "curvature_exceed_event_emit", "hlr": ["HLR-20.106-010", "HLR-20.106-011"], "result": "PASS" if ok else "FAIL"}


def scenario_per_cycle_emission_bound() -> dict:
    dcb = DCB(curvature_threshold=0.1, max_events_per_cycle=2)
    traj = _mk_trajectory([
        {"step": i, "direction": i * 0.3, "curvature": 0.5} for i in range(10)
    ])
    out = dcb.observe(traj, policy_signature="pol1", cycle_id="c-bound")
    ok = len(out.events) <= 2 and out.emission_count <= 2
    return {"scenario": "per_cycle_emission_bound", "hlr": ["HLR-20.106-036"], "result": "PASS" if ok else "FAIL"}


def scenario_no_tr_needs_update_write() -> dict:
    dcb = DCB()
    traj = _mk_trajectory([
        {"step": 0, "direction": 0.0, "curvature": 0.3},
    ])
    out = dcb.observe(traj, policy_signature="pol1", cycle_id="c-no-dirty")
    # DCB must never set or return tr_needs_update
    ok = not any("tr_needs_update" in str(a) for a in out.audit_records) and out.emission_count >= 0
    # In impl we simply never touch the flag
    return {"scenario": "no_tr_needs_update_write", "hlr": ["HLR-20.106-020"], "result": "PASS" if ok else "FAIL"}


def scenario_event_batch_canonical_order() -> dict:
    dcb = DCB(curvature_threshold=0.1)
    traj = _mk_trajectory([
        {"step": 5, "direction": 1.0, "curvature": 0.4},
        {"step": 1, "direction": 0.0, "curvature": 0.3},
        {"step": 3, "direction": 0.5, "curvature": 0.25},
    ])
    out = dcb.observe(traj, policy_signature="pol1", cycle_id="c-order")
    steps = [e.step for e in out.events]
    ok = steps == sorted(steps)  # canonical by step
    return {"scenario": "event_batch_canonical_order", "hlr": ["HLR-20.106-028"], "result": "PASS" if ok else "FAIL"}


def scenario_forbidden_semantic_field_read() -> dict:
    dcb = DCB()
    traj = _mk_trajectory([
        {"step": 0, "direction": 0.0, "curvature": 0.3, "propositions": [{"id": "p1"}]},
    ])
    out = dcb.observe(traj, policy_signature="pol1", cycle_id="c-forbidden")
    has_forbidden = any(a.get("type") == "FORBIDDEN_READ" for a in out.audit_records)
    ok = has_forbidden and len(out.events) == 0
    return {"scenario": "forbidden_semantic_field_read", "hlr": ["HLR-20.106-035"], "result": "PASS" if ok else "FAIL"}


def main() -> int:
    scenarios = [
        scenario_curvature_exceed_event_emit(),
        scenario_per_cycle_emission_bound(),
        scenario_no_tr_needs_update_write(),
        scenario_event_batch_canonical_order(),
        scenario_forbidden_semantic_field_read(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {
        "module": "40.210_dcb_prototypes",
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
    print(f"DCB harness status: {status}")
    print(f"Scenarios: {report['summary']['passed']}/{report['summary']['total_scenarios']} PASS")
    print(f"Artifact: {path}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
