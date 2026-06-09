"""Verification harness for 40.200_ob_prototypes (W3 Phase B)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import ObjectBasin, OBOutput

ARTIFACT_NAME = "ob_verification_run_2026-06-09.json"


def _mk_lane_view(lane_id: str, content: str = "", propositions: list | None = None,
                  change: bool = False, messy: dict | None = None,
                  truth_hypotheses: list | None = None, overflow: bool = False) -> dict:
    view = {
        "lane_id": lane_id,
        "content": content or f"lane-content-{lane_id}",
        "propositions": propositions or [{"id": f"p-{lane_id}"}],
        "change_detected": change,
    }
    if messy:
        view["messy_input_record"] = messy
    if truth_hypotheses is not None:
        view["truth_hypotheses"] = truth_hypotheses
    if overflow:
        view["overflow"] = True
    return view


def scenario_lane_local_evidence_emit() -> dict:
    ob = ObjectBasin()
    view = _mk_lane_view("l1", content="simple statement about math")
    out = ob.process_lane(view, policy_signature="pol1", cycle_id="c-emit")
    ok = len(out.evidence_fields) >= 1 and "tr_input_fields" in out.as_dict()
    return {"scenario": "lane_local_evidence_emit", "hlr": ["HLR-20.040-001", "HLR-20.040-022"], "result": "PASS" if ok else "FAIL"}


def scenario_tr_needs_update_set_on_change() -> dict:
    ob = ObjectBasin()
    view = _mk_lane_view("l2", change=True, propositions=[{"id": "p1"}, {"id": "p2"}, {"id": "p3"}])
    out = ob.process_lane(view, policy_signature="pol1", cycle_id="c-tr-dirty")
    ok = out.tr_needs_update is True and len(out.tr_input_fields) > 0
    return {"scenario": "tr_needs_update_set_on_change", "hlr": ["20.37 step 2"], "result": "PASS" if ok else "FAIL"}


def scenario_forbidden_truth_hypotheses_read() -> dict:
    ob = ObjectBasin()
    view = _mk_lane_view("l3", truth_hypotheses=[{"id": "th1"}])
    out = ob.process_lane(view, policy_signature="pol1", cycle_id="c-forbidden")
    has_forbidden = any(a.get("type") == "FORBIDDEN_READ" for a in out.audit_records)
    ok = has_forbidden and len(out.evidence_fields) == 0
    return {"scenario": "forbidden_truth_hypotheses_read", "hlr": ["HLR-20.040-043"], "result": "PASS" if ok else "FAIL"}


def scenario_overflow_deterministic_degrade() -> dict:
    ob = ObjectBasin()
    view = _mk_lane_view("l4", propositions=[{"id": f"p{i}"} for i in range(40)], overflow=True)
    out = ob.process_lane(view, policy_signature="pol1", cycle_id="c-overflow", overflow_limit=32)
    has_overflow = out.overflow_metadata is not None and "OVERFLOW" in str(out.overflow_metadata)
    # evidence degraded but still some output
    ok = has_overflow and len(out.evidence_fields) >= 1
    return {"scenario": "overflow_deterministic_degrade", "hlr": ["HLR-20.040-025", "HLR-20.040-026"], "result": "PASS" if ok else "FAIL"}


def scenario_replay_identical_outputs() -> dict:
    ob = ObjectBasin()
    view = _mk_lane_view("l5", content="replay test", change=True)
    out1 = ob.process_lane(view, policy_signature="pol-rep", cycle_id="c-rep1")
    d1 = out1.as_dict()
    out2 = ob.process_lane(view, policy_signature="pol-rep", cycle_id="c-rep2")
    d2 = out2.as_dict()
    ok = json.dumps(d1, sort_keys=True) == json.dumps(d2, sort_keys=True)
    return {"scenario": "replay_identical_outputs", "hlr": ["HLR-20.040-009"], "result": "PASS" if ok else "FAIL"}


def main() -> int:
    scenarios = [
        scenario_lane_local_evidence_emit(),
        scenario_tr_needs_update_set_on_change(),
        scenario_forbidden_truth_hypotheses_read(),
        scenario_overflow_deterministic_degrade(),
        scenario_replay_identical_outputs(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {
        "module": "40.200_ob_prototypes",
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
    print(f"OB harness status: {status}")
    print(f"Scenarios: {report['summary']['passed']}/{report['summary']['total_scenarios']} PASS")
    print(f"Artifact: {path}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
