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
    repairs: list = field(default_factory=list)
    anomalies: list = field(default_factory=list)
    tokens: list = field(default_factory=list)
    structure: dict = field(default_factory=dict)
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
                raw_input = test.get("input", "")

            tp = ThoughtPacket(raw_input=raw_input)

            # Execute primitives
            tp = InB(tp)
            tp = IIInB(tp)

            # Expected block (new YAML structure)
            expected = test.get("expected", {})

            expected_inb_status = expected.get("inb_status", "accepted")
            expected_iiinb_status = expected.get("iiinb_status", "inspected")
            expected_repairs = expected.get("repair_operations", [])
            expected_anomalies = expected.get("anomaly_flags", [])
            expected_normalized = expected.get("normalized", raw_input)
            expected_tokens = expected.get("tokens", None)
            expected_structure = expected.get("structure", None)

            # Checks
            inb_ok = (tp.metadata.get("inb_status") == expected_inb_status)
            iiinb_ok = (tp.metadata.get("iiinb_status") == expected_iiinb_status)
            repairs_ok = (tp.repairs == expected_repairs)
            anomalies_ok = (tp.anomalies == expected_anomalies)
            normalized_ok = (tp.normalized == expected_normalized)

            tokens_ok = True
            if expected_tokens is not None:
                tokens_ok = (tp.tokens == expected_tokens)

            structure_ok = True
            if expected_structure is not None:
                structure_ok = (tp.structure == expected_structure)

            passed = (
                inb_ok and iiinb_ok and repairs_ok and anomalies_ok and
                normalized_ok and tokens_ok and structure_ok
            )

            print("PASS" if passed else "FAIL")
            self.assertTrue(passed, f"Test failed: {name}")

# ---------------------------------------------------------------------------
# Main (only used when running directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
