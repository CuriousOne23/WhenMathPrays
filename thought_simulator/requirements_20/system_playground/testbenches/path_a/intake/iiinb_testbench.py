"""
IIInB Intake Inspection Testbench — Path A
Runs: InB → IIInB
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

from thought_simulator.requirements_20.system_playground.primitives.iiinb.iiinb import IIInB

# ---------------------------------------------------------------------------
# Testbench Loader
# ---------------------------------------------------------------------------

def load_testbench():
    yaml_path = os.path.join(
        os.path.dirname(__file__),
        "iiinb_testbench.yaml"
    )
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Testbench Class (unittest-compatible)
# ---------------------------------------------------------------------------

class TestIIInB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.testbench = load_testbench()
        cls.tests = cls.testbench.get("tests", [])
        print(f"Loaded {len(cls.tests)} IIInB intake inspection test cases.\n")

    def test_iiinb_cases(self):
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

            # Expected values
            expected_inb_status = test.get("expected_inb_status", "accepted")
            expected_iiinb_status = test.get("expected_iiinb_status", "inspected")
            expected_repairs = test.get("expected_repairs", [])
            expected_normalized = test.get("expected_normalized", raw_input)

            # Checks
            inb_ok = (tp.metadata.get("inb_status") == expected_inb_status)
            iiinb_ok = (tp.metadata.get("iiinb_status") == expected_iiinb_status)
            repairs_ok = (tp.repairs == expected_repairs)
            normalized_ok = (tp.normalized == expected_normalized)

            passed = inb_ok and iiinb_ok and repairs_ok and normalized_ok

            print("PASS" if passed else "FAIL")

            self.assertTrue(passed, f"Test failed: {name}")

# ---------------------------------------------------------------------------
# Main (only used when running directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
