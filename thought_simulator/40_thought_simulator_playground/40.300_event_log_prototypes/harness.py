"""Verification harness for event log prototype."""

from __future__ import annotations

from pathlib import Path
import json

from prototype import EventLog


ARTIFACT_NAME = "event_log_verification_run_2026-05-28.json"


def _build_events() -> list[dict[str, object]]:
    return [
        {"sequence": 0, "tick": 0, "event_type": "created", "payload": {"tp_id": "tp-1"}},
        {"sequence": 1, "tick": 1, "event_type": "moved", "payload": {"basin": "B1"}},
    ]


def _positive_replay() -> dict[str, object]:
    events = _build_events()
    a = EventLog()
    b = EventLog()
    last_a = {}
    last_b = {}
    for event in events:
        last_a = a.append(event)
        last_b = b.append(event)
    return {
        "scenario": "positive_deterministic_replay",
        "result": "PASS" if last_a.get("verification_digest") == last_b.get("verification_digest") else "FAIL",
        "digest": last_a.get("verification_digest"),
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
    log = EventLog()
    scenarios = [
        _positive_replay(),
        _expect_value_error(
            "negative_out_of_order_sequence",
            lambda: [log.append({"sequence": 1, "tick": 0, "event_type": "created", "payload": {}})],
        ),
        _expect_value_error(
            "negative_missing_field",
            lambda: EventLog().append({"sequence": 0, "tick": 0, "event_type": "created"}),
        ),
    ]
    status = "PASS" if all(item["result"] == "PASS" for item in scenarios) else "FAIL"
    report = {
        "module": "40.2600_event_log_prototypes",
        "date": "2026-05-28",
        "status": status,
        "scenarios": scenarios,
    }
    artifact_path = _write_artifact(report)
    print(f"event-log harness status: {status}")
    print(f"artifact: {artifact_path}")


if __name__ == "__main__":
    main()
