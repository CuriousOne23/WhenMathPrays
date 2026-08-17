"""
RBU — Register / Belief / Usage Commit (Version 1.0)
Aligned with:
  - 20.51_rbu_prim.md v4.0
  - rbu_py_struc_pgm.md
  - progressive_lineup_testing.md v4.1

Meaning-side commit stage after IdOB. Commits identity-conditioned meaning
fields into the TP and writes only:
  TP.semantic.identity
  TP.semantic.stance
  TP.semantic.register
  TP.semantic.tone
  TP.semantic.tags
  TP.metadata.lineage_markers
  TP.metadata.provenance  (RBU entries only)

No structural modification, no semantic inference beyond IdOB payload,
no TPTB/TPSF, no Path-B interaction.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional

PRIMITIVE_NAME = "rbu"


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


def _ensure_list(val: Any) -> List:
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return [val]


def _ensure_dict(val: Any) -> dict:
    return val if isinstance(val, dict) else {}


class RBU:
    """
    Register / Belief / Usage Commit.

    Usage (testbench style, matching STPX / ISc):
        rbu = RBU(tp_input)
        tp_out = rbu.process()
    """

    def __init__(self, tp_input: Optional[dict] = None):
        self.tp = copy.deepcopy(tp_input) if tp_input is not None else {}

    def process(self) -> dict:
        meaning = self._extract_meaning_fields(self.tp)
        meta = self._extract_meaning_adjacent_metadata(self.tp)

        if not self._has_required_inputs(meaning):
            self._commit_minimal_meaning(meaning, meta)
            self._write_provenance(empty=True)
            self._append_audit(empty=True)
            return self.tp

        identity = self._commit_identity(meaning, meta)
        stance = self._commit_stance(meaning, meta)
        register = self._commit_register(meaning, meta)
        tone = self._commit_tone(meaning, meta)
        tags = self._commit_tags(meaning, meta)
        lineage_markers = self._commit_lineage_markers(meaning, meta)

        self._write_meaning_commit(
            identity, stance, register, tone, tags, lineage_markers
        )
        self._write_provenance(empty=False)
        self._append_audit(empty=False)
        return self.tp

    # ------------------------------------------------------------------
    # Extraction
    # ------------------------------------------------------------------

    def _extract_meaning_fields(self, tp: dict) -> dict:
        semantic = _ensure_dict(tp.get("semantic"))
        meta = _ensure_dict(tp.get("metadata"))
        return {
            "identity": _ensure_dict(semantic.get("identity")),
            "stance": _ensure_dict(semantic.get("stance")),
            "register": _ensure_dict(semantic.get("register")),
            "tone": _ensure_dict(semantic.get("tone")),
            "tags": _ensure_list(semantic.get("tags")),
            "lineage_markers": _ensure_dict(meta.get("lineage_markers")),
        }

    def _extract_meaning_adjacent_metadata(self, tp: dict) -> dict:
        meta = _ensure_dict(tp.get("metadata"))
        return {
            "semantic_layer_metadata": _ensure_dict(meta.get("semantic_layer_metadata")),
            "continuity_metadata": _ensure_dict(meta.get("continuity_metadata")),
            "expressive_metadata": _ensure_dict(meta.get("expressive_metadata")),
            "normalization_metadata": _ensure_dict(meta.get("normalization_metadata")),
            "identity_metadata": _ensure_dict(meta.get("identity_metadata")),
            "provenance": _ensure_dict(meta.get("provenance")),
            "provenance_metadata": _ensure_dict(meta.get("provenance_metadata")),
            "lineage_log": _ensure_list(tp.get("lineage_log")),
        }

    def _has_required_inputs(self, meaning: dict) -> bool:
        # Minimal: at least one of identity / stance / register / tone / tags present
        if meaning.get("identity"):
            return True
        if meaning.get("stance"):
            return True
        if meaning.get("register"):
            return True
        if meaning.get("tone"):
            return True
        if meaning.get("tags"):
            return True
        if meaning.get("lineage_markers"):
            return True
        return False

    # ------------------------------------------------------------------
    # Commit helpers (pass-through + light deterministic consolidation)
    # ------------------------------------------------------------------

    def _commit_identity(self, meaning: dict, meta: dict) -> dict:
        base = dict(meaning.get("identity") or {})
        id_meta = meta.get("identity_metadata") or {}
        cont = meta.get("continuity_metadata") or {}

        # Preserve IdOB fields; add continuity flags only if present and not already set
        if "continuity_flags" not in base:
            flags = _ensure_list(cont.get("continuity_flags") or id_meta.get("continuity_flags"))
            if flags:
                base["continuity_flags"] = list(flags)

        return base

    def _commit_stance(self, meaning: dict, meta: dict) -> dict:
        base = dict(meaning.get("stance") or {})
        expr = meta.get("expressive_metadata") or {}
        cont = meta.get("continuity_metadata") or {}

        # Light fill from expressive / continuity only when IdOB left a field empty
        if not base.get("certainty") and expr.get("certainty_hint"):
            base["certainty"] = str(expr.get("certainty_hint"))
        if not base.get("direction") and cont.get("direction"):
            base["direction"] = str(cont.get("direction"))

        return base

    def _commit_register(self, meaning: dict, meta: dict) -> dict:
        base = dict(meaning.get("register") or {})
        expr = meta.get("expressive_metadata") or {}

        if not base.get("formality") and expr.get("formality_hint"):
            base["formality"] = str(expr.get("formality_hint"))

        return base

    def _commit_tone(self, meaning: dict, meta: dict) -> dict:
        base = dict(meaning.get("tone") or {})
        expr = meta.get("expressive_metadata") or {}

        if not base.get("affect") and expr.get("affect_hint"):
            base["affect"] = str(expr.get("affect_hint"))

        return base

    def _commit_tags(self, meaning: dict, meta: dict) -> List[str]:
        tags = [str(t) for t in _ensure_list(meaning.get("tags"))]
        # Deterministic unique preserve-order
        seen = set()
        out: List[str] = []
        for t in tags:
            if t not in seen:
                seen.add(t)
                out.append(t)
        return out

    def _commit_lineage_markers(self, meaning: dict, meta: dict) -> dict:
        markers = dict(meaning.get("lineage_markers") or {})
        log = meta.get("lineage_log") or []

        # Derive identity_cycle from lineage_log if not already present
        if "identity_cycle" not in markers and log:
            cycles = [
                e.get("cycle")
                for e in log
                if isinstance(e, dict) and e.get("primitive") in ("IdOB", "idob") and e.get("cycle") is not None
            ]
            if cycles:
                markers["identity_cycle"] = max(int(c) for c in cycles)

        return markers

    def _commit_minimal_meaning(self, meaning: dict, meta: dict) -> None:
        """Replay-safe minimal commit when IdOB-refined fields are absent."""
        semantic = self.tp.setdefault("semantic", {})
        if not isinstance(semantic, dict):
            self.tp["semantic"] = {}
            semantic = self.tp["semantic"]

        # Write empty-but-present structures so downstream sees committed shape
        semantic["identity"] = {}
        semantic["stance"] = {}
        semantic["register"] = {}
        semantic["tone"] = {}
        semantic["tags"] = []

        meta_tp = self.tp.setdefault("metadata", {})
        if not isinstance(meta_tp, dict):
            self.tp["metadata"] = {}
            meta_tp = self.tp["metadata"]
        meta_tp["lineage_markers"] = {}

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def _write_meaning_commit(
        self,
        identity: dict,
        stance: dict,
        register: dict,
        tone: dict,
        tags: List[str],
        lineage_markers: dict,
    ) -> None:
        semantic = self.tp.setdefault("semantic", {})
        if not isinstance(semantic, dict):
            self.tp["semantic"] = {}
            semantic = self.tp["semantic"]

        semantic["identity"] = identity
        semantic["stance"] = stance
        semantic["register"] = register
        semantic["tone"] = tone
        semantic["tags"] = tags

        meta = self.tp.setdefault("metadata", {})
        if not isinstance(meta, dict):
            self.tp["metadata"] = {}
            meta = self.tp["metadata"]
        meta["lineage_markers"] = lineage_markers

    def _write_provenance(self, empty: bool = False) -> None:
        meta = self.tp.setdefault("metadata", {})
        if not isinstance(meta, dict):
            self.tp["metadata"] = {}
            meta = self.tp["metadata"]

        # Prefer provenance_metadata (upstream) then provenance
        prov_in = meta.get("provenance_metadata") or meta.get("provenance") or {}
        if not isinstance(prov_in, dict):
            prov_in = {}

        commit_id = prov_in.get("commit_id", "rbu_v1")
        sequence = list(prov_in.get("commit_sequence") or [])
        if "RBU" not in sequence:
            sequence = sequence + ["RBU"]

        # Write under metadata.provenance (RBU-owned entries)
        meta["provenance"] = {
            "origin": "RBU",
            "last_update": "RBU",
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
                "rbu_ref": {
                    "origin": "RBU",
                    "last_update": "RBU",
                    "empty": bool(empty),
                    "committed_fields": [
                        "semantic.identity",
                        "semantic.stance",
                        "semantic.register",
                        "semantic.tone",
                        "semantic.tags",
                        "metadata.lineage_markers",
                    ],
                }
            }
        )


def run(tp: dict) -> dict:
    """Functional entrypoint matching rbu_py_struc_pgm.md."""
    return RBU(tp).process()
