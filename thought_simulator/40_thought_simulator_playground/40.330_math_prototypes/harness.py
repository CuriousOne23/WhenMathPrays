"""Verification harness for deterministic math prototypes."""

from __future__ import annotations

from pathlib import Path
import json

from prototype import euclidean_distance, project_vector


ARTIFACT_NAME = "math_prototype_verification_run_2026-05-28.json"


def _positive_projection_replay() -> dict[str, object]:
    vector = [1.0, 2.0, 3.0]
    matrix = [[1.0, 0.0, 0.0], [0.0, 1.0, 1.0]]
    first = project_vector(vector, matrix)
    second = project_vector(vector, matrix)
    return {
        "scenario": "positive_projection_replay",
        "result": "PASS" if first == second else "FAIL",
        "first": first,
        "second": second,
    }


def _positive_distance_contract() -> dict[str, object]:
    first = euclidean_distance([0.0, 0.0], [3.0, 4.0])
    second = euclidean_distance([0.0, 0.0], [3.0, 4.0])
    return {
        "scenario": "positive_distance_contract",
        "result": "PASS" if first == second and first["distance"] == 5.0 else "FAIL",
        "distance": first,
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
        _positive_projection_replay(),
        _positive_distance_contract(),
        _expect_value_error(
            "negative_dimension_mismatch",
            lambda: project_vector([1.0, 2.0], [[1.0, 0.0, 1.0]]),
        ),
        _expect_value_error(
            "negative_non_finite_input",
            lambda: euclidean_distance([1.0, float("nan")], [1.0, 2.0]),
        ),
    ]
    status = "PASS" if all(item["result"] == "PASS" for item in scenarios) else "FAIL"
    report = {
        "module": "40.1200_math_prototypes",
        "date": "2026-05-28",
        "status": status,
        "scenarios": scenarios,
    }
    artifact_path = _write_artifact(report)
    print(f"math harness status: {status}")
    print(f"artifact: {artifact_path}")


if __name__ == "__main__":
    main()
