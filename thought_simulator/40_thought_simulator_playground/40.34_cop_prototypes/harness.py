"""Deterministic verification harness for 40.34_cop_prototypes."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import traceback

from prototype import COPDeterministicReject, COPState


MODULE_NAME = "40.34_cop_prototypes"
RUN_COMMAND = "python harness.py"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACT_PATH = ARTIFACT_DIR / "cop_verification_run_2026-06-03.json"


REQ = {
    "provenance_queue": {
        "hlr": "HLR-20.033-002",
        "llr": "LLR-COP-PROP-001",
        "doc": "thought_simulator/20_requirements/20.34_cop_requirements.md",
        "section": "Normative Requirements 2, 4, 18, 20",
    },
    "boundary_commit": {
        "hlr": "HLR-20.033-003",
        "llr": "LLR-COP-COMMIT-001",
        "doc": "thought_simulator/20_requirements/20.34_cop_requirements.md",
        "section": "Normative Requirements 1, 3, 9, 12",
    },
    "overload_safety": {
        "hlr": "HLR-20.033-006",
        "llr": "LLR-COP-OL-001",
        "doc": "thought_simulator/20_requirements/20.34_cop_requirements.md",
        "section": "Normative Requirements 4, 6, 7, 18, 19",
    },
    "profile_precedence": {
        "hlr": "HLR-20.033-013",
        "llr": "LLR-COP-PROF-001",
        "doc": "thought_simulator/20_requirements/20.34_cop_requirements.md",
        "section": "Normative Requirements 13, 14",
    },
    "sequence_violation": {
        "hlr": "HLR-20.033-011",
        "llr": "LLR-COP-SEQ-001",
        "doc": "thought_simulator/20_requirements/20.34_cop_requirements.md",
        "section": "Normative Requirements 11, 18, 20",
    },
    "safe_boundary": {
        "hlr": "HLR-20.033-012",
        "llr": "LLR-COP-SAFE-001",
        "doc": "thought_simulator/20_requirements/20.34_cop_requirements.md",
        "section": "Normative Requirements 3, 12, 20",
    },
    "unsupported_state": {
        "hlr": "HLR-20.033-008",
        "llr": "LLR-COP-REJ-001",
        "doc": "thought_simulator/20_requirements/20.34_cop_requirements.md",
        "section": "Normative Requirements 8, 15, 16, 22",
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


def _seed_state(active_profile: str = "P2", env_default_profile: str = "P1") -> COPState:
    return COPState(active_profile=active_profile, env_default_profile=env_default_profile, sequence=0)


def scenario_provenance_queue_fairness() -> tuple[ScenarioResult, dict[str, object]]:
    _emit_requirement("provenance_queue")
    state = _seed_state(active_profile="P1", env_default_profile="P2")
    state.apply_event(
        {
            "event_type": "submit_proposal",
            "sequence": 1,
            "safe_boundary": False,
            "payload": {
                "proposal_id": "cop-001",
                "source": "cil",
                "basis_snapshot": "snap-a",
                "priority": "normal",
                "proposal_input": {"topic": "alpha", "confidence": 0.81},
            },
        }
    )
    state.apply_event(
        {
            "event_type": "submit_proposal",
            "sequence": 2,
            "safe_boundary": False,
            "payload": {
                "proposal_id": "cop-002",
                "source": "cob",
                "basis_snapshot": "snap-b",
                "priority": "normal",
                "proposal_input": {"topic": "beta", "confidence": 0.73},
            },
        }
    )

    snap = state.snapshot()
    _assert(snap["pending_queue"][0]["proposal_id"] == "cop-001", "FIFO ordering violated for first proposal")
    _assert(snap["pending_queue"][1]["proposal_id"] == "cop-002", "FIFO ordering violated for second proposal")
    _assert(
        snap["pending_queue"][0]["deterministic_input_hash"] != snap["pending_queue"][1]["deterministic_input_hash"],
        "distinct proposal inputs should produce distinct hashes",
    )

    return (
        ScenarioResult(
            name="provenance_queue_fairness",
            status="PASS",
            requirement_key="provenance_queue",
            detail="Proposal provenance hashing and deterministic FIFO queue admission validated.",
            io_fields="proposal_id, source, basis_snapshot, proposal_input, sequence -> pending_queue order, deterministic_input_hash",
        ),
        snap,
    )


def scenario_boundary_commit_visibility() -> tuple[ScenarioResult, dict[str, object]]:
    _emit_requirement("boundary_commit")
    state = _seed_state()
    state.apply_event(
        {
            "event_type": "submit_proposal",
            "sequence": 1,
            "safe_boundary": False,
            "payload": {
                "proposal_id": "cop-100",
                "source": "cil",
                "basis_snapshot": "snap-c",
                "priority": "normal",
                "proposal_input": {"summary": "candidate reply"},
            },
        }
    )
    state.apply_event(
        {
            "event_type": "gb_decision",
            "sequence": 2,
            "safe_boundary": True,
            "payload": {"proposal_id": "cop-100", "decision": "approve"},
        }
    )
    staged_snapshot = state.snapshot()
    _assert(len(staged_snapshot["visible_commits"]) == 0, "approved proposal should not be visible before commit")
    _assert(len(staged_snapshot["staged_commits"]) == 1, "approved proposal should remain staged")

    state.apply_event(
        {
            "event_type": "commit_ready",
            "sequence": 3,
            "safe_boundary": True,
            "payload": {"proposal_id": "cop-100"},
        }
    )
    final_snapshot = state.snapshot()
    _assert(len(final_snapshot["visible_commits"]) == 1, "commit should become visible only after safe-boundary commit")
    _assert(final_snapshot["visible_commits"][0]["proposal_id"] == "cop-100", "wrong proposal committed")

    return (
        ScenarioResult(
            name="boundary_commit_visibility",
            status="PASS",
            requirement_key="boundary_commit",
            detail="Approved proposals remain staged until deterministic safe-boundary commit visibility.",
            io_fields="proposal_id, decision, safe_boundary -> staged_commits, visible_commits",
        ),
        final_snapshot,
    )


def scenario_overload_safety_priority() -> tuple[ScenarioResult, dict[str, object]]:
    _emit_requirement("overload_safety")
    state = _seed_state(active_profile="P2", env_default_profile="P1")
    state.apply_event(
        {
            "event_type": "submit_proposal",
            "sequence": 1,
            "safe_boundary": False,
            "payload": {
                "proposal_id": "cop-201",
                "source": "cob",
                "basis_snapshot": "snap-d",
                "priority": "normal",
                "proposal_input": {"work": "summarize"},
            },
        }
    )
    state.apply_event(
        {
            "event_type": "submit_proposal",
            "sequence": 2,
            "safe_boundary": False,
            "payload": {
                "proposal_id": "cop-202",
                "source": "cil",
                "basis_snapshot": "snap-e",
                "priority": "normal",
                "proposal_input": {"work": "classify"},
            },
        }
    )
    state.apply_event(
        {
            "event_type": "submit_proposal",
            "sequence": 3,
            "safe_boundary": False,
            "payload": {
                "proposal_id": "cop-203",
                "source": "gb",
                "basis_snapshot": "snap-f",
                "priority": "safety_critical",
                "proposal_input": {"work": "policy guard"},
            },
        }
    )

    snap = state.snapshot()
    queued_ids = [proposal["proposal_id"] for proposal in snap["pending_queue"]]
    _assert(len(queued_ids) == 2, "queue should remain bounded")
    _assert("cop-203" in queued_ids, "safety-critical proposal should be admitted")
    _assert("cop-201" not in queued_ids, "oldest noncritical proposal should be deterministically preempted")

    return (
        ScenarioResult(
            name="overload_safety_priority",
            status="PASS",
            requirement_key="overload_safety",
            detail="Bounded overload handling deterministically preserves safety-critical admission by preempting noncritical work.",
            io_fields="priority, sequence, max_queue -> bounded queue, preemption, audit_log",
        ),
        snap,
    )


def scenario_profile_precedence() -> ScenarioResult:
    _emit_requirement("profile_precedence")
    state = _seed_state(active_profile="P2", env_default_profile="P1")
    state.apply_event(
        {
            "event_type": "submit_proposal",
            "sequence": 1,
            "safe_boundary": False,
            "payload": {
                "proposal_id": "cop-301",
                "source": "cil",
                "basis_snapshot": "snap-g",
                "priority": "normal",
                "proposal_input": {"work": "routine"},
            },
        }
    )
    state.apply_event(
        {
            "event_type": "submit_proposal",
            "sequence": 2,
            "safe_boundary": False,
            "payload": {
                "proposal_id": "cop-302",
                "source": "gb",
                "basis_snapshot": "snap-h",
                "priority": "safety_critical",
                "proposal_input": {"work": "guard"},
            },
        }
    )

    snap = state.snapshot()
    _assert(snap["policy"]["fairness_policy"] == "safety_first", "active profile should control fairness policy")
    _assert(snap["env_default_profile"] == "P1", "environment default should remain unchanged")
    _assert(snap["pending_queue"][0]["proposal_id"] == "cop-302", "safety-first ordering should dominate env default")

    return ScenarioResult(
        name="profile_precedence_signature_over_env_default",
        status="PASS",
        requirement_key="profile_precedence",
        detail="Execution-signature profile controls COP queue policy; environment default remains non-authoritative.",
        io_fields="active_profile, env_default_profile, priority -> policy selection, pending_queue order",
    )


def scenario_negative_sequence_violation() -> ScenarioResult:
    _emit_requirement("sequence_violation")
    state = _seed_state()
    state.apply_event(
        {
            "event_type": "submit_proposal",
            "sequence": 1,
            "safe_boundary": False,
            "payload": {
                "proposal_id": "cop-401",
                "source": "cil",
                "basis_snapshot": "snap-i",
                "priority": "normal",
                "proposal_input": {"work": "draft"},
            },
        }
    )
    try:
        state.apply_event(
            {
                "event_type": "gb_decision",
                "sequence": 3,
                "safe_boundary": True,
                "payload": {"proposal_id": "cop-401", "decision": "approve"},
            }
        )
    except COPDeterministicReject as exc:
        _assert(exc.reason_code == "COP_RSN_002_SEQUENCE_VIOLATION", "unexpected reason code")
        return ScenarioResult(
            name="negative_sequence_violation",
            status="PASS",
            requirement_key="sequence_violation",
            detail="Out-of-order sequence was rejected with deterministic reason code.",
            io_fields="sequence -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected sequence violation reject")


def scenario_negative_safe_boundary_violation() -> ScenarioResult:
    _emit_requirement("safe_boundary")
    state = _seed_state()
    state.apply_event(
        {
            "event_type": "submit_proposal",
            "sequence": 1,
            "safe_boundary": False,
            "payload": {
                "proposal_id": "cop-501",
                "source": "cil",
                "basis_snapshot": "snap-j",
                "priority": "normal",
                "proposal_input": {"work": "draft"},
            },
        }
    )
    try:
        state.apply_event(
            {
                "event_type": "gb_decision",
                "sequence": 2,
                "safe_boundary": False,
                "payload": {"proposal_id": "cop-501", "decision": "approve"},
            }
        )
    except COPDeterministicReject as exc:
        _assert(exc.reason_code == "COP_RSN_003_SAFE_BOUNDARY_REQUIRED", "unexpected reason code")
        return ScenarioResult(
            name="negative_safe_boundary_violation",
            status="PASS",
            requirement_key="safe_boundary",
            detail="Boundary-sensitive supervisory action outside safe boundary was rejected.",
            io_fields="safe_boundary, event_type -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected safe-boundary reject")


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
    except COPDeterministicReject as exc:
        _assert(exc.reason_code == "COP_RSN_004_UNSUPPORTED_PROFILE", "unexpected reason code")
        return ScenarioResult(
            name="negative_unsupported_profile",
            status="PASS",
            requirement_key="unsupported_state",
            detail="Unsupported profile was rejected with fixed deterministic reason code.",
            io_fields="profile -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected unsupported profile reject")


def _build_report() -> dict[str, object]:
    try:
        provenance_result, provenance_snapshot = scenario_provenance_queue_fairness()
        boundary_result, boundary_snapshot = scenario_boundary_commit_visibility()
        overload_result, overload_snapshot = scenario_overload_safety_priority()
        profile_result = scenario_profile_precedence()
        neg_seq = scenario_negative_sequence_violation()
        neg_safe = scenario_negative_safe_boundary_violation()
        neg_profile = scenario_negative_unsupported_profile()

        scenarios = [
            provenance_result.as_dict(),
            boundary_result.as_dict(),
            overload_result.as_dict(),
            profile_result.as_dict(),
            neg_seq.as_dict(),
            neg_safe.as_dict(),
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
                "thought_simulator/20_requirements/20.34_cop_requirements.md",
                "thought_simulator/20_requirements/20.30_ts_functional_model.md",
                "thought_simulator/20_requirements/20.10_ts_architectural_principles.md",
                "thought_simulator/20_requirements/20.80_gb_requirements.md",
                "thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md",
                "thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md",
                "thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md",
            ],
            "scenarios": scenarios,
            "determinism_evidence": {
                "provenance_queue_digest": provenance_snapshot["verification_digest"],
                "boundary_commit_digest": boundary_snapshot["verification_digest"],
                "overload_queue_order": [proposal["proposal_id"] for proposal in overload_snapshot["pending_queue"]],
            },
            "state_snapshots": {
                "provenance_snapshot": provenance_snapshot,
                "boundary_snapshot": boundary_snapshot,
                "overload_snapshot": overload_snapshot,
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
