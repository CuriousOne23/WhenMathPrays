from dataclasses import asdict
from typing import Any, Dict, List

from tp_substrate import TP, init_tp, clone_tp
from primitives_pathA_short import (
    InB, IIInB, IE,
    CEx, CE, ISc, TPU,
    SOB, SROB, CnOB, SmOB, SSG,
    RBU, RB, TR, TRU, RTU, CTP,
    IdOB, OuBA,
)


PrimitiveFn = Any  # simple alias; each primitive is a callable(tp) -> tp


PRIMITIVES: List[PrimitiveFn] = [
    InB, IIInB, IE,
    CEx, CE, ISc, TPU,
    SOB, SROB, CnOB, SmOB, SSG,
    RBU, RB, TR, TRU, RTU, CTP,
    IdOB, OuBA,
]


def primitive_notes(name: str, tp: TP) -> str:
    """Optional human-readable notes per primitive."""
    macro = {
        "InB": "Intake",
        "IIInB": "Intake",
        "IE": "Intake",
        "CEx": "Correction",
        "CE": "Correction",
        "ISc": "Correction",
        "TPU": "Correction",
        "SOB": "OB-Set",
        "SROB": "OB-Set",
        "CnOB": "OB-Set",
        "SmOB": "OB-Set",
        "SSG": "OB-Set",
        "RBU": "Routing",
        "RB": "Routing",
        "TR": "Routing",
        "TRU": "Routing",
        "RTU": "Routing",
        "CTP": "Routing",
        "IdOB": "Semantic",
        "OuBA": "Final Commit",
    }.get(name, "Unknown")

    if name == "SOB":
        return f"[{macro}] Segments: {tp.struct_segments}; Segment tokens: {tp.segment_tokens}"
    if name == "SROB":
        return f"[{macro}] Roles: {tp.struct_roles}; Role segments: {tp.role_segments}"
    if name == "TR":
        return f"[{macro}] Thought Router placeholder: {tp.routing_metadata.get('thought_router_note', 'no note')}"
    if name == "TRU":
        return f"[{macro}] Truth relation: {tp.truth_relation}"
    if name == "IdOB":
        return f"[{macro}] Semantic core: {tp.semantic_core}"
    return f"[{macro}]"


def run_pathA_short(raw_text: str) -> Dict[str, Any]:
    """Run the short Path-A flow on a sentence and return TP + trace."""
    tp = init_tp(raw_text)
    trace: List[Dict[str, Any]] = []

    for fn in PRIMITIVES:
        input_snapshot = clone_tp(tp)
        tp = fn(tp)
        trace.append({
            "primitive": fn.__name__,
            "input": asdict(input_snapshot),
            "output": asdict(tp),
            "notes": primitive_notes(fn.__name__, tp),
        })

    return {
        "final_tp": asdict(tp),
        "trace": trace,
    }
