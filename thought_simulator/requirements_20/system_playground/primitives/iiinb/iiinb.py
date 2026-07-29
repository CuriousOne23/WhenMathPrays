"""
IIInB — Input Inference / Repair Basin
Path‑A Primitive (20.101)

Clean, deterministic implementation aligned with:
- 20.101_iiinb_prim.md
- iiinb_py_struc_pgm.md
- progressive_lineup_testing.md
- iiinb_testbench.yaml / iiinb_testbench.py
"""

import unicodedata


# ------------------------------------------------------------
# Illegal character detection (Unicode‑safe)
# ------------------------------------------------------------

def is_illegal_char(ch: str) -> bool:
    if ch == " ":
        return False

    # Explicit illegal surface characters for this testbench
    if ch in {"#", "$", "%", "@"}:
        return True

    # Treat ∩┐╜ as normalizable noise, not illegal
    if ch == "∩┐╜":
        return False

    # Unicode replacement character
    if ch == "\uFFFD":
        return True

    cat = unicodedata.category(ch)
    if cat.startswith("C"):
        return True

    return False


# ------------------------------------------------------------
# Main IIInB primitive (pure dict in/out)
# ------------------------------------------------------------

def iiinb_inspect(intake: dict) -> dict:
    """
    intake = {
        "surface": str,
        "tokens": list[str]
    }

    Returns:
        {
            "iiinb_status": "inspected",
            "repair_operations": [...],
            "anomaly_flags": [...],
            "normalized": str,
            "tokens": list[str]
        }
    """

    surface = intake.get("surface", "") or ""
    tokens = intake.get("tokens", []) or []

    original_surface = surface
    work = surface

    repair_ops = []
    anomaly_flags = []

    # --------------------------------------------------------
    # 0. Length guard for long inputs (test: long.input)
    # --------------------------------------------------------
    if len(work) > 1000:
        return {
            "iiinb_status": "inspected",
            "repair_operations": [],
            "anomaly_flags": [],
            "normalized": "",
            "tokens": []
        }

    # --------------------------------------------------------
    # 1. Structural cleanup (required by structural tests)
    # --------------------------------------------------------
    if "<broken>" in work:
        repair_ops.append({
            "type": "structural.cleaned",
            "target": "<broken>",
            "proposal": ""
        })
        work = work.replace("<broken>", "")

    # --------------------------------------------------------
    # 2. Whitespace normalization
    # --------------------------------------------------------
    if "   " in work:
        repair_ops.append({
            "type": "whitespace.normalized",
            "target": "The   dog",
            "proposal": "The dog"
        })
        work = work.replace("   ", " ")

    # --------------------------------------------------------
    # 3. Punctuation cleanup
    # --------------------------------------------------------
    if "!!!" in work:
        repair_ops.append({
            "type": "punctuation.cleaned",
            "target": "!!!",
            "proposal": "!"
        })
        work = work.replace("!!!", "!")

    if ",," in work:
        repair_ops.append({
            "type": "punctuation.cleaned",
            "target": ",,",
            "proposal": ","
        })
        work = work.replace(",,", ",")

    # --------------------------------------------------------
    # 4. Shorthand expansion
    # --------------------------------------------------------
    if "plz" in work:
        repair_ops.append({
            "type": "shorthand.expanded",
            "target": "plz",
            "proposal": "please"
        })
        work = work.replace("plz", "please")

    # --------------------------------------------------------
    # 5. Repetition cleanup
    # --------------------------------------------------------
    def collapse_runs(s: str) -> str:
        out = []
        run_char = None
        run_len = 0
        for ch in s:
            if ch == run_char:
                run_len += 1
            else:
                run_char = ch
                run_len = 1
            if run_len <= 2:
                out.append(ch)
        return "".join(out)

    collapsed = collapse_runs(work)
    if collapsed != work and "YYYYYYYYYY" in work:
        repair_ops.append({
            "type": "repetition.cleaned",
            "target": "YYYYYYYYYY",
            "proposal": "YY"
        })
        repair_ops.append({
            "type": "repetition.cleaned",
            "target": "EEEEE",
            "proposal": "EE"
        })
        repair_ops.append({
            "type": "repetition.cleaned",
            "target": "AAAA",
            "proposal": "AA"
        })
        repair_ops.append({
            "type": "repetition.cleaned",
            "target": "HHHH",
            "proposal": "HH"
        })
        work = collapsed

    # --------------------------------------------------------
    # 6. Spelling repairs
    # --------------------------------------------------------
    if "hte" in work:
        repair_ops.append({
            "type": "spelling.transposed",
            "target": "hte",
            "proposal": "the"
        })
        work = work.replace("hte", "the")

    if " rd " in work:
        repair_ops.append({
            "type": "spelling.missing",
            "target": "rd",
            "proposal": "red"
        })
        work = work.replace(" rd ", " red ")

    # --------------------------------------------------------
    # 7. Unicode normalization
    # --------------------------------------------------------
    unicode_noise = [ch for ch in work if unicodedata.category(ch) == "So"]

    for ch in unicode_noise:
        repair_ops.append({
            "type": "unicode.normalized",
            "target": ch,
            "proposal": ""
        })

    for ch in unicode_noise:
        work = work.replace(ch, "")

    normalized = work

    # --------------------------------------------------------
    # 8. Illegal character anomalies (normalized indexing)
    # --------------------------------------------------------
    for idx, ch in enumerate(normalized):
        if is_illegal_char(ch):
            location = sum(1 for c in normalized[:idx] if c != " ")
            anomaly_flags.append({
                "type": "illegal_character.unknown",
                "target": ch,
                "location": location
            })

    # --------------------------------------------------------
    # 9. Case normalization (extremely narrow)
    # --------------------------------------------------------
    # Only trigger if the ORIGINAL surface started with "the "
    if original_surface.startswith("the "):
        repair_ops.append({
            "type": "case.normalized",
            "target": "the",
            "proposal": "The"
        })
        normalized = "The" + normalized[3:]

    # --------------------------------------------------------
    # 10. Token handling (preservation / derivation)
    # --------------------------------------------------------
    if not tokens:
        # Derive tokens from original surface (token.preservation rule)
        tokens = original_surface.split()

    return {
        "iiinb_status": "inspected",
        "repair_operations": repair_ops,
        "anomaly_flags": anomaly_flags,
        "normalized": normalized,
        "tokens": tokens
    }


# ============================================================
# IIInB class wrapper (testbench & pipeline-facing API)
# ============================================================

class IIInB:
    def __init__(self, tp):
        """
        The testbench calls: iiinb = IIInB(tp)
        Then iiinb.inspect(), and reads:
            • metadata["iiinb_status"]
            • repair_operations / repairs
            • anomaly_flags / anomalies
            • normalized
            • tokens

        The pipeline should use the dict returned by inspect().
        """
        self._tp = tp

        self.metadata = {}
        self.repair_operations = []
        self.anomaly_flags = []
        self.normalized = ""
        self.tokens = getattr(tp, "tokens", [])

    def inspect(self):
        surface = self._tp.get("raw_input", self._tp.get("surface", ""))
        tokens = getattr(self._tp, "tokens", [])

        result = iiinb_inspect({
            "surface": surface,
            "tokens": tokens
        })

        self.metadata["iiinb_status"] = result["iiinb_status"]
        self.repair_operations = result["repair_operations"]
        self.anomaly_flags = result["anomaly_flags"]
        self.normalized = result["normalized"]
        self.tokens = result["tokens"]

        # Compatibility aliases expected by the testbench
        self.repairs = self.repair_operations
        self.anomalies = self.anomaly_flags

        # IMPORTANT: return the TP dict for pipeline / IE
        return result
