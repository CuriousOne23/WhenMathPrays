"""
OuBA - Output Basin Primitive (v0.1)
Deterministic commit/freeze primitive aligned to:
  - 20.40.060_ouba_prim.md
  - 20.40.060.010_ouba_input_data_spec.md
  - ouba_py_struc_pgm.md

OuBA writes only commit-layer output envelopes and does not recompute semantics.
"""

from __future__ import annotations

import copy
import hashlib
import json
import time
from typing import Any, Dict, Tuple


PRIMITIVE_NAME = "ouba"


def get_primitive_name() -> str:
	return PRIMITIVE_NAME


def _deep_get(d: dict, *keys, default=None):
	cur = d
	for k in keys:
		if not isinstance(cur, dict):
			return default
		cur = cur.get(k)
	return cur if cur is not None else default


def _canonical_bytes(obj: Any) -> bytes:
	return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


class OUBA:
	"""Deterministic commit primitive that freezes TP state into TPSnS/CTP."""

	def __init__(self, tp: dict | None = None):
		self.tp = copy.deepcopy(tp) if tp is not None else {}

	def process(self, mode: str = "general", **kwargs) -> dict:
		tp = self.tp
		before = copy.deepcopy(tp)

		view = self._extract_commit_view(tp)
		self._validate_commit_view(view)

		commit_timestamp = self._derive_commit_timestamp(tp, mode, kwargs)
		routing_epoch_id = self._derive_routing_epoch_id(view)

		# Build immutable commit payload (without commit hash first).
		tpsns = {
			"tpsns_id": self._derive_tpsns_id(view, commit_timestamp),
			"commit_timestamp": commit_timestamp,
			"commit_hash": "",
			"routing_epoch_id": routing_epoch_id,
			"semantic_core": copy.deepcopy(view["semantic_core"]),
			"proposition_set": copy.deepcopy(view["proposition_set"]),
			"truth_evidence": copy.deepcopy(view["truth_evidence"]),
			"completion_state": copy.deepcopy(view["completion_state"]),
			"semantic_tags": copy.deepcopy(view["semantic_tags"]),
			"lane_local_identity": copy.deepcopy(view["lane_local_identity"]),
			"messy_input_record": copy.deepcopy(view["messy_input_record"]),
			"delta_h_percent": copy.deepcopy(view["delta_h_percent"]),
			"ob_trace": copy.deepcopy(view["ob_trace"]),
			"tb_trace": copy.deepcopy(view["tb_trace"]),
			"policy_markers": copy.deepcopy(view["policy_markers"]),
			"next_context": copy.deepcopy(view["next_context"]),
			"lineage_log": copy.deepcopy(view["lineage_log"]),
			"cob_state_snapshot": copy.deepcopy(view["cob_state_snapshot"]),
			"contextual_alignment_record": copy.deepcopy(view["contextual_alignment_record"]),
			"identity_shift_record": copy.deepcopy(view["identity_shift_record"]),
			"topic_anchor_record": copy.deepcopy(view["topic_anchor_record"]),
			"continuity_record": copy.deepcopy(view["continuity_record"]),
			"intent_record": copy.deepcopy(view["intent_record"]),
			"provenance": {
				"sob_id": view["sob_id"],
				"srob_id": view["srob_id"],
				"cnob_id": view["cnob_id"],
				"smob_id": view["smob_id"],
				"idob_id": view["idob_id"],
				"routing_path": copy.deepcopy(view["routing_path"]),
				"ruleset_ids": copy.deepcopy(view["ruleset_ids"]),
			},
			"metadata": {
				"entropy_history": copy.deepcopy(view["entropy_history"]),
				"signature_history": copy.deepcopy(view["signature_history"]),
			},
		}

		tpsns["commit_hash"] = self._derive_commit_hash(tpsns)

		out = copy.deepcopy(tp)
		out["TPSnS"] = copy.deepcopy(tpsns)
		out["CTP"] = copy.deepcopy(tpsns)
		out["ouba_complete"] = True

		self._write_boundary_guard(before, out)

		self.tp = out
		return out

	def _extract_commit_view(self, tp: dict) -> Dict[str, Any]:
		semantic = tp.get("semantic") if isinstance(tp.get("semantic"), dict) else {}
		metadata = tp.get("metadata") if isinstance(tp.get("metadata"), dict) else {}

		# Allow either top-level or nested sources while preserving values verbatim.
		return {
			"semantic_core": semantic.get("semantic_core", tp.get("semantic_core")),
			"proposition_set": tp.get("proposition_set", semantic.get("proposition_set")),
			"truth_evidence": tp.get("truth_evidence", semantic.get("truth_evidence")),
			"completion_state": tp.get("completion_state", semantic.get("completion_state")),
			"semantic_tags": semantic.get("semantic_tags", tp.get("semantic_tags")),
			"lane_local_identity": semantic.get("lane_local_identity", tp.get("lane_local_identity")),
			"messy_input_record": _deep_get(tp, "metadata", "messy_input_record", default=tp.get("messy_input_record")),
			"delta_h_percent": _deep_get(tp, "metadata", "delta_h_percent", default=tp.get("delta_h_percent")),
			"ob_trace": tp.get("ob_trace", metadata.get("ob_trace")),
			"tb_trace": tp.get("tb_trace", metadata.get("tb_trace")),
			"policy_markers": tp.get("policy_markers", metadata.get("policy_markers")),
			"next_context": tp.get("next_context", metadata.get("next_context")),
			"lineage_log": tp.get("lineage_log", metadata.get("lineage_log")),
			"cob_state_snapshot": tp.get("cob_state_snapshot", metadata.get("cob_state_snapshot")),
			"contextual_alignment_record": metadata.get("contextual_alignment_record"),
			"identity_shift_record": metadata.get("identity_shift_record"),
			"topic_anchor_record": metadata.get("topic_anchor_record"),
			"continuity_record": metadata.get("continuity_record"),
			"intent_record": metadata.get("intent_record"),
			"entropy_history": metadata.get("entropy_history"),
			"signature_history": metadata.get("signature_history"),
			"sob_id": tp.get("sob_id", _deep_get(tp, "metadata", "provenance", "sob_id")),
			"srob_id": tp.get("srob_id", _deep_get(tp, "metadata", "provenance", "srob_id")),
			"cnob_id": tp.get("cnob_id", _deep_get(tp, "metadata", "provenance", "cnob_id")),
			"smob_id": tp.get("smob_id", _deep_get(tp, "metadata", "provenance", "smob_id")),
			"idob_id": tp.get("idob_id", _deep_get(tp, "metadata", "provenance", "idob_id")),
			"routing_path": tp.get("routing_path", _deep_get(tp, "metadata", "provenance", "routing_path")),
			"ruleset_ids": tp.get("ruleset_ids", _deep_get(tp, "metadata", "provenance", "ruleset_ids")),
		}

	def _validate_commit_view(self, view: Dict[str, Any]) -> None:
		required = (
			"semantic_core",
			"proposition_set",
			"truth_evidence",
			"completion_state",
			"semantic_tags",
			"lane_local_identity",
			"messy_input_record",
			"delta_h_percent",
			"ob_trace",
			"tb_trace",
			"policy_markers",
			"next_context",
			"lineage_log",
			"cob_state_snapshot",
			"contextual_alignment_record",
			"identity_shift_record",
			"topic_anchor_record",
			"continuity_record",
			"intent_record",
			"entropy_history",
			"signature_history",
		)
		for key in required:
			if view.get(key) is None:
				raise ValueError(f"OUBA invariant failure: missing required field '{key}'")

	def _derive_commit_timestamp(self, tp: dict, mode: str, kwargs: dict) -> float:
		override = kwargs.get("commit_timestamp_override")
		if override is None:
			override = _deep_get(tp, "_ouba_commit_context", "commit_timestamp")
		if override is not None:
			return float(override)

		if mode == "testbench":
			# Testbench mode must remain deterministic.
			return 0.0
		return float(round(time.time(), 6))

	def _derive_routing_epoch_id(self, view: Dict[str, Any]) -> str:
		base = {
			"routing_path": view.get("routing_path"),
			"ruleset_ids": view.get("ruleset_ids"),
			"lineage_log": view.get("lineage_log"),
		}
		digest = hashlib.sha256(_canonical_bytes(base)).hexdigest()
		return f"route-{digest[:12]}"

	def _derive_tpsns_id(self, view: Dict[str, Any], commit_timestamp: float) -> str:
		base = {
			"semantic_core": view.get("semantic_core"),
			"proposition_set": view.get("proposition_set"),
			"lineage_log": view.get("lineage_log"),
			"commit_timestamp": commit_timestamp,
		}
		digest = hashlib.sha256(_canonical_bytes(base)).hexdigest()
		return f"tpsns-{digest[:16]}"

	def _derive_commit_hash(self, tpsns: Dict[str, Any]) -> str:
		hash_input = copy.deepcopy(tpsns)
		hash_input["commit_hash"] = ""
		return hashlib.sha256(_canonical_bytes(hash_input)).hexdigest()

	def _write_boundary_guard(self, before: dict, after: dict) -> None:
		allowed_new_top_level = {"TPSnS", "CTP", "ouba_complete"}

		# Existing top-level keys must remain unchanged.
		for key, before_val in before.items():
			if key in allowed_new_top_level:
				continue
			if after.get(key) != before_val:
				raise ValueError(f"OUBA write-boundary violation: field '{key}' was modified")

		# No unexpected new top-level keys except OuBA-owned commit fields.
		new_keys = set(after.keys()) - set(before.keys())
		illegal = new_keys - allowed_new_top_level
		if illegal:
			raise ValueError(f"OUBA write-boundary violation: unexpected new fields {sorted(illegal)}")


def process(tp: dict, mode: str = "general", **kwargs) -> dict:
	"""Module-level entry used by testbenches / run.py."""
	return OUBA(tp).process(mode=mode, **kwargs)

