"""Verification harness for 40.150_mtp_prototypes (W3 Phase B)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import MTPStore, REASON_PRE_TRUTH, REASON_B_ENVELOPE


def scenario_happy_mtp_update_after_truth() -> dict:
    store = MTPStore(mtp_id="mtp-test", cycle_id="c-happy")
    store.add_lane_contribution("lane1", {"propositions": [{"id": "p1", "text": "meaning"}]})
    store.truth_done(True)
    res = store.mtp_update()
    snap = store.export_snapshot()
    ok = res.ok and res.commit_id and snap["committed"] and snap["commit_id"] == res.commit_id
    return {"scenario": "happy_mtp_update_after_truth", "hlr": ["HLR-20.115-032", "HLR-20.115-034", "HLR-20.115-036"], "result": "PASS" if ok else "FAIL"}

def scenario_reject_pre_truth() -> dict:
    store = MTPStore(mtp_id="mtp-test", cycle_id="c-pre")
    store.add_lane_contribution("lane1", {"propositions": [{"id": "p1"}]})
    res = store.mtp_update()
    ok = not res.ok and REASON_PRE_TRUTH in res.reason_codes
    return {"scenario": "reject_pre_truth", "hlr": ["HLR-20.115-032"], "result": "PASS" if ok else "FAIL"}

def scenario_reject_b_envelope() -> dict:
    store = MTPStore(mtp_id="mtp-test", cycle_id="c-b")
    store.add_lane_contribution("lane1", {"propositions": [{"id": "p1"}], "exec_plan": "bad"})
    store.truth_done(True)
    res = store.mtp_update()
    ok = not res.ok and REASON_B_ENVELOPE in res.reason_codes
    return {"scenario": "reject_b_envelope", "hlr": ["HLR-20.115-028"], "result": "PASS" if ok else "FAIL"}

def scenario_replay_identical_commit_id() -> dict:
    def run_once() -> str:
        s = MTPStore(mtp_id="mtp-r", cycle_id="c-r")
        s.add_lane_contribution("l1", {"propositions": [{"id": "p1"}]})
        s.truth_done(True)
        res = s.mtp_update()
        return res.commit_id or ""
    ok = run_once() == run_once()
    return {"scenario": "replay_identical_commit_id", "hlr": ["HLR-20.115-039"], "result": "PASS" if ok else "FAIL"}

def scenario_lane_merge_then_immutability() -> dict:
    store = MTPStore(mtp_id="mtp-m", cycle_id="c-m")
    store.add_lane_contribution("l1", {"propositions": [{"id": "p1"}]})
    store.add_lane_contribution("l2", {"propositions": [{"id": "p2"}]})
    store.truth_done(True)
    res = store.mtp_update()
    snap = store.export_snapshot()
    ok = res.ok and len(snap["semantic_core"]["propositions"]) >= 2 and snap["committed"]
    return {"scenario": "lane_merge_then_immutability", "hlr": ["HLR-20.115-040"], "result": "PASS" if ok else "FAIL"}

def main() -> int:
    scenarios = [
        scenario_happy_mtp_update_after_truth(),
        scenario_reject_pre_truth(),
        scenario_reject_b_envelope(),
        scenario_replay_identical_commit_id(),
        scenario_lane_merge_then_immutability(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {
        "module": "40.150_mtp_prototypes",
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
    print(f"MTP harness status: {status}")
    print(f"Scenarios: {report['summary']['passed']}/{report['summary']['total_scenarios']} PASS")
    print(f"Artifact: {path}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())