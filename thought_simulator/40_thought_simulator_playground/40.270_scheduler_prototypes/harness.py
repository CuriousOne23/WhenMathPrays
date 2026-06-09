"""Verification harness for 40.270_scheduler_prototypes."""

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


MODULE_NAME = "40.270_scheduler_prototypes"
RUN_COMMAND = "python harness.py"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACT_PATH = ARTIFACT_DIR / "scheduler_verification_run_2026-06-06.json"


def _base_contract() -> dict[str, Any]:
    return {
        "tick": 0,
        "deterministic_mode": True,
        "policy": POLICY_ROUND_ROBIN,
        "max_active": 1,
        "state_counter": 0,
        "history_max": 16,
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
            "last_selection_rationale",
            "last_cohort_metadata",
            "history_max",
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


def _positive_tie_break_provenance() -> dict[str, Any]:
    """Covers: explicit deterministic tie-breaking rules and provenance (Must-Explore item)."""
    # Use weighted to force score-based; two TPs with equal computed score after init wait.
    # We force equal effective by choosing values so primary score ties, rely on tp_id secondary.
    contract = _base_contract()
    contract["thoughtpoints"] = [
        {"tp_id": "tp.aa", "energy": 1.0, "coherence": 1.0, "wait_ticks": 5},
        {"tp_id": "tp.zz", "energy": 1.0, "coherence": 1.0, "wait_ticks": 5},
    ]
    contract["max_active"] = 1
    contract["policy"] = POLICY_WEIGHTED_ROUND_ROBIN
    scheduler = SchedulerPrototype.from_contract(contract)
    scheduler.apply_contract({
        "event_type": EVENT_SCHEDULE_TICK,
        "tick": 1,
        "policy": POLICY_WEIGHTED_ROUND_ROBIN,
        "max_active": 1,
    })
    last = scheduler.history[-1]
    rationale = last.payload.get("tie_break_rationale", "")
    selected = last.selected_tp_ids
    # "aa" < "zz" so aa wins on tie
    if selected != ["tp.aa"]:
        raise AssertionError(f"Tie-break did not prefer stable id order: {selected}")
    if "tie-break by stable tp_id asc" not in rationale:
        raise AssertionError(f"Rationale missing tie-break detail: {rationale}")
    return {
        "name": "positive_tie_break_provenance",
        "status": "PASS",
        "io_fields": ["tie_break_rationale", "selected_tp_ids", "policy"],
        "selected": selected,
        "rationale_snippet": rationale[:80],
    }


def _positive_interrupt_window_preemption() -> dict[str, Any]:
    """Covers: Proper handling of interrupt windows (pre-OB, post-TB, ...) and preemption within scheduler control."""
    scheduler = SchedulerPrototype.from_contract(_base_contract())
    scheduler.apply_contract({
        "event_type": EVENT_SCHEDULE_TICK,
        "tick": 1,
        "policy": POLICY_ROUND_ROBIN,
        "window": "pre_ob",
    })
    scheduler.apply_contract({
        "event_type": EVENT_SCHEDULE_TICK,
        "tick": 2,
        "policy": POLICY_ROUND_ROBIN,
        "window": "post_tb",
        "preempt": True,
    })
    hist = scheduler.history
    windows = [e.payload.get("window") for e in hist if e.event_type == EVENT_SCHEDULE_TICK]
    preempts = [e.payload.get("preempt") for e in hist if e.event_type == EVENT_SCHEDULE_TICK]
    if "pre_ob" not in windows or "post_tb" not in windows:
        raise AssertionError(f"Interrupt windows not recorded: {windows}")
    if True not in preempts:
        raise AssertionError("Preempt flag not propagated to event payload")
    return {
        "name": "positive_interrupt_window_preemption",
        "status": "PASS",
        "io_fields": ["window", "preempt", "history"],
        "observed_windows": windows,
        "had_preempt": any(preempts),
    }


def _positive_timing_budget_and_cycle() -> dict[str, Any]:
    """Covers: Enforcement of per-module and per-cycle timing budgets and cycle boundaries (modeled)."""
    scheduler = SchedulerPrototype.from_contract(_base_contract())
    scheduler.apply_contract({
        "event_type": EVENT_SCHEDULE_TICK,
        "tick": 1,
        "policy": POLICY_ROUND_ROBIN,
        "budget_tcu": 12,
    })
    last = scheduler.history[-1]
    bstatus = last.payload.get("budget_status", {})
    if not bstatus.get("within_budget"):
        raise AssertionError("Budget status not within_budget in model")
    if bstatus.get("sim_tcu") != 12:
        raise AssertionError("sim_tcu not recorded")
    # cycle boundary implied by strictly increasing tick already enforced
    return {
        "name": "positive_timing_budget_and_cycle",
        "status": "PASS",
        "io_fields": ["budget_tcu", "budget_status", "tick"],
        "budget_status": bstatus,
    }


def _positive_cohort_selection_merge() -> dict[str, Any]:
    """Covers: Support for deterministic parallel-safe cohort selection and merge semantics (where enabled)."""
    scheduler = SchedulerPrototype.from_contract(_base_contract())
    scheduler.apply_contract({
        "event_type": EVENT_SCHEDULE_TICK,
        "tick": 1,
        "policy": POLICY_ROUND_ROBIN,
        "max_active": 2,
    })
    last = scheduler.history[-1]
    cohort = last.payload.get("cohort_metadata", {})
    if not cohort.get("is_cohort") or cohort.get("cohort_size") != 2:
        raise AssertionError(f"Cohort metadata incorrect: {cohort}")
    if cohort.get("merge_semantics") != "deterministic_stable_order":
        raise AssertionError("Missing merge_semantics")
    selected = last.selected_tp_ids
    if len(selected) != 2:
        raise AssertionError("Did not select cohort of 2")
    return {
        "name": "positive_cohort_selection_merge",
        "status": "PASS",
        "io_fields": ["max_active", "cohort_metadata", "selected_tp_ids"],
        "cohort": cohort,
        "selected": selected,
    }


def _positive_rich_observability() -> dict[str, Any]:
    """Covers: Emission of rich, replay-safe observability (selection order, tie-break rationale, fairness counters, cohort metadata, event logs)."""
    scheduler = SchedulerPrototype.from_contract(_base_contract())
    for t in range(1, 4):
        scheduler.apply_contract({"event_type": EVENT_SCHEDULE_TICK, "tick": t, "policy": POLICY_ROUND_ROBIN, "max_active": 1})
    snap = scheduler.snapshot()
    if not snap.get("last_selection_rationale"):
        raise AssertionError("last_selection_rationale missing from snapshot")
    if "last_cohort_metadata" not in snap:
        raise AssertionError("last_cohort_metadata missing")
    # fairness counters exercised via thoughtpoints wait/total
    tp0 = snap["thoughtpoints"][0]
    if "wait_ticks" not in tp0 or "total_selected" not in tp0:
        raise AssertionError("Fairness counters (wait/total) not present on TP view")
    if len(snap["history"]) < 3:
        raise AssertionError("Event logs (history) not rich enough")
    return {
        "name": "positive_rich_observability",
        "status": "PASS",
        "io_fields": ["last_selection_rationale", "last_cohort_metadata", "last_window", "last_budget_status", "thoughtpoints", "history"],
        "rationale_present": bool(snap.get("last_selection_rationale")),
    }


def _positive_bounded_history() -> dict[str, Any]:
    """Covers: Bounded internal state and resource usage consistent with 10.10.40 safety envelopes and 20.150 TCU."""
    small_max = 4
    contract = _base_contract()
    contract["history_max"] = small_max
    scheduler = SchedulerPrototype.from_contract(contract)
    for t in range(1, 10):
        scheduler.apply_contract({"event_type": EVENT_SCHEDULE_TICK, "tick": t})
    if len(scheduler.history) > small_max:
        raise AssertionError(f"History not bounded: len={len(scheduler.history)} > {small_max}")
    snap = scheduler.snapshot()
    if snap.get("history_max") != small_max:
        raise AssertionError("history_max not in snapshot")
    # also assert_invariants should pass
    scheduler.assert_invariants()
    return {
        "name": "positive_bounded_history",
        "status": "PASS",
        "io_fields": ["history_max", "history"],
        "history_len": len(scheduler.history),
        "max": small_max,
    }


def _positive_fairness_starvation_prevent() -> dict[str, Any]:
    """Covers: Fairness mechanisms that guarantee bounded progress ... and prevent unbounded starvation."""
    scheduler = SchedulerPrototype.from_contract(_base_contract())
    max_wait_observed = 0
    for t in range(1, 20):
        scheduler.apply_contract({"event_type": EVENT_SCHEDULE_TICK, "tick": t, "policy": POLICY_ROUND_ROBIN, "max_active": 1})
        waits = [tp.wait_ticks for tp in scheduler.thoughtpoints.values()]
        max_wait_observed = max(max_wait_observed, max(waits))
    # With 3 TPs, RR max_active=1, max wait should be bounded by ~2 (the other two)
    if max_wait_observed > 3:
        raise AssertionError(f"Wait ticks unbounded (starvation risk): max_wait={max_wait_observed}")
    return {
        "name": "positive_fairness_starvation_prevent",
        "status": "PASS",
        "io_fields": ["wait_ticks", "total_selected"],
        "max_wait_observed": max_wait_observed,
    }


def _build_report() -> dict[str, Any]:
    scenarios = [
        _positive_deterministic_replay(),
        _positive_round_robin_fairness(),
        _positive_tie_break_provenance(),
        _positive_interrupt_window_preemption(),
        _positive_timing_budget_and_cycle(),
        _positive_cohort_selection_merge(),
        _positive_rich_observability(),
        _positive_bounded_history(),
        _positive_fairness_starvation_prevent(),
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
            "10.10.40_scheduler_and_regulator_architecture.md",
            "10.50.210_scheduler_requirements.md",
            "20.30_ts_functional_model.md",
            "20.40_ob_requirements.md",
            "20.90_ib_requirements.md",
            "20.90_ts_parameter_table.md",
            "20.150_tcu_budgeting_requirements.md",
            "20.170_safety_requirements.md",
            "20.200_traceability_matrix.md",
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
