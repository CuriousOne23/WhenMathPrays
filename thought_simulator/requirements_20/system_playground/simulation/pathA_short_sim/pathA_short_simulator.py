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
    semantic_operations: List[str] = []

    if "theme-state" in tp.constraints_matched:
        semantic_operations.append("theme_state")

    if "state-location" in tp.constraints_matched:
        semantic_operations.append("state_location")

    if "query-focus-predicate" in tp.constraints_matched:
        semantic_operations.append("query_resolution")

        query_focus_text = " ".join(tp.role_segments.get("query_focus", []))
        has_location_role = "location" in tp.struct_roles
        has_state_role = "state" in tp.struct_roles

        if query_focus_text in ("where", "where?") or has_location_role:
            semantic_operations.append("interrogative_relation_request")
        elif query_focus_text in ("why", "why?") or has_state_role:
            semantic_operations.append("interrogative_property_request")
        else:
            semantic_operations.append("interrogative_identity_request")

    if "modifier_chain" in tp.semantic_adjacent_cues or "relation" in tp.struct_roles:
        semantic_operations.append("nested_modifier_resolution")

    if "nested_state_link" in tp.semantic_adjacent_cues or "nested_locative_link" in tp.semantic_adjacent_cues or (
        "state" in tp.struct_roles and "location" in tp.struct_roles
    ):
        semantic_operations.append("nested_state_location_resolution")

    if "agent-action" in tp.constraints_matched:
        semantic_operations.append("agent_action")

    if "action-relation" in tp.constraints_matched:
        semantic_operations.append("action_patient")

    if "relation-patient" in tp.constraints_matched:
        semantic_operations.append("relation_modifier")

    if tp.semantic_adjacent_cues:
        semantic_operations.append("modifier_resolution")

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
        "selected_ops": semantic_operations,
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

    idob_packet = tp.idob
    if isinstance(idob_packet, dict):
        # Keep IdOB packet semantic payload in sync unless the contract expects null.
        if idob_packet.get("meaning_semantics") is not None:
            idob_packet["meaning_semantics"] = dict(tp.semantic_core)
            idob_packet["meaning_semantics_prime"] = dict(tp.semantic_core)

    if not hasattr(tp, "trace"):
        tp.trace = []
    tp.trace.append({
        "primitive": "IdOB",
        "notes": "[Semantic]",
        "idob_packet": tp.idob,
        "selected_ops": semantic_operations,
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
        return (
            f"[{macro}] constraints_matched={tp.constraints_matched}; "
            f"constraints_unmatched={tp.constraints_unmatched}; "
            f"constraint_residue={tp.constraint_residue}"
        )
    if name == "SmOB":
        return (
            f"[{macro}] smoothing_operations={tp.smoothing_operations}; "
            f"semantic_adjacent_cues={tp.semantic_adjacent_cues}; "
            f"basin_residue={tp.smoothing_residue}"
        )
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
        input_tp_snapshot = clone_tp(tp)
        tp = fn(tp)
        if fn.__name__ == "IdOB":
            tp = _minimal_idob_selection(tp)

        primitive_trace_entry = {
            "primitive": fn.__name__,
            "input": asdict(input_tp_snapshot),
            "output": asdict(tp),
            "notes": primitive_notes(fn.__name__, tp),
        }

        bridge_trace_entry = tp.bridge_trace.get(fn.__name__, {
            "mode": "n/a",
            "committed_adapter_used": False,
            "legacy_fallback_used": False,
            "detail": "primitive does not use intake bridge adapters",
        })
        primitive_trace_entry["bridge_trace"] = bridge_trace_entry

        # Carry primitive-level diagnostic payloads (e.g., token_relations)
        # from tp.trace into the public run trace consumed by run_examples.py.
        if hasattr(tp, "trace") and tp.trace:
            latest = tp.trace[-1]
            if latest.get("primitive") == fn.__name__:
                for key in (
                    "constraints_matched",
                    "constraints_unmatched",
                    "constraint_residue",
                    "smoothing_operations",
                    "semantic_adjacent_cues",
                    "basin_residue",
                    "idob_packet",
                    "selected_ops",
                    "semantic_core",
                    "token_relations",
                ):
                    if key in latest:
                        primitive_trace_entry[key] = latest[key]

        trace.append(primitive_trace_entry)

    return {
        "final_tp": asdict(tp),
        "trace": trace,
    }
