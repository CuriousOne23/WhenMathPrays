"""
MCB — Meaning–Clarifying Bridge Primitive (v0.1)
Deterministic realization per:
  20.40.055_mcb_prim.md v2.0
  mcb_py_struc_pgm.md v0.1
  progressive_lineup_testing.md v4.2

Owns:
  - mcb_delta_h, mcb_semantics[], meaning_semantics[] refinement
  - TP.next_context{} (next-turn context generation)
  - mcb_context_coherence, mcb_context_shift_required
  - mcb_complete, mcb_next_ob_candidates[]
  - TPU.mcb_update payload

Does NOT own / mutate:
  - current-turn clarifying fields
  - routing / RED / TR
  - structural ΔH% / DCB geometry
  - Path-B envelopes
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Tuple

PRIMITIVE_NAME = "mcb"

# First-order stance polarity for reinforcement / conflict detection
STANCE_POLARITY = {
    "confirm": 1,
    "emphasize": 1,
    "clarify": 0,
    "uncertain": -1,
    "reject": -2,
}


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


class MCB:
    """Meaning–clarifying reconciliation and next-turn context generation."""

    def __init__(self, tp: Optional[dict] = None):
        self.tp = copy.deepcopy(tp) if tp is not None else {}

    # ------------------------------------------------------------------
    # Public entry
    # ------------------------------------------------------------------
    def process(self, mode: str = "general", **kwargs) -> dict:
        tp = self.tp
        before = copy.deepcopy(tp)

        meaning = self._extract_meaning_view(tp)
        clarifying = self._extract_clarifying_view(tp)

        outcome, agreement_score = self._detect_reinforcement_or_conflict(
            meaning, clarifying
        )
        mcb_delta_h = self._compute_mcb_delta_h(outcome, agreement_score)
        mcb_semantics = self._build_mcb_semantics(outcome, meaning, clarifying)

        coherent = outcome == "reinforcement"
        shift_required = outcome == "conflict"

        next_context = self._generate_next_context(
            meaning, clarifying, coherent, shift_required
        )

        # Completion: v0.1 treats a finished next_context block as complete
        # unless serial refinement is explicitly requested by residual conflict
        complete = outcome != "conflict"
        next_candidates: List[str] = [] if complete else ["mcb"]

        # Surface under semantic (HLR-018, 024, 025)
        semantic = tp.setdefault("semantic", {})
        semantic["mcb_delta_h"] = mcb_delta_h
        semantic["mcb_semantics"] = mcb_semantics
        semantic["mcb_context_coherence"] = coherent
        semantic["mcb_context_shift_required"] = shift_required

        # Preserve / lightly refine meaning_semantics when present
        existing_ms = semantic.get("meaning_semantics") or []
        if mcb_semantics and outcome == "reinforcement":
            semantic["meaning_semantics"] = list(existing_ms) + [
                {"cue": "clarifying_reinforced", "source": "mcb"}
            ]
        elif mcb_semantics and outcome == "conflict":
            semantic["meaning_semantics"] = list(existing_ms) + [
                {"cue": "clarifying_conflict", "source": "mcb"}
            ]

        # Next-context ownership (HLR-032 … 041)
        tp["next_context"] = next_context

        # Completion flags
        tp["mcb_complete"] = complete
        tp["mcb_next_ob_candidates"] = next_candidates

        # TPU.mcb_update payload (HLR-030)
        tp.setdefault("tpu", {})
        tp["tpu"]["mcb_update"] = {
            "mcb_delta_h": mcb_delta_h,
            "mcb_semantics": mcb_semantics,
            "meaning_semantics": semantic.get("meaning_semantics", []),
            "next_context": next_context,
            "mcb_context_coherence": coherent,
            "mcb_context_shift_required": shift_required,
            "mcb_complete": complete,
            "mcb_next_ob_candidates": next_candidates,
        }

        # Diagnostic observability
        tp.setdefault("_mcb_diagnostics", {})
        tp["_mcb_diagnostics"]["outcome"] = outcome
        tp["_mcb_diagnostics"]["agreement_score"] = agreement_score

        self._write_boundary_guard(before, tp)

        self.tp = tp
        return tp

    # ------------------------------------------------------------------
    # Extract views (read-only)
    # ------------------------------------------------------------------
    def _extract_meaning_view(self, tp: dict) -> dict:
        meta = (tp or {}).get("metadata") or {}
        semantic = (tp or {}).get("semantic") or {}
        identity = meta.get("identity") or semantic.get("identity") or {}
        stance = meta.get("stance") or {}
        direction = meta.get("direction") or {}
        importance = meta.get("importance") or {}

        return {
            "geometry": identity.get("geometry"),
            "continuity": identity.get("continuity"),
            "pressure": identity.get("pressure"),
            "stance_category": stance.get("category", "clarify"),
            "direction_flow": direction.get("flow", "next"),
            "importance_level": importance.get("level", "medium"),
            "meaning_delta_h": semantic.get("meaning_delta_h"),
            "topic_hint": (meta.get("context") or {}).get("topic")
            or (meta.get("context_metadata") or {}).get("topic"),
        }

    def _extract_clarifying_view(self, tp: dict) -> dict:
        meta = (tp or {}).get("metadata") or {}
        context = meta.get("context") or meta.get("context_metadata") or {}
        clarifying = meta.get("clarifying") or meta.get("clarifying_metadata") or {}

        # Prefer explicit clarifying block; fall back to context fields
        topic = clarifying.get("topic") or context.get("topic") or "unknown"
        stance = clarifying.get("stance") or context.get("stance") or "clarify"
        intent = clarifying.get("intent") or context.get("intent") or "continue"
        register = clarifying.get("register") or context.get("register") or "neutral"
        politeness = clarifying.get("politeness") or context.get("politeness") or "neutral"
        continuity = clarifying.get("continuity") or context.get("continuity") or "continuation"
        direction = clarifying.get("direction") or context.get("direction") or "next"
        importance = clarifying.get("importance") or context.get("importance") or "medium"

        return {
            "topic": topic,
            "stance": stance,
            "intent": intent,
            "register": register,
            "politeness": politeness,
            "continuity": continuity,
            "direction": direction,
            "importance": importance,
        }

    # ------------------------------------------------------------------
    # Reconciliation (first-order)
    # ------------------------------------------------------------------
    def _detect_reinforcement_or_conflict(
        self, meaning: dict, clarifying: dict
    ) -> Tuple[str, float]:
        """
        Returns (outcome, agreement_score).
        outcome ∈ {reinforcement, conflict, neutral}
        agreement_score ∈ [-1.0, 1.0] approximately
        """
        m_stance = meaning.get("stance_category", "clarify")
        c_stance = clarifying.get("stance", "clarify")

        m_pol = STANCE_POLARITY.get(m_stance, 0)
        c_pol = STANCE_POLARITY.get(c_stance, 0)

        # Same-sign or both neutral → reinforcement tendency
        # Opposite polarity (especially reject vs confirm) → conflict
        product = m_pol * c_pol

        # Continuity signal
        cont = clarifying.get("continuity", "continuation")
        cont_bonus = 0.2 if cont in ("continuation", "stabilize") else (
            -0.3 if cont in ("shift", "reset", "break") else 0.0
        )

        score = float(product) * 0.4 + cont_bonus

        # Explicit reject in clarifying against confirm/emphasize meaning
        if c_pol <= -2 and m_pol >= 1:
            return "conflict", max(-1.0, score - 0.5)
        if m_pol <= -2 and c_pol >= 1:
            return "conflict", max(-1.0, score - 0.5)

        if score >= 0.15:
            return "reinforcement", min(1.0, score)
        if score <= -0.25:
            return "conflict", max(-1.0, score)
        return "neutral", score

    def _compute_mcb_delta_h(self, outcome: str, agreement_score: float) -> float:
        """
        Scalar magnitude of clarifying–meaning refinement in [0, 1].
        Reinforcement → moderate positive magnitude.
        Conflict → larger corrective magnitude.
        Neutral → near-zero.
        """
        if outcome == "reinforcement":
            return round(min(1.0, 0.25 + abs(agreement_score) * 0.35), 4)
        if outcome == "conflict":
            return round(min(1.0, 0.45 + abs(agreement_score) * 0.40), 4)
        return round(min(0.15, abs(agreement_score) * 0.20), 4)

    def _build_mcb_semantics(
        self, outcome: str, meaning: dict, clarifying: dict
    ) -> List[dict]:
        base = {
            "outcome": outcome,
            "meaning_stance": meaning.get("stance_category"),
            "clarifying_stance": clarifying.get("stance"),
            "topic": clarifying.get("topic"),
        }
        if outcome == "reinforcement":
            return [{**base, "cue": "reinforcement", "direction": "strengthen"}]
        if outcome == "conflict":
            return [{**base, "cue": "conflict", "direction": "correct"}]
        return [{**base, "cue": "neutral", "direction": "hold"}]

    # ------------------------------------------------------------------
    # Next-context generation (HLR-019 … 041)
    # ------------------------------------------------------------------
    def _generate_next_context(
        self,
        meaning: dict,
        clarifying: dict,
        coherent: bool,
        shift_required: bool,
    ) -> dict:
        topic = clarifying.get("topic") or meaning.get("topic_hint") or "unknown"
        stance = clarifying.get("stance") or meaning.get("stance_category") or "clarify"
        intent = clarifying.get("intent") or "continue"
        register = clarifying.get("register") or "neutral"
        politeness = clarifying.get("politeness") or "neutral"
        importance = clarifying.get("importance") or meaning.get("importance_level") or "medium"

        if shift_required:
            continuity = "shift"
            direction = "pivot"
            epistemic = "open"
        elif coherent:
            continuity = clarifying.get("continuity") or "continuation"
            direction = clarifying.get("direction") or meaning.get("direction_flow") or "next"
            epistemic = "stable"
        else:
            continuity = "hold"
            direction = "next"
            epistemic = "uncertain"

        return {
            "topic": topic,
            "stance": stance,
            "intent": intent,
            "register": register,
            "politeness": politeness,
            "epistemic_shading": epistemic,
            "continuity": continuity,
            "direction": direction,
            "coherence": coherent,
            "shift_required": shift_required,
            "importance": importance,
        }

    # ------------------------------------------------------------------
    # Write-boundary guard (diagnostic in v0.1; hard-fail in rulechecker)
    # ------------------------------------------------------------------
    def _write_boundary_guard(self, before: dict, after: dict) -> None:
        def _get(d, *keys):
            cur = d
            for k in keys:
                if not isinstance(cur, dict):
                    return None
                cur = cur.get(k)
            return cur

        diagnostics = after.setdefault("_mcb_diagnostics", {})

        # Must not mutate routing_filter
        if _get(before, "process", "routing_filter") is not None:
            if _get(before, "process", "routing_filter") != _get(
                after, "process", "routing_filter"
            ):
                diagnostics["routing_filter_mutated"] = True

        # Must not mutate geometric_state (DCB)
        if _get(before, "metadata", "geometric_state") is not None:
            if _get(before, "metadata", "geometric_state") != _get(
                after, "metadata", "geometric_state"
            ):
                diagnostics["geometric_state_mutated"] = True

        # Must not mutate current-turn clarifying block if present
        before_clar = _get(before, "metadata", "clarifying") or _get(
            before, "metadata", "clarifying_metadata"
        )
        after_clar = _get(after, "metadata", "clarifying") or _get(
            after, "metadata", "clarifying_metadata"
        )
        if before_clar is not None and before_clar != after_clar:
            diagnostics["current_turn_clarifying_mutated"] = True


def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    """Module-level entry used by testbenches / run.py."""
    return MCB(tp).process(mode=mode, **kwargs)
