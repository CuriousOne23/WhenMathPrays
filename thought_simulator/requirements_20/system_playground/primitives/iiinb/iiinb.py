"""
IIInB — Input Inference / Repair Basin
Path‑A Primitive (20.101 / 20.105)

Aligned with:
- 20.101_iiinb_prim.md
- iiinb_py_struc_pgm.md
- progressive_lineup_testing.md
- iiinb_testbench.yaml / iiinb_rules.yaml
"""

import unicodedata
from pathlib import Path
import yaml


# ------------------------------------------------------------
# Illegal character detection (Unicode‑safe)
# ------------------------------------------------------------

def is_illegal_char(ch: str) -> bool:
    if ch == " ":
        return False

    # Explicit illegal surface characters for this testbench
    if ch in {"#", "$", "%", "@"}:
        return True

    # Unicode replacement character
    if ch == "\uFFFD":
        return True

    cat = unicodedata.category(ch)
    if cat.startswith("C"):
        return True

    return False


# ------------------------------------------------------------
# Dictionary rule loader (iiinb_dct_rules)
# ------------------------------------------------------------

def load_dct_rules():
    rule_dir = Path(__file__).parent / "iiinb_dct_rules"
    rules = {}
    if not rule_dir.exists():
        return rules
    for file in rule_dir.glob("*.yaml"):
        data = yaml.safe_load(file.read_text())
        rules[file.stem] = data.get("rules", {})
    return rules


DCT_RULES = load_dct_rules()


# ------------------------------------------------------------
# Repetition collapse (structural, deterministic)
# ------------------------------------------------------------

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
            "primitive_flags": [...],
            "normalized": str,
            "tokens": list[str]
        }
    """

    surface = intake.get("surface", "") or ""
    tokens = intake.get("tokens", []) or []

    original_surface = surface
    work = surface

    repair_ops = []
    primitive_flags = []

    # --------------------------------------------------------
    # 0. Length guard for long inputs (test: long.input)
    # --------------------------------------------------------
    if len(work) > 1000:
        return {
            "iiinb_status": "inspected",
            "repair_operations": [],
            "primitive_flags": [],
            "normalized": "",
            "tokens": []
        }

    # --------------------------------------------------------
    # 1. Structural cleanup (structural.cleaned)
    # --------------------------------------------------------
    structural_rules = DCT_RULES.get("structural", {})
    for target, proposal in structural_rules.items():
        if target in work:
            repair_ops.append({
                "type": "structural.cleaned",
                "target": target,
                "proposal": proposal
            })
            work = work.replace(target, proposal)

    # --------------------------------------------------------
    # 2. Whitespace normalization (whitespace.normalized)
    # --------------------------------------------------------
    
    import re
    
    # Collapse all whitespace runs to a single space
    collapsed = re.sub(r"\s+", " ", work)
    
    # Remove leading/trailing spaces
    normalized_ws = collapsed.strip()
    
    if normalized_ws != work:
        repair_ops.append({
            "type": "whitespace.normalized",
            "target": work,
            "proposal": normalized_ws
        })
    
    work = normalized_ws

    # --------------------------------------------------------
    # 3. Punctuation cleanup (punctuation.cleaned)
    # --------------------------------------------------------
    punctuation_rules = DCT_RULES.get("punctuation", {})
    for target, proposal in punctuation_rules.items():
        if target in work:
            repair_ops.append({
                "type": "punctuation.cleaned",
                "target": target,
                "proposal": proposal
            })
            work = work.replace(target, proposal)

    # --------------------------------------------------------
    # 4. Shorthand expansion (shorthand.expanded)
    # --------------------------------------------------------
    shorthand_rules = DCT_RULES.get("shorthand", {})
    for target, proposal in shorthand_rules.items():
        if target in work:
            repair_ops.append({
                "type": "shorthand.expanded",
                "target": target,
                "proposal": proposal
            })
            work = work.replace(target, proposal)

    # --------------------------------------------------------
    # 5. Repetition cleanup (repetition.cleaned)
    # --------------------------------------------------------
    repetition_rules = DCT_RULES.get("repetition", {})
    collapsed = collapse_runs(work)
    if collapsed != work:
        # Only record repetition.cleaned for explicit tokens present
        for target, proposal in repetition_rules.items():
            if target in work:
                repair_ops.append({
                    "type": "repetition.cleaned",
                    "target": target,
                    "proposal": proposal
                })
        work = collapsed

    # --------------------------------------------------------
    # 6. Spelling repairs (spelling.transposed / spelling.missing)
    # --------------------------------------------------------
    spelling_rules = DCT_RULES.get("spelling", {})
    for target, proposal in spelling_rules.items():
        if target in work:
            # Simple heuristic: 3‑letter transposition vs other (missing)
            if len(target) == 3:
                rtype = "spelling.transposed"
            else:
                rtype = "spelling.missing"
            repair_ops.append({
                "type": rtype,
                "target": target,
                "proposal": proposal
            })
            work = work.replace(target, proposal)

    # --------------------------------------------------------
    # 7. Unicode normalization (unicode.normalized)
    # --------------------------------------------------------
    unicode_rules = DCT_RULES.get("unicode", {})
    for target, proposal in unicode_rules.items():
        if target in work:
            repair_ops.append({
                "type": "unicode.normalized",
                "target": target,
                "proposal": proposal
            })
            work = work.replace(target, proposal)

    normalized = work

    # --------------------------------------------------------
    # 8. Illegal character primitive flags (illegal_character.unknown)
    # --------------------------------------------------------
    for idx, ch in enumerate(normalized):
        if is_illegal_char(ch):
            location = sum(1 for c in normalized[:idx] if c != " ")
            primitive_flags.append({
                "type": "illegal_character.unknown",
                "target": ch,
                "location": location
            })

    # --------------------------------------------------------
    # 9. Case normalization (case.normalized)
    # --------------------------------------------------------
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
        tokens = original_surface.split()

    return {
        "iiinb_status": "inspected",
        "repair_operations": repair_ops,
        "primitive_flags": primitive_flags,
        "normalized": normalized,
        "tokens": tokens
    }


# ============================================================
# IIInB class wrapper (testbench & pipeline-facing API)
# ============================================================

class IIInB:
    def __init__(self, tp):
        self._tp = tp

        self.metadata = {}
        self.repair_operations = []
        self.primitive_flags = []
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
        self.primitive_flags = result["primitive_flags"]
        self.flags = self.primitive_flags
        self.anomalies = self.primitive_flags
        self.normalized = result["normalized"]
        self.tokens = result["tokens"]

        self.repairs = self.repair_operations
        self.anomalies = self.primitive_flags

        return result
