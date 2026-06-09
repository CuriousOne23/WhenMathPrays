"""Verification harness for regulator prototype."""

from __future__ import annotations

from pathlib import Path
import json

from prototype import evaluate_regulator, Regulator, SUPPORTED_POLICIES


ARTIFACT_NAME = "regulator_verification_run_2026-06-06.json"


def _positive_deterministic_replay() -> dict[str, object]:
    contract = {"policy": "clamp", "enforcement_area": "delta_h", "pressure": 3.0, "max_delta": 2.0}
    first = evaluate_regulator(contract).to_dict()
    second = evaluate_regulator(contract).to_dict()
    return {
        "scenario": "positive_deterministic_replay",
        "result": "PASS" if first == second else "FAIL",
        "first": first,
        "second": second,
    }


def _positive_policy_comparison() -> dict[str, object]:
    clamp = evaluate_regulator({"policy": "clamp", "enforcement_area": "delta_h", "pressure": 2.0, "max_delta": 2.0}).to_dict()
    atten = evaluate_regulator({"policy": "attenuate", "enforcement_area": "delta_h", "pressure": 2.0, "max_delta": 2.0}).to_dict()
    return {
        "scenario": "positive_policy_comparison",
        "result": "PASS" if clamp["applied_delta"] > atten["applied_delta"] else "FAIL",
        "clamp": clamp,
        "attenuate": atten,
    }


def _expect_value_error(name: str, contract: dict[str, object]) -> dict[str, object]:
    try:
        evaluate_regulator(contract)
    except ValueError as exc:
        return {"scenario": name, "result": "PASS", "error": str(exc)}
    return {"scenario": name, "result": "FAIL", "error": "ValueError not raised"}


def _delta_h_enforcement() -> dict[str, object]:
    d = evaluate_regulator({"policy": "clamp", "enforcement_area": "delta_h", "pressure": 0.9, "max_delta": 0.5}).to_dict()
    ok = d["enforcement_area"] == "delta_h" and d["interrupt_level"] in ("L1", "none") and "delta_h" in str(d["rationale"])
    return {"scenario": "delta_h_enforcement", "result": "PASS" if ok else "FAIL", "decision": d}


def _fan_out_enforcement() -> dict[str, object]:
    d = evaluate_regulator({"policy": "clamp", "enforcement_area": "fan_out", "pressure": 10, "max_delta": 4}).to_dict()
    ok = d["enforcement_area"] == "fan_out" and d.get("interrupt_level") == "L2"
    return {"scenario": "fan_out_enforcement", "result": "PASS" if ok else "FAIL", "decision": d}


def _operator_cost_enforcement() -> dict[str, object]:
    d = evaluate_regulator({"policy": "attenuate", "enforcement_area": "operator_cost", "pressure": 150, "max_delta": 100}).to_dict()
    ok = d["enforcement_area"] == "operator_cost" and d.get("interrupt_level") == "L2"
    return {"scenario": "operator_cost_enforcement", "result": "PASS" if ok else "FAIL", "decision": d}


def _overflow_enforcement() -> dict[str, object]:
    d = evaluate_regulator({"policy": "clamp", "enforcement_area": "overflow", "pressure": 0.8, "max_delta": 0.3}).to_dict()
    ok = d["enforcement_area"] == "overflow" and d.get("interrupt_level") == "L1"
    return {"scenario": "overflow_enforcement", "result": "PASS" if ok else "FAIL", "decision": d}


def _memory_bound_enforcement() -> dict[str, object]:
    d = evaluate_regulator({"policy": "attenuate", "enforcement_area": "memory", "pressure": 0.9, "max_delta": 0.4}).to_dict()
    ok = d["enforcement_area"] == "memory" and d.get("interrupt_level") == "L1"
    return {"scenario": "memory_bound_enforcement", "result": "PASS" if ok else "FAIL", "decision": d}


def _cycle_time_enforcement() -> dict[str, object]:
    d = evaluate_regulator({"policy": "clamp", "enforcement_area": "cycle_time", "pressure": 60, "max_delta": 30}).to_dict()
    ok = d["enforcement_area"] == "cycle_time" and d.get("interrupt_level") == "L2"
    return {"scenario": "cycle_time_enforcement", "result": "PASS" if ok else "FAIL", "decision": d}


def _interrupt_generation() -> dict[str, object]:
    d = evaluate_regulator({"policy": "clamp", "enforcement_area": "delta_h", "pressure": 1.0, "max_delta": 0.1}).to_dict()
    ok = d.get("interrupt_level") == "L1"
    return {"scenario": "interrupt_generation", "result": "PASS" if ok else "FAIL", "decision": d}


def _rich_observability() -> dict[str, object]:
    d = evaluate_regulator({"policy": "stabilize", "enforcement_area": "fan_out", "pressure": 8, "max_delta": 3}).to_dict()
    obs = d.get("obs", {})
    ok = "enforcements" in obs and "interrupt_level" in d and "policy_signature" in obs
    return {"scenario": "rich_observability", "result": "PASS" if ok else "FAIL", "decision": d}


def _explicit_auditable_decision() -> dict[str, object]:
    d = evaluate_regulator({"policy": "clamp", "enforcement_area": "delta_h", "pressure": 0.7, "max_delta": 0.4}).to_dict()
    ok = "action" in d and "rationale" in d and "applied_delta" in d and "enforcement_area" in d and "boundary_marker" in d.get("obs", {})
    return {"scenario": "explicit_auditable_decision", "result": "PASS" if ok else "FAIL", "decision": d}


def _bounded_internal_state() -> dict[str, object]:
    reg = Regulator(max_history=4)
    for i in range(10):
        reg.evaluate({"policy": "clamp", "enforcement_area": "delta_h", "pressure": 0.5, "max_delta": 0.3, "tick": i})
    ok = reg.get_history_len() == 4
    return {"scenario": "bounded_internal_state", "result": "PASS" if ok else "FAIL", "history_len": reg.get_history_len()}


def _full_deterministic_mode() -> dict[str, object]:
    # Always deterministic in this prototype
    c = {"policy": "attenuate", "enforcement_area": "overflow", "pressure": 0.6, "max_delta": 0.2}
    d1 = evaluate_regulator(c).to_dict()
    d2 = evaluate_regulator(c).to_dict()
    ok = d1 == d2 and d1["verification_digest"] == d2["verification_digest"]
    return {"scenario": "full_deterministic_mode", "result": "PASS" if ok else "FAIL"}


def _write_artifact(report: dict[str, object]) -> Path:
    artifact_dir = Path(__file__).resolve().parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = artifact_dir / ARTIFACT_NAME
    artifact_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return artifact_path


def main() -> None:
    scenarios = [
        _positive_deterministic_replay(),
        _positive_policy_comparison(),
        _delta_h_enforcement(),
        _fan_out_enforcement(),
        _operator_cost_enforcement(),
        _overflow_enforcement(),
        _memory_bound_enforcement(),
        _cycle_time_enforcement(),
        _interrupt_generation(),
        _rich_observability(),
        _explicit_auditable_decision(),
        _bounded_internal_state(),
        _full_deterministic_mode(),
        _expect_value_error("negative_invalid_policy", {"policy": "unknown", "enforcement_area": "delta_h", "pressure": 1.0, "max_delta": 1.0}),
        _expect_value_error("negative_negative_pressure", {"policy": "clamp", "enforcement_area": "delta_h", "pressure": -1.0, "max_delta": 1.0}),
    ]
    passed = sum(1 for s in scenarios if s["result"] == "PASS")
    status = "PASS" if passed == len(scenarios) else "FAIL"
    report = {
        "module": "40.320_regulator_prototypes",
        "run_command": "python harness.py",
        "run_timestamp_utc": "2026-06-06",
        "summary": {
            "total_scenarios": len(scenarios),
            "passed": passed,
            "failed": len(scenarios) - passed,
            "overall_status": status,
        },
        "requirements_anchors": [
            "20.150_tcu_budgeting_requirements.md",
            "20.170_safety_requirements.md",
            "20.200_traceability_matrix.md",
            "20.30_ts_functional_model.md",
            "20.40_ob_requirements.md",
            "20.90_ib_requirements.md",
            "20.90_ts_parameter_table.md",
            "10.10.40_scheduler_and_regulator_architecture.md",
            "10.50.50_regulator_requirements.md",
        ],
        "scenarios": scenarios,
    }
    artifact_path = _write_artifact(report)
    print(f"Module: 40.320_regulator_prototypes")
    print(f"Artifact: {artifact_path}")
    for s in scenarios:
        print(f"{s['scenario']}: {s['result']}")
    print(f"Overall: {status}")


if __name__ == "__main__":
    main()
