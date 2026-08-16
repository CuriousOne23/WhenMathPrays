"""
SSG — Structural Signature Generator (Version 1.0)
Aligned with:
  - 20.47_ssg_prim.md v3.0 (Unified Structural-Only Rewrite)
  - ssg_py_struc_pgm.md (Unified Structural-Only Rewrite)
  - progressive_lineup_testing.md v4.0

Maps the SmOB structural graph into a fixed-length L2-normalized
structural signature. Writes only the four SSG-owned fields.
No semantic-layer, routing, identity, or meaning writes.
"""

from __future__ import annotations

import copy
import math
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

PRIMITIVE_NAME = "ssg"

# Provisional dimension and family lengths (open for geometric investigation)
# f1 arc patterns (8), f2 binding depth (2), f3 residue entropy (1),
# f4 curvature (2), f5 motif frequencies (7)  → d = 20
F1_LEN = 8
F2_LEN = 2
F3_LEN = 1
F4_LEN = 2
F5_LEN = 7
D = F1_LEN + F2_LEN + F3_LEN + F4_LEN + F5_LEN  # 20

# Canonical arc-label vocabulary for f1 (provisional)
ARC_VOCAB = [
    "bind",
    "order",
    "adj",
    "constrain",
    "refine",
    "continue",
    "segment",
    "other",
]

# Provisional motif keys for f5
MOTIF_KEYS = [
    "chain2",
    "chain3",
    "star",
    "cycle3",
    "parallel",
    "self_loop",
    "isolated",
]


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


def _safe_float(x: Any, default: float = 0.0) -> float:
    try:
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return default
        return v
    except (TypeError, ValueError):
        return default


def _l2_normalize(vec: List[float]) -> List[float]:
    norm = math.sqrt(sum(v * v for v in vec))
    if norm <= 0.0:
        return [0.0] * len(vec)
    return [v / norm for v in vec]


def _shannon_entropy(counts: List[float]) -> float:
    total = sum(counts)
    if total <= 0.0:
        return 0.0
    h = 0.0
    for c in counts:
        if c > 0.0:
            p = c / total
            h -= p * math.log2(p)
    return float(h)


class SSG:
    """
    Structural Signature Generator.

    Usage (testbench style, matching ISc):
        ssg = SSG(tp_input)
        tp_out = ssg.process()
    """

    def __init__(self, tp_input: Optional[dict] = None):
        self.tp = copy.deepcopy(tp_input) if tp_input is not None else {}

    def process(self) -> dict:
        graph = self._extract_graph(self.tp)
        if graph is None:
            self._write_missing()
            return self.tp

        phi, layer_bits = self._compute_phi(graph)
        signature = _l2_normalize(phi)

        # Status / reason
        non_zero_layers = sum(1 for b in layer_bits if b)
        if all(abs(v) < 1e-15 for v in phi):
            if self._graph_nonempty(graph):
                status = "DEGENERATE"
                reason = "EMPTY"
            else:
                status = "OK"
                reason = "EMPTY"
            bitmap = 0
        else:
            bitmap = sum(b << i for i, b in enumerate(layer_bits))
            if non_zero_layers == 4:
                reason = "FULL"
            elif non_zero_layers == 0:
                reason = "EMPTY"
            else:
                reason = "PARTIAL"
            status = "OK"
            if status == "OK" and reason == "EMPTY" and self._graph_nonempty(graph):
                status = "DEGENERATE"

        if status == "DEGENERATE":
            signature = [0.0] * D

        self._write(signature, bitmap, reason, status)
        self._append_audit(status, reason, bitmap)
        return self.tp

    def _extract_graph(self, tp: dict) -> Optional[dict]:
        meta = tp.get("metadata") or {}
        residue = meta.get("residue")
        if residue is None:
            sg = meta.get("structural_graph") or tp.get("structural_graph")
            if isinstance(sg, dict):
                return self._normalize_graph(sg)
            return None

        if not isinstance(residue, dict):
            return None

        sr = residue.get("structural_residue")
        if isinstance(sr, dict) and ("nodes" in sr or "arcs" in sr):
            return self._normalize_graph(sr)

        nodes = []
        arcs = []
        for key in (
            "structural_residue",
            "refinement_residue",
            "constraint_residue",
            "semantic_adjacent_residue",
        ):
            val = residue.get(key)
            if val is None:
                continue
            if isinstance(val, dict) and "nodes" in val:
                nodes.extend(val.get("nodes") or [])
                arcs.extend(val.get("arcs") or [])
            elif isinstance(val, list):
                for i, item in enumerate(val):
                    nid = f"{key}_{i}"
                    nodes.append({"id": nid, "label": key, "layer": 3})
            elif isinstance(val, (str, int, float)) and val != "":
                nid = f"{key}_0"
                nodes.append({"id": nid, "label": str(key), "layer": 3})

        return self._normalize_graph({"nodes": nodes, "arcs": arcs})

    def _normalize_graph(self, g: dict) -> dict:
        nodes = g.get("nodes") or []
        arcs = g.get("arcs") or []
        if not isinstance(nodes, list):
            nodes = []
        if not isinstance(arcs, list):
            arcs = []
        norm_nodes = []
        for i, n in enumerate(nodes):
            if not isinstance(n, dict):
                norm_nodes.append({"id": str(i), "label": str(n), "layer": 3})
            else:
                norm_nodes.append(
                    {
                        "id": str(n.get("id", i)),
                        "label": str(n.get("label", "node")),
                        "layer": int(n.get("layer", 3)),
                    }
                )
        norm_arcs = []
        for a in arcs:
            if not isinstance(a, dict):
                continue
            label = str(a.get("label", "other")).lower()
            if label not in ARC_VOCAB:
                label = "other"
            norm_arcs.append(
                {
                    "src": str(a.get("src", "")),
                    "dst": str(a.get("dst", "")),
                    "label": label,
                    "layer": int(a.get("layer", 3)),
                }
            )
        return {"nodes": norm_nodes, "arcs": norm_arcs}

    def _graph_nonempty(self, graph: dict) -> bool:
        return bool(graph.get("nodes") or graph.get("arcs"))

    def _compute_phi(self, graph: dict) -> Tuple[List[float], List[int]]:
        f1 = self._f1_arc_patterns(graph)
        f2 = self._f2_binding_depth(graph)
        f3 = self._f3_residue_entropy(graph)
        f4 = self._f4_curvature(graph)
        f5 = self._f5_motif_frequencies(graph)

        layer_bits = [0, 0, 0, 0]
        for n in graph.get("nodes") or []:
            ly = int(n.get("layer", 3))
            if 0 <= ly <= 3:
                layer_bits[ly] = 1
        for a in graph.get("arcs") or []:
            ly = int(a.get("layer", 3))
            if 0 <= ly <= 3:
                layer_bits[ly] = 1
        if self._graph_nonempty(graph) and sum(layer_bits) == 0:
            layer_bits[3] = 1

        phi = f1 + f2 + f3 + f4 + f5
        if all(abs(v) < 1e-15 for v in phi):
            layer_bits = [0, 0, 0, 0]

        return phi, layer_bits

    def _f1_arc_patterns(self, graph: dict) -> List[float]:
        arcs = graph.get("arcs") or []
        counts = Counter(a.get("label", "other") for a in arcs)
        total = sum(counts.values()) or 1
        return [counts.get(lab, 0) / total for lab in ARC_VOCAB]

    def _f2_binding_depth(self, graph: dict) -> List[float]:
        nodes = {n["id"] for n in graph.get("nodes") or []}
        out_edges: Dict[str, List[str]] = {nid: [] for nid in nodes}
        for a in graph.get("arcs") or []:
            s, d = a.get("src"), a.get("dst")
            if s in out_edges:
                out_edges[s].append(d)

        if not nodes:
            return [0.0, 0.0]

        def depth_from(start: str) -> int:
            seen = set()
            stack = [(start, 0)]
            max_d = 0
            while stack:
                u, d = stack.pop()
                if u in seen:
                    continue
                seen.add(u)
                max_d = max(max_d, d)
                for v in out_edges.get(u, []):
                    if v not in seen:
                        stack.append((v, d + 1))
            return max_d

        depths = [depth_from(nid) for nid in nodes]
        max_depth = float(max(depths) if depths else 0)
        mean_depth = float(sum(depths) / len(depths)) if depths else 0.0
        return [max_depth / 10.0, mean_depth / 10.0]

    def _f3_residue_entropy(self, graph: dict) -> List[float]:
        labels = [n.get("label", "node") for n in graph.get("nodes") or []]
        if not labels:
            return [0.0]
        counts = list(Counter(labels).values())
        return [_shannon_entropy([float(c) for c in counts])]

    def _f4_curvature(self, graph: dict) -> List[float]:
        nodes = {n["id"] for n in graph.get("nodes") or []}
        n = len(nodes)
        arcs = graph.get("arcs") or []
        m = len(arcs)
        if n < 2:
            return [0.0, 0.0]

        possible = n * (n - 1)
        cycle_proxy = (m / possible) if possible else 0.0

        out_deg = Counter(a.get("src") for a in arcs)
        clustered = sum(1 for v in out_deg.values() if v >= 2)
        clustering = clustered / n if n else 0.0

        return [float(cycle_proxy), float(clustering)]

    def _f5_motif_frequencies(self, graph: dict) -> List[float]:
        nodes = graph.get("nodes") or []
        arcs = graph.get("arcs") or []
        n = len(nodes)
        m = len(arcs)
        if n == 0:
            return [0.0] * F5_LEN

        out_deg = Counter(a.get("src") for a in arcs)
        in_deg = Counter(a.get("dst") for a in arcs)
        self_loops = sum(1 for a in arcs if a.get("src") == a.get("dst"))
        isolated = sum(
            1
            for node in nodes
            if out_deg[node["id"]] == 0 and in_deg[node["id"]] == 0
        )

        chain2 = sum(1 for d in out_deg.values() if d == 1)
        chain3 = sum(1 for d in out_deg.values() if d >= 2)
        star = sum(1 for d in out_deg.values() if d >= 3)
        cycle3 = 0.0
        parallel = max(0, m - n)
        vals = [
            chain2 / max(n, 1),
            chain3 / max(n, 1),
            star / max(n, 1),
            cycle3,
            parallel / max(m, 1),
            self_loops / max(m, 1),
            isolated / max(n, 1),
        ]
        return [float(v) for v in vals]

    def _write(
        self,
        signature: List[float],
        bitmap: int,
        reason: str,
        status: str,
    ) -> None:
        self.tp["ssg_signature"] = [float(v) for v in signature]
        self.tp["ssg_layer_bitmap"] = int(bitmap) & 0xF
        self.tp["ssg_reason_code"] = reason
        self.tp["ssg_status"] = status

    def _write_missing(self) -> None:
        self.tp.pop("ssg_signature", None)
        self.tp["ssg_layer_bitmap"] = 0
        self.tp["ssg_reason_code"] = "EMPTY"
        self.tp["ssg_status"] = "MISSING_INPUT"
        self._append_audit("MISSING_INPUT", "EMPTY", 0)

    def _append_audit(self, status: str, reason: str, bitmap: int) -> None:
        self.tp.setdefault("exec_trace", [])
        if not isinstance(self.tp["exec_trace"], list):
            self.tp["exec_trace"] = []
        self.tp["exec_trace"].append(
            {
                "ssg_ref": {
                    "status": status,
                    "reason_code": reason,
                    "layer_bitmap": bitmap,
                    "origin": "SSG",
                    "last_update": "SSG",
                }
            }
        )


def run(tp: dict) -> dict:
    """Functional entrypoint matching ssg_py_struc_pgm.md."""
    return SSG(tp).process()
