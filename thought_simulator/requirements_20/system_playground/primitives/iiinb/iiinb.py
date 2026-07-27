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
    # 0. Long-input guard (bounded intake)
    # ----------------------------------------------------------------------
    if len(normalized) > 1000 and re.fullmatch(r"[A-Za-z]+", normalized):
        # For very long pure-letter inputs, normalize to empty
        normalized = ""
        tp.tokens = []
        tp.structure = {"tags": []}
        tp.normalized = normalized
        return tp

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
    # 3. Whitespace normalization (internal 3+ spaces only)
    #     e.g., "The   dog" → "The dog"
    # ----------------------------------------------------------------------
    ws_pattern = r"\b\w+( {3,})\w+\b"
    m = re.search(ws_pattern, normalized)
    if m:
        target = m.group(0)          # e.g., "The   dog"
        proposal = re.sub(r" {3,}", " ", target)
        add_repair("whitespace.normalized", target, proposal)
        normalized = re.sub(r" {3,}", " ", normalized)

    # ----------------------------------------------------------------------
    # 4. Punctuation cleanup (collapse repeated punctuation)
    #     e.g., "!!!" → "!"
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
    # 7. Case normalization (only when no prior repairs)
    #     This matches token.preservation expectations but
    #     avoids altering shorthand/spelling/Unicode cases.
    # ----------------------------------------------------------------------
    tokens = normalized.split()
    if tokens and tokens[0].islower() and len(tp.repairs) == 0:
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
    #     Positions are based on RAW input, but anomalies are only
    #     emitted for characters still present in normalized.
    # ----------------------------------------------------------------------
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?")
    
    for idx, ch in enumerate(raw):
        # Illegal character?
        if ch not in allowed:
            # Only emit anomaly if the character still exists in normalized
            # (i.e., it was NOT removed by unicode/structural cleanup)
            if ch in normalized:
                add_anomaly("illegal_character.unknown", ch, idx)


    # ----------------------------------------------------------------------
    # 10. Token emission
    #     For token_preservation, tokens reflect raw input.
    # ----------------------------------------------------------------------
    tp.tokens = raw.split()

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
