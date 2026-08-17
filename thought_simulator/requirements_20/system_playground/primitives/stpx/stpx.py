"""
STPX — Structured Token & Pattern Extractor (Version 1.0)
Aligned with:
  - 20.49_stpx_prim.md v4.0
  - stpx_py_struc_pgm.md
  - progressive_lineup_testing.md v4.1

Post-SSG structural cue extractor. Produces a deterministic four-family
cue_envelope (lexical / structural / constraint / repair) and writes only:
  TP.metadata.semantic_layer_metadata.stpx_cues
  TP.metadata.semantic_layer_metadata.semantic_layer_provenance
No semantic interpretation, routing, identity, or upstream mutation.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Tuple

PRIMITIVE_NAME = "stpx"

# Provisional lexical marker vocabularies (structural surface cues only)
CONTRAST_MARKERS = {"but", "however", "yet", "although", "though", "whereas", "instead", "nevertheless"}
TEMPORAL_MARKERS = {"then", "after", "before", "while", "when", "later", "earlier", "next", "previously", "subsequently"}
DISCOURSE_MARKERS = {"therefore", "thus", "hence", "so", "because", "since", "if", "unless", "moreover", "furthermore"}
CAUSAL_MARKERS = {"because", "since", "therefore", "thus", "hence", "so", "cause", "effect"}


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


def _ensure_list(val: Any) -> List:
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return [val]


def _sort_key_type_token(item: dict) -> Tuple:
    return (str(item.get("type", "")), str(item.get("token", item.get("segment", ""))))


class STPX:
    """
    Structured Token & Pattern Extractor.

    Usage (testbench style, matching SSG / ISc):
        stpx = STPX(tp_input)
        tp_out = stpx.process()
    """

    def __init__(self, tp_input: Optional[dict] = None):
        self.tp = copy.deepcopy(tp_input) if tp_input is not None else {}

    def process(self) -> dict:
        geom = self._extract_structural_geometry(self.tp)
        ssg = self._extract_ssg_outputs(self.tp)
        tokens = self._extract_tokens(self.tp)
        meta = self._extract_struct_adjacent_metadata(self.tp)

        if geom is None and tokens is None:
            cues = self._empty_cues()
            self._write_cues(cues)
            self._write_provenance(empty=True)
            self._append_audit(empty=True)
            return self.tp

        lexical = self._compute_lexical_cues(tokens or [], meta)
        structural = self._compute_structural_cues(geom or {}, ssg, meta)
        constraint = self._compute_constraint_cues(geom or {}, meta)
        repair = self._compute_repair_markers(geom or {}, tokens or [], meta)

        cues = self._assemble_cue_envelope(lexical, structural, constraint, repair)
        self._write_cues(cues)
        self._write_provenance(empty=False)
        self._append_audit(empty=False)
        return self.tp

    # ------------------------------------------------------------------
    # Extraction helpers
    # ------------------------------------------------------------------

    def _extract_structural_geometry(self, tp: dict) -> Optional[dict]:
        meta = tp.get("metadata") or {}
        # Preferred: structural_metadata / residue_metadata (canonical 20.49 paths)
        structural = meta.get("structural_metadata")
        residue = meta.get("residue_metadata") or meta.get("residue")

        if isinstance(structural, dict) or isinstance(residue, dict):
            return {
                "structural_metadata": structural if isinstance(structural, dict) else {},
                "residue_metadata": residue if isinstance(residue, dict) else {},
            }

        # Fallback: SSG-shaped residue under metadata.residue (common in upstream fixtures)
        if isinstance(residue, dict):
            return {"structural_metadata": {}, "residue_metadata": residue}

        # Last resort: any structural_graph
        sg = meta.get("structural_graph") or tp.get("structural_graph")
        if isinstance(sg, dict):
            return {"structural_metadata": {"structural_graph": sg}, "residue_metadata": {}}

        return None

    def _extract_ssg_outputs(self, tp: dict) -> dict:
        return {
            "ssg_signature": tp.get("ssg_signature"),
            "ssg_layer_bitmap": tp.get("ssg_layer_bitmap"),
            "ssg_reason_code": tp.get("ssg_reason_code"),
            "ssg_status": tp.get("ssg_status"),
        }

    def _extract_tokens(self, tp: dict) -> Optional[List]:
        meta = tp.get("metadata") or {}
        norm = meta.get("normalization_metadata") or {}
        tokens = norm.get("normalized_tokens")
        if isinstance(tokens, list) and tokens:
            return [str(t).lower() for t in tokens]

        # Fallback: try IE-style or surface tokens if present
        for key in ("tokens", "canonical_tokens", "surface_tokens"):
            val = tp.get(key) or meta.get(key)
            if isinstance(val, list) and val:
                return [str(t).lower() for t in val]

        return None

    def _extract_struct_adjacent_metadata(self, tp: dict) -> dict:
        meta = tp.get("metadata") or {}
        return {
            "normalization_metadata": meta.get("normalization_metadata") or {},
            "expressive_metadata": meta.get("expressive_metadata") or {},
            "continuity_metadata": meta.get("continuity_metadata") or {},
            "entropy_metadata": meta.get("entropy_metadata") or {},
            "provenance_metadata": meta.get("provenance_metadata") or {},
            "residue_metadata": meta.get("residue_metadata") or meta.get("residue") or {},
        }

    # ------------------------------------------------------------------
    # Cue family computation
    # ------------------------------------------------------------------

    def _compute_lexical_cues(self, tokens: List[str], meta: dict) -> List[dict]:
        cues: List[dict] = []
        seen = set()
        for tok in tokens:
            t = tok.lower().strip()
            if not t or t in seen:
                continue
            if t in CONTRAST_MARKERS:
                cues.append({"type": "contrast_marker", "token": t})
                seen.add(t)
            elif t in TEMPORAL_MARKERS:
                cues.append({"type": "temporal_marker", "token": t})
                seen.add(t)
            elif t in DISCOURSE_MARKERS:
                cues.append({"type": "discourse_marker", "token": t})
                seen.add(t)

        # Expressive stylization hints (structural surface only)
        expr = meta.get("expressive_metadata") or {}
        for key in ("elongation_patterns", "abbreviation_patterns", "omission_patterns"):
            for item in _ensure_list(expr.get(key)):
                cues.append({"type": f"expressive_{key}", "token": str(item)})

        return cues

    def _compute_structural_cues(self, geom: dict, ssg: dict, meta: dict) -> List[dict]:
        cues: List[dict] = []
        residue = geom.get("residue_metadata") or {}
        sr = residue.get("structural_residue") if isinstance(residue.get("structural_residue"), dict) else residue

        nodes = _ensure_list(sr.get("nodes") if isinstance(sr, dict) else [])
        arcs = _ensure_list(sr.get("arcs") if isinstance(sr, dict) else [])

        # Segment / role cues
        layers_seen = set()
        for n in nodes:
            if not isinstance(n, dict):
                continue
            ly = n.get("layer")
            if ly is not None:
                layers_seen.add(int(ly))
            label = str(n.get("label", ""))
            if label:
                cues.append({"type": "structural_role", "segment": str(n.get("id", "")), "label": label})

        if len(nodes) >= 2:
            cues.append({"type": "segment_boundary", "count": len(nodes)})

        # SSG-derived structural cues
        status = ssg.get("ssg_status")
        reason = ssg.get("ssg_reason_code")
        bitmap = ssg.get("ssg_layer_bitmap")
        if status:
            cues.append({"type": "ssg_status", "value": str(status)})
        if reason:
            cues.append({"type": "ssg_reason", "value": str(reason)})
        if isinstance(bitmap, int) and bitmap > 0:
            cues.append({"type": "ssg_layer_bitmap", "value": bitmap})
            if bitmap == 15:
                cues.append({"type": "cycle_density_high", "layer": "multi"})

        # Continuity / discourse-context structural cues
        cont = meta.get("continuity_metadata") or {}
        for flag in _ensure_list(cont.get("continuity_flags")):
            cues.append({"type": "continuity_flag", "value": str(flag)})
        if cont.get("identity_anchors"):
            cues.append({"type": "identity_anchor_present", "count": len(_ensure_list(cont.get("identity_anchors")))})

        # Temporal / contrastive structure from arcs
        for a in arcs:
            if not isinstance(a, dict):
                continue
            lab = str(a.get("label", "")).lower()
            if lab in ("order", "continue"):
                cues.append({"type": "temporal_shift", "segment": f"{a.get('src')}-{a.get('dst')}"})
            if lab in ("constrain", "bind") and len(arcs) > 1:
                cues.append({"type": "contrastive_structure", "segments": [str(a.get("src")), str(a.get("dst"))]})

        return cues

    def _compute_constraint_cues(self, geom: dict, meta: dict) -> List[dict]:
        cues: List[dict] = []
        residue = geom.get("residue_metadata") or {}
        sr = residue.get("structural_residue") if isinstance(residue.get("structural_residue"), dict) else residue
        structural = geom.get("structural_metadata") or {}

        # Constraint surfaces
        for cs in _ensure_list(structural.get("constraint_surfaces")):
            if isinstance(cs, dict):
                cues.append({"type": "constraint_surface", "value": str(cs.get("type", cs))})
            else:
                cues.append({"type": "constraint_surface", "value": str(cs)})

        # Constraint residue
        cr = residue.get("constraint_residue")
        for item in _ensure_list(cr):
            if isinstance(item, dict):
                cues.append({"type": "constraint_residue", "value": str(item.get("type", item))})
            else:
                cues.append({"type": "constraint_residue", "value": str(item)})

        # Causal / referential from arcs or labels
        arcs = _ensure_list(sr.get("arcs") if isinstance(sr, dict) else [])
        for a in arcs:
            if not isinstance(a, dict):
                continue
            lab = str(a.get("label", "")).lower()
            if lab in ("constrain", "cause", "effect"):
                cues.append(
                    {
                        "type": "causal_link",
                        "from": str(a.get("src", "")),
                        "to": str(a.get("dst", "")),
                    }
                )
            if lab in ("bind", "ref", "refer"):
                cues.append({"type": "referential_stability", "entity": str(a.get("dst", a.get("src", "")))})

        return cues

    def _compute_repair_markers(self, geom: dict, tokens: List[str], meta: dict) -> List[dict]:
        cues: List[dict] = []
        residue = geom.get("residue_metadata") or {}
        norm = meta.get("normalization_metadata") or {}

        # Alignment map anomalies
        align = norm.get("token_alignment_map")
        if isinstance(align, dict) and align:
            for k, v in align.items():
                if v is None or v == "" or v != k:
                    cues.append({"type": "alignment_anomaly", "segment": str(k)})

        # Explicit repair spans if present in residue or expressive
        for key in ("repair_spans", "repair_regions"):
            for span in _ensure_list(residue.get(key) or norm.get(key)):
                if isinstance(span, dict):
                    cues.append(
                        {
                            "type": "repair_span",
                            "start": span.get("start"),
                            "end": span.get("end"),
                        }
                    )
                else:
                    cues.append({"type": "repair_span", "value": str(span)})

        # High repair confidence flags
        if residue.get("repair_confidence") is not None:
            try:
                conf = float(residue.get("repair_confidence"))
                if conf > 0.5:
                    cues.append({"type": "high_repair_confidence", "value": conf})
            except (TypeError, ValueError):
                pass

        return cues

    # ------------------------------------------------------------------
    # Assembly & write
    # ------------------------------------------------------------------

    def _empty_cues(self) -> dict:
        return {
            "lexical": [],
            "structural": [],
            "constraint": [],
            "repair": [],
        }

    def _assemble_cue_envelope(
        self,
        lexical: List[dict],
        structural: List[dict],
        constraint: List[dict],
        repair: List[dict],
    ) -> dict:
        return {
            "lexical": sorted(lexical, key=_sort_key_type_token),
            "structural": sorted(structural, key=_sort_key_type_token),
            "constraint": sorted(constraint, key=_sort_key_type_token),
            "repair": sorted(repair, key=_sort_key_type_token),
        }

    def _write_cues(self, cues: dict) -> None:
        meta = self.tp.setdefault("metadata", {})
        if not isinstance(meta, dict):
            self.tp["metadata"] = {}
            meta = self.tp["metadata"]
        slm = meta.setdefault("semantic_layer_metadata", {})
        if not isinstance(slm, dict):
            meta["semantic_layer_metadata"] = {}
            slm = meta["semantic_layer_metadata"]
        slm["stpx_cues"] = cues

    def _write_provenance(self, empty: bool = False) -> None:
        meta = self.tp.setdefault("metadata", {})
        if not isinstance(meta, dict):
            self.tp["metadata"] = {}
            meta = self.tp["metadata"]
        slm = meta.setdefault("semantic_layer_metadata", {})
        if not isinstance(slm, dict):
            meta["semantic_layer_metadata"] = {}
            slm = meta["semantic_layer_metadata"]

        prov_in = (meta.get("provenance_metadata") or {})
        commit_id = prov_in.get("commit_id", "stpx_v1")
        sequence = list(prov_in.get("commit_sequence") or [])
        if "STPX" not in sequence:
            sequence = sequence + ["STPX"]

        slm["semantic_layer_provenance"] = {
            "origin": "STPX",
            "last_update": "STPX",
            "commit_id": commit_id,
            "commit_sequence": sequence,
            "empty": bool(empty),
        }

    def _append_audit(self, empty: bool = False) -> None:
        self.tp.setdefault("exec_trace", [])
        if not isinstance(self.tp["exec_trace"], list):
            self.tp["exec_trace"] = []
        self.tp["exec_trace"].append(
            {
                "stpx_ref": {
                    "origin": "STPX",
                    "last_update": "STPX",
                    "empty": bool(empty),
                    "families": ["lexical", "structural", "constraint", "repair"],
                }
            }
        )


def run(tp: dict) -> dict:
    """Functional entrypoint matching stpx_py_struc_pgm.md."""
    return STPX(tp).process()
