from typing import Any, Dict, List


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


def extract_segments(
    tokens: List[str],
    token_classes_map: Dict[str, str],
    segment_patterns: Dict[str, List[str]],
) -> Dict[str, Any]:
    classes = [token_classes_map.get(tok, "UNK") for tok in tokens]
    struct_segments: List[str] = []
    segment_tokens: List[List[str]] = []

    i = 0
    while i < len(tokens):
        if classes[i] == "UNK":
            i += 1
            continue

        np_pattern = segment_patterns.get("NP", [])
        np_len = _match_np_with_pattern(classes, i, np_pattern)
        if np_len > 0:
            struct_segments.append("NP")
            segment_tokens.append(tokens[i:i + np_len])
            i += np_len
            continue

        matched = False
        for seg_name, pattern in segment_patterns.items():
            if seg_name == "NP" or not pattern:
                continue
            plen = len(pattern)
            if classes[i:i + plen] == pattern:
                struct_segments.append(seg_name)
                segment_tokens.append(tokens[i:i + plen])
                i += plen
                matched = True
                break
        if matched:
            continue

        i += 1

    return {
        "struct_segments": struct_segments,
        "segment_tokens": segment_tokens,
    }
