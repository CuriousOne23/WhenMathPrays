"""Harness for 40.207 — REPLAY_CLASS_7 C7-A..E per 20.36 §9."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from prototype import run_class_7_suite, strip_b_envelopes, canonical_json_digest

ARTIFACT_NAME = "replay_class7_verification_run_2026-06-08.json"


def _strip_replay_demo() -> dict:
    trace = {
        "semantic_core": {"meaning": "frozen"},
        "exec_plan": {"should_strip": True},
        "exec_trace": {"should_strip": True},
        "input_repair_tags": [{"segment_ref": "seg-001"}],
    }
    stripped = strip_b_envelopes(trace)
    ok = "exec_plan" not in stripped and "exec_trace" not in stripped and "semantic_core" in stripped
    return {"scenario": "strip_replay_invariant", "result": "PASS" if ok else "FAIL", "stripped_digest": canonical_json_digest(stripped)}


def main() -> int:
    class7 = run_class_7_suite()
    strip_demo = _strip_replay_demo()
    status = "PASS" if class7["status"] == "PASS" and strip_demo["result"] == "PASS" else "FAIL"

    report = {
        "module": "40.207_replay_prototypes",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "status": status,
        "class_7": class7,
        "additional_scenarios": [strip_demo],
        "summary": {
            "c7_passed": sum(1 for r in class7["sub_scenarios"].values() if r["pass"]),
            "c7_total": len(class7["sub_scenarios"]),
        },
    }

    artifact_dir = Path(__file__).resolve().parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = artifact_dir / ARTIFACT_NAME
    artifact_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    print(f"Replay harness status: {status}")
    print(f"C7: {report['summary']['c7_passed']}/{report['summary']['c7_total']} PASS")
    print(f"Artifact: {artifact_path}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())