"""Harness for 40.70 replay prototypes (Phase B complete).

Scenarios: REPLAY_CLASS_7 C7-A..E, E1 strip, regen validation scaffold,
Class 1 strip demo, governance guards, deterministic replay.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import (
    CLASS_7_FIXTURE_IDS,
    CLASS_7_RUNNERS,
    REPLAY_VERDICTS,
    STRIP_SCOPE,
    assert_no_forbidden_lane_tp_fields,
    b_regeneration_equivalent_scaffold,
    canonical_json_digest,
    export_replay_diagnostics,
    merge_regeneration_input,
    run_c7_a,
    run_c7_b,
    run_c7_c,
    run_c7_d,
    run_c7_e,
    run_class_7_suite,
    strip_b_envelopes,
    validate_regeneration_input,
)

ARTIFACT_NAME = "replay_class7_verification_run_2026-06-08.json"


def _wrap_c7(name: str, runner, hlr: list[str]) -> dict:
    result = runner()
    return {
        "scenario": name,
        "hlr": hlr,
        "result": "PASS" if result["pass"] else "FAIL",
        "sub_id": result.get("sub_id"),
        "fixture_id": result.get("fixture_id"),
        "assertions": result.get("assertions"),
    }


def scenario_c7_a() -> dict:
    return _wrap_c7("replay_c7_a_profile_disabled", run_c7_a, ["HLR-20.36-059"])


def scenario_c7_b() -> dict:
    return _wrap_c7("replay_c7_b_usp_rule_apply", run_c7_b, ["HLR-20.36-058", "HLR-20.36-060"])


def scenario_c7_c() -> dict:
    return _wrap_c7("replay_c7_c_escalate_no_guess", run_c7_c, ["HLR-20.36-058", "HLR-20.36-060"])


def scenario_c7_d() -> dict:
    return _wrap_c7("replay_c7_d_cross_turn_usp", run_c7_d, ["HLR-20.36-061"])


def scenario_c7_e() -> dict:
    return _wrap_c7("replay_c7_e_gb_veto", run_c7_e, ["HLR-20.36-062"])


def scenario_strip_replay_invariant() -> dict:
    trace = {
        "semantic_core": {"meaning": "frozen"},
        "exec_plan": {"should_strip": True},
        "exec_trace": {"should_strip": True},
        "input_repair_tags": [{"segment_ref": "seg-001"}],
    }
    stripped = strip_b_envelopes(trace)
    ok = (
        "exec_plan" not in stripped
        and "exec_trace" not in stripped
        and "semantic_core" in stripped
        and stripped["input_repair_tags"]
    )
    return {
        "scenario": "positive_strip_replay_invariant",
        "hlr": ["HLR-20.207-001", "HLR-20.207-019"],
        "result": "PASS" if ok else "FAIL",
        "stripped_digest": canonical_json_digest(stripped),
    }


def scenario_strip_semantic_core_retained() -> dict:
    core = {"commit_id": "c-001", "meaning": "frozen"}
    trace = {"semantic_core": core, "exec_plan": {"x": 1}, "exec_trace": {"y": 2}}
    stripped = strip_b_envelopes(trace)
    ok = stripped["semantic_core"] == core
    return {
        "scenario": "positive_strip_semantic_core_retained",
        "hlr": ["HLR-20.207-001", "HLR-20.36-060"],
        "result": "PASS" if ok else "FAIL",
    }


def scenario_strip_digest_deterministic() -> dict:
    trace = {"semantic_core": {"a": 1}, "exec_plan": {"b": 2}, "exec_trace": {"c": 3}}
    d1 = canonical_json_digest(strip_b_envelopes(trace))
    d2 = canonical_json_digest(strip_b_envelopes(trace))
    ok = d1 == d2
    return {
        "scenario": "positive_strip_digest_deterministic",
        "hlr": ["HLR-20.36-018"],
        "result": "PASS" if ok else "FAIL",
        "digest": d1,
    }


def scenario_class7_suite_deterministic() -> dict:
    a = run_class_7_suite()
    b = run_class_7_suite()
    ok = (
        a["status"] == b["status"] == "PASS"
        and all(
            a["sub_scenarios"][k]["pass"] == b["sub_scenarios"][k]["pass"]
            for k in a["sub_scenarios"]
        )
    )
    return {
        "scenario": "positive_class7_suite_deterministic",
        "hlr": ["HLR-20.36-058"],
        "result": "PASS" if ok else "FAIL",
    }


def scenario_c7_b_intake_path_order() -> dict:
    result = run_c7_b()
    from prototype import run_intake_path, InB, UspSnapshot, UspRule

    inb_out = InB().normalize({"content": "see tmrw", "source": "c7b", "intake_order": 0})
    snap = UspSnapshot(usp_version_id=1, rules=[UspRule(rule_id="rule-abc", pattern="tmrw", expansion="tomorrow")])
    intake = run_intake_path(inb_out, profile_enabled=True, usp_snapshot=snap)
    names = [s["stage_name"] for s in intake["intake_path"]]
    ok = names == ["inb_surface_norm", "input_semantic_repair", "routing"] and result["pass"]
    return {
        "scenario": "positive_c7_b_intake_path_order",
        "hlr": ["HLR-20.36-058", "HLR-20.101-003"],
        "result": "PASS" if ok else "FAIL",
        "stage_names": names,
    }


def scenario_class1_strip_semantic_core_stable() -> dict:
    """Class 1 E1 strip minimum: semantic_core stable across strip (W1 demo)."""
    trace = {
        "semantic_core": {"commit_id": "cmt-1", "lanes": ["L1"]},
        "exec_plan": {"opbeh_id": "ob1"},
        "exec_trace": {"imr_record": []},
    }
    s1 = strip_b_envelopes(trace)
    s2 = strip_b_envelopes(trace)
    ok = s1["semantic_core"] == s2["semantic_core"] == trace["semantic_core"]
    return {
        "scenario": "positive_class1_strip_semantic_core_stable",
        "hlr": ["HLR-20.36-021", "HLR-20.207-001"],
        "result": "PASS" if ok else "FAIL",
    }


def scenario_negative_regen_input_incomplete() -> dict:
    out = validate_regeneration_input({})
    ok = out["verdict"] == "FAIL_REGEN_INPUT" and out["reason_code"] == "REGEN_INPUT_INCOMPLETE"
    return {
        "scenario": "negative_regen_input_incomplete",
        "hlr": ["HLR-20.207-004", "HLR-20.207-028"],
        "result": "PASS" if ok else "FAIL",
        "validation": out,
    }


def scenario_negative_regen_forbidden_lane_tp() -> dict:
    out = validate_regeneration_input(
        {
            "commit_id": "c1",
            "semantic_snapshot_ref": "ref-1",
            "routing_epoch_id": "epoch-1",
            "seed_scope_ref": "seed-1",
            "lane_id": "forbidden",
        }
    )
    ok = out["verdict"] == "FAIL_REGEN_FORBIDDEN_READ"
    return {
        "scenario": "negative_regen_forbidden_lane_tp",
        "hlr": ["HLR-20.207-007", "HLR-20.207-029", "HLR-20.36-053"],
        "result": "PASS" if ok else "FAIL",
        "validation": out,
    }


def scenario_scaffold_b_regeneration_equivalent() -> dict:
    fixture_root = {
        "cycle_id": "cycle-001",
        "policy_signature": "pol-1",
        "execution_signature": "exec-1",
        "published_routing_tables": {"epoch": 1},
    }
    regen_input = {
        "commit_id": "cmt-1",
        "semantic_snapshot_ref": "snap-hash-1",
        "routing_epoch_id": "epoch-1",
        "seed_scope_ref": "seed-1",
    }
    merged = merge_regeneration_input(fixture_root, regen_input)
    scaffold = b_regeneration_equivalent_scaffold(regen_input, fixture_root=fixture_root)
    ok = (
        scaffold["pass"]
        and scaffold["replay_verdict"] == "SCAFFOLD_DEFERRED"
        and merged["cycle_id"] == "cycle-001"
    )
    return {
        "scenario": "scaffold_b_regeneration_equivalent",
        "hlr": ["HLR-20.207-017", "HLR-20.207-020"],
        "result": "PASS" if ok else "FAIL",
        "scaffold": scaffold,
    }


def scenario_positive_regen_merge_from_fixture_root() -> dict:
    root = {"cycle_id": "c-root", "policy_signature": "p-root"}
    partial = {
        "commit_id": "cmt",
        "semantic_snapshot_ref": "ref",
        "routing_epoch_id": "ep",
        "seed_scope_ref": "seed",
    }
    merged = merge_regeneration_input(root, partial)
    ok = merged["cycle_id"] == "c-root" and validate_regeneration_input(merged)["verdict"] == "PASS"
    return {
        "scenario": "positive_regen_merge_from_fixture_root",
        "hlr": ["HLR-20.207-004"],
        "result": "PASS" if ok else "FAIL",
    }


def scenario_positive_no_forbidden_b_fields() -> dict:
    clean = {"exec_plan": {"opbeh_id": "x"}, "exec_trace": {"stage": "oub"}}
    dirty = {"exec_plan": {"lane_id": "bad"}, "exec_trace": {}}
    ok = assert_no_forbidden_lane_tp_fields(clean) and not assert_no_forbidden_lane_tp_fields(dirty)
    return {
        "scenario": "positive_b_envelope_no_lane_tp",
        "hlr": ["HLR-20.36-053", "HLR-20.207-007"],
        "result": "PASS" if ok else "FAIL",
    }


def scenario_positive_class7_fixture_ids() -> dict:
    ok = all(
        CLASS_7_RUNNERS[sub_id]().get("fixture_id") == fixture_id
        for sub_id, fixture_id in CLASS_7_FIXTURE_IDS.items()
    )
    return {
        "scenario": "positive_class7_fixture_ids",
        "hlr": ["HLR-20.36-017"],
        "result": "PASS" if ok else "FAIL",
    }


def scenario_positive_replay_diagnostic_export() -> dict:
    records = [
        {"replay_class": "REPLAY_CLASS_7", "fixture_id": "REPLAY_C7_USP_RULE_APPLY"},
        {"replay_class": "REPLAY_CLASS_7", "fixture_id": "REPLAY_C7_PROFILE_DISABLED"},
    ]
    export_a = export_replay_diagnostics(records)
    export_b = export_replay_diagnostics(list(reversed(records)))
    parsed = json.loads(export_a)
    ok = (
        export_a == export_b
        and [r["fixture_id"] for r in parsed]
        == ["REPLAY_C7_PROFILE_DISABLED", "REPLAY_C7_USP_RULE_APPLY"]
    )
    return {
        "scenario": "positive_replay_diagnostic_export",
        "hlr": ["HLR-20.36-018"],
        "result": "PASS" if ok else "FAIL",
        "export": export_a,
    }


def _write_artifact(report: dict) -> Path:
    artifact_dir = Path(__file__).resolve().parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    path = artifact_dir / ARTIFACT_NAME
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return path


def main() -> int:
    scenarios = [
        scenario_c7_a(),
        scenario_c7_b(),
        scenario_c7_c(),
        scenario_c7_d(),
        scenario_c7_e(),
        scenario_strip_replay_invariant(),
        scenario_strip_semantic_core_retained(),
        scenario_strip_digest_deterministic(),
        scenario_class7_suite_deterministic(),
        scenario_c7_b_intake_path_order(),
        scenario_class1_strip_semantic_core_stable(),
        scenario_negative_regen_input_incomplete(),
        scenario_negative_regen_forbidden_lane_tp(),
        scenario_scaffold_b_regeneration_equivalent(),
        scenario_positive_regen_merge_from_fixture_root(),
        scenario_positive_no_forbidden_b_fields(),
        scenario_positive_class7_fixture_ids(),
        scenario_positive_replay_diagnostic_export(),
    ]
    status = "PASS" if all(s["result"] == "PASS" for s in scenarios) else "FAIL"
    failed = [s["scenario"] for s in scenarios if s["result"] != "PASS"]
    report = {
        "module": "40.70_replay_prototypes",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "phase": "B",
        "status": status,
        "scenarios": scenarios,
        "class_7_suite": run_class_7_suite(),
        "summary": {
            "total_scenarios": len(scenarios),
            "passed": sum(1 for s in scenarios if s["result"] == "PASS"),
            "failed_scenarios": failed,
            "c7_sub_scenarios": len(CLASS_7_FIXTURE_IDS),
            "core_invariants_demonstrated": [
                "replay_class_7_c7_a_through_e",
                "e1_strip_scope",
                "semantic_core_retained_on_strip",
                "class7_deterministic_replay",
                "intake_path_ordering",
                "regen_input_validation",
                "b_regeneration_scaffold",
                "b_envelope_no_lane_tp",
                "replay_diagnostic_export",
            ],
            "replay_verdicts_registry": sorted(REPLAY_VERDICTS),
            "strip_scope": list(STRIP_SCOPE),
        },
    }
    artifact = _write_artifact(report)
    print(f"Replay harness status: {status}")
    print(f"Scenarios: {report['summary']['passed']}/{report['summary']['total_scenarios']} PASS")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    print(f"Artifact: {artifact}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())