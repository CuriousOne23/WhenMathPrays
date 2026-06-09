"""Verification harness for snapshot prototype."""

from __future__ import annotations

from pathlib import Path
import json

from prototype import dump_snapshot, load_snapshot


ARTIFACT_NAME = "snapshot_verification_run_2026-05-28.json"


def _positive_round_trip() -> dict[str, object]:
    state = {"tp_id": "tp-001", "state_counter": 3, "entropy": {"total": 0.2}}
    snap = dump_snapshot(state)
    loaded = load_snapshot(snap)
    return {
        "scenario": "positive_round_trip",
        "result": "PASS" if loaded["state"] == state else "FAIL",
        "snapshot": snap,
    }


def _positive_deterministic_replay() -> dict[str, object]:
    state = {"tp_id": "tp-001", "state_counter": 3, "entropy": {"total": 0.2}}
    a = dump_snapshot(state)
    b = dump_snapshot(state)
    return {
        "scenario": "positive_deterministic_replay",
        "result": "PASS" if a == b else "FAIL",
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
    sample = dump_snapshot({"x": 1})
    broken = dict(sample)
    broken["digest"] = "bad"

    scenarios = [
        _positive_round_trip(),
        _positive_deterministic_replay(),
        _expect_value_error("negative_corrupt_digest", lambda: load_snapshot(broken)),
        _expect_value_error("negative_schema_mismatch", lambda: load_snapshot(sample, expected_schema="v2")),
    ]
    status = "PASS" if all(item["result"] == "PASS" for item in scenarios) else "FAIL"
    report = {
        "module": "40.520_snapshot_prototypes",
        "date": "2026-05-28",
        "status": status,
        "scenarios": scenarios,
    }
    artifact_path = _write_artifact(report)
    print(f"snapshot harness status: {status}")
    print(f"artifact: {artifact_path}")


if __name__ == "__main__":
    main()
