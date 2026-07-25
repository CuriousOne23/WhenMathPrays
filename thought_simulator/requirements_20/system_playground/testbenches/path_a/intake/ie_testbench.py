"""
IE Intake Envelope Testbench — Path A
Three-test version to validate flow before expanding to full 7 tests.

Supports:
    • standalone vs progressive pipeline
    • per-test selection (User inputs "Yes" or "No")
    • per-test expectation (User inputs True or False)
    • upstream toggles (InB, IIInB, IE)
    • development-mode full execution (no early exit)
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

    return full_yaml.get("tests", [])

# ---------------------------------------------------------------------------
# Pipeline Harness
# ---------------------------------------------------------------------------

class PipelineHarness:
    def __init__(self, cfg):
        self.use_inb = cfg.get("use_inb", False)
        self.use_iiinb = cfg.get("use_iiinb", False)
        self.use_ie = cfg.get("use_ie", True)

    def run(self, tp: ThoughtPacket):
        if self.use_inb:
            tp = InB(tp)
        else:
            tp.metadata["inb_status"] = "accepted"

        if self.use_iiinb:
            tp = IIInB(tp)
        else:
            tp.metadata["iiinb_status"] = "inspected"

        if self.use_ie:
            tp = IE(tp)
        else:
            tp.metadata["ie_status"] = "normalized"

        return tp

# ---------------------------------------------------------------------------
# Development-mode Testbench Runner
# ---------------------------------------------------------------------------

def run_testbench():
    tests = load_testbench()
    print("Loaded {} IE test cases.\n".format(len(tests)))

    harness = PipelineHarness(CONFIG)

    tests_to_run = CONFIG.get("tests_to_run", {})
    expect_map = CONFIG.get("user_expects_failure", {})

    primitive_failures = []

    for test in tests:
        test_id = test.get("id", "unnamed")

        # Skip tests marked "No"
        if tests_to_run.get(test_id, "No") != "Yes":
            print("Skipping: {} (tests_to_run = No)".format(test_id))
            continue

        print("Running: {} ... ".format(test_id), end="")

        user_expects_failure = expect_map.get(test_id, False)

        tp = ThoughtPacket(raw_input=test["input"])
        tp = harness.run(tp)

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

        # Expectation logic

        # ------------------------------------------------------------
        # EXPECTATION LOGIC (log only)
        # ------------------------------------------------------------
        # User semantics:
        #   user_expects_failure = True  → user expects primitive FAIL
        #   user_expects_failure = False → user expects primitive PASS
        
        user_expects_pass = not user_expects_failure   # True → expect PASS, False → expect FAIL
        
        if passed == user_expects_pass:
            # User expectation satisfied
            if passed:
                print("PASS, Expectation (Pass, clean result)")
            else:
                print("PASS, Expectation (Fail, failure detected)")
        else:
            # User expectation violated
            if passed:
                print("FAIL, Expectation (Pass, no failure detected)")
            else:
                print("FAIL, Expectation (Fail, primitive reported failure)")

        # Development-mode primitive failure logging
        if not passed:
            primitive_failures.append(test_id)

    # Final summary
    print("\n=== Primitive Failure Summary ===")
    if len(primitive_failures) == 0:
        print("All selected tests passed primitive correctness.\n")
    else:
        print("Primitive failures detected in:")
        for tid in primitive_failures:
            print("  - {}".format(tid))
        print()

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_testbench()
