"""W2 clarification_event wire harness for 40.33 CIL prototypes."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from prototype import CILDeterministicReject, CILState

_ROOT = Path(__file__).resolve().parent.parent
for name, rel in (("upi_prototype", "40.103_upi_prototypes/prototype.py"),):
    spec = importlib.util.spec_from_file_location(name, _ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)

UPI = sys.modules["upi_prototype"].UPI
USPStore = sys.modules["upi_prototype"].USPStore

ARTIFACT = Path(__file__).resolve().parent / "artifacts" / "cil_w2_verification_run_2026-06-08.json"


def scenario_escalation_to_event() -> dict:
    cil = CILState(active_profile="P1", sequence=0)
    event = cil.emit_clarification_event(sequence=1, escalation_ref="esc-1", pattern="tmrw", expansion="tomorrow")
    ok = event["schema_version"] == "clarification_event_v1" and event["integration_seq"] == 1
    return {"scenario": "positive_escalation_to_clarification_event", "result": "PASS" if ok else "FAIL"}


def scenario_fifo_ordering() -> dict:
    cil = CILState(active_profile="P1", sequence=0)
    e2 = cil.emit_clarification_event(sequence=1, escalation_ref="esc-2", pattern="b", expansion="B")
    e3 = cil.emit_clarification_event(sequence=2, escalation_ref="esc-3", pattern="c", expansion="C")
    upi = UPI(USPStore())
    recs = upi.process_fifo([e3, e2])
    ok = upi._processed_seq == [1, 2] and recs[0].commit_status == "COMMITTED"
    return {"scenario": "positive_fifo_clarification_ordering", "result": "PASS" if ok else "FAIL"}


def scenario_integration_seq_monotonic() -> dict:
    cil = CILState(active_profile="P1", sequence=0)
    seqs = []
    for i in range(3):
        ev = cil.emit_clarification_event(sequence=i + 1, escalation_ref=f"esc-{i}", pattern=f"p{i}", expansion=f"e{i}")
        seqs.append(ev["integration_seq"])
    ok = seqs == [1, 2, 3]
    return {"scenario": "positive_integration_seq_monotonic", "result": "PASS" if ok else "FAIL"}


def scenario_incomplete_payload() -> dict:
    cil = CILState(active_profile="P1", sequence=0)
    try:
        cil.emit_clarification_event(sequence=1, escalation_ref="esc-x", pattern="", expansion="x")
        ok = False
    except CILDeterministicReject:
        ok = True
    return {"scenario": "negative_incomplete_clarification_payload", "result": "PASS" if ok else "FAIL"}


def main() -> int:
    scenarios = [
        scenario_escalation_to_event(),
        scenario_fifo_ordering(),
        scenario_integration_seq_monotonic(),
        scenario_incomplete_payload(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {"module": "40.33_cil_prototypes_w2", "phase": "B", "status": status, "scenarios": scenarios}
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"CIL W2 harness: {status}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())