"""Deterministic regulator prototype.

This module defines a small regulator contract that is importable, deterministic,
and JSON-friendly for harness verification.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json


POLICY_CLAMP = "clamp"
POLICY_ATTENUATE = "attenuate"
SUPPORTED_POLICIES = {POLICY_CLAMP, POLICY_ATTENUATE}


def _canonical_json(payload: dict[str, object]) -> str:
	return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _digest(payload: dict[str, object]) -> str:
	return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _require_number(name: str, value: object, minimum: float | None = None) -> float:
	if not isinstance(value, (int, float)):
		raise ValueError(f"{name} must be numeric")
	parsed = float(value)
	if minimum is not None and parsed < minimum:
		raise ValueError(f"{name} must be >= {minimum}")
	return parsed


def _require_policy(value: object) -> str:
	if not isinstance(value, str) or value not in SUPPORTED_POLICIES:
		raise ValueError("policy must be one of clamp|attenuate")
	return value


@dataclass(frozen=True)
class RegulatorDecision:
	action: str
	applied_delta: float
	rationale: str
	verification_digest: str

	def to_dict(self) -> dict[str, object]:
		return {
			"action": self.action,
			"applied_delta": self.applied_delta,
			"rationale": self.rationale,
			"verification_digest": self.verification_digest,
		}


def evaluate_regulator(contract: dict[str, object]) -> RegulatorDecision:
	"""Evaluate a deterministic regulator decision from a JSON-style contract."""
	policy = _require_policy(contract.get("policy"))
	pressure = _require_number("pressure", contract.get("pressure"), minimum=0.0)
	max_delta = _require_number("max_delta", contract.get("max_delta"), minimum=0.0)

	if policy == POLICY_CLAMP:
		applied_delta = min(pressure, max_delta)
		action = "clamp" if pressure > 0 else "noop"
		rationale = "bounded_by_max_delta"
	else:
		applied_delta = min(pressure, max_delta) * 0.5
		action = "attenuate" if pressure > 0 else "noop"
		rationale = "half_bounded_delta"

	body = {
		"policy": policy,
		"pressure": pressure,
		"max_delta": max_delta,
		"action": action,
		"applied_delta": applied_delta,
		"rationale": rationale,
	}
	return RegulatorDecision(
		action=action,
		applied_delta=applied_delta,
		rationale=rationale,
		verification_digest=_digest(body),
	)
