"""
IdOB primitive — structure-to-meaning hop (Path A).

Implementation template: testbenches/idob_structure_to_meaning/11_idob_core/
See 11_idob_core/idob_core.md.

The 10-geometry identity-envelope walk (formation…closure, L1/K) is archived
with path_a/identity/idob_lifecycle_archive.yaml. It is not this meaning vector.

Public surface kept for Path A runners:
  get_primitive_name(), IdOB(tp).process(), process(tp)
"""
from __future__ import annotations

import copy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any, Optional

PRIMITIVE_NAME = "idob"

_CORE_PATH = (
    Path(__file__).resolve().parents[2]
    / "testbenches"
    / "idob_structure_to_meaning"
    / "11_idob_core"
    / "idob.py"
)


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


def _load_core():
    spec = spec_from_file_location("idob_core_kernel", _CORE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load 11 kernel: {_CORE_PATH}")
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _flatten_flags(tp: dict, pkt: dict) -> dict:
    """HLR-era runners read flags on the TP root. Packet also lives under tp['idob']."""
    tp["idob_complete"] = bool(pkt.get("idob_complete"))
    tp["path_b_eligible"] = bool(pkt.get("path_b_eligible"))
    tp["ready_for_ouba"] = bool(pkt.get("ready_for_ouba"))
    semantic = tp.setdefault("semantic", {})
    if pkt.get("meaning_delta_h") is not None:
        semantic["meaning_delta_h"] = pkt.get("meaning_delta_h")
    return tp


def process(tp: Optional[dict] = None, mode: str = "general", **kwargs) -> dict:
    core = _load_core()
    incoming = copy.deepcopy(tp) if isinstance(tp, dict) else {}
    # card_id / utterance may sit on the TP or under idob / kwargs
    if "card_id" not in kwargs:
        kwargs["card_id"] = incoming.get("card_id") or (incoming.get("idob") or {}).get("card_id")
    if "utterance" not in kwargs:
        kwargs["utterance"] = incoming.get("utterance") or (incoming.get("idob") or {}).get("utterance")
    out = core.process(incoming, mode=mode, **kwargs)
    pkt = out.get("idob") or {}
    return _flatten_flags(out, pkt)


class IdOB:
    """Identity-conditioned structure-to-meaning hop after routing commitment."""

    def __init__(self, tp: Optional[dict] = None):
        self.tp = copy.deepcopy(tp) if tp is not None else {}

    def process(self, mode: str = "general", **kwargs) -> dict:
        self.tp = process(self.tp, mode=mode, **kwargs)
        return self.tp
