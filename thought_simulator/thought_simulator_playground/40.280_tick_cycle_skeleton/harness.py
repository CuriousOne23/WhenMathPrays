"""Verification harness for tick-cycle skeleton prototype."""

from __future__ import annotations

from pathlib import Path
import json

from prototype import CANONICAL_PHASES, TickCycle


ARTIFACT_NAME = "tick_cycle_verification_run_2026-05-28.json"


def _positive_replay() -> dict[str, object]:
    run_a = TickCycle()
    out_a = [run_a.execute_tick({"tick": i, "phases": list(CANONICAL_PHASES)}) for i in range(3)]

    run_b = TickCycle()
    out_b = [run_b.execute_tick({"tick": i, "phases": list(CANONICAL_PHASES)}) for i in range(3)]

    return {
        "scenario": "positive_deterministic_replay",
        "result": "PASS" if out_a == out_b else "FAIL",
        "outputs": out_a,
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
    cycle = TickCycle()
    scenarios = [
        _positive_replay(),
        _expect_value_error("negative_non_monotonic_tick", lambda: cycle.execute_tick({"tick": 1, "phases": list(CANONICAL_PHASES)})),
        _expect_value_error("negative_invalid_phase_order", lambda: TickCycle().execute_tick({"tick": 0, "phases": ["process", "schedule", "transition", "log"]})),
    ]
    status = "PASS" if all(item["result"] == "PASS" for item in scenarios) else "FAIL"
    report = {
        "module": "40.280_tick_cycle_skeleton",
        "date": "2026-05-28",
        "status": status,
        "scenarios": scenarios,
    }
    artifact_path = _write_artifact(report)
    print(f"tick-cycle harness status: {status}")
    print(f"artifact: {artifact_path}")


if __name__ == "__main__":
    main()
