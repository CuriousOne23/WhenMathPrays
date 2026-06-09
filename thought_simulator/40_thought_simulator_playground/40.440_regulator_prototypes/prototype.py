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
POLICY_STABILIZE = "stabilize"  # exploratory, non-canonical per Non-Goals
SUPPORTED_POLICIES = {POLICY_CLAMP, POLICY_ATTENUATE, POLICY_STABILIZE}

ENFORCEMENT_AREAS = ["delta_h", "fan_out", "operator_cost", "overflow", "memory", "cycle_time"]


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
		raise ValueError(f"policy must be one of {sorted(SUPPORTED_POLICIES)}")
	return value

def _require_area(value: object) -> str:
	if not isinstance(value, str) or value not in ENFORCEMENT_AREAS:
		raise ValueError(f"area must be one of {ENFORCEMENT_AREAS}")
	return value


@dataclass(frozen=True)
class RegulatorDecision:
	action: str
	applied_delta: float
	rationale: str
	enforcement_area: str
	interrupt_level: str
	obs: dict[str, object]
	verification_digest: str

	def to_dict(self) -> dict[str, object]:
		return {
			"action": self.action,
			"applied_delta": self.applied_delta,
			"rationale": self.rationale,
			"enforcement_area": self.enforcement_area,
			"interrupt_level": self.interrupt_level,
			"obs": self.obs,
			"verification_digest": self.verification_digest,
		}


def evaluate_regulator(contract: dict[str, object]) -> RegulatorDecision:
	"""Evaluate a deterministic regulator decision from a JSON-style contract.
	Supports multiple enforcement areas per the 40.50 Phase A "What Phase B Must Explore".
	Exploratory only — numeric thresholds and exact policy algos are non-canonical (see Non-Goals, governed by 20.95/50-series and 10.50.50).
	"""
	policy = _require_policy(contract.get("policy"))
	area = contract.get("enforcement_area", "delta_h")  # default for backward compat
	if area not in ENFORCEMENT_AREAS:
		# allow multi or default
		area = "multi"

	# Support single pressure (backward) or per-area
	if "pressure" in contract:
		pressure = _require_number("pressure", contract.get("pressure"), minimum=0.0)
		max_val = _require_number("max_delta", contract.get("max_delta", 1.0), minimum=0.0)
		areas = {area: {"pressure": pressure, "max": max_val}}
	else:
		# richer multi-area input for full coverage
		areas = {}
		for a in ENFORCEMENT_AREAS:
			if f"{a}_pressure" in contract:
				p = _require_number(f"{a}_pressure", contract[f"{a}_pressure"], minimum=0.0 if a != "fan_out" else 0)
				m = _require_number(f"{a}_max", contract.get(f"{a}_max", 1.0), minimum=0.0)
				areas[a] = {"pressure": p, "max": m}

	if not areas:
		areas = {"delta_h": {"pressure": 0.0, "max": 1.0}}  # default

	# Compute per area
	enforcements = {}
	overall_interrupt = "none"
	total_applied = 0.0
	rationale_parts = []
	SEVERITY = {"none": 0, "L2": 1, "L1": 2, "L0": 3}
	for a, vals in areas.items():
		p = vals["pressure"]
		m = vals["max"]
		if policy == POLICY_CLAMP:
			applied = min(p, m)
			act = "clamp" if p > 0 else "noop"
			rat = f"{a}:bounded_by_max"
		elif policy == POLICY_ATTENUATE:
			applied = min(p, m) * 0.5
			act = "attenuate" if p > 0 else "noop"
			rat = f"{a}:half_bounded"
		else:  # stabilize exploratory
			applied = p * 0.1
			act = "stabilize" if p > 0 else "noop"
			rat = f"{a}:stabilized"
		enforcements[a] = {"action": act, "applied": applied, "rationale": rat}
		total_applied += applied
		rationale_parts.append(rat)

		# Determine interrupt per area (exploratory thresholds, non-final)
		if p > m:
			if a in ("delta_h", "overflow", "memory"):
				level = "L1"
			elif a in ("fan_out", "operator_cost", "cycle_time"):
				level = "L2"
			else:
				level = "L1"
			if SEVERITY.get(level, 0) > SEVERITY.get(overall_interrupt, 0):
				overall_interrupt = level

	rationale = " ; ".join(rationale_parts) or "no_violation"
	action = "multi_enforce" if len(areas) > 1 else list(enforcements.values())[0]["action"]

	obs = {
		"enforcements": enforcements,
		"interrupt_level": overall_interrupt,
		"total_applied_impact": total_applied,
		"areas_covered": list(areas.keys()),
		"policy": policy,
		"boundary_marker": "enforcement",
		"policy_signature": "exploratory_v1",  # non-canonical
	}

	body = {
		"policy": policy,
		"areas": areas,
		"action": action,
		"applied_delta": total_applied,
		"rationale": rationale,
		"enforcement_area": "multi" if len(areas) > 1 else list(areas.keys())[0],
		"interrupt_level": overall_interrupt,
		"obs": obs,
	}

	return RegulatorDecision(
		action=action,
		applied_delta=total_applied,
		rationale=rationale,
		enforcement_area="multi" if len(areas) > 1 else list(areas.keys())[0],
		interrupt_level=overall_interrupt,
		obs=obs,
		verification_digest=_digest(body),
	)


class Regulator:
	"""Stateful regulator for bounded history and rich stateful tests (Part B)."""
	def __init__(self, max_history: int = 16):
		self.max_history = max_history
		self.decision_history: list[dict] = []
		self.state_counter: int = 0

	def evaluate(self, contract: dict[str, object]) -> dict[str, object]:
		decision = evaluate_regulator(contract)
		d = decision.to_dict()
		self.state_counter += 1
		hist_entry = {
			"enforcement_area": d["enforcement_area"],
			"pressure": contract.get("pressure", 0.0),
			"applied_delta": d["applied_delta"],
			"interrupt_level": d["interrupt_level"],
			"rationale": d["rationale"],
			"tick": contract.get("tick", self.state_counter),
		}
		self.decision_history.append(hist_entry)
		if len(self.decision_history) > self.max_history:
			self.decision_history = self.decision_history[-self.max_history:]
		d["obs"] = {**d.get("obs", {}), "history_len": len(self.decision_history), "state_counter": self.state_counter}
		# refresh digest with state
		body_for_digest = {k: v for k, v in d.items() if k != "verification_digest"}
		d["verification_digest"] = _digest(body_for_digest)
		return d

	def get_history_len(self) -> int:
		return len(self.decision_history)
