"""Verification harness for 40.90 UPI prototypes (W2 Phase B)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import REASON_INCOMPLETE, REASON_PENDING_CAP, ClarificationEvent, USPStore, UPI

ARTIFACT_NAME = "upi_verification_run_2026-06-08.json"


def _event(eid: str, seq: int, pattern: str, expansion: str) -> ClarificationEvent:
    return ClarificationEvent(eid, seq, pattern, expansion)


def scenario_single_commit() -> dict:
    upi = UPI(USPStore())
    rec = upi.process_event(_event("e1", 1, "tmrw", "tomorrow"))
    ok = rec.commit_status == "COMMITTED" and rec.usp_version_id == 1
    return {"scenario": "positive_single_commit", "hlr": ["HLR-20.103-005", "HLR-20.103-006"], "result": "PASS" if ok else "FAIL"}


def scenario_fifo_two_events() -> dict:
    upi = UPI(USPStore())
    recs = upi.process_fifo([_event("e2", 2, "b", "B"), _event("e1", 1, "a", "A")])
    ok = recs[0].commit_status == "COMMITTED" and recs[1].commit_status == "COMMITTED"
    ok = ok and upi._processed_seq == [1, 2]
    return {"scenario": "positive_fifo_two_events", "hlr": ["HLR-20.103-005", "HLR-20.103-012"], "result": "PASS" if ok else "FAIL"}


def scenario_gb_approve() -> dict:
    upi = UPI(USPStore())
    rec = upi.process_event(_event("e1", 1, "tmrw", "tomorrow"), gb_decision="approve")
    ok = rec.commit_status == "COMMITTED" and rec.gb_reason_code == "GB_TEST_OK"
    return {"scenario": "positive_gb_approve", "hlr": ["HLR-20.103-009", "HLR-20.103-011"], "result": "PASS" if ok else "FAIL"}


def scenario_gb_veto() -> dict:
    upi = UPI(USPStore())
    rec = upi.process_event(_event("e1", 1, "tmrw", "tomorrow"), gb_decision="veto")
    snap = upi.usp.export_snapshot()
    ok = rec.commit_status == "GB_VETOED" and snap["rules"] == []
    return {"scenario": "positive_gb_veto", "hlr": ["HLR-20.103-010"], "result": "PASS" if ok else "FAIL"}


def scenario_incomplete_event() -> dict:
    upi = UPI(USPStore())
    rec = upi.process_event({"event_id": "e1", "integration_seq": 1, "pattern": "", "expansion": "x"})
    ok = rec.commit_status == "REJECTED" and REASON_INCOMPLETE in rec.reason_codes
    return {"scenario": "negative_incomplete_event", "hlr": ["HLR-20.103-008"], "result": "PASS" if ok else "FAIL"}


def scenario_usp_cap_overflow() -> dict:
    upi = UPI(USPStore(max_active_rules=1))
    upi.process_event(_event("e1", 1, "a", "A"))
    rec = upi.process_event(_event("e2", 2, "b", "B"))
    ok = rec.commit_status == "REJECTED"
    return {"scenario": "negative_usp_cap_overflow", "hlr": ["HLR-20.103-015"], "result": "PASS" if ok else "FAIL"}


def scenario_pending_commit_cap() -> dict:
    upi = UPI(USPStore(), pending_cap=0)
    rec = upi.process_event(_event("e1", 1, "a", "A"))
    ok = rec.commit_status == "REJECTED" and REASON_PENDING_CAP in rec.reason_codes
    return {"scenario": "negative_pending_commit_cap", "hlr": ["HLR-20.103-016"], "result": "PASS" if ok else "FAIL"}


def scenario_replay_identical_ref() -> dict:
    def run() -> str | None:
        upi = UPI(USPStore())
        upi.process_fifo([_event("e1", 1, "a", "A"), _event("e2", 2, "b", "B")])
        return upi.usp.export_snapshot()["usp_version_ref"]

    ok = run() == run()
    return {"scenario": "positive_replay_identical_ref", "hlr": ["HLR-20.103-012"], "result": "PASS" if ok else "FAIL"}


def main() -> int:
    scenarios = [
        scenario_single_commit(),
        scenario_fifo_two_events(),
        scenario_gb_approve(),
        scenario_gb_veto(),
        scenario_incomplete_event(),
        scenario_usp_cap_overflow(),
        scenario_pending_commit_cap(),
        scenario_replay_identical_ref(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {
        "module": "40.90_upi_prototypes",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "phase": "B",
        "status": status,
        "scenarios": scenarios,
        "summary": {
            "total_scenarios": len(scenarios),
            "passed": sum(1 for s in scenarios if s["result"] == "PASS"),
            "failed_scenarios": [s["scenario"] for s in scenarios if s["result"] != "PASS"],
        },
    }
    artifact_dir = Path(__file__).resolve().parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    path = artifact_dir / ARTIFACT_NAME
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(f"UPI harness status: {status}")
    print(f"Scenarios: {report['summary']['passed']}/{report['summary']['total_scenarios']} PASS")
    print(f"Artifact: {path}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())