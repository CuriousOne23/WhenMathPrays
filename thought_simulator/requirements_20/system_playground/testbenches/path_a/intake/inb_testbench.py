"""
InB Intake Testbench — Path A
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
        "inb_testbench.yaml"
    )
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Testbench Class (unittest-compatible)
# ---------------------------------------------------------------------------

class TestInBIntake(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.testbench = load_testbench()
        cls.tests = cls.testbench.get("tests", [])
        print(f"Loaded {len(cls.tests)} InB intake test cases.\n")

    def test_inb_cases(self):
        for test in self.tests:
            print("\nDEBUG RAW TEST ENTRY:", test)   # <‑‑ ADD THIS
        
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
            expected_defects = test.get("expected_defects", [])
            expected_repairs = test.get("expected_repairs", [])
            expected_normalized = test.get("expected_normalized", tp.raw_input)

            # Checks
            defects_ok = (tp.defects == expected_defects)
            repairs_ok = (tp.repairs == expected_repairs)
            normalized_ok = (tp.normalized == expected_normalized)

            passed = defects_ok and repairs_ok and normalized_ok

            print("DEBUG CHECKS:", {
                "defects_ok": defects_ok,
                "repairs_ok": repairs_ok,
                "normalized_ok": normalized_ok,
                "tp.defects": tp.defects,
                "expected_defects": expected_defects,
                "tp.repairs": tp.repairs,
                "expected_repairs": expected_repairs,
                "tp.normalized": tp.normalized,
                "expected_normalized": expected_normalized,
            })

            print("PASS" if passed else "FAIL")
            
            self.assertTrue(passed, f"Test failed: {name}")

# ---------------------------------------------------------------------------
# Main (only used when running directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
