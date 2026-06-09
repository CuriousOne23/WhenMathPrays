"""Deterministic snapshot prototype."""

from __future__ import annotations

import hashlib
import json


def _canonical(value: object) -> str:
	return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _digest_state(state: dict[str, object]) -> str:
	return hashlib.sha256(_canonical(state).encode("utf-8")).hexdigest()


def dump_snapshot(state: dict[str, object], schema_version: str = "v1") -> dict[str, object]:
	if not isinstance(state, dict):
		raise ValueError("state must be a dictionary")
	if not isinstance(schema_version, str) or not schema_version:
		raise ValueError("schema_version must be a non-empty string")
	return {
		"schema_version": schema_version,
		"state": state,
		"digest": _digest_state(state),
	}


def load_snapshot(snapshot: dict[str, object], expected_schema: str = "v1") -> dict[str, object]:
	if not isinstance(snapshot, dict):
		raise ValueError("snapshot must be a dictionary")
	schema = snapshot.get("schema_version")
	if schema != expected_schema:
		raise ValueError("schema version mismatch")
	state = snapshot.get("state")
	if not isinstance(state, dict):
		raise ValueError("snapshot state must be a dictionary")
	digest = snapshot.get("digest")
	if not isinstance(digest, str) or digest != _digest_state(state):
		raise ValueError("snapshot digest mismatch")
	return {"schema_version": schema, "state": state, "digest": digest}
