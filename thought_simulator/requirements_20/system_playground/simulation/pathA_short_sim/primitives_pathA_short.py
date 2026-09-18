from typing import List
from tp_substrate import TP


# ----- helpers (coarse heuristics) -------------------------------------------------


def _simple_tokenize(text: str) -> List[str]:
    return text.replace(".", " .").split()


def _normalize_tokens(tokens: List[str]) -> List[str]:
    return [t.lower() for t in tokens]


def _simple_segments(tokens: List[str]) -> List[str]:
    # Very coarse: DET/ADJ/NOUN → NP, VERB → VP, PREP → PP
    # This is just to give you a feel; you can refine later.
    segments = []
    has_verb = any(t.endswith("s") for t in tokens)  # crude verb heuristic
    if has_verb:
        segments = ["NP", "VP"]
        if "over" in tokens or "under" in tokens or "on" in tokens:
            segments.append("PP")
            segments.append("NP")
    else:
        segments = ["NP"]
    return segments


def _simple_roles(segments: List[str]) -> List[str]:
    roles = []
    for seg in segments:
        if seg == "NP" and not roles:
            roles.append("agent")
        elif seg == "VP":
            roles.append("action")
        elif seg == "PP":
            roles.append("relation")
        elif seg == "NP":
            roles.append("patient")
        else:
            roles.append("modifier")
    return roles


# ----- primitives ------------------------------------------------------------------


def InB(tp: TP) -> TP:
    tp.tokens = _simple_tokenize(tp.raw_text)
    return tp


def IIInB(tp: TP) -> TP:
    # For now, assume no defects.
    tp.defects = []
    return tp


def IE(tp: TP) -> TP:
    tp.tokens = _normalize_tokens(tp.tokens)
    tp.normalized_text = " ".join(tp.tokens)
    return tp


def CEx(tp: TP) -> TP:
    # Stub: no correction needed.
    tp.corrections = ["no_change"]
    return tp


def CE(tp: TP) -> TP:
    # Choose first candidate.
    if tp.corrections:
        tp.normalized_text = tp.normalized_text  # no-op for now
    return tp


def ISc(tp: TP) -> TP:
    tp.correction_score = 1.0
    return tp


def TPU(tp: TP) -> TP:
    tp.commit_flags["correction"] = True
    return tp


def SOB(tp: TP) -> TP:
    tp.struct_segments = _simple_segments(tp.tokens)
    return tp


def SROB(tp: TP) -> TP:
    tp.struct_roles = _simple_roles(tp.struct_segments)
    return tp


def CnOB(tp: TP) -> TP:
    constraints = []
    roles = tp.struct_roles
    for i in range(len(roles) - 1):
        pair = f"{roles[i]}-{roles[i+1]}"
        constraints.append(pair)
    tp.constraints = constraints
    return tp


def SmOB(tp: TP) -> TP:
    # Stub: mark geometry as smoothed.
    tp.smoothed_geometry = True
    return tp


def SSG(tp: TP) -> TP:
    tp.structural_vector_frozen = True
    return tp


def RBU(tp: TP) -> TP:
    # Very coarse routing metadata from roles.
    meta = {}
    if "agent" in tp.struct_roles:
        meta["agent_role_index"] = tp.struct_roles.index("agent")
    if "action" in tp.struct_roles:
        meta["action_role_index"] = tp.struct_roles.index("action")
    if "patient" in tp.struct_roles:
        meta["patient_role_index"] = tp.struct_roles.index("patient")
    tp.routing_metadata = meta
    return tp


def RB(tp: TP) -> TP:
    tp.routing_decision = "semantic"
    return tp


def RTU(tp: TP) -> TP:
    tp.routing_committed = True
    return tp


def CTP(tp: TP) -> TP:
    tp.commit_flags["routing"] = True
    return tp


def IdOB(tp: TP) -> TP:
    # Extremely coarse semantic core: use positions.
    tokens = tp.tokens
    core = {}

    # Agent: first noun-ish token (just take first non-stopword).
    if tokens:
        core["agent"] = tokens[0]

    # Action: crude verb heuristic: token ending with "s".
    action = next((t for t in tokens if t.endswith("s")), None)
    if action:
        core["action"] = action

    # Patient: last noun-ish token.
    core["patient"] = tokens[-2] if len(tokens) > 2 else tokens[-1]

    # Modifiers: everything between agent and patient that isn't action.
    modifiers = []
    if "agent" in core and "patient" in core:
        try:
            a_idx = tokens.index(core["agent"])
            p_idx = tokens.index(core["patient"])
            for i in range(a_idx + 1, p_idx):
                if tokens[i] != core.get("action"):
                    modifiers.append(tokens[i])
        except ValueError:
            pass
    core["modifiers"] = modifiers

    tp.semantic_core = core
    return tp


def TR(tp: TP) -> TP:
    # Stub: treat as descriptive factual if no defects.
    tp.truth_relation = "descriptive_factual" if not tp.defects else "uncertain"
    return tp


def OuBA(tp: TP) -> TP:
    tp.commit_flags["pathA_complete"] = True
    return tp
