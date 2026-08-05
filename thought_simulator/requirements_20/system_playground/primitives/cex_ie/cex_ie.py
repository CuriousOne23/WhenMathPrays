"""
cex_ie.py
CEx-IE primitive implementation (Python)
Aligned with 20.107.010 and cex_ie_py_struc_pgm.md.

CEx-IE:
- Copies IE tokens/flags/normalized_text
- Detects structural cue-phrases via cex_ie_cue_dictionary.yaml
- Derives structural hints (topic/intent/continuity/reference/register/politeness/direction/coherence/importance)
- Emits TP.cex.ie envelope deterministically
"""

import yaml
from pathlib import Path


# ------------------------------------------------------------
# Utility: load cue dictionary
# ------------------------------------------------------------
def load_cex_ie_cue_dictionary() -> dict:
    BASE_DIR = Path(__file__).parent
    DICT_DIR = BASE_DIR.parent / "dictionary"

    dict_path = DICT_DIR / "cex_ie_cue_dictionary.yaml"
    dict_path = dict_path.resolve()

    with dict_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ------------------------------------------------------------
# Utility: simple normalized text search
# ------------------------------------------------------------
def _contains_phrase(normalized_text: str, phrase: str) -> bool:
    return phrase.lower() in normalized_text.lower()


# ------------------------------------------------------------
# Cue detection
# ------------------------------------------------------------
def detect_cues(tokens, normalized_text, cue_dict):
    cues_cfg = cue_dict.get("cues", {})
    phrases = []

    # Continuity
    cont = cues_cfg.get("continuity", {})
    for key, plist in cont.items():
        for p in plist:
            if _contains_phrase(normalized_text, p):
                phrases.append(f"continuity_{key}")
                break

    # Reference
    ref = cues_cfg.get("reference", {})
    for key, plist in ref.items():
        for p in plist:
            if _contains_phrase(normalized_text, p):
                phrases.append(f"reference_{key}")
                break

    # Intent
    intent = cues_cfg.get("intent", {})
    for key, plist in intent.items():
        for p in plist:
            if _contains_phrase(normalized_text, p):
                phrases.append(f"intent_{key}")
                break

    # Topic
    topic = cues_cfg.get("topic", {})
    for key, plist in topic.items():
        for p in plist:
            if _contains_phrase(normalized_text, p):
                phrases.append(f"topic_{key}")
                break

    # Direction
    direction = cues_cfg.get("direction", {})
    for key, plist in direction.items():
        for p in plist:
            if _contains_phrase(normalized_text, p):
                phrases.append(f"direction_{key}")
                break

    # Politeness
    politeness = cues_cfg.get("politeness", {})
    for key, plist in politeness.items():
        for p in plist:
            if _contains_phrase(normalized_text, p):
                phrases.append(f"politeness_{key}")
                break

    # Register
    register = cues_cfg.get("register", {})
    for key, plist in register.items():
        for p in plist:
            if _contains_phrase(normalized_text, p):
                phrases.append(f"register_{key}")
                break

    # Importance
    importance = cues_cfg.get("importance", {})
    for key, plist in importance.items():
        for p in plist:
            if _contains_phrase(normalized_text, p):
                phrases.append(f"importance_{key}")
                break

    return list(dict.fromkeys(phrases))  # preserve order, remove duplicates


# ------------------------------------------------------------
# Hint derivation
# ------------------------------------------------------------
def derive_hints(tokens, token_flags, normalized_text,
                 structural_phrases, tags, spans, markup, repairs):
    # Defaults
    topic_hint = "other"
    intent_hint = "none"
    continuity_hint = "continue"
    reference_hint = "none"
    register_hint = "none"
    politeness_hint = "none"
    direction_hint = "none"
    coherence_hint = "stable"
    importance_hint = "low"

    # Topic
    if any(p.startswith("topic_greeting") for p in structural_phrases):
        topic_hint = "greeting"
    elif any(p.startswith("topic_assistance") for p in structural_phrases):
        topic_hint = "assistance"
    elif any(p.startswith("topic_system") for p in structural_phrases):
        topic_hint = "system"
    elif any(p.startswith("topic_noise") for p in structural_phrases):
        topic_hint = "noise"
    elif any(p.startswith("topic_misc") for p in structural_phrases):
        topic_hint = "misc"

    # Intent
    if any(p.startswith("intent_request") for p in structural_phrases):
        intent_hint = "request"
    elif any(p.startswith("intent_inform") for p in structural_phrases):
        intent_hint = "inform"
    elif any(p.startswith("intent_begin") for p in structural_phrases):
        intent_hint = "begin"

    # Continuity
    if any(p.startswith("continuity_reset") for p in structural_phrases):
        continuity_hint = "reset"
    elif any(p.startswith("continuity_shift") for p in structural_phrases):
        continuity_hint = "shift"
    elif any(p.startswith("continuity_continue") for p in structural_phrases):
        continuity_hint = "continue"

    # Reference
    if any(p.startswith("reference_specific_previous") for p in structural_phrases):
        reference_hint = "specific_previous"
    elif any(p.startswith("reference_previous") for p in structural_phrases):
        reference_hint = "previous"
    elif any(p.startswith("reference_ambiguous_previous") for p in structural_phrases):
        reference_hint = "ambiguous_previous"

    # Register
    if any(p.startswith("register_casual") for p in structural_phrases):
        register_hint = "casual"
    elif any(p.startswith("register_formal") for p in structural_phrases):
        register_hint = "formal"
    elif any(p.startswith("register_informal") for p in structural_phrases):
        register_hint = "informal"

    # Politeness
    if any(p.startswith("politeness_high") for p in structural_phrases):
        politeness_hint = "high"
    elif any(p.startswith("politeness_normal") for p in structural_phrases):
        politeness_hint = "normal"

    # Direction
    if any(p.startswith("direction_forward") for p in structural_phrases):
        direction_hint = "forward"
    elif any(p.startswith("direction_backward") for p in structural_phrases):
        direction_hint = "backward"

    # Coherence: if anomalies/repairs present, mark unstable
    anomaly_spans = [s for s in spans if "anomaly" in s.get("type", "")]
    if anomaly_spans or repairs:
        coherence_hint = "unstable"

    # Importance
    if any(p.startswith("importance_high") for p in structural_phrases):
        importance_hint = "high"
    elif any(p.startswith("importance_medium") for p in structural_phrases):
        importance_hint = "medium"
    else:
        importance_hint = "low"

    return {
        "topic_hint": topic_hint,
        "intent_hint": intent_hint,
        "continuity_hint": continuity_hint,
        "reference_hint": reference_hint,
        "register_hint": register_hint,
        "politeness_hint": politeness_hint,
        "direction_hint": direction_hint,
        "coherence_hint": coherence_hint,
        "importance_hint": importance_hint,
    }


# ------------------------------------------------------------
# Primitive class
# ------------------------------------------------------------
class CExIE:
    def __init__(self, tp: dict):
        """
        tp: full TP envelope before CEx-IE (dict with TP.intake, TP.structure, TP.metadata)
        """
        self.tp = tp
        self.output = {"cex": {"ie": {}}}

    def inspect(self):
        # 1. Receive IE fields
        intake = self.tp.get("intake", {})
        structure = self.tp.get("structure", {})
        metadata = self.tp.get("metadata", {})

        tokens = intake.get("ie_tokens", [])
        token_flags = intake.get("token_flags", [])
        normalized = intake.get("normalized_text", "")

        tags = structure.get("tags", [])
        spans = structure.get("spans", [])
        markup = structure.get("markup", [])

        repairs = metadata.get("repair_annotations", [])

        # 2. Load cue dictionary
        cue_dict = load_cex_ie_cue_dictionary()

        # 3. Detect structural cue-phrases
        structural_phrases = detect_cues(tokens, normalized, cue_dict)

        # 4. Derive hint fields
        hints = derive_hints(tokens, token_flags, normalized,
                             structural_phrases, tags, spans, markup, repairs)

        # 5. Construct TP.cex.ie envelope
        self.output["cex"]["ie"] = {
            "tokens": tokens,
            "token_flags": token_flags,
            "normalized_text": normalized,
            "structural_phrases": structural_phrases,
            **hints,
        }

        return self.output

