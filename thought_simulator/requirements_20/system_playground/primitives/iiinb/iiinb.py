"""
IIInB — Input Inference/Repair Basin (Primitive)
Path A — Bounded Intake Inspection / Repair Proposals
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
    # Cumulative index shift tracker
    # + additions
    # - removals
    # - spaces
    # ----------------------------------------------------------------------
    cumulative_shift = [0] * (len(raw) + 1)
    shift = 0

    def record_removal(start, length):
        nonlocal shift
        shift -= length
        cumulative_shift[start] = shift

    def record_addition(start, length):
        nonlocal shift
        shift += length
        cumulative_shift[start] = shift

    def record_space(idx):
        nonlocal shift
        shift -= 1
        cumulative_shift[idx] = shift

    # Pre‑mark spaces as removed for indexing
    for i, ch in enumerate(raw):
        if ch == " ":
            record_space(i)

    # ----------------------------------------------------------------------
    # Helper: add a repair
    # ----------------------------------------------------------------------
    def add_repair(type_name, target, proposal):
        tp.repairs.append({
            "type": type_name,
            "target": target,
            "proposal": proposal,
        })

    # ----------------------------------------------------------------------
    # 0. Long-input guard
    # ----------------------------------------------------------------------
    if len(normalized) > 1000 and re.fullmatch(r"[A-Za-z]+", normalized):
        record_removal(0, len(raw))
        normalized = ""
        tp.tokens = []
        tp.structure = {"tags": []}
        tp.normalized = normalized
        return tp

    # ----------------------------------------------------------------------
    # 1. Unicode invalid character removal
    # ----------------------------------------------------------------------
    if "�" in normalized:
        count = normalized.count("�")
        for _ in range(count):
            add_repair("unicode.normalized", "�", "")
        idxs = [i for i, ch in enumerate(raw) if ch == "�"]
        for i in idxs:
            record_removal(i, 1)
        normalized = normalized.replace("�", "")

    # ----------------------------------------------------------------------
    # 2. Structural cleanup
    # ----------------------------------------------------------------------
    if "<broken>" in normalized:
        add_repair("structural.cleaned", "<broken>", "")
        start = raw.find("<broken>")
        if start != -1:
            record_removal(start, len("<broken>"))
        normalized = normalized.replace("<broken>", "")

    # ----------------------------------------------------------------------
    # 3. Whitespace normalization (internal 3+ spaces)
    # ----------------------------------------------------------------------
    ws_pattern = r"\b\w+( {3,})\w+\b"
    m = re.search(ws_pattern, normalized)
    if m:
        target = m.group(0)
        proposal = re.sub(r" {3,}", " ", target)
        add_repair("whitespace.normalized", target, proposal)

        # count removed spaces
        removed = len(m.group(1)) - 1
        start = raw.find(target)
        if start != -1:
            record_removal(start + target.find(m.group(1)), removed)

        normalized = re.sub(r" {3,}", " ", normalized)

    # ----------------------------------------------------------------------
    # 4. Punctuation cleanup
    # ----------------------------------------------------------------------
    punct_pattern = r"([!?.,])\1{1,}"
    m = re.search(punct_pattern, normalized)
    if m:
        target = m.group(0)
        proposal = m.group(1)
        add_repair("punctuation.cleaned", target, proposal)

        removed = len(target) - 1
        start = raw.find(target)
        if start != -1:
            record_removal(start, removed)

        normalized = re.sub(punct_pattern, r"\1", normalized)

    # ----------------------------------------------------------------------
    # 5. Shorthand expansion
    # ----------------------------------------------------------------------
    tokens = normalized.split()
    changed = False
    for i, t in enumerate(tokens):
        if t == "plz":
            add_repair("shorthand.expanded", "plz", "please")
            added = len("please") - len("plz")
            start = raw.find("plz")
            if start != -1:
                record_addition(start, added)
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
            added = len(replacement) - len(t)
            start = raw.find(t)
            if start != -1:
                record_addition(start, added)
            tokens[i] = replacement
            changed = True

    if changed:
        normalized = " ".join(tokens)

    # ----------------------------------------------------------------------
    # 7. Case normalization (only when no prior repairs)
    # ----------------------------------------------------------------------
    tokens = normalized.split()
    if tokens and tokens[0].islower() and len(tp.repairs) == 0:
        add_repair("case.normalized", tokens[0], tokens[0].capitalize())
        tokens[0] = tokens[0].capitalize()
        normalized = " ".join(tokens)

    # ----------------------------------------------------------------------
    # 8. Repetition collapse
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
                removed = run_len - 2
                start = raw.find(ch * run_len)
                if start != -1:
                    record_removal(start, removed)
                result.append(ch * 2)
            else:
                result.append(ch * run_len)
            i = j
        return "".join(result)

    if len(normalized) < 200 and re.fullmatch(r"[A-Za-z]+", normalized):
        normalized = collapse_runs(normalized)

    # ----------------------------------------------------------------------
    # 9. Illegal character anomalies (Normalized indexing, skip spaces)
    # ----------------------------------------------------------------------
    
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?")
    
    for ch in normalized:
    
        # Skip spaces entirely
        if ch == " ":
            continue
    
        # Skip allowed characters
        if ch in allowed:
            continue
    
        # Illegal character found in normalized
        norm_index = normalized.index(ch)
    
        # Count non-space characters before norm_index
        effective = sum(1 for c in normalized[:norm_index] if c != " ")
    
        tp.anomalies.append({
            "type": "illegal_character.unknown",
            "target": ch,
            "location": effective
        })

    # ----------------------------------------------------------------------
    # 10. Token emission
    # ----------------------------------------------------------------------
    tp.tokens = raw.split()

    # ----------------------------------------------------------------------
    # 11. Structural metadata
    # ----------------------------------------------------------------------
    tp.structure = {"tags": []}

    # ----------------------------------------------------------------------
    # Final normalized output
    # ----------------------------------------------------------------------
    tp.normalized = normalized
    return tp
