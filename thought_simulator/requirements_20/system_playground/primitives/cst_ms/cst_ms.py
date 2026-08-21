"""
CST-MS — Metric Synthesis Module
System Playground Version 0.1

Aligned with:
- 20.32.010.020_cst-ms.md
- cst-ms_requirements.md
- cst_ms_py_struc_pgm.md
- patha_field_names.md (TP.cst.ms lock)
- progressive_lineup_testing.md

Provisional weights/thresholds are deterministic stubs
(audit.provisional_metrics=true). Final tables remain Defer.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple
import copy


PRIMITIVE_NAME = "cst_ms"

# v0.1 provisional constants (heritage-aligned)
WEIGHTS = {
    "drift": 0.25,
    "oscillation": 0.25,
    "ambiguity": 0.25,
    "collapse": 0.25,
    "continuity": 0.25,
}
MAXIMA = {
    "drift": 1.0,
    "oscillation": 1.0,
    "ambiguity": 1.0,
    "collapse": 1.0,
    "continuity": 1.0,
}
WINDOW_LEN = 10
THRESH_FREEZE = 0.5
THRESH_THAW = 0.5
THRESH_COLLAPSE_RECOVERY = 0.5
THRESH_CONTINUITY_BREAK = 0.40
THRESH_INSTABILITY_TREND = 0.60
THRESH_COLLAPSE_SPIKE = 0.50
THRESH_AMBIGUITY_SPIKE = 3
THRESH_FREEZE_SPIKE = 0.50
THRESH_FRAGMENT_CONTINUITY = 0.75


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


def _as_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clip01(x: float) -> float:
    return max(0.0, min(1.0, x))


def _empty_commands() -> Dict[str, Any]:
    return {
        "freeze": {"layers": [], "reason": ""},
        "thaw": {"layers": [], "reason": ""},
        "collapse_recovery": {"layers": [], "reason": ""},
        "create_identity_layer": {"requests": []},
        "split": {"layers": [], "reason": ""},
        "merge": {"pairs": [], "reason": ""},
    }


class CST_MS:
    """Stateful CST-MS synthesizer; window may also ride on TP for replay."""

    def __init__(self):
        self._stability_window: List[Dict[str, Any]] = []
        self._command_log: List[Dict[str, Any]] = []
        self._frozen_layers: Set[str] = set()

    # ------------------------------------------------------------------
    # Extraction
    # ------------------------------------------------------------------

    @staticmethod
    def extract_core(tp: Dict[str, Any]) -> Dict[str, Any]:
        return ((tp.get("cst") or {}).get("core")) or {}

    @staticmethod
    def extract_lineage_log(tp: Dict[str, Any]) -> List[Dict[str, Any]]:
        log = tp.get("lineage_log") or []
        return list(log) if isinstance(log, list) else []

    @staticmethod
    def structural_event_present(lineage_log: List[Dict[str, Any]]) -> bool:
        for ev in lineage_log:
            if isinstance(ev, dict) and ev.get("event_type") in ("MERGE", "SPLIT"):
                return True
        return False

    def gather_aggregate_raw(self, core: Dict[str, Any]) -> Dict[str, float]:
        signals = core.get("signals") or {}
        metrics = (core.get("metrics") or {}).get("per_layer") or {}

        drift = _as_float((signals.get("drift") or {}).get("magnitude"))
        osc = _as_float((signals.get("oscillation") or {}).get("frequency"))
        amb_sig = signals.get("ambiguity") or {}
        amb_count = len(amb_sig.get("increased") or [])
        collapse = _as_float((signals.get("collapse") or {}).get("severity"))

        # Prefer mean of per_layer metrics when present
        if metrics:
            drifts, oscs, ambs, cols, conts = [], [], [], [], []
            for lid in sorted(metrics.keys()):
                m = metrics[lid] or {}
                drifts.append(_as_float(m.get("drift")))
                oscs.append(_as_float(m.get("oscillation")))
                ambs.append(_as_float(m.get("ambiguity")))
                cols.append(_as_float(m.get("collapse")))
                conts.append(_as_float(m.get("continuity"), default=-1.0))
            if drifts:
                drift = sum(drifts) / len(drifts)
            if oscs:
                osc = sum(oscs) / len(oscs)
            if ambs:
                amb_from_layer = sum(ambs) / len(ambs)
            else:
                amb_from_layer = 0.0
            if cols:
                collapse = sum(cols) / len(cols)
            continuity_from_layer = None
            valid_c = [c for c in conts if c >= 0.0]
            if valid_c:
                continuity_from_layer = sum(valid_c) / len(valid_c)
        else:
            amb_from_layer = float(amb_count)
            continuity_from_layer = None

        amb_raw = max(float(amb_count), amb_from_layer)
        if continuity_from_layer is None:
            continuity_raw = 1.0 - _clip01(collapse)
        else:
            continuity_raw = continuity_from_layer

        return {
            "drift": drift,
            "oscillation": osc,
            "ambiguity": amb_raw,
            "collapse": collapse,
            "continuity": continuity_raw,
            "ambiguity_count": float(amb_count),
            "oscillation_amplitude": _as_float(
                (signals.get("oscillation") or {}).get("amplitude")
            ),
        }

    def gather_per_layer_raw(self, core: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        metrics = (core.get("metrics") or {}).get("per_layer") or {}
        out: Dict[str, Dict[str, float]] = {}
        for lid in sorted(metrics.keys()):
            m = metrics[lid] or {}
            collapse = _as_float(m.get("collapse"))
            cont = m.get("continuity")
            continuity = _as_float(cont) if cont is not None else (1.0 - _clip01(collapse))
            out[str(lid)] = {
                "drift": _as_float(m.get("drift")),
                "oscillation": _as_float(m.get("oscillation")),
                "ambiguity": _as_float(m.get("ambiguity")),
                "collapse": collapse,
                "continuity": continuity,
            }
        return out

    # ------------------------------------------------------------------
    # Normalize / weight / synthesize
    # ------------------------------------------------------------------

    def normalize_one(self, raw: Dict[str, float]) -> Dict[str, float]:
        nm = {}
        for key in ("drift", "oscillation", "ambiguity", "collapse", "continuity"):
            mx = MAXIMA.get(key, 1.0) or 1.0
            nm[key] = _clip01(_as_float(raw.get(key)) / mx)
        return nm

    def weight_one(self, nm: Dict[str, float]) -> Dict[str, float]:
        return {k: nm[k] * WEIGHTS.get(k, 1.0) for k in nm}

    def synthesize_one(self, wm: Dict[str, float]) -> Tuple[float, float, float, float, float]:
        stability = _clip01(sum(wm.values()))
        instability = _clip01(1.0 - stability)
        collapse_risk = _clip01(wm.get("collapse", 0.0))
        freeze_risk = _clip01(wm.get("ambiguity", 0.0) + wm.get("collapse", 0.0))
        thaw_readiness = _clip01(wm.get("continuity", 0.0))
        return stability, instability, collapse_risk, freeze_risk, thaw_readiness

    # ------------------------------------------------------------------
    # Commands / window / new context
    # ------------------------------------------------------------------

    def decide_commands(
        self,
        turn_index: int,
        per_layer_scores: Dict[str, Dict[str, float]],
        agg_scores: Dict[str, float],
        new_context_required: bool,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        commands = _empty_commands()
        log_additions: List[Dict[str, Any]] = []

        freeze_layers: List[str] = []
        thaw_layers: List[str] = []
        collapse_layers: List[str] = []

        if per_layer_scores:
            for lid in sorted(per_layer_scores.keys()):
                s = per_layer_scores[lid]
                fr = s["freeze_risk"]
                tr = s["thaw_readiness"]
                cr = s["collapse_risk"]
                if fr >= THRESH_FREEZE:
                    freeze_layers.append(lid)
                    self._frozen_layers.add(lid)
                elif lid in self._frozen_layers and tr >= THRESH_THAW:
                    thaw_layers.append(lid)
                    self._frozen_layers.discard(lid)
                if cr >= THRESH_COLLAPSE_RECOVERY:
                    collapse_layers.append(lid)
        else:
            # aggregate-only path
            if agg_scores["freeze_risk"] >= THRESH_FREEZE:
                freeze_layers.append("__aggregate__")
            if agg_scores["thaw_readiness"] >= THRESH_THAW and self._frozen_layers:
                thaw_layers.extend(sorted(self._frozen_layers))
                self._frozen_layers.clear()
            if agg_scores["collapse_risk"] >= THRESH_COLLAPSE_RECOVERY:
                collapse_layers.append("__aggregate__")

        if freeze_layers:
            commands["freeze"] = {
                "layers": freeze_layers,
                "reason": "freeze_risk_threshold",
            }
            log_additions.append(
                {
                    "turn_index": turn_index,
                    "command_type": "freeze",
                    "targets": freeze_layers,
                    "reason": "freeze_risk_threshold",
                    "metrics_snapshot_ref": None,
                }
            )
        if thaw_layers:
            commands["thaw"] = {
                "layers": thaw_layers,
                "reason": "thaw_readiness_threshold",
            }
            log_additions.append(
                {
                    "turn_index": turn_index,
                    "command_type": "thaw",
                    "targets": thaw_layers,
                    "reason": "thaw_readiness_threshold",
                    "metrics_snapshot_ref": None,
                }
            )
        if collapse_layers:
            commands["collapse_recovery"] = {
                "layers": collapse_layers,
                "reason": "collapse_risk_threshold",
            }
            log_additions.append(
                {
                    "turn_index": turn_index,
                    "command_type": "collapse_recovery",
                    "targets": collapse_layers,
                    "reason": "collapse_risk_threshold",
                    "metrics_snapshot_ref": None,
                }
            )

        # create linked optionally to new_context_required (structural program §4.4)
        if new_context_required:
            commands["create_identity_layer"] = {
                "requests": [{"reason": "new_context_required"}],
            }
            log_additions.append(
                {
                    "turn_index": turn_index,
                    "command_type": "create_identity_layer",
                    "targets": ["new_context"],
                    "reason": "new_context_required",
                    "metrics_snapshot_ref": None,
                }
            )

        # split/merge Defer — empty shells
        return commands, log_additions

    def detect_new_context(
        self,
        nm: Dict[str, float],
        scores: Dict[str, float],
        ambiguity_count: int,
        structural_event: bool,
    ) -> bool:
        continuity_break = nm.get("continuity", 1.0) < THRESH_CONTINUITY_BREAK
        if self._stability_window:
            avg_inst = sum(
                _as_float((e.get("instability") or {}).get("value"))
                for e in self._stability_window
            ) / len(self._stability_window)
        else:
            avg_inst = 0.0
        instability_trend = avg_inst > THRESH_INSTABILITY_TREND
        collapse_spike = scores["collapse_risk"] > THRESH_COLLAPSE_SPIKE
        ambiguity_spike = ambiguity_count > THRESH_AMBIGUITY_SPIKE
        freeze_spike = scores["freeze_risk"] > THRESH_FREEZE_SPIKE
        fragmentation = structural_event and nm.get("continuity", 1.0) < THRESH_FRAGMENT_CONTINUITY
        return bool(
            continuity_break
            or instability_trend
            or collapse_spike
            or ambiguity_spike
            or freeze_spike
            or fragmentation
        )

    def update_window(self, turn_index: int, scores: Dict[str, float]) -> List[Dict[str, Any]]:
        entry = {
            "turn_index": turn_index,
            "stability": {"value": scores["stability"]},
            "instability": {"value": scores["instability"]},
            "collapse_risk": {"value": scores["collapse_risk"]},
            "freeze_risk": {"value": scores["freeze_risk"]},
            "thaw_readiness": {"value": scores["thaw_readiness"]},
        }
        self._stability_window.append(entry)
        if len(self._stability_window) > WINDOW_LEN:
            self._stability_window = self._stability_window[-WINDOW_LEN:]
        return list(self._stability_window)

    @staticmethod
    def write_boundary_guard(tp_before: Dict[str, Any], tp_after: Dict[str, Any]) -> List[str]:
        errors: List[str] = []
        before_snap = ((tp_before.get("identity") or {}).get("cob_state_snapshot"))
        after_snap = ((tp_after.get("identity") or {}).get("cob_state_snapshot"))
        if before_snap is not None and after_snap != before_snap:
            errors.append("cob_state_snapshot mutated by cst_ms")

        before_core = ((tp_before.get("cst") or {}).get("core"))
        after_core = ((tp_after.get("cst") or {}).get("core"))
        if before_core is not None and after_core != before_core:
            errors.append("TP.cst.core mutated by cst_ms")

        for forbidden in ("routing_filter", "geometric_state", "semantic_core"):
            if forbidden in tp_after and forbidden not in tp_before:
                errors.append(f"forbidden field written: {forbidden}")

        if "cil" in tp_after and "cil" not in tp_before:
            errors.append("cil envelope written by cst_ms")

        return errors

    def write_envelope(
        self,
        tp: Dict[str, Any],
        turn_index: int,
        layer_count: int,
        nm_agg: Dict[str, float],
        wm_agg: Dict[str, float],
        scores_agg: Dict[str, float],
        per_layer_nm: Dict[str, Dict[str, float]],
        per_layer_wm: Dict[str, Dict[str, float]],
        per_layer_scores: Dict[str, Dict[str, float]],
        ambiguity_count: int,
        drift_magnitude: float,
        osc_freq: float,
        osc_amp: float,
        commands: Dict[str, Any],
        command_log: List[Dict[str, Any]],
        new_context_required: bool,
        window: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        cst = tp.setdefault("cst", {})

        def pack_scores(s: Dict[str, float]) -> Dict[str, Dict[str, float]]:
            return {
                "stability": {"value": s["stability"]},
                "instability": {"value": s["instability"]},
                "collapse_risk": {"value": s["collapse_risk"]},
                "freeze_risk": {"value": s["freeze_risk"]},
                "thaw_readiness": {"value": s["thaw_readiness"]},
            }

        per_stability = {lid: {"value": s["stability"]} for lid, s in per_layer_scores.items()}
        per_instability = {lid: {"value": s["instability"]} for lid, s in per_layer_scores.items()}
        per_collapse = {lid: {"value": s["collapse_risk"]} for lid, s in per_layer_scores.items()}
        per_freeze = {lid: {"value": s["freeze_risk"]} for lid, s in per_layer_scores.items()}
        per_thaw = {lid: {"value": s["thaw_readiness"]} for lid, s in per_layer_scores.items()}

        ms = {
            "status": {
                "turn_index": turn_index,
                "layer_count": layer_count,
            },
            "normalized_metrics": {
                "per_layer": per_layer_nm,
                "aggregate": {
                    k: nm_agg[k]
                    for k in ("drift", "oscillation", "ambiguity", "collapse", "continuity")
                },
            },
            "weighted_metrics": {
                "per_layer": per_layer_wm,
                "aggregate": {
                    k: wm_agg[k]
                    for k in ("drift", "oscillation", "ambiguity", "collapse", "continuity")
                },
            },
            "stability": {
                "per_layer": per_stability,
                "aggregate": {"value": scores_agg["stability"]},
            },
            "instability": {
                "per_layer": per_instability,
                "aggregate": {"value": scores_agg["instability"]},
            },
            "collapse_risk": {
                "per_layer": per_collapse,
                "aggregate": {"value": scores_agg["collapse_risk"]},
            },
            "freeze_risk": {
                "per_layer": per_freeze,
                "aggregate": {"value": scores_agg["freeze_risk"]},
            },
            "thaw_readiness": {
                "per_layer": per_thaw,
                "aggregate": {"value": scores_agg["thaw_readiness"]},
            },
            "ambiguity_summary": {"count": int(ambiguity_count)},
            "drift_summary": {"magnitude": drift_magnitude},
            "oscillation_summary": {
                "frequency": osc_freq,
                "amplitude": osc_amp,
            },
            "commands": commands,
            "command_log": command_log,
            "diagnostics": {
                "sync_mismatch": False,
                "sync_mismatch_detail": None,
            },
            "metadata": {
                "new_context_required": bool(new_context_required),
            },
            "stability_window": window,
            "history": {"window_len": WINDOW_LEN},
            "audit": {
                "slice": "v0.1_provisional",
                "provisional_metrics": True,
                "notes": [
                    "provisional weights/thresholds; final tables Defer",
                    "split/merge command predicates Defer (empty shells)",
                ],
            },
        }
        cst["ms"] = ms

        routing_path = tp.setdefault("routing_path", [])
        if isinstance(routing_path, list) and "cst_ms" not in routing_path:
            routing_path.append("cst_ms")

        return tp

    def process(self, tp: Dict[str, Any], mode: str = "general", **kwargs) -> Dict[str, Any]:
        tp_before = copy.deepcopy(tp) if tp is not None else {}
        tp = copy.deepcopy(tp_before)

        prior_ms = ((tp.get("cst") or {}).get("ms")) or {}
        prior_window = prior_ms.get("stability_window")
        if isinstance(prior_window, list):
            self._stability_window = list(prior_window)
        prior_log = prior_ms.get("command_log")
        if isinstance(prior_log, list):
            self._command_log = list(prior_log)

        turn_index = (
            tp.get("turn_index")
            or (tp.get("metadata") or {}).get("turn_index")
            or kwargs.get("turn_index")
            or ((self.extract_core(tp).get("status") or {}).get("turn_index"))
            or 0
        )
        turn_index = int(turn_index)

        core = self.extract_core(tp)
        lineage_log = self.extract_lineage_log(tp)
        structural = self.structural_event_present(lineage_log)

        raw_agg = self.gather_aggregate_raw(core)
        per_raw = self.gather_per_layer_raw(core)

        # MERGE/SPLIT neutrality: structural event alone does not force instability;
        # metrics still flow from Core. No extra inflation here.

        nm_agg = self.normalize_one(raw_agg)
        wm_agg = self.weight_one(nm_agg)
        st, inst, cr, fr, tr = self.synthesize_one(wm_agg)
        scores_agg = {
            "stability": st,
            "instability": inst,
            "collapse_risk": cr,
            "freeze_risk": fr,
            "thaw_readiness": tr,
        }

        per_layer_nm: Dict[str, Dict[str, float]] = {}
        per_layer_wm: Dict[str, Dict[str, float]] = {}
        per_layer_scores: Dict[str, Dict[str, float]] = {}
        for lid in sorted(per_raw.keys()):
            nm = self.normalize_one(per_raw[lid])
            wm = self.weight_one(nm)
            s, i, c, f, t = self.synthesize_one(wm)
            per_layer_nm[lid] = nm
            per_layer_wm[lid] = wm
            per_layer_scores[lid] = {
                "stability": s,
                "instability": i,
                "collapse_risk": c,
                "freeze_risk": f,
                "thaw_readiness": t,
            }

        ambiguity_count = int(raw_agg.get("ambiguity_count", 0))
        # detect new context BEFORE appending current window entry (heritage uses prior window for trend)
        new_ctx = self.detect_new_context(nm_agg, scores_agg, ambiguity_count, structural)

        commands, log_add = self.decide_commands(
            turn_index, per_layer_scores, scores_agg, new_ctx
        )
        self._command_log.extend(log_add)

        window = self.update_window(turn_index, scores_agg)

        signals = core.get("signals") or {}
        drift_mag = _as_float((signals.get("drift") or {}).get("magnitude"), raw_agg["drift"])
        osc_freq = _as_float((signals.get("oscillation") or {}).get("frequency"), raw_agg["oscillation"])
        osc_amp = _as_float((signals.get("oscillation") or {}).get("amplitude"), raw_agg["oscillation_amplitude"])

        tp = self.write_envelope(
            tp,
            turn_index=turn_index,
            layer_count=len(per_raw),
            nm_agg=nm_agg,
            wm_agg=wm_agg,
            scores_agg=scores_agg,
            per_layer_nm=per_layer_nm,
            per_layer_wm=per_layer_wm,
            per_layer_scores=per_layer_scores,
            ambiguity_count=ambiguity_count,
            drift_magnitude=drift_mag,
            osc_freq=osc_freq,
            osc_amp=osc_amp,
            commands=commands,
            command_log=list(self._command_log),
            new_context_required=new_ctx,
            window=window,
        )

        violations = self.write_boundary_guard(tp_before, tp)
        if violations:
            notes = tp["cst"]["ms"]["audit"].setdefault("notes", [])
            for v in violations:
                notes.append(f"WRITE_BOUNDARY: {v}")

        return tp


def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    ms = CST_MS()
    return ms.process(tp, mode=mode, **kwargs)
