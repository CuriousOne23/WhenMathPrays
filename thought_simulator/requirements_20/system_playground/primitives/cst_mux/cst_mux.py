"""
CST-Mux — Stability Signal Multiplexing Module
System Playground Version 0.1

Aligned with:
- 20.32.010.030_cst-mux.md
- cst-mux_requirements.md
- cst_mux_py_struc_pgm.md
- patha_field_names.md (TP.cst.mux lock)
- progressive_lineup_testing.md

Pure packaging: no reinterpretation of Core/MS signals.
Presence-based flags (not heritage thresholds).
USP is CIL-only (never written toward COB).
"""

from __future__ import annotations

from typing import Any, Dict, List, Set
import copy


PRIMITIVE_NAME = "cst_mux"
WINDOW_LEN = 10


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


def _deep_get(d: Any, *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
        if cur is None:
            return default
    return cur


def _shallow_copy(obj: Any) -> Any:
    if obj is None:
        return None
    return copy.deepcopy(obj)


class CST_MUX:
    """Pure functional multiplexer; optional usp_window may ride on TP."""

    def __init__(self):
        self._usp_window: List[Dict[str, Any]] = []

    @staticmethod
    def extract_core(tp: Dict[str, Any]) -> Dict[str, Any]:
        return ((tp.get("cst") or {}).get("core")) or {}

    @staticmethod
    def extract_ms(tp: Dict[str, Any]) -> Dict[str, Any]:
        return ((tp.get("cst") or {}).get("ms")) or {}

    def collect_layer_ids(self, core: Dict[str, Any], ms: Dict[str, Any]) -> List[str]:
        ids: Set[str] = set()

        per = ((core.get("metrics") or {}).get("per_layer")) or {}
        if isinstance(per, dict):
            ids.update(str(k) for k in per.keys())

        status = core.get("status") or {}
        for lid in status.get("frozen_layers") or []:
            ids.add(str(lid))

        signals = core.get("signals") or {}
        for key, list_key in (
            ("freeze", "frozen_objects"),
            ("thaw", "thawed_objects"),
            ("continuity_restoration", "restored_objects"),
            ("drift", "affected_objects"),
            ("oscillation", "affected_objects"),
            ("ambiguity", "affected_objects"),
            ("collapse", "collapsed_objects"),
        ):
            for lid in (signals.get(key) or {}).get(list_key) or []:
                ids.add(str(lid))

        for block_name in (
            "stability",
            "instability",
            "collapse_risk",
            "freeze_risk",
            "thaw_readiness",
            "normalized_metrics",
            "weighted_metrics",
        ):
            block = ms.get(block_name) or {}
            per_ms = block.get("per_layer") or {}
            if isinstance(per_ms, dict):
                ids.update(str(k) for k in per_ms.keys())

        commands = ms.get("commands") or {}
        for cmd in ("freeze", "thaw", "collapse_recovery", "split"):
            for lid in (commands.get(cmd) or {}).get("layers") or []:
                ids.add(str(lid))

        return sorted(ids)

    def assign_layer_indices(self, layer_ids: List[str]) -> Dict[str, int]:
        return {lid: i for i, lid in enumerate(layer_ids)}

    def package_core(self, core: Dict[str, Any]) -> Dict[str, Any]:
        signals = core.get("signals") or {}
        metrics = core.get("metrics") or {}
        status = core.get("status") or {}
        return {
            "signals": _shallow_copy(signals),
            "metrics": _shallow_copy(metrics),
            "status": {
                "frozen_layers": list(status.get("frozen_layers") or []),
            },
        }

    def package_ms(self, ms: Dict[str, Any]) -> Dict[str, Any]:
        meta = ms.get("metadata") or {}
        diagnostics = ms.get("diagnostics") or {}
        return {
            "normalized_metrics": _shallow_copy(ms.get("normalized_metrics")),
            "weighted_metrics": _shallow_copy(ms.get("weighted_metrics")),
            "stability": _shallow_copy(ms.get("stability")),
            "instability": _shallow_copy(ms.get("instability")),
            "collapse_risk": _shallow_copy(ms.get("collapse_risk")),
            "freeze_risk": _shallow_copy(ms.get("freeze_risk")),
            "thaw_readiness": _shallow_copy(ms.get("thaw_readiness")),
            "ambiguity_summary": _shallow_copy(ms.get("ambiguity_summary")),
            "drift_summary": _shallow_copy(ms.get("drift_summary")),
            "oscillation_summary": _shallow_copy(ms.get("oscillation_summary")),
            "commands": _shallow_copy(ms.get("commands")),
            "command_log": _shallow_copy(ms.get("command_log")),
            "diagnostics": {
                "sync_mismatch": bool(diagnostics.get("sync_mismatch", False)),
                "sync_mismatch_detail": diagnostics.get("sync_mismatch_detail"),
            },
            "metadata": {
                "new_context_required": bool(meta.get("new_context_required", False)),
            },
        }

    def package_presence_flags(
        self,
        layer_ids: List[str],
        core: Dict[str, Any],
        ms: Dict[str, Any],
    ) -> Dict[str, Any]:
        signals = core.get("signals") or {}
        commands = ms.get("commands") or {}

        frozen = set(str(x) for x in (signals.get("freeze") or {}).get("frozen_objects") or [])
        frozen |= set(str(x) for x in ((core.get("status") or {}).get("frozen_layers") or []))
        frozen |= set(str(x) for x in (commands.get("freeze") or {}).get("layers") or [])

        thawed = set(str(x) for x in (signals.get("thaw") or {}).get("thawed_objects") or [])
        thawed |= set(str(x) for x in (commands.get("thaw") or {}).get("layers") or [])

        continuous = set(
            str(x)
            for x in (signals.get("continuity_restoration") or {}).get("restored_objects")
            or []
        )

        activation = {lid: True for lid in layer_ids}
        freeze_flags = {lid: (lid in frozen) for lid in layer_ids}
        thaw_flags = {lid: (lid in thawed) for lid in layer_ids}
        continuity_flags = {lid: (lid in continuous) for lid in layer_ids}

        # Aggregate convenience (heritage-compatible shape)
        return {
            "activation": activation,
            "freeze": freeze_flags,
            "thaw": thaw_flags,
            "continuity": continuity_flags,
            "activated": bool(layer_ids),
            "frozen": bool(frozen),
            "thawed": bool(thawed),
            "continuous": bool(continuous),
        }

    def assemble_usp(
        self,
        turn_index: int,
        layer_index: Dict[str, int],
        core_pack: Dict[str, Any],
        ms_pack: Dict[str, Any],
        flags: Dict[str, Any],
        new_context_required: bool,
    ) -> Dict[str, Any]:
        # Fixed key order for deterministic comparison
        return {
            "turn_index": turn_index,
            "layer_index": dict(layer_index),
            "core": core_pack,
            "ms": ms_pack,
            "flags": flags,
            "new_context_required": bool(new_context_required),
        }

    @staticmethod
    def write_boundary_guard(tp_before: Dict[str, Any], tp_after: Dict[str, Any]) -> List[str]:
        errors: List[str] = []

        before_snap = ((tp_before.get("identity") or {}).get("cob_state_snapshot"))
        after_snap = ((tp_after.get("identity") or {}).get("cob_state_snapshot"))
        if before_snap is not None and after_snap != before_snap:
            errors.append("cob_state_snapshot mutated by cst_mux")

        before_core = ((tp_before.get("cst") or {}).get("core"))
        after_core = ((tp_after.get("cst") or {}).get("core"))
        if before_core is not None and after_core != before_core:
            errors.append("TP.cst.core mutated by cst_mux")

        before_ms = ((tp_before.get("cst") or {}).get("ms"))
        after_ms = ((tp_after.get("cst") or {}).get("ms"))
        if before_ms is not None and after_ms != before_ms:
            errors.append("TP.cst.ms mutated by cst_mux")

        if "cil" in tp_after and "cil" not in tp_before:
            errors.append("cil envelope written by cst_mux")

        for forbidden in ("routing_filter", "geometric_state", "semantic_core"):
            if forbidden in tp_after and forbidden not in tp_before:
                errors.append(f"forbidden field written: {forbidden}")

        return errors

    def write_envelope(
        self,
        tp: Dict[str, Any],
        turn_index: int,
        layer_count: int,
        layer_index: Dict[str, int],
        usp: Dict[str, Any],
        usp_tags: List[str],
        usp_window: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        cst = tp.setdefault("cst", {})
        cst["mux"] = {
            "status": {
                "turn_index": turn_index,
                "layer_count": layer_count,
            },
            "layer_index": dict(layer_index),
            "unified_stability_packet": usp,
            "usp_tags": list(usp_tags),
            "history": {
                "window_len": WINDOW_LEN,
                "usp_window": list(usp_window),
            },
            "audit": {
                "slice": "v0.1_pure_pack",
                "provisional_flags": False,
                "notes": [
                    "presence-based flags; no threshold synthesis",
                    "USP for CIL only; not for COB",
                ],
            },
        }

        routing_path = tp.setdefault("routing_path", [])
        if isinstance(routing_path, list) and "cst_mux" not in routing_path:
            routing_path.append("cst_mux")

        return tp

    def process(self, tp: Dict[str, Any], mode: str = "general", **kwargs) -> Dict[str, Any]:
        tp_before = copy.deepcopy(tp) if tp is not None else {}
        tp = copy.deepcopy(tp_before)

        prior_mux = ((tp.get("cst") or {}).get("mux")) or {}
        prior_window = ((prior_mux.get("history") or {}).get("usp_window"))
        if isinstance(prior_window, list):
            self._usp_window = list(prior_window)

        turn_index = (
            tp.get("turn_index")
            or (tp.get("metadata") or {}).get("turn_index")
            or kwargs.get("turn_index")
            or ((self.extract_core(tp).get("status") or {}).get("turn_index"))
            or ((self.extract_ms(tp).get("status") or {}).get("turn_index"))
            or 0
        )
        turn_index = int(turn_index)

        core = self.extract_core(tp)
        ms = self.extract_ms(tp)

        layer_ids = self.collect_layer_ids(core, ms)
        layer_index = self.assign_layer_indices(layer_ids)

        core_pack = self.package_core(core)
        ms_pack = self.package_ms(ms)
        flags = self.package_presence_flags(layer_ids, core, ms)

        new_ctx = bool(
            ((ms.get("metadata") or {}).get("new_context_required"))
            or False
        )

        usp = self.assemble_usp(
            turn_index=turn_index,
            layer_index=layer_index,
            core_pack=core_pack,
            ms_pack=ms_pack,
            flags=flags,
            new_context_required=new_ctx,
        )

        self._usp_window.append(copy.deepcopy(usp))
        if len(self._usp_window) > WINDOW_LEN:
            self._usp_window = self._usp_window[-WINDOW_LEN:]

        tp = self.write_envelope(
            tp,
            turn_index=turn_index,
            layer_count=len(layer_ids),
            layer_index=layer_index,
            usp=usp,
            usp_tags=[],
            usp_window=list(self._usp_window),
        )

        violations = self.write_boundary_guard(tp_before, tp)
        if violations:
            notes = tp["cst"]["mux"]["audit"].setdefault("notes", [])
            for v in violations:
                notes.append(f"WRITE_BOUNDARY: {v}")

        return tp


def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    mux = CST_MUX()
    return mux.process(tp, mode=mode, **kwargs)
