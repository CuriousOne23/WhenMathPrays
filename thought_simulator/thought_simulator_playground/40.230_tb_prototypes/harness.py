"""Verification harness for 40.230_tb_prototypes (W3 Phase B)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import TruthBasin

ARTIFACT_NAME = "tb_verification_run_2026-06-09.json"


def _mk_ob_evidence(n: int = 2, with_tr: bool = False, overflow: bool = False) -> list[dict]:
    evs = []
    for i in range(n):
        ev = {
            "evidence_id": f"e-ob-{i}",
            "content": f"evidence {i} about math and reason",
            "propositions": [{"id": f"p-{i}"}],
        }
        if with_tr:
            ev["tr_input_fields"] = {"pattern": "tr"}
        evs.append(ev)
    if overflow:
        for i in range(20):
            evs.append({"evidence_id": f"e-overflow-{i}", "content": "overflow evidence"})
    return evs


def scenario_five_channel_happy_path() -> dict:
    tb = TruthBasin()
    evs = _mk_ob_evidence(3)
    out = tb.interpret(evs, policy_signature="pol1", cycle_id="c-happy")
    ok = (len(out.channel_interpretations) == 5 and
          len(out.truth_hypothesis_records) >= 1 and
          out.truth_hypothesis_records[0]["evidence_refs"])
    return {"scenario": "five_channel_happy_path", "hlr": ["HLR-20.060-005", "HLR-20.060-022"], "result": "PASS" if ok else "FAIL"}


def scenario_forbidden_tr_field_read() -> dict:
    tb = TruthBasin()
    evs = _mk_ob_evidence(1, with_tr=True)
    out = tb.interpret(evs, policy_signature="pol1", cycle_id="c-forbidden")
    has_forbidden = any(a.get("type") == "FORBIDDEN_READ" for a in out.audit_records)
    ok = has_forbidden and len(out.truth_hypothesis_records) == 0
    return {"scenario": "forbidden_tr_field_read", "hlr": ["HLR-20.060-043"], "result": "PASS" if ok else "FAIL"}


def scenario_overflow_no_silent_drop() -> dict:
    tb = TruthBasin()
    evs = _mk_ob_evidence(overflow=True)
    out = tb.interpret(evs, policy_signature="pol1", cycle_id="c-overflow", overflow_limit=5)
    has_overflow = any(a.get("type") == "OVERFLOW" for a in out.audit_records)
    ok = has_overflow and len(out.truth_hypothesis_records) > 0  # still emits some
    return {"scenario": "overflow_no_silent_drop", "hlr": ["HLR-20.060-025", "HLR-20.060-026"], "result": "PASS" if ok else "FAIL"}


def scenario_channel_map_canonical_order() -> dict:
    tb = TruthBasin()
    evs = _mk_ob_evidence(2)
    out = tb.interpret(evs, policy_signature="pol1", cycle_id="c-order")
    hyps = out.truth_hypothesis_records
    ids = [h["hypothesis_id"] for h in hyps]
    ok = ids == sorted(ids)
    return {"scenario": "channel_map_canonical_order", "hlr": ["HLR-20.060-044"], "result": "PASS" if ok else "FAIL"}


def scenario_replay_seed_independent() -> dict:
    tb = TruthBasin()
    evs = _mk_ob_evidence(2)
    out1 = tb.interpret(evs, policy_signature="pol-rep", cycle_id="c-rep1")
    d1 = out1.as_dict()
    out2 = tb.interpret(evs, policy_signature="pol-rep", cycle_id="c-rep2")
    d2 = out2.as_dict()
    ok = json.dumps(d1, sort_keys=True) == json.dumps(d2, sort_keys=True)
    return {"scenario": "replay_seed_independent", "hlr": ["HLR-20.060-009", "HLR-20.060-036"], "result": "PASS" if ok else "FAIL"}


def main() -> int:
    scenarios = [
        scenario_five_channel_happy_path(),
        scenario_forbidden_tr_field_read(),
        scenario_overflow_no_silent_drop(),
        scenario_channel_map_canonical_order(),
        scenario_replay_seed_independent(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {
        "module": "40.230_tb_prototypes",
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
    print(f"TB harness status: {status}")
    print(f"Scenarios: {report['summary']['passed']}/{report['summary']['total_scenarios']} PASS")
    print(f"Artifact: {path}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
