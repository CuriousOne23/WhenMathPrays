"""
TR — Thought Router (Version 1.0)
Aligned with:
  - 20.37 (v3.0)
  - tr_py_struc_pgm.md
  - progressive_lineup_testing.md v4.2
  - TR theory suite (readset, mapping families, geometry)

Exclusive writer of TP.TR. Runs only when tr_needs_update is True.
Clears dirty flag after successful write. Narrow 20.37 read-set +
optional _tr_diagnostics enrichment. Deterministic omission defaults.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional

PRIMITIVE_NAME = "tr"

LINEAGE_BOUND_K = 3

ROUTING_FIELDS_KEYS = (
    "semantic_drift",
    "identity_drift",
    "commitment_instability",
    "freeze_conflict",
    "topology_instability",
    "curvature_level",
    "stance_instability",
    "shading_instability",
    "tension_instability",
    "lineage_instability",
    "adjacency_valence",
    "continuity_state",
    "invariant_delta_h",
    "routing_severity",
)

# STPX structural cue → intent (v1 locked map)
STPX_INTENT_MAP = {
    "question": "request",
    "interrogative": "request",
    "correction_marker": "correct",
    "correction": "correct",
    "declarative": "inform",
    "commitment": "commit",
    "hypothetical": "speculate",
    "ambiguous": "clarify",
}

STPX_LOGICAL_MAP = {
    "conditional": "conditional",
    "causal": "causal",
    "contrastive": "contrastive",
    "additive": "additive",
    "corrective": "corrective",
    "correction_marker": "corrective",
}


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


class TR:
    def __init__(self, tp_input: Optional[dict] = None):
        self.tp = copy.deepcopy(tp_input) if tp_input is not None else {}

    def process(self) -> dict:
        if not self._needs_update():
            return self.tp

        inputs = self._extract_tr_inputs(self.tp)
        geometry = self._compute_geometry(inputs)
        mappings = self._compute_mapping_fields(inputs, geometry)
        lineage_additions = self._compute_lineage_additions(inputs)
        delta_h = self._compute_epistemic_delta_h(inputs)
        routing_fields = self._build_routing_fields(
            inputs, geometry, mappings, delta_h, lineage_additions
        )
        tr_block = self._build_tr_block(
            mappings, delta_h, lineage_additions, routing_fields
        )
        self._write_tr(tr_block)
        self._clear_dirty_flag()
        self._write_provenance_optional(inputs)
        self._append_audit_optional(tr_block)
        return self.tp

    # ------------------------------------------------------------------
    # Gate
    # ------------------------------------------------------------------

    def _needs_update(self) -> bool:
        return bool(self.tp.get("tr_needs_update"))

    # ------------------------------------------------------------------
    # Extract
    # ------------------------------------------------------------------

    def _extract_tr_inputs(self, tp: dict) -> dict:
        semantic = tp.get("semantic") if isinstance(tp.get("semantic"), dict) else {}
        process = tp.get("process") if isinstance(tp.get("process"), dict) else {}
        meta = tp.get("metadata") if isinstance(tp.get("metadata"), dict) else {}
        routing_metadata = (
            process.get("routing_metadata")
            if isinstance(process.get("routing_metadata"), dict)
            else {}
        )
        stpx = tp.get("STPX") if isinstance(tp.get("STPX"), dict) else {}
        diagnostics = (
            tp.get("_tr_diagnostics")
            if isinstance(tp.get("_tr_diagnostics"), dict)
            else {}
        )
        geometric_state = (
            meta.get("geometric_state")
            if isinstance(meta.get("geometric_state"), dict)
            else {}
        )

        enable_diag = bool(diagnostics.get("enable_diagnostics", False))

        def _diag_int(key: str) -> Optional[int]:
            if not enable_diag or key not in diagnostics:
                return None
            try:
                return int(diagnostics[key])
            except (TypeError, ValueError):
                return None

        return {
            "semantic": semantic,
            "routing_metadata": routing_metadata,
            "lineage": semantic.get("lineage"),
            "stpx": stpx,
            "diagnostics": diagnostics,
            "enable_diagnostics": enable_diag,
            "adjacency": _diag_int("adjacency"),
            "continuity": _diag_int("continuity"),
            "identity_geometry": _diag_int("identity_geometry"),
            "invariant_H_t": diagnostics.get("invariant_H_t") if enable_diag else None,
            "invariant_H_t1": diagnostics.get("invariant_H_t1") if enable_diag else None,
            "referent_lineage": (
                diagnostics.get("referent_lineage") if enable_diag else None
            ),
            "qualifier_lineage": (
                diagnostics.get("qualifier_lineage") if enable_diag else None
            ),
            "geometric_state": geometric_state,
            "timestamp": diagnostics.get("timestamp", 0.0),
        }

    # ------------------------------------------------------------------
    # Geometry (minimal path + optional diagnostics)
    # ------------------------------------------------------------------

    def _compute_geometry(self, inputs: dict) -> dict:
        # Minimal-input defaults (geometry §11)
        x_s, x_a, x_e, x_p, x_t = 1, 0, 1, 1, 0

        A = inputs.get("adjacency")
        C = inputs.get("continuity")
        I = inputs.get("identity_geometry")

        # Adjacency projection
        if A is not None:
            x_a = max(-1, min(1, int(A)))
            if x_a > 0:
                x_p = 2
            elif x_a < 0:
                x_p = 0
            else:
                x_p = 1
            # adjacency_modifier provisional {-1,0,+1}
            x_s = x_s + (1 if x_a > 0 else (-1 if x_a < 0 else 0))

        # Continuity
        if C is not None:
            c = max(-1, min(1, int(C)))
            x_s = x_s + c
            x_e = x_e + max(0, -c)

        # Identity
        if I is not None:
            i = max(-1, min(1, int(I)))
            x_s = x_s + i
            x_e = x_e + max(0, -i)
            x_t = x_t + max(0, -i)

        # Curvature from DCB geometric_state (v1 normative minimal envelope)
        gs = inputs.get("geometric_state") or {}
        curv = gs.get("curvature")
        if curv is not None:
            try:
                cf = float(curv)
            except (TypeError, ValueError):
                cf = 0.0
            if cf >= 1.0:
                x_t = max(x_t, 1)  # medium
            elif cf > 0.0:
                x_t = max(x_t, 1)

        # Clamp ordinal ranges
        x_s = max(0, min(4, x_s))
        x_a = max(-1, min(1, x_a))
        x_e = max(0, min(3, x_e))
        x_p = max(0, min(2, x_p))
        x_t = max(0, min(2, x_t))

        return {
            "x_s": x_s,
            "x_a": x_a,
            "x_e": x_e,
            "x_p": x_p,
            "x_t": x_t,
            "A": A if A is not None else 0,
            "C": C if C is not None else 0,
            "I": I if I is not None else 0,
            "curvature_level": int(x_t),
        }

    # ------------------------------------------------------------------
    # Mapping fields
    # ------------------------------------------------------------------

    def _stance_label(self, x_s: int) -> str:
        return {
            0: "supportive",
            1: "neutral",
            2: "corrective",
            3: "adversarial",
            4: "exploratory",
        }.get(x_s, "neutral")

    def _affect_label(self, x_a: int) -> str:
        return {-1: "negative", 0: "neutral", 1: "positive"}.get(x_a, "neutral")

    def _shading_label(self, x_e: int) -> str:
        return {
            0: "confident",
            1: "neutral",
            2: "uncertain",
            3: "speculative",
        }.get(x_e, "neutral")

    def _tension_label(self, x_t: int) -> str:
        return {0: "low", 1: "medium", 2: "high"}.get(x_t, "low")

    def _politeness_label(self, x_p: int) -> str:
        return {0: "direct", 1: "neutral", 2: "polite"}.get(x_p, "neutral")

    def _stpx_cues(self, inputs: dict) -> List[str]:
        stpx = inputs.get("stpx") or {}
        cues = stpx.get("cues") if isinstance(stpx.get("cues"), dict) else {}
        structural = cues.get("structural") or []
        if not isinstance(structural, list):
            return []
        return [str(c).lower() for c in structural]

    def _compute_intent(self, inputs: dict) -> str:
        for cue in self._stpx_cues(inputs):
            if cue in STPX_INTENT_MAP:
                return STPX_INTENT_MAP[cue]
        return "inform"

    def _compute_logical_structure(self, inputs: dict) -> str:
        for cue in self._stpx_cues(inputs):
            if cue in STPX_LOGICAL_MAP:
                return STPX_LOGICAL_MAP[cue]
        return "additive"

    def _compute_mapping_fields(self, inputs: dict, geometry: dict) -> dict:
        return {
            "stance": self._stance_label(geometry["x_s"]),
            "intent": self._compute_intent(inputs),
            "affect": self._affect_label(geometry["x_a"]),
            "epistemic_shading": self._shading_label(geometry["x_e"]),
            "tension": self._tension_label(geometry["x_t"]),
            "politeness": self._politeness_label(geometry["x_p"]),
            "commitment": "weak",
            "reservation": "none",
            "logical_structure": self._compute_logical_structure(inputs),
        }

    # ------------------------------------------------------------------
    # Lineage / delta_h
    # ------------------------------------------------------------------

    def _compute_lineage_additions(self, inputs: dict) -> List[Any]:
        if not inputs.get("enable_diagnostics"):
            return []

        candidates: List[Any] = []
        ref = inputs.get("referent_lineage")
        qual = inputs.get("qualifier_lineage")
        if isinstance(ref, list):
            candidates.extend(ref)
        if isinstance(qual, list):
            candidates.extend(qual)

        # Only append when continuity/identity suggest drift (v1 heuristic)
        C = inputs.get("continuity")
        I = inputs.get("identity_geometry")
        if C is not None and int(C) >= 0 and I is not None and int(I) >= 0:
            # stable — no forced additions unless novelty list non-empty and C/I negative
            if not candidates:
                return []

        if C is not None and int(C) < 0 or I is not None and int(I) < 0:
            # drift path: take up to k candidates deterministically
            out = []
            seen = set()
            for item in candidates:
                key = str(item)
                if key in seen:
                    continue
                seen.add(key)
                out.append(item)
                if len(out) >= LINEAGE_BOUND_K:
                    break
            return out

        return []

    def _compute_epistemic_delta_h(self, inputs: dict) -> int:
        if not inputs.get("enable_diagnostics"):
            return 0
        h_t = inputs.get("invariant_H_t")
        h_t1 = inputs.get("invariant_H_t1")
        if h_t is None or h_t1 is None:
            return 0
        try:
            return int(h_t1) - int(h_t)
        except (TypeError, ValueError):
            return 0

    # ------------------------------------------------------------------
    # routing_fields
    # ------------------------------------------------------------------

    def _build_routing_fields(
        self,
        inputs: dict,
        geometry: dict,
        mappings: dict,
        delta_h: int,
        lineage_additions: List[Any],
    ) -> dict:
        A = geometry.get("A", 0)
        C = geometry.get("C", 0)
        curv_level = int(geometry.get("curvature_level", 0))

        rf = {
            "semantic_drift": bool(A != 0 or C < 0 or curv_level > 0),
            "identity_drift": bool(
                inputs.get("identity_geometry") is not None
                and int(inputs["identity_geometry"]) < 0
            ),
            "commitment_instability": False,
            "freeze_conflict": False,
            "topology_instability": False,
            "curvature_level": curv_level,
            "stance_instability": False,
            "shading_instability": bool(
                inputs.get("continuity") is not None and int(inputs["continuity"]) < 0
            ),
            "tension_instability": bool(curv_level > 0),
            "lineage_instability": bool(len(lineage_additions) > 0),
            "adjacency_valence": int(A) if A is not None else 0,
            "continuity_state": int(C) if C is not None else 0,
            "invariant_delta_h": int(delta_h),
            "routing_severity": min(3, max(0, curv_level + (1 if C is not None and int(C) < 0 else 0))),
        }
        # Ensure complete key set in declaration order
        return {k: rf[k] for k in ROUTING_FIELDS_KEYS}

    def _build_tr_block(
        self,
        mappings: dict,
        delta_h: int,
        lineage_additions: List[Any],
        routing_fields: dict,
    ) -> dict:
        return {
            "stance": mappings["stance"],
            "intent": mappings["intent"],
            "affect": mappings["affect"],
            "epistemic_shading": mappings["epistemic_shading"],
            "tension": mappings["tension"],
            "politeness": mappings["politeness"],
            "commitment": mappings["commitment"],
            "reservation": mappings["reservation"],
            "logical_structure": mappings["logical_structure"],
            "epistemic_delta_h": int(delta_h),
            "lineage_additions": list(lineage_additions)[:LINEAGE_BOUND_K],
            "routing_fields": dict(routing_fields),
        }

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def _write_tr(self, tr_block: dict) -> None:
        self.tp["TR"] = tr_block

    def _clear_dirty_flag(self) -> None:
        self.tp["tr_needs_update"] = False

    def _write_provenance_optional(self, inputs: dict) -> None:
        meta = self.tp.setdefault("metadata", {})
        if not isinstance(meta, dict):
            self.tp["metadata"] = {}
            meta = self.tp["metadata"]
        prov = meta.setdefault("provenance", {})
        if not isinstance(prov, dict):
            meta["provenance"] = {}
            prov = meta["provenance"]
        try:
            prov["tr_last_update"] = float(inputs.get("timestamp", 0.0))
        except (TypeError, ValueError):
            prov["tr_last_update"] = 0.0

    def _append_audit_optional(self, tr_block: dict) -> None:
        self.tp.setdefault("exec_trace", [])
        if not isinstance(self.tp["exec_trace"], list):
            self.tp["exec_trace"] = []
        self.tp["exec_trace"].append(
            {
                "tr_ref": {
                    "origin": "TR",
                    "last_update": "TR",
                    "stance": tr_block.get("stance"),
                    "intent": tr_block.get("intent"),
                    "tension": tr_block.get("tension"),
                }
            }
        )


def run(tp: dict) -> dict:
    return TR(tp).process()
