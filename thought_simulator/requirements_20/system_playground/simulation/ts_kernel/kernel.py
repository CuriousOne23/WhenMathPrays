"""Kernel loop: schedule from yaml names, TP residency, tick."""
from __future__ import annotations

import copy
from typing import Any, Dict, List

from .legality import check_spec
from .registry import load
from .replay import freeze


def run_pipeline(spec: List[str], tp_in: Dict[str, Any], mode: str = "general") -> Dict[str, Any]:
    names = check_spec(spec)
    tp = copy.deepcopy(tp_in) if isinstance(tp_in, dict) else {}
    trace = []
    for tick, name in enumerate(names):
        module = load(name)
        tp = module.process(tp, mode=mode)
        if not isinstance(tp, dict):
            raise TypeError("{0}.process did not return a dict TP".format(name))
        trace.append({"tick": tick, "name": name, "freeze": freeze(tp)})
    return {"tp": tp, "spec": names, "trace": trace, "freeze": freeze(tp)}
