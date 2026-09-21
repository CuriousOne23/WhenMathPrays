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

    if "theme-state" in tp.constraints_matched:
        selected_ops.append("theme_state")

    if "state-location" in tp.constraints_matched:
        selected_ops.append("state_location")

    if "query-focus-predicate" in tp.constraints_matched:
        selected_ops.append("query_resolution")

        q_focus = " ".join(tp.role_segments.get("query_focus", []))
        has_location = "location" in tp.struct_roles
        has_state = "state" in tp.struct_roles

        if q_focus in ("where", "where?") or has_location:
            selected_ops.append("interrogative_relation_request")
        elif q_focus in ("why", "why?") or has_state:
            selected_ops.append("interrogative_property_request")
        else:
            selected_ops.append("interrogative_identity_request")

    if "modifier_chain" in tp.semantic_adjacent_cues or "relation" in tp.struct_roles:
        selected_ops.append("nested_modifier_resolution")

    if "nested_state_link" in tp.semantic_adjacent_cues or "nested_locative_link" in tp.semantic_adjacent_cues or (
        "state" in tp.struct_roles and "location" in tp.struct_roles
    ):
        selected_ops.append("nested_state_location_resolution")

    if "agent-action" in tp.constraints_matched:
        selected_ops.append("agent_action")

    if "action-relation" in tp.constraints_matched:
        selected_ops.append("action_patient")

    if "relation-patient" in tp.constraints_matched:
        selected_ops.append("relation_modifier")

    if tp.semantic_adjacent_cues:
        selected_ops.append("modifier_resolution")

    query_focus = " ".join(tp.role_segments.get("query_focus", []))
    predicate = " ".join(tp.role_segments.get("predicate", []))
    theme = " ".join(tp.role_segments.get("theme", tp.role_segments.get("agent", [])))
    relation_modifiers = " ".join(tp.role_segments.get("relation", []))

    location_tokens = tp.role_segments.get("location", [])
    has_location = bool(location_tokens)

    state_tokens: List[str] = []
    if has_location:
        for seg, role, seg_tokens in zip(tp.struct_segments, tp.struct_roles, tp.segment_tokens):
            if role == "state" and seg in ("CP", "ST"):
                state_tokens.extend(seg_tokens)
    else:
        for seg, role, seg_tokens in zip(tp.struct_segments, tp.struct_roles, tp.segment_tokens):
            if role == "state" and seg != "CP":
                state_tokens.extend(seg_tokens)

    if not state_tokens:
        state_tokens = tp.role_segments.get("state", [])

    tp.semantic_core = {
        "selected_ops": selected_ops,
        "query_focus": query_focus,
        "predicate": predicate,
        "theme": theme,
        "relation_modifiers": relation_modifiers,
        "complement": " ".join(location_tokens if location_tokens else state_tokens),
        "agent": theme,
        "state": " ".join(state_tokens),
        "location": " ".join(location_tokens),
        "action": " ".join(tp.role_segments.get("action", [])),
        "patient": " ".join(tp.role_segments.get("patient", [])),
        "modifiers": [
            c
            for c in tp.semantic_adjacent_cues
            if c not in ("copular_state_link", "locative_link", "interrogative_scope")
        ],
    }

    if isinstance(tp.idob, dict):
        # Keep IdOB packet semantic payload in sync unless the contract expects null.
        if tp.idob.get("meaning_semantics") is not None:
            tp.idob["meaning_semantics"] = dict(tp.semantic_core)
            tp.idob["meaning_semantics_prime"] = dict(tp.semantic_core)

    if not hasattr(tp, "trace"):
        tp.trace = []
    tp.trace.append({
        "primitive": "IdOB",
        "notes": "[Semantic]",
        "idob_packet": tp.idob,
        "selected_ops": selected_ops,
        "semantic_core": tp.semantic_core,
        "token_relations": {
            "query_focus": " ".join(tp.role_segments.get("query_focus", [])),
            "predicate": " ".join(tp.role_segments.get("predicate", [])),
            "theme": " ".join(tp.role_segments.get("theme", [])),
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

        trace_entry = {
            "primitive": fn.__name__,
            "input": asdict(input_snapshot),
            "output": asdict(tp),
            "notes": primitive_notes(fn.__name__, tp),
        }

        bridge_payload = tp.bridge_trace.get(fn.__name__, {
            "mode": "n/a",
            "committed_adapter_used": False,
            "legacy_fallback_used": False,
            "detail": "primitive does not use intake bridge adapters",
        })
        trace_entry["bridge_trace"] = bridge_payload

        # Carry primitive-level diagnostic payloads (e.g., token_relations)
        # from tp.trace into the public run trace consumed by run_examples.py.
        if hasattr(tp, "trace") and tp.trace:
            latest = tp.trace[-1]
            if latest.get("primitive") == fn.__name__:
                for key in (
                    "matched",
                    "unmatched",
                    "residue",
                    "operations",
                    "semantic_adjacent_cues",
                    "idob_packet",
                    "selected_ops",
                    "semantic_core",
                    "token_relations",
                ):
                    if key in latest:
                        trace_entry[key] = latest[key]

        trace.append(trace_entry)

    return {
        "final_tp": asdict(tp),
        "trace": trace,
    }
