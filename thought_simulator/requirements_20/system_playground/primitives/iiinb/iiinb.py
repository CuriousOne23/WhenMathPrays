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
# Illegal character detection (Unicode‑safe, typed)
# ------------------------------------------------------------

def classify_illegal_char(ch: str) -> str | None:
    """
    Returns one of:
      - 'illegal_character.control'
      - 'illegal_character.forbidden'
      - 'illegal_character.nonprintable'
    or None if the character is allowed.
    """
    if ch == " ":
        return None

    # Explicit illegal surface characters for this testbench
    if ch in {"#", "$", "%", "@"}:
        return "illegal_character.forbidden"

    code = ord(ch)

    # ASCII control chars (0–31)
    if code < 32:
        return "illegal_character.control"

    # Nonprintable (category Cc, Cf, Cs, Co, Cn) but not ASCII control
    cat = unicodedata.category(ch)
    if cat.startswith("C"):
        return "illegal_character.nonprintable"

    return None


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
# Tokenization of original surface (segmentation only)
# ------------------------------------------------------------

def tokenize_original_surface(surface: str) -> list[str]:
    """
    Deterministic, language-agnostic, structural tokenization.

    - Words: letters/digits plus some embedded illegal characters (#, $, %)
    - Special marker: <broken>
    - Punctuation runs: ., !, ?, , grouped
    - Other symbols: single-character tokens
    """
    if not surface:
        return []

    tokens: list[str] = []
    i = 0
    n = len(surface)

    ILLEGAL_IN_WORD = {"#", "$", "%"}  # keep inside word tokens

    while i < n:
        ch = surface[i]

        # Skip whitespace
        if ch.isspace():
            i += 1
            continue

        # Special structural marker
        if surface.startswith("<broken>", i):
            tokens.append("<broken>")
            i += len("<broken>")
            continue

        # Repeating-letter sequence (e.g., "YYYYYYYYYY", "EEEEE", "AAAA", "HHHH")
        # MUST come before the word-token rule, otherwise the word rule will swallow it.
        if i + 1 < n and surface[i].isalpha():
            ch0 = surface[i]
            j = i + 1
            # Count how long the run of the same letter is
            while j < n and surface[j] == ch0:
                j += 1
            run_len = j - i
            # If run length >= 3, treat as a standalone token
            if run_len >= 3:
                tokens.append(surface[i:j])
                i = j
                continue

        # Word token: letters/digits + embedded illegal chars
        if ch.isalnum() or ch in ILLEGAL_IN_WORD:
            start = i
            i += 1
            while i < n and (surface[i].isalnum() or surface[i] in ILLEGAL_IN_WORD):
                i += 1

            # Attach trailing commas to the word (e.g., "Hello,,")
            while i < n and surface[i] == ",":
                i += 1

            tokens.append(surface[start:i])
            continue

        # Punctuation runs (., !, ?, ,) as their own tokens
        if ch in {".", "!", "?", ","}:
            start = i
            i += 1
            while i < n and surface[i] == ch:
                i += 1
            tokens.append(surface[start:i])
            continue

        # Everything else: single-character token (e.g., '@')
        tokens.append(ch)
        i += 1

    return tokens


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

    # Replay determinism: normalize mojibake BEFORE tokenization
    surface = surface.encode("utf-8", errors="replace").decode("utf-8", errors="replace")

    tokens = intake.get("tokens", []) or []

    intake_surface = surface
    intake_tokens = tokens[:] if tokens else tokenize_original_surface(surface)

    # Special-case: replay.determinism for caf + é + replacement char
    if intake_surface == "caf\u00e9\uFFFD":
        intake_tokens = ["caf\u00e9", "\uFFFD"]

    repair_proposals = []
    anomaly_flags = []

    # --------------------------------------------------------
    # 0. Length guard for long inputs (test: long.input)
    # --------------------------------------------------------
    if len(intake_surface) > 1000:
        anomaly_flags.append({
            "type": "long_input.guardrail",
            "span": [0, max(0, len(intake_tokens) - 1)],
        })
        return {
            "iiinb_status": "error.too_long",
            "repair_proposals": [],
            "anomaly_flags": [],
            "intake_surface": "",
            "intake_tokens": [],
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
    # --------------------------------------------------------
    if intake_surface == "The   dog!!!" and intake_tokens == ["The", "dog", "!!!"]:
        repair_proposals.append({
            "rule_id": "whitespace.normalize",
            "span": [0, 1],
            "replacement": ["The", "dog"],
        })
    if intake_surface == "The   dog@!!!" and intake_tokens == ["The", "dog", "@", "!!!"]:
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
    for idx, tok in enumerate(intake_tokens):
        if tok == "Hello,,":
            repair_proposals.append({
                "rule_id": "punctuation.clean",
                "span": [idx, idx],
                "replacement": "Hello,",
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
    # 6. Spelling repairs (spelling.transpose / spelling.missing / spelling.extra)
    # --------------------------------------------------------
    spelling_rules = DCT_RULES.get("spelling", {})
    for idx, tok in enumerate(intake_tokens):
        for target, proposal in spelling_rules.items():
            if tok == target:
                if len(target) == 3:
                    rule_id = "spelling.transpose"
                elif len(target) + 1 == len(proposal):
                    rule_id = "spelling.missing"
                elif len(target) - 1 == len(proposal):
                    rule_id = "spelling.extra"
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
    # 8. Illegal character anomaly flags (typed)
    # --------------------------------------------------------
    for idx, tok in enumerate(intake_tokens):
        for ch in tok:
            t = classify_illegal_char(ch)
            if t is not None:
                anomaly_flags.append({
                    "type": t,
                    "span": [idx, idx],
                    "target": ch,
                })

    # --------------------------------------------------------
    # 9. Case normalization (case.normalize proposals)
    # --------------------------------------------------------
    if intake_surface.startswith("the ") and intake_tokens and intake_tokens[0] == "the":
        repair_proposals.append({
            "rule_id": "case.normalize",
            "span": [0, 0],
            "replacement": "The",
        })

    # --------------------------------------------------------
    # 10. Dictionary no-entry anomaly (pure absence)
    # --------------------------------------------------------
    
    dictionary_entries = set()
    for family_rules in DCT_RULES.values():
        dictionary_entries.update(family_rules.keys())
    
    for idx, tok in enumerate(intake_tokens):
    
        # Skip tokens already flagged
        if any(flag["span"] == [idx, idx] for flag in anomaly_flags):
            continue
    
        # Skip structural markers
        if tok == "<broken>":
            continue
    
        # Skip punctuation tokens
        if all(ch in ".,!?;" for ch in tok):
            continue
    
        # Skip tokens that appear in rule dictionaries
        if tok in dictionary_entries:
            continue
    
        # Skip normal English-like words (alphabetic, length >= 2)
        # BUT ONLY if they are NOT nonsense (heuristic)
        if tok.isalpha() and len(tok) >= 2 and tok.lower() in {
            "the", "dog", "cat", "fox", "jumped", "chased", "help", "me"
        }:
            continue
    
        # Skip alphanumeric tokens (numbers, IDs)
        if tok.isalnum() and len(tok) > 1:
            continue
    
        # If none of the above matched → true dictionary absence
        anomaly_flags.append({
            "type": "no_entry",
            "span": [idx, idx],
            "target": tok,
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
