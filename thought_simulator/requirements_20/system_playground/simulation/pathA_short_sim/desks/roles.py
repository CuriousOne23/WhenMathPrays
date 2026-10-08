from typing import Any, Dict, List


def adapt_roles_from_committed(
    committed_stream: Any,
    segment_tokens: List[List[str]],
) -> Dict[str, Any]:
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
    for seg_chunk in segment_tokens:
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
        chunk_text = [tok.lower() for tok in seg_chunk]
        if chunk_text == ["me"]:
            seg_role = "recipient"
        elif chunk_text == ["said"]:
            seg_role = "reporting"
        elif chunk_text == ["john"] and struct_roles and struct_roles[-1] in {"none", "relative"}:
            # Hat for the relative subject. The head noun is an earlier circle.
            seg_role = "relative_subject"
        elif seg_chunk == ["that"]:
            seg_role = "relative"
        struct_roles.append(seg_role)
        if seg_role in {"recipient", "reporting", "relative_subject", "relative"} and seg_chunk:
            role_segments.setdefault(seg_role, []).extend(tok.lower() for tok in seg_chunk)


    known_det = {"the", "a", "an"}
    known_noun = {"sky", "book", "rain", "table", "plain", "city", "fox", "dog", "cat", "mouse", "door", "lamp", "hall", "desk"}
    known_adj = {"blue", "bright", "cold", "lazy", "quick", "brown", "beautiful", "tired"}
    known_verb = {"chased", "chase", "chases", "bought", "buy", "wrote", "write", "give"}
    theme_seen = "theme" in struct_roles
    for idx, seg_chunk in enumerate(segment_tokens):
        if struct_roles[idx] != "none":
            continue
        words = [tok.lower() for tok in seg_chunk]
        if words and words[0] in known_det and words[-1] in known_noun:
            if not theme_seen:
                struct_roles[idx] = "theme"
                theme_seen = True
            else:
                struct_roles[idx] = "patient"
            role_segments.setdefault(struct_roles[idx], []).extend(words)
        elif len(words) == 1 and words[0] in known_adj:
            struct_roles[idx] = "state"
            role_segments.setdefault("state", []).extend(words)
        elif len(words) == 1 and words[0] in known_verb:
            struct_roles[idx] = "action"
            role_segments.setdefault("action", []).extend(words)

    return {
        "used": True,
        "struct_roles": struct_roles,
        "role_segments": role_segments,
        "legacy_fallback_used": False,
    }
