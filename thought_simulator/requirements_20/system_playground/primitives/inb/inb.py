"""
InB — Intake Normalization Basin (Path‑A)
Compliant with:
- inb_py_struc_pgm.md
- 20.100_inb_requirements.md
- 20.105 TP Requirements
- Architecture Scaffold 20.15
- run.py
- inb_testbench.yaml
"""

from thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_rulechecker import validate_inb

def InB(tp_dict):
    """
    InB receives and returns a TP envelope dictionary.

    Required TP input fields:
        tp_dict["raw_input"]
        tp_dict.get("tokens", [])

    Required TP output fields:
        {
            "surface": <str>,
            "defects": <list>,
            "tokens": <list>,
            "metadata": {
                "inb_status": <"accepted"|"degraded">,
                "intake_audit": <list>,
                "signature_history": <list>
            }
        }
    """

    # ------------------------------------------------------------
    # Extract required intake fields
    # ------------------------------------------------------------
    raw = tp_dict.get("raw_input", "")
    tokens = tp_dict.get("tokens", [])

    defects = []
    audit = []

    # ------------------------------------------------------------
    # Minimal deterministic defect detection (InB_v1)
    # ------------------------------------------------------------

    # 1. Empty input
    if raw == "":
        defects.append("empty.input")
        audit.append({"reason": "empty.input"})

    # 2. Excess whitespace
    if "  " in raw:
        defects.append("whitespace.excess")
        audit.append({"reason": "whitespace.excess"})

    # 3. Excess punctuation
    if "!!!" in raw:
        defects.append("punctuation.excess")
        audit.append({"reason": "punctuation.excess"})

    # 4. Unicode invalid (replacement char)
    if "�" in raw:
        defects.append("unicode.invalid")
        audit.append({"reason": "unicode.invalid"})

    # 5. Structural malformed (literal match)
    if "<broken>" in raw:
        defects.append("structural.malformed")
        audit.append({"reason": "structural.malformed"})

    # ------------------------------------------------------------
    # Metadata construction (deterministic, replay‑safe)
    # ------------------------------------------------------------
    metadata = tp_dict.get("metadata", {})
    metadata.setdefault("signature_history", []).append("inb_v2")
    metadata["intake_audit"] = audit
    metadata["inb_status"] = "accepted" if not defects else "degraded"

    # ------------------------------------------------------------
    # Construct primitive output envelope (pre‑rulechecker)
    # ------------------------------------------------------------
    output = {
        "surface": raw,
        "defects": defects[:],   # copy for safety
        "tokens": tokens,
        "metadata": metadata,
        "raw_input": raw         # required by rulechecker
    }

    # ------------------------------------------------------------
    # Apply rulechecker (InB_v2 enhancement)
    # ------------------------------------------------------------
    rule_defects = validate_inb(output)

    # Merge primitive + rulechecker defects deterministically
    merged = sorted(set(output["defects"] + rule_defects))
    output["defects"] = merged

    # Update degraded/accepted status
    output["metadata"]["inb_status"] = "accepted" if not merged else "degraded"

    return output
