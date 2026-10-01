from typing import Any, Callable, Dict, List


def compute_smoothing_state(
    raw_text: str,
    struct_segments: List[str],
    struct_roles: List[str],
    segment_tokens: List[List[str]],
    constraints_matched: List[str],
    constraints_unmatched: List[str],
    apply_smoothing_fn: Callable[[List[List[str]], List[str]], Any],
) -> Dict[str, List[str]]:
    base_ops, base_cues, _ = apply_smoothing_fn(segment_tokens, struct_roles)

    allowed_ops = {
        "adjacency_smoothing",
        "continuity_smoothing",
        "role_smoothing",
        "segment_smoothing",
        "basin_compression_smoothing",
    }
    allowed_cues = {
        "interrogative_scope",
        "locative_adjacent",
        "quantified_np",
        "negated_state",
        "coordinated_clauses",
        "conditional_clauses",
        "fragment_ellipsis",
        "first_person_speaker",
        "passive_voice_clause",
        "imperative_voice_clause",
        "request_imperative_clause",
        "exclamative_force_clause",
        "action_clause",
    }

    semantic_adjacent_cues = [cue for cue in base_cues if cue in allowed_cues]
    if ("WQ" in struct_segments or raw_text.strip().endswith("?")) and "interrogative_scope" not in semantic_adjacent_cues:
        semantic_adjacent_cues.append("interrogative_scope")
    if "LOC" in struct_segments and "locative_adjacent" not in semantic_adjacent_cues:
        semantic_adjacent_cues.append("locative_adjacent")
    if "quantifier_scope_rule" in constraints_matched and "quantified_np" not in semantic_adjacent_cues:
        semantic_adjacent_cues.append("quantified_np")
    if "negation_scope_rule" in constraints_matched and "negated_state" not in semantic_adjacent_cues:
        semantic_adjacent_cues.append("negated_state")
    if "coordination_composition_rule" in constraints_matched and "coordinated_clauses" not in semantic_adjacent_cues:
        semantic_adjacent_cues.append("coordinated_clauses")
    if "conditional_composition_rule" in constraints_matched and "conditional_clauses" not in semantic_adjacent_cues:
        semantic_adjacent_cues.append("conditional_clauses")
    if "fragment_ellipsis_rule" in constraints_matched and "fragment_ellipsis" not in semantic_adjacent_cues:
        semantic_adjacent_cues.append("fragment_ellipsis")
    if "first_person_state_rule" in constraints_matched and "first_person_speaker" not in semantic_adjacent_cues:
        semantic_adjacent_cues.append("first_person_speaker")
    if "passive_voice_rule" in constraints_matched and "passive_voice_clause" not in semantic_adjacent_cues:
        semantic_adjacent_cues.append("passive_voice_clause")
    if "imperative_voice_rule" in constraints_matched and "imperative_voice_clause" not in semantic_adjacent_cues:
        semantic_adjacent_cues.append("imperative_voice_clause")
    if "request_imperative_rule" in constraints_matched and "request_imperative_clause" not in semantic_adjacent_cues:
        semantic_adjacent_cues.append("request_imperative_clause")
    if "exclamative_force_rule" in constraints_matched and "exclamative_force_clause" not in semantic_adjacent_cues:
        semantic_adjacent_cues.append("exclamative_force_clause")
    if "action_clause_rule" in constraints_matched and "action_clause" not in semantic_adjacent_cues:
        semantic_adjacent_cues.append("action_clause")

    smoothing_operations = [op for op in base_ops if op in allowed_ops]
    if "interrogative_scope" in semantic_adjacent_cues and "adjacency_smoothing" not in smoothing_operations:
        smoothing_operations.append("adjacency_smoothing")
    if "locative_adjacent" in semantic_adjacent_cues and "segment_smoothing" not in smoothing_operations:
        smoothing_operations.append("segment_smoothing")
    if constraints_unmatched and "continuity_rule" in constraints_unmatched and "continuity_smoothing" not in smoothing_operations:
        smoothing_operations.append("continuity_smoothing")
    if any(role == "none" for role in struct_roles) and "role_smoothing" not in smoothing_operations:
        smoothing_operations.append("role_smoothing")
    if not smoothing_operations:
        smoothing_operations.append("basin_compression_smoothing")

    basin_residue: List[str] = []

    return {
        "smoothing_operations": list(dict.fromkeys(smoothing_operations)),
        "semantic_adjacent_cues": list(dict.fromkeys(semantic_adjacent_cues)),
        "basin_residue": basin_residue,
    }
