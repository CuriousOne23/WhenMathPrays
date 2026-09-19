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


def _minimal_idob_selection(tp: TP) -> TP:
    selected_ops = []

    if "agent-action" in tp.constraints_matched:
        selected_ops.append("agent_action")

    if "action-relation" in tp.constraints_matched:
        selected_ops.append("action_patient")

    if "relation-patient" in tp.constraints_matched:
        selected_ops.append("relation_modifier")

    if tp.semantic_adjacent_cues:
        selected_ops.append("modifier_resolution")

    tp.semantic_core = {
        "selected_ops": selected_ops,
        "agent": " ".join(tp.role_segments.get("agent", [])),
        "action": " ".join(tp.role_segments.get("action", [])),
        "patient": " ".join(tp.role_segments.get("patient", [])),
        "modifiers": tp.semantic_adjacent_cues,
    }

    if not hasattr(tp, "trace"):
        tp.trace = []
    tp.trace.append({
        "primitive": "IdOB",
        "notes": "[Semantic]",
        "selected_ops": selected_ops,
        "semantic_core": tp.semantic_core,
        "token_relations": {
            "agent": " ".join(tp.role_segments.get("agent", [])),
            "action": " ".join(tp.role_segments.get("action", [])),
            "relation": " ".join(tp.role_segments.get("relation", [])),
            "patient": " ".join(tp.role_segments.get("patient", [])),
            "modifiers": tp.semantic_adjacent_cues
        }
    })
    return tp


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
    if name == "CnOB":
        return f"[{macro}] matched={tp.constraints_matched}; unmatched={tp.constraints_unmatched}; residue={tp.constraint_residue}"
    if name == "SmOB":
        return f"[{macro}] operations={tp.smoothing_operations}; semantic_adjacent_cues={tp.semantic_adjacent_cues}; residue={tp.smoothing_residue}"
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
        if fn.__name__ == "IdOB":
            tp = _minimal_idob_selection(tp)
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
