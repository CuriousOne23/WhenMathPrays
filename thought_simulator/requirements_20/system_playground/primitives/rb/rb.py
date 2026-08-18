"""
RB — Relational Basin (Version 1.0)
Aligned with:
  - 20.50_rb_requirements.md (v3.0)
  - rb_py_struc_pgm.md
  - progressive_lineup_testing.md v4.2
  - ts_rb_idob_foundations (RED / regime vocabulary)

Writes only process.routing_filter (+ optional provenance/audit).
Does not mutate TR, tr_needs_update, IdOB, or DCB geometry ownership.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Tuple

PRIMITIVE_NAME = "rb"

# Foundation placeholders (relational model)
H_SMALL = 0.15
H_CRIT = 0.40
A_LOCAL = 0.30
A_NONLOCAL = 0.70

DEFAULT_MAX_FANOUT = 8
DEFAULT_MAX_LANE_DEPTH = 4


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


class RB:
    def __init__(self, tp_input: Optional[dict] = None):
        self.tp = copy.deepcopy(tp_input) if tp_input is not None else {}

    def process(self) -> dict:
        inputs = self._extract_routing_inputs(self.tp)
        route_to_tr = self._tr_gate(inputs)
        candidates = self._select_core_local_obs(inputs)
        candidates = self._apply_bounds(candidates, inputs)
        split_merge = self._arbitrate_split_merge(candidates, inputs)
        firing_order = self._compute_firing_order(candidates)
        rationales = self._transition_rationale(candidates, inputs, route_to_tr)
        red = self._compute_red_fields(inputs)
        rf = self._build_routing_filter(
            candidates, firing_order, rationales, split_merge, inputs, red, route_to_tr
        )
        self._write_routing_filter(rf)
        self._write_provenance_optional(inputs)
        self._append_audit_optional(rf)
        return self.tp

    # ------------------------------------------------------------------
    def _extract_routing_inputs(self, tp: dict) -> dict:
        process = tp.get("process") if isinstance(tp.get("process"), dict) else {}
        routing_metadata = (
            process.get("routing_metadata")
            if isinstance(process.get("routing_metadata"), dict)
            else {}
        )
        foundation = tp.get("_rb_foundation") if isinstance(tp.get("_rb_foundation"), dict) else {}
        delta_h = process.get("deltaH", process.get("delta_h", 0.0))
        try:
            delta_h = float(delta_h)
        except (TypeError, ValueError):
            delta_h = 0.0

        return {
            "tr": tp.get("TR"),
            "tr_needs_update": bool(tp.get("tr_needs_update", False)),
            "delta_h": delta_h,
            "lineage": (tp.get("semantic") or {}).get("lineage") if isinstance(tp.get("semantic"), dict) else None,
            "routing_metadata": routing_metadata,
            "foundation": foundation,
            "semantic": tp.get("semantic"),
            "timestamp": foundation.get("timestamp", 0.0),
        }

    def _tr_gate(self, inputs: dict) -> bool:
        return bool(inputs.get("tr_needs_update"))

    def _select_core_local_obs(self, inputs: dict) -> List[dict]:
        rm = inputs["routing_metadata"]
        core_id = rm.get("core_id")
        ortho = rm.get("orthogonality_signature")
        candidates = rm.get("candidate_obs") or []
        if not isinstance(candidates, list):
            return []

        selected = []
        for ob in candidates:
            if not isinstance(ob, dict):
                continue
            if core_id is not None and ob.get("core_id") != core_id:
                continue
            if ortho is not None and ob.get("orthogonality_signature") != ortho:
                continue
            oid = ob.get("ob_id")
            if oid is None:
                continue
            selected.append(dict(ob))
        return selected

    def _apply_bounds(self, candidates: List[dict], inputs: dict) -> List[dict]:
        rm = inputs["routing_metadata"]
        policy = rm.get("policy") if isinstance(rm.get("policy"), dict) else {}
        max_fanout = int(policy.get("max_ob_fanout", DEFAULT_MAX_FANOUT))
        # stable order before truncate
        ordered = sorted(candidates, key=lambda o: str(o.get("ob_id")))
        return ordered[: max(0, max_fanout)]

    def _arbitrate_split_merge(self, candidates: List[dict], inputs: dict) -> dict:
        rm = inputs["routing_metadata"]
        policy = rm.get("policy") if isinstance(rm.get("policy"), dict) else {}
        allow_merge = bool(policy.get("allow_merge", False))
        allow_split = bool(policy.get("allow_split", False))
        return {
            "merge_eligibility": True if allow_merge else None,
            "split_directive": True if allow_split else None,
        }

    def _compute_firing_order(self, candidates: List[dict]) -> List[str]:
        return sorted(str(c["ob_id"]) for c in candidates)

    def _transition_rationale(
        self, candidates: List[dict], inputs: dict, route_to_tr: bool
    ) -> List[str]:
        rationales = []
        rationales.append("tr_gate:true" if route_to_tr else "tr_gate:false")
        if not candidates:
            rationales.append("no_core_local_obs")
        else:
            rationales.append("core_local_ok")
        return sorted(rationales)

    def _compute_red_fields(self, inputs: dict) -> dict:
        foundation = inputs.get("foundation") or {}
        if not foundation.get("enable_red"):
            return {
                "adjacency_class": None,
                "rt_adj": None,
                "regime_hint": None,
                "displacement_scale": None,
                "route_proposal": None,
            }

        try:
            rt = float(foundation.get("Rt_adj", foundation.get("rt_adj", 0.0)))
        except (TypeError, ValueError):
            rt = 0.0
        try:
            dh = abs(float(foundation.get("delta_H", inputs.get("delta_h", 0.0))))
        except (TypeError, ValueError):
            dh = abs(float(inputs.get("delta_h", 0.0)))

        if rt < A_LOCAL and dh < H_SMALL:
            adjacency_class = "local"
        elif rt > A_NONLOCAL or dh > H_CRIT:
            adjacency_class = "non_local"
        else:
            adjacency_class = "local" if rt <= 0.5 else "non_local"

        if adjacency_class == "local" and dh < H_SMALL:
            displacement_scale = "small"
        elif adjacency_class == "non_local" and dh > H_CRIT:
            displacement_scale = "large"
        else:
            displacement_scale = "medium"

        regime_hint = self._regime_hint(foundation, dh, adjacency_class)

        # Prefer local under Stable/Refinement unless already non_local from hard conditions
        if regime_hint in ("Stable", "Refinement") and not (
            rt > A_NONLOCAL or dh > H_CRIT
        ):
            adjacency_class = "local"
            if dh < H_SMALL:
                displacement_scale = "small"

        # Must not force false local under Transition/Collapse
        if regime_hint in ("Transition", "Collapse") and (rt > A_NONLOCAL or dh > H_CRIT):
            adjacency_class = "non_local"

        route_proposal = foundation.get("route_proposal")

        return {
            "adjacency_class": adjacency_class,
            "rt_adj": rt,
            "regime_hint": regime_hint,
            "displacement_scale": displacement_scale,
            "route_proposal": route_proposal,
        }

    def _regime_hint(self, foundation: dict, dh: float, adjacency_class: str) -> str:
        def f(key, default=0.0):
            try:
                return float(foundation.get(key, default))
            except (TypeError, ValueError):
                return default

        i_stab = f("I_stab")
        r_res = f("R_res")
        p_cont = f("P_cont")

        if i_stab < 0.3 and r_res < 0.3:
            return "Collapse"
        if dh >= H_CRIT or adjacency_class == "non_local" and (rt := f("Rt_adj")) > A_NONLOCAL:
            return "Transition"
        if i_stab < 0.5 or p_cont < 0.4:
            return "Drift"
        if dh < H_SMALL and adjacency_class == "local":
            if i_stab >= 0.7 and r_res >= 0.6:
                return "Stable"
            return "Refinement"
        if i_stab >= 0.7 and r_res >= 0.6 and p_cont >= 0.5:
            return "Stable"
        return "Drift"

    def _build_routing_filter(
        self,
        candidates: List[dict],
        firing_order: List[str],
        rationales: List[str],
        split_merge: dict,
        inputs: dict,
        red: dict,
        route_to_tr: bool,
    ) -> dict:
        selected = sorted(str(c["ob_id"]) for c in candidates)
        return {
            "selected_ob_ids": selected,
            "lane_projections": [],
            "delta_h_routing_context": float(inputs.get("delta_h", 0.0)),
            "firing_order": list(firing_order),
            "transition_rationale": list(rationales),
            "policy_justification": {
                "tr_needs_update": bool(route_to_tr),
                "core_id": inputs["routing_metadata"].get("core_id"),
            },
            "inquiry_escalation": None,
            "merge_eligibility": split_merge.get("merge_eligibility"),
            "split_directive": split_merge.get("split_directive"),
            "adjacency_class": red.get("adjacency_class"),
            "rt_adj": red.get("rt_adj"),
            "regime_hint": red.get("regime_hint"),
            "displacement_scale": red.get("displacement_scale"),
            "route_proposal": red.get("route_proposal"),
        }

    def _write_routing_filter(self, rf: dict) -> None:
        process = self.tp.setdefault("process", {})
        if not isinstance(process, dict):
            self.tp["process"] = {}
            process = self.tp["process"]
        process["routing_filter"] = rf

    def _write_provenance_optional(self, inputs: dict) -> None:
        meta = self.tp.setdefault("metadata", {})
        if not isinstance(meta, dict):
            self.tp["metadata"] = {}
            meta = self.tp["metadata"]
        prov = meta.setdefault("provenance", {})
        if not isinstance(prov, dict):
            meta["provenance"] = {}
            prov = meta["provenance"]
        ts = inputs.get("timestamp", 0.0)
        try:
            prov["rb_last_update"] = float(ts)
        except (TypeError, ValueError):
            prov["rb_last_update"] = 0.0

    def _append_audit_optional(self, rf: dict) -> None:
        self.tp.setdefault("exec_trace", [])
        if not isinstance(self.tp["exec_trace"], list):
            self.tp["exec_trace"] = []
        self.tp["exec_trace"].append(
            {
                "rb_ref": {
                    "origin": "RB",
                    "last_update": "RB",
                    "selected_count": len(rf.get("selected_ob_ids") or []),
                    "adjacency_class": rf.get("adjacency_class"),
                }
            }
        )


def run(tp: dict) -> dict:
    return RB(tp).process()
