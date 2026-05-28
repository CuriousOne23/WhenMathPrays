"""Deterministic scheduler prototype for 40.40_scheduler_prototypes.

This module exposes a JSON-first contract and deterministic scheduling behavior
for replay and verification in playground experiments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any
import json
import math


MODULE_NAME = "40.40_scheduler_prototypes"
CONTRACT_VERSION = "1.0"
EVENT_CREATED = "created"
EVENT_SCHEDULE_TICK = "schedule_tick"
POLICY_ROUND_ROBIN = "round_robin"
POLICY_WEIGHTED_ROUND_ROBIN = "weighted_round_robin"


def _require_non_empty_str(field_name: str, value: Any) -> str:
	if not isinstance(value, str):
		raise ValueError(f"{field_name} must be a string")
	normalized = value.strip()
	if not normalized:
		raise ValueError(f"{field_name} must be non-empty")
	return normalized


def _require_non_negative_int(field_name: str, value: Any) -> int:
	if isinstance(value, bool) or not isinstance(value, int):
		raise ValueError(f"{field_name} must be an integer")
	if value < 0:
		raise ValueError(f"{field_name} must be non-negative")
	return value


def _require_positive_int(field_name: str, value: Any) -> int:
	number = _require_non_negative_int(field_name, value)
	if number <= 0:
		raise ValueError(f"{field_name} must be positive")
	return number


def _require_non_negative_float(field_name: str, value: Any) -> float:
	try:
		result = float(value)
	except (TypeError, ValueError) as exc:
		raise ValueError(f"{field_name} must be numeric") from exc
	if not math.isfinite(result):
		raise ValueError(f"{field_name} must be finite")
	if result < 0.0:
		raise ValueError(f"{field_name} must be non-negative")
	return result


def _normalize_json_object(field_name: str, value: Any) -> dict[str, Any]:
	if value is None:
		return {}
	if not isinstance(value, dict):
		raise ValueError(f"{field_name} must be a JSON object")
	return {str(k): _json_safe(v) for k, v in value.items()}


def _json_safe(value: Any) -> Any:
	if value is None or isinstance(value, (str, int, bool)):
		return value
	if isinstance(value, float):
		if not math.isfinite(value):
			raise ValueError("JSON values must be finite")
		return value
	if isinstance(value, list):
		return [_json_safe(item) for item in value]
	if isinstance(value, tuple):
		return [_json_safe(item) for item in value]
	if isinstance(value, dict):
		return {str(key): _json_safe(item) for key, item in value.items()}
	raise TypeError(f"Unsupported JSON value: {type(value).__name__}")


def _digest_from_payload(payload: dict[str, Any]) -> str:
	canonical = json.dumps(_json_safe(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
	return sha256(canonical.encode("utf-8")).hexdigest()


def _supported_policy(value: str) -> str:
	normalized = _require_non_empty_str("policy", value)
	if normalized not in {POLICY_ROUND_ROBIN, POLICY_WEIGHTED_ROUND_ROBIN}:
		raise ValueError(f"Unsupported policy: {normalized}")
	return normalized


@dataclass(slots=True)
class ThoughtPoint:
	tp_id: str
	energy: float
	coherence: float
	total_selected: int = 0
	wait_ticks: int = 0
	last_scheduled_tick: int = -1

	def __post_init__(self) -> None:
		self.tp_id = _require_non_empty_str("tp_id", self.tp_id)
		self.energy = _require_non_negative_float("energy", self.energy)
		self.coherence = _require_non_negative_float("coherence", self.coherence)
		self.total_selected = _require_non_negative_int("total_selected", self.total_selected)
		self.wait_ticks = _require_non_negative_int("wait_ticks", self.wait_ticks)
		if self.last_scheduled_tick != -1:
			self.last_scheduled_tick = _require_non_negative_int("last_scheduled_tick", self.last_scheduled_tick)

	@classmethod
	def from_dict(cls, payload: dict[str, Any]) -> ThoughtPoint:
		data = _normalize_json_object("thoughtpoint", payload)
		return cls(
			tp_id=_require_non_empty_str("tp_id", data["tp_id"]),
			energy=_require_non_negative_float("energy", data.get("energy", 1.0)),
			coherence=_require_non_negative_float("coherence", data.get("coherence", 1.0)),
			total_selected=_require_non_negative_int("total_selected", data.get("total_selected", 0)),
			wait_ticks=_require_non_negative_int("wait_ticks", data.get("wait_ticks", 0)),
			last_scheduled_tick=int(data.get("last_scheduled_tick", -1)),
		)

	def as_dict(self) -> dict[str, Any]:
		return {
			"tp_id": self.tp_id,
			"energy": self.energy,
			"coherence": self.coherence,
			"total_selected": self.total_selected,
			"wait_ticks": self.wait_ticks,
			"last_scheduled_tick": self.last_scheduled_tick,
		}


@dataclass(slots=True)
class SchedulerEvent:
	event_type: str
	tick: int
	state_counter: int
	selected_tp_ids: list[str] = field(default_factory=list)
	policy: str = POLICY_ROUND_ROBIN
	payload: dict[str, Any] = field(default_factory=dict)

	def as_dict(self) -> dict[str, Any]:
		return {
			"event_type": self.event_type,
			"tick": self.tick,
			"state_counter": self.state_counter,
			"selected_tp_ids": list(self.selected_tp_ids),
			"policy": self.policy,
			"payload": _json_safe(self.payload),
		}


@dataclass(slots=True)
class SchedulerPrototype:
	tick: int
	deterministic_mode: bool
	policy: str
	max_active: int
	thoughtpoints: dict[str, ThoughtPoint]
	round_robin_cursor: int = 0
	state_counter: int = 0
	history: list[SchedulerEvent] = field(default_factory=list)
	verification_digest: str = ""

	def __post_init__(self) -> None:
		self.tick = _require_non_negative_int("tick", self.tick)
		self.deterministic_mode = bool(self.deterministic_mode)
		self.policy = _supported_policy(self.policy)
		self.max_active = _require_positive_int("max_active", self.max_active)
		if not self.thoughtpoints:
			raise ValueError("thoughtpoints must not be empty")
		if len(set(self.thoughtpoints)) != len(self.thoughtpoints):
			raise ValueError("thoughtpoints must have unique tp_id keys")
		self.round_robin_cursor = _require_non_negative_int("round_robin_cursor", self.round_robin_cursor)
		self.state_counter = _require_non_negative_int("state_counter", self.state_counter)
		self._refresh_digest()

	@classmethod
	def from_contract(cls, payload: dict[str, Any]) -> SchedulerPrototype:
		contract = _normalize_json_object("payload", payload)
		thoughtpoint_payloads = contract.get("thoughtpoints")
		if not isinstance(thoughtpoint_payloads, list) or not thoughtpoint_payloads:
			raise ValueError("thoughtpoints must be a non-empty list")
		thoughtpoints = [ThoughtPoint.from_dict(item) for item in thoughtpoint_payloads]
		tp_map = {tp.tp_id: tp for tp in thoughtpoints}
		if len(tp_map) != len(thoughtpoints):
			raise ValueError("tp_id values must be unique")

		instance = cls(
			tick=_require_non_negative_int("tick", contract.get("tick", 0)),
			deterministic_mode=bool(contract.get("deterministic_mode", True)),
			policy=_supported_policy(contract.get("policy", POLICY_ROUND_ROBIN)),
			max_active=_require_positive_int("max_active", contract.get("max_active", 1)),
			thoughtpoints=tp_map,
			round_robin_cursor=_require_non_negative_int("round_robin_cursor", contract.get("round_robin_cursor", 0)),
			state_counter=_require_non_negative_int("state_counter", contract.get("state_counter", 0)),
		)
		instance._record_event(
			event_type=EVENT_CREATED,
			tick=instance.tick,
			selected_tp_ids=[],
			payload={"source": "from_contract"},
			advance_state=False,
		)
		return instance

	def apply_contract(self, payload: dict[str, Any]) -> dict[str, Any]:
		event = _normalize_json_object("payload", payload)
		event_type = _require_non_empty_str("event_type", event["event_type"])
		if event_type != EVENT_SCHEDULE_TICK:
			raise ValueError(f"Unsupported event_type: {event_type}")

		next_tick = _require_non_negative_int("tick", event.get("tick", self.tick + 1))
		if next_tick <= self.tick:
			raise ValueError("tick must be strictly increasing")

		requested_policy = _supported_policy(event.get("policy", self.policy))
		if not self.deterministic_mode and requested_policy == POLICY_WEIGHTED_ROUND_ROBIN:
			pass
		self.policy = requested_policy
		if "max_active" in event:
			self.max_active = _require_positive_int("max_active", event["max_active"])

		selected = self._select_for_tick()
		selected_set = set(selected)

		for tp in self.thoughtpoints.values():
			if tp.tp_id in selected_set:
				tp.total_selected += 1
				tp.wait_ticks = 0
				tp.last_scheduled_tick = next_tick
			else:
				tp.wait_ticks += 1

		self.tick = next_tick
		self._record_event(
			event_type=EVENT_SCHEDULE_TICK,
			tick=self.tick,
			selected_tp_ids=selected,
			payload={
				"max_active": self.max_active,
				"policy": self.policy,
				"thoughtpoint_count": len(self.thoughtpoints),
			},
		)
		return self.snapshot()

	def snapshot(self) -> dict[str, Any]:
		body = self._snapshot_body()
		body["verification_digest"] = self.verification_digest
		return body

	def assert_invariants(self) -> None:
		if not self.thoughtpoints:
			raise ValueError("Scheduler invariant violation: empty thoughtpoint set")
		if len(set(self.thoughtpoints)) != len(self.thoughtpoints):
			raise ValueError("Scheduler invariant violation: duplicate thoughtpoint IDs")
		if self.max_active <= 0:
			raise ValueError("Scheduler invariant violation: max_active must be positive")
		expected = _digest_from_payload(self._snapshot_body())
		if self.verification_digest != expected:
			raise ValueError("verification_digest is out of sync with scheduler state")

	def _select_for_tick(self) -> list[str]:
		ordered_ids = sorted(self.thoughtpoints)
		selection_count = min(self.max_active, len(ordered_ids))
		if selection_count <= 0:
			return []

		if self.policy == POLICY_ROUND_ROBIN:
			cursor = self.round_robin_cursor % len(ordered_ids)
			rotated = ordered_ids[cursor:] + ordered_ids[:cursor]
			selected = rotated[:selection_count]
			self.round_robin_cursor = (cursor + selection_count) % len(ordered_ids)
			return selected

		def weighted_score(tp: ThoughtPoint) -> float:
			age_weight = 1.0
			energy_weight = 0.1
			coherence_weight = 0.1
			return (
				age_weight * float(tp.wait_ticks)
				+ energy_weight * float(tp.energy)
				+ coherence_weight * float(tp.coherence)
			)

		weighted = sorted(
			ordered_ids,
			key=lambda tp_id: (-weighted_score(self.thoughtpoints[tp_id]), tp_id),
		)
		return weighted[:selection_count]

	def _record_event(
		self,
		*,
		event_type: str,
		tick: int,
		selected_tp_ids: list[str],
		payload: dict[str, Any],
		advance_state: bool = True,
	) -> None:
		if advance_state:
			self.state_counter += 1
		self.history.append(
			SchedulerEvent(
				event_type=event_type,
				tick=tick,
				state_counter=self.state_counter,
				selected_tp_ids=list(selected_tp_ids),
				policy=self.policy,
				payload=_normalize_json_object("event_payload", payload),
			)
		)
		self._refresh_digest()

	def _snapshot_body(self) -> dict[str, Any]:
		return {
			"module": MODULE_NAME,
			"contract_version": CONTRACT_VERSION,
			"tick": self.tick,
			"deterministic_mode": self.deterministic_mode,
			"policy": self.policy,
			"max_active": self.max_active,
			"round_robin_cursor": self.round_robin_cursor,
			"state_counter": self.state_counter,
			"thoughtpoints": [
				self.thoughtpoints[tp_id].as_dict() for tp_id in sorted(self.thoughtpoints)
			],
			"history": [event.as_dict() for event in self.history],
		}

	def _refresh_digest(self) -> None:
		self.verification_digest = _digest_from_payload(self._snapshot_body())


__all__ = [
	"EVENT_SCHEDULE_TICK",
	"POLICY_ROUND_ROBIN",
	"POLICY_WEIGHTED_ROUND_ROBIN",
	"SchedulerPrototype",
]
