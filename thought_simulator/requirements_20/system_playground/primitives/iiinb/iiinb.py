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
    tp.repairs = []            # IE expects "repair_operations"
    tp.anomalies = []          # IE expects "anomaly_flags"
    tp.tokens = []             # optional
    tp.structure = {}          # optional
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
    for idx, ch in enumerate(normalized):
        if ch == "�":
            add_repair("unicode.normalized", "�", "")
            normalized = normalized.replace("�", "")

    # ----------------------------------------------------------------------
    # 2. Illegal character anomalies (non-alnum punctuation except allowed)
    # ----------------------------------------------------------------------
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?")
    for idx, ch in enumerate(normalized):
        if ch not in allowed:
            add_anomaly("illegal_character.unknown", ch, idx)

    # ----------------------------------------------------------------------
    # 3. Structural token cleanup
    # ----------------------------------------------------------------------
    if "<broken>" in normalized:
        add_repair("structural.cleaned", "<broken>", "")
        normalized = normalized.replace("<broken>", "")

    # ----------------------------------------------------------------------
    # 4. Shorthand expansion ("plz" → "please")
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
    # 5. Spelling corrections
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
    # 6. Repetition collapse (bounded expressive noise)
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
    # 7. Token emission (optional but IE-compatible)
    # ----------------------------------------------------------------------
    tp.tokens = normalized.split()

    # ----------------------------------------------------------------------
    # 8. Structural metadata (optional)
    # ----------------------------------------------------------------------
    tp.structure = {
        "tags": []
    }

    # ----------------------------------------------------------------------
    # Final normalized output
    # ----------------------------------------------------------------------
    tp.normalized = normalized
    return tp
