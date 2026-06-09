"""Deterministic math prototype helpers for projection and distance contracts."""

from __future__ import annotations

import hashlib
import json
import math


def _digest(payload: dict[str, object]) -> str:
	encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
	return hashlib.sha256(encoded).hexdigest()


def _validate_vector(name: str, vector: list[float]) -> None:
	if not isinstance(vector, list) or not vector:
		raise ValueError(f"{name} must be a non-empty list")
	for value in vector:
		if not isinstance(value, (int, float)):
			raise ValueError(f"{name} must contain numeric values")
		if not math.isfinite(float(value)):
			raise ValueError(f"{name} contains non-finite values")


def _validate_matrix(matrix: list[list[float]], width: int) -> None:
	if not isinstance(matrix, list) or not matrix:
		raise ValueError("matrix must be a non-empty list")
	for row in matrix:
		if not isinstance(row, list) or len(row) != width:
			raise ValueError("matrix row width must match vector length")
		for value in row:
			if not isinstance(value, (int, float)):
				raise ValueError("matrix must contain numeric values")
			if not math.isfinite(float(value)):
				raise ValueError("matrix contains non-finite values")


def project_vector(vector: list[float], matrix: list[list[float]], deterministic_mode: bool = True) -> dict[str, object]:
	_validate_vector("vector", vector)
	_validate_matrix(matrix, len(vector))
	if not deterministic_mode:
		raise ValueError("deterministic_mode must be True for this prototype")

	projected = [sum(float(cell) * float(item) for cell, item in zip(row, vector)) for row in matrix]
	norm = math.sqrt(sum(value * value for value in projected))
	body = {
		"projected": projected,
		"norm": norm,
	}
	body["verification_digest"] = _digest(body)
	return body


def euclidean_distance(left: list[float], right: list[float]) -> dict[str, object]:
	_validate_vector("left", left)
	_validate_vector("right", right)
	if len(left) != len(right):
		raise ValueError("left and right must have equal dimensions")

	distance = math.sqrt(sum((float(a) - float(b)) ** 2 for a, b in zip(left, right)))
	body = {"distance": distance}
	body["verification_digest"] = _digest(body)
	return body
