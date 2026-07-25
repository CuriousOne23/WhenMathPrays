"""
IE Intake Envelope Testbench — Path A
Supports standalone and progressive execution.
Configuration is passed from run.py via set_testbench_config().
"""

import os
import yaml
import unittest
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
# Pipeline Harness (simple version for IE testbench)
# ---------------------------------------------------------------------------

class PipelineHarness:
    def __init__(self, cfg):
        self.use_inb = cfg.get("use_inb", False)
        self.use_iiinb = cfg.get("use_iiinb", False)
        self.use_ie = cfg.get("use_ie", True)

    def run(self, tp: ThoughtPacket):
        # InB
        if self.use_inb:
            tp = InB(tp)
        else:
            tp.metadata["inb_status"] = "accepted"  # stub

        # IIInB
        if self.use_iiinb:
            tp = IIInB(tp)
        else:
            tp.metadata["iiinb_status"] = "inspected"  # stub

        # IE
        if self.use_ie:
            tp = IE(tp)
        else:
            tp.metadata["ie_status"] = "normalized"  # stub

        return tp

# ---------------------------------------------------------------------------
# Testbench Class (unittest-compatible)
# ---------------------------------------------------------------------------

class TestIE(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.testbench = load_testbench()
        cls.tests = cls.testbench.get("tests", [])
        print(f"Loaded {len(cls.tests)} IE intake envelope test cases.\n")

        # Build harness from run.py configuration
        cls.harness = PipelineHarness(CONFIG)

    def test_ie_cases(self):
        expect_failure = CONFIG.get("expect_failure", False)

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

            # Execute pipeline via harness
            tp = self.harness.run(tp)

            # Expected values
            expected_inb_status = test.get("expected_inb_status", "accepted")
            expected_iiinb_status = test.get("expected_iiinb_status", "inspected")
            expected_ie_status = test.get("expected_ie_status", "normalized")
            expected_repairs = test.get("expected_repairs", [])

            if test.get("expected_long_input", False):
                expected_normalized = raw_input
            else:
                expected_normalized = test.get("expected_normalized", tp.raw_input)

            # Checks
            inb_ok = (tp.metadata.get("inb_status") == expected_inb_status)
            iiinb_ok = (tp.metadata.get("iiinb_status") == expected_iiinb_status)
            ie_ok = (tp.metadata.get("ie_status") == expected_ie_status)
            repairs_ok = (tp.repairs == expected_repairs)
            normalized_ok = (tp.normalized == expected_normalized)

            passed = inb_ok and iiinb_ok and ie_ok and repairs_ok and normalized_ok

            # ------------------------------------------------------------
            # EXPECTATION LOGIC (from run.py)
            # ------------------------------------------------------------
            if expect_failure:
                # User expects failure → test passes if pipeline FAILED
                if passed:
                    print("FAIL (Fail, no failure detected)")
                else:
                    print("PASS (Fail detected as expected)")
                self.assertFalse(passed, f"Test should have failed: {name}")

# ---------------------------------------------------------------------------
# Main (only used when running directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
