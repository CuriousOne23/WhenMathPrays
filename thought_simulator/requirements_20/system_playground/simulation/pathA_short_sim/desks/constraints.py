from typing import Any, Callable, Dict, List


def compute_constraint_fit(
    raw_text: str,
    tokens: List[str],
    struct_segments: List[str],
    struct_roles: List[str],
    segment_tokens: List[List[str]],
    check_constraints_fn: Callable[[List[str]], Any],
) -> Dict[str, List[str]]:
    _ = check_constraints_fn(struct_roles)

    quantifier_heads = {"every", "all", "each"}
    first_token = tokens[0].strip().lower() if tokens else ""
    has_quantified_np = first_token in quantifier_heads
    has_negation_marker = any(tok in {"not", "n't", "never"} for tok in tokens)
    has_coordination = "and" in tokens and struct_segments.count("CP") >= 2 and struct_segments.count("LOC") >= 2
    has_conditional_composition = first_token == "if" and struct_segments.count("CP") >= 2 and struct_segments.count("LOC") >= 2
    has_locative_fragment = len(struct_segments) == 1 and struct_segments[0] == "LOC"
    has_first_person_state = first_token == "i" and "am" in tokens
    passive_auxiliaries = {"was", "were", "is", "are", "been", "be"}
    passive_participles = {"written", "known", "seen", "given", "taken", "done", "made", "closed"}
    has_passive_voice = any(tok in passive_auxiliaries for tok in tokens) and any(tok.endswith("ed") or tok in passive_participles for tok in tokens)
    imperative_heads = {"close", "open", "stop", "go", "put", "take"}
    has_imperative_voice = first_token in imperative_heads and not raw_text.strip().endswith("?")
    has_request_imperative = first_token == "please" and len(tokens) > 1 and tokens[1] in imperative_heads
    has_exclamative_force = raw_text.strip().endswith("!") and first_token in {"what", "how"}
    wh_words = {"who", "what", "where", "when", "why", "how"}
    aux_heads = {"is", "are", "was", "were", "do", "does", "did"}
    has_polar_question = raw_text.strip().endswith("?") and first_token in aux_heads and not any(tok in wh_words for tok in tokens)

    canonical_rules = [
        "adjacency_rule",
        "compatibility_rule",
        "structural_rule",
        "continuity_rule",
    ]
    if has_quantified_np:
        canonical_rules.append("quantifier_scope_rule")
    if has_negation_marker:
        canonical_rules.append("negation_scope_rule")
    if has_coordination:
        canonical_rules.append("coordination_composition_rule")
    if has_conditional_composition:
        canonical_rules.append("conditional_composition_rule")
    if has_locative_fragment:
        canonical_rules.append("fragment_ellipsis_rule")
    if has_first_person_state:
        canonical_rules.append("first_person_state_rule")
    if has_passive_voice:
        canonical_rules.append("passive_voice_rule")
    if has_imperative_voice:
        canonical_rules.append("imperative_voice_rule")
    if has_request_imperative:
        canonical_rules.append("request_imperative_rule")
    if has_exclamative_force:
        canonical_rules.append("exclamative_force_rule")
    if has_polar_question:
        canonical_rules.append("polar_question_rule")
    action_verbs = {"chased", "chase", "chases", "bought", "buy", "wrote", "write", "jumps", "jump", "jumped"}
    has_action_clause = "VP" in struct_segments and any(tok in action_verbs for tok in tokens) and not has_imperative_voice and not has_request_imperative
    if has_action_clause:
        canonical_rules.append("action_clause_rule")

    constraints_matched: List[str] = []
    if struct_segments and segment_tokens:
        constraints_matched.append("structural_rule")
    if struct_roles and any(role != "none" for role in struct_roles):
        constraints_matched.append("compatibility_rule")
    if "WQ" in struct_segments or "LOC" in struct_segments:
        constraints_matched.append("adjacency_rule")
    if struct_roles and all(role != "none" for role in struct_roles):
        constraints_matched.append("continuity_rule")
    if has_quantified_np and "NP" in struct_segments:
        constraints_matched.append("quantifier_scope_rule")
    if has_negation_marker and "CP" in struct_segments:
        constraints_matched.append("negation_scope_rule")
    if has_coordination:
        constraints_matched.append("coordination_composition_rule")
    if has_conditional_composition:
        constraints_matched.append("conditional_composition_rule")
    if has_locative_fragment:
        constraints_matched.append("fragment_ellipsis_rule")
    if has_first_person_state and "NP" in struct_segments:
        constraints_matched.append("first_person_state_rule")
    if has_passive_voice and "CP" in struct_segments:
        constraints_matched.append("passive_voice_rule")
    if has_imperative_voice and "NP" in struct_segments:
        constraints_matched.append("imperative_voice_rule")
    if has_request_imperative and "NP" in struct_segments:
        constraints_matched.append("request_imperative_rule")
    if has_exclamative_force:
        constraints_matched.append("exclamative_force_rule")
    if has_polar_question:
        constraints_matched.append("polar_question_rule")
    if has_action_clause:
        constraints_matched.append("action_clause_rule")

    constraints_matched = list(dict.fromkeys(constraints_matched))
    constraints_unmatched = [rule for rule in canonical_rules if rule not in constraints_matched]

    constraint_residue: List[str] = []
    if ("WQ" in struct_segments or raw_text.strip().endswith("?")) and "continuity_rule" in constraints_unmatched:
        constraint_residue.append("interrogative_scope")
    if "LOC" in struct_segments and "adjacency_rule" in constraints_matched:
        constraint_residue.append("locative_adjacent")

    return {
        "constraints_matched": constraints_matched,
        "constraints_unmatched": constraints_unmatched,
        "constraint_residue": constraint_residue,
    }
