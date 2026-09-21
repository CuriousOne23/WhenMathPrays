from pathlib import Path
from typing import Any, Dict, List

import yaml
from ie_compat_intake import build_committed_stream
from tp_substrate import TP

try:
    from thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.cnob_rulechecker import check_constraints  # type: ignore
except ImportError:
    def check_constraints(struct_roles: List[str]) -> Any:
        allowed = set(load_constraint_rules())
        all_pairs = [f"{struct_roles[i]}-{struct_roles[i+1]}" for i in range(max(0, len(struct_roles) - 1))]
        matched = [pair for pair in all_pairs if pair in allowed]
        unmatched = [pair for pair in all_pairs if pair not in allowed]
        residue = [pair for pair in allowed if pair not in matched]
        return matched, unmatched, residue

try:
    from thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.smob_rulechecker import apply_smoothing  # type: ignore
except ImportError:
    def apply_smoothing(segment_tokens: List[List[str]], struct_roles: List[str]) -> Any:
        ops: List[str] = []
        cues: List[str] = []
        residue: List[str] = []

        for i in range(max(0, len(struct_roles) - 1)):
            ops.append(f"smooth:{struct_roles[i]}->{struct_roles[i+1]}")

        for seg_tokens, role in zip(segment_tokens, struct_roles):
            if role == "relation":
                cues.extend(seg_tokens)

        if not cues:
            residue.append("no_relation_cues")
        return ops, cues, residue

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


def _record_bridge(
    tp: TP,
    primitive: str,
    committed_adapter_used: bool,
    legacy_fallback_used: bool,
    detail: str,
) -> None:
    mode = "committed"
    if committed_adapter_used and legacy_fallback_used:
        mode = "mixed"
    elif legacy_fallback_used and not committed_adapter_used:
        mode = "legacy"
    elif not committed_adapter_used and not legacy_fallback_used:
        mode = "n/a"

    tp.bridge_trace[primitive] = {
        "mode": mode,
        "committed_adapter_used": committed_adapter_used,
        "legacy_fallback_used": legacy_fallback_used,
        "detail": detail,
    }


def _committed_segment_tokens(committed_stream: Dict[str, Any]) -> List[List[str]]:
    tokens = committed_stream.get("tokens", [])
    segments = committed_stream.get("segments", [])
    by_id = {int(t.get("token_id", 0)): t for t in tokens}

    grouped: List[List[str]] = []
    for seg in sorted(segments, key=lambda s: int(s.get("segment_id", 0))):
        start_id = int(seg.get("start_token_id", 0))
        end_id = int(seg.get("end_token_id", 0))
        seg_tokens: List[str] = []
        for token_id in range(start_id, end_id + 1):
            tok = by_id.get(token_id)
            if not tok:
                continue
            seg_tokens.append(str(tok.get("normalized", tok.get("surface", ""))))
        if seg_tokens:
            grouped.append(seg_tokens)
    return grouped


def _derive_segment_label_from_role(role: str) -> str:
    role_to_segment = {
        "query_focus": "WQ",
        "predicate": "IQ",
        "theme": "NP",
        "agent": "NP",
        "patient": "NP",
        "action": "VP",
        "relation": "PP",
        "location": "LOC",
        "state": "AP",
    }
    return role_to_segment.get(role, "NP")


def _rule_based_segment_label(seg_tokens: List[str], previous_labels: List[str]) -> str:
    if not seg_tokens:
        return "NP"

    wh_words = {"who", "what", "where", "when", "why", "how"}
    aux_q = {"is", "are", "was", "were", "do", "does", "did", "can", "could", "will", "would", "shall", "should"}
    copular = {"is", "are", "was", "were", "be", "been", "being"}
    state_verbs = {"stay", "stays", "stayed", "remain", "remains", "remained"}
    preps = {"in", "on", "at", "under", "over", "into", "onto", "from", "to", "of", "with", "by", "for"}
    rel_markers = {"that", "which", "who", "whom", "whose"}
    determiners = {"the", "a", "an", "this", "that", "these", "those", "my", "your", "our", "their"}
    pronouns = {"i", "you", "he", "she", "it", "we", "they"}

    first = seg_tokens[0]
    non_punct = [t for t in seg_tokens if t.isalnum()]
    last_label = previous_labels[-1] if previous_labels else ""

    if first in wh_words:
        return "WQ"
    if first in rel_markers and len(seg_tokens) > 1:
        return "RELC"
    if first in aux_q and last_label == "WQ":
        return "IQ"
    if first in copular:
        return "CP"
    if first in state_verbs:
        return "ST"
    if first in preps:
        return "LOC"

    # If this chunk follows a copular/auxiliary chunk and is short/non-determiner-led,
    # treat it as adjectival complement.
    if last_label in ("CP", "IQ") and first not in determiners and first not in pronouns and len(non_punct) <= 2:
        return "AP"

    return "NP"


def _split_and_label_committed_segment(seg_tokens: List[str], previous_labels: List[str]) -> Dict[str, List[Any]]:
    wh_words = {"who", "what", "where", "when", "why", "how"}
    aux_q = {"is", "are", "was", "were", "do", "does", "did", "can", "could", "will", "would", "shall", "should"}
    copular = {"is", "are", "was", "were", "be", "been", "being"}
    state_verbs = {"stay", "stays", "stayed", "remain", "remains", "remained"}
    preps = {"in", "on", "at", "under", "over", "into", "onto", "from", "to", "of", "with", "by", "for"}
    rel_markers = {"that", "which", "who", "whom", "whose"}
    determiners = {"the", "a", "an", "this", "that", "these", "those", "my", "your", "our", "their"}
    punctuation = {".", "!", "?", ",", ";", ":"}

    labels: List[str] = []
    chunks: List[List[str]] = []

    i = 0
    while i < len(seg_tokens):
        tok = seg_tokens[i]
        if tok in punctuation:
            i += 1
            continue

        if tok in wh_words:
            labels.append("WQ")
            chunks.append([tok])
            i += 1
            continue

        if tok in rel_markers:
            labels.append("RELC")
            chunks.append([tok])
            i += 1
            continue

        if tok in aux_q and labels and labels[-1] == "WQ":
            labels.append("IQ")
            chunks.append([tok])
            i += 1
            continue

        if tok in copular:
            labels.append("CP")
            chunks.append([tok])
            i += 1
            continue

        if tok in state_verbs:
            labels.append("ST")
            chunks.append([tok])
            i += 1
            continue

        if tok in preps:
            j = i + 1
            loc_chunk = [tok]
            while j < len(seg_tokens):
                nxt = seg_tokens[j]
                if nxt in punctuation:
                    break
                if nxt in wh_words or nxt in aux_q or nxt in copular or nxt in state_verbs or nxt in rel_markers:
                    break
                loc_chunk.append(nxt)
                j += 1
            labels.append("LOC")
            chunks.append(loc_chunk)
            i = j
            continue

        j = i
        phrase_chunk: List[str] = []
        while j < len(seg_tokens):
            nxt = seg_tokens[j]
            if nxt in punctuation:
                break
            if j > i and (nxt in wh_words or nxt in aux_q or nxt in copular or nxt in state_verbs or nxt in preps or nxt in rel_markers):
                break
            phrase_chunk.append(nxt)
            j += 1

        inferred = _rule_based_segment_label(phrase_chunk, previous_labels + labels)
        if inferred == "NP" and labels and labels[-1] in ("CP", "IQ", "ST"):
            if phrase_chunk and phrase_chunk[0] not in determiners:
                inferred = "AP"

        labels.append(inferred)
        chunks.append(phrase_chunk)
        i = j

    if not labels:
        fallback_label = _rule_based_segment_label(seg_tokens, previous_labels)
        return {
            "labels": [fallback_label],
            "chunks": [seg_tokens],
        }

    return {
        "labels": labels,
        "chunks": chunks,
    }


def _adapter_segments_from_committed(committed_stream: Dict[str, Any]) -> Dict[str, Any]:
    tokens = committed_stream.get("tokens", [])
    segments = committed_stream.get("segments", [])
    by_id = {int(t.get("token_id", 0)): t for t in tokens}

    struct_segments: List[str] = []
    segment_tokens: List[List[str]] = []
    for seg in sorted(segments, key=lambda s: int(s.get("segment_id", 0))):
        start_id = int(seg.get("start_token_id", 0))
        end_id = int(seg.get("end_token_id", 0))
        seg_surface_tokens: List[str] = []
        roles: List[str] = []
        for token_id in range(start_id, end_id + 1):
            tok = by_id.get(token_id)
            if not tok:
                continue
            seg_surface_tokens.append(str(tok.get("normalized", tok.get("surface", ""))))
            chosen = str(tok.get("role", {}).get("chosen", "none"))
            if chosen and chosen != "none":
                roles.append(chosen)

        if not seg_surface_tokens:
            continue

        if roles:
            struct_segments.append(_derive_segment_label_from_role(roles[0]))
            segment_tokens.append(seg_surface_tokens)
            continue

        # Deterministic bridge labeling from committed boundaries and token stream.
        # No legacy YAML segment-pattern fallback is used here.
        split = _split_and_label_committed_segment(seg_surface_tokens, struct_segments)
        struct_segments.extend(split["labels"])
        segment_tokens.extend(split["chunks"])

    return {
        "segments": struct_segments,
        "segment_tokens": segment_tokens,
        "legacy_fallback_used": False,
    }


def _adapter_roles_from_committed(tp: TP) -> Dict[str, Any]:
    committed_stream = tp.committed_stream
    tokens = committed_stream.get("tokens", []) if isinstance(committed_stream, dict) else []

    if not tokens:
        return {
            "used": False,
            "struct_roles": [],
            "role_segments": {},
            "legacy_fallback_used": False,
        }

    def _token_role(tok: Dict[str, Any]) -> str:
        role_obj = tok.get("role", {})
        chosen = str(role_obj.get("chosen", "none"))
        if chosen and chosen != "none":
            return chosen

        candidates = role_obj.get("candidates", [])
        if candidates:
            candidate_role = str(candidates[0].get("role_name", "none"))
            if candidate_role:
                return candidate_role
        return "none"

    # Map committed token roles onto SOB-produced segment token chunks.
    # Use only committed-stream role fields; no YAML role fallback.
    stream_tokens: List[tuple[str, str]] = []
    for tok in tokens:
        if str(tok.get("token_class", "")) == "PUNCT":
            continue
        token_text = str(tok.get("normalized", tok.get("surface", "")))
        stream_tokens.append((token_text, _token_role(tok)))

    struct_roles: List[str] = []
    role_segments: Dict[str, List[str]] = {}

    cursor = 0
    for seg_chunk in tp.segment_tokens:
        chunk_roles: List[str] = []
        for _ in seg_chunk:
            if cursor < len(stream_tokens):
                token_text, role = stream_tokens[cursor]
                cursor += 1
            else:
                token_text, role = "", "none"
            chunk_roles.append(role)
            if role != "none" and token_text:
                role_segments.setdefault(role, []).append(token_text)

        seg_role = next((r for r in chunk_roles if r != "none"), "none")
        struct_roles.append(seg_role)

    return {
        "used": True,
        "struct_roles": struct_roles,
        "role_segments": role_segments,
        "legacy_fallback_used": False,
    }


# ----- primitives ------------------------------------------------------------------


def InB(tp: TP) -> TP:
    committed_stream = build_committed_stream(tp.raw_text)
    tp.committed_stream = committed_stream

    committed_tokens = committed_stream.get("tokens", [])
    if committed_tokens:
        tp.tokens = [str(t.get("surface", "")) for t in committed_tokens]
        _record_bridge(tp, "InB", committed_adapter_used=True, legacy_fallback_used=False, detail="tokens sourced from committed_stream")
    else:
        tp.tokens = _simple_tokenize(tp.raw_text)
        _record_bridge(tp, "InB", committed_adapter_used=False, legacy_fallback_used=True, detail="committed_stream empty; legacy tokenizer used")
    return tp


def IIInB(tp: TP) -> TP:
    anomalies = []
    if isinstance(tp.committed_stream, dict):
        anomalies = tp.committed_stream.get("anomalies", [])
    tp.defects = [f"anomaly:{a.get('anomaly_type', 'unknown')}" for a in anomalies] if anomalies else []
    _record_bridge(
        tp,
        "IIInB",
        committed_adapter_used=isinstance(tp.committed_stream, dict) and bool(tp.committed_stream),
        legacy_fallback_used=not (isinstance(tp.committed_stream, dict) and bool(tp.committed_stream)),
        detail="defects mapped from committed_stream anomalies",
    )
    return tp


def IE(tp: TP) -> TP:
    committed_tokens = tp.committed_stream.get("tokens", []) if isinstance(tp.committed_stream, dict) else []
    if committed_tokens:
        tp.tokens = [str(t.get("normalized", t.get("surface", ""))) for t in committed_tokens]
        _record_bridge(tp, "IE", committed_adapter_used=True, legacy_fallback_used=False, detail="normalized tokens sourced from committed_stream")
    else:
        tp.tokens = _normalize_tokens(tp.tokens)
        _record_bridge(tp, "IE", committed_adapter_used=False, legacy_fallback_used=True, detail="committed_stream missing; legacy normalization used")
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
    if isinstance(tp.committed_stream, dict) and tp.committed_stream.get("segments"):
        extracted = _adapter_segments_from_committed(tp.committed_stream)
        _record_bridge(
            tp,
            "SOB",
            committed_adapter_used=True,
            legacy_fallback_used=bool(extracted.get("legacy_fallback_used")),
            detail="segments and segment_tokens mapped from committed_stream",
        )
    else:
        extracted = _extract_segments(tp.tokens)
        _record_bridge(tp, "SOB", committed_adapter_used=False, legacy_fallback_used=True, detail="committed segments unavailable; legacy segment extractor used")

    tp.struct_segments = extracted["segments"]
    tp.segment_tokens = extracted["segment_tokens"]
    return tp


def SROB(tp: TP) -> TP:
    committed_adapted = _adapter_roles_from_committed(tp)
    if not committed_adapted["used"]:
        tp.struct_roles = ["none" for _ in tp.struct_segments]
        tp.role_segments = {}
        _record_bridge(
            tp,
            "SROB",
            committed_adapter_used=False,
            legacy_fallback_used=False,
            detail="committed roles unavailable; emitted deterministic 'none' roles",
        )
        return tp

    tp.struct_roles = committed_adapted["struct_roles"]
    tp.role_segments = committed_adapted["role_segments"]
    _record_bridge(
        tp,
        "SROB",
        committed_adapter_used=True,
        legacy_fallback_used=False,
        detail="roles mapped from committed token.role fields only",
    )
    return tp


def CnOB(tp: TP) -> TP:
    matched, unmatched, residue = check_constraints(tp.struct_roles)

    def _add_match(name: str) -> None:
        if name not in matched:
            matched.append(name)
        if name in residue:
            residue.remove(name)

    def _ordered_transition(from_role: str, to_role: str) -> bool:
        from_indices = [i for i, r in enumerate(tp.struct_roles) if r == from_role]
        to_indices = [i for i, r in enumerate(tp.struct_roles) if r == to_role]
        return any(i < j for i in from_indices for j in to_indices)

    # Copular link is a structural state transition cue, not a role-pair literal.
    if "CP" in tp.struct_segments and "theme-state" in matched and "copular_state_link" not in matched:
        _add_match("copular_state_link")

    if "ST" in tp.struct_segments and "theme-state" not in matched:
        if "theme" in tp.struct_roles and "state" in tp.struct_roles:
            _add_match("theme-state")

    if "LOC" in tp.struct_segments and "state-location" in matched and "locative_link" not in matched:
        _add_match("locative_link")

    # Interrogative transitions: WH-led and yes/no auxiliary-led question forms.
    if "WQ" in tp.struct_segments and "IQ" in tp.struct_segments and "query-focus-predicate" not in matched:
        _add_match("query-focus-predicate")

    if tp.raw_text.strip().endswith("?") and tp.struct_segments[:1] == ["IQ"] and "query-focus-predicate" not in matched:
        _add_match("query-focus-predicate")

    if "predicate-theme" not in matched and "predicate" in tp.struct_roles and "theme" in tp.struct_roles:
        p_i = tp.struct_roles.index("predicate")
        t_i = tp.struct_roles.index("theme")
        if p_i < t_i:
            _add_match("predicate-theme")

    # Nested interrogative transitions.
    if _ordered_transition("theme", "relation"):
        _add_match("theme-relation")
    if _ordered_transition("relation", "state"):
        _add_match("relation-state")
    if _ordered_transition("state", "location"):
        _add_match("state-location")

    tp.constraints_matched = matched
    tp.constraints_unmatched = unmatched
    tp.constraint_residue = residue

    tp.constraints = matched
    if not hasattr(tp, "trace"):
        tp.trace = []
    tp.trace.append({
        "primitive": "CnOB",
        "notes": "[OB-Set]",
        "matched": matched,
        "unmatched": unmatched,
        "residue": residue,
        "token_relations": {
            "agent-action": (
                " ".join(tp.role_segments.get("agent", [])),
                " ".join(tp.role_segments.get("action", []))
            ),
            "action-relation": (
                " ".join(tp.role_segments.get("action", [])),
                " ".join(tp.role_segments.get("relation", []))
            ),
            "relation-patient": (
                " ".join(tp.role_segments.get("relation", [])),
                " ".join(tp.role_segments.get("patient", []))
            ),
            "state-location": (
                " ".join(tp.role_segments.get("state", [])),
                " ".join(tp.role_segments.get("location", []))
            ),
            "query-focus-predicate": (
                " ".join(tp.role_segments.get("query_focus", [])),
                " ".join(tp.role_segments.get("predicate", []))
            ),
            "predicate-theme": (
                " ".join(tp.role_segments.get("predicate", [])),
                " ".join(tp.role_segments.get("theme", []))
            )
        }
    })
    return tp


def SmOB(tp: TP) -> TP:
    ops, cues, residue = apply_smoothing(tp.segment_tokens, tp.struct_roles)

    if "CP" in tp.struct_segments and "theme-state" in tp.constraints_matched:
        if "copular_state_link" not in cues:
            cues.append("copular_state_link")
        if "smooth:copular_state_link" not in ops:
            ops.append("smooth:copular_state_link")
        if "no_relation_cues" in residue:
            residue = [r for r in residue if r != "no_relation_cues"]

    if "LOC" in tp.struct_segments and "state-location" in tp.constraints_matched:
        if "locative_link" not in cues:
            cues.append("locative_link")
        if "smooth:locative_link" not in ops:
            ops.append("smooth:locative_link")
        if "no_relation_cues" in residue:
            residue = [r for r in residue if r != "no_relation_cues"]

    if "query-focus-predicate" in tp.constraints_matched or tp.raw_text.strip().endswith("?"):
        if "interrogative_scope" not in cues:
            cues.append("interrogative_scope")
        if "smooth:interrogative_scope" not in ops:
            ops.append("smooth:interrogative_scope")
        if "no_relation_cues" in residue:
            residue = [r for r in residue if r != "no_relation_cues"]

    # Nested interrogative smoothing cues.
    is_nested = "RELC" in tp.struct_segments or (
        "relation" in tp.struct_roles and ("state" in tp.struct_roles or "location" in tp.struct_roles)
    )
    if is_nested:
        if "modifier_chain" not in cues:
            cues.append("modifier_chain")
        if "smooth:modifier_chain" not in ops:
            ops.append("smooth:modifier_chain")
    if is_nested and "location" in tp.struct_roles:
        if "nested_locative_link" not in cues:
            cues.append("nested_locative_link")
        if "smooth:nested_locative_link" not in ops:
            ops.append("smooth:nested_locative_link")
    if is_nested and "state" in tp.struct_roles:
        if "nested_state_link" not in cues:
            cues.append("nested_state_link")
        if "smooth:nested_state_link" not in ops:
            ops.append("smooth:nested_state_link")

    tp.smoothing_operations = ops
    tp.semantic_adjacent_cues = cues
    tp.smoothing_residue = residue

    tp.smoothed_geometry = True
    if not hasattr(tp, "trace"):
        tp.trace = []
    tp.trace.append({
        "primitive": "SmOB",
        "notes": "[OB-Set]",
        "operations": ops,
        "semantic_adjacent_cues": cues,
        "residue": residue,
        "token_relations": {
            "agent->action": (
                " ".join(tp.role_segments.get("agent", [])),
                " ".join(tp.role_segments.get("action", []))
            ),
            "action->relation": (
                " ".join(tp.role_segments.get("action", [])),
                " ".join(tp.role_segments.get("relation", []))
            ),
            "relation->patient": (
                " ".join(tp.role_segments.get("relation", [])),
                " ".join(tp.role_segments.get("patient", []))
            ),
            "state->location": (
                " ".join(tp.role_segments.get("state", [])),
                " ".join(tp.role_segments.get("location", []))
            ),
            "query_focus->predicate": (
                " ".join(tp.role_segments.get("query_focus", [])),
                " ".join(tp.role_segments.get("predicate", []))
            )
        }
    })
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
    # Copular/state sentences use descriptive_state; fallback keeps prior behavior.
    is_interrogative = "query-focus-predicate" in tp.constraints_matched or tp.raw_text.strip().endswith("?")
    is_nested = "RELC" in tp.struct_segments or (
        "relation" in tp.struct_roles and ("state" in tp.struct_roles or "location" in tp.struct_roles)
    )

    if is_interrogative and is_nested:
        tp.truth_relation = "interrogative_nested"
    elif is_interrogative:
        tp.truth_relation = "interrogative_open"
    elif "LOC" in tp.struct_segments and "state-location" in tp.constraints_matched:
        tp.truth_relation = "descriptive_locative"
    elif "CP" in tp.struct_segments and "theme-state" in tp.constraints_matched:
        tp.truth_relation = "descriptive_state"
    else:
        tp.truth_relation = "descriptive_factual" if not tp.defects else "uncertain"
    return tp


def OuBA(tp: TP) -> TP:
    tp.commit_flags["pathA_complete"] = True
    return tp
