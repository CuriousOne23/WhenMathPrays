"""Verification harness for 40.101 IIInB prototypes."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import IIInB, UspRule, UspSnapshot, run_intake_path

ARTIFACT_NAME = "iiinb_verification_run_2026-06-08.json"


def _accepted_inb(content: str = "yeah baby meet tmrw") -> dict:
    return {
        "canonical_content": content,
        "provenance": {"outcome": "accepted", "source": "harness"},
        "metadata": {"intake_order": 0},
        "state_digest": "inb-digest-placeholder",
    }


def _snapshot_with_rules() -> UspSnapshot:
    return UspSnapshot(
        usp_version_id=1,
        rules=[
            UspRule(rule_id="rule-abc", pattern="tmrw", expansion="tomorrow", precedence=10),
            UspRule(rule_id="rule-baby", pattern="baby", expansion="darling", precedence=5),
        ],
    )


def scenario_profile_disabled_skip() -> dict:
    path = run_intake_path(_accepted_inb(), profile_enabled=False)
    repair = path["repair_result"]
    ok = (
        repair["skipped"]
        and not path["usp_loaded"]
        and repair.get("iiinb_repair_record") is None
        and path["intake_path"][1]["stage_name"] == "routing"
    )
    return {"scenario": "profile_disabled_skip", "hlr": ["HLR-20.101-001", "HLR-20.101-002"], "result": "PASS" if ok else "FAIL", "path": path}


def scenario_rule_apply() -> dict:
    snap = _snapshot_with_rules()
    iiinb = IIInB()
    out = iiinb.repair_pass(
        _accepted_inb("tmrw"),
        profile_enabled=True,
        usp_snapshot=snap,
    )
    tags = out["tp_intake_fields"]["input_repair_tags"]
    ok = (
        out["usp_loaded"]
        and out["iiinb_repair_record"]["applied_rule_count"] == 1
        and any(t["repair_outcome"] == "APPLIED" and t["rule_id"] == "rule-abc" for t in tags)
        and out["envelope_guard"]["semantic_core_unchanged"]
        and out["envelope_guard"]["tp_tr_unchanged"]
    )
    return {"scenario": "positive_usp_rule_apply", "hlr": ["HLR-20.101-011", "HLR-20.101-015"], "result": "PASS" if ok else "FAIL", "output": out}


def scenario_escalate_no_guess() -> dict:
    snap = UspSnapshot(usp_version_id=1, rules=[])
    out = IIInB().repair_pass(
        _accepted_inb("unknownshorthand"),
        profile_enabled=True,
        usp_snapshot=snap,
    )
    esc = out["tp_intake_fields"]["iiinb_escalation_refs"]
    tags = out["tp_intake_fields"]["input_repair_tags"]
    ok = (
        esc
        and all(t["repair_outcome"] == "ESCALATED" for t in tags)
        and out["iiinb_repair_record"]["applied_rule_count"] == 0
        and out["envelope_guard"]["semantic_core_unchanged"]
    )
    return {"scenario": "negative_escalate_no_guess", "hlr": ["HLR-20.101-012", "HLR-20.101-017"], "result": "PASS" if ok else "FAIL", "output": out}


def scenario_deterministic_replay() -> dict:
    snap = _snapshot_with_rules()
    raw = _accepted_inb("tmrw baby")
    a = IIInB().repair_pass(raw, profile_enabled=True, usp_snapshot=snap, cycle_id="c1")
    b = IIInB().repair_pass(raw, profile_enabled=True, usp_snapshot=snap, cycle_id="c1")
    ok = a["state_digest"] == b["state_digest"] and a == b
    return {"scenario": "positive_deterministic_replay", "hlr": ["HLR-20.101-021"], "result": "PASS" if ok else "FAIL"}


def scenario_inb_to_iiinb_to_rb_order() -> dict:
    path = run_intake_path(_accepted_inb("tmrw"), profile_enabled=True, usp_snapshot=_snapshot_with_rules())
    names = [s["stage_name"] for s in path["intake_path"]]
    ok = names == ["inb_surface_norm", "input_semantic_repair", "routing"]
    return {"scenario": "positive_inb_iiinb_rb_order", "hlr": ["HLR-20.101-003"], "result": "PASS" if ok else "FAIL", "stage_names": names}


def scenario_apply_cap() -> dict:
    rules = [UspRule(rule_id=f"r{i}", pattern=f"w{i}", expansion=f"word{i}") for i in range(20)]
    snap = UspSnapshot(usp_version_id=1, rules=rules)
    content = " ".join(f"w{i}" for i in range(20))
    out = IIInB().repair_pass(_accepted_inb(content), profile_enabled=True, usp_snapshot=snap)
    ok = (
        out["iiinb_repair_record"]["applied_rule_count"] <= 16
        and out["iiinb_repair_record"]["cap_status"] in ("OK", "APPLY_CAP", "SEGMENT_CAP")
    )
    return {"scenario": "negative_apply_cap", "hlr": ["HLR-20.101-019"], "result": "PASS" if ok else "FAIL", "output": out}


def _write_artifact(report: dict) -> Path:
    artifact_dir = Path(__file__).resolve().parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    path = artifact_dir / ARTIFACT_NAME
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return path


def main() -> int:
    scenarios = [
        scenario_profile_disabled_skip(),
        scenario_rule_apply(),
        scenario_escalate_no_guess(),
        scenario_deterministic_replay(),
        scenario_inb_to_iiinb_to_rb_order(),
        scenario_apply_cap(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    report = {
        "module": "40.101_iiinb_prototypes",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "status": status,
        "scenarios": scenarios,
        "summary": {
            "total": len(scenarios),
            "passed": sum(1 for s in scenarios if s["result"] == "PASS"),
        },
    }
    artifact = _write_artifact(report)
    print(f"IIInB harness status: {status}")
    print(f"Artifact: {artifact}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())