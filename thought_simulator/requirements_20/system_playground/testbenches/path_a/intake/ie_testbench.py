"""
IE Intake Envelope Testbench — Path A
Three‑test version to validate flow before expanding to full 7 tests.
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
    tp.defects = []
    return tp

def IE(tp: ThoughtPacket):
    tp.metadata["ie_status"] = "normalized"
    tp.normalized = tp.raw_input
    tp.repairs = []
    return tp

# ---------------------------------------------------------------------------
# Load YAML testbench
# ---------------------------------------------------------------------------

def load_testbench():
    yaml_path = os.path.join(
        os.path.dirname(__file__),
        "ie_testbench.yaml"
    )
    with open(yaml_path, "r", encoding="utf-8") as f:
        full_yaml = yaml.safe_load(f)

    # Only keep first 3 tests
    trimmed = full_yaml.get("tests", [])[:3]
    return trimmed

# ---------------------------------------------------------------------------
# Pipeline Harness
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
            tp.metadata["inb_status"] = "accepted"

        # IIInB
        if self.use_iiinb:
            tp = IIInB(tp)
        else:
            tp.metadata["iiinb_status"] = "inspected"

        # IE
        if self.use_ie:
            tp = IE(tp)
        else:
            tp.metadata["ie_status"] = "normalized"

        return tp

# ---------------------------------------------------------------------------
# Testbench Class
# ---------------------------------------------------------------------------

class TestIE(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tests = load_testbench()
        print(f"Loaded {len(cls.tests)} IE test cases (3‑test mode).\n")
        cls.harness = PipelineHarness(CONFIG)

    def test_ie_cases(self):
        expect_failure = CONFIG.get("expect_failure", False)

        for test in self.tests:
            name = test.get("id", "unnamed")
            print(f"Running: {name} ...", end=" ")

            raw_input = test["input"]
            tp = ThoughtPacket(raw_input=raw_input)

            # Execute pipeline
            tp = self.harness.run(tp)

            # Expected values
            expected_inb_status = test.get("expected_inb_status", "accepted")
            expected_iiinb_status = test.get("expected_iiinb_status", "inspected")
            expected_ie_status = test.get("expected_ie_status", "normalized")
            expected_repairs = test.get("expected_repairs", [])
            expected_normalized = test.get("expected_normalized", raw_input)

            # Checks
            inb_ok = (tp.metadata.get("inb_status") == expected_inb_status)
            iiinb_ok = (tp.metadata.get("iiinb_status") == expected_iiinb_status)
            ie_ok = (tp.metadata.get("ie_status") == expected_ie_status)
            repairs_ok = (tp.repairs == expected_repairs)
            normalized_ok = (tp.normalized == expected_normalized)

            passed = inb_ok and iiinb_ok and ie_ok and repairs_ok and normalized_ok

            # ------------------------------------------------------------
            # EXPECTATION LOGIC (log only)
            # ------------------------------------------------------------
            if expect_failure:
                if passed:
                    print("FAIL, Expectation (Fail, no failure detected)")
                else:
                    print("PASS, Expectation (Fail, failure detected)")
            else:
                if passed:
                    print("PASS, Expectation (Pass, clean result)")
                else:
                    print("FAIL, Expectation (Pass, primitive reported failure)")

            # ------------------------------------------------------------
            # unittest asserts primitive truth ONLY
            # ------------------------------------------------------------
            self.assertTrue(passed, f"Primitive reported failure: {name}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
