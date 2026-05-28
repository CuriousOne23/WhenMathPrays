"""Verification harness for regulator prototype."""

from __future__ import annotations

from pathlib import Path
import json

from prototype import evaluate_regulator


ARTIFACT_NAME = "regulator_verification_run_2026-05-28.json"


def _positive_deterministic_replay() -> dict[str, object]:
    contract = {"policy": "clamp", "pressure": 3.0, "max_delta": 2.0}
    first = evaluate_regulator(contract).to_dict()
    second = evaluate_regulator(contract).to_dict()
    return {
        "scenario": "positive_deterministic_replay",
        "result": "PASS" if first == second else "FAIL",
        "first": first,
        "second": second,
    }


def _positive_policy_comparison() -> dict[str, object]:
    clamp = evaluate_regulator({"policy": "clamp", "pressure": 2.0, "max_delta": 2.0}).to_dict()
    atten = evaluate_regulator({"policy": "attenuate", "pressure": 2.0, "max_delta": 2.0}).to_dict()
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


def _write_artifact(report: dict[str, object]) -> Path:
    artifact_dir = Path(__file__).resolve().parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = artifact_dir / ARTIFACT_NAME
    artifact_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return artifact_path


def main() -> None:
    scenarios = [
        _positive_deterministic_replay(),
        _positive_policy_comparison(),
        _expect_value_error("negative_invalid_policy", {"policy": "unknown", "pressure": 1.0, "max_delta": 1.0}),
        _expect_value_error("negative_negative_pressure", {"policy": "clamp", "pressure": -1.0, "max_delta": 1.0}),
    ]
    status = "PASS" if all(item["result"] == "PASS" for item in scenarios) else "FAIL"
    report = {
        "module": "40.50_regulator_prototypes",
        "date": "2026-05-28",
        "status": status,
        "scenarios": scenarios,
    }
    artifact_path = _write_artifact(report)
    print(f"regulator harness status: {status}")
    print(f"artifact: {artifact_path}")


if __name__ == "__main__":
    main()
