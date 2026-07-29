"""
InB Rulechecker — Path‑A Intake Envelope
Applies declarative rules from inb_rules.yaml to InB primitive outputs.

Location:
thought_simulator/requirements_20/system_playground/testbenches/path_a/intake/inb_rulechecker.py
"""

from __future__ import annotations

import os
import yaml
from typing import Any, Dict, List


# -------------------------------------------------------------------
# YAML loading
# -------------------------------------------------------------------

def _load_inb_rules() -> List[Dict[str, Any]]:
    """
    Load rules from inb_rules.yaml (Option C schema).
    """
    here = os.path.dirname(__file__)
    rules_path = os.path.join(here, "inb_rules.yaml")

    with open(rules_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    rules = data.get("rules", [])
    if not isinstance(rules, list):
        raise ValueError("inb_rules.yaml: 'rules' must be a list.")

    return rules


# -------------------------------------------------------------------
# Rule function implementations (InB-specific)
# Each rule function returns a list of defect strings (possibly empty).
# -------------------------------------------------------------------

def rule_whitespace_excess(raw_input: str, params: Dict[str, Any]) -> List[str]:
    defects: List[str] = []
    max_run = int(params.get("max_run", 1))

    run = 0
    for ch in raw_input:
        if ch == " ":
            run += 1
            if run > max_run:
                defects.append("whitespace.excess")
                break
        else:
            run = 0

    return defects


def rule_whitespace_leading(raw_input: str, params: Dict[str, Any]) -> List[str]:
    defects: List[str] = []
    if not params.get("enabled", True):
        return defects

    if raw_input.startswith(" "):
        defects.append("whitespace.leading")

    return defects


def rule_whitespace_trailing(raw_input: str, params: Dict[str, Any]) -> List[str]:
    defects: List[str] = []
    if not params.get("enabled", True):
        return defects

    if raw_input.endswith(" "):
        defects.append("whitespace.trailing")

    return defects


def rule_punctuation_excess(raw_input: str, params: Dict[str, Any]) -> List[str]:
    defects: List[str] = []
    max_cluster = int(params.get("max_cluster", 1))
    allowed_marks = set(params.get("allowed_marks", ["!", "?", ".", ","]))

    run = 0
    for ch in raw_input:
        if ch in allowed_marks:
            run += 1
            if run > max_cluster:
                defects.append("punctuation.excess")
                break
        else:
            run = 0

    return defects


def rule_punctuation_illegal(raw_input: str, params: Dict[str, Any]) -> List[str]:
    defects: List[str] = []
    allowed_marks = set(params.get("allowed_marks", ["!", "?", ".", ",", ";", ":"]))

    for ch in raw_input:
        if not ch.isalnum() and not ch.isspace() and ch not in allowed_marks:
            defects.append("punctuation.illegal")
            break

    return defects


def rule_unicode_invalid(raw_input: str, params: Dict[str, Any]) -> List[str]:
    defects: List[str] = []
    allow_replacement = bool(params.get("allow_replacement_char", False))

    for ch in raw_input:
        # U+FFFD replacement character
        if ch == "\uFFFD" and not allow_replacement:
            defects.append("unicode.invalid")
            break

    return defects


def rule_unicode_non_ascii(raw_input: str, params: Dict[str, Any]) -> List[str]:
    defects: List[str] = []
    ascii_only = bool(params.get("ascii_only", False))
    if not ascii_only:
        return defects

    for ch in raw_input:
        if ord(ch) > 127:
            defects.append("unicode.non_ascii")
            break

    return defects


def rule_structural_malformed(raw_input: str, params: Dict[str, Any]) -> List[str]:
    defects: List[str] = []
    allowed_tags = params.get("allowed_tags", [])
    max_tag_length = int(params.get("max_tag_length", 10))
    require_balanced = bool(params.get("require_balanced", True))

    # Very simple heuristic: look for '<' and '>' patterns
    # and treat anything not in allowed_tags or too long as malformed.
    tokens: List[str] = []
    buf = ""
    inside = False

    for ch in raw_input:
        if ch == "<":
            inside = True
            buf = "<"
        elif ch == ">" and inside:
            buf += ">"
            tokens.append(buf)
            inside = False
            buf = ""
        elif inside:
            buf += ch

    # Check tokens
    for t in tokens:
        if len(t) > max_tag_length:
            defects.append("structural.malformed")
            break
        if t not in allowed_tags:
            defects.append("structural.malformed")
            break

    # Optional: very simple balance check
    if require_balanced:
        opens = sum(1 for t in tokens if not t.startswith("</"))
        closes = sum(1 for t in tokens if t.startswith("</"))
        if opens != closes:
            defects.append("structural.malformed")

    return defects


def rule_structural_illegal(raw_input: str, params: Dict[str, Any]) -> List[str]:
    defects: List[str] = []
    allowed_tags = params.get("allowed_tags", [])

    tokens: List[str] = []
    buf = ""
    inside = False

    for ch in raw_input:
        if ch == "<":
            inside = True
            buf = "<"
        elif ch == ">" and inside:
            buf += ">"
            tokens.append(buf)
            inside = False
            buf = ""
        elif inside:
            buf += ch

    for t in tokens:
        if t not in allowed_tags:
            defects.append("structural.illegal")
            break

    return defects


def rule_output_defects_list_shape(output: Dict[str, Any], params: Dict[str, Any]) -> List[str]:
    defects: List[str] = []
    require_unique = bool(params.get("require_unique", True))
    require_sorted = bool(params.get("require_sorted", True))
    require_string_entries = bool(params.get("require_string_entries", True))

    out_defects = output.get("defects")

    if not isinstance(out_defects, list):
        defects.append("output.shape.invalid")
        return defects

    if require_string_entries and any(not isinstance(d, str) for d in out_defects):
        defects.append("output.shape.invalid")

    if require_unique and len(set(out_defects)) != len(out_defects):
        defects.append("output.shape.duplicate")

    if require_sorted and out_defects != sorted(out_defects):
        defects.append("output.shape.unsorted")

    return defects


def rule_deterministic_replay(raw_input: str, params: Dict[str, Any]) -> List[str]:
    # This rule is more about system‑level testing than per‑call checking.
    # Here we just provide a placeholder; real replay checks belong in a higher‑level harness.
    if not params.get("enabled", True):
        return []
    return []


def rule_deterministic_no_external_state(raw_input: str, params: Dict[str, Any]) -> List[str]:
    # Placeholder: actual enforcement requires architectural constraints.
    if not params.get("enabled", True):
        return []
    return []


# -------------------------------------------------------------------
# Rule registry
# -------------------------------------------------------------------

_RULES = _load_inb_rules()

_RULE_FUNCTIONS = {
    "whitespace.excess": rule_whitespace_excess,
    "whitespace.leading": rule_whitespace_leading,
    "whitespace.trailing": rule_whitespace_trailing,
    "punctuation.excess": rule_punctuation_excess,
    "punctuation.illegal": rule_punctuation_illegal,
    "unicode.invalid": rule_unicode_invalid,
    "unicode.non_ascii": rule_unicode_non_ascii,
    "structural.malformed": rule_structural_malformed,
    "structural.illegal": rule_structural_illegal,
    "output.defects_list_shape": rule_output_defects_list_shape,
    "deterministic.replay": rule_deterministic_replay,
    "deterministic.no_external_state": rule_deterministic_no_external_state,
}


# -------------------------------------------------------------------
# Public API
# -------------------------------------------------------------------

def validate_inb(primitive_output: Dict[str, Any]) -> List[str]:
    """
    Apply all InB rules to the given primitive output.

    primitive_output is expected to contain at least:
      - "raw_input": original text
      - "defects": list of defect strings (produced by InB)
    """
    raw_input = primitive_output.get("raw_input", "")
    collected: List[str] = []

    for rule in _RULES:
        rule_id = rule.get("id")
        params = rule.get("params", {})

        fn = _RULE_FUNCTIONS.get(rule_id)
        if fn is None:
            # Unknown rule id in YAML; skip or log.
            continue

        # Some rules operate on raw_input, some on the full output.
        if rule_id.startswith("output."):
            new_defects = fn(primitive_output, params)
        else:
            new_defects = fn(raw_input, params)

        collected.extend(new_defects)

    # Deduplicate and sort for deterministic behavior
    collected = sorted(set(collected))
    return collected
