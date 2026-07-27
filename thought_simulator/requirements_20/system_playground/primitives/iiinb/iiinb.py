"""
IIInB — Input Inference/Repair Basin (Primitive)
Path A — Bounded Intake Inspection / Repair Proposals

This primitive operates on TP.intake.surface (tp.raw_input) and produces:
  - deterministic repair_operations
  - deterministic anomaly_flags
  - deterministic normalized surface
  - optional tokens / structure metadata

It is designed for the Path A pipeline:
InB → IIInB → IE
"""

import re

def IIInB(tp):
    raw = tp.raw_input

    # ----------------------------------------------------------------------
    # Initialize IIInB fields
    # ----------------------------------------------------------------------
    tp.metadata["iiinb_status"] = "inspected"
    tp.repairs = []
    tp.anomalies = []
    tp.tokens = []
    tp.structure = {}
    normalized = raw

    # ----------------------------------------------------------------------
    # Helper: add a repair in IE-compatible format
    # ----------------------------------------------------------------------
    def add_repair(type_name, target, proposal):
        tp.repairs.append({
            "type": type_name,
            "target": target,
            "proposal": proposal,
        })

    # ----------------------------------------------------------------------
    # Helper: add an anomaly in IE-compatible format
    # ----------------------------------------------------------------------
    def add_anomaly(type_name, target, location):
        tp.anomalies.append({
            "type": type_name,
            "target": target,
            "location": location,
        })

    # ----------------------------------------------------------------------
    # 1. Unicode invalid character removal (�)
    # ----------------------------------------------------------------------
    if "�" in normalized:
        count = normalized.count("�")
        for _ in range(count):
            add_repair("unicode.normalized", "�", "")
        normalized = normalized.replace("�", "")

    # ----------------------------------------------------------------------
    # 2. Structural cleanup BEFORE anomaly scan
    # ----------------------------------------------------------------------
    if "<broken>" in normalized:
        add_repair("structural.cleaned", "<broken>", "")
        normalized = normalized.replace("<broken>", "")

    # ----------------------------------------------------------------------
    # 3. Whitespace normalization
    # ----------------------------------------------------------------------
    ws_pattern = r"\s{2,}"
    m = re.search(ws_pattern, normalized)
    if m:
        add_repair("whitespace.normalized", m.group(0), " ")
        normalized = re.sub(ws_pattern, " ", normalized)

    # ----------------------------------------------------------------------
    # 4. Punctuation cleanup (collapse repeated punctuation)
    # ----------------------------------------------------------------------
    punct_pattern = r"([!?.,])\1{1,}"
    m = re.search(punct_pattern, normalized)
    if m:
        add_repair("punctuation.cleaned", m.group(0), m.group(1))
        normalized = re.sub(punct_pattern, r"\1", normalized)

    # ----------------------------------------------------------------------
    # 5. Shorthand expansion ("plz" → "please")
    # ----------------------------------------------------------------------
    tokens = normalized.split()
    changed = False
    for i, t in enumerate(tokens):
        if t == "plz":
            add_repair("shorthand.expanded", "plz", "please")
            tokens[i] = "please"
            changed = True
    if changed:
        normalized = " ".join(tokens)

    # ----------------------------------------------------------------------
    # 6. Spelling corrections
    # ----------------------------------------------------------------------
    spelling_map = {
        "hte": ("the", "spelling.transposed"),
        "rd": ("red", "spelling.missing"),
    }

    tokens = normalized.split()
    changed = False
    for i, t in enumerate(tokens):
        if t in spelling_map:
            replacement, type_name = spelling_map[t]
            add_repair(type_name, t, replacement)
            tokens[i] = replacement
            changed = True

    if changed:
        normalized = " ".join(tokens)

    # ----------------------------------------------------------------------
    # 7. Case normalization (capitalize first token)
    # ----------------------------------------------------------------------
    tokens = normalized.split()
    if tokens and tokens[0].islower():
        add_repair("case.normalized", tokens[0], tokens[0].capitalize())
        tokens[0] = tokens[0].capitalize()
        normalized = " ".join(tokens)

    # ----------------------------------------------------------------------
    # 8. Repetition collapse (bounded expressive noise)
    # ----------------------------------------------------------------------
    def collapse_runs(s):
        result = []
        i = 0
        while i < len(s):
            ch = s[i]
            j = i + 1
            while j < len(s) and s[j] == ch:
                j += 1
            run_len = j - i
            if run_len > 2:
                add_repair("repetition.cleaned", ch * run_len, ch * 2)
                result.append(ch * 2)
            else:
                result.append(ch * run_len)
            i = j
        return "".join(result)

    if len(normalized) < 200 and re.fullmatch(r"[A-Za-z]+", normalized):
        normalized = collapse_runs(normalized)

    # ----------------------------------------------------------------------
    # 9. Illegal character anomalies AFTER all repairs
    # ----------------------------------------------------------------------
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?")
    for idx, ch in enumerate(normalized):
        if ch not in allowed:
            add_anomaly("illegal_character.unknown", ch, idx)

    # ----------------------------------------------------------------------
    # 10. Token emission
    # ----------------------------------------------------------------------
    tp.tokens = normalized.split()

    # ----------------------------------------------------------------------
    # 11. Structural metadata
    # ----------------------------------------------------------------------
    tp.structure = {
        "tags": []
    }

    # ----------------------------------------------------------------------
    # Final normalized output
    # ----------------------------------------------------------------------
    tp.normalized = normalized
    return tp
