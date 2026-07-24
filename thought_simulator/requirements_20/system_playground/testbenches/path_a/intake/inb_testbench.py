"""
inb_testbench.py
TS Path A — Intake Testbench Driver
Executes: InB → IIInB → IE

- Terminal output: short PASS/FAIL summary
- Log file output: full detailed trace (ignored by .gitignore)
"""

import yaml
import os
import datetime
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

def load_testbench(yaml_path: str):
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Test Execution
# ---------------------------------------------------------------------------

def run_test_case(test):
    name = test.get("name", "unnamed")

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

    print("PASS" if passed else "FAIL")

# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main():
    yaml_path = os.path.join(
        os.path.dirname(__file__),
        "inb_testbench.yaml"
    )

    testbench = load_testbench(yaml_path)
    tests = testbench.get("tests", [])

    print(f"Loaded {len(tests)} test cases.")
    print("Starting InB → IIInB → IE testbench...\n")

    for test in tests:
        run_test_case(test)   # <-- no log argument

    print("\nAll tests complete.")

if __name__ == "__main__":
    main()
