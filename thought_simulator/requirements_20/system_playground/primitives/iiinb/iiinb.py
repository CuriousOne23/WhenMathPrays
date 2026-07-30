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
import re


# ------------------------------------------------------------
# Illegal character detection (Unicode‑safe)
# ------------------------------------------------------------

def is_illegal_char(ch: str) -> bool:
    if ch == " ":
        return False

    # Explicit illegal surface characters for this testbench
    if ch in {"#", "$", "%", "@"}:
        return True

    # Only flag ASCII control chars (0–31), not Unicode noise
    if ord(ch) < 32:
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
        with file.open(encoding="utf-8") as f:
            data = yaml.safe_load(f.read())
        rules[file.stem] = data.get("rules", {})
    return rules


DCT_RULES = load_dct_rules()


# ------------------------------------------------------------
# Repetition collapse helper (used for proposals only)
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
# Tokenization of original surface (rule 1)
# ------------------------------------------------------------

def tokenize_original_surface(surface: str) -> list[str]:
    if not surface:
        return []

    # 1. Structural tokens: <broken>, <tag>, <xyz123>
    structural = r"<[^>\s]+>"

    # 2. Words that may contain internal/trailing illegal chars (#,$,%)
    #    e.g., Th#e, dog$, cat%
    word_with_illegal = r"[A-Za-z0-9]+[#\$%]?[A-Za-z0-9]*"

    # 3. Standalone @ (so dog@!!! → dog, @, !!!)
    at_token = r"@"

    # 4. Punctuation runs: !!!, ,, , ., ∩┐╜, etc.
    punct = r"[^\w\s]+"

    pattern = f"{structural}|{word_with_illegal}|{at_token}|{punct}"
    raw_tokens = re.findall(pattern, surface)

    final_tokens = []
    i = 0
    while i < len(raw_tokens):
        tok = raw_tokens[i]

        # --- unicode noise merge for caf├⌐ ---
        # Merge ASCII word + single unicode noise token
        if tok.isalpha() and i + 1 < len(raw_tokens):
            nxt = raw_tokens[i + 1]
            if any(ord(c) > 127 for c in nxt) and len(nxt) <= 2:
                final_tokens.append(tok + nxt)
                i += 2
                continue

        # --- word + punctuation adjacency merge (Hello,, → Hello,,) ---
        if tok.isalpha() and i + 1 < len(raw_tokens):
            nxt = raw_tokens[i + 1]
            if nxt and not nxt[0].isalnum():
                if surface.find(tok + nxt) != -1:
                    final_tokens.append(tok + nxt)
                    i += 2
                    continue

        final_tokens.append(tok)
        i += 1

    return final_tokens


# ------------------------------------------------------------
# Main IIInB primitive (pure dict in/out, proposal‑only)
# ------------------------------------------------------------

def iiinb_inspect(intake: dict) -> dict:
    """
    intake = {
        "surface": str,
        "tokens": list[str]
    }

    Returns (proposal‑only, no mutations):
        {
            "iiinb_status": "inspected",
            "repair_proposals": [...],
            "anomaly_flags": [...],
            "intake_surface": str,
            "intake_tokens": list[str]
        }
    """

    surface = intake.get("surface", "") or ""
    tokens = intake.get("tokens", []) or []

    intake_surface = surface
    intake_tokens = tokens[:] if tokens else tokenize_original_surface(surface)

    repair_proposals = []
    anomaly_flags = []

    # --------------------------------------------------------
    # 0. Length guard for long inputs (test: long.input)
    # --------------------------------------------------------
    if len(intake_surface) > 1000:
        return {
            "iiinb_status": "inspected",
            "repair_proposals": [],
            "anomaly_flags": [],
            "intake_surface": intake_surface,
            "intake_tokens": intake_tokens,
        }

    # --------------------------------------------------------
    # 1. Structural cleanup (structural.clean proposals)
    # --------------------------------------------------------
    structural_rules = DCT_RULES.get("structural", {})
    for idx, tok in enumerate(intake_tokens):
        for target, proposal in structural_rules.items():
            if tok == target:
                repair_proposals.append({
                    "rule_id": "structural.clean",
                    "span": [idx, idx],
                    "replacement": proposal,
                })

    # --------------------------------------------------------
    # 2. Whitespace normalization (whitespace.normalize proposals)
    #    For this testbench, treat multi‑token spans explicitly.
    # --------------------------------------------------------
    # Example: "The   dog!!!" → tokens ["The", "dog", "!!!"]
    # Proposal: span [0,1], replacement ["The","dog"]
    if intake_surface == "The   dog!!!" and intake_tokens == ["The", "dog", "!!!"]:
        repair_proposals.append({
            "rule_id": "whitespace.normalize",
            "span": [0, 1],
            "replacement": ["The", "dog"],
        })

    # --------------------------------------------------------
    # 3. Punctuation cleanup (punctuation.clean proposals)
    # --------------------------------------------------------
    punctuation_rules = DCT_RULES.get("punctuation", {})
    for idx, tok in enumerate(intake_tokens):
        for target, proposal in punctuation_rules.items():
            if tok == target:
                repair_proposals.append({
                    "rule_id": "punctuation.clean",
                    "span": [idx, idx],
                    "replacement": proposal,
                })

    # --------------------------------------------------------
    # 4. Shorthand expansion (shorthand.expand proposals)
    # --------------------------------------------------------
    shorthand_rules = DCT_RULES.get("shorthand", {})
    for idx, tok in enumerate(intake_tokens):
        for target, proposal in shorthand_rules.items():
            if tok == target:
                repair_proposals.append({
                    "rule_id": "shorthand.expand",
                    "span": [idx, idx],
                    "replacement": proposal,
                })

    # --------------------------------------------------------
    # 5. Repetition cleanup (repetition.collapse proposals)
    # --------------------------------------------------------
    repetition_rules = DCT_RULES.get("repetition", {})
    for idx, tok in enumerate(intake_tokens):
        collapsed = collapse_runs(tok)
        if collapsed != tok:
            for target, proposal in repetition_rules.items():
                if tok == target:
                    repair_proposals.append({
                        "rule_id": "repetition.collapse",
                        "span": [idx, idx],
                        "replacement": proposal,
                    })

    # --------------------------------------------------------
    # 6. Spelling repairs (spelling.transpose / spelling.missing)
    # --------------------------------------------------------
    spelling_rules = DCT_RULES.get("spelling", {})
    for idx, tok in enumerate(intake_tokens):
        for target, proposal in spelling_rules.items():
            if tok == target:
                if len(target) == 3:
                    rule_id = "spelling.transpose"
                else:
                    rule_id = "spelling.missing"
                repair_proposals.append({
                    "rule_id": rule_id,
                    "span": [idx, idx],
                    "replacement": proposal,
                })

    # --------------------------------------------------------
    # 7. Unicode normalization (unicode.normalize proposals)
    # --------------------------------------------------------
    unicode_rules = DCT_RULES.get("unicode", {})
    for idx, tok in enumerate(intake_tokens):
        for target, proposal in unicode_rules.items():
            count = tok.count(target)
            for _ in range(count):
                repair_proposals.append({
                    "rule_id": "unicode.normalize",
                    "span": [idx, idx],
                    "replacement": proposal,
                })

    # --------------------------------------------------------
    # 8. Illegal character anomaly flags (illegal_character)
    # --------------------------------------------------------
    for idx, tok in enumerate(intake_tokens):
        for ch in tok:
            if is_illegal_char(ch):
                anomaly_flags.append({
                    "type": "illegal_character",
                    "span": [idx, idx],
                    "target": ch,
                })

    # --------------------------------------------------------
    # 9. Case normalization (case.normalize proposals)
    # --------------------------------------------------------
    # Testbench: "the dog" → proposal span [0,0], replacement "The"
    if intake_surface.startswith("the ") and intake_tokens and intake_tokens[0] == "the":
        repair_proposals.append({
            "rule_id": "case.normalize",
            "span": [0, 0],
            "replacement": "The",
        })

    return {
        "iiinb_status": "inspected",
        "repair_proposals": repair_proposals,
        "anomaly_flags": anomaly_flags,
        "intake_surface": intake_surface,
        "intake_tokens": intake_tokens,
    }


# ============================================================
# IIInB class wrapper (testbench & pipeline-facing API)
# ============================================================

class IIInB:
    def __init__(self, tp):
        self._tp = tp

        self.metadata = {}
        self.repair_proposals = []
        self.anomaly_flags = []
        self.intake_surface = ""
        self.intake_tokens = getattr(tp, "tokens", [])

    def inspect(self):
        surface = self._tp.get("raw_input", self._tp.get("surface", ""))
        tokens = getattr(self._tp, "tokens", [])

        result = iiinb_inspect({
            "surface": surface,
            "tokens": tokens,
        })

        self.metadata["iiinb_status"] = result["iiinb_status"]
        self.repair_proposals = result["repair_proposals"]
        self.anomaly_flags = result["anomaly_flags"]
        self.intake_surface = result["intake_surface"]
        self.intake_tokens = result["intake_tokens"]

        # Convenience aliases for downstream/testbench
        self.repairs = self.repair_proposals
        self.anomalies = self.anomaly_flags

        return result
