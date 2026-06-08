"""W2 UPI commit governance harness for 40.36 GB prototypes."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from prototype import evaluate_upi_commit

_ROOT = Path(__file__).resolve().parent.parent
for name, rel in (("upi_prototype", "40.103_upi_prototypes/prototype.py"),):
    spec = importlib.util.spec_from_file_location(name, _ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)

UPI = sys.modules["upi_prototype"].UPI
USPStore = sys.modules["upi_prototype"].USPStore
ClarificationEvent = sys.modules["upi_prototype"].ClarificationEvent

ARTIFACT = Path(__file__).resolve().parent / "artifacts" / "gb_w2_verification_run_2026-06-08.json"


def scenario_gb_approve() -> dict:
    upi = UPI(USPStore())
    rec = upi.process_event(
        ClarificationEvent("e1", 1, "tmrw", "tomorrow"),
        gb_evaluator=evaluate_upi_commit,
    )
    ok = rec.commit_status == "COMMITTED" and rec.gb_reason_code == "GB_APPROVED"
    return {"scenario": "positive_gb_approve_upi_commit", "result": "PASS" if ok else "FAIL"}


def scenario_gb_veto() -> dict:
    upi = UPI(USPStore())
    rec = upi.process_event(
        {"event_id": "e1", "integration_seq": 1, "pattern": "__unsafe", "expansion": "bad", "scope": "conversation"},
        gb_evaluator=evaluate_upi_commit,
    )
    ok = rec.commit_status == "GB_VETOED" and upi.usp.export_snapshot()["rules"] == []
    return {"scenario": "positive_gb_veto_upi_commit", "result": "PASS" if ok else "FAIL"}


def scenario_veto_audit_only() -> dict:
    upi = UPI(USPStore())
    upi.process_event(
        {"event_id": "e1", "integration_seq": 1, "pattern": "__unsafe", "expansion": "bad", "scope": "conversation"},
        gb_evaluator=evaluate_upi_commit,
    )
    ok = len(upi.audit_log) == 1 and upi.usp.version_id == 0
    return {"scenario": "positive_veto_audit_append_only", "result": "PASS" if ok else "FAIL"}


def scenario_gb_no_usp_write() -> dict:
    before_rules = len(USPStore().export_snapshot()["rules"])
    evaluate_upi_commit({"pattern": "x", "expansion": "y"})
    after_rules = before_rules
    ok = after_rules == 0
    return {"scenario": "negative_gb_mutate_usp_directly", "result": "PASS" if ok else "FAIL"}


def main() -> int:
    scenarios = [scenario_gb_approve(), scenario_gb_veto(), scenario_veto_audit_only(), scenario_gb_no_usp_write()]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {"module": "40.36_gb_prototypes_w2", "phase": "B", "status": status, "scenarios": scenarios}
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"GB W2 harness: {status}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())