"""Macro-style basin prototype for the Thought Simulator playground.

The module keeps all mutable state inside classes, exposes a JSON-first public API,
and produces deterministic snapshots when the same contract sequence is replayed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any, Iterable
import json
import math


MODULE_NAME = "30.30_basin_prototypes"
CONTRACT_VERSION = "1.0"
EVENT_CREATED = "created"
EVENT_PROVENANCE_ADD = "provenance_add"
EVENT_TRANSITION = "transition"
EVENT_ENTROPY_UPDATE = "entropy_update"


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


def _require_iterable(field_name: str, value: Any) -> list[Any]:
	if isinstance(value, (str, bytes)):
		raise ValueError(f"{field_name} must be a sequence, not text")
	try:
		return list(value)
	except TypeError as exc:
		raise ValueError(f"{field_name} must be iterable") from exc


def _normalize_float_vector(values: Any, field_name: str) -> list[float]:
	normalized = []
	for item in _require_iterable(field_name, values):
		try:
			coerced = float(item)
		except (TypeError, ValueError) as exc:
			raise ValueError(f"{field_name} must contain numeric values") from exc
		if not math.isfinite(coerced):
			raise ValueError(f"{field_name} must contain finite values")
		if coerced < 0.0:
			raise ValueError(f"{field_name} must contain non-negative values")
		normalized.append(coerced)
	if not normalized:
		raise ValueError(f"{field_name} must not be empty")
	return normalized


def _normalize_string_list(values: Any, field_name: str, allow_empty: bool = False) -> list[str]:
	normalized: list[str] = []
	for item in _require_iterable(field_name, values):
		normalized.append(_require_non_empty_str(field_name, item))
	if not normalized and not allow_empty:
		raise ValueError(f"{field_name} must not be empty")
	if len(set(normalized)) != len(normalized):
		raise ValueError(f"{field_name} must contain unique values")
	return normalized


def _normalize_json_object(field_name: str, value: Any) -> dict[str, Any]:
	if value is None:
		return {}
	if not isinstance(value, dict):
		raise ValueError(f"{field_name} must be a JSON object")
	return {str(key): _json_safe(item) for key, item in value.items()}


def _json_safe(value: Any) -> Any:
	if value is None or isinstance(value, (str, int, bool)):
		return value
	if isinstance(value, float):
		if not math.isfinite(value):
			raise ValueError("JSON values must be finite")
		return value
	if isinstance(value, dict):
		return {str(key): _json_safe(item) for key, item in value.items()}
	if isinstance(value, list):
		return [_json_safe(item) for item in value]
	if isinstance(value, tuple):
		return [_json_safe(item) for item in value]
	raise TypeError(f"Unsupported JSON value: {type(value).__name__}")


def _digest_from_payload(payload: dict[str, Any]) -> str:
	canonical = json.dumps(_json_safe(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
	return sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class BasinEvent:
	event_type: str
	tick: int
	state_counter: int
	basin_id: str
	tp_id: str
	provenance_id: str | None = None
	note: str = ""
	payload: dict[str, Any] = field(default_factory=dict)

	def as_dict(self) -> dict[str, Any]:
		return {
			"event_type": self.event_type,
			"tick": self.tick,
			"state_counter": self.state_counter,
			"basin_id": self.basin_id,
			"tp_id": self.tp_id,
			"provenance_id": self.provenance_id,
			"note": self.note,
			"payload": _json_safe(self.payload),
		}


@dataclass(slots=True)
class BasinPrototype:
	basin_id: str
	tp_id: str
	state_counter: int
	deterministic_mode: bool
	entropy_vector: list[float]
	provenance_ids: list[str] = field(default_factory=list)
	tags: list[str] = field(default_factory=list)
	metadata: dict[str, Any] = field(default_factory=dict)
	history: list[BasinEvent] = field(default_factory=list)
	last_event: str = EVENT_CREATED
	last_tick: int = 0
	verification_digest: str = ""

	def __post_init__(self) -> None:
		self.basin_id = _require_non_empty_str("basin_id", self.basin_id)
		self.tp_id = _require_non_empty_str("tp_id", self.tp_id)
		self.state_counter = _require_non_negative_int("state_counter", self.state_counter)
		self.deterministic_mode = bool(self.deterministic_mode)
		self.entropy_vector = _normalize_float_vector(self.entropy_vector, "entropy_vector")
		self.provenance_ids = _normalize_string_list(self.provenance_ids, "provenance_ids", allow_empty=True)
		self.tags = _normalize_string_list(self.tags, "tags", allow_empty=True)
		self.metadata = _normalize_json_object("metadata", self.metadata)
		self.history = list(self.history)
		self.last_event = _require_non_empty_str("last_event", self.last_event)
		self.last_tick = _require_non_negative_int("last_tick", self.last_tick)
		self._refresh_digest()

	@classmethod
	def from_contract(cls, payload: dict[str, Any]) -> BasinPrototype:
		contract = _normalize_json_object("payload", payload)
		basin_id = _require_non_empty_str("basin_id", contract["basin_id"])
		tp_id = _require_non_empty_str("tp_id", contract["tp_id"])
		state_counter = _require_non_negative_int("state_counter", contract["state_counter"])
		deterministic_mode = bool(contract["deterministic_mode"])
		entropy_vector = _normalize_float_vector(contract["entropy_vector"], "entropy_vector")
		provenance_ids = _normalize_string_list(contract.get("provenance_ids", []), "provenance_ids", allow_empty=True)
		tags = _normalize_string_list(contract.get("tags", []), "tags", allow_empty=True)
		metadata = _normalize_json_object("metadata", contract.get("metadata", {}))
		last_tick = _require_non_negative_int("tick", contract.get("tick", 0))
		instance = cls(
			basin_id=basin_id,
			tp_id=tp_id,
			state_counter=state_counter,
			deterministic_mode=deterministic_mode,
			entropy_vector=entropy_vector,
			provenance_ids=provenance_ids,
			tags=tags,
			metadata=metadata,
			last_event=EVENT_CREATED,
			last_tick=last_tick,
		)
		instance._record_event(
			event_type=EVENT_CREATED,
			tick=last_tick,
			provenance_id=provenance_ids[0] if provenance_ids else None,
			note="from_contract",
			payload={"source": "from_contract"},
			advance_state=False,
		)
		return instance

	def apply_contract(self, payload: dict[str, Any]) -> dict[str, Any]:
		event = _normalize_json_object("payload", payload)
		event_type = _require_non_empty_str("event_type", event["event_type"])
		tick = _require_non_negative_int("tick", event.get("tick", self.last_tick))
		if tick < self.last_tick:
			raise ValueError("tick must be monotonic")

		if event_type == EVENT_PROVENANCE_ADD:
			provenance_id = _require_non_empty_str("provenance_id", event["provenance_id"])
			if provenance_id in self.provenance_ids:
				raise ValueError("provenance_id must be unique")
			self.provenance_ids.append(provenance_id)
			self._record_event(
				event_type=EVENT_PROVENANCE_ADD,
				tick=tick,
				provenance_id=provenance_id,
				note=_require_non_empty_str("note", event.get("note", "provenance_added")),
				payload={"provenance_id": provenance_id},
			)
		elif event_type == EVENT_TRANSITION:
			target_basin_id = _require_non_empty_str("target_basin_id", event["target_basin_id"])
			if target_basin_id == self.basin_id:
				raise ValueError("target_basin_id must differ from basin_id")
			previous_basin_id = self.basin_id
			self.basin_id = target_basin_id
			self._record_event(
				event_type=EVENT_TRANSITION,
				tick=tick,
				provenance_id=_require_non_empty_str("provenance_id", event.get("provenance_id")) if event.get("provenance_id") is not None else None,
				note=_require_non_empty_str("note", event.get("note", "transition")),
				payload={"previous_basin_id": previous_basin_id, "target_basin_id": target_basin_id},
			)
		elif event_type == EVENT_ENTROPY_UPDATE:
			entropy_vector = _normalize_float_vector(event["entropy_vector"], "entropy_vector")
			if len(entropy_vector) != len(self.entropy_vector):
				raise ValueError("entropy_vector length must remain stable")
			previous_entropy_vector = list(self.entropy_vector)
			self.entropy_vector = entropy_vector
			self._record_event(
				event_type=EVENT_ENTROPY_UPDATE,
				tick=tick,
				provenance_id=_require_non_empty_str("provenance_id", event.get("provenance_id")) if event.get("provenance_id") is not None else None,
				note=_require_non_empty_str("note", event.get("note", "entropy_update")),
				payload={"previous_entropy_vector": previous_entropy_vector, "entropy_vector": list(self.entropy_vector)},
			)
		else:
			raise ValueError(f"Unsupported event_type: {event_type}")

		return self.snapshot()

	def snapshot(self) -> dict[str, Any]:
		body = self._snapshot_body()
		body["verification_digest"] = self.verification_digest
		return body

	def assert_invariants(self) -> None:
		invariants = self._invariants_snapshot()
		if not all(invariants.values()):
			raise ValueError(f"Basin invariant violation: {invariants}")
		expected_digest = _digest_from_payload(self._snapshot_body())
		if self.verification_digest != expected_digest:
			raise ValueError("verification_digest is out of sync with basin state")

	def _record_event(
		self,
		*,
		event_type: str,
		tick: int,
		provenance_id: str | None,
		note: str,
		payload: dict[str, Any],
		advance_state: bool = True,
	) -> BasinEvent:
		if tick < self.last_tick:
			raise ValueError("tick must be monotonic")
		if advance_state:
			self.state_counter += 1
		self.last_tick = tick
		self.last_event = event_type
		event = BasinEvent(
			event_type=event_type,
			tick=tick,
			state_counter=self.state_counter,
			basin_id=self.basin_id,
			tp_id=self.tp_id,
			provenance_id=provenance_id,
			note=note,
			payload=payload,
		)
		self.history.append(event)
		self._refresh_digest()
		self.assert_invariants()
		return event

	def _invariants_snapshot(self) -> dict[str, bool]:
		history_state_counters = [event.state_counter for event in self.history]
		return {
			"basin_id_non_empty": bool(self.basin_id),
			"tp_id_non_empty": bool(self.tp_id),
			"state_counter_non_negative": self.state_counter >= 0,
			"deterministic_mode_is_bool": isinstance(self.deterministic_mode, bool),
			"entropy_vector_non_empty": bool(self.entropy_vector),
			"entropy_vector_is_finite": all(math.isfinite(value) and value >= 0.0 for value in self.entropy_vector),
			"provenance_ids_unique": len(self.provenance_ids) == len(set(self.provenance_ids)),
			"tags_unique": len(self.tags) == len(set(self.tags)),
			"history_monotonic": history_state_counters == sorted(history_state_counters),
			"history_matches_state_counter": not self.history or self.history[-1].state_counter == self.state_counter,
		}

	def _snapshot_body(self) -> dict[str, Any]:
		return {
			"module": MODULE_NAME,
			"contract_version": CONTRACT_VERSION,
			"basin_id": self.basin_id,
			"tp_id": self.tp_id,
			"state_counter": self.state_counter,
			"deterministic_mode": self.deterministic_mode,
			"entropy_vector": list(self.entropy_vector),
			"provenance_ids": list(self.provenance_ids),
			"tags": list(self.tags),
			"metadata": _json_safe(self.metadata),
			"last_event": self.last_event,
			"last_tick": self.last_tick,
			"history": [event.as_dict() for event in self.history],
			"invariants": self._invariants_snapshot(),
		}

	def _refresh_digest(self) -> None:
		self.verification_digest = _digest_from_payload(self._snapshot_body())
