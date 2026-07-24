"""Verification harness for experiment runner prototype."""

from __future__ import annotations

from pathlib import Path
import json

from prototype import run_batch, run_experiment


ARTIFACT_NAME = "experiment_runner_verification_run_2026-05-28.json"


def _base_request() -> dict[str, object]:
    return {"experiment_id": "exp-001", "max_ticks": 5, "seed": 42}


def _positive_deterministic_replay() -> dict[str, object]:
    req = _base_request()
    a = run_experiment(req)
    b = run_experiment(req)
    return {
        "scenario": "positive_deterministic_replay",
        "result": "PASS" if a == b else "FAIL",
        "run": a,
    }


def _positive_batch_run() -> dict[str, object]:
    requests = [_base_request(), {"experiment_id": "exp-002", "max_ticks": 3, "seed": 7}]
    out = run_batch(requests)
    return {
        "scenario": "positive_batch_run",
        "result": "PASS" if out["result_count"] == 2 else "FAIL",
        "batch_digest": out["verification_digest"],
    }


def _expect_value_error(name: str, fn) -> dict[str, object]:
    try:
        fn()
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
        _positive_batch_run(),
        _expect_value_error("negative_invalid_max_ticks", lambda: run_experiment({"experiment_id": "exp-bad", "max_ticks": 0, "seed": 1})),
        _expect_value_error("negative_empty_request_list", lambda: run_batch([])),
    ]
    status = "PASS" if all(item["result"] == "PASS" for item in scenarios) else "FAIL"
    report = {
        "module": "40.310_experiment_runner",
        "date": "2026-05-28",
        "status": status,
        "scenarios": scenarios,
    }
    artifact_path = _write_artifact(report)
    print(f"experiment-runner harness status: {status}")
    print(f"artifact: {artifact_path}")


if __name__ == "__main__":
    main()
