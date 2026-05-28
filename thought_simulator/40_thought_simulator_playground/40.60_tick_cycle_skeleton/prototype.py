"""Deterministic tick-cycle skeleton prototype."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json


CANONICAL_PHASES = ("schedule", "process", "transition", "log")


def _digest(payload: dict[str, object]) -> str:
	encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
	return hashlib.sha256(encoded).hexdigest()


@dataclass
class TickCycle:
	last_tick: int = -1

	def execute_tick(self, contract: dict[str, object]) -> dict[str, object]:
		tick = contract.get("tick")
		if not isinstance(tick, int) or tick < 0:
			raise ValueError("tick must be a non-negative integer")
		if tick != self.last_tick + 1:
			raise ValueError("tick must advance by exactly one")

		phases = contract.get("phases", list(CANONICAL_PHASES))
		if not isinstance(phases, list):
			raise ValueError("phases must be a list")
		if phases != list(CANONICAL_PHASES):
			raise ValueError("phases must match canonical order")

		self.last_tick = tick
		body = {
			"tick": tick,
			"executed_phases": phases,
			"state_digest": _digest({"tick": tick, "phases": phases}),
		}
		return body
