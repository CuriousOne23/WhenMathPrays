"""
ISc — Inference Scorer (Version 1.0)
Aligned with:
  - isc_py_struc_pgm.md v2.0
  - 20.45_ts_isc_scoring.md v2.0
  - progressive_lineup_testing.md v4.0

Deterministic scoring of TP.ce.candidate_set[] using FFTM four-field weights.
No meaning generation, no candidate expansion, no upstream mutation.
"""

from __future__ import annotations

import copy
import math
from typing import Any, Dict, List, Optional, Tuple

PRIMITIVE_NAME = "isc"

# Default scoring config (ISc-owned). YAML may override later.
DEFAULT_FFTM_WEIGHTS = {
    "w_s": 0.15,
    "w_b": 0.20,
    "w_e": 0.30,
    "w_i": 0.35,
}
DEFAULT_COP = {
    "threshold_amb": 0.85,   # entropy / log2(N)
    "threshold_col": 0.95,   # top normalized mass
    "threshold_drift": 25.0, # |ΔH%|
}
ENTROPY_LOG_BASE = 2.0


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


def _field_feature(value: Any) -> float:
    """Deterministic presence feature in {0.0, 1.0}."""
    if value is None:
        return 0.0
    if isinstance(value, str) and value.strip() == "":
        return 0.0
    if value == "" or value == [] or value == {}:
        return 0.0
    return 1.0


def _log(p: float) -> float:
    if ENTROPY_LOG_BASE == 2.0:
        return math.log2(p)
    return math.log(p) / math.log(ENTROPY_LOG_BASE)


class ISc:
    def __init__(self, tp_input: Optional[dict] = None):
        self.tp = copy.deepcopy(tp_input) if tp_input is not None else {}
        self.weights = dict(DEFAULT_FFTM_WEIGHTS)
        self.cop_cfg = dict(DEFAULT_COP)

    def process(self) -> dict:
        candidates = self._load_candidates(self.tp)
        prior_entropy = self._prior_entropy(self.tp)

        if len(candidates) == 0:
            record, metadata = self._defect_record("TP_DEFECT_EMPTY_CANDIDATE_SET")
            self._write(record, metadata)
            return self.tp

        scored: List[Dict[str, Any]] = []
        for cand in candidates:
            entry = self._score_one(cand)
            scored.append(entry)

        raw_scores = [e["raw_score"] for e in scored]
        normalized = self._normalize(raw_scores)
        for e, n in zip(scored, normalized):
            e["normalized_score"] = n

        entropy = self._entropy(normalized)
        delta_h = self._delta_h_percent(entropy, prior_entropy)
        cop_flag = self._check_cop(normalized, entropy, delta_h)
        conflict = self._score_conflict(normalized)
        reason = self._reason_code(scored, cop_flag, conflict)

        record = self._assemble_record(
            scored, entropy, delta_h, cop_flag, conflict, reason
        )
        metadata = self._build_scoring_metadata(
            scored, entropy, delta_h, cop_flag, conflict, reason
        )
        self._write(record, metadata)
        return self.tp

    # ------------------------------------------------------------------
    # Intake
    # ------------------------------------------------------------------

    def _load_candidates(self, tp: dict) -> List[dict]:
        ce = tp.get("ce") or {}
        cs = ce.get("candidate_set")
        if not isinstance(cs, list):
            return []
        return cs

    def _prior_entropy(self, tp: dict) -> Optional[float]:
        history = tp.get("isc_output") or []
        if not history:
            meta = (tp.get("metadata") or {}).get("scoring_metadata") or {}
            h = meta.get("entropy")
            if isinstance(h, (int, float)):
                return float(h)
            return None
        last = history[-1] if isinstance(history[-1], dict) else {}
        h = last.get("entropy")
        if isinstance(h, (int, float)):
            return float(h)
        return None

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    def _score_one(self, cand: dict) -> Dict[str, Any]:
        fftm = (cand or {}).get("fftm_fields") or {}
        f_s = _field_feature(fftm.get("token_surface"))
        f_b = _field_feature(fftm.get("token_base"))
        f_e = _field_feature(fftm.get("token_expression"))
        f_i = _field_feature(fftm.get("token_intent"))

        raw = (
            self.weights["w_s"] * f_s
            + self.weights["w_b"] * f_b
            + self.weights["w_e"] * f_e
            + self.weights["w_i"] * f_i
        )

        reason_codes = []
        if f_s:
            reason_codes.append("fftm_surface")
        if f_b:
            reason_codes.append("fftm_base")
        if f_e:
            reason_codes.append("fftm_expression")
        if f_i:
            reason_codes.append("fftm_intent")
        if not reason_codes:
            reason_codes.append("zero_score")

        cid = cand.get("candidate_id")
        if cid is None:
            cid = -1

        return {
            "candidate_id": cid,
            "raw_score": float(raw),
            "normalized_score": 0.0,
            "reason_codes": reason_codes,
            "fftm_components": {
                "f_s": f_s,
                "f_b": f_b,
                "f_e": f_e,
                "f_i": f_i,
            },
            "structural_cues": {},
            "semantic_adjacent_cues": {},
        }

    def _normalize(self, raw_scores: List[float]) -> List[float]:
        total = sum(raw_scores)
        n = len(raw_scores)
        if n == 0:
            return []
        if total <= 0.0:
            return [1.0 / n] * n
        return [s / total for s in raw_scores]

    def _entropy(self, probs: List[float]) -> float:
        h = 0.0
        for p in probs:
            if p > 0.0:
                h -= p * _log(p)
        return float(h)

    def _delta_h_percent(self, current: float, prior: Optional[float]) -> float:
        if prior is None or prior == 0.0:
            return 0.0
        return float((current - prior) / prior * 100.0)

    def _check_cop(
        self, probs: List[float], entropy: float, delta_h: float
    ) -> bool:
        n = len(probs)
        if n == 0:
            return False
        max_h = _log(float(n)) if n > 1 else 0.0
        amb = (entropy / max_h) if max_h > 0.0 else 0.0
        top = max(probs) if probs else 0.0
        # collapse uses high top mass; ambiguity uses high relative entropy
        amb_hit = amb > self.cop_cfg["threshold_amb"]
        col_hit = top > self.cop_cfg["threshold_col"] and n > 1
        drift_hit = abs(delta_h) > self.cop_cfg["threshold_drift"]
        return bool(amb_hit or col_hit or drift_hit)

    def _score_conflict(self, probs: List[float]) -> float:
        if len(probs) < 2:
            return 0.0
        ordered = sorted(probs, reverse=True)
        gap = ordered[0] - ordered[1]
        # conflict high when top-two are close
        conflict = max(0.0, 1.0 - gap)
        return float(conflict)

    def _reason_code(
        self, scored: List[dict], cop_flag: bool, conflict: float
    ) -> str:
        if not scored:
            return "TP_DEFECT_EMPTY_CANDIDATE_SET"
        if all(e["raw_score"] == 0.0 for e in scored):
            return "ZERO_SCORE_UNIFORM"
        if cop_flag:
            return "COP_TRIGGERED"
        if conflict >= 0.5:
            return "SCORE_CONFLICT"
        return "SCORED_OK"

    # ------------------------------------------------------------------
    # Output assembly
    # ------------------------------------------------------------------

    def _assemble_record(
        self,
        scored: List[dict],
        entropy: float,
        delta_h: float,
        cop_flag: bool,
        conflict: float,
        reason: str,
    ) -> dict:
        distribution = []
        score_set = []
        for e in scored:
            distribution.append(
                {
                    "candidate_id": e["candidate_id"],
                    "normalized_score": e["normalized_score"],
                    "rationale": ",".join(e["reason_codes"]),
                }
            )
            score_set.append(
                {
                    "candidate_id": e["candidate_id"],
                    "score": e["normalized_score"],
                }
            )

        confidence = 0.0
        if scored:
            confidence = max(e["normalized_score"] for e in scored)

        return {
            "distribution": distribution,
            "entropy": entropy,
            "delta_h_percent": delta_h,
            "confidence": confidence,
            "cop_triggered": cop_flag,
            "score_set": score_set,
            "score_conflict": conflict,
            "score_reason_code": reason,
            "provenance": {
                "origin": "ISc",
                "last_update": "ISc",
                "timestamp": "deterministic",
            },
        }

    def _build_scoring_metadata(
        self,
        scored: List[dict],
        entropy: float,
        delta_h: float,
        cop_flag: bool,
        conflict: float,
        reason: str,
    ) -> dict:
        score_set = [
            {"candidate_id": e["candidate_id"], "score": e["normalized_score"]}
            for e in scored
        ]
        fftm_log = {
            str(e["candidate_id"]): e["fftm_components"] for e in scored
        }
        decisions = [
            {
                "candidate_id": e["candidate_id"],
                "raw_score": e["raw_score"],
                "normalized_score": e["normalized_score"],
                "reason_codes": e["reason_codes"],
            }
            for e in scored
        ]
        return {
            "score_set": score_set,
            "score_conflict": conflict,
            "score_reason_code": reason,
            "cop_triggered": cop_flag,
            "entropy": entropy,
            "delta_h_percent": delta_h,
            "rationale_record": {
                "fftm_components": fftm_log,
                "structural_cues": {},
                "semantic_adjacent_cues": {},
                "scoring_decisions": decisions,
                "cop_flags": ["cop_triggered"] if cop_flag else [],
            },
            "provenance": {
                "origin": "ISc",
                "last_update": "ISc",
            },
        }

    def _defect_record(self, reason: str) -> Tuple[dict, dict]:
        record = {
            "distribution": [],
            "entropy": 0.0,
            "delta_h_percent": 0.0,
            "confidence": 0.0,
            "cop_triggered": False,
            "score_set": [],
            "score_conflict": 0.0,
            "score_reason_code": reason,
            "provenance": {
                "origin": "ISc",
                "last_update": "ISc",
                "timestamp": "deterministic",
            },
        }
        metadata = {
            "score_set": [],
            "score_conflict": 0.0,
            "score_reason_code": reason,
            "cop_triggered": False,
            "entropy": 0.0,
            "delta_h_percent": 0.0,
            "rationale_record": {
                "fftm_components": {},
                "structural_cues": {},
                "semantic_adjacent_cues": {},
                "scoring_decisions": [],
                "cop_flags": [],
            },
            "provenance": {
                "origin": "ISc",
                "last_update": "ISc",
            },
        }
        return record, metadata

    def _write(self, record: dict, metadata: dict) -> None:
        self.tp.setdefault("isc_output", [])
        if not isinstance(self.tp["isc_output"], list):
            self.tp["isc_output"] = []
        self.tp["isc_output"].append(record)

        self.tp.setdefault("metadata", {})
        if not isinstance(self.tp["metadata"], dict):
            self.tp["metadata"] = {}
        self.tp["metadata"]["scoring_metadata"] = metadata

        self.tp["isc"] = {
            "score_set": record.get("score_set"),
            "score_conflict": record.get("score_conflict"),
            "score_reason_code": record.get("score_reason_code"),
            "cop_triggered": record.get("cop_triggered"),
        }
