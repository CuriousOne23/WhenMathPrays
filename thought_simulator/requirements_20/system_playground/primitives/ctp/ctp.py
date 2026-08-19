"""
CTP — Collect Thought Point (Version 1.0)
Aligned with:
  - 20.145 (v3.0)
  - ctp_py_struc_pgm.md
  - progressive_lineup_testing.md v4.2

Always-before-RB barrier. Policy freeze only (no TP.CTP block).
Appends exactly one schema-stable cognitive_history entry per invocation.
Missing sources → null. Never invents. Never rejects for missing IdOB.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, Optional

PRIMITIVE_NAME = "ctp"

INVARIANT_KEYS = (
    "I_stab",
    "R_res",
    "P_cont",
    "L_depth",
    "Rt_adj",
    "delta_H",
    "E_dens",
    "C_coh",
)

HISTORY_TOP_KEYS = (
    "cycle_id",
    "timestamp",
    "invariants",
    "idob_geometry",
    "idob_roles",
    "idob_residue",
    "idob_stability",
    "rb_adjacency_class",
    "rb_displacement_scale",
    "rb_regime_hint",
    "rb_route_proposal",
)


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


class CTP:
    def __init__(
        self,
        tp_input: Optional[dict] = None,
        cycle_id=None,
        timestamp=None,
    ):
        self.tp = copy.deepcopy(tp_input) if tp_input is not None else {}
        ctx = self.tp.get("_ctp_cycle_context") or {}
        if not isinstance(ctx, dict):
            ctx = {}
        self._ctx_cycle_id = cycle_id if cycle_id is not None else ctx.get("cycle_id")
        self._ctx_timestamp = (
            timestamp if timestamp is not None else ctx.get("timestamp")
        )

    def process(self) -> dict:
        cycle_id = self._resolve_cycle_id()
        timestamp = self._resolve_timestamp()
        entry = self._build_cognitive_history_entry(cycle_id, timestamp)
        self._append_cognitive_history(entry)
        self._write_provenance(timestamp)
        self._append_audit_optional(cycle_id, timestamp)
        return self.tp

    # ------------------------------------------------------------------
    # Resolve cycle context
    # ------------------------------------------------------------------

    def _meta(self) -> dict:
        meta = self.tp.get("metadata")
        if not isinstance(meta, dict):
            self.tp["metadata"] = {}
            meta = self.tp["metadata"]
        return meta

    def _resolve_cycle_id(self):
        if self._ctx_cycle_id is not None:
            try:
                return int(self._ctx_cycle_id)
            except (TypeError, ValueError):
                pass

        meta = self.tp.get("metadata") if isinstance(self.tp.get("metadata"), dict) else {}
        prov = meta.get("provenance") if isinstance(meta.get("provenance"), dict) else {}
        if prov.get("dcb_cycle_id") is not None:
            try:
                return int(prov["dcb_cycle_id"])
            except (TypeError, ValueError):
                pass

        hist = meta.get("geometric_history") or []
        if isinstance(hist, list) and hist:
            last = hist[-1]
            if isinstance(last, dict) and last.get("cycle_id") is not None:
                try:
                    return int(last["cycle_id"])
                except (TypeError, ValueError):
                    pass
        return None

    def _resolve_timestamp(self):
        if self._ctx_timestamp is not None:
            try:
                return float(self._ctx_timestamp)
            except (TypeError, ValueError):
                pass

        meta = self.tp.get("metadata") if isinstance(self.tp.get("metadata"), dict) else {}
        prov = meta.get("provenance") if isinstance(meta.get("provenance"), dict) else {}
        if prov.get("dcb_last_update") is not None:
            try:
                return float(prov["dcb_last_update"])
            except (TypeError, ValueError):
                pass
        return None

    # ------------------------------------------------------------------
    # Read helpers (copy or null)
    # ------------------------------------------------------------------

    def _foundation(self) -> dict:
        f = self.tp.get("_ctp_foundation")
        return f if isinstance(f, dict) else {}

    def _read_foundation_value(self, key: str):
        f = self._foundation()
        if key in f and f.get(key) is not None:
            return f.get(key)
        # optional alternate key for delta_H
        if key == "delta_H" and "deltaH" in f and f.get("deltaH") is not None:
            return f.get("deltaH")
        return None

    def _read_idob(self) -> dict:
        semantic = self.tp.get("semantic") if isinstance(self.tp.get("semantic"), dict) else {}
        idob = semantic.get("idob")
        return idob if isinstance(idob, dict) else {}

    def _read_rb_filter(self) -> dict:
        process = self.tp.get("process") if isinstance(self.tp.get("process"), dict) else {}
        rf = process.get("routing_filter")
        return rf if isinstance(rf, dict) else {}

    def _build_cognitive_history_entry(self, cycle_id, timestamp) -> dict:
        idob = self._read_idob()
        geom = idob.get("geometry") if isinstance(idob.get("geometry"), dict) else {}
        rf = self._read_rb_filter()

        invariants = {k: self._read_foundation_value(k) for k in INVARIANT_KEYS}

        entry = {
            "cycle_id": cycle_id,
            "timestamp": timestamp,
            "invariants": invariants,
            "idob_geometry": {
                "neighborhood": geom.get("neighborhood") if geom else None,
                "k_id": geom.get("k_id") if geom else None,
            },
            "idob_roles": idob.get("roles") if idob else None,
            "idob_residue": idob.get("residue") if idob else None,
            "idob_stability": idob.get("stability") if idob else None,
            "rb_adjacency_class": rf.get("adjacency_class") if rf else None,
            "rb_displacement_scale": rf.get("displacement_scale") if rf else None,
            "rb_regime_hint": rf.get("regime_hint") if rf else None,
            "rb_route_proposal": rf.get("route_proposal") if rf else None,
        }
        # Ensure neighborhood/k_id keys exist even when geometry missing
        if entry["idob_geometry"]["neighborhood"] is None and not geom:
            entry["idob_geometry"]["neighborhood"] = None
        if entry["idob_geometry"]["k_id"] is None and not geom:
            entry["idob_geometry"]["k_id"] = None
        return entry

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def _append_cognitive_history(self, entry: dict) -> None:
        meta = self._meta()
        hist = meta.get("cognitive_history")
        if not isinstance(hist, list):
            hist = []
            meta["cognitive_history"] = hist
        hist.append(entry)

    def _write_provenance(self, timestamp) -> None:
        meta = self._meta()
        prov = meta.get("provenance")
        if not isinstance(prov, dict):
            prov = {}
            meta["provenance"] = prov
        if timestamp is not None:
            try:
                prov["ctp_last_update"] = float(timestamp)
            except (TypeError, ValueError):
                prov["ctp_last_update"] = timestamp
        else:
            prov["ctp_last_update"] = None

    def _append_audit_optional(self, cycle_id, timestamp) -> None:
        self.tp.setdefault("exec_trace", [])
        if not isinstance(self.tp["exec_trace"], list):
            self.tp["exec_trace"] = []
        self.tp["exec_trace"].append(
            {
                "ctp_ref": {
                    "origin": "CTP",
                    "last_update": "CTP",
                    "cycle_id": cycle_id,
                    "timestamp": timestamp,
                }
            }
        )


def run(tp: dict, **kwargs) -> dict:
    return CTP(tp, **kwargs).process()
