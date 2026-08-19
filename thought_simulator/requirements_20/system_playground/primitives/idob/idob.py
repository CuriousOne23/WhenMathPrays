"""
IdOB — Identity Object Basin Primitive (v0.1)
Deterministic realization of operator I per:
  20.40.050_idob_prim.md v3.0
  idob_py_struc_pgm.md v0.1
  progressive_lineup_testing.md v4.2

meaning_delta_h (HLR-043..049):
  meaning_delta_h = ||m_after - m_before||_1 / K
  K is the fixed sum of max_range(m_i) over the meaning-layer feature layout.
  m_before = 0 on first IdOB pass / post-reset (HLR-048).
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Tuple

PRIMITIVE_NAME = "idob"

# ---------------------------------------------------------------------------
# Provisional meaning-layer feature layout (v0.1)
# Ordered, fixed ranges. K is constant across all TP snapshots (HLR-049).
# When the semantic_core / FFTM meaning-layer schema is locked, replace this
# table; do not derive K from runtime values of m_before / m_after.
# ---------------------------------------------------------------------------
GEOMETRY_MAP = {
    "formation": 0,
    "refinement": 1,
    "correction": 2,
    "drift": 3,
    "conflict": 4,
    "bifurcation": 5,
    "stabilization": 6,
    "convergence": 7,
    "alignment": 8,
    "closure": 9,
}
CONTINUITY_MAP = {
    "continuation": 0,
    "correction": 1,
    "drift": 2,
    "bifurcation": 3,
    "stabilization": 4,
}
PRESSURE_MAP = {"low": 0, "medium": 1, "high": 2}
MAG_MAP = {"small": 0, "medium": 1, "large": 2}
PATTERN_MAP = {
    "small": 0,
    "collapsed": 1,
    "collapsing": 2,
    "medium": 3,
    "explosion": 4,
    "two_clusters": 5,
}
FREEZE_MAP = {"none": 0, "identity_freeze": 1}
BASIN_MAP = {
    "none": 0,
    "basin": 1,
    "unstable": 2,
    "transition_surface": 3,
    "split": 4,
}

# max_range for each ordered feature (must match the maps above)
FEATURE_MAX_RANGES: List[float] = [
    9.0,  # geometry
    4.0,  # continuity
    2.0,  # pressure
    2.0,  # residual magnitude
    5.0,  # residual pattern
    1.0,  # freeze
    4.0,  # basin_surface
]
K: float = sum(FEATURE_MAX_RANGES)  # 27.0 — constant


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


class IdOB:
    """Identity-conditioned meaning refinement after routing commitment."""

    def __init__(self, tp: Optional[dict] = None):
        self.tp = copy.deepcopy(tp) if tp is not None else {}

    # ------------------------------------------------------------------
    # Public entry
    # ------------------------------------------------------------------
    def process(self, mode: str = "general", **kwargs) -> dict:
        tp = self.tp
        before = copy.deepcopy(tp)

        meta = tp.setdefault("metadata", {})
        identity = meta.get("identity") or {}
        # If identity lives under semantic for some fixtures, normalize
        if not identity and isinstance(tp.get("semantic"), dict):
            identity = (tp.get("semantic") or {}).get("identity") or {}

        # Snapshot meaning vector before transition (HLR-048 first-pass rule)
        m_before = self._encode_meaning_vector(identity)
        if self._is_first_meaning_cycle(identity):
            m_before = [0.0] * len(FEATURE_MAX_RANGES)

        # Apply deterministic transition rules (struc_pgm §4)
        new_identity = self._apply_transition(identity, meta)

        # Write identity envelope back under metadata.identity
        meta["identity"] = new_identity

        # Meaning delta (HLR-043..049)
        m_after = self._encode_meaning_vector(new_identity)
        meaning_delta_h = self._l1_normalized(m_before, m_after)

        # Completion / eligibility (struc_pgm §6)
        complete, eligible = self._completion_flags(new_identity)
        tp["idob_complete"] = complete
        tp["path_b_eligible"] = eligible

        # Minimal TPU-style markers (HLR-024 surface)
        tp.setdefault("tpu", {})
        tp["tpu"]["idob_update"] = {
            "idob_complete": complete,
            "path_b_eligible": eligible,
            "meaning_delta_h": meaning_delta_h,
            "idob_semantics": [],
            "idob_next_ob_candidates": [] if complete else ["idob"],
        }

        # Also surface under TP.semantic for downstream consumers (HLR-014)
        semantic = tp.setdefault("semantic", {})
        semantic["meaning_delta_h"] = meaning_delta_h

        # Write-boundary guard (diagnostic only in this v0.1)
        self._write_boundary_guard(before, tp)

        self.tp = tp
        return tp

    # ------------------------------------------------------------------
    # Meaning-layer vector & delta (HLR-043..049)
    # ------------------------------------------------------------------
    def _encode_meaning_vector(self, identity: dict) -> List[float]:
        """Map identity envelope fields → fixed-length meaning-layer vector."""
        if not identity:
            return [0.0] * len(FEATURE_MAX_RANGES)

        geom = identity.get("geometry", "formation")
        cont = identity.get("continuity", "continuation")
        press = identity.get("pressure", "low")
        residuals = identity.get("residuals") or {}
        mag = residuals.get("magnitude", "small")
        pattern = residuals.get("pattern", "small")
        freeze = (identity.get("freeze") or {}).get("state", "none")
        basin = (identity.get("basin_surface") or {}).get("region", "none")

        return [
            float(GEOMETRY_MAP.get(geom, 0)),
            float(CONTINUITY_MAP.get(cont, 0)),
            float(PRESSURE_MAP.get(press, 0)),
            float(MAG_MAP.get(mag, 0)),
            float(PATTERN_MAP.get(pattern, 0)),
            float(FREEZE_MAP.get(freeze, 0)),
            float(BASIN_MAP.get(basin, 0)),
        ]

    def _is_first_meaning_cycle(self, identity: dict) -> bool:
        """
        True when no prior meaning state exists (HLR-048).
        First IdOB pass or first meaning cycle after reset.
        Do not infer from missing TP fields alone; require positive evidence
        of an empty / pre-formation state.
        """
        if not identity:
            return True
        geom = identity.get("geometry")
        basin = (identity.get("basin_surface") or {}).get("region")
        # Formation with no basin surface yet is the canonical first-pass signal
        if geom == "formation" and basin in (None, "none"):
            return True
        return False

    def _l1_normalized(self, m_before: List[float], m_after: List[float]) -> float:
        """||m_after - m_before||_1 / K  →  [0, 1]"""
        if len(m_before) != len(m_after) or len(m_before) != len(FEATURE_MAX_RANGES):
            # Defensive: should never happen with the fixed layout
            return 0.0
        l1 = sum(abs(a - b) for a, b in zip(m_after, m_before))
        if K <= 0.0:
            return 0.0
        delta = l1 / K
        # Clamp for numerical safety (should already be in [0, 1])
        return max(0.0, min(1.0, delta))

    # ------------------------------------------------------------------
    # Transition table (seeded by the 10 examples / struc_pgm §4.1)
    # ------------------------------------------------------------------
    def _apply_transition(self, identity: dict, meta: dict) -> dict:
        geom = identity.get("geometry", "formation")
        pressure = identity.get("pressure", "low")
        residuals = identity.get("residuals") or {}
        mag = residuals.get("magnitude", "small")
        pattern = residuals.get("pattern", "small")
        freeze_in = (identity.get("freeze") or {}).get("state", "none")
        basin_in = (identity.get("basin_surface") or {}).get("region", "none")
        stance = (meta.get("stance") or {}).get("category", "clarify")
        routing = (meta.get("routing") or {}).get("mode", "forward")

        out = copy.deepcopy(identity) if identity else {}
        out.setdefault("geometry", geom)
        out.setdefault("continuity", identity.get("continuity", "continuation"))
        out.setdefault("pressure", pressure)
        out.setdefault("residuals", {"magnitude": mag, "pattern": pattern})
        out.setdefault("freeze", {"state": freeze_in})
        out.setdefault("basin_surface", {"region": basin_in})

        # Deterministic adjustments matching the 10-case expected blocks
        if geom == "formation":
            out["geometry"] = "formation"
            out["continuity"] = "continuation"
            out["freeze"] = {"state": "none"}
            out["basin_surface"] = {"region": "basin"}
            out["residuals"] = {"magnitude": "small", "pattern": "small"}

        elif geom == "refinement":
            out["geometry"] = "refinement"
            out["continuity"] = "continuation"
            out["freeze"] = {"state": "none"}
            out["basin_surface"] = {"region": "basin"}
            out["residuals"] = {"magnitude": "small", "pattern": "collapsed"}

        elif geom == "correction":
            out["geometry"] = "correction"
            out["continuity"] = "correction"
            out["freeze"] = {"state": "none"}
            out["basin_surface"] = {"region": "unstable"}
            out["residuals"] = {"magnitude": "medium", "pattern": "medium"}

        elif geom == "drift":
            out["geometry"] = "drift"
            out["continuity"] = "correction"
            out["freeze"] = {"state": "identity_freeze"}
            out["basin_surface"] = {"region": "unstable"}
            out["residuals"] = {"magnitude": "medium", "pattern": "medium"}

        elif geom == "conflict":
            out["geometry"] = "conflict"
            out["continuity"] = "correction"
            out["freeze"] = {"state": "identity_freeze"}
            out["basin_surface"] = {"region": "transition_surface"}
            out["residuals"] = {"magnitude": "large", "pattern": "explosion"}

        elif geom == "bifurcation":
            out["geometry"] = "bifurcation"
            out["continuity"] = "bifurcation"
            out["freeze"] = {"state": "identity_freeze"}
            out["basin_surface"] = {"region": "split"}
            out["residuals"] = {"magnitude": "large", "pattern": "two_clusters"}

        elif geom == "stabilization":
            out["geometry"] = "stabilization"
            out["continuity"] = "continuation"
            out["freeze"] = {"state": "none"}
            out["basin_surface"] = {"region": "basin"}
            out["residuals"] = {"magnitude": "medium", "pattern": "collapsing"}

        elif geom == "convergence":
            out["geometry"] = "convergence"
            out["continuity"] = "continuation"
            out["freeze"] = {"state": "none"}
            out["basin_surface"] = {"region": "basin"}
            out["residuals"] = {"magnitude": "small", "pattern": "small"}

        elif geom == "alignment":
            out["geometry"] = "alignment"
            out["continuity"] = "continuation"
            out["freeze"] = {"state": "none"}
            out["basin_surface"] = {"region": "basin"}
            out["residuals"] = {"magnitude": "small", "pattern": "collapsed"}

        elif geom == "closure":
            out["geometry"] = "closure"
            out["continuity"] = "continuation"
            out["freeze"] = {"state": "none"}
            out["basin_surface"] = {"region": "basin"}
            out["residuals"] = {"magnitude": "small", "pattern": "collapsed"}

        # Preserve pressure from input unless overridden
        out["pressure"] = pressure

        return out

    def _completion_flags(self, identity: dict) -> tuple[bool, bool]:
        geom = identity.get("geometry")
        residuals = identity.get("residuals") or {}
        pattern = residuals.get("pattern", "")
        freeze = (identity.get("freeze") or {}).get("state", "none")

        complete = (
            geom in ("stabilization", "convergence", "alignment", "closure")
            and pattern in ("small", "collapsed", "collapsing")
            and freeze == "none"
            and geom == "closure"  # strict for v0.1: only final closure marks complete
        )
        # path_b_eligible true from alignment onward
        eligible = geom in ("alignment", "closure")
        return complete, eligible

    def _write_boundary_guard(self, before: dict, after: dict) -> None:
        """Diagnostic only in v0.1; hard fail belongs in rulechecker/testbench."""
        # Ensure we did not invent routing_filter or geometric_state writes
        def _get(d, *keys):
            cur = d
            for k in keys:
                if not isinstance(cur, dict):
                    return None
                cur = cur.get(k)
            return cur

        # No mutation of process.routing_filter if it existed
        if _get(before, "process", "routing_filter") is not None:
            if _get(before, "process", "routing_filter") != _get(after, "process", "routing_filter"):
                # In production this would raise; here we leave a marker
                after.setdefault("_idob_diagnostics", {})["routing_filter_mutated"] = True


def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    """Module-level entry used by testbenches / run.py."""
    return IdOB(tp).process(mode=mode, **kwargs)
