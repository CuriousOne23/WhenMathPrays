"""Verification harness for 40.80 USP prototypes (W2 Phase B)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import REASON_CAP_EXCEEDED, REASON_GB_VETOED, USPStore

ARTIFACT_NAME = "usp_verification_run_2026-06-08.json"


def scenario_empty_profile_snapshot() -> dict:
    store = USPStore()
    snap = store.export_snapshot()
    ok = snap["usp_version_id"] == 0 and snap["rules"] == [] and snap["usp_version_ref"]
    return {"scenario": "positive_empty_profile_snapshot", "hlr": ["HLR-20.102-024"], "result": "PASS" if ok else "FAIL"}


def scenario_single_rule_commit() -> dict:
    store = USPStore()
    res = store.apply_commit(pattern="tmrw", expansion="tomorrow", rule_id="r1")
    snap = store.export_snapshot()
    ok = res.ok and res.usp_version_id == 1 and len(snap["rules"]) == 1
    return {"scenario": "positive_single_rule_commit", "hlr": ["HLR-20.102-009", "HLR-20.102-018"], "result": "PASS" if ok else "FAIL"}


def scenario_supersede_chain() -> dict:
    store = USPStore()
    store.apply_commit(pattern="tmrw", expansion="tomorrow", rule_id="r1")
    store.apply_commit(pattern="tmrw", expansion="next day", rule_id="r1", transition="supersede")
    active = [r for r in store._rules if r.state == "ACTIVE"]
    superseded = [r for r in store._rules if r.state == "SUPERSEDED"]
    ok = len(active) == 1 and len(superseded) == 1 and active[0].expansion == "next day"
    return {"scenario": "positive_supersede_chain", "hlr": ["HLR-20.102-012", "HLR-20.102-013"], "result": "PASS" if ok else "FAIL"}


def scenario_revoke_rule() -> dict:
    store = USPStore()
    store.apply_commit(pattern="tmrw", expansion="tomorrow", rule_id="r1")
    store.apply_commit(pattern="tmrw", expansion="tomorrow", rule_id="r1", transition="revoke")
    snap = store.export_snapshot()
    ok = snap["rules"] == []
    return {"scenario": "positive_revoke_rule", "hlr": ["HLR-20.102-015"], "result": "PASS" if ok else "FAIL"}


def scenario_iiinb_readonly_load() -> dict:
    store = USPStore()
    store.apply_commit(pattern="tmrw", expansion="tomorrow", rule_id="r1")
    before = json.dumps(store.export_snapshot(), sort_keys=True)
    snap_copy = store.export_snapshot()
    snap_copy["rules"].append({"rule_id": "injected", "pattern": "x", "expansion": "y", "state": "ACTIVE"})
    after = json.dumps(store.export_snapshot(), sort_keys=True)
    ok = before == after
    return {"scenario": "positive_iiinb_readonly_load", "hlr": ["HLR-20.102-006", "HLR-20.102-007"], "result": "PASS" if ok else "FAIL"}


def scenario_cap_overflow() -> dict:
    store = USPStore(max_active_rules=1)
    store.apply_commit(pattern="a", expansion="A", rule_id="r1")
    res = store.apply_commit(pattern="b", expansion="B", rule_id="r2")
    ok = not res.ok and REASON_CAP_EXCEEDED in res.reason_codes
    return {"scenario": "negative_cap_overflow", "hlr": ["HLR-20.102-016"], "result": "PASS" if ok else "FAIL"}


def scenario_gb_veto_no_active() -> dict:
    store = USPStore()
    res = store.apply_commit(pattern="tmrw", expansion="tomorrow", rule_id="r1", gb_approved=False)
    snap = store.export_snapshot()
    ok = not res.ok and REASON_GB_VETOED in res.reason_codes and snap["rules"] == []
    return {"scenario": "negative_gb_veto_no_active", "hlr": ["HLR-20.102-014"], "result": "PASS" if ok else "FAIL"}


def scenario_replay_identical_ref() -> dict:
    def run_sequence() -> str:
        s = USPStore()
        s.apply_commit(pattern="tmrw", expansion="tomorrow", rule_id="r1")
        s.apply_commit(pattern="lol", expansion="laugh", rule_id="r2")
        return s.export_snapshot()["usp_version_ref"]

    ok = run_sequence() == run_sequence()
    return {"scenario": "positive_replay_identical_ref", "hlr": ["HLR-20.102-018"], "result": "PASS" if ok else "FAIL"}


def main() -> int:
    scenarios = [
        scenario_empty_profile_snapshot(),
        scenario_single_rule_commit(),
        scenario_supersede_chain(),
        scenario_revoke_rule(),
        scenario_iiinb_readonly_load(),
        scenario_cap_overflow(),
        scenario_gb_veto_no_active(),
        scenario_replay_identical_ref(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {
        "module": "40.80_usp_prototypes",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "phase": "B",
        "status": status,
        "scenarios": scenarios,
        "summary": {
            "total_scenarios": len(scenarios),
            "passed": sum(1 for s in scenarios if s["result"] == "PASS"),
            "failed_scenarios": [s["scenario"] for s in scenarios if s["result"] != "FAIL"],
        },
    }
    report["summary"]["failed_scenarios"] = [s["scenario"] for s in scenarios if s["result"] != "PASS"]
    artifact_dir = Path(__file__).resolve().parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    path = artifact_dir / ARTIFACT_NAME
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(f"USP harness status: {status}")
    print(f"Scenarios: {report['summary']['passed']}/{report['summary']['total_scenarios']} PASS")
    print(f"Artifact: {path}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())