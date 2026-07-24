"""
IE Intake Envelope Testbench — Path A
Runs: InB → IIInB → IE
Designed to be executed by run.py
"""

import os
import yaml
import unittest
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Thought Packet (TP) structure
# ---------------------------------------------------------------------------

@dataclass
class ThoughtPacket:
    raw_input: str
    metadata: dict = field(default_factory=dict)
    defects: list = field(default_factory=list)
    repairs: list = field(default_factory=list)
    normalized: str = ""

# ---------------------------------------------------------------------------
# Primitive stubs (replace with real implementations later)
# ---------------------------------------------------------------------------

def InB(tp: ThoughtPacket):
    tp.metadata["inb_status"] = "accepted"
    return tp

def IIInB(tp: ThoughtPacket):
    tp.metadata["iiinb_status"] = "inspected"
    tp.defects = []  # clean path default
    return tp

def IE(tp: ThoughtPacket):
    tp.metadata["ie_status"] = "normalized"
    tp.normalized = tp.raw_input
    tp.repairs = []  # clean path default
    return tp

# ---------------------------------------------------------------------------
# Testbench Loader
# ---------------------------------------------------------------------------

def load_testbench():
    yaml_path = os.path.join(
        os.path.dirname(__file__),
        "ie_testbench.yaml"
    )
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Testbench Class (unittest-compatible)
# ---------------------------------------------------------------------------

class TestIE(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.testbench = load_testbench()
        cls.tests = cls.testbench.get("tests", [])
        print(f"Loaded {len(cls.tests)} IE intake envelope test cases.\n")

    def test_ie_cases(self):
        for test in self.tests:
            name = test.get("id", "unnamed")
            print(f"Running: {name} ...", end=" ")

            # Generate long input if requested
            if test.get("generate_long_input", False):
                length = test.get("long_length", 5000)
                raw_input = "A" * length
            else:
                raw_input = test["input"]

            tp = ThoughtPacket(raw_input=raw_input)

            # Execute primitives
            tp = InB(tp)
            tp = IIInB(tp)
            tp = IE(tp)

            # Expected values
            expected_inb_status = test.get("expected_inb_status", "accepted")
            expected_iiinb_status = test.get("expected_iiinb_status", "inspected")
            expected_ie_status = test.get("expected_ie_status", "normalized")
            expected_repairs = test.get("expected_repairs", [])
            expected_normalized = test.get("expected_normalized", tp.raw_input)

            # Checks
            inb_ok = (tp.metadata.get("inb_status") == expected_inb_status)
            iiinb_ok = (tp.metadata.get("iiinb_status") == expected_iiinb_status)
            ie_ok = (tp.metadata.get("ie_status") == expected_ie_status)
            repairs_ok = (tp.repairs == expected_repairs)
            normalized_ok = (tp.normalized == expected_normalized)

            passed = inb_ok and iiinb_ok and ie_ok and repairs_ok and normalized_ok

            print("PASS" if passed else "FAIL")

            self.assertTrue(passed, f"Test failed: {name}")

# ---------------------------------------------------------------------------
# Main (only used when running directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
