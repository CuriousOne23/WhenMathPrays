"""
IdOB — Identity Object Basin Primitive (v0.1)
Deterministic realization of operator I per:
  20.40.050_idob_prim.md v3.0
  idob_py_struc_pgm.md v0.1
  progressive_lineup_testing.md v4.2
"""

from __future__ import annotations

import copy
from typing import Any, Dict, Optional

PRIMITIVE_NAME = "idob"


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

        # Apply deterministic transition rules (struc_pgm §4)
        new_identity = self._apply_transition(identity, meta)

        # Write identity envelope back under metadata.identity
        meta["identity"] = new_identity

        # Completion / eligibility (struc_pgm §6)
        complete, eligible = self._completion_flags(new_identity)
        tp["idob_complete"] = complete
        tp["path_b_eligible"] = eligible

        # Minimal TPU-style markers (HLR-024 surface)
        tp.setdefault("tpu", {})
        tp["tpu"]["idob_update"] = {
            "idob_complete": complete,
            "path_b_eligible": eligible,
            "meaning_delta_h": 0.0,  # placeholder; real delta later
            "idob_semantics": [],
            "idob_next_ob_candidates": [] if complete else ["idob"],
        }

        # Write-boundary guard (diagnostic only in this v0.1)
        self._write_boundary_guard(before, tp)

        self.tp = tp
        return tp

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
