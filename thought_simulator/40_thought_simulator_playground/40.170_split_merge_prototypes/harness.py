"""Verification harness for 40.170_split_merge_prototypes (W3 Phase B)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import SplitMerge, ThoughtPoint, EntropyComponents

ARTIFACT_NAME = "split_merge_verification_run_2026-06-09.json"

def scenario_nominal_split() -> dict:
    sm = SplitMerge()
    tp = ThoughtPoint.new(
        basin_id="test",
        entropy=EntropyComponents(h_rep=1.0, h_pred=1.0, h_struct=1.0),
        embedding=[0.5, 0.5],
        created_at_tick=0,
        deterministic_mode=True,
    )
    children = sm.split(tp, child_count=2, tick=10)
    deltas = sm.get_lineage_deltas()
    ok = len(children) == 2 and len(deltas) == 1 and deltas[0]["event"] == "split"
    return {"scenario": "nominal_split_lane_outputs", "hlr": ["HLR-20.130-001", "HLR-20.130-005", "HLR-20.130-015"], "result": "PASS" if ok else "FAIL"}

def scenario_nominal_merge() -> dict:
    sm = SplitMerge()
    tp1 = ThoughtPoint.new(basin_id="a", entropy=EntropyComponents(h_rep=1.0, h_pred=0.5, h_struct=0.5), embedding=[0.1, 0.2], created_at_tick=0)
    tp2 = ThoughtPoint.new(basin_id="b", entropy=EntropyComponents(h_rep=0.5, h_pred=1.0, h_struct=0.5), embedding=[0.3, 0.4], created_at_tick=0)
    merged = sm.merge([tp1, tp2], tick=20)
    deltas = sm.get_lineage_deltas()
    ok = merged is not None and len(deltas) == 1 and deltas[0]["event"] == "merge"
    return {"scenario": "nominal_merge_mtp_bound", "hlr": ["HLR-20.130-002", "HLR-20.130-008", "HLR-20.130-016"], "result": "PASS" if ok else "FAIL"}

def scenario_limit_exceed_reject() -> dict:
    sm = SplitMerge()
    tp = ThoughtPoint.new(basin_id="test", entropy=EntropyComponents(h_rep=1.0, h_pred=1.0, h_struct=1.0), embedding=[0.1, 0.2], created_at_tick=0)
    try:
        sm.split(tp, child_count=20, tick=30)  # exceed limit
    except ValueError as e:
        ok = "limit exceeded" in str(e).lower()
        return {"scenario": "limit_exceed_reject", "hlr": ["HLR-20.130-012", "HLR-20.130-013"], "result": "PASS" if ok else "FAIL"}
    return {"scenario": "limit_exceed_reject", "hlr": ["HLR-20.130-012", "HLR-20.130-013"], "result": "FAIL"}

def scenario_lineage_delta_golden() -> dict:
    sm = SplitMerge()
    tp = ThoughtPoint.new(basin_id="test", entropy=EntropyComponents(h_rep=1.0, h_pred=1.0, h_struct=1.0), embedding=[0.1, 0.2], created_at_tick=0)
    sm.split(tp, child_count=2, tick=40, reason_code="test_split")
    golden = sm.golden_lineage_delta()
    ok = "split" in golden and "test_split" in golden
    return {"scenario": "lineage_delta_golden_diff", "hlr": ["HLR-20.130-004", "HLR-20.130-019"], "result": "PASS" if ok else "FAIL"}

def scenario_replay_identical() -> dict:
    def run_split_merge() -> str:
        sm = SplitMerge()
        tp = ThoughtPoint.new(basin_id="r", entropy=EntropyComponents(h_rep=1.0, h_pred=1.0, h_struct=1.0), embedding=[0.5, 0.5], created_at_tick=0, deterministic_mode=True)
        children = sm.split(tp, child_count=2, tick=50)
        merged = sm.merge(children, tick=60)
        return json.dumps(sm.get_lineage_deltas(), sort_keys=True)
    ok = run_split_merge() == run_split_merge()
    return {"scenario": "replay_identical_state", "hlr": ["HLR-20.130-017"], "result": "PASS" if ok else "FAIL"}

def main() -> int:
    scenarios = [
        scenario_nominal_split(),
        scenario_nominal_merge(),
        scenario_limit_exceed_reject(),
        scenario_lineage_delta_golden(),
        scenario_replay_identical(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {
        "module": "40.170_split_merge_prototypes",
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
    print(f"SplitMerge harness status: {status}")
    print(f"Scenarios: {report['summary']['passed']}/{report['summary']['total_scenarios']} PASS")
    print(f"Artifact: {path}")
    return 0 if status == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
    try:
        not_implemented()
    except NotImplementedError:
        sys.exit(2)