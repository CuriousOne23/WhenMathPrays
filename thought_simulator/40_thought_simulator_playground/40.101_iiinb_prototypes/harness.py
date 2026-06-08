"""Verification harness for 40.101 IIInB prototypes (Phase B complete).

Scenarios exercise full test matrix: profile gate, USP apply, escalation,
intake ordering, caps, replay, envelope guards, diagnostics, TCU reporting.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import (
    BASIN_CHAIN_STAGES,
    INTAKE_PATH_STAGES,
    IIInB,
    REASON_CODES,
    UspRule,
    UspSnapshot,
    run_intake_path,
)

ARTIFACT_NAME = "iiinb_verification_run_2026-06-08.json"


def _accepted_inb(content: str = "yeah baby meet tmrw") -> dict:
    return {
        "canonical_content": content,
        "provenance": {"outcome": "accepted", "source": "harness"},
        "metadata": {"intake_order": 0},
        "state_digest": "inb-digest-placeholder",
    }


def _rejected_inb(content: str = "rejected payload") -> dict:
    return {
        "canonical_content": content,
        "provenance": {"outcome": "rejected", "source": "harness", "reason_code": "MALFORMED_INPUT"},
        "metadata": {"intake_order": 0},
    }


def _snapshot_with_rules() -> UspSnapshot:
    return UspSnapshot(
        usp_version_id=1,
        rules=[
            UspRule(rule_id="rule-abc", pattern="tmrw", expansion="tomorrow", precedence=10),
            UspRule(rule_id="rule-baby", pattern="baby", expansion="darling", precedence=5),
        ],
    )


def _all_envelope_unchanged(guard: dict) -> bool:
    return all(
        guard.get(k, True)
        for k in (
            "semantic_core_unchanged",
            "tp_tr_unchanged",
            "exec_plan_unchanged",
            "exec_trace_unchanged",
        )
    )


def scenario_profile_disabled_skip() -> dict:
    path = run_intake_path(_accepted_inb(), profile_enabled=False)
    repair = path["repair_result"]
    ok = (
        repair["skipped"]
        and not path["usp_loaded"]
        and repair.get("iiinb_repair_record") is None
        and path["intake_path"][1]["stage_name"] == "routing"
        and repair["reason_codes"] == ["PROFILE_DISABLED"]
    )
    return {"scenario": "profile_disabled_skip", "hlr": ["HLR-20.101-001", "HLR-20.101-002"], "result": "PASS" if ok else "FAIL"}


def scenario_rule_apply() -> dict:
    snap = _snapshot_with_rules()
    out = IIInB().repair_pass(_accepted_inb("tmrw"), profile_enabled=True, usp_snapshot=snap)
    tags = out["tp_intake_fields"]["input_repair_tags"]
    ok = (
        out["usp_loaded"]
        and out["iiinb_repair_record"]["applied_rule_count"] == 1
        and any(t["repair_outcome"] == "APPLIED" and t["rule_id"] == "rule-abc" for t in tags)
        and _all_envelope_unchanged(out["envelope_guard"])
    )
    return {"scenario": "positive_usp_rule_apply", "hlr": ["HLR-20.101-005", "HLR-20.101-008", "HLR-20.101-011", "HLR-20.101-014", "HLR-20.101-015"], "result": "PASS" if ok else "FAIL"}


def scenario_escalate_no_guess() -> dict:
    snap = UspSnapshot(usp_version_id=1, rules=[])
    out = IIInB().repair_pass(_accepted_inb("unknownshorthand"), profile_enabled=True, usp_snapshot=snap)
    esc = out["tp_intake_fields"]["iiinb_escalation_refs"]
    tags = out["tp_intake_fields"]["input_repair_tags"]
    ok = (
        esc
        and all(t["repair_outcome"] == "ESCALATED" for t in tags)
        and out["iiinb_repair_record"]["applied_rule_count"] == 0
        and out["envelope_guard"]["semantic_core_unchanged"]
    )
    return {"scenario": "negative_escalate_no_guess", "hlr": ["HLR-20.101-009", "HLR-20.101-012"], "result": "PASS" if ok else "FAIL"}


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
    return {"scenario": "negative_apply_cap", "hlr": ["HLR-20.101-019"], "result": "PASS" if ok else "FAIL"}


def scenario_not_in_rb_ob_chain() -> dict:
    path = run_intake_path(_accepted_inb("tmrw"), profile_enabled=True, usp_snapshot=_snapshot_with_rules())
    names = {s["stage_name"] for s in path["intake_path"]}
    ok = names <= INTAKE_PATH_STAGES and not (names & BASIN_CHAIN_STAGES)
    return {"scenario": "positive_not_in_rb_ob_chain", "hlr": ["HLR-20.101-004"], "result": "PASS" if ok else "FAIL", "stage_names": sorted(names)}


def scenario_multi_rule_precedence() -> dict:
    snap = UspSnapshot(
        usp_version_id=1,
        rules=[
            UspRule(rule_id="rule-low", pattern="x", expansion="low", precedence=1),
            UspRule(rule_id="rule-high", pattern="x", expansion="high", precedence=10),
            UspRule(rule_id="rule-inactive", pattern="x", expansion="inactive", precedence=99, state="INACTIVE"),
        ],
    )
    out = IIInB().repair_pass(_accepted_inb("x"), profile_enabled=True, usp_snapshot=snap)
    tags = out["tp_intake_fields"]["input_repair_tags"]
    ok = (
        len(tags) == 1
        and tags[0]["rule_id"] == "rule-high"
        and tags[0]["repair_outcome"] == "APPLIED"
    )
    return {"scenario": "positive_multi_rule_precedence", "hlr": ["HLR-20.101-007"], "result": "PASS" if ok else "FAIL"}


def scenario_rejected_inb_handoff() -> dict:
    out = IIInB().repair_pass(_rejected_inb(), profile_enabled=True, usp_snapshot=_snapshot_with_rules())
    ok = (
        out["skipped"]
        and not out["usp_loaded"]
        and out.get("error") == "inb_not_accepted"
        and out["reason_codes"] == ["INB_HANDOFF_REJECTED"]
        and out.get("iiinb_repair_record") is None
    )
    return {"scenario": "negative_rejected_inb_handoff", "hlr": ["HLR-20.101-003"], "result": "PASS" if ok else "FAIL"}


def scenario_usp_load_failure() -> dict:
    out = IIInB().repair_pass(_accepted_inb("tmrw"), profile_enabled=True, usp_snapshot=None)
    ok = (
        not out["usp_loaded"]
        and out.get("error") == "usp_load_failed"
        and out["reason_codes"] == ["USP_LOAD_FAILED"]
        and "USP_LOAD_FAILED" in REASON_CODES
    )
    return {"scenario": "negative_usp_load_failure", "hlr": ["HLR-20.101-005", "HLR-20.101-022"], "result": "PASS" if ok else "FAIL"}


def scenario_cil_escalation_nonblocking() -> dict:
    path = run_intake_path(_accepted_inb("unknownshorthand"), profile_enabled=True, usp_snapshot=UspSnapshot(usp_version_id=1, rules=[]))
    repair = path["repair_result"]
    esc = repair["tp_intake_fields"]["iiinb_escalation_refs"]
    ok = (
        esc
        and repair["handoff_next_stage"] == "routing"
        and path["intake_path"][-1]["stage_name"] == "routing"
        and not repair.get("blocked")
    )
    return {"scenario": "positive_cil_escalation_nonblocking", "hlr": ["HLR-20.101-017", "HLR-20.101-018"], "result": "PASS" if ok else "FAIL"}


def scenario_tcu_cost_reported() -> dict:
    snap = _snapshot_with_rules()
    out = IIInB().repair_pass(_accepted_inb("tmrw baby"), profile_enabled=True, usp_snapshot=snap)
    record = out["iiinb_repair_record"]
    expected = record["segment_count"] + record["applied_rule_count"]
    ok = record["tcu_cost"] == expected and record["tcu_cost"] > 0
    return {"scenario": "positive_tcu_cost_reported", "hlr": ["HLR-20.101-020"], "result": "PASS" if ok else "FAIL", "tcu_cost": record["tcu_cost"]}


def scenario_segment_cap() -> dict:
    words = [f"w{i:02d}" for i in range(40)]
    snap = UspSnapshot(usp_version_id=1, rules=[UspRule(rule_id="r0", pattern="w00", expansion="word0")])
    out = IIInB().repair_pass(_accepted_inb(" ".join(words)), profile_enabled=True, usp_snapshot=snap)
    record = out["iiinb_repair_record"]
    ok = (
        record["segment_count"] == 32
        and record["cap_status"] == "SEGMENT_CAP"
        and "SEGMENT_CAP" in out["reason_codes"]
    )
    return {"scenario": "negative_segment_cap", "hlr": ["HLR-20.101-010", "HLR-20.101-019"], "result": "PASS" if ok else "FAIL"}


def scenario_usp_version_ref_pinned() -> dict:
    snap = _snapshot_with_rules()
    out = IIInB().repair_pass(_accepted_inb("tmrw"), profile_enabled=True, usp_snapshot=snap)
    ok = (
        out["usp_version_ref"] == snap.version_ref
        and out["iiinb_repair_record"]["usp_version_ref"] == snap.version_ref
    )
    return {"scenario": "positive_usp_version_ref_pinned", "hlr": ["HLR-20.101-006"], "result": "PASS" if ok else "FAIL"}


def scenario_pipeline_b_envelope_unchanged() -> dict:
    tp_state = {
        "semantic_core": {"meaning": "frozen"},
        "tp_tr": {"truth": "pinned"},
        "exec_plan": {"lane": "B", "steps": [1, 2]},
        "exec_trace": {"events": ["e1"]},
    }
    out = IIInB().repair_pass(
        _accepted_inb("tmrw"),
        profile_enabled=True,
        usp_snapshot=_snapshot_with_rules(),
        tp_state=tp_state,
    )
    ok = _all_envelope_unchanged(out["envelope_guard"])
    return {"scenario": "positive_pipeline_b_envelope_unchanged", "hlr": ["HLR-20.101-024"], "result": "PASS" if ok else "FAIL"}


def scenario_audit_record_per_pass() -> dict:
    out = IIInB().repair_pass(_accepted_inb("tmrw"), profile_enabled=True, usp_snapshot=_snapshot_with_rules())
    ok = (
        out.get("audit_records")
        and len(out["audit_records"]) == 1
        and out["audit_records"][0] == out["iiinb_repair_record"]
    )
    return {"scenario": "positive_audit_record_per_pass", "hlr": ["HLR-20.101-016"], "result": "PASS" if ok else "FAIL"}


def scenario_diagnostic_export_ordering() -> dict:
    iiinb = IIInB()
    records = [
        {"cycle_id": "c2", "iiinb_event_id": "iiinb-evt-c2-0002", "applied_rule_count": 1},
        {"cycle_id": "c1", "iiinb_event_id": "iiinb-evt-c1-0001", "applied_rule_count": 2},
    ]
    export_a = iiinb.export_repair_diagnostics(records)
    export_b = iiinb.export_repair_diagnostics(list(reversed(records)))
    parsed = json.loads(export_a)
    ok = (
        export_a == export_b
        and [r["cycle_id"] for r in parsed] == ["c1", "c2"]
        and export_a == json.dumps(parsed, sort_keys=True, separators=(",", ":"))
    )
    return {"scenario": "positive_diagnostic_export_ordering", "hlr": ["HLR-20.101-027", "HLR-20.101-028"], "result": "PASS" if ok else "FAIL", "export": export_a}


def scenario_usp_snapshot_immutable() -> dict:
    snap = _snapshot_with_rules()
    before = json.dumps(snap.to_dict(), sort_keys=True)
    IIInB().repair_pass(_accepted_inb("tmrw baby"), profile_enabled=True, usp_snapshot=snap)
    after = json.dumps(snap.to_dict(), sort_keys=True)
    ok = before == after
    return {"scenario": "positive_usp_snapshot_immutable", "hlr": ["HLR-20.101-008"], "result": "PASS" if ok else "FAIL"}


def scenario_segmentation_deterministic() -> dict:
    raw = _accepted_inb("alpha beta gamma")
    snap = UspSnapshot(usp_version_id=1, rules=[])
    a = IIInB().repair_pass(raw, profile_enabled=True, usp_snapshot=snap)
    b = IIInB().repair_pass(raw, profile_enabled=True, usp_snapshot=snap)
    ok = a["tp_intake_fields"]["input_segments"] == b["tp_intake_fields"]["input_segments"]
    return {"scenario": "positive_segmentation_deterministic", "hlr": ["HLR-20.101-010"], "result": "PASS" if ok else "FAIL"}


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
        scenario_not_in_rb_ob_chain(),
        scenario_multi_rule_precedence(),
        scenario_rejected_inb_handoff(),
        scenario_usp_load_failure(),
        scenario_cil_escalation_nonblocking(),
        scenario_tcu_cost_reported(),
        scenario_segment_cap(),
        scenario_usp_version_ref_pinned(),
        scenario_pipeline_b_envelope_unchanged(),
        scenario_audit_record_per_pass(),
        scenario_diagnostic_export_ordering(),
        scenario_usp_snapshot_immutable(),
        scenario_segmentation_deterministic(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    failed = [s["scenario"] for s in scenarios if s["result"] != "PASS"]
    report = {
        "module": "40.101_iiinb_prototypes",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "phase": "B",
        "status": status,
        "scenarios": scenarios,
        "summary": {
            "total_scenarios": len(scenarios),
            "passed": sum(1 for s in scenarios if s["result"] == "PASS"),
            "failed_scenarios": failed,
            "core_invariants_demonstrated": [
                "profile_enabled_gate",
                "read_only_usp_apply",
                "escalate_without_guess",
                "inb_iiinb_rb_ordering",
                "apply_and_segment_caps",
                "deterministic_replay",
                "envelope_write_guard",
                "pipeline_b_envelope_isolation",
                "usp_version_pinning",
                "tcu_cost_reporting",
                "audit_record_per_pass",
                "diagnostic_export_ordering",
                "multi_rule_precedence",
            ],
            "reason_codes_registry": sorted(REASON_CODES),
        },
    }
    artifact = _write_artifact(report)
    print(f"IIInB harness status: {status}")
    print(f"Scenarios: {report['summary']['passed']}/{report['summary']['total_scenarios']} PASS")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    print(f"Artifact: {artifact}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())