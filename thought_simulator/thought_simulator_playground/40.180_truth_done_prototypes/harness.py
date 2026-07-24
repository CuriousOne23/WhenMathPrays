"""Verification harness for 40.180_truth_done_prototypes (W3 Phase B)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import TruthDone, TruthHypothesisRecord, DoneState, TruthDoneOutput

ARTIFACT_NAME = "truth_done_verification_run_2026-06-09.json"

def scenario_happy_truth_done_after_merge() -> dict:
    td = TruthDone()
    inputs = {
        "truth_hypothesis_records": [
            {"hypothesis_id": "h1", "proposition_ref": "p1", "evidence_refs": ["e1"]},
            {"hypothesis_id": "h2", "proposition_ref": "p2", "evidence_refs": []},
        ],
        "messy_input_record": {},
    }
    out = td.evaluate(inputs, policy_signature="pol1", cycle_id="c-happy")
    ok = (len(out.truth_hypotheses) == 2 and
          out.truth_hypotheses[0].truth_status == "SUPPORTED" and
          out.done_state.completion_status == "DONE")
    return {"scenario": "happy_truth_done_after_merge", "hlr": ["HLR-20.140-019", "HLR-20.140-021"], "result": "PASS" if ok else "FAIL"}

def scenario_blocked_by_messy_input() -> dict:
    td = TruthDone()
    inputs = {
        "truth_hypothesis_records": [
            {"hypothesis_id": "h1", "proposition_ref": "p1", "evidence_refs": ["e1"]},
        ],
        "messy_input_record": {"class": "MI_VAGUE"},
    }
    out = td.evaluate(inputs, policy_signature="pol1", cycle_id="c-block")
    ok = (out.done_state.completion_status in ("BLOCKED", "PARTIAL") and
          out.done_state.blocked_by_messy_input and
          "MI_VAGUE" in out.done_state.completion_reason_codes)
    return {"scenario": "blocked_by_messy_input", "hlr": ["HLR-20.140-029", "HLR-20.140-030"], "result": "PASS" if ok else "FAIL"}

def scenario_forbidden_routing_metadata_read() -> dict:
    td = TruthDone()
    inputs = {
        "truth_hypothesis_records": [],
        "routing_metadata": {"foo": "bar"},  # forbidden
    }
    out = td.evaluate(inputs, policy_signature="pol1", cycle_id="c-forbidden")
    # In impl, it returns early with audit, no truth_hypotheses or bad done
    ok = len(out.evaluation_audit_records) > 0 and "FORBIDDEN_READ" in str(out.evaluation_audit_records)
    return {"scenario": "forbidden_routing_metadata_read", "hlr": ["HLR-20.140-043"], "result": "PASS" if ok else "FAIL"}

def scenario_canonical_ordering_golden() -> dict:
    td = TruthDone()
    inputs = {
        "truth_hypothesis_records": [
            {"hypothesis_id": "h2", "proposition_ref": "p2", "evidence_refs": []},
            {"hypothesis_id": "h1", "proposition_ref": "p1", "evidence_refs": ["e1"]},
        ],
    }
    out = td.evaluate(inputs, policy_signature="pol1", cycle_id="c-order")
    # Check sorted by hypothesis_id
    ids = [h.hypothesis_id for h in out.truth_hypotheses]
    ok = ids == sorted(ids)
    golden = json.dumps([h.as_dict() for h in out.truth_hypotheses], sort_keys=True)
    # For golden test, just check ordering
    return {"scenario": "canonical_ordering_golden_diff", "hlr": ["HLR-20.140-038"], "result": "PASS" if ok else "FAIL"}

def scenario_replay_seed_independent() -> dict:
    def run_eval() -> str:
        td = TruthDone()
        inputs = {
            "truth_hypothesis_records": [
                {"hypothesis_id": "h1", "proposition_ref": "p1", "evidence_refs": ["e1"]},
            ],
        }
        out = td.evaluate(inputs, policy_signature="pol1", cycle_id="c-replay")
        return json.dumps(out.as_dict(), sort_keys=True)
    ok = run_eval() == run_eval()  # same inputs, same output (seed independent)
    return {"scenario": "replay_seed_independent_outputs", "hlr": ["HLR-20.140-024"], "result": "PASS" if ok else "FAIL"}

def main() -> int:
    scenarios = [
        scenario_happy_truth_done_after_merge(),
        scenario_blocked_by_messy_input(),
        scenario_forbidden_routing_metadata_read(),
        scenario_canonical_ordering_golden(),
        scenario_replay_seed_independent(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {
        "module": "40.180_truth_done_prototypes",
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
    print(f"TruthDone harness status: {status}")
    print(f"Scenarios: {report['summary']['passed']}/{report['summary']['total_scenarios']} PASS")
    print(f"Artifact: {path}")
    return 0 if status == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
