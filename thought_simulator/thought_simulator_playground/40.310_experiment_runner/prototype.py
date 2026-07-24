"""Deterministic experiment runner prototype."""

from __future__ import annotations

import hashlib
import json


def _canonical(payload: dict[str, object]) -> str:
	return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _run_digest(payload: dict[str, object]) -> str:
	return hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()


def _validate_request(request: dict[str, object]) -> None:
	experiment_id = request.get("experiment_id")
	max_ticks = request.get("max_ticks")
	seed = request.get("seed")
	if not isinstance(experiment_id, str) or not experiment_id:
		raise ValueError("experiment_id must be a non-empty string")
	if not isinstance(max_ticks, int) or max_ticks <= 0:
		raise ValueError("max_ticks must be a positive integer")
	if not isinstance(seed, int):
		raise ValueError("seed must be an integer")


def run_experiment(request: dict[str, object]) -> dict[str, object]:
	_validate_request(request)
	run_id = _run_digest(request)[:16]
	return {
		"run_id": run_id,
		"experiment_id": request["experiment_id"],
		"status": "PASS",
		"max_ticks": request["max_ticks"],
		"seed": request["seed"],
		"verification_digest": _run_digest({"run_id": run_id, "request": request}),
	}


def run_batch(requests: list[dict[str, object]]) -> dict[str, object]:
	if not isinstance(requests, list) or not requests:
		raise ValueError("requests must be a non-empty list")
	results = [run_experiment(item) for item in requests]
	return {
		"result_count": len(results),
		"results": results,
		"verification_digest": _run_digest({"results": results}),
	}
