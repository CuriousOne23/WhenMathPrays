from dataclasses import dataclass, field


@dataclass
class ThoughtPacket:
    raw_input: str
    messy_input_record: str = ""
    defects: list = field(default_factory=list)
    repairs: list = field(default_factory=list)
    normalized: str = ""
    metadata: dict = field(default_factory=dict)


def InB(tp: ThoughtPacket) -> ThoughtPacket:
    """
    InB — Intake Buffer (20.100 + 20.15 aligned, minimal first pass)

    - Reads:  tp.raw_input
    - Writes: tp.messy_input_record
              tp.defects
              tp.metadata["inb_status"]
              tp.metadata["intake_audit"]
              tp.metadata["signature_history"]
    """

    raw = tp.raw_input
    tp.messy_input_record = raw

    defects = []
    audit = []

    # Empty input
    if raw == "":
        defects.append("empty.input")
        audit.append({"reason": "empty.input"})

    # Excess whitespace (simple heuristic: double spaces)
    if "  " in raw:
        defects.append("whitespace.excess")
        audit.append({"reason": "whitespace.excess"})

    # Excess punctuation (simple heuristic: triple exclamation)
    if "!!!" in raw:
        defects.append("punctuation.excess")
        audit.append({"reason": "punctuation.excess"})

    # Unicode noise
    if "�" in raw:
        defects.append("unicode.invalid")
        audit.append({"reason": "unicode.invalid"})

    # Structural malformed tokens
    if "<broken>" in raw:
        defects.append("structural.malformed")
        audit.append({"reason": "structural.malformed"})

    tp.defects = defects

    # Minimal metadata writes
    tp.metadata.setdefault("signature_history", []).append("inb_v1")
    tp.metadata["intake_audit"] = audit
    tp.metadata["inb_status"] = "accepted" if not defects else "degraded"

    return tp
