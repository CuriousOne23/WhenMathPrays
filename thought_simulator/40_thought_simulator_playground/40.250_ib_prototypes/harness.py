"""Deterministic verification harness for 40.250_ib_prototypes."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import traceback

from prototype import IBDeterministicReject, IBState


MODULE_NAME = "40.250_ib_prototypes"
RUN_COMMAND = "python harness.py"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACT_PATH = ARTIFACT_DIR / "ib_verification_run_2026-06-09.json"


REQ = {
    "async_creation": {
        "hlr": "HLR-20.090-006",
        "llr": "LLR-IB-CREATE-001",
        "doc": "thought_simulator/20_requirements/20.90_ib_requirements.md",
        "section": "Normative Requirements 6, 32, 33",
    },
    "evolution_tp": {
        "hlr": "HLR-20.090-008",
        "llr": "LLR-IB-EVOLVE-001",
        "doc": "thought_simulator/20_requirements/20.90_ib_requirements.md",
        "section": "Normative Requirements 8, 14, 35, 36, 37, 38",
    },
    "split_merge": {
        "hlr": "HLR-20.090-021",
        "llr": "LLR-IB-LC-001",
        "doc": "thought_simulator/20_requirements/20.90_ib_requirements.md",
        "section": "Normative Requirements 19, 21, 22",
    },
    "promote_retire": {
        "hlr": "HLR-20.090-023",
        "llr": "LLR-IB-PROM-001",
        "doc": "thought_simulator/20_requirements/20.90_ib_requirements.md",
        "section": "Normative Requirements 23, 24, 25, 26",
    },
    "direct_bypass": {
        "hlr": "HLR-20.090-007",
        "llr": "LLR-IB-REJ-001",
        "doc": "thought_simulator/20_requirements/20.90_ib_requirements.md",
        "section": "Normative Requirement 7",
    },
    "safe_boundary": {
        "hlr": "HLR-20.090-020",
        "llr": "LLR-IB-SAFE-001",
        "doc": "thought_simulator/20_requirements/20.90_ib_requirements.md",
        "section": "Normative Requirements 20, 38",
    },
    "sequence_violation": {
        "hlr": "HLR-20.090-019",
        "llr": "LLR-IB-SEQ-001",
        "doc": "thought_simulator/20_requirements/20.90_ib_requirements.md",
        "section": "Normative Requirements 19, 34, 38",
    },
    # W3 Extension (40.510-411)
    "w3_iiinb_ib_distinction": {
        "hlr": "20.510 §15.3, 20.17",
        "llr": "LLR-IB-W3-001",
        "doc": "thought_simulator/20_requirements/20.510_refactoring_for_input_correction_track_h.md",
        "section": "§15.3; 20.17_messy_input_handling.md",
    },
    "w3_imr_pipeline_a_only": {
        "hlr": "20.510 §15.3, 20.17",
        "llr": "LLR-IB-W3-002",
        "doc": "thought_simulator/20_requirements/20.510_refactoring_for_input_correction_track_h.md",
        "section": "§15.3; 20.17_messy_input_handling.md",
    },
    "w3_iiinb_cil_cross": {
        "hlr": "20.510 §15.3, 20.17",
        "llr": "LLR-IB-W3-003",
        "doc": "thought_simulator/20_requirements/20.510_refactoring_for_input_correction_track_h.md",
        "section": "§15.3; 20.17_messy_input_handling.md",
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


def _seed_state() -> IBState:
    return IBState(profile_signature="P1", sequence=0)


def _create_approved_ib(state: IBState, base_sequence: int, ib_id: str, snapshot_id: str) -> int:
    state.apply_event(
        {
            "event_type": "request_create",
            "sequence": base_sequence,
            "safe_boundary": False,
            "payload": {
                "snapshot_id": snapshot_id,
                "triggering_ob_ids": ["ob-1", "ob-2"],
                "request_reason": "ambiguity_detected",
                "source_channel": "ob_ib",
            },
        }
    )
    request_id = state.snapshot()["pending_requests"][0]["request_id"]
    state.apply_event(
        {
            "event_type": "gb_decision",
            "sequence": base_sequence + 1,
            "safe_boundary": True,
            "payload": {
                "request_id": request_id,
                "decision": "approve",
                "ib_id": ib_id,
                "hypotheses": ["h1"],
                "pending_evidence_requests": ["ask_user"],
                "gb_reference": f"gb-ref-{ib_id}",
            },
        }
    )
    return base_sequence + 1


def scenario_async_creation_approval() -> tuple[ScenarioResult, dict[str, object]]:
    _emit_requirement("async_creation")
    state = _seed_state()
    next_sequence = _create_approved_ib(state, 1, "ib-001", "snap-a")
    snap = state.snapshot()
    _assert(next_sequence == 2, "unexpected sequence after approval")
    _assert(len(snap["pending_requests"]) == 0, "approved request should be removed from pending queue")
    _assert(snap["active_ibs"][0]["ib_id"] == "ib-001", "approved IB was not instantiated")
    _assert(snap["active_ibs"][0]["origin_snapshot"] == "snap-a", "origin snapshot mismatch")
    return (
        ScenarioResult(
            name="async_creation_approval",
            status="PASS",
            requirement_key="async_creation",
            detail="Asynchronous GB approval creates IB state only from approved pending inquiry snapshots.",
            io_fields="snapshot_id, request_id, decision, gb_reference -> pending_requests, active_ibs",
        ),
        snap,
    )


def scenario_deterministic_evolution_tp_tagging() -> ScenarioResult:
    _emit_requirement("evolution_tp")
    state = _seed_state()
    _create_approved_ib(state, 1, "ib-002", "snap-b")
    state.apply_event(
        {
            "event_type": "evolve",
            "sequence": 3,
            "safe_boundary": True,
            "payload": {
                "ib_id": "ib-002",
                "hypothesis_delta": ["h2"],
                "evidence_request_delta": ["ask_history"],
                "partial_interpretations": ["interp-a"],
                "depth_increment": 1,
                "gb_reference": "gb-ref-ib-002-e1",
            },
        }
    )
    snap = state.snapshot()
    ib = snap["active_ibs"][0]
    _assert(ib["depth_state"] == 1, "depth state not updated")
    _assert("h2" in ib["hypotheses"], "hypothesis delta missing")
    _assert(len(ib["tp_log"]) == 2, "TP log should include create and evolve tags")
    return ScenarioResult(
        name="deterministic_evolution_tp_tagging",
        status="PASS",
        requirement_key="evolution_tp",
        detail="Deterministic inquiry evolution updates bounded state and appends TP-visible lifecycle tags at safe boundary.",
        io_fields="ib_id, hypothesis_delta, evidence_request_delta, depth_increment -> hypotheses, pending_evidence_requests, tp_log",
    )


def scenario_split_merge_lifecycle() -> ScenarioResult:
    _emit_requirement("split_merge")
    state = _seed_state()
    _create_approved_ib(state, 1, "ib-003", "snap-c")
    state.apply_event(
        {
            "event_type": "split",
            "sequence": 3,
            "safe_boundary": True,
            "payload": {"ib_id": "ib-003", "child_suffixes": ["x2", "x1"], "gb_reference": "gb-ref-split"},
        }
    )
    state.apply_event(
        {
            "event_type": "merge",
            "sequence": 4,
            "safe_boundary": True,
            "payload": {
                "source_ib_ids": ["ib-003:x2", "ib-003:x1"],
                "merged_ib_id": "ib-003-merged",
                "gb_reference": "gb-ref-merge",
            },
        }
    )
    snap = state.snapshot()
    active_ids = [ib["ib_id"] for ib in snap["active_ibs"]]
    retired_ids = [ib["ib_id"] for ib in snap["retired_ibs"]]
    _assert("ib-003-merged" in active_ids, "merged IB missing")
    _assert("ib-003:x1" in retired_ids and "ib-003:x2" in retired_ids, "merge sources should retire")
    return ScenarioResult(
        name="split_merge_lifecycle",
        status="PASS",
        requirement_key="split_merge",
        detail="Deterministic split and merge lifecycle transitions preserve auditable lineage under GB control.",
        io_fields="ib_id, child_suffixes, source_ib_ids, merged_ib_id -> active_ibs, retired_ibs, branch_state",
    )


def scenario_promote_and_retire() -> ScenarioResult:
    _emit_requirement("promote_retire")
    state = _seed_state()
    _create_approved_ib(state, 1, "ib-004", "snap-d")
    state.apply_event(
        {
            "event_type": "promote",
            "sequence": 3,
            "safe_boundary": True,
            "payload": {"ib_id": "ib-004", "gb_reference": "gb-ref-promote", "oub_output_id": "oub-001"},
        }
    )
    state.apply_event(
        {
            "event_type": "retire",
            "sequence": 4,
            "safe_boundary": True,
            "payload": {"ib_id": "ib-004", "gb_reference": "gb-ref-retire"},
        }
    )
    snap = state.snapshot()
    _assert(len(snap["promoted_outputs"]) == 1, "promotion output missing")
    _assert(any(ib["ib_id"] == "ib-004" for ib in snap["retired_ibs"]), "retired IB missing")
    return ScenarioResult(
        name="promote_and_retire",
        status="PASS",
        requirement_key="promote_retire",
        detail="Promotion and retirement remain GB-mediated, safe-boundary applied, and audit-visible without direct OB mutation.",
        io_fields="ib_id, oub_output_id, gb_reference -> promoted_outputs, retired_ibs",
    )


def scenario_negative_direct_oub_bypass() -> ScenarioResult:
    _emit_requirement("direct_bypass")
    state = _seed_state()
    try:
        state.apply_event(
            {
                "event_type": "request_create",
                "sequence": 1,
                "safe_boundary": False,
                "payload": {
                    "snapshot_id": "snap-x",
                    "triggering_ob_ids": ["ob-x"],
                    "request_reason": "bypass",
                    "source_channel": "oub_direct",
                },
            }
        )
    except IBDeterministicReject as exc:
        _assert(exc.reason_code == "IB_RSN_006_DIRECT_OUB_BYPASS", "unexpected reason code")
        return ScenarioResult(
            name="negative_direct_oub_bypass",
            status="PASS",
            requirement_key="direct_bypass",
            detail="Direct OuB routing bypass is deterministically rejected.",
            io_fields="source_channel -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected direct OuB bypass reject")


def scenario_negative_safe_boundary_violation() -> ScenarioResult:
    _emit_requirement("safe_boundary")
    state = _seed_state()
    _create_approved_ib(state, 1, "ib-005", "snap-e")
    try:
        state.apply_event(
            {
                "event_type": "evolve",
                "sequence": 3,
                "safe_boundary": False,
                "payload": {
                    "ib_id": "ib-005",
                    "hypothesis_delta": ["h-next"],
                    "evidence_request_delta": [],
                    "partial_interpretations": [],
                    "depth_increment": 1,
                    "gb_reference": "gb-ref-bad",
                },
            }
        )
    except IBDeterministicReject as exc:
        _assert(exc.reason_code == "IB_RSN_003_SAFE_BOUNDARY_REQUIRED", "unexpected reason code")
        return ScenarioResult(
            name="negative_safe_boundary_violation",
            status="PASS",
            requirement_key="safe_boundary",
            detail="IB evolution outside a deterministic safe boundary was rejected.",
            io_fields="safe_boundary, event_type -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected safe-boundary reject")


def scenario_negative_sequence_violation() -> ScenarioResult:
    _emit_requirement("sequence_violation")
    state = _seed_state()
    state.apply_event(
        {
            "event_type": "request_create",
            "sequence": 1,
            "safe_boundary": False,
            "payload": {
                "snapshot_id": "snap-f",
                "triggering_ob_ids": ["ob-y"],
                "request_reason": "ambiguity_detected",
                "source_channel": "ob_ib",
            },
        }
    )
    try:
        state.apply_event(
            {
                "event_type": "gb_decision",
                "sequence": 3,
                "safe_boundary": True,
                "payload": {"request_id": state.snapshot()["pending_requests"][0]["request_id"], "decision": "deny"},
            }
        )
    except IBDeterministicReject as exc:
        _assert(exc.reason_code == "IB_RSN_002_SEQUENCE_VIOLATION", "unexpected reason code")
        return ScenarioResult(
            name="negative_sequence_violation",
            status="PASS",
            requirement_key="sequence_violation",
            detail="Out-of-order IB lifecycle transition was rejected with deterministic reason code.",
            io_fields="sequence -> reject reason_code",
            negative_path="YES",
        )
    raise AssertionError("Expected sequence violation reject")


def scenario_w3_iiinb_repair_escalation_distinction() -> ScenarioResult:
    _emit_requirement("w3_iiinb_ib_distinction")
    state = _seed_state()
    # Simulate IIInB repair escalation attempt that must not bypass to OUB; must go through proper channel
    # The prototype enforces source_channel == "ob_ib" for creation (distinguishes from direct/repair bypass paths)
    try:
        state.apply_event(
            {
                "event_type": "request_create",
                "sequence": 1,
                "safe_boundary": False,
                "payload": {
                    "snapshot_id": "snap-iiinb",
                    "triggering_ob_ids": ["ob-repair-1"],
                    "request_reason": "iiinb_repair_escalation",
                    "source_channel": "oub_direct",  # invalid for escalation/repair path
                },
            }
        )
    except IBDeterministicReject as exc:
        _assert(exc.reason_code == "IB_RSN_006_DIRECT_OUB_BYPASS", "unexpected reason code for IIInB escalation")
        return ScenarioResult(
            name="w3_iiinb_repair_escalation_distinction",
            status="PASS",
            requirement_key="w3_iiinb_ib_distinction",
            detail="IIInB repair escalation path is distinguished from direct OUB; bypass rejected (no direct OUB for repair).",
            io_fields="source_channel (must be ob_ib for creation) -> reject",
            negative_path="YES",
        )
    raise AssertionError("Expected OUB bypass reject for IIInB escalation")


def scenario_w3_imr_correction_to_a_pipeline() -> ScenarioResult:
    _emit_requirement("w3_imr_pipeline_a_only")
    state = _seed_state()
    _create_approved_ib(state, 1, "ib-imr", "snap-imr")
    # IMR Type A/B correction triggers should route into Pipeline A (via promote to OUB-ready, not direct B mutation)
    # Here we exercise the promote path which is the A-side handoff
    state.apply_event(
        {
            "event_type": "promote",
            "sequence": 3,
            "safe_boundary": True,
            "payload": {"ib_id": "ib-imr", "gb_reference": "gb-ref-imr", "oub_output_id": "oub-imr-a"},
        }
    )
    snap = state.snapshot()
    _assert(len(snap["promoted_outputs"]) == 1, "IMR correction did not produce A-pipeline output")
    _assert(snap["promoted_outputs"][0]["oub_output_id"] == "oub-imr-a", "IMR output mismatch")
    return ScenarioResult(
        name="w3_imr_correction_to_a_pipeline",
        status="PASS",
        requirement_key="w3_imr_pipeline_a_only",
        detail="IMR correction routes through IB promote to OUB-ready (Pipeline A only, no direct B mutation).",
        io_fields="promote payload -> promoted_outputs (A-side handoff)",
    )


def scenario_w3_iiinb_cil_cross_evidence() -> ScenarioResult:
    _emit_requirement("w3_iiinb_cil_cross")
    state = _seed_state()
    # Cross-evidence simulation: IIInB unknown-token escalation leads to CIL path (via IB request with appropriate reason)
    # We use evolve with pending_evidence_requests that would trigger CIL upstream; IB accepts and tags
    _create_approved_ib(state, 1, "ib-cil", "snap-cil")
    state.apply_event(
        {
            "event_type": "evolve",
            "sequence": 3,
            "safe_boundary": True,
            "payload": {
                "ib_id": "ib-cil",
                "hypothesis_delta": [],
                "evidence_request_delta": ["cil_unknown_token"],
                "partial_interpretations": [],
                "depth_increment": 0,
                "gb_reference": "gb-ref-cil",
            },
        }
    )
    snap = state.snapshot()
    ib = snap["active_ibs"][0]
    _assert("cil_unknown_token" in ib["pending_evidence_requests"], "CIL cross-evidence request not recorded in IB")
    return ScenarioResult(
        name="w3_iiinb_cil_cross_evidence",
        status="PASS",
        requirement_key="w3_iiinb_cil_cross",
        detail="IIInB escalation cross-evidence (unknown token) is accepted into IB pending_evidence_requests for CIL path.",
        io_fields="evidence_request_delta (cil_*) -> pending_evidence_requests",
    )


def _build_report() -> dict[str, object]:
    try:
        create_result, create_snapshot = scenario_async_creation_approval()
        evolve_result = scenario_deterministic_evolution_tp_tagging()
        split_merge_result = scenario_split_merge_lifecycle()
        promote_result = scenario_promote_and_retire()
        neg_bypass = scenario_negative_direct_oub_bypass()
        neg_safe = scenario_negative_safe_boundary_violation()
        neg_seq = scenario_negative_sequence_violation()
        w3_iiinb = scenario_w3_iiinb_repair_escalation_distinction()
        w3_imr = scenario_w3_imr_correction_to_a_pipeline()
        w3_cil = scenario_w3_iiinb_cil_cross_evidence()

        scenarios = [
            create_result.as_dict(),
            evolve_result.as_dict(),
            split_merge_result.as_dict(),
            promote_result.as_dict(),
            neg_bypass.as_dict(),
            neg_safe.as_dict(),
            neg_seq.as_dict(),
            w3_iiinb.as_dict(),
            w3_imr.as_dict(),
            w3_cil.as_dict(),
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
                "thought_simulator/20_requirements/20.90_ib_requirements.md",
                "thought_simulator/20_requirements/20.30_ts_functional_model.md",
                "thought_simulator/20_requirements/20.80_gb_requirements.md",
                "thought_simulator/20_requirements/20.150_tcu_budgeting_requirements.md",
                "thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md",
                "thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md",
            ],
            "scenarios": scenarios,
            "determinism_evidence": {
                "creation_digest": create_snapshot["verification_digest"],
                "active_ids_after_creation": [ib["ib_id"] for ib in create_snapshot["active_ibs"]],
                "pending_requests_after_creation": len(create_snapshot["pending_requests"]),
            },
            "state_snapshots": {"creation_snapshot": create_snapshot},
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


if __name__ == '__main__':
    raise SystemExit(main())
