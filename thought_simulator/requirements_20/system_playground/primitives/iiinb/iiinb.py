"""
IIInB — Input Inference/Repair Basin (Primitive)
Path A — Bounded Intake Inspection / Repair Proposals

This primitive operates on TP.intake.surface (here: tp.raw_input) and
produces deterministic, pre‑semantic repair proposals and a suggested
normalized surface form, without applying semantic inference.

It is designed to be called from the Path A intake testbenches:
InB → IIInB → IE
"""

import re


def IIInB(tp):
    """
    IIInB primitive.

    Expected TP fields (as used by the testbenches):
      - tp.raw_input: str
      - tp.metadata: dict
      - tp.repairs: list
      - tp.normalized: str

    This implementation:
      - sets iiinb_status = "inspected"
      - analyzes tp.raw_input
      - proposes deterministic repairs in tp.repairs
      - sets tp.normalized to a suggested normalized surface
    """

    raw = tp.raw_input
    tp.metadata.setdefault("iiinb_status", "inspected")
    tp.repairs = []
    normalized = raw

    # ------------------------------------------------------------
    # 1. Unicode noise normalization (e.g., '�')
    # ------------------------------------------------------------
    if "�" in normalized:
        new = normalized.replace("�", "")
        tp.repairs.append({
            "op": "normalize_unicode",
            "target": "�",
            "replacement": "",
            "rule_id": "iiinb.unicode.invalid",
        })
        normalized = new

    # ------------------------------------------------------------
    # 2. Structural token removal (e.g., "<broken>")
    # ------------------------------------------------------------
    if "<broken>" in normalized:
        new = normalized.replace("<broken>", "")
        tp.repairs.append({
            "op": "remove_structural_token",
            "target": "<broken>",
            "replacement": "",
            "rule_id": "iiinb.structural.malformed",
        })
        normalized = new

    # ------------------------------------------------------------
    # 3. Shorthand expansion (e.g., "plz" → "please")
    # ------------------------------------------------------------
    tokens = normalized.split()
    changed = False
    for i, t in enumerate(tokens):
        if t == "plz":
            tokens[i] = "please"
            tp.repairs.append({
                "op": "expand_shorthand",
                "target": "plz",
                "replacement": "please",
                "rule_id": "iiinb.shorthand.plz",
            })
            changed = True
    if changed:
        normalized = " ".join(tokens)

    # ------------------------------------------------------------
    # 4. Spelling corrections — transposition and missing letter
    # ------------------------------------------------------------
    spelling_map = {
        "hte": ("the", "iiinb.spelling.transposed", "correct_transposition"),
        "rd": ("red", "iiinb.spelling.missing", "correct_missing_letter"),
    }
    
    tokens = normalized.split()
    changed = False
    for i, t in enumerate(tokens):
        if t in spelling_map:
            replacement, rule_id, op_name = spelling_map[t]
            tokens[i] = replacement
            tp.repairs.append({
                "op": op_name,
                "target": t,
                "replacement": replacement,
                "rule_id": rule_id,
            })
            changed = True
    
    if changed:
        normalized = " ".join(tokens)

    # ------------------------------------------------------------
    # 5. Repeating‑letter noise collapse
    #    Example: "YYYYYYYYYYEEEEEAAAAHHHH" → "YYEEAAHH"
    # ------------------------------------------------------------
    def collapse_runs(s: str) -> str:
        result = []
        i = 0
        while i < len(s):
            ch = s[i]
            j = i + 1
            while j < len(s) and s[j] == ch:
                j += 1
            run_len = j - i
            if run_len > 2:
                # collapse to exactly two characters
                result.append(ch * 2)
                tp.repairs.append({
                    "op": "collapse_repeated_chars",
                    "target": ch * run_len,
                    "replacement": ch * 2,
                    "rule_id": "iiinb.repeating.letters",
                })
            else:
                result.append(ch * run_len)
            i = j
        return "".join(result)

    # Only collapse repeated letters if the string is SHORT
    # (expressive noise, not long input)
    if len(normalized) < 200 and re.fullmatch(r"[A-Za-z]+", normalized):
        collapsed = collapse_runs(normalized)
        normalized = collapsed


    # ------------------------------------------------------------
    # 6. Long input / empty input
    #    For now, IIInB does not propose repairs; it simply passes
    #    the surface through. Length/emptiness are handled by InB.
    # ------------------------------------------------------------
    # (No additional logic here — normalized already set.)

    tp.normalized = normalized
    return tp
