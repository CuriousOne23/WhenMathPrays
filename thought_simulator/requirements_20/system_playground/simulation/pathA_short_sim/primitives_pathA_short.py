from pathlib import Path
from typing import Any, Dict, List

import yaml
from tp_substrate import TP

try:
    from support.dictionaries import (  # type: ignore
        load_constraint_rules,
        load_role_patterns,
        load_segment_patterns,
        load_semantic_rules,
        load_token_classes,
    )
except ImportError:
    _DICT_DIR = Path(__file__).resolve().parent / "support" / "dictionaries"

    def _load_yaml_dictionary(file_name: str, root_key: str) -> Any:
        file_path = _DICT_DIR / file_name
        if not file_path.exists():
            return {} if root_key.endswith("patterns") or root_key.endswith("classes") else []
        with file_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data.get(root_key, {} if root_key.endswith("patterns") or root_key.endswith("classes") else [])

    def load_token_classes() -> Dict[str, str]:
        return _load_yaml_dictionary("token_classes.yaml", "token_classes")

    def load_segment_patterns() -> Dict[str, List[str]]:
        return _load_yaml_dictionary("segment_patterns.yaml", "segment_patterns")

    def load_role_patterns() -> Dict[str, List[str]]:
        return _load_yaml_dictionary("role_patterns.yaml", "role_patterns")

    def load_constraint_rules() -> List[str]:
        return _load_yaml_dictionary("constraint_rules.yaml", "constraint_rules")

    def load_semantic_rules() -> Dict[str, str]:
        return _load_yaml_dictionary("semantic_rules.yaml", "semantic_rules")


# ----- helpers (coarse heuristics) -------------------------------------------------


def _simple_tokenize(text: str) -> List[str]:
    return text.replace(".", " .").split()


def _normalize_tokens(tokens: List[str]) -> List[str]:
    return [t.lower() for t in tokens]


def _match_np_with_pattern(token_classes: List[str], start: int, pattern: List[str]) -> int:
    if not pattern or "NOUN" not in pattern:
        return 0
    i = start
    if i < len(token_classes) and token_classes[i] == "DET":
        i += 1
    adj_seen = False
    while i < len(token_classes) and token_classes[i] == "ADJ":
        adj_seen = True
        i += 1
    if i < len(token_classes) and token_classes[i] == "NOUN":
        # If ADJ is part of pattern, allow one or many ADJ.
        if "ADJ" in pattern and not adj_seen and "DET" in pattern:
            return 0
        return i - start + 1
    return 0


def _extract_segments(tokens: List[str]) -> Dict[str, Any]:
    token_classes_map = load_token_classes()
    segment_patterns = load_segment_patterns()

    classes = [token_classes_map.get(tok, "UNK") for tok in tokens]
    segments: List[str] = []
    segment_tokens: List[List[str]] = []

    i = 0
    while i < len(tokens):
        if classes[i] == "UNK":
            i += 1
            continue

        np_pattern = segment_patterns.get("NP", [])
        np_len = _match_np_with_pattern(classes, i, np_pattern)
        if np_len > 0:
            segments.append("NP")
            segment_tokens.append(tokens[i:i + np_len])
            i += np_len
            continue

        matched = False
        for seg_name, pattern in segment_patterns.items():
            if seg_name == "NP" or not pattern:
                continue
            plen = len(pattern)
            if classes[i:i + plen] == pattern:
                segments.append(seg_name)
                segment_tokens.append(tokens[i:i + plen])
                i += plen
                matched = True
                break
        if matched:
            continue

        i += 1

    return {
        "segments": segments,
        "segment_tokens": segment_tokens,
    }


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
    extracted = _extract_segments(tp.tokens)
    tp.struct_segments = extracted["segments"]
    tp.segment_tokens = extracted["segment_tokens"]
    return tp


def SROB(tp: TP) -> TP:
    role_patterns = load_role_patterns()
    segment_counts: Dict[str, int] = {}
    roles: List[str] = []
    role_segments: Dict[str, List[str]] = {}

    for idx, seg in enumerate(tp.struct_segments):
        options = role_patterns.get(seg, ["modifier"])
        seg_count = segment_counts.get(seg, 0)
        role = options[min(seg_count, len(options) - 1)]
        roles.append(role)
        role_segments.setdefault(role, []).extend(tp.segment_tokens[idx] if idx < len(tp.segment_tokens) else [])
        segment_counts[seg] = seg_count + 1

    tp.struct_roles = roles
    tp.role_segments = role_segments
    return tp


def CnOB(tp: TP) -> TP:
    allowed = set(load_constraint_rules())
    constraints = []
    roles = tp.struct_roles
    for i in range(len(roles) - 1):
        pair = f"{roles[i]}-{roles[i+1]}"
        if pair in allowed:
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


def TR(tp: TP) -> TP:
    # Placeholder Thought Router primitive.
    tp.routing_metadata["thought_router_note"] = "TR placeholder executed (no-op)"
    return tp


def RTU(tp: TP) -> TP:
    tp.routing_committed = True
    return tp


def CTP(tp: TP) -> TP:
    tp.commit_flags["routing"] = True
    return tp


def IdOB(tp: TP) -> TP:
    semantic_rules = load_semantic_rules()
    tokens = tp.tokens
    core: Dict[str, Any] = {}

    spans = []
    cursor = 0
    for seg_tokens in tp.segment_tokens:
        start = cursor
        end = cursor + len(seg_tokens)
        spans.append((start, end))
        cursor = end

    np_segments = [seg for seg, seg_tokens in zip(tp.struct_segments, tp.segment_tokens) if seg == "NP"]
    np_tokens = [seg_tokens for seg, seg_tokens in zip(tp.struct_segments, tp.segment_tokens) if seg == "NP"]

    if semantic_rules.get("agent") == "first_np" and np_tokens:
        core["agent"] = " ".join(np_tokens[0])
    elif tp.role_segments.get("agent"):
        core["agent"] = " ".join(tp.role_segments["agent"])

    if semantic_rules.get("action") == "first_verb":
        action_token = None
        for seg, seg_tokens in zip(tp.struct_segments, tp.segment_tokens):
            if seg == "VP" and seg_tokens:
                action_token = seg_tokens[0]
                break
        if action_token is None:
            action_token = next((t for t in tokens if t.endswith("s")), None)
        if action_token:
            core["action"] = action_token

    if semantic_rules.get("patient") == "last_np" and np_tokens:
        core["patient"] = " ".join(np_tokens[-1])
    elif tp.role_segments.get("patient"):
        core["patient"] = " ".join(tp.role_segments["patient"])

    modifiers: List[str] = []
    if semantic_rules.get("modifiers") == "between_agent_patient":
        agent_i = None
        patient_i = None
        for i, role in enumerate(tp.struct_roles):
            if role == "agent" and agent_i is None:
                agent_i = i
            if role == "patient":
                patient_i = i

        if agent_i is not None and patient_i is not None and agent_i < patient_i:
            for i in range(agent_i + 1, patient_i):
                for tok in tp.segment_tokens[i]:
                    if tok != core.get("action"):
                        modifiers.append(tok)
    core["modifiers"] = modifiers

    tp.semantic_core = core
    return tp


def TRU(tp: TP) -> TP:
    # Stub: treat as descriptive factual if no defects.
    tp.truth_relation = "descriptive_factual" if not tp.defects else "uncertain"
    return tp


def OuBA(tp: TP) -> TP:
    tp.commit_flags["pathA_complete"] = True
    return tp
