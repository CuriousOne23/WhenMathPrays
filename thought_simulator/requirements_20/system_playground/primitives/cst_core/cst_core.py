"""
CST-Core — Conversation Stability Tracker (Core)
System Playground Version 0.1

Aligned with:
- 20.32.010.010_cst-core.md
- cst-core_requirements.md
- cst_core_py_struc_pgm.md
- patha_field_names.md (TP.cst.core lock)
- progressive_lineup_testing.md

Provisional metrics are deterministic stubs (audit.provisional_metrics=true).
Final distance/ambiguity/collapse formulas remain Defer.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple
import copy


PRIMITIVE_NAME = "cst_core"

# v0.1 provisional thresholds (not normative physics)
THRESH_FREEZE = 1.0
THRESH_THAW = 0.2
THRESH_COMPONENT_EMIT = 0.5
THRESH_CONTINUITY = 0.8
HISTORY_WINDOW = 10


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


def _empty_signals() -> Dict[str, Any]:
    return {
        "freeze": {"frozen_objects": [], "reason": ""},
        "thaw": {"thawed_objects": [], "reason": ""},
        "continuity_restoration": {"restored_objects": [], "reason": ""},
        "drift": {"affected_objects": [], "magnitude": 0.0},
        "oscillation": {"affected_objects": [], "frequency": 0.0, "amplitude": 0},
        "ambiguity": {"affected_objects": [], "increased": [], "decreased": []},
        "collapse": {"collapsed_objects": [], "severity": 0},
    }


def _as_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _sorted_ids(ids: List[str]) -> List[str]:
    return sorted(ids)


class CST:
    """Stateful CST-Core metric generator. History may also ride on TP for replay."""

    def __init__(self):
        self._history_turns: List[Dict[str, Any]] = []
        self._frozen_layers: Set[str] = set()
        self._prev_snapshots: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Extraction
    # ------------------------------------------------------------------

    @staticmethod
    def extract_layers(tp: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Read identity layers from COB snapshot (read-only)."""
        identity = tp.get("identity") or {}
        snap = identity.get("cob_state_snapshot") or {}
        objects = snap.get("objects") or []
        if not objects and isinstance(tp.get("layers"), list):
            objects = tp["layers"]
        return list(objects)

    @staticmethod
    def extract_lineage_log(tp: Dict[str, Any]) -> List[Dict[str, Any]]:
        log = tp.get("lineage_log") or []
        return list(log) if isinstance(log, list) else []

    @staticmethod
    def build_layer_snapshot(obj: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "layer_id": obj.get("id") or obj.get("layer_id"),
            "referent_map": obj.get("referent_map"),
            "anchors": obj.get("anchors") or [],
            "lineage": obj.get("lineage") or {},
            "register": obj.get("register"),
            "importance": obj.get("importance"),
            "stability_metrics": dict(obj.get("stability_metrics") or {}),
            "ambiguity": dict(obj.get("ambiguity") or {}),
            "frozen": bool((obj.get("stability_metrics") or {}).get("frozen")),
        }

    # ------------------------------------------------------------------
    # MERGE/SPLIT hygiene
    # ------------------------------------------------------------------

    @staticmethod
    def merge_split_excluded_parents(lineage_log: List[Dict[str, Any]]) -> Set[str]:
        excluded: Set[str] = set()
        for ev in lineage_log:
            if not isinstance(ev, dict):
                continue
            et = ev.get("event_type")
            if et in ("MERGE", "SPLIT"):
                parents = ev.get("parent_ref") or []
                if isinstance(parents, str):
                    parents = [parents]
                for p in parents:
                    if p is not None:
                        excluded.add(str(p))
        return excluded

    # ------------------------------------------------------------------
    # Provisional metrics
    # ------------------------------------------------------------------

    def compute_layer_metrics(
        self,
        snap: Dict[str, Any],
        prev: Optional[Dict[str, Any]],
        excluded: Set[str],
    ) -> Dict[str, float]:
        lid = snap.get("layer_id")
        sm = snap.get("stability_metrics") or {}
        amb = snap.get("ambiguity") or {}

        # Priority 1: fixture-injected metrics
        drift = _as_float(sm.get("drift"), 0.0)
        oscillation = _as_float(sm.get("oscillation"), 0.0)
        collapse_flag = sm.get("collapse")
        collapse = _as_float(collapse_flag, 0.0)

        # Priority 2: simple structural delta vs previous snapshot
        if prev is not None:
            if snap.get("referent_map") != prev.get("referent_map"):
                drift = max(drift, 1.0)
            if snap.get("anchors") != prev.get("anchors"):
                oscillation = max(oscillation, 0.5)

        # Ambiguity provisional
        ambiguity = 0.0
        if amb.get("ambiguity") == "high" or amb.get("certainty") == "low":
            ambiguity = 1.0
        elif amb.get("ambiguity") == "low" or amb.get("certainty") == "high":
            ambiguity = 0.0
        else:
            ambiguity = _as_float(amb.get("ambiguity"), 0.0)

        continuity = 1.0 - min(1.0, max(drift, oscillation, ambiguity, collapse))
        combined = max(drift, oscillation, ambiguity, collapse)

        if lid in excluded:
            # Structural parents: suppress false instability attribution
            collapse = 0.0
            combined = min(combined, THRESH_COMPONENT_EMIT - 0.01)

        stability = 1.0 - combined

        return {
            "drift": drift,
            "oscillation": oscillation,
            "ambiguity": ambiguity,
            "stability": stability,
            "collapse": collapse,
            "continuity": continuity,
            "combined_instability": combined,
        }

    def decide_signals(
        self,
        per_layer: Dict[str, Dict[str, float]],
        layer_snaps: Dict[str, Dict[str, Any]],
        excluded: Set[str],
    ) -> Dict[str, Any]:
        signals = _empty_signals()

        drift_ids: List[str] = []
        osc_ids: List[str] = []
        amb_inc: List[str] = []
        amb_dec: List[str] = []
        amb_aff: List[str] = []
        col_ids: List[str] = []
        freeze_ids: List[str] = []
        thaw_ids: List[str] = []
        restore_ids: List[str] = []

        max_drift = 0.0
        max_osc = 0.0
        col_severity = 0

        for lid in _sorted_ids(list(per_layer.keys())):
            m = per_layer[lid]
            snap = layer_snaps.get(lid) or {}
            was_frozen = lid in self._frozen_layers or bool(snap.get("frozen"))

            # Local freeze policy: if frozen, skip metric-driven emission updates
            # except thaw/recovery checks against combined
            combined = m["combined_instability"]

            if m["drift"] >= THRESH_COMPONENT_EMIT and lid not in excluded:
                drift_ids.append(lid)
                max_drift = max(max_drift, m["drift"])

            if m["oscillation"] >= THRESH_COMPONENT_EMIT and lid not in excluded:
                osc_ids.append(lid)
                max_osc = max(max_osc, m["oscillation"])

            if m["ambiguity"] >= THRESH_COMPONENT_EMIT:
                amb_aff.append(lid)
                amb_inc.append(lid)
            elif m["ambiguity"] <= 0.0 and lid in (snap.get("stability_metrics") or {}):
                # low ambiguity path
                amb_dec.append(lid)

            if m["collapse"] >= THRESH_COMPONENT_EMIT and lid not in excluded:
                col_ids.append(lid)
                col_severity += 1

            if combined >= THRESH_FREEZE:
                freeze_ids.append(lid)
                self._frozen_layers.add(lid)
            elif was_frozen and combined <= THRESH_THAW:
                thaw_ids.append(lid)
                self._frozen_layers.discard(lid)

            if m["continuity"] >= THRESH_CONTINUITY and was_frozen is False:
                # Optional continuity restore when high continuity after instability window
                # v0.1: only emit if previously had high combined and now recovered
                prev = self._prev_snapshots.get(lid)
                if prev is not None:
                    prev_sm = prev.get("stability_metrics") or {}
                    prev_combined = max(
                        _as_float(prev_sm.get("drift")),
                        _as_float(prev_sm.get("oscillation")),
                        _as_float(prev_sm.get("collapse")),
                    )
                    if prev_combined >= THRESH_COMPONENT_EMIT and m["continuity"] >= THRESH_CONTINUITY:
                        restore_ids.append(lid)

        signals["drift"] = {
            "affected_objects": drift_ids,
            "magnitude": max_drift,
        }
        signals["oscillation"] = {
            "affected_objects": osc_ids,
            "frequency": max_osc,
            "amplitude": len(osc_ids),
        }
        signals["ambiguity"] = {
            "affected_objects": amb_aff,
            "increased": amb_inc,
            "decreased": amb_dec,
        }
        signals["collapse"] = {
            "collapsed_objects": col_ids,
            "severity": col_severity,
        }
        signals["freeze"] = {
            "frozen_objects": freeze_ids,
            "reason": "combined_instability_threshold" if freeze_ids else "",
        }
        signals["thaw"] = {
            "thawed_objects": thaw_ids,
            "reason": "recovery_threshold" if thaw_ids else "",
        }
        signals["continuity_restoration"] = {
            "restored_objects": restore_ids,
            "reason": "continuity_threshold" if restore_ids else "",
        }
        return signals

    def lineage_stability(
        self, layer_snaps: Dict[str, Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        stable: List[str] = []
        unstable: List[str] = []
        for lid in _sorted_ids(list(layer_snaps.keys())):
            lin = (layer_snaps[lid].get("lineage") or {})
            st = lin.get("stability")
            if st == "stable":
                stable.append(lid)
            elif st == "unstable":
                unstable.append(lid)
        return {"stable_lineage": stable, "unstable_lineage": unstable}

    def update_history(self, turn_index: int, metric_summary: Dict[str, Any]) -> Dict[str, Any]:
        entry = {
            "turn_index": turn_index,
            "per_layer_snapshot_ref_or_digest": None,
            "metric_summary": metric_summary,
        }
        self._history_turns.append(entry)
        if len(self._history_turns) > HISTORY_WINDOW:
            self._history_turns = self._history_turns[-HISTORY_WINDOW:]
        return {
            "window_len": HISTORY_WINDOW,
            "turns": list(self._history_turns),
        }

    # ------------------------------------------------------------------
    # Envelope write
    # ------------------------------------------------------------------

    def write_envelope(
        self,
        tp: Dict[str, Any],
        turn_index: int,
        layer_count: int,
        signals: Dict[str, Any],
        per_layer: Dict[str, Dict[str, float]],
        history: Dict[str, Any],
        lineage_stability: Dict[str, List[str]],
    ) -> Dict[str, Any]:
        cst = tp.setdefault("cst", {})
        core = {
            "status": {
                "turn_index": turn_index,
                "layer_count": layer_count,
                "frozen_layers": _sorted_ids(list(self._frozen_layers)),
            },
            "signals": signals,
            "metrics": {
                "per_layer": per_layer,
                "integrated": {},
            },
            "history": history,
            "lineage_stability": lineage_stability,
            "audit": {
                "slice": "v0.1_provisional",
                "provisional_metrics": True,
                "notes": [
                    "provisional deterministic stubs; final formulas Defer",
                ],
            },
        }
        cst["core"] = core

        routing_path = tp.setdefault("routing_path", [])
        if isinstance(routing_path, list) and "cst_core" not in routing_path:
            routing_path.append("cst_core")

        return tp

    @staticmethod
    def write_boundary_guard(tp_before: Dict[str, Any], tp_after: Dict[str, Any]) -> List[str]:
        errors: List[str] = []
        # Must not mutate cob_state_snapshot
        before_snap = ((tp_before.get("identity") or {}).get("cob_state_snapshot"))
        after_snap = ((tp_after.get("identity") or {}).get("cob_state_snapshot"))
        if before_snap is not None and after_snap != before_snap:
            errors.append("cob_state_snapshot mutated by cst_core")

        for forbidden in ("routing_filter", "geometric_state", "semantic_core"):
            if forbidden in tp_after and forbidden not in tp_before:
                errors.append(f"forbidden field written: {forbidden}")

        # Must not write CIL packet
        if "cil" in tp_after and "cil" not in tp_before:
            errors.append("cil envelope written by cst_core")

        return errors

    # ------------------------------------------------------------------
    # process
    # ------------------------------------------------------------------

    def process(self, tp: Dict[str, Any], mode: str = "general", **kwargs) -> Dict[str, Any]:
        tp_before = copy.deepcopy(tp) if tp is not None else {}
        tp = copy.deepcopy(tp_before)

        # Restore history from TP when present (replay-friendly)
        prior_core = ((tp.get("cst") or {}).get("core") or {})
        prior_hist = (prior_core.get("history") or {}).get("turns")
        if isinstance(prior_hist, list):
            self._history_turns = list(prior_hist)
        prior_frozen = (prior_core.get("status") or {}).get("frozen_layers") or []
        if prior_frozen:
            self._frozen_layers = set(str(x) for x in prior_frozen)

        turn_index = (
            tp.get("turn_index")
            or (tp.get("metadata") or {}).get("turn_index")
            or kwargs.get("turn_index")
            or 0
        )

        layers = self.extract_layers(tp)
        lineage_log = self.extract_lineage_log(tp)
        excluded = self.merge_split_excluded_parents(lineage_log)

        layer_snaps: Dict[str, Dict[str, Any]] = {}
        per_layer: Dict[str, Dict[str, float]] = {}

        for obj in layers:
            snap = self.build_layer_snapshot(obj)
            lid = snap.get("layer_id")
            if not lid:
                continue
            lid = str(lid)
            # Skip metric update for frozen layers (local freeze policy)
            if lid in self._frozen_layers and not kwargs.get("force_update_frozen"):
                # Keep last metrics if available
                prev_m = ((prior_core.get("metrics") or {}).get("per_layer") or {}).get(lid)
                if prev_m:
                    per_layer[lid] = dict(prev_m)
                else:
                    per_layer[lid] = self.compute_layer_metrics(snap, self._prev_snapshots.get(lid), excluded)
            else:
                per_layer[lid] = self.compute_layer_metrics(snap, self._prev_snapshots.get(lid), excluded)
            layer_snaps[lid] = snap

        signals = self.decide_signals(per_layer, layer_snaps, excluded)
        lin_stab = self.lineage_stability(layer_snaps)

        metric_summary = {
            lid: {
                "combined_instability": m["combined_instability"],
                "drift": m["drift"],
                "collapse": m["collapse"],
            }
            for lid, m in per_layer.items()
        }
        history = self.update_history(int(turn_index), metric_summary)

        # Update prev snapshots for next turn
        self._prev_snapshots = {lid: copy.deepcopy(s) for lid, s in layer_snaps.items()}

        tp = self.write_envelope(
            tp,
            turn_index=int(turn_index),
            layer_count=len(layer_snaps),
            signals=signals,
            per_layer=per_layer,
            history=history,
            lineage_stability=lin_stab,
        )

        # Soft guard: record violations under audit.notes in general; tests assert hard
        violations = self.write_boundary_guard(tp_before, tp)
        if violations:
            notes = tp["cst"]["core"]["audit"].setdefault("notes", [])
            for v in violations:
                notes.append(f"WRITE_BOUNDARY: {v}")

        return tp


def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    """Module-level entry matching progressive / structural-program contract."""
    cst = CST()
    return cst.process(tp, mode=mode, **kwargs)
