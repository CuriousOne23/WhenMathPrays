"""Deterministic verification harness for 40.120_cil_prototypes."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import traceback

from prototype import CILDeterministicReject, CILState


MODULE_NAME = "40.120_cil_prototypes"
RUN_COMMAND = "python harness.py"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACT_PATH = ARTIFACT_DIR / "cil_verification_run_2026-06-03.json"


REQ = {
    "fifo_snapshot": {
        "hlr": "HLR-20.032-001",
        "llr": "LLR-CIL-FIFO-001",
        "doc": "thought_simulator/20_requirements/20.33_cil_requirements.md",
        "section": "Normative Requirements 1, 2, 22",
    },
    "classification_escalation": {
        "hlr": "HLR-20.032-003",
        "llr": "LLR-CIL-CLS-001",
        "doc": "thought_simulator/20_requirements/20.33_cil_requirements.md",
        "section": "Normative Requirements 3, 4, 9",
    },
    "gb_timeout_reentry": {
        "hlr": "HLR-20.032-006",
        "llr": "LLR-CIL-GB-001",
        "doc": "thought_simulator/20_requirements/20.33_cil_requirements.md",
        "section": "Normative Requirements 6, 7, 23",
    },
    "profile_precedence": {
        "hlr": "HLR-20.032-012",
        "llr": "LLR-CIL-PROF-001",
        "doc": "thought_simulator/20_requirements/20.33_cil_requirements.md",
        "section": "Normative Requirements 12, 13",
    },
    "sequence_violation": {
        "hlr": "HLR-20.032-014",
        "llr": "LLR-CIL-SEQ-001",
        "doc": "thought_simulator/20_requirements/20.33_cil_requirements.md",
        "section": "Normative Requirements 14, 22",
    },
    "safe_boundary": {
        "hlr": "HLR-20.032-015",
        "llr": "LLR-CIL-SAFE-001",
        "doc": "thought_simulator/20_requirements/20.33_cil_requirements.md",
        "section": "Normative Requirement 15",
    },
    "direct_inquiry_bypass": {
        "hlr": "HLR-20.032-005",
        "llr": "LLR-CIL-GB-002",
        "doc": "thought_simulator/20_requirements/20.33_cil_requirements.md",
        "section": "Normative Requirements 5, 18",
    },
    "unsupported_state": {
        "hlr": "HLR-20.032-011",
        "llr": "LLR-CIL-REJ-001",
        "doc": "thought_simulator/20_requirements/20.33_cil_requirements.md",
        "section": "Normative Requirements 11, 20, 21",
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


def _seed_state() -> CILState:
    return CILState(active_profile="P1", env_default_profile="P2", sequence=0)


def scenario_fifo_snapshot_coherence() -> tuple[ScenarioResult, dict[str, object]]:
    _emit_requirement("fifo_snapshot")
    state = _seed_state()
    state.apply_event(
        {
            "event_type": "ingest",
            "sequence": 1,
            "safe_boundary": True,
            "payload": {"packet_id": "pkt-001", "snapshot_id": "snap-a", "confidence": 0.95},
        }
    )
    state.apply_event(
        {
            "event_type": "ingest",
            "sequence": 2,
            "safe_boundary": True,
            "payload": {"packet_id": "pkt-002", "snapshot_id": "snap-a", "confidence": 0.99},
        }
    )
    state.apply_event({"event_type": "process_next", "sequence": 3, "safe_boundary": True, "payload": {}})
    state.apply_event({"event_type": "process_next", "sequence": 4, "safe_boundary": True, "payload": {}})

    snap = state.snapshot()
    _assert(snap["integrated_packets"][0]["packet_id"] == "pkt-001", "FIFO order violated for first packet")
    _assert(snap["integrated_packets"][1]["packet_id"] == "pkt-002", "FIFO order violated for second packet")
    _assert(snap["integrated_packets"][0]["snapshot_id"] == "snap-a", "snapshot coherence missing")
    _assert(snap["integrated_packets"][1]["snapshot_id"] == "snap-a", "snapshot coherence missing")

    return (
        ScenarioResult(
            name="fifo_snapshot_coherence",
            status="PASS",
            requirement_key="fifo_snapshot",
            detail="FIFO-preserving intake and snapshot coherence validated.",
            io_fields="packet_id, snapshot_id, sequence, safe_boundary -> integrated_packets ordering",
        ),
        snap,
    )


def scenario_classification_escalation_gb_flow() -> ScenarioResult:
    _emit_requirement("classification_escalation")
    _emit_requirement("gb_timeout_reentry")

    state = _seed_state()
    state.apply_event(
        {
            "event_type": "ingest",
            "sequence": 1,
            "safe_boundary": True,
            "payload": {"packet_id": "pkt-100", "snapshot_id": "snap-b", "confidence": 0.20},
        }
    )
    state.apply_event({"event_type": "process_next", "sequence": 2, "safe_boundary": True, "payload": {}})
    _assert(len(state.escalation_requests) == 1, "low-confidence packet should escalate")

    request_id = state.escalation_requests[0]["request_id"]
    state.apply_event(
        {
            "event_type": "gb_response",
            "sequence": 3,
            "safe_boundary": True,
            "payload": {"request_id": request_id, "decision": "timeout"},
        }
    )
    _assert(state.escalation_requests[0]["status"] == "timeout_default_deny", "timeout default path incorrect")

    state.apply_event(
        {
            "event_type": "gb_response",
            "sequence": 4,
            "safe_boundary": True,
            "payload": {"request_id": request_id, "decision": "late_approve"},
        }
    )
    _assert(state.escalation_requests[0]["status"] == "late_approved_queued", "late approval re-entry mismatch")

    return ScenarioResult(
        name="classification_escalation_gb_flow",
        status="PASS",
        requirement_key="gb_timeout_reentry",
        detail="Deterministic escalation, timeout default, and late-approval re-entry behavior validated.",
        io_fields="confidence, request_id, decision, safe_boundary -> escalation_requests status, integrated_packets",
    )


def scenario_profile_precedence() -> ScenarioResult:
    _emit_requirement("profile_precedence")
    state = _seed_state()
    state.apply_event(
        {
            "event_type": "ingest",
            "sequence": 1,
            "safe_boundary": True,
            "payload": {"packet_id": "pkt-200", "snapshot_id": "snap-c", "confidence": 0.70},
        }
    )
    # Under P1 (threshold=0.75), this packet should escalate when processed.
    state.apply_event({"event_type": "process_next", "sequence": 2, "safe_boundary": True, "payload": {}})
    _assert(len(state.escalation_requests) == 1, "packet should escalate under P1 threshold")

    state.apply_event(
        {
            "event_type": "profile_change",
            "sequence": 3,
            "safe_boundary": True,
            "payload": {"profile": "P2"},
        }
    )
    _assert(state.active_profile == "P2", "profile change failed")
    _assert(state.env_default_profile == "P2", "env default should remain unchanged")

    return ScenarioResult(
        name="profile_precedence_signature_over_env_default",
        status="PASS",
        requirement_key="profile_precedence",
        detail="Execution-signature profile controls behavior; environment defaults remain non-authoritative.",
        io_fields="active_profile, env_default_profile, confidence -> escalation behavior and profile state",
    )


def scenario_negative_sequence_violation() -> ScenarioResult:
    _emit_requirement("sequence_violation")
    state = _seed_state()
    state.apply_event(
        {
            "event_type": "ingest",
            "sequence": 1,
            "safe_boundary": True,
            "payload": {"packet_id": "pkt-300", "snapshot_id": "snap-d", "confidence": 0.9},
        }
    )
    try:
        state.apply_event({"event_type": "process_next", "sequence": 3, "safe_boundary": True, "payload": {}})
    except CILDeterministicReject as exc:
        _assert(exc.reason_code == "CIL_RSN_002_SEQUENCE_VIOLATION", "unexpected reason code")
        return ScenarioResult(
            name="negative_sequence_violation",
            status="PASS",
            requirement_key="sequence_violation",
            detail="Out-of-order sequence rejected with deterministic reason code.",
            io_fields="sequence -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected sequence violation reject")


def scenario_negative_safe_boundary_violation() -> ScenarioResult:
    _emit_requirement("safe_boundary")
    state = _seed_state()
    try:
        state.apply_event({"event_type": "process_next", "sequence": 1, "safe_boundary": False, "payload": {}})
    except CILDeterministicReject as exc:
        _assert(exc.reason_code == "CIL_RSN_003_SAFE_BOUNDARY_REQUIRED", "unexpected reason code")
        return ScenarioResult(
            name="negative_safe_boundary_violation",
            status="PASS",
            requirement_key="safe_boundary",
            detail="Routing/escalation-affecting transition outside safe boundary was rejected.",
            io_fields="safe_boundary, event_type -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected safe-boundary reject")


def scenario_negative_direct_inquiry_bypass() -> ScenarioResult:
    _emit_requirement("direct_inquiry_bypass")
    state = _seed_state()
    try:
        state.apply_event(
            {
                "event_type": "ingest",
                "sequence": 1,
                "safe_boundary": True,
                "payload": {
                    "packet_id": "pkt-400",
                    "snapshot_id": "snap-e",
                    "confidence": 0.8,
                    "request_channel": "direct_inquiry",
                },
            }
        )
    except CILDeterministicReject as exc:
        _assert(exc.reason_code == "CIL_RSN_006_DIRECT_INQUIRY_BYPASS", "unexpected reason code")
        return ScenarioResult(
            name="negative_direct_inquiry_bypass",
            status="PASS",
            requirement_key="direct_inquiry_bypass",
            detail="Direct inquiry channel bypass rejected without GB approval.",
            io_fields="request_channel -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected direct inquiry bypass reject")


def scenario_negative_unsupported_profile() -> ScenarioResult:
    _emit_requirement("unsupported_state")
    state = _seed_state()
    try:
        state.apply_event(
            {
                "event_type": "profile_change",
                "sequence": 1,
                "safe_boundary": True,
                "payload": {"profile": "P9"},
            }
        )
    except CILDeterministicReject as exc:
        _assert(exc.reason_code == "CIL_RSN_004_UNSUPPORTED_PROFILE", "unexpected reason code")
        return ScenarioResult(
            name="negative_unsupported_profile",
            status="PASS",
            requirement_key="unsupported_state",
            detail="Unsupported profile rejected with fixed deterministic reason code.",
            io_fields="profile -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected unsupported profile reject")


def _build_report() -> dict[str, object]:
    try:
        fifo_result, fifo_snapshot = scenario_fifo_snapshot_coherence()
        class_result = scenario_classification_escalation_gb_flow()
        profile_result = scenario_profile_precedence()
        neg_seq = scenario_negative_sequence_violation()
        neg_safe = scenario_negative_safe_boundary_violation()
        neg_direct = scenario_negative_direct_inquiry_bypass()
        neg_profile = scenario_negative_unsupported_profile()

        scenarios = [
            fifo_result.as_dict(),
            class_result.as_dict(),
            profile_result.as_dict(),
            neg_seq.as_dict(),
            neg_safe.as_dict(),
            neg_direct.as_dict(),
            neg_profile.as_dict(),
        ]

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
                "thought_simulator/20_requirements/20.33_cil_requirements.md",
                "thought_simulator/20_requirements/20.30_ts_functional_model.md",
                "thought_simulator/20_requirements/20.10_ts_architectural_principles.md",
                "thought_simulator/20_requirements/20.80_gb_requirements.md",
                "thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md",
                "thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md",
                "thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md",
            ],
            "scenarios": scenarios,
            "determinism_evidence": {
                "fifo_snapshot_digest": fifo_snapshot["verification_digest"],
                "queue_empty_after_fifo": len(fifo_snapshot["pending_queue"]) == 0,
                "integrated_order": [pkt["packet_id"] for pkt in fifo_snapshot["integrated_packets"]],
            },
            "state_snapshots": {
                "fifo_snapshot": fifo_snapshot,
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
