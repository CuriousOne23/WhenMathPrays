import re

def IE(tp):
    """
    Minimal IE primitive for intake testbench alignment.
    Performs:
      - whitespace normalization
      - punctuation cleanup
      - unicode cleanup
      - structural token cleanup
      - applies bounded repairs
      - sets ie_status = "normalized"
    """

    text = tp.normalized  # output from IIInB

    tp.metadata["ie_status"] = "normalized"
    tp.repairs = []

    # 1. Whitespace normalization
    new_text = re.sub(r"\s+", " ", text).strip()
    if new_text != text:
        tp.repairs.append({
            "op": "normalize_whitespace",
            "target": text,
            "replacement": new_text,
            "rule_id": "ie.normalize.whitespace",
        })
        text = new_text

    # 2. Punctuation cleanup (example: remove stray commas)
    new_text = re.sub(r"\s+,", ",", text)
    if new_text != text:
        tp.repairs.append({
            "op": "cleanup_punctuation",
            "target": text,
            "replacement": new_text,
            "rule_id": "ie.cleanup.punctuation",
        })
        text = new_text

    # 3. Unicode cleanup (remove invalid unicode)
    if "�" in text:
        new_text = text.replace("�", "")
        tp.repairs.append({
            "op": "cleanup_unicode",
            "target": "�",
            "replacement": "",
            "rule_id": "ie.cleanup.unicode",
        })
        text = new_text

    # 4. Structural token cleanup
    if "<broken>" in text:
        new_text = text.replace("<broken>", "")
        tp.repairs.append({
            "op": "cleanup_structural",
            "target": "<broken>",
            "replacement": "",
            "rule_id": "ie.cleanup.structural",
        })
        text = new_text

    tp.normalized = text
    return tp

