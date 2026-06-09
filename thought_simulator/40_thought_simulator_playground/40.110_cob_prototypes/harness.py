"""Deterministic verification harness for 40.110_cob_prototypes."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import traceback

from prototype import COBDeterministicReject, COBState


MODULE_NAME = "40.110_cob_prototypes"
RUN_COMMAND = "python harness.py"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACT_PATH = ARTIFACT_DIR / "cob_verification_run_2026-06-03.json"


REQ = {
    "lifecycle_lineage": {
        "hlr": "HLR-20.031-003",
        "llr": "LLR-COB-LC-001",
        "doc": "thought_simulator/20_requirements/20.32_cob_requirements.md",
        "section": "Normative Requirements 3, 4, 5, 20",
    },
    "deterministic_replay_export": {
        "hlr": "HLR-20.031-010",
        "llr": "LLR-COB-EXP-001",
        "doc": "thought_simulator/20_requirements/20.32_cob_requirements.md",
        "section": "Normative Requirements 10, 11, 12, 13, 15",
    },
    "profile_precedence": {
        "hlr": "HLR-20.031-016",
        "llr": "LLR-COB-PROF-001",
        "doc": "thought_simulator/20_requirements/20.32_cob_requirements.md",
        "section": "Normative Requirements 16, 17",
    },
    "sequence_determinism": {
        "hlr": "HLR-20.031-014",
        "llr": "LLR-COB-SEQ-001",
        "doc": "thought_simulator/20_requirements/20.32_cob_requirements.md",
        "section": "Normative Requirements 14, 26",
    },
    "unsupported_replay_mode": {
        "hlr": "HLR-20.031-018",
        "llr": "LLR-COB-REJ-001",
        "doc": "thought_simulator/20_requirements/20.32_cob_requirements.md",
        "section": "Normative Requirements 18, 25",
    },
    "safe_boundary": {
        "hlr": "HLR-20.031-024",
        "llr": "LLR-COB-SAFE-001",
        "doc": "thought_simulator/20_requirements/20.32_cob_requirements.md",
        "section": "Normative Requirement 24",
    },
    "unsupported_event": {
        "hlr": "HLR-20.031-018",
        "llr": "LLR-COB-REJ-002",
        "doc": "thought_simulator/20_requirements/20.32_cob_requirements.md",
        "section": "Normative Requirements 18, 25",
    },
}


@dataclass
class ScenarioResult:
    name: str
    status: str
    requirement_key: str
    detail: str
    io_fields: str
    negative_path: str = "NO"

    def as_dict(self) -> dict[str, str]:
        req = REQ[self.requirement_key]
        return {
            "name": self.name,
            "status": self.status,
            "detail": self.detail,
            "hlr_ref": req["hlr"],
            "llr_ref": req["llr"],
            "req_doc": req["doc"],
            "req_section": req["section"],
            "io_fields": self.io_fields,
            "negative_path": self.negative_path,
        }


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _emit_requirement(requirement_key: str) -> None:
    req = REQ[requirement_key]
    print(
        f"REQ ATTACHMENT | HLR={req['hlr']} | LLR={req['llr']} | "
        f"DOC={req['doc']} | SECTION={req['section']}"
    )


def _seed_state() -> COBState:
    return COBState(cob_id="cob.alpha", profile_signature="P1", replay_mode="full", sequence=0)


def scenario_lifecycle_lineage_and_audit() -> tuple[ScenarioResult, dict[str, object]]:
    _emit_requirement("lifecycle_lineage")
    state = _seed_state()

    state.apply_event({"event_type": "promote", "sequence": 1, "safe_boundary": True, "payload": {"winner_lineage": "wl-001"}})
    state.apply_event({"event_type": "split", "sequence": 2, "safe_boundary": True, "payload": {"split_children": ["cob.alpha.1", "cob.alpha.2"]}})
    state.apply_event({"event_type": "merge", "sequence": 3, "safe_boundary": True, "payload": {"merge_sources": ["cob.prev.1", "cob.prev.2"]}})

    snap = state.snapshot()
    _assert(snap["lifecycle_state"] == "active", "promote should set lifecycle_state=active")
    _assert(snap["lineage"]["winner_lineage"] == "wl-001", "winner_lineage mismatch")
    _assert(len(snap["lineage"]["split_children"]) == 2, "split children not recorded")
    _assert(len(snap["lineage"]["merge_sources"]) == 2, "merge sources not recorded")
    _assert(len(snap["audit_log"]) == 4, "audit log should be append-only and include create + 3 transitions")

    return (
        ScenarioResult(
            name="lifecycle_lineage_and_audit",
            status="PASS",
            requirement_key="lifecycle_lineage",
            detail="Lifecycle transitions, lineage fields, and append-only audit behavior validated.",
            io_fields="event_type, sequence, safe_boundary, winner_lineage, split_children, merge_sources -> lifecycle_state, lineage, audit_log",
        ),
        snap,
    )


def scenario_deterministic_replay_and_export() -> tuple[ScenarioResult, dict[str, object], dict[str, object]]:
    _emit_requirement("deterministic_replay_export")

    sequence = [
        {"event_type": "promote", "sequence": 1, "safe_boundary": True, "payload": {"winner_lineage": "wl-100"}},
        {"event_type": "replay_mode_change", "sequence": 2, "safe_boundary": True, "payload": {"replay_mode": "summary_proof"}},
        {
            "event_type": "export",
            "sequence": 3,
            "safe_boundary": True,
            "payload": {"window_events": 0, "env_default_profile": "P2"},
        },
        {"event_type": "compact", "sequence": 4, "safe_boundary": True, "payload": {}},
    ]

    state_one = _seed_state()
    state_two = _seed_state()

    for event in sequence:
        state_one.apply_event(event)
        state_two.apply_event(event)

    snap_one = state_one.snapshot()
    snap_two = state_two.snapshot()

    _assert(snap_one == snap_two, "deterministic replay produced different snapshots")
    _assert(snap_one["exports"][0]["empty_artifact"] is True, "zero-event export should set empty_artifact=true")
    _assert(
        snap_one["exports"][0]["profile_signature"] == "P1",
        "export should preserve active signature over env defaults",
    )

    return (
        ScenarioResult(
            name="deterministic_replay_and_export",
            status="PASS",
            requirement_key="deterministic_replay_export",
            detail="Deterministic replay, empty-artifact export behavior, and canonical digest stability validated.",
            io_fields="replay_mode, profile_signature, window_events, env_default_profile -> exports, summary_proof, verification_digest",
        ),
        snap_one,
        snap_two,
    )


def scenario_profile_precedence() -> ScenarioResult:
    _emit_requirement("profile_precedence")
    state = _seed_state()
    state.apply_event({"event_type": "promote", "sequence": 1, "safe_boundary": True, "payload": {"winner_lineage": "wl-200"}})
    state.apply_event(
        {
            "event_type": "export",
            "sequence": 2,
            "safe_boundary": True,
            "payload": {"window_events": 3, "env_default_profile": "P2"},
        }
    )
    snap = state.snapshot()
    _assert(snap["exports"][0]["profile_signature"] == "P1", "active signature should win")
    return ScenarioResult(
        name="profile_precedence_signature_over_env_default",
        status="PASS",
        requirement_key="profile_precedence",
        detail="Export manifest selected active signature-bound profile over environment default.",
        io_fields="profile_signature, env_default_profile, window_events -> export_manifest.profile_signature",
    )


def scenario_negative_sequence_violation() -> ScenarioResult:
    _emit_requirement("sequence_determinism")
    state = _seed_state()
    state.apply_event({"event_type": "promote", "sequence": 1, "safe_boundary": True, "payload": {"winner_lineage": "wl-301"}})
    try:
        state.apply_event({"event_type": "split", "sequence": 3, "safe_boundary": True, "payload": {"split_children": ["c1", "c2"]}})
    except COBDeterministicReject as exc:
        _assert(exc.reason_code == "COB_RSN_002_SEQUENCE_VIOLATION", "unexpected reason code")
        return ScenarioResult(
            name="negative_sequence_violation",
            status="PASS",
            requirement_key="sequence_determinism",
            detail="Out-of-order sequence was rejected with deterministic reason code.",
            io_fields="sequence -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected deterministic reject for sequence violation")


def scenario_negative_unsupported_replay_mode() -> ScenarioResult:
    _emit_requirement("unsupported_replay_mode")
    state = _seed_state()
    state.apply_event({"event_type": "promote", "sequence": 1, "safe_boundary": True, "payload": {"winner_lineage": "wl-401"}})
    try:
        state.apply_event(
            {
                "event_type": "replay_mode_change",
                "sequence": 2,
                "safe_boundary": True,
                "payload": {"replay_mode": "quantum"},
            }
        )
    except COBDeterministicReject as exc:
        _assert(exc.reason_code == "COB_RSN_004_UNSUPPORTED_REPLAY_MODE", "unexpected reason code")
        return ScenarioResult(
            name="negative_unsupported_replay_mode",
            status="PASS",
            requirement_key="unsupported_replay_mode",
            detail="Unsupported replay mode rejected with fixed deterministic reason code.",
            io_fields="replay_mode -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected deterministic reject for unsupported replay mode")


def scenario_negative_safe_boundary_violation() -> ScenarioResult:
    _emit_requirement("safe_boundary")
    state = _seed_state()
    try:
        state.apply_event({"event_type": "promote", "sequence": 1, "safe_boundary": False, "payload": {"winner_lineage": "wl-501"}})
    except COBDeterministicReject as exc:
        _assert(exc.reason_code == "COB_RSN_003_SAFE_BOUNDARY_REQUIRED", "unexpected reason code")
        return ScenarioResult(
            name="negative_safe_boundary_violation",
            status="PASS",
            requirement_key="safe_boundary",
            detail="Lifecycle transition outside deterministic safe boundary was rejected.",
            io_fields="safe_boundary, event_type -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected deterministic reject for safe-boundary violation")


def scenario_negative_unsupported_event() -> ScenarioResult:
    _emit_requirement("unsupported_event")
    state = _seed_state()
    try:
        state.apply_event({"event_type": "teleport", "sequence": 1, "safe_boundary": True, "payload": {}})
    except COBDeterministicReject as exc:
        _assert(exc.reason_code == "COB_RSN_001_UNSUPPORTED_EVENT", "unexpected reason code")
        return ScenarioResult(
            name="negative_unsupported_event_type",
            status="PASS",
            requirement_key="unsupported_event",
            detail="Unsupported event type rejected with fixed deterministic reason code.",
            io_fields="event_type -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected deterministic reject for unsupported event type")


def _build_report() -> dict[str, object]:
    try:
        lifecycle_result, lifecycle_snapshot = scenario_lifecycle_lineage_and_audit()
        deterministic_result, replay_snapshot_a, replay_snapshot_b = scenario_deterministic_replay_and_export()
        profile_result = scenario_profile_precedence()
        neg_sequence = scenario_negative_sequence_violation()
        neg_mode = scenario_negative_unsupported_replay_mode()
        neg_boundary = scenario_negative_safe_boundary_violation()
        neg_event = scenario_negative_unsupported_event()

        scenario_results = [
            lifecycle_result,
            deterministic_result,
            profile_result,
            neg_sequence,
            neg_mode,
            neg_boundary,
            neg_event,
        ]

        scenarios = [result.as_dict() for result in scenario_results]
        passed = sum(1 for row in scenarios if row["status"] == "PASS")
        failed = len(scenarios) - passed

        return {
            "module": MODULE_NAME,
            "run_command": RUN_COMMAND,
            "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "total_scenarios": len(scenarios),
                "passed": passed,
                "failed": failed,
                "overall_status": "PASS" if failed == 0 else "FAIL",
            },
            "requirements_anchors": [
                "thought_simulator/20_requirements/20.32_cob_requirements.md",
                "thought_simulator/20_requirements/20.10_ts_architectural_principles.md",
                "thought_simulator/20_requirements/20.30_ts_functional_model.md",
                "thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md",
                "thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md",
                "thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md",
            ],
            "scenarios": scenarios,
            "determinism_evidence": {
                "snapshot_a_digest": replay_snapshot_a["verification_digest"],
                "snapshot_b_digest": replay_snapshot_b["verification_digest"],
                "match": replay_snapshot_a == replay_snapshot_b,
            },
            "state_snapshots": {
                "lifecycle_snapshot": lifecycle_snapshot,
                "replay_snapshot": replay_snapshot_a,
            },
        }
    except Exception:
        return {
            "module": MODULE_NAME,
            "run_command": RUN_COMMAND,
            "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "summary": {"total_scenarios": 0, "passed": 0, "failed": 1, "overall_status": "FAIL"},
            "scenarios": [],
            "fatal_error": traceback.format_exc(),
        }


def _write_artifact(report: dict[str, object]) -> Path:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return ARTIFACT_PATH


def main() -> int:
    report = _build_report()
    artifact_path = _write_artifact(report)
    print(f"Module: {MODULE_NAME}")
    print(f"Command: {RUN_COMMAND}")
    print(f"Artifact: {artifact_path}")
    print(f"Overall: {report['summary']['overall_status']}")
    for scenario in report.get("scenarios", []):
        print(f"{scenario['name']}: {scenario['status']}")
    if report["summary"]["overall_status"] == "FAIL" and "fatal_error" in report:
        print(report["fatal_error"])
    return 0 if report["summary"]["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
