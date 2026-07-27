"""
InB Intake Testbench — Path A
Runs: InB only
Designed to be executed by run.py
"""

import os
import yaml
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Thought Packet (TP) structure
# ---------------------------------------------------------------------------

@dataclass
class ThoughtPacket:
    raw_input: str
    messy_input_record: str = ""
    defects: list = field(default_factory=list)
    repairs: list = field(default_factory=list)
    normalized: str = ""
    metadata: dict = field(default_factory=dict)

# ---------------------------------------------------------------------------
# Import REAL InB primitive
# ---------------------------------------------------------------------------

from thought_simulator.requirements_20.system_playground.primitives.inb.inb import InB

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
# Configuration injection (required by run.py)
# ---------------------------------------------------------------------------

CONFIG = {}

def set_testbench_config(config_dict):
    global CONFIG
    CONFIG = config_dict

# ---------------------------------------------------------------------------
# Development-mode runner (no unittest)
# ---------------------------------------------------------------------------

def run_testbench():

    testbench = load_testbench()
    tests = testbench.get("tests", [])

    print(f"\nLoaded {len(tests)} InB intake test cases.\n")

    for test in tests:

        name = test.get("id", "unnamed")
        print(f"Running: {name} ...", end=" ")

        # Generate long input if requested
        if test.get("generate_long_input", False):
            length = test.get("long_length", 5000)
            raw_input = "A" * length
        else:
            raw_input = test["input"]

        tp = ThoughtPacket(raw_input=raw_input)

        # Execute REAL InB primitive
        tp = InB(tp)

        # Expected values
        expected_defects = test.get("expected_defects", [])
        expected_failure = test.get("expected_failure", False)

        # Checks
        defects_ok = (tp.defects == expected_defects)
        passed = defects_ok

        # ------------------------------------------------------------------
        # Requirement-aware PASS/FAIL messaging
        # ------------------------------------------------------------------
        if passed:
            if expected_failure:
                print(f"EXPECTED FAILURE — {name}")
                print("PASS: This test case contains known defects. A failure was expected and the system behaved correctly.\n")
            else:
                print(f"PASS — {name}\n")
        else:
            if expected_failure:
                print(f"UNEXPECTED PASS — {name}")
                print("FAIL: This test case contains known defects, but the system did not detect them.\n")
            else:
                print(f"UNEXPECTED FAILURE — {name}")
                print("FAIL: This test case should have passed. The failure indicates a real defect in the system.\n")
