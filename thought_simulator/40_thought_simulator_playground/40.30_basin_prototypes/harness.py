"""Verification harness for 40.30_basin_prototypes."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from prototype import BasinPrototype


MODULE_NAME = "40.30_basin_prototypes"
RUN_COMMAND = "python harness.py"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACT_PATH = ARTIFACT_DIR / "basin_verification_run_2026-05-27.json"


def _base_contract() -> dict[str, Any]:
	return {
		"basin_id": "basin.alpha",
		"tp_id": "tp.alpha",
		"state_counter": 0,
		"deterministic_mode": True,
		"entropy_vector": [0.40, 0.60],
		"provenance_ids": ["seed"],
		"tags": ["seeded"],
		"metadata": {"source": "harness"},
		"tick": 0,
	}


def _positive_deterministic_replay() -> dict[str, Any]:
	sequence = [
		{"event_type": "provenance_add", "tick": 1, "provenance_id": "prov.alpha", "note": "first provenance"},
		{"event_type": "transition", "tick": 2, "target_basin_id": "basin.beta", "provenance_id": "prov.alpha", "note": "move basin"},
		{"event_type": "entropy_update", "tick": 3, "entropy_vector": [0.25, 0.75], "provenance_id": "prov.alpha", "note": "rebalance entropy"},
	]

	first = BasinPrototype.from_contract(_base_contract())
	for event in sequence:
		first.apply_contract(event)
	first_snapshot = first.snapshot()

	second = BasinPrototype.from_contract(_base_contract())
	for event in sequence:
		second.apply_contract(event)
	second_snapshot = second.snapshot()

	if first_snapshot != second_snapshot:
		raise AssertionError("Deterministic replay produced different snapshots")

	return {
		"name": "positive_deterministic_replay",
		"status": "PASS",
		"io_fields": ["basin_id", "tp_id", "state_counter", "deterministic_mode", "entropy_vector", "provenance_ids", "history", "verification_digest"],
		"snapshot": first_snapshot,
		"evidence_digest": first_snapshot["verification_digest"],
	}


def _negative_empty_basin_id() -> dict[str, Any]:
	contract = _base_contract()
	contract["basin_id"] = ""
	try:
		BasinPrototype.from_contract(contract)
	except ValueError as exc:
		return {
			"name": "negative_empty_basin_id",
			"status": "PASS",
			"error": str(exc),
			"io_fields": ["basin_id"],
		}
	raise AssertionError("Empty basin_id should have failed")


def _negative_duplicate_provenance() -> dict[str, Any]:
	basin = BasinPrototype.from_contract(_base_contract())
	try:
		basin.apply_contract({"event_type": "provenance_add", "tick": 1, "provenance_id": "seed", "note": "duplicate provenance"})
	except ValueError as exc:
		return {
			"name": "negative_duplicate_provenance",
			"status": "PASS",
			"error": str(exc),
			"io_fields": ["provenance_ids", "event_type", "provenance_id"],
		}
	raise AssertionError("Duplicate provenance_id should have failed")


def _negative_entropy_length_mismatch() -> dict[str, Any]:
	basin = BasinPrototype.from_contract(_base_contract())
	try:
		basin.apply_contract({"event_type": "entropy_update", "tick": 1, "entropy_vector": [0.1, 0.2, 0.7], "provenance_id": "prov.alpha", "note": "length mismatch"})
	except ValueError as exc:
		return {
			"name": "negative_entropy_length_mismatch",
			"status": "PASS",
			"error": str(exc),
			"io_fields": ["entropy_vector", "event_type"],
		}
	raise AssertionError("Mismatched entropy_vector length should have failed")


def _build_report() -> dict[str, Any]:
	scenarios = [
		_positive_deterministic_replay(),
		_negative_empty_basin_id(),
		_negative_duplicate_provenance(),
		_negative_entropy_length_mismatch(),
	]
	passed = sum(1 for scenario in scenarios if scenario["status"] == "PASS")
	failed = len(scenarios) - passed
	artifact = {
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
			"20.30_tp_requirements.md",
			"20.50_observability_requirements.md",
			"20.60_testing_and_validation.md",
			"20.90_interfaces_and_io.md",
			"20.120_stability_requirements.md",
			"20.140_program_flow.md",
			"20.150_glossary.md",
			"20.160_traceability_matrix.md",
		],
		"scenarios": scenarios,
	}
	return artifact


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