"""Deterministic event log prototype."""

from __future__ import annotations

import hashlib
import json


REQUIRED_FIELDS = ("sequence", "tick", "event_type", "payload")


def _digest(events: list[dict[str, object]]) -> str:
	encoded = json.dumps(events, sort_keys=True, separators=(",", ":")).encode("utf-8")
	return hashlib.sha256(encoded).hexdigest()


class EventLog:
	def __init__(self) -> None:
		self._events: list[dict[str, object]] = []
		self._last_sequence = -1

	def append(self, event: dict[str, object]) -> dict[str, object]:
		if not isinstance(event, dict):
			raise ValueError("event must be a dictionary")
		for field in REQUIRED_FIELDS:
			if field not in event:
				raise ValueError(f"missing required event field: {field}")
		sequence = event["sequence"]
		if not isinstance(sequence, int) or sequence < 0:
			raise ValueError("sequence must be a non-negative integer")
		if sequence != self._last_sequence + 1:
			raise ValueError("sequence must advance by exactly one")

		self._events.append(event)
		self._last_sequence = sequence
		return {
			"event_count": len(self._events),
			"verification_digest": _digest(self._events),
		}

	def replay(self) -> list[dict[str, object]]:
		return list(self._events)
