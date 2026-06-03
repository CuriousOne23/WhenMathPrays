"""Verification harness for 40.40_scheduler_prototypes."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from prototype import (
    EVENT_SCHEDULE_TICK,
    POLICY_ROUND_ROBIN,
    POLICY_WEIGHTED_ROUND_ROBIN,
    SchedulerPrototype,
)


MODULE_NAME = "40.40_scheduler_prototypes"
RUN_COMMAND = "python harness.py"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACT_PATH = ARTIFACT_DIR / "scheduler_verification_run_2026-05-28.json"


def _base_contract() -> dict[str, Any]:
    return {
        "tick": 0,
        "deterministic_mode": True,
        "policy": POLICY_ROUND_ROBIN,
        "max_active": 1,
        "state_counter": 0,
        "thoughtpoints": [
            {"tp_id": "tp.alpha", "energy": 0.9, "coherence": 0.7},
            {"tp_id": "tp.beta", "energy": 0.6, "coherence": 0.9},
            {"tp_id": "tp.gamma", "energy": 0.4, "coherence": 0.5},
        ],
    }


def _positive_deterministic_replay() -> dict[str, Any]:
    events = [
        {"event_type": EVENT_SCHEDULE_TICK, "tick": 1, "policy": POLICY_ROUND_ROBIN, "max_active": 1},
        {"event_type": EVENT_SCHEDULE_TICK, "tick": 2, "policy": POLICY_ROUND_ROBIN, "max_active": 1},
        {"event_type": EVENT_SCHEDULE_TICK, "tick": 3, "policy": POLICY_WEIGHTED_ROUND_ROBIN, "max_active": 2},
    ]

    first = SchedulerPrototype.from_contract(_base_contract())
    for event in events:
        first.apply_contract(event)
    first_snapshot = first.snapshot()

    second = SchedulerPrototype.from_contract(_base_contract())
    for event in events:
        second.apply_contract(event)
    second_snapshot = second.snapshot()

    if first_snapshot != second_snapshot:
        raise AssertionError("Deterministic replay produced different scheduler snapshots")

    return {
        "name": "positive_deterministic_replay",
        "status": "PASS",
        "io_fields": [
            "tick",
            "policy",
            "max_active",
            "selected_tp_ids",
            "thoughtpoints",
            "history",
            "verification_digest",
        ],
        "snapshot": first_snapshot,
        "evidence_digest": first_snapshot["verification_digest"],
    }


def _positive_round_robin_fairness() -> dict[str, Any]:
    scheduler = SchedulerPrototype.from_contract(_base_contract())
    expected = ["tp.alpha", "tp.beta", "tp.gamma", "tp.alpha"]
    observed: list[str] = []
    for tick in range(1, 5):
        scheduler.apply_contract(
            {
                "event_type": EVENT_SCHEDULE_TICK,
                "tick": tick,
                "policy": POLICY_ROUND_ROBIN,
                "max_active": 1,
            }
        )
        observed.append(scheduler.history[-1].selected_tp_ids[0])

    if observed != expected:
        raise AssertionError(f"Round-robin fairness mismatch: expected {expected}, observed {observed}")

    return {
        "name": "positive_round_robin_fairness",
        "status": "PASS",
        "io_fields": ["tick", "policy", "max_active", "selected_tp_ids", "wait_ticks", "total_selected"],
        "observed": observed,
    }


def _negative_empty_tp_id() -> dict[str, Any]:
    contract = _base_contract()
    contract["thoughtpoints"] = [
        {"tp_id": "", "energy": 0.9, "coherence": 0.7},
        {"tp_id": "tp.beta", "energy": 0.6, "coherence": 0.9},
    ]
    try:
        SchedulerPrototype.from_contract(contract)
    except ValueError as exc:
        return {
            "name": "negative_empty_tp_id",
            "status": "PASS",
            "error": str(exc),
            "io_fields": ["tp_id"],
        }
    raise AssertionError("Empty tp_id should have failed")


def _negative_non_monotonic_tick() -> dict[str, Any]:
    scheduler = SchedulerPrototype.from_contract(_base_contract())
    scheduler.apply_contract({"event_type": EVENT_SCHEDULE_TICK, "tick": 1})
    try:
        scheduler.apply_contract({"event_type": EVENT_SCHEDULE_TICK, "tick": 1})
    except ValueError as exc:
        return {
            "name": "negative_non_monotonic_tick",
            "status": "PASS",
            "error": str(exc),
            "io_fields": ["tick", "event_type"],
        }
    raise AssertionError("Non-monotonic tick should have failed")


def _negative_invalid_policy() -> dict[str, Any]:
    scheduler = SchedulerPrototype.from_contract(_base_contract())
    try:
        scheduler.apply_contract(
            {
                "event_type": EVENT_SCHEDULE_TICK,
                "tick": 1,
                "policy": "lottery",
            }
        )
    except ValueError as exc:
        return {
            "name": "negative_invalid_policy",
            "status": "PASS",
            "error": str(exc),
            "io_fields": ["policy"],
        }
    raise AssertionError("Invalid policy should have failed")


def _build_report() -> dict[str, Any]:
    scenarios = [
        _positive_deterministic_replay(),
        _positive_round_robin_fairness(),
        _negative_empty_tp_id(),
        _negative_non_monotonic_tick(),
        _negative_invalid_policy(),
    ]
    passed = sum(1 for scenario in scenarios if scenario["status"] == "PASS")
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
            "20.30_ts_functional_model.md",
            "20.150_tcu_budgeting_requirements.md",
            "20.170_safety_requirements.md",
            "20.200_traceability_matrix.md",
            "20.40_ob_requirements.md",
            "20.90_ib_requirements.md",
        ],
        "scenarios": scenarios,
    }


def _write_artifact(report: dict[str, Any]) -> Path:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return ARTIFACT_PATH


def main() -> int:
    report = _build_report()
    artifact_path = _write_artifact(report)
    print(f"Module: {MODULE_NAME}")
    print(f"Command: {RUN_COMMAND}")
    print(f"Artifact: {artifact_path}")
    for scenario in report["scenarios"]:
        print(f"{scenario['name']}: {scenario['status']}")
    print(f"Overall: {report['summary']['overall_status']}")
    return 0 if report["summary"]["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
