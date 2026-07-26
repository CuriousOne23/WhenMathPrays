"""
IE Intake Envelope Testbench — Path A
Updated version: removes user_expects_failure logic entirely.

Supports:
    • standalone vs progressive pipeline
    • per-test selection (User inputs "Yes" or "No")
    • upstream toggles (InB, IIInB, IE)
    • absolute PASS/FAIL per test (no expected-failure mode)
"""

import os
import yaml
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Global configuration (populated by run.py)
# ---------------------------------------------------------------------------

CONFIG = {}

def set_testbench_config(cfg):
    """Called by run.py to inject configuration."""
    global CONFIG
    CONFIG = cfg

# ---------------------------------------------------------------------------
# Thought Packet (TP) structure (simplified for IE-only testing)
# ---------------------------------------------------------------------------

@dataclass
class ThoughtPacket:
    raw_input: str
    inb_status: str = None
    iiinb_status: str = None
    ie_status: str = None
    repairs: list = field(default_factory=list)
    normalized: str = None

# ---------------------------------------------------------------------------
# Dummy IE primitive (placeholder for real implementation)
# ---------------------------------------------------------------------------

def run_ie(tp: ThoughtPacket):
    """
    Placeholder IE implementation.
    Normalizes whitespace, cleans punctuation, and sets status.
    """
    text = tp.raw_input.strip()

    # Whitespace normalization
    while "  " in text:
        text = text.replace("  ", " ")

    # Punctuation cleanup
    if text.endswith("!!!"):
        text = text[:-2] + "!"

        tp.repairs.append("punctuation.cleaned")

    tp.normalized = text
    tp.ie_status = "normalized"
    return tp

# ---------------------------------------------------------------------------
# Testbench runner
# ---------------------------------------------------------------------------

def run_testbench():

    yaml_path = os.path.join(
        os.path.dirname(__file__),
        "ie_testbench.yaml"
    )

    with open(yaml_path, "r") as f:
        tb = yaml.safe_load(f)

    tests = tb.get("tests", [])

    print("Loaded {} IE tests from YAML".format(len(tests)))
    print("Pipeline mode:", CONFIG.get("mode"))
    print("Upstream toggles:", CONFIG.get("use_inb"), CONFIG.get("use_iiinb"), CONFIG.get("use_ie"))
    print()

    for test in tests:

        test_id = test.get("id")
        run_flag = CONFIG["tests_to_run"].get(test_id, "No")

        if run_flag != "Yes":
            print(f"[SKIP] {test_id}")
            continue

        print(f"[RUN ] {test_id} — {test.get('description')}")

        # Build TP
        tp = ThoughtPacket(
            raw_input=test.get("input"),
            inb_status=test.get("expected_inb_status"),
            iiinb_status=test.get("expected_iiinb_status")
        )

        # Run IE (standalone mode)
        if CONFIG.get("use_ie"):
            tp = run_ie(tp)

        # Compare results
        expected_ie_status = test.get("expected_ie_status")
        expected_repairs = test.get("expected_repairs", [])
        expected_normalized = test.get("expected_normalized")

        status_ok = (tp.ie_status == expected_ie_status)
        repairs_ok = (tp.repairs == expected_repairs)
        normalized_ok = (tp.normalized == expected_normalized)

        if status_ok and repairs_ok and normalized_ok:
            print(f"  PASS — {test_id}\n")
        else:
            print(f"  FAIL — {test_id}")
            print(f"    Expected status: {expected_ie_status}, got: {tp.ie_status}")
            print(f"    Expected repairs: {expected_repairs}, got: {tp.repairs}")
            print(f"    Expected normalized: {expected_normalized}, got: {tp.normalized}\n")
